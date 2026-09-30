---
description: Describe when these instructions should be loaded by the agent based on task context
applyTo: '**'
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

## Repository Documentation
- Whenever it is required to understand how the repository is organised, how it works, what it represents, or where certain things are located, refer to:
  1. **`ARCHITECTURE.md`** if it exists in the repository.
  2. **`docs/`** directory if it exists in the repository.
  3. The **repository's GitHub Wiki** if it exists.

- Ensure repository-relative file and directory links in documentation are verified before inclusion.