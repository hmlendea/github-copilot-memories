---
description: Describe when these instructions should be loaded by the agent based on task context
# applyTo: 'Describe when these instructions should be loaded by the agent based on task context' # when provided, instructions will automatically be added to the request context when the pattern matches an attached file
---

When the user refers to "the instructions", they mean the instruction files in:

- Linux: ~/.config/Code/User/prompts/
- macOS: ~/Library/Application Support/Code/User/prompts/
- Windows: %APPDATA%\Code\User\prompts\

Treat those files as the primary source of project instructions. If you need clarification, search that directory before asking.

## Safety rules for editing files

- Never delete an existing file as a method of updating it.
- Never delete a target file before all required source material has been found and read.
- Prefer `apply_patch` for existing files.
- If a patch fails, reread the file and retry with smaller, exact-context patches.
- If two patch attempts fail, stop and explain the failure.
- Do not use `create_file` to replace an existing file.
- Do not repeat an identical unsuccessful search.
- After two failed searches for a referenced instruction file, stop and ask the user for its exact path.
- Never modify a file based on an instruction file that has not actually been read.