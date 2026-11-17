# Events and On Actions

## Event Checklist

An event must:

- live in a `.txt` file in `events/` (subfolders are allowed);
- declare `namespace = <name>` on the first line of every file that uses it;
- be named `<namespace>.<number>`, with an ID below 9999 (the calling system misbehaves above it);
- be fired by something — events never fire on their own.

Every candidate event is polled against every eligible object by default only if it has no `is_triggered_only`-style guard; CK3 events are not polled in the CK2 fashion, so they need an explicit caller: an on_action, a decision, a character interaction, a scripted GUI, another event, or a story cycle.

## Minimal Event

```
namespace = example

example.1 = {
	desc = example.1.desc
	option = {
		name = example.1.a
	}
}
```

A more representative event:

```
superexample.1337 = {              # keep the event name in a comment on the definition line
	type = character_event
	title = "A Modding Example Worthy of Kings"
	desc = superexample.1337.desc

	theme = mental_break
	left_portrait = root

	trigger = {
		is_alive = yes
	}

	immediate = { }

	option = {
		name = superexample.1337.a
		add_stress = 10
	}

	after = { }
}
```

## Namespace and ID

`namespace` is an alphanumeric string with no `.`, declared once per file. The ID is unique within the namespace. The namespace must be re-declared in every file that uses it.

## Flags

| Flag | Meaning | Values |
|------|---------|--------|
| `type` | Determines the kind of scope the event runs against | `character_event`, `letter_event`, `duel_event`, `none` (root unused), `empty` (required for characterless events) |
| `hidden` | Runs without a window | `true`, `false` |

## Trigger

Evaluated before anything else; a false result stops the event. The trigger cannot see scopes created in `immediate`, so use a list builder to prefetch:

```
trigger = {
	any_knight = {
		has_trait = brave
	}
}
```

`on_trigger_fail = { }` runs when the trigger fails.

## Description

Literal strings work but log an error and forfeit data types; prefer localisation keys.

Branching descriptions use `first_valid` (first matching block wins) and `random_valid` (a random matching block wins), with `triggered_desc = { trigger = { } desc = <key> }` for conditional blocks and bare `desc = <key>` for always-valid entries.

```
desc = {
	first_valid = {
		triggered_desc = {
			trigger = { has_trait = drunkard }
			desc = my_event.0001.desc.drunkard
		}
		desc = my_event.0001.desc.fallback
	}
}
```

Multiple `desc` blocks concatenate with a **space** between them, so fragments containing punctuation must account for that (the vanilla text uses en-dashes for this reason). `first_valid` and `random_valid` can be nested for curated variety.

For options, wrap the branching block in `text`: `name = { text = { first_valid = { ... } } }`, or use the short form `name = { trigger = { } text = <key> }`. `flavor` blocks take the description form directly.

## Immediate, Options, After

| Block | Order | Typical use |
|-------|-------|-------------|
| `immediate = { }` | Before the window renders | Variables, saved scopes needed by text or portraits, unconditional effects |
| `option = { }` | Player choice | Effects, follow-up events, AI weighting |
| `after = { }` | After an option resolves | Cleanup — deleting temporary characters, clearing variables. Does nothing for option-less events |

Option keys:

| Key | Purpose |
|-----|---------|
| `name` | Localisation key for the button text, required |
| arbitrary effects | Written directly inside the `option` block |
| `trigger` | Availability condition for the option |
| `show_as_unavailable` | Shows the option greyed out when invalid |
| `trait`, `skill` | Decorative icon and tooltip hint; no functional effect |
| `add_internal_flag` | `special` (yellow) or `dangerous` (red); decoration only |
| `highlight_portrait` | Highlights a portrait while the option is hovered |
| `fallback` | Shown when no other option is valid |
| `exclusive` | If valid, shown alone |
| `flavor` | Tooltip flavour text; loc key or dynamic block |
| `hidden_effect` | Effects that are hidden from the tooltip |
| `ai_chance = { base = <n> modifier = { add = <n> <trigger> } }` | AI option weighting |
| `trigger_event = { id = <event> days = <n|{a b}> }` | Fires a follow-up event, optionally delayed |

## Portraits

Positions: `left_portrait`, `right_portrait`, `lower_left_portrait`, `lower_center_portrait`, `lower_right_portrait`.

```
left_portrait = {
	character = scope:accuser
	animation = anger
	triggered_animation = { trigger = { has_trait = brave } animation = rage }
	triggered_outfit = { trigger = { } outfit_tags = { western_stealth_hood } remove_default_outfit = yes }
	hide_info = no
}
```

Assigning a genetic-model-specific animation to a character without that model can crash the game; stay within the documented animation list, or guard with `triggered_animation`.

## Themes, Backgrounds, Environments

`theme = <key>` selects a background, lighting environment and sound set, declared in `common/event_themes/`. Individual parts can be overridden with `override_background`, `override_icon`, `override_sound` and `override_environment`; only override the environment when the automatic pairing is wrong.

## On Actions

Defined in `common/on_action` — **singular**, a common mistake. They fire script whenever game code or another script reaches a named action.

```
on_birth_child = {
	events = {
		my_event.1
	}
}
```

### Appending instead of overwriting

`events`, `random_events` and `on_actions` are appended across files; `trigger` and `effect` are overwritten and error when restated. To add behaviour safely, chain a custom on_action:

```
on_birth_child = { on_actions = { my_mod_on_birth } }
my_mod_on_birth = {
	trigger = { }          # applies only to this on_action
	effect = { add_gold = 100 }
}
```

### Properties

| Key | Behaviour |
|-----|-----------|
| `trigger` | On_action does nothing when false |
| `weight_multiplier` | Weights the on_action inside `random_on_actions` |
| `events` | All listed events fire if their own triggers pass; `delay = { days = N }` / `months = { a b }` postpones entries below it, and an event must be valid both at scheduling and at firing |
| `random_events` | One event is chosen. Supports `chance_to_happen`, `chance_of_no_event` (script value, evaluated only if the chance passes), weights per entry, and `0 = <weight>` for "nothing happens" |
| `first_valid` | First event whose trigger passes, with an optional triggerless fallback |
| `on_actions` | Fires other on_actions under the same rules |
| `random_on_actions` | Weighted random on_action, with the same `0 = <weight>` idiom |
| `first_valid_on_action` | First on_action in the list |
| `effect` | Runs effects in parallel with the fired events, in a separate chain — scopes and local variables set here are not visible to the events |
| `fallback` | Fired when nothing else ran. Never create a fallback loop |

### Common on_actions

| Name | Fires | Scope |
|------|-------|-------|
| `on_birth_child` | On a birth | Character |
| `on_16th_birthday` | On coming of age | Character |
| `on_birthday` | Every birthday; chains to `on_birthday_adulthood` when `is_adult` | Character |
| `on_death` | Just before death; the standard place to transfer variables to `primary_heir` | Character |
| `on_marriage`, `on_divorce`, `on_concubinage` | Relationship events | Character / none |
| `on_game_start` | Before character selection, so `every_player` is unavailable | None |
| `on_game_start_after_lobby` | After character confirmation — the place to touch player characters | None |
| `random_yearly_playable_pulse`, `yearly_playable_pulse`, `three_year_playable_pulse`, `five_year_playable_pulse`, `quarterly_playable_pulse` | Periodic pulses for count-tier and above | Character |
| `random_yearly_everyone_pulse`, `five_year_everyone_pulse`, `three_year_pool_pulse`, `yearly_global_pulse` | Broader periodic pulses | Character / none |
| `on_title_gain*`, `on_title_lost`, `on_title_destroyed` | Title changes | Character / none |
| `on_character_faith_change`, `on_county_faith_change`, `on_faith_created`, `on_faith_conversion` | Faith changes | Character / landed title / none |
| `on_character_culture_change`, `on_county_culture_change`, `on_culture_era_changed` | Culture changes | Character / none |
| `on_war_started`, `on_war_won_attacker`, `on_war_won_defender`, `on_war_white_peace` | Wars; `on_war_started` provides `scope:defender`, `scope:attacker`, `scope:war` | Casus belli / none |
| `on_combat_end_winner`, `on_combat_end_loser`, `on_commander_combat_pulse`, `on_knight_combat_pulse` | Combat | Combat side / character |
| `on_siege_completion`, `on_siege_looting`, `on_imprison`, `on_release_from_prison` | Sieges and imprisonment | Character / none |
| `on_raid_action_start`, `on_raid_action_weekly`, `on_raid_action_completion` | Raiding | Army / none |

There is **no monthly on_action** — the omission is deliberate for performance. If a monthly cadence is genuinely required, chain a custom on_action three times off `quarterly_playable_pulse` with increasing delays, or have the on_action re-fire itself with a one-month delay.

Check the comment above each on_action for its available scopes: `on_game_start` has no root and needs global effects such as `every_ruler`, while pulses run once per character and must not iterate all living characters.

## Firing Events From Anywhere

```
trigger_event = { id = my_event.1 }
trigger_event = { id = my_event.1 days = { 7 14 } }
trigger_event = { on_action = my_on_action }
```

Use `run <file>.txt` and the console's `event <id>` for iteration; `-develop` reloads the file without a restart.
