# Actions and Interactions: Generic Actions, Character and Country Interactions, Cabinet Actions, and Scripted GUIs

## Common Action Syntax

**Folders:** `common/generic_actions/`, `common/character_interactions/`, `common/country_interactions/`, `common/cabinet_actions/`.

All action types share a common syntax skeleton:

```
my_action = {
    potential = { ... }                   # scope:actor precheck; controls whether the action is listed
    allow = { ... }                       # scope:actor; controls whether activation succeeds

    effect = { ... }                      # scope:actor, plus selection targets

    # --- Interaction target ---
    select_trigger = {
        looking_for_a = country           # country / province / location / value / market / ...
        source = actor                     # optional: source the candidates from this scope
        target_flag = target_country       # name the selection for scope:target_country
        name = "select_country"            # localisation key for the picker header
        none_available_msg_key = "no_countries_available"
        visible = { ... }                  # per-candidate visibility
        enabled = { ... }                  # per-candidate enabled check
        show_if = { ... }                  # whether the picker itself should be available
        show_why_not_visible = yes         # default; if candidates are visible=false, show visible triggers in tooltip
        show_why_not_enabled = yes         # default; if candidates are enabled=false, show enabled triggers
        allow_null = yes                   # adds "None" option; skips setting target_flag
        allow_self = yes                   # includes the actor country in the candidates
    }

    # --- AI ---
    ai_chance = { ... }                    # MTTH-style weighting
    ai_will_do = { ... }                   # script value weighting

    # --- Cost / restrictions ---
    price = { ... }                        # link to common/prices/ if used
    cooldown = { ... }
    exclusive_group = my_group             # only one action per group is shown at a time
}
```

### `potential`, `allow`, and `effect` scopes

- `potential` and `allow` receive `scope:actor`.
- `effect` receives `scope:actor` **and** every `scope:<target_flag>` from `select_trigger` blocks.

### Interaction targets

`select_trigger` displays a picker, optionally constrained by `visible` and `enabled` triggers. The picked object is saved under `target_flag` and referenced as `scope:target_flag`.

`looking_for_a` accepts:
- `country`, `province`, `location`, `market`, `value`, and many scope types
- `value` is a lesser-known but valid target for numeric input

Candidate sourcing:
- Without `source`, the engine gathers all possible candidates, which is expensive.
- With `source = actor`, candidates are gathered from the actor's scope chain, which is cheaper and often more sensible.

Per-candidate conditional behaviour:
```
select_trigger = {
    looking_for_a = province
    source = actor
    target_flag = target
    visible = {
        NOT = {
            any_location_in_province = {
                percent = 1
                development = 100
            }
        }
    }
    show_if = { scope:actor = { num_provinces > 1 } }
    enabled = { population >= 10 }
}
```

## Generic Actions

**Folder:** `common/generic_actions/`

Generic actions are the most basic action implementation. Their `type` field determines their UI behaviour:

| `type` | Recipient Required | Recipient Scope | Use |
|--------|--------------------|-----------------|-----|
| `owncountry` | Forbidden | N/A | Default; self-targeting actions |
| `country` | Required | country | Diplomatic actions targeting another country |
| `province` | Required | province | Actions targeting a province |
| `location` | Required | location | Actions targeting a location |
| `character` | Required | character | Actions targeting a character |

Other generic action fields:
- `generic_action_list` in `common/generic_action_ai_lists/` controls AI usage of action lists.
- GUI references use `GenericAction` data types (e.g., `GenericAction.IsVisible`, `GenericAction.Execute`).

### Cabinet actions

**Folder:** `common/cabinet_actions/` — modelled on generic actions with additional research/cabinet fields:
- `cabinet` slot targeting and assignment.
- `action_progress` and progression tracking.
- `modifier` applied while the cabinet action is active.

### Character interactions

**Folder:** `common/character_interactions/`

Same skeleton, with `scope:recipient` and `scope:actor` for the two characters; no `root`.

### Country interactions

**Folder:** `common/country_interactions/`

Same skeleton, plus diplomacy-specific fields:
- `interaction_type` — determines category (diplomatic, subject, war-coordination, etc.)
- `target_country` — usually `scope:recipient`.
- `acceptance` — scripted acceptance score modifier for AI and UI.
- `rejection` — rejection reason script value.
- `diplomat_cost` — link into `common/diplomatic_costs/`.
- `diplomatic_cost` — direct cost definition or script value.

## Scripted GUIs

**Folder:** `common/scripted_guis/`

Scripted GUIs bind triggers and effects to GUI elements, allowing UI elements to execute script.

```
my_sgui = {
    scope = country                       # country / character / location / etc.

    is_shown = { ... }                    # trigger: element is visible
    is_valid = { ... }                    # trigger: element can be activated

    effect = { ... }                      # effect executed on activation

    saved_scopes = { scope1 scope2 }      # scopes saved for use in triggers/effects
    notification_key = my_notification    # optional notification message

    confirm_title = { ... }               # optional confirmation window title
    confirm_text = { ... }                # optional confirmation window text

    ai_is_valid = { ... }                 # trigger: AI can activate
    ai_chance = { ... }                   # MTTH value 1–100: AI activation weight
    ai_frequency = { ... }                # script value: months between AI evaluations
}
```

Scripted GUIs are typed keyed-database entries: a compatibility submod must not copy another mod's `<mod_id>__<setting_id>_on_changed` definitions merely to register the corresponding setting. Use an explicit `REPLACE:` or a distinct key when behaviour actually changes.

## Scripted Widgets

**Folder:** `in_game/gui/scripted_widgets/`

Files here register `.gui` windows for scripted visibility toggling:
```
gui/my_mod_interface.gui = my_mod_window
```
Without this registration, the window only opens via console command (`GUI.CreateWidget`).

## Cooldowns, Prices, and Exclusive Groups

- `cooldown = { days = <n> }` for action availability locks.
- `price = { gold = 50 }` or a link to a named price object in `common/prices/`.
- `exclusive_group = <group>` groups actions in a dropdown menu; only one action per group is displayed at once.

## Trace and Debugging

- Use `GenericAction.Execute` (or the action-specific data function) from GUI to fire the action.
- `error.log` records unknown scope links, missing `select_trigger` targets, and `ai_*` block misuses.

## Compatibility Notes

- `INJECT:`/`REPLACE:` entries are keyed to the action key.
- Multiple `select_trigger` blocks in the same action are additive if the game supports them (documented for generic actions).
- For multi-mod safety, prefix any new action keys with your mod identifier.
- When replacing an action to remove a feature, also remove all references to it in GUI files; otherwise the tooltip renders an empty or broken action button.