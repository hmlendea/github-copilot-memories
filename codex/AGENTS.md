# Personal instructions

My reusable instruction library is located at:

`~/.codex/instructions` (or `$CODEX_HOME/instructions` when `CODEX_HOME` is set).

Before editing files:

1. Inspect the target file type and task.
2. Find instruction files whose `applyTo` pattern matches the target.
3. Also load relevant semantic instructions based on their `description`.
4. Follow the Markdown body, treating Copilot-specific tool names as equivalent
   Codex operations where appropriate.
5. Do not load unrelated instruction files.
