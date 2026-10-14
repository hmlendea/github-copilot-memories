const assertModule = require('node:assert/strict');
const childProcess = require('node:child_process');
const fileSystem = require('node:fs');
const operatingSystem = require('node:os');
const pathModule = require('node:path');
const test = require('node:test');

const SCRIPT_PATH = pathModule.join(__dirname, 'litellm-instruction-gate.cjs');

function runHook(eventData, cacheDirectory, instructionRoot) {
    const result = childProcess.spawnSync(process.execPath, [SCRIPT_PATH], {
        encoding: 'utf8',
        env: {
            ...process.env,
            LITELLM_INSTRUCTION_ROOT: instructionRoot,
            XDG_CACHE_HOME: cacheDirectory
        },
        input: JSON.stringify(eventData)
    });

    assertModule.equal(result.status, 0, result.stderr);

    return result.stdout;
}

function createEvent(hookEventName, toolName, toolInput = {}, workingDirectory) {
    return {
        cwd: workingDirectory,
        hook_event_name: hookEventName,
        session_id: 'instruction-gate-test-session',
        tool_input: toolInput,
        tool_name: toolName
    };
}

function createInstructionSource(instructionRoot, familyName, fileName, applyTo) {
    const familyDirectory = pathModule.join(instructionRoot, familyName);
    const filePath = pathModule.join(familyDirectory, fileName);
    const applyToLine = applyTo ? `applyTo: '${applyTo}'\n` : '';
    fileSystem.mkdirSync(familyDirectory, { recursive: true });
    fileSystem.writeFileSync(
        filePath,
        `---\ndescription: Test instruction.\n${applyToLine}---\nRule.\n`);

    return filePath;
}

test('injects scoped instructions without repeated blocking', () => {
    const testDirectory = fileSystem.mkdtempSync(
        pathModule.join(operatingSystem.tmpdir(), 'litellm-instruction-gate-'));
    const cacheDirectory = pathModule.join(testDirectory, 'cache');
    const instructionRoot = pathModule.join(testDirectory, 'instructions');
    const workingDirectory = pathModule.join(testDirectory, 'workspace');
    const commonSource = createInstructionSource(
        instructionRoot, 'common', 'common.instructions.md', '**');
    const languageSource = createInstructionSource(
        instructionRoot, 'language', 'language.english.instructions.md');
    const csharpCodingSource = createInstructionSource(
        instructionRoot, 'csharp', 'csharp.coding.instructions.md', '**/*.cs');
    const csharpNamingSource = createInstructionSource(
        instructionRoot, 'csharp', 'csharp.naming.instructions.md', '**/*.cs');
    const csharpTestingSource = createInstructionSource(
        instructionRoot, 'csharp', 'csharp.testing.instructions.md', '**/*Tests.cs');
    const pythonSource = createInstructionSource(
        instructionRoot, 'python', 'python.coding.instructions.md', '**/*.py');
    fileSystem.mkdirSync(workingDirectory, { recursive: true });
    fileSystem.writeFileSync(pathModule.join(workingDirectory, 'Client.cs'), 'sealed class Client;\n');
    fileSystem.writeFileSync(pathModule.join(workingDirectory, 'ClientTests.cs'), 'sealed class ClientTests;\n');

    try {
        const injectedContext = runHook(
            createEvent('SessionStart', undefined, {}, workingDirectory),
            cacheDirectory,
            instructionRoot);
        assertModule.match(injectedContext, /common\.instructions\.md/);
        assertModule.match(injectedContext, /language\.english\.instructions\.md/);
        assertModule.match(injectedContext, /csharp\.coding\.instructions\.md/);
        assertModule.match(injectedContext, /csharp\.naming\.instructions\.md/);
        assertModule.match(injectedContext, /csharp\.testing\.instructions\.md/);

        const allowedAfterInjection = runHook(
            createEvent('PreToolUse', 'apply_patch', {}, workingDirectory),
            cacheDirectory,
            instructionRoot);
        assertModule.equal(allowedAfterInjection, '');

        const deniedForNewLanguage = runHook(
            createEvent('PreToolUse', 'create_file', {
                filePath: pathModule.join(workingDirectory, 'client.py')
            }, workingDirectory),
            cacheDirectory,
            instructionRoot);
        assertModule.match(deniedForNewLanguage, /python\.coding\.instructions\.md/);
        assertModule.match(deniedForNewLanguage, /"permissionDecision":"deny"/);

        runHook(
            createEvent('UserPromptSubmit', undefined, {}, workingDirectory),
            cacheDirectory,
            instructionRoot);

        const allowedForNewLanguage = runHook(
            createEvent('PreToolUse', 'create_file', {
                filePath: pathModule.join(workingDirectory, 'client.py')
            }, workingDirectory),
            cacheDirectory,
            instructionRoot);
        assertModule.equal(allowedForNewLanguage, '');

        const allowedAfterRecovery = runHook(
            createEvent('UserPromptSubmit', undefined, {}, workingDirectory),
            cacheDirectory,
            instructionRoot);
        assertModule.equal(allowedAfterRecovery, '');

        const allowedRepeatedAction = runHook(
            createEvent('PreToolUse', 'apply_patch', {}, workingDirectory),
            cacheDirectory,
            instructionRoot);
        assertModule.equal(allowedRepeatedAction, '');

        assertModule.ok(fileSystem.existsSync(commonSource));
        assertModule.ok(fileSystem.existsSync(languageSource));
        assertModule.ok(fileSystem.existsSync(csharpCodingSource));
        assertModule.ok(fileSystem.existsSync(csharpNamingSource));
        assertModule.ok(fileSystem.existsSync(csharpTestingSource));
        assertModule.ok(fileSystem.existsSync(pythonSource));
    } finally {
        fileSystem.rmSync(testDirectory, { force: true, recursive: true });
    }
});

test('recovers when SessionStart is unavailable', () => {
    const testDirectory = fileSystem.mkdtempSync(
        pathModule.join(operatingSystem.tmpdir(), 'litellm-instruction-gate-fallback-'));
    const cacheDirectory = pathModule.join(testDirectory, 'cache');
    const instructionRoot = pathModule.join(testDirectory, 'instructions');
    const workingDirectory = pathModule.join(testDirectory, 'workspace');
    createInstructionSource(instructionRoot, 'common', 'common.instructions.md', '**');
    createInstructionSource(instructionRoot, 'csharp', 'csharp.coding.instructions.md', '**/*.cs');
    fileSystem.mkdirSync(workingDirectory, { recursive: true });
    fileSystem.writeFileSync(pathModule.join(workingDirectory, 'Client.cs'), 'sealed class Client;\n');

    try {
        runHook(
            createEvent('UserPromptSubmit', undefined, {}, workingDirectory),
            cacheDirectory,
            instructionRoot);

        const initialDenial = runHook(
            createEvent('PreToolUse', 'apply_patch', {}, workingDirectory),
            cacheDirectory,
            instructionRoot);
        assertModule.match(initialDenial, /csharp\.coding\.instructions\.md/);
        assertModule.match(initialDenial, /"permissionDecision":"deny"/);

        runHook(
            createEvent('UserPromptSubmit', undefined, {}, workingDirectory),
            cacheDirectory,
            instructionRoot);

        const retryOutput = runHook(
            createEvent('PreToolUse', 'apply_patch', {}, workingDirectory),
            cacheDirectory,
            instructionRoot);
        assertModule.equal(retryOutput, '');
    } finally {
        fileSystem.rmSync(testDirectory, { force: true, recursive: true });
    }
});
