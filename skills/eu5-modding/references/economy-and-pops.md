# Economy and Population: Goods, Demand, Buildings, Production Methods, Employment, Prices, Pops, Institutions, and Advances

## Goods

**Folder:** `common/goods/`

```
copper = {
    method = mining                  # mining / farming / fishing / forestry / hunting (farming default)
    category = raw_material          # raw_material / produced
    color = goods_copper
    default_market_price = 3
    transport_cost = 2
}
```

- Raw materials need `category = raw_material` and a `method`.
- Non-raw goods must explicitly state `category = produced`.
- Hardcoded goods (e.g. slaves) cannot be removed.
- AI weighting is scripted with `ai_` keys.
- Icons use the `TRADE_GOODS_ICON_PATH` define.

### Good demand blocks

**Folder:** `common/goods_demand/`

```
road_maintenance = {
    lumber = 0.02
    masonry = 0.02
    sand = 0.01
    category = building_maintenance
}
```

- Values are script values only for pop demands; other uses take constant numbers.
- `copy_from = <key>` adds the copied values onto existing entries (or inserts them).
- `hidden = yes` hides the tooltip.
- Required hardcoded demands: `grant_privilege`, `revoke_privilege`, `set_cabinet_action`, `set_cabinet_member`, `remove_government_reform`, `embrace_institution`.

### Good demand categories

**Folder:** `common/goods_demand_category/`

### Pop demand groups

Pop demand membership follows pop type: in 1.3.11 the `upper` demand group covers `nobles`, `clergy`, `burghers`, `laborers`, and `soldiers`, but not `peasants` or `tribesmen`. This applies to both `demand_add` and `demand_multiply`. Verify the membership against the installed version before calibrating demand; patch notes have changed group membership.

## Buildings

**Folder:** `common/building_types/`

```
sanssouci = {
    is_foreign = no
    pop_type = nobles
    max_levels = 1
    employment_size = noble_cultural_employment
    category = cultural_category
    town = yes
    city = yes
    expensive = yes
    build_time = cultural_building_time

    country_potential = {
        always = no                  # ROOT = the country attempting to build
    }
    allow = { ... }

    modifier = {
        local_cultural_tradition = 0.33
        local_cultural_influence = 0.33
        local_crown_estate_power = 0.25
    }

    possible_production_methods = { capital_building_maintenance }

    custom_tags = { unique_palace }
    construction_demand = capital_building_construction
}
```

Key fields:
- `pop_type` — the pop type employed; `employment_size` is a number or named script value.
- `obsolete` — marks another building obsolete; the obsolete building must be defined earlier, and one building can obsolete several.
- `country_potential` — visibility gate; discoverability via `unlock_building` in an advance also gates on that advance.
- `possible_production_methods` — links into `common/production_methods/`.
- `construction_demand` / maintenance demand — links into `common/goods_demand/`.
- `max_levels`, `town`, `city` — placement and level limits.

Building categories are defined in `common/building_categories/`. The `building_category` trigger accepts only `=`; negate it with a boolean wrapper:
```
NOT = { building_category = government_category }
```
`building_category != government_category` is a compile error.

### Counting estate buildings

Iterate buildings and filter by estate type rather than hardcoding names:
```
every_buildings_in_location = {
    limit = { estate_type ?= estate_type:nobles_estate }
    ...
}
```

## Production Methods

**Folder:** `common/production_methods/`

```
my_method = {
    potential = { ... }               # ROOT = country; scope:target = location
    allow = { ... }

    # Maintenance good demands
    lumber = 0.5
    tools = 0.1

    produced = cloth
    output = 2

    no_upkeep = yes                   # disable the passive upkeep cost
    debug_max_profit = 10             # error.log profit testing helper
}
```

- `potential` / `allow` receive both country and location scope; location is `scope:target`, not `location`.
- Unlock via an advance `unlock_production_method` gate also applies.
- Respective localisation key is the production method key.
- Passive upkeep = market price of inputs × the `BUILDING_UPKEEP_FACTOR` define.

## Employment Systems

**Folder:** `common/employment_systems/`
- Define pop counts and type distribution per building category.
- Referenced by `employment_size` in building definitions.
- A cached employment system is resolved at load; changing a vanilla employment system requires replacing its whole file.

## Prices

**Folder:** `common/prices/`

```
some_price = {
    gold = 50
}
```

**Important**: price objects are not additive. When an `INJECT:` repeats a scalar resource field, the later field **replaces** the earlier value instead of adding a delta. Two mods injecting `gold = -10` yield a final `gold = -10`, not `-20`, and the value may be clamped at zero. Use `REPLACE:` (or a sorting filename) when the intended final price must be deterministic.

## Roads

**Folder:** `common/road_types/` (see `references/setup-and-history.md` for start road placement)
- Road types define movement cost, proximity, market access, colour, splines, and building costs.
- Levels scale their effects.

## Pops

**Folder:** `common/pop_types/`

```
pop_type_name = {
    color = pop_color
    editor = 0.05
    assimilation_conversion_factor = 0.05
    pop_food_consumption = 20.0
    city_graphics = 1.0

    dhimmi_estate = { is_dhimmi = yes }
    tribes_estate = { is_gaelic_clans = yes }
    nobles_estate = {}

    promotion_factor = 0.1
    migration_factor = 0.5

    upper = yes
    has_cap = yes
    grow = yes
    counts_towards_market_language = yes

    promote_to = burghers
    promote_to = clergy
    promote_to = nobles

    literacy_impact = {
        local_cultural_tradition = 0.2
        local_monthly_control = 0.01
    }

    pop_percentage_impact = {
        local_distance_from_capital_cost_modifier = 0.5
    }
}
```

Estate assignment triggers run in pop scope. A single pop type can be assigned to multiple estates through mutually exclusive triggers, but must resolve to exactly one at runtime.

## Institutions

**Folder:** `common/institutions/` (the wiki path is sometimes written `common/institution/`; vanilla uses `common/institutions/` — verify against the installation)

```
institution_name = {
    age = age_1_traditions

    can_spawn = {
        continent = continent:europe
        has_owner = yes
        num_pop_type:nobles > 0.1
    }

    promote_chance = {
        add = {
            value = num_pop_type:nobles
            multiply = 10
        }
    }

    spread_from_friendly_coast_border_location = {
        value = institution_base_spread_from_friendly_neighbor_with_early
        add = { value = num_pop_type:nobles multiply = 0.5 }
    }
    spread_from_any_coast_border_location = institution_base_spread_from_neighbor_with_early
    spread_from_any_import = institution_trade_spread_value_early
    spread_scale_on_control_if_owner_embraced = 2
    spread_embraced_to_capital = institution_total_embraced_to_capital_early
    spread_to_market_member = institution_spread_to_market_member_early
}
```

- `age` binds the institution to an age tab (`age_1_traditions` … `age_6_revolutions`).
- Spread mechanics use MTTH-style notation.
- Starting presence is set per location in setup (`feudalism = yes`) and origins via `institution_manager`.

## Advances

**Folder:** `common/advances/`

```
ostentatious_clothing = {
    icon = fla_cloth
    age = age_5_absolutism
    requires = lead_ore_dressing

    global_alum_output_modifier = 0.1
    global_dyes_output_modifier = 0.1
}
```

- `age` is required; it determines the age tab.
- An advance is an implicit modifier block: any modifier type valid for a country may be listed.
- `modifier_while_progressing` blocks apply during research and support `scale` (script value) and `potential_trigger`:
```
modifier_while_progressing = {
    scale = {
        value = 1
        add = { value = legitimacy divide = 100 }
    }
    potential_trigger = { government_type = government_type:monarchy }
    monthly_prestige = 0.05
}
```
- Only one `requires` prerequisite is allowed, creating a tree. The prerequisite must be defined before the child.
- `allow_children = no` prevents random child assignment and errors if another advance lists it as a prerequisite.
- `potential` controls visibility; `allow` controls researchability. Both run with the researching country as root.
- Unlocks reference `unlock_building`, `unlock_production_method`, and similar keys.
- The `ages_of_eu.1` age event plus age preferences control age progression.
- Icons resolve from either the `icon` attribute or the advance key as a filename, under the advance icon define path.

## Practical Rules

- Every modifier key must exist in `common/modifier_type_definitions`; unresolved keys are logged and skipped.
- Static modifiers accept only static script values (constants or pure named values); dynamically calculated values do not work there.
- Numeric entries in static modifiers are additive across mods, so use delta-only `TRY_INJECT:` blocks.
- Pop demand calibration depends on the installed patch; re-verify demand group membership and hardcoded demand keys after each patch.
- Float literals are truncated to 5 decimal places; round generated values before writing them.