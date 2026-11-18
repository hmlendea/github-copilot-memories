# Scripting: Syntax, Effects, Triggers, Scopes, Event Targets, Variables, and Macros

Victoria 3 uses the Paradox scripting language (Jomini layer). Apply this reference to `common/`, `events/`, and `history` files.

## Syntax Fundamentals

```
key = value
key = { ... }
key = { a b c }        # whitespace-separated list
```

- `#` starts a comment to end of line.
- Indent with tabs; matching braces at the same column is the single most effective syntax check.
- `=` is overloaded: assignment, block opener, condition evaluation, effect activation, and scope change. Do not read it as assignment.
- Booleans are `yes` / `no`. Numbers are fixed-point, five decimal places maximum.
- Strings need quotes when they contain spaces or are localisation keys.
- `@name = value` declares a file-local constant; use it for shared numbers and textures.
- Files must be UTF-8 with BOM or they are ignored.

Case sensitivity: script keys are lowercase with underscores; `scope:`, `c:`, `cu:`, `rel:`, `s:`, `sr:`, `ig:`, `je:`, `law_type:`, `b:`, `bg:`, `bt:`, `g:` targets are lowercase prefixes with case-sensitive payloads (`c:GBR`, `s:STATE_UTAH`, `p:x1A6E5B`).

## Documentation First

`script_docs` and `DumpDataTypes` in the console dump the authoritative lists into `<user data>/Victoria 3/docs/`. Regenerate after every patch; search those files before trusting wiki tables or another Paradox title's syntax.

| Dump | Contents |
|------|----------|
| Effects | Every hardcoded effect, arguments, legal scopes |
| Triggers | Every hardcoded trigger, arguments, legal scopes |
| Event targets | Input and output scope of every target |
| Data types | GUI script data types, functions, promotes |
| Modifier types | Every modifier key and where it can be used |
| On actions | Every on_action with its scopes |

## Effects and Triggers

- **Effects** change state: `add_treasury`, `set_variable`, `create_character`, `add_journal_entry`, `every_scope_state`.
- **Triggers** test state and evaluate to yes/no: `has_variable`, `has_law`, `is_incorporated`, `any_scope_state`, `country_rank = rank_value:great_power`.
- Iterator effects are `every_*`, `random_*`, `ordered_*`; iterator triggers are `any_*`, `all_*`, `count_*`. Mixing them is the most common silent failure.
- Every effect and trigger has a required scope. A scope-illegal use writes to `error.log` and aborts the surrounding block.

## Scopes

`root` is the origin scope of the script instance — often a country, but never assume it. `this` is the current scope, used for identity comparisons. `prev` steps back through the chain (`prev.prev` works, deeper chains are discouraged).

The `?=` assertion operator scopes or compares only when the object exists:

```
capital ?= state_region.s:STATE_HOME_COUNTIES
```

Common scope types: `country`, `state`, `state_region`, `strategic_region`, `province`, `character`, `interest_group`, `pop`, `building`, `market`, `market_goods`, `goods`, `law`, `journal_entry`, `power_bloc`, `political_movement`, `party`, `institution`, `treaty`, `war`, `diplomatic_play`, `front`, `battle`, `military_formation`, `hq`, `company`, `culture`, `religion`, `technology`, `value`, `none`.

## Event Targets

| Target | From | To | Example |
|--------|------|----|---------|
| `c:` | none | country | `c:GBR` |
| `cd:` | none | country_definition | `cd:FRA` |
| `s:` | none | state_region | `s:STATE_UTAH` |
| `sr:` | none | strategic_region | `sr:region_persia` |
| `p:` | none | province | `p:x1A6E5B` |
| `cu:` | none | culture | `cu:welsh` |
| `rel:` | none | religion | `rel:catholic` |
| `g:` | none | goods | `g:iron` |
| `bg:` / `bt:` | none | building group / type | `bg:bg_logging` |
| `b:` | state | building | `b:building_port` |
| `ig:` | country | interest group | `ig:ig_armed_forces` |
| `je:` | country | journal entry | `je:je_antarctica` |
| `law_type:` | none or law | law type | `law_type:law_protected_speech` |
| `institution:` | country | institution | `institution:institution_health_system` |
| `company:` | country | company | `company:company_rheinmetall` |
| `market` | many | market | `market` |
| `state`, `region`, `province` | many | object | `state`, `region` |
| `front` | battle, character, formation, province | front | `front` |
| `scope:<name>` | none | saved scope | `scope:unfriendly_country` |
| `var:` / `global_var:` / `local_var:` | none | variable value | `var:my_counter` |

Data targets take input: `active_law:lawgroup_trade_policy`, `ai_army_comparison:root`, `define:Namespace|Name`, `array_define:Namespace|Name|Index`. Some use the `target(argument)` form and must be quoted, e.g. `"scope:power_bloc.power_bloc_leader.market.market_number_goods_shortages_with(scope:with_country)"`.

Value targets return numbers and can be used wherever a script value is accepted: `infrastructure`, `expenses`, `income`, `num_states`, `level`, `relations:root`, `ai_state_value:root`.

## Saved Scopes and Values

```
random_country = {
    limit = { relations:root < relations_threshold:neutral }
    save_scope_as = unfriendly_country
}
create_diplomatic_incident = { target = scope:unfriendly_country value = 10 }
```

- Saved scopes live only for the current effect chain and are discarded at its end; `clear_saved_scope` clears one early.
- Only scopes saved **before** the call are forwarded to a triggered event. Saving after `trigger_event` inside the same block does not reach that event.
- On actions forward their own scopes (`scope:target`, `scope:recipient`, `scope:actor`, …) — read the on_action table before assuming.
- `save_scope_value_as = { name = x value = 3 }` stores a number or boolean; retrieve with `scope:x`.
- `save_temporary_scope_as` / `save_temporary_scope_value_as` persist only inside the same effect block.
- The UI can pass scopes into scripted GUIs and script values with `AddScope(...)`.

## Variables

```
set_variable = my_flag                          # boolean flag
set_variable = { name = my_counter value = 3 }
change_variable = { name = my_counter add = 1 }  # add num subtract multiply divide modulo min max
remove_variable = my_counter
has_variable = my_counter
```

Scoped variants exist for every operation: `set_local_variable`, `set_global_variable`, `change_local_variable`, `change_global_variable`, `remove_local_variable`, `remove_global_variable`, `has_local_variable`, `has_global_variable`, `clamp_variable`/`clamp_local_variable`/`clamp_global_variable`, `round_variable`, `sort_variable_list`.

Read with `var:name`, `local_var:name`, `global_var:name`. Variable lists and maps are supported (`has_variable_list`, `has_variable_map`).

Rules of thumb:
- Plain variables belong to their scope and are invisible outside it.
- Local variables exist for the current effect chain only.
- Global variables are visible everywhere and survive; use them for cross-mod signalling.
- `set_variable = flag` inside a `trigger` guard plus `NOT = { has_variable = flag }` is the standard fire-once pattern.

## Script Values

Script values are numeric formulas, either named (`common/script_values/`) or inline.

```
example_value = {
    add = 5          # 5
    multiply = 4     # 20
    max = 10         # 10
    subtract = 3     # 7
    value = 13       # 13
}
```

- Operators: `value`, `add`, `subtract`, `multiply`, `divide`, `modulo`, `max`, `min`, `round`, `ceiling`, `floor`, `round_to`, `fixed_range`, `integer_range`, `pow`.
- **No operator precedence.** Evaluation is strictly left-to-right, top-to-bottom. Use nested blocks for grouping.
- Conditionals use `if`, `else_if`, `else` with `limit` blocks and are applied cumulatively unless the branches are exclusive.
- Iterators (`every_scope_state`, `every_scope_building`, …) accumulate into the value; put the combining operator outside the iterator block when averaging.
- Scope: a script value is evaluated in the scope where it is called. Use dot scoping (`c:GBR.half_expenses`) or scope the individual terms to pin it.
- Display with `ScriptValue('name')` in localisation. Add `desc = loc_key` to explain an operator and `format = loc_key` with `$VALUE$` / `$KEY$`.
- `save_temporary_value_as` stores an intermediate; retrieve with `scope:name`.
- Five decimal places maximum; the range is roughly ±9.22e13.

`@` values are file-local constants, resolved at load time and usable in any file including `.gui`:

```
@pi = 3.1416
@third = @[1/3]
@tex = "path/to/texture.dds"
```

`@[...]` formulas follow normal precedence and support `+ - * /` and parentheses. `@` values cannot read game state.

## Scripted Effects and Triggers (Macros)

Defined in `common/scripted_effects/` and `common/scripted_triggers/`; called as `name = yes`. They may take `$PARAMETER$` arguments when called as `name = { PARAMETER = value }`.

- `INJECT:` on these folders behaves like `REPLACE:`; only `REPLACE:` is supported.
- Wrap the body in `hidden_effect` / `hidden_trigger`, `custom_tooltip`, or `custom_description` to control what the player sees — otherwise the expanded script produces its auto-generated tooltip.
- Scripted triggers inside scripted effects and vice versa are allowed; avoid mutual recursion.

## Scripted Lists and Geographic Regions

```
princely_state = {
    base = country
    conditions = { is_princely_state = yes }
}
```

Used as `any_princely_state = { ... }`. `base` must be an existing iterator base (`country`, `scope_state`, `interest_group`, …).

Geographic regions live in `common/geographic_regions/`, use a `short_key`, and produce `{any|every|ordered|random}_{country|province|state|state_region|strategic_region}_in_<short_key>`. The developers recommend georegion iterators over country/state iterators for performance. `is_in_geographic_region = <key>` tests membership.

## Flow Control

| Block | Purpose |
|-------|---------|
| `if` / `else_if` / `else` with `limit` | Conditional branches |
| `while` with `limit` | Loop; must be guaranteed to terminate |
| `random_list = { 100 = { ... } 200 = { ... } }` | Weighted random pick |
| `first_valid` / `random_valid` | First or random entry whose trigger passes (events, descriptions) |
| `every_*` / `random_*` / `ordered_*` with `limit` | Iteration |
| `hidden_effect` / `hidden_trigger` | Execute without tooltip output |
| `custom_tooltip = { text = key ... }` | Replace auto tooltips with one key |
| `custom_description` | Full effect/trigger localisation (see `references/localisation.md`) |
| `show_as_tooltip` | Show effects without executing them |
| `trigger_event` | Fire an event immediately or after a delay |
| `debug_log = "message"` / `debug_log_scopes = yes` | Trace script execution |

`ordered_*` blocks accept `order_by`, `position`, `min`, `max`, and `check_range_bounds` to select ranked slices instead of iterating everything.

## Modifiers

Static modifiers live in `common/static_modifiers/`:

```
splendid_coastal_state = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_gear_positive.dds
    state_infrastructure_add = 20
}
```

Apply with `add_modifier = { name = ... months = 3 multiplier = -1 is_decaying = no }` or the short `add_modifier = static_modifier_name` (permanent, no multiplier). Remove with `remove_modifier`; test with `has_modifier`.

- Modifier keys must exist in `common/modifier_type_definitions`; an unknown key is ignored with a log line.
- Modifier keys usually encode their flow with a prefix (`country_`, `state_`, `building_`, `character_`) and a suffix (`_add`, `_mult`, `_factor`). A key applied to the wrong scope has no effect.
- `modifier = { ... }` blocks inside scripted types apply automatically to that object and are not static modifiers.

## Modding Safety

- A `while` loop without a guaranteed exit freezes the game.
- Deep `every_*` nesting over countries multiplies cost by the number of countries; use georegions or `ordered_` slices.
- A trigger chain ending in `always = yes` in a high-frequency on_action is a performance problem, not a correctness bug.
- Reserve `debug_log` calls for development branches; purge them before release.