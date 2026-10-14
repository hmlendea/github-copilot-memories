const cryptoModule = require('node:crypto');
const fileSystem = require('node:fs');
const operatingSystem = require('node:os');
const pathModule = require('node:path');

const READ_ONLY_TOOL_PATTERN = /(ask|fetch|get|grep|list|read|search|todo|usage|view)/i;
const PROGRAMMING_FAMILIES = new Map([
    ['.cs', 'csharp'],
    ['.csproj', 'csharp'],
    ['.sln', 'csharp'],
    ['.slnx', 'csharp'],
    ['.ms', 'methodscript'],
    ['.msa', 'methodscript'],
    ['.py', 'python'],
    ['.sh', 'shell'],
    ['.ts', 'typescript'],
    ['.tsx', 'typescript']
]);
const IGNORED_DIRECTORY_NAMES = new Set([
    '.git',
    '.idea',
    '.vs',
    '.vscode',
    'bin',
    'build',
    'dist',
    'node_modules',
    'obj'
]);

function readStandardInput() {
    return new Promise((resolve, reject) => {
        let input = '';

        process.stdin.setEncoding('utf8');
        process.stdin.on('data', chunk => {
            input += chunk;
        });
        process.stdin.on('end', () => resolve(input));
        process.stdin.on('error', reject);
    });
}

function getStateFilePath(eventData) {
    const sessionIdentity = eventData.session_id
        || eventData.transcript_path
        || eventData.cwd
        || 'unknown-session';
    const sessionHash = cryptoModule
        .createHash('sha256')
        .update(sessionIdentity)
        .digest('hex');
    const cacheRoot = process.env.XDG_CACHE_HOME
        || pathModule.join(operatingSystem.homedir(), '.cache');

    return pathModule.join(cacheRoot, 'github-copilot-instruction-gate', `${sessionHash}.json`);
}

function getInstructionRoot() {
    return process.env.LITELLM_INSTRUCTION_ROOT
        || pathModule.resolve(__dirname, '..', 'prompts', 'instructions');
}

function listFiles(directoryPath) {
    if (!fileSystem.existsSync(directoryPath)) {
        return [];
    }

    return fileSystem.readdirSync(directoryPath, { withFileTypes: true })
        .flatMap(directoryEntry => {
            const entryPath = pathModule.join(directoryPath, directoryEntry.name);

            if (directoryEntry.isDirectory()) {
                return listFiles(entryPath);
            }

            return [entryPath];
        });
}

function collectWorkspaceFiles(directoryPath, workspaceRoot, workspaceFiles = []) {
    if (!directoryPath || !fileSystem.existsSync(directoryPath)) {
        return workspaceFiles;
    }

    for (const directoryEntry of fileSystem.readdirSync(directoryPath, { withFileTypes: true })) {
        if (directoryEntry.isDirectory() && IGNORED_DIRECTORY_NAMES.has(directoryEntry.name)) {
            continue;
        }

        const entryPath = pathModule.join(directoryPath, directoryEntry.name);

        if (directoryEntry.isDirectory()) {
            collectWorkspaceFiles(entryPath, workspaceRoot, workspaceFiles);
            continue;
        }

        workspaceFiles.push(pathModule.relative(workspaceRoot, entryPath).replaceAll('\\', '/'));
    }

    return workspaceFiles;
}

function splitGlobPatterns(applyToValue) {
    const patterns = [];
    let braceDepth = 0;
    let patternStart = 0;

    for (let characterIndex = 0; characterIndex < applyToValue.length; characterIndex += 1) {
        const character = applyToValue[characterIndex];

        if (character === '{') {
            braceDepth += 1;
        } else if (character === '}') {
            braceDepth -= 1;
        } else if (character === ',' && braceDepth === 0) {
            patterns.push(applyToValue.slice(patternStart, characterIndex).trim());
            patternStart = characterIndex + 1;
        }
    }

    patterns.push(applyToValue.slice(patternStart).trim());

    return patterns.filter(Boolean);
}

function getApplyToPatterns(instructionSource) {
    const sourceText = fileSystem.readFileSync(instructionSource, 'utf8');
    const quotedMatch = sourceText.match(/^applyTo:\s*(['"])(.*?)\1\s*$/m);
    const unquotedMatch = sourceText.match(/^applyTo:\s*([^'"\r\n]+)\s*$/m);
    const applyToValue = quotedMatch?.[2] || unquotedMatch?.[1];

    return applyToValue
        ? splitGlobPatterns(applyToValue)
            .map(applyToPattern => applyToPattern.replace(/\{([^,{}]+)\}/g, '$1'))
        : [];
}

function instructionAppliesToFiles(instructionSource, filePaths) {
    const applyToPatterns = getApplyToPatterns(instructionSource);

    return applyToPatterns.some(applyToPattern =>
        applyToPattern === '**'
        || filePaths.some(filePath => pathModule.matchesGlob(filePath, applyToPattern)));
}

function getCandidatePaths(value) {
    return collectStringValues(value)
        .flatMap(stringValue => stringValue.match(/[\w./\\-]+\.[A-Za-z0-9]+/g) || [])
        .map(filePath => filePath.replaceAll('\\', '/'));
}

function getAllInstructionSources() {
    return listFiles(getInstructionRoot())
        .filter(filePath => filePath.endsWith('.instructions.md'))
        .map(filePath => fileSystem.realpathSync(filePath));
}

function getInstructionFamily(instructionSource) {
    return pathModule.relative(getInstructionRoot(), instructionSource)
        .split(pathModule.sep)[0];
}

function getProgrammingFamilies(filePaths) {
    return new Set(filePaths
        .map(filePath => PROGRAMMING_FAMILIES.get(pathModule.extname(filePath).toLowerCase()))
        .filter(Boolean));
}

function getApplicableSources(filePaths, allowedFamilies) {
    return getAllInstructionSources()
        .filter(instructionSource =>
            (!allowedFamilies || allowedFamilies.has(getInstructionFamily(instructionSource)))
            && (pathModule.basename(instructionSource) === 'language.english.instructions.md'
                || instructionAppliesToFiles(instructionSource, filePaths)))
        .sort();
}

function getRequiredSources(eventData) {
    const workspaceFiles = collectWorkspaceFiles(eventData.cwd, eventData.cwd);
    const promptPaths = getCandidatePaths(eventData.prompt);
    const programmingFamilies = getProgrammingFamilies(workspaceFiles);
    const startupFamilies = new Set(['common', 'language', ...programmingFamilies]);

    return getApplicableSources([...workspaceFiles, ...promptPaths], startupFamilies);
}

function addRequiredSources(state, value) {
    const candidatePaths = getCandidatePaths(value);

    if (candidatePaths.length === 0) {
        return;
    }

    const additionalSources = getApplicableSources(candidatePaths);
    state.requiredSources = [...new Set([...state.requiredSources, ...additionalSources])].sort();
}

function buildInstructionContext(instructionSources) {
    const sourceSections = instructionSources.map(instructionSource => {
        const sourceText = fileSystem.readFileSync(instructionSource, 'utf8');

        return `## ${instructionSource}\n\n${sourceText}`;
    });

    return `Apply every instruction in the following sources to this task. These sources were supplied automatically by the LiteLLM hook.\n\n${sourceSections.join('\n\n')}`;
}

function readState(stateFilePath) {
    try {
        return JSON.parse(fileSystem.readFileSync(stateFilePath, 'utf8'));
    } catch (error) {
        if (error.code === 'ENOENT') {
            return { injectedSources: [], requiredSources: [] };
        }

        throw error;
    }
}

function writeState(stateFilePath, state) {
    fileSystem.mkdirSync(pathModule.dirname(stateFilePath), { recursive: true });
    fileSystem.writeFileSync(stateFilePath, `${JSON.stringify(state)}\n`, { mode: 0o600 });
}

function collectStringValues(value, collectedValues = []) {
    if (typeof value === 'string') {
        collectedValues.push(value);
    } else if (Array.isArray(value)) {
        value.forEach(item => collectStringValues(item, collectedValues));
    } else if (value && typeof value === 'object') {
        Object.values(value).forEach(item => collectStringValues(item, collectedValues));
    }

    return collectedValues;
}

function isDiscoveryTool(eventData) {
    return READ_ONLY_TOOL_PATTERN.test(eventData.tool_name || '');
}

function getMissingSources(state) {
    const injectedSources = new Set(state.injectedSources);

    return state.requiredSources.filter(filePath => !injectedSources.has(filePath));
}

function denyToolUse(missingSources) {
    return {
        hookSpecificOutput: {
            hookEventName: 'PreToolUse',
            permissionDecision: 'deny',
            permissionDecisionReason: 'New path-scoped instructions were injected. Re-evaluate the action against them before retrying.',
            additionalContext: buildInstructionContext(missingSources)
        }
    };
}

async function main() {
    const input = await readStandardInput();
    const eventData = JSON.parse(input);
    const stateFilePath = getStateFilePath(eventData);

    if (eventData.hook_event_name === 'SessionStart') {
        const requiredSources = getRequiredSources(eventData);
        writeState(stateFilePath, {
            injectedSources: requiredSources,
            requiredSources
        });
        process.stdout.write(JSON.stringify({
            hookSpecificOutput: {
                additionalContext: buildInstructionContext(requiredSources),
                hookEventName: 'SessionStart'
            }
        }));
        return;
    }

    const state = readState(stateFilePath);
    state.injectedSources ||= [];

    if (!Array.isArray(state.requiredSources) || state.requiredSources.length === 0) {
        state.requiredSources = getRequiredSources(eventData);
    }

    addRequiredSources(state, eventData.tool_input);

    if (eventData.hook_event_name === 'UserPromptSubmit') {
        addRequiredSources(state, eventData.prompt);
        writeState(stateFilePath, state);
        return;
    }

    const missingSources = getMissingSources(state);

    if (eventData.hook_event_name === 'PreToolUse'
        && missingSources.length > 0
        && !isDiscoveryTool(eventData)) {
        state.injectedSources = [...new Set([...state.injectedSources, ...missingSources])].sort();
        writeState(stateFilePath, state);
        process.stdout.write(JSON.stringify(denyToolUse(missingSources)));
    }
}

main().catch(error => {
    console.error(`[ERROR] Instruction gate failed: ${error.message}`);
    process.exit(2);
});
