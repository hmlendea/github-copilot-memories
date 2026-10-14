const cryptoModule = require('node:crypto');
const fileSystem = require('node:fs');
const operatingSystem = require('node:os');
const pathModule = require('node:path');

const READ_ONLY_TOOL_PATTERN = /(ask|fetch|get|grep|list|read|search|todo|usage|view)/i;
const INSTRUCTION_SOURCE_PATTERN = /(?:\.instructions\.md|\/SKILL\.md|\/AGENTS\.md|\/copilot-instructions\.md)$/i;

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

function readState(stateFilePath) {
    try {
        return JSON.parse(fileSystem.readFileSync(stateFilePath, 'utf8'));
    } catch (error) {
        if (error.code === 'ENOENT') {
            return { instructionSources: [], ready: false };
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

function recordsInstructionRead(eventData) {
    if (!/read/i.test(eventData.tool_name || '')) {
        return [];
    }

    return collectStringValues(eventData.tool_input)
        .filter(value => INSTRUCTION_SOURCE_PATTERN.test(value));
}

function isDiscoveryTool(eventData) {
    return READ_ONLY_TOOL_PATTERN.test(eventData.tool_name || '');
}

function denyToolUse() {
    return {
        hookSpecificOutput: {
            hookEventName: 'PreToolUse',
            permissionDecision: 'deny',
            permissionDecisionReason: 'Read every applicable instruction and skill file before using execution or editing tools.',
            additionalContext: 'The instruction gate is closed. Use discovery tools to read the applicable sources before retrying this action.'
        }
    };
}

async function main() {
    const input = await readStandardInput();
    const eventData = JSON.parse(input);
    const stateFilePath = getStateFilePath(eventData);

    if (eventData.hook_event_name === 'SessionStart'
        || eventData.hook_event_name === 'UserPromptSubmit') {
        writeState(stateFilePath, { instructionSources: [], ready: false });
        return;
    }

    const state = readState(stateFilePath);

    if (eventData.hook_event_name === 'PostToolUse') {
        const instructionSources = recordsInstructionRead(eventData);
        state.instructionSources = [...new Set([...state.instructionSources, ...instructionSources])];
        state.ready = state.instructionSources.length > 0;

        writeState(stateFilePath, state);
        return;
    }

    if (eventData.hook_event_name === 'PreToolUse' && !state.ready && !isDiscoveryTool(eventData)) {
        process.stdout.write(JSON.stringify(denyToolUse()));
    }
}

main().catch(error => {
    console.error(`[ERROR] Instruction gate failed: ${error.message}`);
    process.exit(2);
});
