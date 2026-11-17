# Events, On Actions, and Decisions

## Event Types

| Type | ROOT scope | Notes |
|------|-----------|-------|
| `character_event` | character | Standard popup |
| `long_character_event` | character | Taller popup |
| `letter_event` | character | Shows a sender; frame keys differ |
| `narrative_event` | character | Ornamented first letter; requires `title` |
| `province_event` | province | Fires to the owner but ROOT is the province; never fires for ownerless provinces |
| `diploresponse_event` | character | Notification for hardcoded diplomatic decisions; `FROM` receives, `FROMFROM` sends; on_action only |
| `unit_event` | unit | `ROOT` is the unit only from `on_entering_port`; on_action only |
| `society_quest_event` | character | Allows `quest_target`, set in `immediate` |

Event IDs must be globally unique. Namespaces remove collision risk and are declared once per file:

```
namespace = mymod

character_event = {
    id = mymod.0001
    desc = EVTDESCmymod.0001
    option = { name = EVTOPTAmymod.0001 }
}
```

- The namespace must be re-declared in **every** file that uses it.
- Namespaces resolve to numeric ranges at load, so IDs without a namespace must stay below 999,999 and IDs inside a namespace below 99,999.
- IDs cannot contain letters after the dot; such an ID collapses to `namespace.0`.
- Leading zeros are truncated: `mymod.003` is `mymod.3`.
- `EVTDESC` and `EVTOPT` prefixes are convention, not requirement, but keep a single naming scheme per mod.

## Event Structure

```
namespace = mymod

character_event = {
    id = mymod.1
    title = TITLE_KEY                 # mandatory for narrative_event
    desc = EVTDESCmymod.1
    picture = GFX_evt_battle
    border = GFX_event_normal_frame_war

    only_playable = yes               # pre-trigger
    min_age = 16                      # pre-trigger

    is_triggered_only = yes
    hide_window = yes                 # optional; suppress the popup

    trigger = { ... }                 # eligibility
    immediate = { ... }               # before the window renders
    after = { ... }                   # after any option is chosen
    fail_trigger_effect = { ... }     # when an attempted trigger fails

    option = {
        name = EVTOPTAmymod.1
        trigger = { ... }             # option visibility
        ai_chance = { factor = 10 }
        # commands
    }
    option = { name = EVTOPTBmymod.1 }
}
```

Field behaviour:
- `desc` accepts a key, a list of keys (one is picked at random), or `desc = { trigger = { ... } text = KEY }` blocks (random among those whose trigger passes; the first block shows if none pass).
- `picture` accepts a `GFX_` key, a list, or `picture = { trigger = { ... } picture = GFX_... }` blocks since 3.0. Description-level pictures take precedence over top-level ones.
- A dynamic `picture` needs a default top-level `picture` anyway.
- `immediate` runs before title and description are resolved; commands fired here inherit the current scopes rather than copying them, which matters with event targets.
- `after` runs once, after whichever option was chosen.
- Every visible event needs at least one option, and at most four are eligible at a time.

## Event Flags

| Flag | Effect |
|------|--------|
| `title` | Header key; mandatory for `narrative_event` |
| `window` | GUI window name from `interface/` to use instead of the default frame |
| `background` | Background graphic used with `window`; also drives `_option` button graphics when present |
| `border` | Frame graphic; must match the event type |
| `picture` | 450×150 event picture |
| `portrait` | `character`, `title`, `offmap`, or `none`; `none` replaces `hide_from = yes` |
| `hide_from` | Suppresses the FROM portrait, overriding `portrait` |
| `hide_new` | Stops newly created characters and event targets replacing ROOT's portrait |
| `hide_window` | Invisible event; options still evaluate |
| `major` | Also shows to other characters; `major_trigger` refines the audience |
| `show_root`, `show_from_from`, `show_from_from_from` | Portrait slot overrides |
| `is_friendly` / `is_hostile` | Forces compliments or insults in letter events |
| `is_triggered_only` | Cannot fire on its own; `trigger` still gates it |
| `offmap` | `allow` or `only` — whether offmap rulers can receive it |
| `triggered_from_code` | Tutorial events referenced from defines |
| `sound` | `sfx` to play |
| `notification` | Respects the player's message settings; unsuitable for events with meaningful options |

`major = yes` changes scope semantics inside `major_trigger`, the description, and options: the default scope is the notified character while `ROOT` remains the original target. `trigger` and `immediate` are unaffected.

## Pre-Triggers

Pre-triggers are evaluated before the `trigger` block and can eliminate an event before any condition is checked. Use them in every polled event.

Filtering pre-triggers (most effective, evaluated in list order):

| Pre-trigger | Restricts to | Equivalent condition |
|-------------|--------------|----------------------|
| `ai` | AI only (`yes`) or player only (`no`); implies playable | `ai` |
| `is_patrician` | Patricians; implies playable | `is_patrician` |
| `only_independent` | Independent rulers; implies playable | `independent` |
| `only_playable` | Count tier or above and not a landless rebel | `is_playable` |
| `is_part_of_plot` | Plot leaders and backers | `has_plot` |
| `only_rulers` | Any landed character | `is_ruler` |
| `religion` / `religion_group` | Members of one religion or group | same |

Cheap additional pre-triggers: `min_age`, `max_age`, `only_men`, `only_women`, `only_capable`/`capable_only`, `has_dlc`, `lacks_dlc`, `friends`, `rivals`, `prisoner`, `is_married`, `has_global_flag`, `war`, `culture`, `culture_group`, `is_in_society`, `has_quest_target`, `has_job_title`.

Documented defects:
- `is_female` raises an error in `error.log`; use `only_men` / `only_women`.
- `in_command` is unreliable.
- `is_sick` is undocumented and unverified.
- More than one `has_character_flag` or `has_global_flag` pre-trigger in one event raises an error.
- Some pre-triggers use different names from the equivalent condition; check the table rather than assuming.

## Mean Time to Happen

```
mean_time_to_happen = {
    months = 6
    modifier = { factor = 2   has_character_flag = cautious }   # halves the chance
    modifier = { factor = 0.5 is_ambitious = yes }              # doubles the chance
}
```

- Units: `days`, `months`, `years`.
- MTTH of 90 days means a 50% chance per 90 days per eligible object.
- Rules: every non-triggered event needs MTTH; triggered-only events must not have it; on_action events must use `weight_multiplier` instead.
- Adding any `modifier` switches the engine to daily re-evaluation per scope, which is markedly more expensive than a bare MTTH.

## Weight Multiplier

`weight_multiplier` replaces MTTH for on_action events. Its modifiers increase the chance of firing instead of shortening the wait, and the engine handles it far more cheaply than a tiny MTTH.

```
weight_multiplier = {
    days = 1
    modifier = { factor = 3 trait = wounded }
}
```

## Options

```
option = {
    name = EVTOPTAmymod.1
    trigger = { stewardship >= 8 }
    ai_chance = {
        factor = 10
        modifier = { factor = 0 trait = gregarious }
    }
    wealth = 200
    character_event = { id = mymod.2 days = 30 tooltip = EVTTOOLTIPmymod.2 }
    set_character_flag = loan_taken
}
```

- The only mandatory field is `name`.
- `name` may also be `name = { trigger = { ... } text = KEY }` blocks, resolved the same way as descriptions.
- `ai_chance` weights options; each option's base `factor` is scaled by its modifiers, and one option is picked by weighted random.
- For `province_event` options, the deciding AI is not `ROOT`: wrap owner conditions in `owner = { ... }` or leave them unwrapped, and do not attempt to test the province itself.
- Option borders and explanation tooltips:
  - `tooltip_info = <trait>` — yellow border and trait tooltip
  - `tooltip_info = martial | diplomacy | intrigue | stewardship | learning` — attribute-coloured borders
  - `tooltip_info = combat_rating` — combat icon
  - `tooltip_info_modifier = <event_modifier>` — yellow border, no icon
  - `tooltip_info = yes` — yellow border only
  - `tooltip_info_custom = <loc_key>` — yellow border with a custom tooltip
- Trait icons added or removed by the option show automatically; `show_trait` adds icons for traits applied later in the chain.

## Option Portraits

- A visible, single-target command in an option shows that character's portrait automatically.
- `hidden_tooltip = { ... }` suppresses the automatic portrait.
- `show_portrait = event_target:foo`, `show_portrait = FROMFROM`, and `show_portrait = <link>` force a portrait.
- The character shown at the top-left (ROOT) and top-right (FROM) can never appear in an option portrait.
- At most ten portraits per option; more than ten `show_portrait` calls removes all of them.
- Portrait order is not controllable.
- A visible single-target command in `immediate` or `after` puts that portrait on **every** option; move such work into `hidden_tooltip` or a separate hidden event.

## Techniques

**Ping event** — moving a character into FROM:

```
# ROOT is A; FROM is A
character_event = {
    id = mymod.1
    option = {
        name = OK
        random_realm_character = {
            character_event = { id = mymod.2 }   # ROOT is B, FROM is A
        }
    }
}

character_event = {
    id = mymod.2                             # ROOT is B, FROM is A
    hide_window = yes
    immediate = { FROM = { character_event = { id = mymod.3 } } }
}

character_event = {
    id = mymod.3                             # ROOT is A, FROM is B, FROMFROM is A
}
```

Use a ping event to reference `any_`/`random_` candidates in localisation, to reuse a chain from several trigger sources, or to hide which character is being pinged.

**More than four options** — let the fourth option call a follow-up event with the remaining branches, and make its last option loop back.

**Recursive events** — `repeat_event = { id = <same id> days = N }` fires the event again without pushing a new FROM, which avoids stack growth.

**Turn-by-turn chains** — keep the opponent in `FROM` and alternate `repeat_event` (resolve in ROOT) with a `FROM = { character_event = ... }` (hand over the turn), so one chain serves both players and both sides of a multiplayer duel.

## On Actions

On_actions fire an event when the engine reaches a hardcoded moment (`on_marriage`, `on_battle_won`, `on_yearly_pulse`, `on_startup`, and roughly a hundred others). Register them in a new file under `common/on_actions/`; vanilla uses `00_on_actions.txt`, and files merge.

```
on_marriage = {
    effect = {
        # runs first, in the on_action's scope
    }
    events = {
        mymod.10         # always fires
        mymod.11
    }
    random_events = {
        100 = mymod.12
        50  = mymod.13
        50  = 0          # explicit chance of nothing happening
        delayed_block = {
            delay = 5    # days
            1 = mymod.14
            1 = 0
        }
    }
}
```

Semantics:
- Each on_action runs in the scope of its own ROOT object; read the scope notes for each trigger before assuming what `FROM` holds.
- Events in `events` and `random_events` must be `is_triggered_only = yes`, must not carry MTTH, and may still use `trigger`.
- Within `random_events`, only one event per named block fires; differently named blocks are independent.
- Blocks with the same name merge across files.
- Relevant pulses: `on_yearly_pulse`, `on_bi_yearly_pulse`, `on_five_year_pulse`, `on_decade_pulse`, `on_childhood_pulse`, `on_adolescence_pulse`, `on_focus_pulse`.
- Relevant lifecycle: `on_startup` (all characters, but not ruler-designed ones), `on_chronicle_start`, `on_death`, `on_birthday`.
- Relevant war: `on_combat_pulse`, `on_combat_starting`, `on_siege_pulse`, `on_battle_won*`, `on_battle_lost*`, `on_major_battle_won*`, `on_major_battle_lost*`.
- Notification triggers (`on_letter_event_message`, `on_character_event_message`) are unsynchronised; never change game state from them in multiplayer.

## Decisions

Files live in `decisions/`. Every decision must sit inside the block type matching its screen.

| Block | Screen | ROOT | Notes |
|-------|--------|------|-------|
| `decisions` / `plot_decisions` | Intrigue | Decider | Standard decisions |
| `vassal_decisions` / `dynasty_decisions` | Intrigue | Decider | Targets a vassal or dynasty member |
| `targeted_decisions` / `targetted_decisions` | Diplomacy | Target, with FROM as decider | Both spellings work |
| `settlement_decisions` | Settlement diplomacy | Target | Same structure as targeted |
| `trade_post_decisions`, `fort_decisions`, `hospital_decisions` | Respective diplomacy views | Target | Same structure |
| `title_decisions` | Title diplomacy | Title | — |
| `society_decisions` | Intrigue | Decider | Evaluated only for society members |
| `offmap_decisions` | Offmap button | Decider | Extra `button_name` field |

Structure:

```
decisions = {
    my_decision = {
        is_high_prio = yes
        ai_check_interval = 12          # months between AI checks, default 1
        potential = { ... }             # visibility to the decider
        allow = { ... }                 # selectability
        effect = { ... }                # commands
        ai_will_do = { factor = 1 }     # AI willingness, 1 = 100% per check
    }
}
```

Additional fields by kind:
- `vassal_decisions` / `dynasty_decisions`: `from_potential` (decider) plus `potential` (target).
- `targeted_decisions`: `filter` (player-facing candidate set) and `ai_target_filter` (AI candidate set), plus `ai_acceptance` for displayed AI willingness.
- Targeted decisions use `FROM` as the decider and `ROOT` as the target; that swap is the most common source of wrong-scope bugs.
- `ai_acceptance` is presentation only: only a score of zero or below mechanically blocks the decision, so script the AI response yourself.

`filter` values, in ascending cost: `self`, `spouse`, `court`, `home_court`, `vassals`, `sub_realm`, `realm`, `dynasty`, `close_relatives`, `rivals`, `friends`, `liege`, `religious_head`, `society`, `vassal_wars`, `independent_rulers`, `all`, `none`. Most add `_including_me` variants. Avoid `all`: it is evaluated per living character.

Authoring rules:
- `potential` carries cheap, stable facts; `allow` carries expensive checks.
- Any syntax error or unknown keyword breaks the whole decision section and malforms the screen headings, so validate after every edit.
- `is_high_prio = yes` raises an alert when the decision becomes available; use it sparingly.
- Keep `ai_check_interval` above 1 month for expensive decisions.
- Register decision localisation as `<decision>`, `<decision>_desc`, and optionally `<decision>_desc_extra`.
- The icon is a `spriteType` named `GFX_<decision_name>` in an `interface/*.gfx` file; vanilla icons are 28×28 `.dds` with a transparent background and a 24×20 glyph inside a 2px border.