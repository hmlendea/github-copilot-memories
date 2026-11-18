# Scripting: Syntax, Scopes, Scope Links, Effects, Triggers, Iterators, Variables, Script Values, Macros, MTTH, and Defines

Europa Universalis V uses the Clausewitz/Jomini scripting language. Apply this reference to `common/`, `events/`, and setup files.

## Syntax Fundamentals

```
key = value
key = { ... }
key = { a b c }        # whitespace-separated list
```

- `#` starts a comment to the end of the line.
- Indent with tabs; matching braces at the same column is the single most effective syntax check.
- `=` is overloaded: assignment, block opener, condition evaluation, effect execution, and scope transition.
- Booleans are `yes` / `no`. Numbers are 64-bit fixed point, with a maximum of **5 decimal places** (digits beyond the 5th are silently truncated).
- Strings need double quotes when they contain spaces or are localisation keys.
- `@name = value` declares a file-local constant; use it for shared numbers and icon paths.
- Localisation `.yml` files must be UTF-8 with BOM; setup files have specific encoding rules.

Case sensitivity: script keys are lowercase with underscores; `scope:`, `c:`, `cu:`, `rel:`, `s:`, `sr:`, `b:`, `g:` target prefixes are lowercase with case-sensitive payloads (`c:FRA`, `c:ENG`).

## Documentation Dumps

Always inspect the generated engine documentation before relying on wiki tables:

- Run `script_docs` (alias `script_documentation`) in the in-game console to generate `Documents/Paradox Interactive/Europa Universalis V/docs/` dumps (`effects.log`, `triggers.log`, `event_targets.log`, `modifier_types.log`).
- Run `dump_data_types` (alias `DumpDataTypes`) to generate `logs/data_types/` for GUI script functions, promotes, and types.

## Scopes

Scopes define the context for an effect, trigger, or script value.

| Scope | Description | Common Ways to Scope To |
|-------|-------------|-------------------------|
| `country` | A sovereign tag or non-playable entity | `c:TAG`, `owner`, `actor`, `recipient`, `root` |
| `location` | Individual map location (atomic map unit) | `capital`, `location:<id>`, `province.any_location_in_province` |
| `province` | Group of locations | `province`, `capital.province` |
| `area` | Group of provinces | `area` |
| `region` | Group of areas | `region` |
| `sub_continent` | Group of regions | `sub_continent` |
| `continent` | Continental landmass | `continent` |
| `character` | Ruler, consort, heir, general, admiral, artist, cabinet member | `ruler`, `heir`, `consort`, `character:<id>` |
| `pop` | Population unit in a location | `every_pop`, `random_pop`, `define_pop` |
| `building` | Building instance on a location | `every_building`, `building:<type>` |
| `market` | Trade market center and network | `market`, `location.market` |
| `goods` | Trade good type | `goods:<type>` |
| `war` | Active war instance | `war`, `every_war` |
| `culture` | Culture type | `culture`, `culture:<name>` |
| `religion` | Religion type | `religion`, `religion:<name>` |
| `institution` | Active institution | `institution:<name>` |
| `international_organization` | HRE, leagues, crusades | `international_organization:<name>` |
| `situation` | Active or inactive situation | `situation:<name>` |
| `disaster` | Active disaster | `disaster:<name>` |
| `unit` | Army or navy subunit | `unit` |
| `value` | Mathematical or scalar result | Wild-card value scope |
| `none` | Scopeless/global (functions anywhere) | Scopeless triggers and effects |

`root` is the entry scope (usually the country, but depends on on_action or event type). `this` is the current scope. `prev` steps one scope back in the execution chain (`prev.prev` supported, but avoid deep chains).

The `?=` operator scopes only when the target exists (existence-safe check):
```
capital ?= location:stockholm
```

## Scope Links (Event Targets)

Scope links navigate between scopes using dot syntax:
```
p:x1A6E5B.province.owner.capital
c:FRA.gold
scope:actor.capital.market
```

Data scope links use `event_target:data` or quoted `"event_target(data)"` form when arguments are required.

## Effects and Triggers

- **Triggers** test the state: `country_rank = rank_kingdom`, `has_variable = my_var`, `is_subject = no`, `gold >= 100`.
- **Effects** change the state: `add_gold = 25`, `set_variable = { ... }`, `trigger_event = test_events.1`, `change_control = 10`.

Assignment vs Comparison:
- `=` is overloaded for simple triggers, effects, and blocks.
- Comparisons use `<`, `<=`, `=`, `!=`, `>`, `>=`.
- Negation wrapper: `NOT = { trigger = condition }`.
- Inverted comparisons inside `NOT` invert their operators (`NOT = { gold >= 50 }` is equivalent to `gold < 50`).
- Certain triggers require boolean syntax: `building_category = government_category` can only use `=`; write `NOT = { building_category = government_category }` instead of `!=`.

## Iterators

Iterators inspect or act on multiple scopes of a given type.

| Iterator | Type | Behavior | Parameters |
|----------|------|----------|------------|
| `any_<type>` | Trigger | Returns true if any matching scope satisfies the inner triggers | `count = <int>`, `percent = <float>`, `filter = { ... }` |
| `every_<type>` | Effect | Executes effects on all matching scopes | `limit = { ... }` |
| `random_<type>` | Effect | Executes effects on exactly one random matching scope | `limit = { ... }`, `weight = { ... }` (MTTH block) |
| `ordered_<type>` | Effect | Executes effects on sorted matching scopes; **returns only the first by default** | `order_by = <val>`, `limit = { ... }`, `position = <int>`, `min = <int>`, `max = <int>`, `check_range_bounds = no` |

**Critical Trap**: An `ordered_*` iterator without an explicit `max` returns only **1** scope, not all matching scopes. To process all matching scopes in order, provide an explicit sufficient `max` value.

## Variables

EU5 has three variable scopes:

| Type | Scoped? | Persistent? | Prefix |
|------|---------|-------------|--------|
| Regular | Yes (saved to an object) | Yes | `var:name` |
| Global | No | Yes | `global_var:name` |
| Local | No | No (dropped at end of chain) | `local_var:name` |

Setting variables:
```
set_variable = {
    name = my_var
    value = 5
}

set_variable = {
    name = target_country
    value = c:FRA
}

# Flag variable holding a localisation key
set_variable = {
    name = title_flag
    value = flag:my_loc_key
}
```

Variable Maps:
Market scopes cannot hold direct variables. Use global variable maps instead:
```
add_to_global_variable_map = {
    name = market_cache
    key = scope:target_market
    value = 42
}
```
`add_to_global_variable_map` is insert-only (does not overwrite existing keys; use `remove_from_global_variable_map` first). Map values cannot be inline math blocks.

## Script Values

Defined in `common/script_values/` or written inline.
- Fixed point with a maximum of **5 decimal places**.
- Evaluated top-to-bottom; no operator precedence (no PEMDAS).
- Supported operators: `value`, `add`, `subtract`, `multiply`, `divide`, `modulo`, `max` (upper clamp), `min` (lower clamp), `round`, `ceiling`, `floor`, `round_to`, `fixed_range`, `integer_range`, `pow`, `abs`.
- Conditional blocks: `if = { limit = { ... } add = 5 }`, `else_if = { ... }`, `else = { ... }`.

### Clamp Direction
- `min` is the **lower clamp** (forces at least this value).
- `max` is the **upper clamp** (forces at most this value).
- To enforce a non-negative number: `value = { value = var:X min = 0 }`.

### Location Scope Navigation Rule
A script value runs in the scope it is called from. The `location.` prefix navigates *to* a location from an outer scope (pop, character, market):
- Inside pop scope calling a location value: `add = location.local_demand_scale` (correct).
- Inside location scope: `value = local_demand_scale` (do not use `location.` here; engine errors with wrong scope type).

## Macros (Scripted Effects and Triggers)

Defined in `common/scripted_effects/` and `common/scripted_triggers/`.
- Macro definitions behave like copy-pasting the script block into the call site.
- Support parameter insertion via `$param$`.
- Inline scripted triggers/effects can be defined inside `events/` files for file-local use.
- Overrides: `INJECT:` on scripted effects or triggers behaves like `REPLACE:`; duplicate declarations without entry modes fail with `Duplicated key`.
- Tooltips: Use `effect_localization` and `trigger_localization` in `common/`, or wrap in `custom_tooltip = { text = key ... }` / `hidden_effect = { ... }`.

## Mean Time to Happen (MTTH)

MTTH is **not** an event-firing mechanism in EU5. It is exclusively a weight and calculation syntax used by:
- Event `weight_multiplier` blocks.
- `random_events` and `random_on_action` candidate weights.
- `random_*` iterator selection weights.
- Institution spread and promote chance.

Syntax:
```
weight = {
    base = 1
    modifier = {
        factor = 2
        trigger = { has_variable = is_wealthy }
    }
    modifier = {
        add = 5
        trigger = { prestige >= 50 }
    }
}
```
`base` and `factor` are interchangeable. `days`, `months`, `years` can be used as multipliers (months * 30, years * 365).

## Defines

Stored in `loading_screen/common/defines/`.
- Base values are defined in `00_defines.txt` and `00_graphics.txt`.
- Define modding allows single-key patching without whole-file replacement:
```
NCountry = {
    COUNTRIES_GETTING_SCORE = 12
}
```
- Multiple mods touching the same define resolve by the latest loaded filename.
- Prefix categories with `N` (`NCountry`, `NDiplomacy`, `NEconomy`, `NEstate`, `NGame`, `NLocation`, `NPop`, `NWar`, `NAI`, `NGUI`).