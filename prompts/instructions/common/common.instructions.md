---
description: "Always-on instruction-source, file-editing, and repository-orientation safeguards."
applyTo: '**'
---

# Instruction Sources

"The instructions" means profile prompt files: Linux `~/.config/Code/User/prompts/`; macOS `~/Library/Application Support/Code/User/prompts/`; Windows `%APPDATA%\Code\User\prompts\`. Search there before requesting clarification.

## Location Registry

Before resolving any path or address, read the agent home `Locations.md` and use a recorded value when present. Other agents keep their registry at `Locations.md` in their own home directory.

| Agent | Linux | macOS | Windows |
|-------|-------|-------|---------|
| Codex | `~/.codex/Locations.md` or `$CODEX_HOME/Locations.md` | `~/.codex/Locations.md` or `$CODEX_HOME/Locations.md` | `%USERPROFILE%\.codex\Locations.md` or `%CODEX_HOME%\Locations.md` |
| GitHub Copilot | `~/.copilot/Locations.md` | `~/.copilot/Locations.md` | `%USERPROFILE%\.copilot\Locations.md` |

Applies to installed software, repository clones, documentation, configuration, data directories, and URLs.

## File Editing

- Read targets and applicable source material before modification.
- Existing files: update via `apply_patch`; never delete or recreate them.
- `create_file`: new files only.
- Failed patch: reread, then retry with smaller exact context. Stop and report after two failures.
- Never repeat an identical failed search. After two failed instruction-file searches, request its exact path.
