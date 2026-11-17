# Scripting: Effects, Triggers, Conditions, Scopes, and Scripting Model

## Syntax Fundamentals

Clausewitz script is a brace-delimited key/value language with no statement terminators.

```
key = value
key = { ... }
key = { a b c }        # whitespace-separated list
```

- `#` starts a comment, to end of line.
- Indent with tabs (vanilla convention); matching braces at the same column is the single most effective syntax check.
- Strings are quoted only when they contain spaces or need to be treated as localisation keys; identifiers and keys are bare.
- `=` is overloaded: it assigns a value, opens a block, activates an effect, evaluates a trigger, and changes a scope. Do not read it as assignment.
- `yes`/`no` are the booleans; bare numbers are fixed-point decimals.
- `@name = value` declares a file-local scripted variable; `[ ... ]` is localisation bracket syntax and does not exist in script.
- A file may define `@` variables anywhere above first use; they cannot cross files unless declared in `common/scripted_variables/`.

Vanilla example, showing flow control mixed with game concepts:

```
capital_scope = {                       # scope change: country -> planet
    every_deposit = {                   # effect: iterate deposits
        limit = { category = deposit_cat_blockers }
        remove_deposit = yes
    }
}
```

## Effects vs Triggers

- **Effects** change state: `set_country_flag`, `add_resource`, `create_fleet`, `every_owned_planet`.
- **Conditions/triggers** test state and evaluate to yes/no: `has_country_flag`, `num_pops > 10`, `any_owned_planet`.
- `every_*` and `random_*` are effects; `any_*`, `all_*`, `count_*` are conditions/triggers. Mixing them is the most common silent failure.

## Scopes

### Scope types

`country`, `sector`, `galactic_object` (a solar system), `megastructure`, `ambient_object`, `planet` (includes stars, asteroids, habitats, ringworlds), `deposit`, `archaeological_site`, `army`, `pop`, `pop_faction`, `species`, `leader`, `ship` (includes starbases), `fleet`, `debris`, `design`, `federation`/`alliance`, `war`, `first_contact` (3.0+), `espionage_operation` (3.0+), `spy_network` (3.0+), `situation` (3.3+), `agreement` (3.4+), `pop_group` (4.0+, replacing `pop`), `global`.

`is_scope_type = <type>` tests the current scope type.

### System scopes

| Scope | Meaning |
|-------|---------|
| `THIS` | The current scope |
| `ROOT` | The scope the event/effect chain started from |
| `FROM` | The caller's scope; `FROMFROM`, `FROMFROMFROM` walk further back |
| `PREV` | The previously scoped object; `prevprev` etc. chain |

`on_action` events override some of these to match the action's participants. Read the comments in `common/on_actions/00_on_actions.txt` before trusting any assumption about `FROM`.

### Scope links

Links are used bare (`owner = { ... }`) or dot-chained (`owner.capital_scope.solar_system = { ... }`). Dot chaining does not create a new `PREV`, and does not work with scope-changing triggers or effects.

Common links by source scope:

| From | Links |
|------|-------|
| `country` | `capital_scope`, `capital_star`, `home_planet`, `leader`, `ruler`, `heir`, `alliance`, `federation`, `overlord`, `subject`, `species`, `owner_species`, `built_species`, `unhappiest_pop`, `branch_office_owner` |
| `planet` | `solar_system`, `star`, `owner`, `controller`, `space_owner`, `starbase`, `orbit`, `sector`, `planet_owner`, `orbital_defence`, `orbital_station`, `ruler`, `heir`, `unhappiest_pop`, `growing_species`, `declining_species`, `assembling_species` |
| `galactic_object` | `star`, `starbase`, `owner`, `space_owner`, `leader`, `ruler`, `heir`, `sector` |
| `fleet` | `orbit`, `star`, `starbase`, `system_star`, `leader`, `owner`, `controller`, `space_owner`, `solar_system`, `archaeological_site` |
| `pop` | `owner`, `planet`, `home_planet`, `species` |
| `species` | `home_planet`, `owner_species` |
| `leader` | `fleet`, `species`, `owner`, `ruler`, `heir`, `sector`, `solar_system`, `home_planet` |
| `megastructure` | `solar_system`, `star`, `planet`, `planet_owner`, `owner`, `leader`, `ruler`, `heir`, `sector` |
| `army` | `fleet`, `leader`, `owner`, `planet_owner`, `planet`, `orbit`, `home_planet`, `sector`, `solar_system`, `pop`, `species`, `owner_species` |
| `pop_faction` | `country`, `leader`, `ruler`, `heir`, `owner_species` |
| `first_contact` | `contact_country`, `owner`, `leader`, `ruler`, `heir`, `star`, `solar_system`, `sector` |
| `spy_network` | `target`, `owner`, `leader`, `ruler`, `heir`, `space_owner` |
| `war` | `attacker`, `defender` |
| `federation` | `leader`, `federation_leader` |

### Scope existence

Always guard optional links. An effect on a non-existent scope does nothing; a **condition** on a non-existent scope writes an error and aborts the block.

```
planet = {
    exists = owner
    owner = { ... }
}
```

## Effects and Conditions Must Be Scope-Legal

Every effect and condition declares the scope(s) it accepts. Using one in the wrong scope writes `error.log` and typically aborts the enclosing block, leaving partial state. Before writing, confirm the entry in `logs/script_documentation/` for the installed patch.

Structural effect keywords:

| Keyword | Behaviour |
|---------|-----------|
| `if = { limit = { ... } ... }` | Conditional block |
| `else_if = { limit = { ... } ... }`, `else = { ... }` | Branches |
| `while = { count = N ... }` / `while = { limit = { ... } ... }` | Loop |
| `every_<scope> = { limit = { ... } ... }` | Iterate all matching |
| `random_<scope> = { limit = { ... } ... }` | Pick one matching |
| `ordered_<scope> = { order_by = ... position = <n> ... }` | Deterministic selection |
| `random_list = { <weight> = { ... } ... }` | Weighted choice |
| `hidden_effect = { ... }` | Execute without generating tooltips |
| `custom_tooltip = <key>` | Add a tooltip in place of generated ones |
| `fire_on_action = { on_action = <key> scopes = { from = X } }` | Fire a custom on_action (3.0+) |

Condition structure:

```
OR = { ... }
AND = { ... }
NOT = { ... }
NOR = { ... }
NAND = { ... }
switch = { trigger = <value> <value> = { ... } }
```

## Flags

Boolean per-scope markers, available on `leader`, `planet`, `country`, `first_contact`, `fleet`, `ship`, `species`, `pop`, `pop_faction`, `federation`, `galactic_object`, `ambient_object`, `megastructure`, `espionage_operation`, and global.

```
set_country_flag = my_flag
set_timed_country_flag = { flag = my_flag days = 360 }
remove_country_flag = my_flag
has_country_flag = my_flag
```

Flags are not timers in the reverse direction: `had_<scope>_flag` is not implemented.

Dynamic flags resolve `@<scope>` to an ID at set/check time:

```
from = { set_leader_flag = is_friend_of_@root }
has_leader_flag = is_friend_of_@from
```

Supported only in `set_/remove_<scope>_flag` and `has_<scope>_flag`; not in `create_leader`.

## Event Targets

```
save_event_target_as = my_target            # namespace-scoped
save_global_event_target_as = my_target     # global
event_target:my_target = { ... }
clear_global_event_target = my_target
```

In localisation, use `[my_target.GetName]` — no `event_target:` prefix. Dynamic targets append `@scope`: `save_event_target_as = foo@root`.

## Performance Rules

1. Never poll every event every tick. Use `is_triggered_only = yes` and fire from an on_action or a single cheap gatekeeper event.
2. Add `pre_triggers` to `planet`, `pop`, `system`, `starbase`, and `leader` events to exclude objects before full trigger evaluation.
3. Prefer `random_events` or explicit `days`/`random` delays over `mean_time_to_happen`; MTTH re-checks conditions daily once modifiers exist.
4. `script_values` used in hot triggers are evaluated on every check; keep them short.
5. Effect-heavy `potential`/`allow` blocks run in the UI every frame the planet or building list is open.

## Validation Loop

1. Write the smallest script that exercises the effect.
2. In-game: `run test.txt` from the user data directory to recompile and execute from the player scope without restarting.
3. Read `error.log`; the first error is the cause, later ones are usually cascades.
4. When a trigger or effect seems ignored, check in this order: scope legality, key spelling, patch availability, then merge type.