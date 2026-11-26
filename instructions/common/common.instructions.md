---
description: "Always-on instruction-source, file-editing, alphabetical-order, and repository-orientation safeguards."
applyTo: '**'
---

# Instruction Sources

"The instructions" means profile prompt files: Linux `~/.config/Code/User/prompts/instructions/`; macOS `~/Library/Application Support/Code/User/prompts/instructions/`; Windows `%APPDATA%\Code\User\prompts\instructions\`. Search there before requesting clarification.

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

## Alphabetical Order

- In any text, code, configuration, data, or documentation, when inserting an item into a list, enumeration, table, set of keys, or other sequence whose existing items are in alphabetical order, place the item at its alphabetical position so that the entire sequence remains in alphabetical order. Never append it out of order.
- Derive the ordering convention (sort key or column, case sensitivity, treatment of punctuation, prefixes, and articles) from the existing items, and apply that convention to the inserted item.
- When renaming an item in such a sequence, move it to its new alphabetical position.
