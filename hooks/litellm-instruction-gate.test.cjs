const assertModule = require('node:assert/strict');
const childProcess = require('node:child_process');
const fileSystem = require('node:fs');
const operatingSystem = require('node:os');
const pathModule = require('node:path');
const test = require('node:test');

const SCRIPT_PATH = pathModule.join(__dirname, 'litellm-instruction-gate.cjs');

function runHook(eventData, cacheDirectory) {
    const result = childProcess.spawnSync(process.execPath, [SCRIPT_PATH], {
        encoding: 'utf8',
        env: { ...process.env, XDG_CACHE_HOME: cacheDirectory },
        input: JSON.stringify(eventData)
    });

    assertModule.equal(result.status, 0, result.stderr);

    return result.stdout;
}

function createEvent(hookEventName, toolName, toolInput = {}) {
    return {
        hook_event_name: hookEventName,
        session_id: 'instruction-gate-test-session',
        tool_input: toolInput,
        tool_name: toolName
    };
}

test('blocks execution until instruction discovery is complete', () => {
    const cacheDirectory = fileSystem.mkdtempSync(
        pathModule.join(operatingSystem.tmpdir(), 'litellm-instruction-gate-'));

    try {
        runHook(createEvent('UserPromptSubmit'), cacheDirectory);

        const deniedBeforeRead = runHook(
            createEvent('PreToolUse', 'apply_patch'), cacheDirectory);
        assertModule.match(deniedBeforeRead, /"permissionDecision":"deny"/);

        runHook(createEvent('PostToolUse', 'read_file', {
            filePath: '/tmp/common.instructions.md'
        }), cacheDirectory);

        const allowedAfterRead = runHook(
            createEvent('PreToolUse', 'apply_patch'), cacheDirectory);
        assertModule.equal(allowedAfterRead, '');

        runHook(createEvent('UserPromptSubmit'), cacheDirectory);

        const deniedAfterReset = runHook(
            createEvent('PreToolUse', 'apply_patch'), cacheDirectory);
        assertModule.match(deniedAfterReset, /"permissionDecision":"deny"/);
    } finally {
        fileSystem.rmSync(cacheDirectory, { force: true, recursive: true });
    }
});
