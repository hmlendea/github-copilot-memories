# Console, Debug Mode, Hotloading, Logs, and Scripted Tests

## Enabling Debug Mode

Launch with `-debug_mode`. Three ways:

1. **Paradox Launcher** → Game Settings → *Open game in Debug Mode* → Launch.
2. **Steam** → right-click Victoria 3 → Properties → Launch Options → add `-debug_mode` → play from the main Play button.
3. **Windows, no Steam** — create a shortcut to `binaries/victoria3.exe` and append ` -debug_mode` to the Target field.

Mods that expose a console toggle work for commands but do **not** enable file hotloading; for modding, always combine launcher/Steam launch options with the console.

Debug mode adds: the console window, debug menus (including the GUI Editor and Script Explorer), extra map tooltips, Ctrl-click to take control of a country, Ctrl-Alt-click to take a state, and a file watcher that reloads changed files.

Disabling debug mode: remove `-debug_mode`, disable all mods, restart, then confirm the checksum in the bottom-right of the main menu.

## Opening the Console

Press the layout-dependent key. On QWERTY it is `` ` ``; other candidates are `^`, `§`, `~`, `°`, `²`, `Shift+2`, `Alt+2+1`, `Shift+3`. `Shift+Alt+C` works when none of those do.

- `↑` / `↓` traverse previous commands.
- `Tab` autocompletes or lists matching commands.
- Repeating many commands toggles them; some require a reload or a game restart.

## Logs and Dumps

| Artifact | Location |
|----------|----------|
| `error.log` | `<user data>/Victoria 3/logs/` |
| `system.log`, `debug.log` | same |
| `script_docs` and `DumpDataTypes` output | `<user data>/Victoria 3/docs/` |
| Save games | `<user data>/Victoria 3/save games/` |

`error.log` is the primary signal. A silent no-op effect or trigger is almost always a wrong scope or an unknown key recorded there.

Debug mode adds an **error deer** button that opens `error.log` and displays the error count since it was last opened. Configure the editor:

```json
{
  "System": {
    "editor": "C:/Program Files/Sublime Text/sublime_text.exe",
    "editor_postfix": ":$:1"
  }
}
```

Edit `pdx_settings.json` in the user data folder, or use the in-game console → Settings → System → Editor.

## Documentation Commands

```
script_docs        # dump effects, triggers, scopes, event targets, modifiers, on_actions
DumpDataTypes      # dump GUI script data types, functions, and promotes
```

Regenerate after every patch. Treat the wiki as a starting point and these dumps as authoritative for the installed build.

## Reloading

| Command | Effect |
|---------|--------|
| `reload <filename>` | Reload one asset or file group |
| `gfx.reloadtexture` | Reload textures after a `.dds` change |
| `debug_mode` | Toggle debug mode (cannot re-enable once closed except via a mod) |
| `map_editor` | Toggle the map editor |
| `gui_editor` | Spawn the GUI editor (removed in 1.9; use the debug menu instead) |
| `Log.ClearAll` | Clear all logs |
| `Log.ClearErrorLog` | Reset the error log and its error count |

Hotloading covers most script and `.gui` files while debug mode is active. It does **not** cover `on_actions`, scripted GUIs (`common/scripted_guis` is loaded at startup only), and several cached definitions; those need a return to the main menu and a new game.

## Diagnostic Commands

Commands that write a delimited log file into the user data directory:

| Command | Output |
|---------|--------|
| `debugcharacters` | all characters |
| `debugcountrybudgets` | every country and its budget |
| `debugemployment <state id>` | employment in one state |
| `debugmarkets` | every goods and market |
| `debugpopconsumption` | all pop consumption |
| `debugpopwealth` | wealth of every pop |
| `debugstates` | all states |
| `debugtheaters` | all theaters |
| `check_save` | save/load round-trip consistency |
| `Print.EventDebug` | event debug statistics (after `Debug.Events` is enabled) |
| `Log.ToggleIncludeKeyInLocOutput` | render localisation keys alongside text |
| `Log.ToggleOnlyKeyInLocOutput` | render localisation keys only |
| `Checksum.Log` | log the game state checksum |
| `Threading.TaskThreadCount <n>` | set or read task thread count |
| `TickTask.Graph` / `TickTask.List` | profiling views |

UI migration aids: `Localization.ToggleIncludeKeyInLocOutput`, `Localization.ToggleOnlyKeyInLocOutput`, `Localization.ToggleSkipDataSystemInLocOutput` — find hardcoded strings by temporarily rendering keys instead of text.

Map tooling: `Map.SavePNG <map mode> <file name> <flat yes/no>` (only the `countries` mode is reliable), `MapObjects.Debug`, `MapObjects.GenerateGameLocators <type> [<filename>]`, `MapObjects.Painter.AddPosition`.

Audio: `Music.PlayTrack <track>`, `Music.PauseFactor`, `Music.Reset`, `Music.StopTrack`.

## Playtest Commands

These alter state directly and are safe for testing but must never be required by shipped content:

| Command | Purpose |
|---------|---------|
| `add_journal_entry <key>` | Activate a journal entry on the player country |
| `Complete_journal_entry <key>` | Force completion |
| `Fail_journal_entry <key>` | Force failure |
| `change_law <law key>` | Swap a law |
| `add_ideology <ig> <ideology>` | Add an ideology to an interest group |
| `add_approval <ig> [amount] [months]` | Approval modifier |
| `add_clout <ig> [amount] [months]` | Clout modifier |
| `add_loyalists <culture> <amount>` | Loyalists by culture fraction |
| `add_radicals <culture> <amount>` | Radicals by culture fraction |
| `add_relations <tag> <amount>` | Change relations |
| `add_mandates <amount>` | Power bloc mandates |
| `add_war_support <tag> <amount>` | War support across all wars |
| `add_liberty_desire <tag> <amount>` | Subject liberty desire |
| `add_supply_ships <amount>` | Immediate supply ships |
| `annex <tag>` / `annex_all` | Annex a country / every country |
| `changestatepop <state id> <pop type|all> <factor>` | Scale pop size (capped by max employment) |
| `clearlines` / `clearspawnedentities` | Remove map lines / spawned entities |

AI inspection: `ai.debug <tag>`, `ai.goal <tag> <goal>`, `ai_evaluate_state <state region> <tag>`, `ai_evaluate_wargoal <type> <tag> <state region>`, `ai_evaluate_autonomous_construction <building> <state region>`, `ai_evaluate_government_construction`, `ai_evaluate_company <company type>`, `ai_evaluate_interest <strategic region>`, `ai_evaluate_mobilization`, `ai_evaluate_privatization`, `ai_evaluate_production_method <building> <pm> <state region>`, `ai_evaluate_subject <tag>`, `ai_evaluate_trade_route <goods> <tag>`, `ai_evaluate_treaty_port <state region> <tag>`.

## Scripted Tests

Scripted tests are utility files that measure how often a defined game state is reached. They do not affect gameplay and are stored in `<mod>/tools/scripted_tests/`.

```
last_date = "1900.1.1"

tests = {
    GER_forms = {
        acceptable_fail_rate = 0.0
        run_count = 1
        success = {
            exists = c:GER
        }
        fail = {
            game_date > "1890.1.1"
        }
    }
}
```

| Element | Meaning |
|---------|---------|
| `last_date` | Deadline for the whole file; tests not decided by then are *skipped* |
| `tests` | Container; a file may hold any number of named tests |
| `success` | Trigger marking the test *passed*; checked daily |
| `fail` | Trigger marking the test *failed*; checked daily. If both pass on the same day, the test passes |
| `acceptable_fail_rate` | Decimal percent metadata only; does not affect behaviour, defaults to 0 |
| `run_count` | Number of runs; values below 0 run until `last_date`; only the final run is recorded, defaults to 1 |

Enable them with a command-line argument or the console:

| Switch / command | Effect |
|------------------|--------|
| `-run_tests` / `-scripted_tests` | Enable scripted tests at launch |
| `-no_save_after_failed_test` | Disable the default save-after-failure |
| `-save_before_failed_test` | Save before a test fails (slow, not recommended) |
| `scripted_tests` | Console toggle; a save is created after the tests |
| `scripted_tests before` | Save before the tests |
| `scripted_tests none` | No save |

Entering the console command again while tests are active disables them. Results are written as a text file into the Documents folder and as an XML file into the game's `binaries` folder.

Keep tests on invariants a manual playthrough cannot easily confirm: every new country has a capital and a defined formation, every new law group has at least one law, every new production method resolves, and every referenced localisation key exists.

## Debug Workflow

1. Launch with `-debug_mode`.
2. Read `error.log` before opening the game UI — most problems are logged there already.
3. Use `-debug_mode` hotloading for script and `.gui` iteration, but restart for on_actions, scripted GUIs, and defines.
4. When a trigger or effect does nothing, confirm its name and scope in the `script_docs` dump for the installed patch.
5. When a localisation key shows raw, check the BOM, the `_l_<language>` suffix, and the one-space indentation.
6. Use `trigger_event` from the console or a scratch decision to reach an event chain without waiting for its natural gate.
7. Validate achievement state by disabling all mods and removing launch options, then confirming the checksum in the main menu.
