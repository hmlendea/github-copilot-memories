# Scripting: Background Scripts, Events, Conditions, and Commands

## Model

Rome Remastered inherits the Total War script language from Rome: Total War and extends it. The language is line-oriented, tab-indented, and `;;`-commented. A script is a sequence of *monitors*: each monitor declares a triggering event (or a polled condition) and runs a block of commands when it fires.

New in Remastered:

- A **background script** listed in `descr_strat.txt` that starts automatically and reloads on save reload, replacing the `show me how` workaround.
- **Persistent counters** stored inside the save.
- Roughly 100 new commands, 50 new conditions, and 100 new events — most of them for the tutorial layer, but the modding-relevant ones are listed below.
- Script **logging** and control flow (`if_not`, `while_not`, `break`, `return`, `for_each`, `goto`/`set_label`).

## Wiring the Background Script

1. Copy `data/world/maps/campaign/imperial_campaign/descr_strat.txt` (or the BI/Alexander equivalent) into the mod at the identical relative path.
2. At the **bottom** of that file, add the script filename, with or without extension as the vanilla files do.
3. Place the script file in the same campaign folder, for example `data/world/maps/campaign/imperial_campaign/my_script.txt`. The example-mod script lives at `data/world/maps/campaign/alexander/alexander_campaign_script.txt`.

Repeat per campaign: each `descr_campaigns.txt` entry has its own `folder`, and each folder has its own `descr_strat.txt`.

## Script Skeleton

```
script

	declare_counter output
	declare_counter flag

	message_prompt
	{
		flag_counter flag
		result_counter output

		title SCRIPT_MESSAGE
		body SCRIPT_MESSAGE_BODY

		image prebattle_night
	}

	;; monitor for our prompt getting a response
	monitor_event ScriptPromptCallback I_CompareCounter flag == 1
		if I_CompareCounter output == 1
			console_command kill_character "Alexander"
		end_if
		if I_CompareCounter output == 0
			console_command kill_character "Parmenion"
		end_if
	end_monitor

end_script
```

Rules that follow from the parser:

- The file opens with `script` and closes with `end_script`; both are required.
- Every `monitor_event` / `monitor_conditions` / `if` / `while` block is closed by its matching `end_` keyword.
- Indentation is a tab per level. The parser is not indentation-sensitive, but the community tooling and every vanilla file use tabs, and mismatched blocks are the most common script defect.
- Braced command bodies (`message_prompt { ... }`) take one key per line without commas.
- Quoted strings appear where a name contains a space: `console_command kill_character "Alexander"`.

## Monitors

| Form | Fires when |
|------|-----------|
| `monitor_event <EventName> <condition> <condition> ...` | The named event occurs **and** every inline condition holds |
| `monitor_conditions <condition> ...` | Evaluated every frame/turn tick; the conditions hold |
| `monitor_event <Event> <cond>` plus `end_monitor` | Standard block |

Inline conditions after the event name are checked at event time, which is far cheaper than polling. Prefer a specific event plus a narrow condition over a polling monitor.

Scripts can be terminated from within: `break` exits the current scope; `return true|false` returns from a faction-spawn script and ends it.

## Counters

| Command | Effect |
|---------|--------|
| `declare_counter <name>` | Integer counter, zeroed on load |
| `declare_persistent_counter <name>` | Integer counter stored in the save; zero-initialised on first use |
| `set_counter <name> <value>` | Assign |
| `inc_counter <name> <value>` | Add (negative to subtract) |
| `counter_operation <result> = <a> <op> <b>` | `+ - * /` |
| `I_CompareCounter <name> <op> <value>` | Condition |
| `store_counter <counter> <location> <label>` | Persist a counter onto a settlement/character/faction/etc. |
| `retrieve_counter <label> <location> <counter>` | Read it back |

`store_counter`/`retrieve_counter` attach named data to a game object in scope; `declare_persistent_counter` keeps one value for the whole save. Choose per scope: a per-settlement flag needs the former, a campaign-wide stage needs the latter.

Debug a counter with `console_command check_persistent_var <name>`; the official tips page treats that as the reliable route to the log file and warns that `script_log` may write to stdout instead. Test whichever one your build actually logs to before relying on it.

## Control Flow

```
if I_CompareCounter stage == 2
	; ...
end_if

if_not I_CompareCounter stage == 2
	; ...
end_if

while I_CompareCounter ticks < 5
	inc_counter ticks 1
end_while

while_not FactionIsAlive romans_julii
	; ...
end_while

for_each settlement in faction "romans_brutii"
	; iteration body
end_for_each

set_label location
goto location
```

`if`/`while`/`monitor` blocks close with `end_if`, `end_while`, `end_monitor`. The shipped example script confirms only `end_if` and `end_monitor`; confirm the `for_each` terminator against a vanilla script before relying on it.

`for_each` reads `for_each <iterator type> in <scope type> [<scope identifier>]`. Both types are drawn from `faction`, `settlement`, `fort`, `character`, `army`, and `unit`; the scope identifier is optional and defaults to the local scope. Iterating `unit` always yields the player's units.

Loop and label constructs are the ones that turn an unmaintainable monitor pile into readable logic; they are all Remastered additions and are absent from original RTW.

## Prompts and Player Input

```
message_prompt
{
	flag_counter flag
	result_counter output
	title <localisation key>
	body <localisation key>
	image <event image key>
}
```

Raises a modal yes/no news item the player must answer before ending the turn, then sets `flag_counter` to `1` and `result_counter` to `1` (yes) or `0` (no). Using the **same** counter for both makes it hold only the result. Detect the answer with a `monitor_event ScriptPromptCallback` monitor.

Related UI commands: `close_news_panel`, `disable_all_ui_cards`, `advance_completed_tasks <n>`, `open_siege_scroll`, `show_ui_element <id>`, `hide_ui_element <id>`.

## Events

Remastered additions:

| Event | Use |
|-------|-----|
| `NewTurnStart` | Start-of-turn work that must not run on game open |
| `FactionDestroyed` | React to a faction being eliminated |
| `TakeOffice` / `LeaveOffice` | Senate office changes (office names are now data) |
| `ScriptPromptCallback` | A `message_prompt` was answered |

Original-game events remain valid (`FactionTurnStart`, `CharacterTurnStart`, `GeneralAssaultsGeneral`, `PostBattle`, `SettlementTurnStart`, `CharacterComesOfAge`, and the rest). Every event declares an export list — `nc_character_record`, `character_record`, `faction`, `region_id`, `character_type`, and similar — and the exported values are the only context the monitor body has without a condition.

The authoritative list is the generated `docudemon_events.txt` in `VFS/Local/Rome/documentation`.

## Conditions

Highlights added by Remastered:

**Diplomacy** — `IsAlly <faction>`, `IsProtectorate <faction>`, `IsProtector <faction>`, `IsSameSuperfaction <faction>`, `at_war <faction>`.

**Settlements** — `IsCapital`, `I_SettlementOwnerCulture`, `I_SettlementLevel <level>`, `SettlementCapabilityLevel <capability>`, `SettlementOrderLevel <level>`, `HomeSettlementBuildingExists <building> <level>`, `HasResource <resource>`, `SettlementRevoltingFrom`.

**Characters** — `CharacterName <name>`, `DistanceCapital <n>`, `I_CharacterNameNearTile`, `HasOffice <office>`.

**Factions and state** — `FactionIsAlive <faction>`, `MajorEventActive <event>`, `LangIs <language>`, `I_CompareCounter`.

Each condition declares a `Trigger requirements` scope (`character`, `faction`, `settlement`, `none`, …) and a `Battle or Strat` domain. A condition evaluated in the wrong scope silently yields false.

The authoritative list is the generated `docudemon_conditions.txt`. The shipped `Scripts_conditions.md` lists only the delta.

## Commands

`console_command <name> <args>` invokes a RomeShell command from script; this is how script reaches anything not wrapped in a dedicated command. Common examples:

```
console_command add_money romans_julii 5000
console_command add_population "Arretium" 500
console_command kill_character "Alexander"
console_command event volcano <x> <y>
console_command check_persistent_var stage
```

`kill_character` and `add_population` take quoted names; `add_money` takes an optional faction followed by an amount.

Direct script commands worth knowing:

| Command | Effect |
|---------|--------|
| `spawn_character_child` | Create a character with a named father; the original-game `spawn_army` and `spawn_character` remain available |
| `create_mercenary_pool` | Add a mercenary pool |
| `move_to_settlement`, `snap_to_settlement` | Move and snap the camera to a settlement |
| `rename_settlement_in_region` | Rename a settlement |
| `destroy_building`, `add_religion`, `add_hidden_resource`, `remove_hidden_resource` | Region and settlement mutation |
| `set_ao_visible "<tag>" show\|hide ["Region"]`, `set_all_ao_visible "<tag>" show\|hide` | Ambient campaign objects |
| `set_faction_senate_standing`, `set_faction_people_standing`, `override_superfaction_popularity` | Senate control |
| `trigger_marriage_proposal` | Player-facing marriage offer |
| `include_script` | Compose a script from parts; the shipped command list documents no parameters |
| `force_autoresolve_outcome`, `disable_specific_shortcut`, `set_marriage_allowed` | Campaign control |

`console_command` commands are documented in `docudemon_romeshell.txt`, generated on launch; the shipped `console_commands.txt` is a readable copy. Each entry states its availability (`campaign`, `battle`, `campaign_ed`) — a command used in the wrong mode does nothing.

## Major Events

`descr_sm_major_events.txt` replaces the hard-coded Marian reforms. Define events there, gate content with the `major_event "<name>"` condition (in EDB and script), and force or suppress state from `descr_strat.txt`:

```
set_major_event_enabled marian_reforms, false
trigger_status marian_reforms, empire_east, true
trigger_status marian_reforms, true
```

`major_event_scripts` folders (for example `marian_reforms_trigger.txt`) carry per-event script.

## Logging

Launch option `verbose_script_logging` writes `VFS/Local/Rome/logs/scripting_log.txt`. It prints every command and every monitor evaluation — best debugging tool for scripts, and completely unusable for play-testing because of its size.

Combine it with `enable_logging` (feature and data-file messages in `message_log.txt`) and `enable_dialogs` (the same messages as pop-ups).

## Common Defects

| Symptom | Cause |
|---------|-------|
| Script never runs | Filename not added to `descr_strat.txt`, wrong campaign folder, stale manifest |
| Script runs on reload twice | Expected: the background script restarts on save reload. Guard with a persistent counter |
| Counter resets | Used `declare_counter` where the value must survive; use `declare_persistent_counter` |
| Monitor never fires | Wrong event name for this build, missing export, or an inline condition that is false in that scope |
| `Unexpected in condition parsing` | A bare `and` / `or` where the parser expected a complete condition on the same line |
| Character commands do nothing | Name mismatch — `kill_character` and friends need the exact character name; verify with `descr_strat` |
| Values not visible in game | `script_log` may write to stdout; prefer `console_command check_persistent_var` |