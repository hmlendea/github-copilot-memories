# Console, Logging, Validator, and Debugging

## Launch Options

Set these in Steam → Properties → Launch Options, or in the launcher's game settings:

| Argument | Effect |
|----------|--------|
| `-debug` | Enables the console and debug tooltips |
| `-debugscripts` | Extra script asserts in `error.log` and `game.log` |
| `-scriptlog` | Logs script errors without asserts |
| `-fullhistoricalsetuplog` | Writes `historical_setup_errors.log` |

Combine them as `-debug -debugscripts -scriptlog -fullhistoricalsetuplog` while developing; on Linux, pass them after `--` in the launch command.

The console is unavailable in ironman games. In other games it opens with `` ` ``, `§`, `^`, `~`, or `°` depending on keyboard layout.

## Log Files

Location: `<user data>/Crusader Kings II/logs/`. Files are truncated on every launch.

| File | Contents |
|------|----------|
| `error.log` | Parsing and loading errors; also asserts with `-debugscripts` |
| `setup.log` | Loaded GUI, modifiers, traits, and other data |
| `game.log` | In-game notifications and `log` output; only written with `-debugscripts` |
| `historical_setup_errors.log` | Title and character history problems, with `-fullhistoricalsetuplog` |
| `system_interface.log` | Interface errors |
| `graphics.log` | Map and graphics errors |
| `text.log` | Localisation asserts |
| `script_optimizations.log` | Asserts on events firing for courtiers |
| `exceptions.log` | Stack trace after a crash, with the last method reached |
| `time.log`, `memory.log` | Load duration and memory use |
| `ai.log` | AI decisions |

Benign lines to ignore:
- `[technology.cpp:718]: Missing Tech seed values`
- `[technology.cpp:755]: None`
- `[texturehandler.cpp:181]: Couldn't find texture file:` followed by nothing

Read `error.log` first after every change. The first entry is normally the cause; later entries cascade from the first aborted block.

## The Validator

The Validator (Jamie550) is a Windows tool that statically checks the whole game and mod load. It catches:
- Brace and syntax errors.
- Invalid scopes, conditions, and commands.
- Misspelled or unknown keys and keywords.
- Duplicate and invalid IDs.
- Missing flags, missing localisation keys, missing adjectives.
- `mean_time_to_happen` used on an on_action event.
- Many engine-level mistakes that otherwise appear as random crashes.

Run it after bulk edits and before playtesting. It is far cheaper than a restart loop, and its false-positive rate is low; investigate every report before dismissing it.

## Console Commands Worth Memorising

Debug and inspection:
- `charinfo` / `debug_mode` — IDs, health, fertility, flags, variables, and AI values on portraits; province, title, and event IDs; scope names on events.
- `observe` — observer mode, revealing hidden traits and secret religions.
- `testevent <id> <char|prov id>` — evaluates an event's conditions and prints pass/fail per condition. Conditions without tooltips are omitted from the output, so flags may appear silent.
- `event <id> <char|prov id>` — fires an event, bypassing all triggers.
- `run <file.txt>` — executes a script file from the CK2 user folder in the player's scope.
- `reloadevents` — recompiles every event without restarting.
- `reloadloc` — reloads the localisation table.
- `log_missing_adjectives` — lists titles without `<title>_adj`.

Character manipulation: `cash`/`wealth`, `prestige`, `piety`, `decadence`, `score`, `age`, `die`, `kill <id>`, `add_trait`, `remove_trait`, `add_modifier`, `remove_modifier`, `claim`, `give_title`, `nickname`, `culture`, `religion`, `gfx_culture`, `imprison`, `banish`, `move`, `add_lover`, `neg_opinion`, `favor_get`, `favor_grant`, `join_society`, `leave_society`, `enable_ambition`, `clr_focus`, `recalc_succ`, `give_birth`.

Realm and map: `capital <prov id>`, `clr_moved_capital`, `max_tech`, `techpoints`, `decision <id> <char id>`, `council_positions`, `enforce_peace`, `liege_enforce_peace`, `coalition`.

Notes:
- `event` ignores every trigger; use `testevent` when the question is whether the event can fire.
- `kill_yourself` is disabled; use `die`.
- `clr_focus` on other characters sometimes crashes; save first.
- `play <char id>` resets the chronicle of the character you switch away from.
- Giving a dead character flags or variables silently fails.

## Time-Saving Workflow

1. Add the change and save the files.
2. Run The Validator.
3. In game, `reloadevents` and `reloadloc` for script and text changes.
4. Restart for `common/`, `history/`, `map/`, `.mod`, and interface layout changes.
5. `testevent` to check conditions, `event` to check design, `run` to iterate on effects without touching the mod.
6. Read `error.log`, `text.log`, and `system_interface.log` after each iteration.

## Common Errors and Their Actual Cause

| Message or symptom | Cause |
|--------------------|-------|
| Nothing happens when the event fires | Wrong scope for the command, or the option is not `is_triggered_only`-safe |
| Event never fires | Trigger false, pre-trigger excludes the character, or MTTH present on a triggered-only event |
| Options greyed out | Option `trigger` false, or `ai_acceptance` returning zero on a targeted decision |
| Decision section headings malformed | Syntax error or unknown keyword anywhere in that decision file |
| Flags shifted between titles | A missing `gfx/flags/<title>.tga` |
| Wrong portrait clothing or missing beard | Property index misaligned with `portrait_properties.txt` |
| Province missing from realm view | Colour-space metadata in `provinces.bmp`, or `max_provinces` not incremented |
| Text shows raw keys | Key missing, `.txt` instead of `.csv`, or wrong encoding |
| Text shows `???` or `§` garbage | UTF-8 saved file, or a semicolon inside a value |
| Duplicate buildings, traits, or CBs | Reused a key in a coexist folder |
| Mod inert for some users | `replace_path` or `archive` in the legacy install directory |
| Crash after adding a religion or focus | Hardcoded interface window expects a matching `.gui` copy |

## Cross-Reference Discipline

The wiki's `Commands` and `Conditions` indexes are snapshots. When a command or condition behaves unexpectedly:
1. Search the shipped `common/`, `events/`, and `decisions/` files for working usage.
2. Confirm the scope in `references/scripting.md`.
3. Confirm the folder override rule in `references/mod-packaging.md`.
4. Re-check with The Validator, which knows the current build's vocabulary.