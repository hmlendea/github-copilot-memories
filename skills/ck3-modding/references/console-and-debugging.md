# Console, Debugging, Logs, and Data Dumps

## Enabling Debugging

Launch the game with `-debug_mode -develop` (`-develop` alone hot-reloads most files; both together open the console). On Steam use launch options; on Xbox Game Pass run `start shell:AppsFolder\ParadoxInteractive.ProjectTitus_zfnrdv2de78ny!App -debug_mode -develop`. Some files (events, defines, map setup, structural GUI in `interface/main.gui`) still need a restart; most reload on save.

The console is unavailable in ironman and multiplayer. Console commands disable **achievements for that session** even when they are purely diagnostic — if you ship a test that relies on console use, state that caveat to players rather than promising achievement compatibility.

## Scenario Launch Options

| Option | Purpose |
|--------|---------|
| `-debug_mode` | Debug tooltips, interactions, console |
| `-develop` | Hot reload of most files as they are saved |
| `-mapeditor` | Map editor |
| `-nographics` | Headless observer game |
| `-skip` | Skip the main menu, load character selection (1066) |
| `-continuelastsave` | Resume the last save |
| `-random_seed=42` | Fixed RNG seed; only useful with `-debug_mode` |
| `-benchmark` | Timed automated test; output goes to `timer_dump` logs |
| `-skipcounselor` | Skips counselors on new game |

`-play=e_hre`, `-play=d_apulia`, `-play=k_poland` start directly as the holder of the named title (title names from debug tooltips).

## Source Modding Workflow

Test-driven iteration:

```
run <file>.txt                    # file in the user data directory, executed in the player's scope
effect add_gold = 100             # run one effect against the current scope
trigger is_ai = yes               # evaluate one trigger against the current scope
event example.1                   # fire an event by namespace.id
explorer                          # object inspector; also open context menus to run effects/triggers
```

`run` recompiles on every call. Place your loop's body in `run/` next to your mod folder and iterate fast.

`script_docs` dumps the authoritative reference to `logs/`:

| File | What it carries |
|------|-----------------|
| `effects.log` | Every hardcoded effect: arguments and legal scopes |
| `triggers.log` | Every hardcoded trigger: parameters, scopes, targets |
| `modifiers.log` | Every modifier plus the object types it may modify |
| `event_scopes.log` | Every scope type |
| `event_targets.log` | Every event target with input/output scopes |
| `on_actions.log` | Every on_action with scope comments |
| `data_types.log` + `logs/data_types/` | GUI promote/function list from `dump_data_types` |
| `logs/data_types/*.txt` | Full data-type listing |

Treat the dumps for your installed patch as authoritative over the wiki; regenerate them every patch (`script_docs`, then `dump_data_types`).

## CK3 Tiger Validation

CK3 Tiger (VS Code extension `unlomtrois.ck3tiger-for-vscode`, also standalone) does static validation: unknown effects/triggers, illegal scopes, missing localisation keys, duplicate definitions. Run it while iterating; it surfaces errors before the game sees them. The Paradox Modding Toolkit / CWTools extensions are alternatives; CWTools is outdated and produces false positives.

## Logs

User-data locations:

| OS | Log path |
|----|----------|
| Windows | `Documents/Paradox Interactive/Crusader Kings III/logs/` |
| Linux/macOS | `~/.local/share/Paradox Interactive/Crusader Kings III/logs/` |

| File | Contents |
|------|----------|
| `error.log` | Script errors, unknown keys, illegal scopes, missing localisation, missing sprites, duplicates. **Read after every change.** The first entry is usually the cause; the rest are cascades from an aborted block |
| `debug.log` | General runtime |
| `setup.log` | Galaxy/province/title setup |
| `script_docs` output | see table above |
| `database_conflicts.log` | Footprint conflicts between active mods |
| `generated/` | Auto-regenerated map locator files; copy corrected copies back into `gfx/map/map_object_data/` |

Key read behaviours:

- Newer errors appear at the top of the console shaft; older at the bottom. Clear the console between iterations so you do not chase stale errors.
- Almost every in-game feature is silent on failure: an effect vanishes, a trigger fails to fire, nothing breaks the save. Always read `error.log` first; do not guess from behaviour.
- `error_log = "..."` and `debug_log = "..."` write to their respective logs from script — both support `[bracket]` text, so you can emit `ROOT.Char.GetName` triage data.
- `release_mode` shows the live Errorhoof error counter; equivalent to clicking the tracker button on the console.
- `log_viewer` opens the in-game log (error and debug together, filterable at the top).

## Save-Game Editing

> The wiki notes "this doesn't seem to work anymore"; the procedure below is historical documentation only.

Save files live in `.../save games/` (user data path). Debug-mode save, then edit the extracted `gamestate` file with a text editor (`unzip FileName.ck3`, edit, zip back). Ironman removes its flag via `ironman=yes` → `ironman=no` inside the extracted save. This is not reliable in current patches; prefer `run` scripts or console commands for state edits.

## Common Workflows

| Task | Steps |
|------|-------|
| New event | `events/my_event.txt`, `namespace = my_mod`, fire via on_action or `event my_mod.1`; check `error.log` |
| Change a trigger | Confirm in `triggers.log`; edit; relaunch if it lives in `common/` |
| Localisation missing | Check the UTF-8 BOM; confirm `l_<language>:` on the first line; `reload text` (missing keys appear in `error.log`) |
| GUI change | Edit `.gui` in the mod folder, save, watch hot reload; inspect the element with `tweak gui.debug` |
| Map change | `-mapeditor`, change heightmap/rivers/province map, **repack**, restart the editor; check locator alignment |
| Conflict between mods | `database_conflicts.log`; compatibility patch loaded after both; review each mod's `footprint` |
| Paradox Mods mod ignoring new files | Installed-manually workaround: unsubscribe, drain the Steam copy, install the unpacked folder manually |

## Tooling Worth Installing

| Tool | Purpose |
|------|---------|
| CK3 Tiger | Static validation of script (scopes, effects, triggers, localisation keys) |
| Paradox Modding Toolkit (VS Code) | Autocomplete, syntax highlighting, CK3 Tiger integration |
| CWTools | Syntax highlighting; outdated validation, false positives common |
| WinMerge / KDiff3 | Re-merge copied vanilla files after each patch |
| Irony Mod Manager | Manage mod collections and resolve load-order conflicts |
| CK3 Tiger for VS Code | real-time syntax validation integrated into the editor |
| FMOD Studio 1.10.20 | Sound event/bank authoring; neither sound nor music hot-reloads |
| GIMP with DDS plugin / Photoshop Intel plugin | `.dds` authoring for portraits, CoA emblems, GUI sprites |

## Honest Limits

- Every obscure bug is just as likely to be a wrong scope, a misspelled key, a patch-level change, or a `replace` localisation error as it is to be a broken install.
- Console commands disable achievements regardless of what the command does.
- `while` loops cap at 1000 iterations and cannot be broken out of.
- New `holding_types` cannot be added; holdings and buildings often require whole-file replacement.
- Map modding works per case: missing locators generate files in `generated/`; river maps with any non-vanilla colour CTD.
- Only one version of a mod may be installed (local vs Workshop vs Paradox Mods).
