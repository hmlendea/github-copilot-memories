# Scripting: Effects, Triggers, Scopes, Variables, Script Values

## Syntax Fundamentals

Clausewitz script is a brace-delimited key/value language.

```
key = value
key = { ... }
key = { a b c }        # whitespace-separated list
```

- `#` starts a comment, to end of line.
- Indent so that matching braces sit at the same column; this is the single most effective syntax check.
- Strings are quoted when they contain spaces; identifiers are usually bare.
- Dates in character and history data use **Ab Urbe Condita**, `YY.MM.DD` (e.g. `418.7.8`).
- Colours appear as `hsv { h s v }`, `rgb { r g b }`, `hsv360 { ... }`, or a named colour key from a colour list.
- Fixed-point script values are plain decimals; many triggers compare with `<`, `<=`, `=`, `!=`, `>`, `>=`.

## Effects and Triggers Are Scope-Bound

Every effect and trigger has a supported scope and, often, a supported target. Using one in the wrong scope produces **no effect and no error in normal play** — the classic silent failure. Check the scope list below or the `script_docs` dump before writing.

- Effects **change** state: `set_variable`, `add_treasury`, `declare_war_with_wargoal`, `add_building_level`.
- Triggers **test** state and always evaluate to true/false: `has_variable`, `treasury >= 100`, `is_ai = no`.
- Confusing the two is the second most common bug. In particular, `every_*` and `random_*` are **effects**, while `any_*` is a **trigger**.

## Scopes

Fundamental scope types: `country`, `character`, `unit` (army/navy), `subunit` (cohort), `legion`, `region`, `area`, `state`, `province` (a *territory*), `pop`, `party`, `family`, `job`, `siege`, `culture`, `culture group`, `religion`, `color`.

Terminology trap: in game terminology a **province** is an area and a **territory** is a province; in script, `province` means the territory, and `area` means the in-game province.

### Target links (scope-to-scope)

| Link | From | To |
|------|------|----|
| `owner` | province, state, governorship, legion | country |
| `controller` | province | country |
| `area`, `region` | province → area → region | area, region |
| `governorship` | province, state | governorship |
| `governor`, `governor_or_ruler`, `job_holder` | province, state, governorship | character |
| `capital_scope` | country, state, governorship | province |
| `current_ruler`, `current_heir`, `primary_heir`, `secondary_heir`, `consort`, `current_co_ruler` | country | character |
| `employer`, `country` | character, pop, job | country |
| `father`, `mother`, `spouse`, `preferred_heir`, `ruler`, `character_party`, `job` | character | character, party, job |
| `overlord`, `every_subject` | country | country |
| `unit_owner`, `commander`, `unit_location`, `unit_destination`, `unit_next_location` | unit | country, character, province |
| `owning_unit`, `personal_loyalty` | subunit | unit, character |
| `party_leader`, `party_country` | party | character, country |
| `family_country`, `head_of_family` | family | country, character |
| `dominant_province_culture`, `dominant_province_culture_group` | province | culture, culture group |
| `color1`, `color2`, `color3`, `color` | country, culture, religion | color |
| `siege` | province, unit | siege |

There are many more. Jomini scope links compose freely, so `capital_scope.owner` is legal; prefer chaining existing links over inventing new ones.

### Iteration scopes

Each family has three flavours:

- `every_X = { limit = { <triggers> } <effects> }` — run effects on all matches.
- `random_X = { limit = { <triggers> } weight = { <mtth/script value> } <effects> }` — one weighted match.
- `ordered_X = { limit = { <triggers> } order_by = <script value> position = <int|min|max> <effects> }` — ordered match.
- `any_X = { count = <n|all> filter = { <triggers> } percent = <fixed point> <triggers> }` — trigger form; true if the condition holds for the required share.

Representative sets, all with matching region/area/state/province variants:

- Geographic: `every_region`, `every_area`, `every_state`, `every_province`, `every_ownable_province`, `every_owned_province`, `every_state_province`, `every_area_province`, `every_region_state`, `every_neighbor_province`, `every_unit_in_province`, `every_pops_in_province`.
- National: `every_country`, `every_subject`, `every_allied_country`, `every_neighbour_country`, `every_countries_at_war_with`, `every_governorships`, `every_governorship_state`, `every_country_state`, `every_country_sub_unit`.
- Characters: `every_character`, `every_living_character`, `every_commander`, `every_successor`, `every_family`, `every_family_member`, `every_child`, `every_sibling`, `every_friend`, `every_rival`, `every_support_as_heir`, `every_integrated_culture`.
- Military: `every_unit`, `every_army`, `every_navy`, `every_sub_unit`, `every_governor_state`.
- Lists: `every_in_list`, `every_in_local_list`, `every_in_global_list`, `random_in_list`, `ordered_in_list`, and their `local`/`global` variants; `list = <name>` or `variable = <name>`.

## Conditions, Effects, and Control Flow

```
if = { limit = { <triggers> } <effects> }
else_if = { limit = { ... } ... }
else = { ... }

trigger_if = { limit = { ... } <triggers> }
trigger_else = { <triggers> }

random_list = {
    10 = { <effects> }
    20 = { trigger = { <triggers> } <effects> }
}
```

Further control constructs used in vanilla and documented by `script_docs`: `hidden_effect`, `custom_tooltip = { text = <key> <triggers-or-effects> }`, `break_if = { <trigger> }`, `while`/`for`-style loops as reported by `script_docs`, and `random_list` with `modifier`/`compare_modifier`/`opinion_modifier` weights.

`weight_multiplier = { <modifiers> }` scales event firing probability; `mtth` blocks are supported inside `weight` of random iterators.

## Scripted Effects and Arguments

Call with an argument block where a boolean would normally go, and read it inside the definition wrapped in `$…$`:

```
# definition (common/scripted_effects/...)
change_color_effect = {
    change_country_color = $my_argument$
}

# call
change_color_effect = { my_argument = color }
```

The argument name is bare in the call site and dollar-wrapped in the definition. The same pattern applies to scripted triggers.

## Variables

Variables live **inside a scope**, have a name, and optionally a value. Types: number, boolean, flag (existence only), and scope reference.

```
# flag
scope:character = { set_variable = has_best_friend_flag }

# value or scope reference
scope:character = {
    set_variable = { name = best_friend value = scope:other_character }
}

# mutate a numeric variable
change_variable = { name = num_friends add = 1 }   # add|subtract|multiply|divide|modulo
```

- Read a flag with the trigger `has_variable = <name>`.
- Read a value with the `.var:<name>` link: `scope:character.var:best_friend = scope:character_to_check`. Numeric comparisons accept `=`, `>=`, `<=`; scopes accept `!=` too.
- `change_variable` takes the bare name — prefixing `var:` there does not work.
- Variable lists: `add_to_variable_list = { name = X target = Y }`, `clear_variable_list = <name>`, and `variable_list_size = { name = X target >= Y }`; iterate with `every_in_local_list` / `ordered_in_global_list` etc.
- **Persistence:** a custom saved scope survives only within one uninterrupted effect chain (an event firing another event, an `on_action`, a scripted effect call). Outside the chain it is gone — persist via variables or country/global variables (`global_variable`, `remove_global_variable`).

## Script Values

Stored in `common/script_values/*.txt`; not persisted, recomputed on each call (and each frame when displayed in the UI).

```
my_value = { value = country_population multiply = 10 add = 20 }

cities_in_state = {
    value = 0
    every_state_province = {
        limit = { has_province_rank = city }
        add = 1
    }
}

slaves_needed = {
    value = 20
    if = { limit = { has_city_status = no } add = -5 }
    if = { limit = { terrain = farmland } add = -2 }
}
```

- Use by name: `add_treasury = my_value`.
- Scope of an svalue is inherited from the call site, so a country-scoped value cannot be called from a province scope.
- Inside an svalue use **effects** (`every_*`, `random_*`, `add`, `if`), never triggers (`any_*`).
- Script values may call each other and read `var:<name>`; a variable can be set from one to persist the result.
- With `-debug_mode`, edits reload instantly, but some triggers (`terrain`, `pop_type`) go stale after a reload — restart the game when an apparently correct value misbehaves.

## Modifiers

Modifiers are applied as keys inside a country/province/character block, in idea/heritage/religion/unit definitions, and in `modifier = { ... }` blocks. Names and validity come from the modifier list (`Modifier list` on the wiki, or `script_docs`); common suffixes are `_modifier`, `local_`, `global_`, `monthly_`. Unknown modifiers fail silently.

## Lists of Effects and Triggers

The wiki's `Effects`, `Triggers`, and `Scopes` pages are tables generated from the `script_docs` console command; the generated dump reflects the installed game and is more trustworthy than the wiki for the current patch:

- In-game: run `script_docs`, then read the generated log in `<user data>/Imperator/logs/`.
- `DumpDataTypes` dumps GUI data types for scripted GUIs and data functions.

Because the dumps are large and version-specific, prefer generating them locally over memorising the wiki tables.