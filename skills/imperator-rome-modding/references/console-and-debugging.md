# Console, Debugging, and Validation

## Enabling Development Mode

The console is disabled by default since patch 1.1. Launch with command-line arguments:

- `-debug_mode` — enables the console, changes the checksum, disables achievements.
- `-develop` / `-developer` — enables developer tools, including the GUI editor and editor-mode reloads.

Typical combined launch options: `-debug_mode -develop`.

Per platform:

- **Steam:** right-click the game → Properties → Launch Options → add the arguments.
- **Windows shortcut:** append to the Target field (outside the quotes).
- **GOG:** Settings → tick "Add command line arguments" → enter the flags.
- **GOG Galaxy 2.0:** duplicate the executable and add the flags to its Arguments field.

Vanilla provides no supported way to add hotkeys; extra convenience hotkeys require external tooling (e.g. AutoHotkey), not a mod.

## Opening the Console

Press `` ` `` (below Esc). If that fails, try `Shift+2`, `Alt+2+1`, `Shift+3`, `§`, `~`, `^`, `°`, or `2`.

- `↑` / `↓` cycle history; `Tab` autocompletes.
- Console commands are unavailable in ironman and multiplayer.
- The purple debug tooltip can be hidden with the community *Hide Debug Tooltip* mod.

## Reload Commands

| Change | Command | Restart required |
|--------|---------|------------------|
| `.gui` layout | `reload gui` | No |
| `.dds` texture | `reload texture` | No |
| Genes (`00_genes.txt`) | `reload genes` | No |
| Defines | automatic with `-debug_mode` | No |
| Script values | automatic with `-debug_mode` (some triggers go stale) | Sometimes |
| Scripted GUIs | — | **Yes** |
| Localisation | — | **Yes** |
| Map, province setup, countries, characters | — | **Yes** |

## Diagnostic Commands

| Command | Purpose |
|---------|---------|
| `script_docs` | Dump all effects, triggers, and scopes for the installed build into a log |
| `DumpDataTypes` | Dump GUI data types to `data_types.log` |
| `gui_editor` | Open the GUI editor |
| `portrait_editor` / `pe` | Open the Portrait Editor for DNA work |
| `help` | List console commands |
| `debug_mode`-dependent `aistats <tag>` | Write AI logs |
| `aiview` | Toggle the AI overlay |
| `3dstats` | Render statistics overlay |

Useful state manipulation while testing: `cash <n>`, `annex <tag>`, `army <count> <province>`, `ai <tag>`, `amnesia <tag>`, `centralization <n>`, `character.age <id> <age>`, `replay` (unlocks the unfinished timelapse).

The full command list is far larger than the wiki table; use `help` in-console or `https://commands.gg/imperator`.

## Logs

`<user data>/Imperator/logs/`:

- `error.log` — script errors, unknown effects/triggers, missing localisation keys, broken GUI references. **Read it after every change.** A script mistake is usually reported here rather than surfacing as a visible failure.
- `data_types.log` — GUI data functions, after `DumpDataTypes` or the corresponding editor action.
- `ai.log` — AI behaviour, after `aistats`.
- Generated script documentation from `script_docs`.

Log paths on Linux: `~/.local/share/Paradox Interactive/Imperator/logs/`.

## Debugging Workflow

1. Enable `-debug_mode -develop`, restart once.
2. Reproduce with the smallest possible mod content.
3. Read `error.log` — the first error is usually the cause; later errors are often cascades.
4. If a trigger or effect misbehaves silently, suspect the **scope** first, then the **key name**, then the **patch version**.
5. Verify localisation keys exist in every shipped language; a missing key shows the raw key in-game.
6. Reload what can be reloaded; restart for everything else.
7. Before publishing, launch once without `-debug_mode` to confirm the mod works in a normal session with achievements' checksum behaviour.

## Data Dump Strategy

The wiki's effect/trigger/scope tables were generated from `script_docs` for old versions. For any current-patch work:

1. Run `script_docs`.
2. Search the produced log for the effect or trigger name.
3. Confirm the supported scope and target columns before using it.

Treat this as the authority over wiki tables and over any memory of another Paradox title's syntax.