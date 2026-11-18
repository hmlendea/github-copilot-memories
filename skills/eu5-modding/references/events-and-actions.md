# Events, Namespaces, Options, On Actions, Situations, Disasters, Missions, and Resolutions

## Events

**Folder:** `events/` (subfolders allowed; subfolders always load after top-level files).

**File structure:**
```
namespace = my_events

scripted_trigger my_custom_gate = {
    ...
}

scripted_effect my_custom_apply = {
    ...
}

my_events.1 = {
    ...
}
```

### Event definition

```
my_events.1 = {
    type = country_event                  # country_event / location_event / exploration_event / age_event
    category = situation_event            # situation_event / io_event / disaster_event (optional)

    title = my_events.1.title              # localisation key
    desc = my_events.1.desc                # localisation key
    historical_info = my_events.1.historical_info  # optional

    trigger = {                            # optional; defaults to always true
        is_subject = no
    }

    fire_only_once = yes                   # global one-shot lock (under the hood: global variable <event>_fire_only_once)
    orphan = yes                           # suppress "not fired from a known source" error; use for console-debug events
    hidden = yes                           # skip window, apply option silently
    major = yes                            # announce to qualifying countries via major_trigger
    interface_lock = no                    # prevent default game pause

    immediate = {                          # effects executed before the window renders; not tooltipped
        ...
    }

    after = {                              # effects executed after any option is selected; tooltipped in each option
        ...
    }

    option = {
        name = my_events.1.a
        historical_option = yes
        trigger = { prestige >= 25 }
        ...
    }
}
```

### Event types

| Type | Root Scope | Notes |
|------|------------|-------|
| `country_event` | `country` | Default type for country events |
| `location_event` | `location` | Fired for locations |
| `exploration_event` | `exploration` | Used by `on_exploration_monthly_pulse` |
| `age_event` | `country` | Used exclusively by `ages_of_eu.1`; has special graphics |
| `unit_event` | `unit` | Declared but unused in vanilla |

If `type` is omitted, the event likely defaults to `country_event`.

### Event categories

| Category | Icon Path |
|----------|-----------|
| `situation_event` | `gfx/interface/icons/situations/` |
| `io_event` | `gfx/interface/icons/international_organizations/` |
| `disaster_event` | `gfx/interface/icons/disasters/` |

### Dynamic titles, descriptions, and historical info

Use `first_valid`, `random_valid`, or `switch` inside `title`, `desc`, and `historical_info`:

```
title = {
    first_valid = {
        triggered_desc = {
            desc = my_events.1.title_rich
            trigger = { gold >= 1000 }
        }
        desc = my_events.1.title_poor
    }
}
```

These blocks can be nested. `triggered_desc` uses `desc = <key>`, even inside `title`.

### Dynamic historical events

```
my_events.1 = {
    dynamic_historical_event = {
        tag = POL                    # repeatable; event can fire for any listed tag
        from = 1444.1.1              # earliest date
        to = 1500.1.1                # latest date
        monthly_chance = 10          # 10% chance per month
    }
    fire_only_once = yes             # required or the game prints an error
}
```

### Major events

A `major = yes` event announces to all countries that satisfy `major_trigger`:
```
my_events.1 = {
    major = yes
    major_trigger = {
        gold >= 100
        "opinion(scope:from)" > 100  # scope:from = the country that received the original event
    }
}
```

### Event options

```
option = {
    name = my_events.1.a             # localisation key
    historical_option = yes          # historical AI always picks this when available
    trigger = { prestige >= 25 }     # option only visible/selectable when true
    ai_will_select = { value = 100 } # AI weight (takes precedence over ai_weight if both are set)
    # ai_weight = { base = 100 }     # alternative MTTH-style weight
    # custom_tooltip = my_events.1.a.tt  # tooltip content is rendered by custom_tooltip, not by any .tt auto-pickup

    add_gold = 25                    # effects on selection
}
```

- Only 5 options are visible at once; extra options are scrollable.
- Option `name` supports dynamic selection by multiple `name = { text = key trigger = { ... } }` blocks; if multiple triggers pass, one is chosen at random.
- Unused but GUI-readable flags: `moral_option`, `evil_option`, `high_risk_option`, `high_reward_option` (readable via `EventOption.IsMoral`, etc. in GUI).

### Modifying base-game events

`INJECT:` and `REPLACE:` **do not work** for events. To alter an event:
1. Create a new file in `events/` whose name sorts alphabetically **before** the vanilla file (`0000_modded_events.txt`).
2. Declare the same `namespace = <vanilla_namespace>` at the top.
3. Copy the specific modified event (`earthquake_events.1`, etc.) into the new file.
4. Copy any inline scripted effects or triggers used by the event **by content**, or copy and rename them.
5. Accept that `error.log` will show `Duplicated event ID` for each modified event; this is expected and harmless.

Subfolders always load after top-level files, so a subfolder event file never wins against a top-level vanilla file.

### Firing events

- `trigger_event = my_events.1` — from effects.
- `on_trigger_fail = { trigger_event = ... }` — fires a cleanup/notification event if the trigger fails.
- `fire_example_event = yes` — custom scripted-effect-style form (defined in script).
- Console: `event my_events.1`.

## On Actions

**Folder:** `common/on_action/` (singular; the wiki path in one page says `on_actions`, but vanilla and community mods use `on_action`).

### Structure

```
on_action_name = {
    trigger = { ... }                  # optional gate

    weight_multiplier = {              # used when this on_action is a candidate in random_on_action
        base = 1
        modifier = {
            add = 1
            trigger = ...
        }
    }

    events = {                         # all listed events fire if triggers pass
        event_id.1
        delay = { days = 365 }
        event_id.2
        delay = { months = { 6 12 } }
        event_id.3
    }

    random_events = {                  # exactly one event fires by weighted random
        chance_to_happen = 25
        chance_of_no_event = {
            value = 0
            if = { limit = { ... } add = 10 }
        }
        # sample_count = 3             # only evaluate this many, for performance
        100 = event_id.1
        200 = event_id.2
        100 = 0                        # chance no event fires
    }

    first_valid = {                    # first event whose trigger passes
        event_id.1
        event_id.2
        fallback_event
    }

    on_actions = {                     # fire other on_actions
        child_on_action
    }

    random_on_action = {               # weighted pick
        100 = child_on_a
        200 = child_on_b
        100 = 0
    }

    first_valid_on_action = {
        child_on_a
        child_on_b
    }

    effect = { ... }                   # runs concurrently with fired events; separate chain
    fallback = some_other_on_action    # called if nothing else fired; avoid infinite loops
}
```

### Modding on actions

Only an `on_actions` block can be added to an existing on_action. Restating `trigger` or `effect` errors and overwrites the vanilla block.

Correct pattern:
```
monthly_country_pulse = {
    on_actions = {
        my_mod_monthly
    }
}

my_mod_monthly = {
    effect = { ... }                   # separate chain
    events = { my_events.1 }
}
```

Compatibility note: Use a unique prefix on the child on_action name. `monthly_country_pulse`, `yearly_country_pulse`, and similar pulses merge their `on_actions` list across mods, so do not copy vanilla or framework entries just to preserve them.

### Parallelisation

The `events` block of an on_action is parallelised across scopes (one thread per scope). The `effect` block is not. Using an event to apply effects to many scopes simultaneously is often faster than using the `effect` block of the same on_action.

### Known on_actions

| Name | Scope | Fires |
|------|-------|-------|
| `monthly_country_pulse` | country | monthly |
| `yearly_country_pulse` | country | yearly |
| `four_yearly_country_pulse` | country | once every 4 years |
| `biyearly_country_pulse` | country | once every 2 years |
| `government_flavor_pulse` | country | periodic government flavour |
| `country_pulse_for_high_infamy` | country | when infamy high |
| `on_game_start` | global | game start |
| `on_exploration_monthly_pulse` | exploration | monthly |
| `earthquake_location_pulse` | location | monthly, one random location |
| `in_battle` | character | per tick while commander of a battle |
| `in_regency_yearly_pulse` | country | yearly while in regency |
| `on_accepted_call_to_arms` | country | call-to-arms accepted |
| `colonial_charter_monthly_pulse` | country + `scope:target` = colonial_charter | monthly |

Retrieve the authoritative list with `script_docs`; the wiki list lags patches.

## Situations

**Folder:** `common/situations/`

```
example_situation = {
    monthly_spawn_chance = 1

    can_start = {
        country_exists = c:FRA
        current_year >= 1400
    }

    can_end = {
        OR = {
            current_year > 1500
            NOT = { country_exists = c:FRA }
        }
    }

    visible = {
        exists = c:FRA
        knows_country = c:FRA
    }

    on_start = {
        set_variable = {
            name = targetted_country
            value = c:FRA
        }
    }

    on_monthly = {
        var:targetted_country = {
            random_list = {
                11 = { }
                1 = { fire_example_situation_event = yes }
            }
        }
    }
}
```

- Situations are a valid scope and can hold variables even while inactive.
- Activated when `can_start` passes, or forcefully via `activate_situation`.
- Ended when `can_end` passes, or forcefully via `end_situation`.
- Icon path uses `SITUATION_ICON_PATH` define.

## Disasters

**Folder:** `common/disasters/`

```
example_disaster = {
    monthly_spawn_chance = 1

    can_start = {
        stability <= 25
        current_year >= 1400
    }

    modifier = {
        monthly_stability = -0.1
    }

    can_end = {
        OR = {
            current_year > 1500
            var:target_var >= 90
        }
    }

    on_start = { set_variable = { name = target_var value = 0 } }
    on_monthly = {
        random_list = {
            11 = { }
            1 = { fire_example_disaster_event = yes }
        }
    }
    on_end = { remove_variable = target_var }
}
```

- `can_start` and `on_start` run in `country` scope.
- Once a disaster ends naturally, it cannot refire without a forceful effect or console command.
- Icon path uses `DISASTER_ICON_PATH` define.

## Missions

**Folder:** `common/missions/`

```
mission_pack_name = {
    icon = mission_icon_name
    repeatable = yes
    player_playstyle = administrative

    visible = {
        game_has_missions_enabled = yes
        has_enabled_mission_trigger = { type = mission_pack_name }
    }

    enabled = {
        exists = capital.market
    }

    chance = 3600                        # AI weight

    select_trigger = {
        looking_for_a = market
        target_flag = mission_target_market
        name = "mission_select_market"
    }

    on_start = { ... }
    on_completion = { ... }
    on_abort = { ... }

    mission_task_name = {
        icon = task_icon
        requires = { previous_task }
        enabled = { ... }
        duration = 365
        on_completion = { ... }
    }
}
```

## Resolutions

Resolutions use two distinct AI script values:
- `ai_will_propose` — probability weight for proposing.
- `ai_will_do` or `ai_vote_weight` — weight for voting.

There is no `ai_will_select` field for resolutions; a player-only resolution can set both documented values to `0` to suppress AI proposals and votes.