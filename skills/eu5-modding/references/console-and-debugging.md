# Console, Debug Mode, Hotloading, Logs, Script Documentation, and Save Editing

## Enabling Debug Mode

Launch with `-debug_mode`. Three ways:

1. **Steam** → right-click *Europa Universalis V* → Properties → General → Launch Options → add `-debug_mode`.
2. **Windows without Steam** → create a shortcut to `binaries/eu5.exe` and append ` -debug_mode` to the Target field.
3. **Mods** that toggle debug mode in-game work for console commands but do not enable file hotloading.

Debug mode adds:

- Console window and debug menus (GUI Editor, Script Explorer, Data Types Explorer, Texture Viewer).
- Extended debug tooltips on the map.
- Ctrl-click a country to take control of it; Ctrl-Alt-click a state.
- A **file watcher** that reloads changed mod files into memory without restarting.
- An in-game **error log button** showing the current line count, which opens `error.log`.
- Text-format save files instead of packed ones.

Disabling debug mode: activate achievements again by disabling all mods, removing `-debug_mode`, restarting, and confirming the checksum shown in the main-menu corner.

## Opening the Console

Press the layout-dependent key. On QWERTY: `` ` ``. Alternatives: `~`, `^`, `§`, `°`, `2`, `Shift+2`, `Alt+2+1`, `Shift+3`. `Alt+C` or `Shift+Alt+C` when none work.

- `↑`/`↓` traverses history.
- `Tab` autocompletes or lists matches.
- Many commands toggle by repeating; some need a save reload or restart.

## Logs and Generated Documentation

| Artifact | Location |
|----------|----------|
| `error.log` | `Documents/Paradox Interactive/Europa Universalis V/logs/error.log` |
| `system.log`, `debug.log` | same `logs/` folder |
| `script_docs` output | `Documents/Paradox Interactive/Europa Universalis V/docs/` |
| `dump_data_types` output | `Documents/Paradox Interactive/Europa Universalis V/logs/data_types/` |
| Settings | `Documents/Paradox Interactive/Europa Universalis V/pdx_settings.json` |
| Saves (local) | `Documents/Paradox Interactive/Europa Universalis V/save games/` |
| Saves (Proton) | `steamapps/compatdata/3450310/pfx/drive_c/users/steamuser/Documents/.../save games` |
| Cloud saves backup | `<steam>/userdata/<steam id>/3450310/remote/save games` |
| Baked map data | `Documents/Paradox Interactive/Europa Universalis V/baked_streaming_data/` |

`error.log` is the primary signal. A silent no-op effect or trigger is almost always a wrong scope or an unknown key recorded there.

### Configuring the log editor

Edit `pdx_settings.json` and add under `System`:

```json
"editor": "C:/Program Files/Sublime Text/sublime_text.exe",
"editor_postfix": ":$:1"
```

`editor_postfix` opens the editor scrolled to the last line (Sublime-specific). Alternatively use the in-game console → Settings → System → Editor.

## Core Commands

| Command | Alias | Purpose |
|---------|-------|---------|
| `script_docs` | `script_documentation` | Dump all effects, triggers, scope links, event targets, modifier types |
| `dump_data_types` | `DumpDataTypes` | Dump GUI data types, functions, and promotes |
| `data_types_explorer` | — | Browse GUI data types in-game |
| `Log.ClearErrorLog` | — | Truncate `error.log` without leaving the game |
| `Log.ClearAll` | — | Clear every log |
| `log` | — | Change log channels; see the wiki for arguments |
| `Localization.ToggleIncludeKeyInLocOutput` | — | Show localisation keys with text (debug) |
| `Localization.ToggleOnlyKeyInLocOutput` | — | Render only localisation keys |
| `Script.Profiling.Start` / `.Stop` / `.Restart` / `.Dump` / `.DumpAll` | — | Profile script cost per subsystem |
| `memory_stats` / `io_stats` / `net_stats` / `3dstats` | `memstats` etc. | Runtime counters |
| `textureviewer`, `texturelist`, `drawcmdsviewer`, `tools.skins` | — | Graphics inspection |
| `Session.GetEnabledDLCs` | — | List active DLC |
| `FullSettings` | — | Dump the full settings tree |
| `Threading.TaskThreadCount` | — | Change the task thread count |

Game-state commands commonly used while developing: `event`, `run` (execute a script file), `kill`, `annex`, `tag`, `add_gold`, `declare_war`, `peace`, `activate_situation`, `end_situation`, `fire_disaster`, `embrace_institution`, `add_advance`, `gu`/`goto` for camera teleports. The full list is on the wiki's `Console commands` page and in-game autocomplete.

## Launch Options

| Option | Purpose |
|--------|---------|
| `-debug_mode` | Console, debug menus, hotloading, text saves |
| `-map_editor` | Launch the map editor |
| `--ignore-disable-mods-on-crash` | Prevent the game from disabling all mods after a resource-load crash, so the same playset is reloaded for debugging |
| `-leavepops` | Disable starting-population recalculation, so defined pop counts are used verbatim for testing |
| `-develop` | Enable developer-mode extras where present |

## Hotloading

The file watcher reloads changed mod files automatically. Known limits:

- Most `.txt`, `.gui`, and script files reload.
- `on_action` files are **not** reliably hotloaded; restart after editing them.
- Some changes to `setup/` require a new game session; the start data is built once per campaign.
- Baked map data and `.dds` textures may need a restart or a `reload` variant from the console.

## Save-Game Editing

Debug-mode saves are text files in the same `name=value` format used by mod files. Packed saves are compressed and need a tool.

**Header line**: `SAV` + 2-digit version (`02`) + `00` (debug/text) or `03` (packed) + ID/checksum digits + `0004` (text) or `0006` (packed) + checksum digits + eight zeros.

Value types in text saves:
- Keywords (`blue`), quoted strings (`"Spain"`), integers, fixed-point numbers (always 5 decimals), dates (`1464.5.18` or `1464.5.18.12`), arrays `{ a b c }`, mappings `{ key=value }`.
- Nested arrays and mappings are permitted.
- A quote inside a quoted string is escaped with `\"`; embedded newlines are allowed.

Tools: **Pdx-Unlimiter** (`crschnick/pdx_unlimiter`) decodes any save format into a structured tree and can preview modded flags without launching the game.

Ironman saves are not covered by this format description.

## Debugging Workflow

1. Launch with `-debug_mode`.
2. Reproduce the issue.
3. Click the error deer to open `error.log`, or read it externally.
4. Filter recognisable error classes:
   - `Unknown effect` / `Unknown trigger` — name or version mismatch.
   - `Invalid scope` / `did not get a matching scope type` — scope chain misuse.
   - `Trigger section already read earlier` — duplicated singleton block from `INJECT:`.
   - `Duplicated key` — two definitions without `REPLACE:`.
   - `Duplicated event ID` — expected when redefining base-game events.
   - `fopen() failed: 2` and encoding messages — path or BOM problem.
   - `Malformed token` — a field value the installed schema rejects.
   - `Variable ... is used but is never set` — a variable setter exists only in unreachable script.
5. Run `script_docs` and `dump_data_types` after patching the game; keep the dumps as the local source of truth.
6. Use `Script.Profiling.Start` / `.Stop` / `.Dump` to find expensive script after a performance regression.
7. For a repeated crash during resource load, relaunch with `--ignore-disable-mods-on-crash` so the same mods load again.

## Troubleshooting Checklist

| Symptom | Check |
|---------|-------|
| Mod content has no effect | `.metadata/metadata.json` present; correct top folder; correct filename casing |
| Files fail to load with lexer error | Non-ASCII user path; file permissions; wrong BOM |
| Localisation shows raw keys | BOM present; `_l_<language>` suffix; correct language folder |
| Localisation changes ignored | Later-loaded key wins; move to `localization/<language>/replace/` |
| Event never fires | No on_action/`trigger_event`; trigger fails; duplicate ID lost to an earlier-loaded file |
| On_action additions ignored | Restated `trigger`/`effect` instead of an added `on_actions` block; on_action not hotloaded |
| GUI window invisible | Missing `gui/scripted_widgets/*.txt` registration; `visible` expression false |
| `INJECT:` has no effect | Target folder does not support entry modes; injecting into a sub-block |
| Repeated field replaces instead of adding | Price object semantics; use `REPLACE:` or operation-order tiebreak |
| Values truncated | More than 5 decimal places written |
| Ordered iterator processes one object | Missing explicit `max` |
| Whole-window GUI patch silently deletes another mod's controls | Merged from vanilla instead of the final downstream owner's file |