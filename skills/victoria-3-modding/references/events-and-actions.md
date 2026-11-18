# Events, On Actions, Decisions, Journal Entries, and Objectives

## Events

**Folder:** `events/` (subfolders allowed; subfolders always load after top-level files).

A minimal country event:

```
namespace = example_event               # once per file, before its events

example_event.1 = {                     # every event needs an ID
    type = country_event                # country_event / state_event / character_event
    placement = root                    # map placement scope
    hidden = yes                        # omit when you want the event window

    title = example_event.1.t           # localisation key
    desc = example_event.1.d
    icon = "gfx/interface/icons/event_icons/event_default.dds"

    trigger = {                          # optional; defaults to always true
        exists = c:USA
        this = c:USA
    }

    immediate = {                        # effects run before the window appears
        ruler = { save_scope_as = ruler_scope }
    }

    cooldown = { years = 3 }             # optional; blocks re-evaluation

    option = {
        name = example_event.1.a
        default_option = yes
        # default_option is required for at least one option on normal events
    }
}
```

Rules:

- **Events never fire by themselves.** Victoria 3 has no `mean_time_to_happen`; an event must be raised by `trigger_event`, an `on_action`, a decision `when_taken`, a journal entry, or another event.
- `type` sets both the root scope and where the event icon sits (`root` default, or `placement = scope:<saved>`).
- `trigger` is evaluated against every object matching `type`. To avoid firing across the whole world, gate it tightly (`exists = c:XXX` + `this = c:XXX`).
- Without at least one `option` the event must be `hidden = yes`; options store localisation keys, not literal text.
- `cooldown` sets a permanent variable-based lock; `variable` duration tools can achieve temporary locks too.
- Hidden events skip localisation, audio, icons, and options; they are purely effect triggers.

Namespaces:

- Every event file starts with `namespace = <name>`.
- Event IDs are `<namespace>.<integer>`, never `0`, unique across all loaded event files (duplicates silently break events).
- Multiple namespaces per file are allowed; each must precede its events.

## On Actions

**Folder:** `common/on_actions/`. Root scope defaults to `root`; the list gives any extra scope per action.

Modding on actions never restate the whole vanilla block. Append a custom chain instead:

```
on_monthly_pulse_country = {
    on_actions = { my_mod_monthly }
}

my_mod_monthly = {
    trigger = { always = yes }
    effect = { ... }                   # separate chain from the events fired below
    events = { example_event.1 }       # fires after the effects block
}
```

Only `on_actions`, `events`, or `random_events` may be appended to an existing on action; changing its `trigger` or `effect` requires replacing the whole file, which breaks other mods trying to append to it. Use `trigger_event = { on_action = <name> ... }` delays optional.

An on_action block supports a fixed menu:

- `trigger = { ... }` — gates firing.
- `events = { id.1 delay = { days = X } id.2 }` — fire every matching event; delays support `{ min max }` ranges.
- `random_events = { chance_to_happen = N chance_of_no_event = { value = N } weights }` — weighted single pick.
- `first_valid = { id.1 id.2 ... }` — first event whose trigger passes.
- `on_actions = { ... }` — chain another on action.
- `random_on_action` / `first_valid_on_action` — same patterns for on actions.
- `effect = { ... }` — effects run concurrently with events, not before; scopes and variables set here do not carry into events fired by this on_action.
- `fallback = <on_action>` — runs only when nothing else fired; avoid infinite loops.
- `weight_multiplier = { base = 1 modifier = ... }` — affects selection weight in random lists.

## Decisions

**Folder:** `common/decisions/`; injectable and replaceable.

```
example_decision = {
    is_shown = {
        this = c:ABC
        NOT = { has_variable = example_decision_taken }
    }
    possible = {
        has_technology_researched = organized_sports
    }
    when_taken = {
        trigger_event = { id = example_events.1 popup = yes }
        set_variable = { name = example_decision_taken }
    }
    ai_chance = {
        value = 100
        <script_value>
    }
}
```

- `is_shown`: whether the player sees it.
- `possible`: whether it can be selected.
- `when_taken`: effects that run when taken, including event invocation.
- `ai_chance`: default weight 1; 0 means the AI never takes it.
- Decisions sit under country scope unless documented otherwise.

Journal entries are the common companion: decisions often fire an event or add a journal entry in `when_taken`.

## Journal Entries

**Folder:** `common/journal_entries/`; injectable and replaceable. They represent ongoing situations or goals.

Minimal entry:

```
je_example = {
    is_shown_when_inactive = {
        is_player = yes
        NOT = { has_variable = je_done }
        has_technology_researched = threshing_machine
    }
    possible = {
        has_technology_researched = mechanized_farming
    }
    immediate = {
        trigger_event = { id = example_events.9 popup = yes }
    }
    group = je_group_mygroup             # optional visual grouping
}
```

Outcome blocks (any number as needed):

```
outcome = {
    header = je_standard_completion_header
    effect_header = je_standard_on_completion_header
    color = "gold_positive"
    conclusion_desc = je_standard_completion_conclusion_desc
    trigger = {
        scope:journal_entry = { is_goal_complete = yes }
    }
    effect = { set_variable = je_done }
}
```

- Pulses: `on_weekly_pulse`, `on_monthly_pulse`, `on_yearly_pulse` run effects on period boundaries.
- Goals pair `current_value` + `goal_add_value` script values with the `is_goal_complete` trigger; they activate independently of completion outcomes.
- `modifiers_while_active` applies static modifiers for the entry's lifetime.
- Progress bars: `progressbar = yes` ties to the goal; scripted progress bars live in `common/scripted_progress_bars/` with `start_value`, `max_value`, `min_value`, weekly/monthly/yearly progress values, and optional `progress_condition`s.
- Scripted buttons: `common/scripted_buttons/`, with `visible`, `possible`, `ai_chance`, and `effect` blocks; each button is unique but shares localisation keys freely.
- Activation: `add_journal_entry = { type = <key> target = scope:x }` or fulfilled trigger blocks (`is_shown_when_inactive` AND `possible`).

## Objectives

**Folder:** `common/objectives/` (plus `common/objective_subgoals`, `common/objective_subgoal_categories`). Objectives structure campaign goals; journal entries track them. `modifiers_while_active` and goal values work similarly.

## Common Conventions

- Every localisation key referenced in `title`, `desc`, `name`, `option.name` must exist in every shipped language, under `localization/<language>/<key>_l_<language>.yml`.
- Journal entry icons go under `gfx/interface/icons/event_icons/` as `.dds`.
- `trigger_event` with `popup = yes` forces the player focus; omit it for background firing.
- Delayed events (`delay = { months = { 6 12 } }`) must still be valid both when the chain fires and when the delay ends.
- Data functions in localisation (`GetName`, `GetHerHis`, `GetFullName`, `ScriptValue(...)`, `GetCustom(...)`) keep dynamic text localised.
- Saved scopes (`save_scope_as` / `scope:`) are forwarded to triggered on_actions and events if saved before the effect that raises them.