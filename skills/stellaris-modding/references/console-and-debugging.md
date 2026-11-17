# Console, Logging, and Debugging

## Enabling Debug Output

The console is always available in any non-ironman, non-multiplayer game. Launch options only affect logging verbosity and startup.

| Platform | How |
|----------|-----|
| Steam | Right-click Stellaris → Properties → Launch Options |
| Paradox Launcher | Game Settings tab |
| GOG | Settings → enable command-line arguments |

Useful arguments: `-debug_mode` (extra logging and additional tooltips), `-nolauncher` (skip the launcher), `-random`, and `-map=<galaxy shape>` when testing generation. `-debug_mode` does not open the console by itself; the console key does.

## Opening the Console

Key varies by layout: `` ` ``, `~`, `^`, `°`, `§`, `2`, `Shift+2`, `Alt+2+1`, `Shift+3`, or `Shift+Alt+C`.

- `↑`/`↓` cycle command history.
- The console is unavailable in ironman and multiplayer.
- Achievements cannot be earned in a game where any console command has been used.
- The console ships with on-screen menus for common commands.

## Reload Matrix

| Change | Command | Restart needed |
|--------|---------|----------------|
| `.gui` layout | `reload <file>.gui` | No |
| Textures via `.gfx` | `reload texture all`, or `reload texture <name>` | No (yes if the texture resolution changed) |
| Localisation | `reload text` | No |
| Shaders | `reloadfx <path>` | No |
| Scripts in a test file | `run <file>.txt` | No (recompiled every call) |
| Graphical map | `reload_graphical_map` | No |
| Events | `reloadevents` is **not implemented** — restart | Yes |
| `common/`, `defines`, initializers, galaxy setup | — | Yes (new game for map changes) |
| `interface/main.gui` and other structural GUI | — | Yes |

## Test-Driving Script

```
run my_test.txt          # file in the user data directory, executed in the player's scope
```

`run` recompiles the file on every call, so it is the fastest iterate–verify loop for effects and triggers.

## Diagnostic Commands

| Command | Purpose |
|---------|---------|
| `help` | Full command list |
| `help <command>` | Parameters for one command |
| `debugtooltip` | Adds IDs and internal data to tooltips |
| `guibounds` | Names the GUI element and file under the cursor |
| `debug_dumpevents` | Prints the fired event list |
| `debug_yesmen` / `debug_nomen` | Force AI acceptance or refusal |
| `observe` | Observer mode; reveals hidden traits and religions |
| `play <country id>` | Return from observer mode to a country |
| `reload_galaxy` | Start a new game immediately |
| `ai` | Toggle AI |
| `techupdate` | Re-roll current tech choices |

State manipulation used constantly while modding planets, empires, and wars: `cash`, `minerals`, `alloys`, `unity`, `influence`, `research_technologies`, `add_relic`, `add_trait_species`, `add_trait_leader`, `activate_ascension_perk`, `activate_tradition`, `add_pops`, `add_ship`, `create_megastructure`, `create_navy`, `colonize`, `own`, `survey`, `planet_size`, `add_time`, `event`, `effect`.

`effect <effect> = <params>` and `event <id> [target]` are the two most valuable commands: they let you fire any piece of script against the current selection without editing a mod file.

## Logs

Location: `<user data>/Stellaris/logs/` — one level above `mod/`.

| File | Contents |
|------|----------|
| `error.log` | Script errors, unknown effects/triggers, illegal scopes, missing localisation keys, missing sprites, duplicate keys |
| `game.log` | Startup, loading, and general runtime |
| `setup.log` | Galaxy/empire generation |
| `script_documentation/` | Generated dumps of effects, triggers, scopes, and localisation commands; `localizations.log` lists every bracket command |
| `data_types.log` | GUI data types |

Read `error.log` after every change. The **first** entry is the cause; the rest are usually cascades from an aborted block.

Typical errors and their meaning:

| Message | Cause |
|---------|-------|
| `Object key already exists` | Duplicate definition in a LIOS folder that also warns on duplicates — check the mod is not defining a vanilla key twice |
| `Object with key ... already exists, using the one at ...` | Benign LIOS override notice |
| `Unexpected token` / `Unknown trigger` | Typo, wrong patch, or effect used where a trigger belongs |
| `Invalid scope` | Effect or trigger illegal in the current scope |
| `Missing localization key` | Key absent in the active language |
| `Missing sprite` / `Could not find texture` | `.gfx` entry missing or `textureFile` path wrong |
| `Error: file not found` | Encoded path wrong, or file in the wrong folder |

## Debugging Workflow

1. Launch, start a game with only the target mod enabled.
2. Reproduce with the smallest possible content.
3. Read `error.log` first; do not guess from symptom behaviour.
4. If a trigger or effect seems ignored, check in order: scope legality, key spelling, patch availability, then merge type (LIOS vs FIOS).
5. Use `effect`/`event` in the console to isolate whether the problem is in the script or in the triggering path.
6. Reload what can be reloaded; restart for events, map, and defines.
7. Verify localisation with `reload text` and `toggle_string_id` before blaming script.
8. Before shipping, run once with no console use to confirm the mod behaves outside debug conditions.

## Data Dump Strategy

The wiki's effect, trigger, scope, and localisation tables are snapshots from older patches.
1. Open `logs/script_documentation/` for the installed build.
2. Grep for the name you need.
3. Confirm the supported scope and parameter list before use.

Treat those generated dumps as authoritative over the wiki and over recollection of another Paradox title's syntax.

## Tooling That Pays Off

| Tool | Why |
|------|-----|
| CWTools (VS Code / Sublime) | Live syntax and scope validation, autocomplete, missing-loc-key report |
| Paradox Syntax Highlighting | Brace and keyword readability |
| WinMerge / KDiff3 / L13 Diff | Re-merging copied vanilla files after each patch |
| Irony Mod Manager | Faster mod management and conflict solving across collections |
| GIMP / paint.net | `.dds` authoring |

CWTools is the closest thing to a compiler this engine has: enable it before writing volume script, not after.