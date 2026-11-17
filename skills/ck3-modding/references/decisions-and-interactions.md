# Decisions, Character Interactions, Schemes, Activities, Story Cycles, Struggles

## Decisions

Defined in `common/decisions/*.txt`; a key/name plus a set of blocks.

```
my_decision = {
	picture = { reference = "gfx/interface/illustrations/decisions/decision_smith.dds" }
	desc = my_decision_desc
	selection_tooltip = my_decision_tooltip

	is_shown = { }
	is_valid_showing_failures_only = { }
	is_valid = { }

	cost = { gold = 42 piety = 42 prestige = 42 }
	effect = { add_gold = 100 }

	ai_check_interval = 0
}
```

Available keys and blocks (full list in `common/decisions/decision.info`):

| Key | Purpose |
|-----|---------|
| `picture` | Image (and sound, via a block with triggers). `extra_picture` is used by struggle decisions |
| `decision_group_type` | Folds the decision into a group declared in `common/decision_group_types` |
| `sort_order` | Ordering within the list; higher sorts above |
| `is_invisible` | Hides the decision from the panel while still allowing it to run |
| `ai_goal` | AI budgets for the decision; `ai_check_interval` then ignored |
| `ai_check_interval` | Months between AI evaluations; `0` means never. Required unless `ai_goal = yes` |
| `cooldown` | e.g. `cooldown = { years = 5 }`; refresh with `remove_decision_cooldown = <id>` |
| `is_shown` | Panel visibility |
| `is_valid` / `is_valid_showing_failures_only` | Both must pass for the decision to be usable; the latter tooltips only unmet conditions |
| `cost` | Resources required and deducted |
| `minimum_cost` | Resources that must be *available*, not deducted (for scripted costs) |
| `effect` | What the decision does |
| `ai_potential`, `ai_will_do` | AI willingness; `ai_will_do = { base = 100 }` |
| `should_create_alert` | Suppresses the alert when taking the decision is pointless |
| `widget` | Custom GUI widget, file named after the widget in `gui/decision_view_widgets/` |

The panel is populated from four localisation keys derived from the decision name: `<name>`, `<name>_desc`, `<name>_tooltip`, `<name>_confirm`. Each can be redirected with `title`, `desc`, `selection_tooltip`, `confirm_text`.

File-level constants avoid repeated literals:

```
@sale_of_titles_prestige_cost = 500

sale_of_titles_decision = {
	cost = { prestige = @sale_of_titles_prestige_cost }
}
```

The default controller does not work for widgets; `controller = create_holy_order` is the documented working example.

## Character Interactions

`common/character_interactions/*.txt`. Interaction effect blocks have **no** `root` — the game provides `scope:actor` and `scope:recipient`.

```
basic_interaction = {
	on_accept = {
		scope:actor = { add_gold = 100 }
		scope:recipient = { remove_short_term_gold = 100 }
	}
	auto_accept = { always = yes }
}
```

- `on_accept` runs when the recipient accepts; `on_send` runs immediately but produces no effect preview.
- `auto_accept` makes the interaction instantaneous (useful while testing).
- Without `category` and an icon the interaction appears under "Uncategorized".
- `is_shown`, `is_valid`, `on_decline`, `ai_accept` and descriptive keys exist; consult `character_interactions.info` in the folder.
- Interaction script can only batch characters one at a time.

## Schemes

Defined under `common/scheme_types` (plus supporting `scheme_agent`, `scheme_countermeasures` folders). Scheme behaviour is largely hardcoded; mods alter agents, success chance, countermeasures, events and on-actions referenced by the scheme. Any new scheme must supply localisation and be reachable through decisions, events or interactions.

## Activities

`common/activities/*.txt` defines activities; activities are hosted by a character, have multiple variants, run through phases, and roll for an event every seven days of each phase. Costs derive from host title rank or company size, then cultural, religious, era and option modifiers. An activity with no attendees is cancelled and the host takes 20 stress.

Supporting surfaces: `common/activity_types`, phase definitions, `common/customizable_localization` entries for the UI text, illustration assets under `gfx/interface/illustrations/activities/`, and scripted GUI widgets where the activity offers array choices.

## Story Cycles

`common/story_cycles/*.txt`. Created from script with `create_story = <story_cycle_name>`, which binds the cycle to an owner.

```
story_cycle_name = {
	on_setup = { }            # effects on creation; scope is the story, use story_owner = { } to reach the owner
	on_end = { }              # effects when ended (end_story = yes)
	on_owner_death = { }      # fires while the owner is still alive, like the on_death on_action

	effect_group = {
		days = 30             # or months / years, and ranges such as { 30 60 }
		chance = 50           # optional 1-100 roll
		trigger = { }
		triggered_effect = {
			trigger = { }
			effect = { }
		}
		first_valid = {       # choose the first triggered_effect whose trigger passes
			triggered_effect = { trigger = { } effect = { } }
			triggered_effect = { }
		}
	}

	effect_group = { }
}
```

Standard uses: transferring the cycle to an heir (`make_story_owner = story_owner.primary_heir`), copying variables on owner death, or ending explicitly with `end_story = yes`. Story cycles double as container objects for pseudo-arrays (see `references/scripting.md`).

## Struggles

`common/struggle/<name>.txt`, with catalysts in `common/struggle/catalysts` and values in `common/script_values/`.

Structure:

- `cultures = { ... }` and `faiths = { ... }` list who participates; unlisted cultures and faiths become interlopers.
- `regions = { ... }` restricts the struggle map area.
- A culture or faith becomes involved once roughly 80% of its counties lie inside the region.
- `start_phase` names the first phase; `phase_list = { <phase> = { ... } }` defines each.
- Each phase has a `duration = { points = N }`, a `future_phases` block listing reachable phases and the catalysts that advance to each, and effect blocks for on-enter/on-exit style behaviour.
- Catalysts accumulate points over time; balance them so a phase change takes the intended number of decades.
- Textures and 2D graphics for the struggle UI live under `gfx/interface/struggles/`.

Localisation, UI hooks and a starting `on_game_start` on_action (see `common/on_action/game_start.txt` in vanilla for the pattern) complete the setup.

## Localisation for These Objects

| Object | Keys |
|--------|------|
| Decision | `<name>`, `<name>_desc`, `<name>_tooltip`, `<name>_confirm` (or the redirected keys) |
| Interaction | Title/description keys named in the interaction plus the on-send/on-accept tooltips |
| Activity | Name, description, option labels and phase labels, plus customizable-localization entries where the UI expects them |
| Story cycle | Any keys its events reference |
| Struggle | Struggle name, phase names and descriptions, catalyst descriptions |
