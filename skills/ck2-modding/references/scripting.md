# Scripting: Syntax, Scopes, Conditions, Commands, Storage

## Syntax Fundamentals

Clausewitz script for CK2 is a brace-delimited key/value language in plain `.txt` files.

```
key = value
key = { ... }
key = { a b c }        # whitespace-separated list
```

- `#` starts a comment to end of line.
- One tab per indent level; matching braces at the same column is the fastest syntax check.
- Quotes are only mandatory when a value contains spaces, but vanilla quotes most strings. Never quote an identifier that the engine expects unquoted.
- `=` is overloaded: it assigns a value, opens a block, evaluates a condition, executes a command, and changes a scope. It is not assignment in the programming sense.
- `yes`/`no` are booleans. Numbers are integers or floats.
- Dates use `YYYY.MM.DD` from `1.1.1`; negative dates are not handled.
- Colours are `{ R G B }` with 0–255 for titles and 0.0–1.0 in culture and religion files. Hexadecimal `0xff0000` is accepted in some places.
- Encoding is ANSI (Windows-1252), never UTF-8.

An entity is a block whose grammar depends on the folder it lives in: `common/religions` defines religion groups, `events/` defines events, `decisions/` defines decisions. The same `key = { }` form means different fields per folder.

## Value Types

| Type | Form | Example |
|------|------|---------|
| bool | `yes` / `no` | `only_playable = yes` |
| int | digits | `martial = 8` |
| float | decimal | `factor = 0.5` |
| date | `YYYY.MM.DD` | `1066.9.15 = { birth = yes }` |
| string | quoted when spaced | `name = "Harold"` |
| colour | `{ R G B }` or hex | `color = { 255 255 0 }` |
| clause | block with condition-specific parameters | `death = { death_reason = death_battle killer = 140 }` |
| ID | bare identifier referencing another definition | `religion = catholic` |

## Conditions and Commands

- **Conditions** (also called triggers) test state and evaluate to yes/no: `trait = genius`, `age >= 16`, `has_character_flag = my_flag`.
- **Commands** (also called effects) change state: `add_trait = genius`, `wealth = 100`, `character_event = { id = mymod.1 }`.
- `any_*` blocks are conditions; `random_*` blocks are commands. Mixing them is the most common silent failure.
- A condition or command is only evaluated if its scope exists. Use this deliberately: `religion_head = { ... }` runs only for religions that have a head, and `always = yes` inside a scope tests existence.

## Operators

| Operator | True when |
|----------|-----------|
| `AND = { ... }` | All enclosed conditions are true; implicit after a scope change |
| `OR = { ... }` | At least one is true |
| `NOT = { ... }` | The enclosed condition is false |
| `NOR = { ... }` | None are true; preferred over nested `NOT`/`OR` |
| `NAND = { ... }` | At least one is false |
| `calc_true_if = { amount >= 3 ... }` | At least `amount` enclosed conditions are true |

Numeric comparisons, generalised in 2.8:

| Operator | Meaning | Note |
|----------|---------|------|
| `=` | Greater or equal | Legacy behaviour; `ai_greed = 5` means "at least 5" |
| `<` `>` `<=` `>=` | Strict comparisons | — |
| `==` | Exact equality | Use this when equality is meant |

`tier` and `among_most_powerful_vassals` still treat `=` as equality for backward compatibility.

## Control Flow

```
if = {
    limit = { ... }
    # commands
}
else_if = {
    limit = { ... }
    # commands
}
else = {
    # commands
}
```

```
trigger_if = {
    limit = { is_female = yes }
    NOR = { religion_group = muslim has_religion_feature = religion_patriarchal }
}
trigger_else = {
    NOT = { has_religion_feature = religion_matriarchal }
}
```

`trigger_switch` (2.4) selects one branch by a condition value; the first matching value wins and `fallback` runs when none match. It does not accept scripted triggers as the tested value.

```
trigger_switch = {
    on_trigger = religion_group
    christian = { wealth = 100 }
    muslim    = { piety = 100 }
    fallback  = { prestige = 100 }
}
```

`break = yes` returns from the current block, skipping everything after it. `while` loops on `limit`, or a fixed `count` (2.8), or both — whichever ends first; the fail-safe stops at 100,000 iterations. `while` produces no tooltip.

```
while = {
    count = 20
    wealth = 5
}
```

## Scopes

Ten scope types can be created from script: `character`, `title`/`holding`, `province`, `war`, `siege`/`flank`, `unit`, `religion`, `culture`, `society`, `artifact`, plus the special `portrait` scope used in portrait rendering rules.

Structural scopes:

| Scope | Meaning |
|-------|---------|
| `ROOT` | The object the event, decision, or command chain started from |
| `FROM` | The caller's scope; `FROMFROM`, `FROMFROMFROM` walk further back |
| `PREV` | The previously scoped object; `PREV` chains with `PREVPREV` |
| `THIS` | The current scope, explicit form |

Scope semantics:
- In a **condition** block, a scope evaluates true if at least one object inside it matches all enclosed conditions.
- In a **command** block, the commands apply to every matched object, filtered by the optional `limit`.
- `count = N` on an `any_` scope means "at least N" as a condition and "at most N, in load order" as a command. It is not randomised.
- `random_` scopes only exist in command blocks.
- Direct-ID scoping exists for characters (`c_12345 = { }`) and for titles and provinces by their identifiers.

Modifiers on selection:

```
random_independent_ruler = {
    limit = { wealth < 1000 }
    preferred_limit = { culture = norwegian }
    preferred_limit = { culture_group = north_germanic }
    wealth = 1000
}
```

`preferred_limit` (on `random_` scopes) takes the first tier that matches at least one candidate, falling back progressively.

```
any_society_member = {
    score_value = {
        value = 1
        additive_modifier = { society_rank == 4 value = 1000 }
        additive_modifier = { society_rank == 3 value = 100 }
    }
    count = 3
    add_trait = maimed
}
```

`score_value` ranks candidates; keep reusable score blocks in `common/scripted_score_values/`.

Guidance:
- Tooltips inside `any_` scopes describe one arbitrary candidate and can be misleading; override them with `custom_tooltip`.
- Dead characters need the `_even_if_dead` scope variants (`any_child_even_if_dead`) and may still reject some inner scopes.
- `any_character`, `any_allied_character`, and `any_claimant` are expensive; avoid them in polled events.
- Trait scopes (`<trait_name> = { }`) require the trait to have `cached = yes`.

## Flags

Boolean, optionally dated, per-scope markers.

| Scope | Set | Check | Clear |
|-------|-----|-------|-------|
| character | `set_character_flag` | `has_character_flag` | `clr_character_flag` |
| province | `set_province_flag` | `has_province_flag` | `clr_province_flag` |
| title | `set_title_flag` | `has_title_flag` | `clr_title_flag` |
| dynasty | `set_dynasty_flag` | `has_dynasty_flag` | `clr_dynasty_flag` |
| global | `set_global_flag` | `has_global_flag` | `clr_global_flag` |
| artifact | `set_artifact_flag` | `has_artifact_flag` | `clr_artifact_flag` |
| offmap power | `set_offmap_flag` | `has_offmap_flag` | `clr_offmap_flag` |
| bloodline | `set_bloodline_flag` | `has_bloodline_flag` | `clr_bloodline_flag` |
| wonder | `set_wonder_flag` | `has_wonder_flag` | `clr_wonder_flag` |
| society | `set_flag` | `has_flag` | `clr_flag` |

Dated checks use `had_character_flag = { flag = <name> days = 365 }`, with `had_flag` and `had_bloodline_flag` variants. Event chains have no flag scope; store chain state in `local_` variables instead.

`set_flag`, `has_flag`, and `clr_flag` work on any scope that can store flags, which covers society and wonder scopes without a dedicated prefix. The prefixed forms exist to make intent explicit and, in a few cases, to reach a scope the generic form cannot address.

## Variables

Numeric values with three decimal places, range ±2,147,483.647, persisted in saves. Variables set to zero are not saved and therefore vanish on reload.

```
set_variable   = { which = myvar value = 5 }
change_variable  = { which = myvar value = 2 }
subtract_variable = { which = myvar value = 1 }
multiply_variable = { which = myvar value = 2 }
divide_variable   = { which = myvar value = 2 }
modulo_variable   = { which = myvar value = 2 }
check_variable  = { which = myvar value >= 3 }
wealth = myvar                       # use a variable as a command value
```

Variants of the second parameter:
- literal value: `value = 5`
- another variable in the same scope: `which = other_var`
- a scope holding a variable of the same name: `which = FROM`

Prefixes select the storage location:
- `global_` — global scope, comparable across scopes (2.7)
- `local_` — event-chain scope, alive only for the duration of the chain (2.8)

`export_to_variable` copies a game value into a variable, with an optional `who` scope:

```
ROOT = {
    export_to_variable = {
        which = myvar
        value = stewardship
        who = FROM
    }
}
```

Exportable values include the five attributes, `age`, `health`, `fertility`, `wealth`, `scaled_wealth`, `piety`, `prestige`, `decadence`, `monthly_income`, `yearly_income`, `realm_levies`, `demesne_size`, `num_of_*` counts, `combat_rating`, `society_currency`, and the date parts `day`, `month`, `year`. Check the shipped `Commands` page for the current list before relying on one.

## Event Targets

```
ROOT = {
    save_event_target_as = target_adulterer     # chain-scoped
}
event_target:target_adulterer = {
    add_character_modifier = { name = adulterer years = 10 }
}
```

- `save_event_target_as` dies with the event chain; `save_global_event_target_as` survives it for the session.
- `event_target:<name>` scopes to the saved object in script; in localisation the name is used bare: `[target_adulterer.GetFullName]`.
- A target saved in one event can be used in that event's own tooltip, which ordinary effects cannot.

Persistent targets are attached to an object instead of a chain:

```
save_persistent_event_target = {
    name = coronation_character
    scope = event_target:my_character
}
persistent_event_target:coronation_character = { ... }
clear_persistent_event_target = coronation_character
```

- The holder must be a character, province, title, artifact, society, or offmap power, and the target survives new event chains until cleared or, for characters, until the holder dies.
- In localisation, `[coronation_character.GetFullName]` resolves; a same-named chain target takes precedence over a persistent one.

Deferred work uses a delayed event (`character_event = { id = … days = N }`) or, inside a chain, `repeat_event`. There is no timer scope in CK2.

## Stored-Information Matrix

| Storage | Global | Event chain | Character | Province | Title | Dynasty | Artifact | Society |
|---------|--------|-------------|-----------|----------|-------|---------|----------|---------|
| variable | `global_` | `local_` | yes | yes | yes | no | yes | yes |
| flag | yes | no | yes | yes | yes | yes | yes | yes |
| modifier | no | no | yes | yes | no | yes | no | yes |
| event target | global | yes | persistent | persistent | persistent | no | persistent | persistent |

Use the matrix before inventing storage; storing on the wrong scope silently fails.

## Scripted Triggers and Effects

Put reusable fragments in `common/scripted_triggers/` and `common/scripted_effects/`. They behave like built-ins, accept `$parameter$` substitution, and are the correct home for logic used by more than one event or decision.

```
# common/scripted_triggers/my_triggers.txt
is_my_valid_target = {
    is_alive = yes
    age >= 16
    NOT = { trait = incapable }
}

# common/scripted_effects/my_effects.txt
grant_my_reward = {
    add_trait = brawny
    wealth = $amount$
}
```

Cautions:
- Redefining a scripted trigger **appends** its conditions instead of replacing them, so a patched scripted trigger inherits the old checks.
- `trigger_switch` cannot test a scripted trigger.

## Performance Rules

1. Polled events evaluate their `trigger` for every eligible character. Use filtering pre-triggers first, then a cheap `trigger`.
2. Prefer `is_triggered_only = yes` plus an on_action, decision, or gatekeeper event over MTTH polling.
3. Use `weight_multiplier` for on_action events; MTTH there is both wrong and slow.
4. Avoid `any_character`, `any_allied_character`, `any_claimant`, `any_realm_character`, and `any_demesne_title` inside polled events.
5. `triggered_modifiers` run daily for every landed character; each one added is a permanent cost.
6. Keep `scripted_effects` and `scripted_triggers` short when they sit on hot paths: they are inlined at every call site.
7. `while` loops with no `count` and a mutable `limit` can hang the game; prefer `count`.