# Events, On Actions, Event Chains, and Anomalies

## Event Types

| Block | Scope |
|-------|-------|
| `event` | Global |
| `country_event` | Empire |
| `planet_event` | Planet (also stars, habitats, ringworlds) |
| `fleet_event` | Fleet |
| `ship_event` | Ship or starbase |
| `pop_faction_event` | Faction |
| `pop_group_event` | Pop group (4.0+; formerly `pop_event`) |
| `system_event` | Solar system / `galactic_object` (3.0+) |
| `starbase_event` | Starbase (3.0+) |
| `leader_event` | Leader (3.0+) |
| `espionage_operation_event` | Espionage operation (3.0+) |
| `first_contact_event` | First contact (3.0+) |
| `situation_event` | Situation (3.3+) |
| `agreement_event` | Subject agreement (3.4+) |
| `observer_event` | Observer, development only |

## Namespaces

Every event file begins with `namespace = <name>`. Every event ID inside is `<namespace>.<integer>`.

```
namespace = my_mod
country_event = {
    id = my_mod.1
    ...
}
```

Rules:
- The numeric part must be an integer. A letter makes the game read the ID as `namespace.0`.
- Leading zeros are truncated: `namespace.003` is `namespace.3`.
- Multiple namespaces per file are allowed; namespace names may contain digits and run to at least 100 characters.
- Call an event by ID: `country_event = { id = my_mod.1 }`.

## Event Skeleton

```
country_event = {
    id = my_mod.1
    title = my_mod.1.name
    desc = my_mod.1.desc
    picture = GFX_evt_my_picture
    show_sound = event_laboratory_sound
    location = root

    is_triggered_only = yes

    trigger = { ... }
    immediate = { ... }

    option = {
        name = my_mod.1.a
        custom_tooltip = my_mod.1.a.tooltip
        hidden_effect = { set_country_flag = my_mod_done }
    }

    after = { ... }
}
```

Key fields:

| Field | Purpose |
|-------|---------|
| `title`, `desc` | Localisation keys; both accept a triggered block form for conditional text |
| `picture` | `GFX_*` sprite, or a triggered block of pictures |
| `show_sound` | Sound key |
| `location` | Scope used to place the event on the map |
| `hide_window = yes` | No window; no options or text needed |
| `is_triggered_only = yes` | Not polled; only fired by script |
| `fire_only_once = yes` | Polled, then removed; the trigger must also exclude refiring or `error.log` records duplicates |
| `trigger = { ... }` | Condition gate |
| `immediate = { ... }` | Effects before the window is shown |
| `after = { ... }` | Effects after any option is chosen; runs regardless of which |
| `mean_time_to_happen = { months = 5 }` | Random delay after triggers pass |
| `diplomatic = yes` | Enables `response_text`, `is_dialog_only`, custom GUI options |
| `custom_gui` / `custom_gui_option` | Replace the event window layout |
| `event_window_type = leader_recruit` | Enables the `tag` / `hide_option_if_not_allowed` option fields |
| `trackable = yes`, `auto_select = yes`, `force_open = yes`, `auto_opens = yes` | Presentation behaviour |
| `picture_event_data = { portrait = ... planet_background = ... city_level = ... room = ... }` | Rich event backdrop |

## Options

```
option = {
    name = my_mod.1.a
    trigger = { ... }              # show only if true
    exclusive_trigger = { ... }    # if true, disable other options
    allow = { ... }                # shown but disabled if false (evaluated once on open)
    default_hide_option = yes      # selected by "Cancel" — does not hide it
    icon = GFX_...
    sound = ...
    custom_tooltip = my_mod.1.a.tooltip
    ai_chance = { factor = 100 modifier = { factor = 0 is_homicidal = yes } }
    hidden_effect = { ... }
    # plain effects may appear directly
}
```

`name` may itself be a triggered block with several `name` entries; the first matching one wins.

`ai_chance` is mandatory in practice for options the AI may evaluate; without it, the AI picks uniformly.

Diplomatic-only additions: `response_text` (without `is_dialog_only`, the window is an OK-only box and `after` runs immediately), `is_dialog_only` (text response only; buttons still fire effects, and `after` does **not** run; requires `response_text` or the game errors and exits the event), `custom_gui`.

## Execution Model

By default every event is evaluated against every applicable object, at least daily. That is the single largest avoidable CPU cost in a mod.

Preferred pattern:
1. One cheap **gatekeeper** event, `is_triggered_only = yes`, fired from an `on_action` or a scripted effect.
2. Gatekeeper checks fast conditions, does setup in `immediate`, then chains the visible event with `days`/`random` delays.

Hidden event chaining visible event is the vanilla norm because `immediate` effects are not fully reflected until the next event tick.

## Firing Events From Script

```
random_galaxy_planet = { planet_event = { id = my_mod.5 } }
country_event = { id = my_mod.6 days = 200 random = 100 }   # 200-300 days
```

- Conditions are checked at execution time, not when queued.
- 3.0+: `scopes = { from = fromfrom }` overrides the calling scope, but local event targets are not scoped into the fired event.
- Since 3.0, `fire_on_action = { on_action = <key> scopes = { from = X } }` fires custom on_actions. Event targets are not propagated when `from` is overwritten (fixed partly in 3.2).

## Pre Triggers

Fast boolean filters evaluated before full triggers. Supported on `planet`, `pop`, `system`, `starbase`, `leader` events; any other key inside the block is an error.

```
pre_triggers = {
    has_owner = yes
    is_homeworld = no
    original_owner = yes
    has_ground_combat = no
    is_capital = no
    is_occupied_flag = no
    is_ai = no            # planet events only
}
```

Pop: `has_owner`, `is_enslaved`, `is_being_purged`, `is_being_assimilated`, `has_planet`, `is_sapient`, `is_robotic` (4.0+).
System: `has_owner`, `is_capital`, `is_occupied_flag`.
Starbase: `has_owner`, `is_occupied_flag`.
Leader: `has_owner`, `is_idle`.

`can_join_pre_triggers` in `pop_faction_types` accepts the pop set.

## Conditional and Dynamic Descriptions

```
desc = {
    trigger = { owner = { NOT = { has_authority = auth_machine_intelligence } }
    }
    text = my_mod.1.desc.organic
}
desc = my_mod.1.desc.machine
```

Multi-part descriptions interleave `text`, `success_text`, `fail_text` with triggers:

```
desc = {
    text = my_mod.1.desc.top
    success_text = {
        text = my_mod.1.desc.multiplayer
        is_multiplayer = yes
    }
    fail_text = {
        text = my_mod.1.desc.singleplayer
        is_multiplayer = no
    }
    text = my_mod.1.desc.bottom
}
```

## On Actions

Registered in `common/on_actions/*.txt` (`NO/MERGE`). Existing vanilla entries cannot be edited; a new file contributes an additional `name = { ... }` block that merges into the vanilla entry of the same name.

```
on_game_start = {
    events = { my_mod.1 my_mod.2 }
    random_events = {
        100 = my_mod.3
        50 = my_mod.4
    }
}
```

- Files load top-first; events inside one action fire in listed order, and actions from multiple files fire in ASCIIbetical file order.
- `events` fires every registered event whose trigger passes.
- `random_events` rolls weights and fires exactly one; weight modifiers are not supported inside `random_events` — put `weight_multiplier = { ... }` in the event instead.
- Registered events must be `is_triggered_only = yes`.
- Add `pre_triggers` to planet, pop, system, starbase, and leader events registered here.

`on_actions` are also available through most effects-bearing blocks (anomalies, edicts, policies, diplomatic actions), and through `fire_on_action`.

## Event Chains

```
begin_event_chain = { event_chain = my_chain target = root }
```

Chains are declared in `common/event_chains/*.txt` (FIOS) and store an image plus referenceable counters. Add `create_point_of_interest` for a situation-log entry.

## Anomalies

- `common/anomalies/*.txt` (LIOS) defines **categories** discovered by science ships.
- `events/` defines the **anomaly events** fired when a discovery is investigated.

Category fields: `should_ai_use` (default no), `should_ai_and_humans_use` (overrides the former), `null_spawn_chance` (0–1 chance of *not* spawning), `max_once` (per empire, default no), `max_once_global` (default no), `spawn_chance` (weights), `on_success` pointing at the anomaly event.

Spawn mechanics are hardcoded: found in `00_defines.txt` as `ANOMALY_SPAWN_CHANCE = 0.050` and `ANOMALY_SPAWN_CHANCE_INCREMENT = 0.005` (increases per failure until an anomaly spawns). Only the first survey of a body by any empire rolls.

Placement rules: only valid where the category's conditions allow; vanilla restricts most narrative categories to humans and gives AI a separate file, `99_anomaly_categories_ai.txt`.

## Special Projects

`common/special_projects/*.txt` (FIOS). Science-ship projects, often paired with anomalies and archaeological sites.

## Validation Checklist

1. Namespace declared; ID numeric and unique.
2. Registered event is `is_triggered_only = yes`.
3. Every option has `name`, and every visible event has at least one option.
4. `ai_chance` present wherever the AI can see the option.
5. All localisation keys exist: `id.name`, `id.desc`, `id.a`, `id.b`, tooltips.
6. `picture` sprite exists in a `.gfx` file.
7. `error.log` clean after firing the event in-game.