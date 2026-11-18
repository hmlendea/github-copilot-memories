# Buildings, Production Methods, Goods, Pops, Technologies, and Modifiers

## Building Groups

**`common/building_groups/`**

```
bg_manufacturing = {
    category = urban                # urban / rural / development
    economy_of_scale = yes
    cash_reserves_max = 25000
    should_auto_expand = { default_auto_expand_rule = yes }
    economy_of_scale_ai_factor = 4.0
    always_possible = yes
    parent_group = <bg_key>          # optional inheritance
    stateregion_max_level = yes      # optional
}
```

Building groups own the shared economics: category, economy of scale, cash reserves, auto-expansion behaviour, and state-region caps.

## Buildings

**`common/buildings/`**

```
building_tooling_workshops = {
    building_group = bg_manufacturing
    icon = "gfx/interface/icons/building_icons/tooling_workshops.dds"
    city_type = city
    levels_per_mesh = 5
    production_method_groups = { pmg_base_building_tooling_workshops }
    required_construction = construction_cost_medium
    buildable = yes
    expandable = yes
    downsizeable = yes
    unlocking_technologies = { mechanical_tools }
    possible = { NOT = { has_law = law_type:law_command_economy } }
    ownership_type = self
    economic_contribution = 1.0
    generates_residences = yes
}
```

Frequently used keys: `buildable`, `expandable`, `downsizeable`, `unique`, `has_max_level`, `ignore_stateregion_max_level`, `port`, `naval`, `canal`, `unlocking_technologies`, `can_build_government` / `can_build_private` (state scope), `construction_points`, `construction_modifier`, `owners`, `ownership_type` (`no_ownership` / `self` / `other`), `economic_contribution` (0–1 tax/GDP multiplier), `min_raise_to_hire`, `ai_value`, `ai_subsidies_weight`, `slaves_role`, `possible`, `should_auto_expand`, `city_type` (`none` / `city` / `farm` / `mine` / `port` / `wood`), `terrain_manipulator`, `residence_points_per_level`, `statue`, `meshes`, `entity_*`, `locator`, `lens`, `background`, `company_headquarter`.

Conventions: `building_<name>`, and every key defined here also needs localisation (name plus description).

Building-scope triggers worth knowing: `is_building_type`, `is_building_group` (uses `building_group =`), `is_subsistence_building`, `is_under_construction`, `is_subsidized`, `is_government_funded`, `has_active_production_method`, `occupancy`, `cash_reserves_ratio`, `cash_reserves_available`, `earnings`, `levels_owned_by_country`, `can_queue_building_levels`, `has_failed_hires`, `has_employee_slots_filled`, `building_has_goods_shortage`, `has_deployed_units`.

Building-scope effects: `add_modifier`, `remove_modifier`, `set_subsidized`, `every_/random_/ordered_combat_unit`.

## Production Method Groups

**`common/production_method_groups/`**

```
pmg_base_building_tooling_workshops = {
    texture = "gfx/interface/icons/generic_icons/method_icons/tools.dds"
    production_methods = { pm_simple_tools pm_mechanized_tools }
}
```

Groups are mutually exclusive slots in a building.

## Production Methods

**`common/production_methods/`**

```
pm_precision_tools = {
    texture = "gfx/interface/icons/generic_icons/method_icons/precision_tools.dds"
    is_default = no
    unlocking_technologies = { mechanical_tools }
    unlocking_laws = { }
    disallowing_laws = { }
    unlocking_production_methods = { pm_simple_tools }
    unlocking_principles = { }
    unlocking_identity = <identity>
    required_input_goods = electricity
    replacement_if_valid = <pm>
    is_hidden_when_unavailable = yes
    ai_weight = 1.0
    pollution_generation = 10

    building_modifiers = {
        workforce_scaled = {
            goods_input_hardwood_add = 25
            goods_output_furniture_add = -55
        }
        level_scaled = {
            building_employment_shopkeepers_add = 1000
        }
        unscaled = {
            building_laborers_mortality_mult = 0.3
        }
    }
    country_modifiers = { workforce_scaled = { country_bureaucracy_add = 65 } }
    state_modifiers = { workforce_scaled = { state_infrastructure_add = 25 } }
    timed_modifiers = { pm_offense_defense_readjustment_minor }
}
```

Scaling suffixes inside `country_modifiers`, `state_modifiers`, and `building_modifiers`:

- `workforce_scaled` — multiplied by building level, then by employment percentage. Goods input/output lives here.
- `level_scaled` — multiplied by building level. Employment lives here.
- `unscaled` — applied as written.

`pollution_generation` accumulates in the state region, scaled by arable land.

Conventions: `pm_<name>`; the first PM in a group is the default unless `is_default = yes` is set elsewhere, and some engine paths additionally expect a `pm_default` key.

## Goods

**`common/goods/`**

```
fabric = {
    texture = "gfx/interface/icons/goods_icons/fabric.dds"
    cost = 20
    category = staple               # staple / industrial / luxury / military
    prestige_factor = 5
    consumption_tax_cost = 10       # optional, authority
    local = yes                     # optional; state-local like electricity
    tradeable = no                  # optional
    fixed_price = yes               # optional; permanent fake demand
}
```

Anything `local` is automatically non-tradeable. Adding a good requires matching icon, localisation (`<good>`, `modifier_goods_input_<good>_add_desc`, output equivalents), and usually a need entry.

## Pop Needs and Buy Packages

**`common/pop_needs/`**

```
INJECT:popneed_crude_items = {
    entry = {
        goods = <good>
        weight = 2
        max_supply_share = 1.0
        min_supply_share = 0.0
    }
}
```

```
popneed_<name> = {
    default = <good>                # substitutes orient around this good
    obsession_demand_min = 0.5
    obsession_demand_mult = 2.0
    prestige_goods_demand_increase = 1.0
    entry = { goods = <good> }
}
```

**`common/buy_packages/`** — `wealth_1` … `wealth_99` each map need → money budget:

```
INJECT:wealth_15 = {
    goods = { popneed_<name> = <int> }
}
```

A new need must be added to **every** relevant wealth level individually; missing levels mean pops never buy it.

## Pops and Professions

**`common/pop_types/`**

```
example = {
    texture = "gfx/interface/icons/pops_icons/example.dds"
    color = { 12 251 123 }
    start_quality_of_life = 10
    wage_weight = 3
    paid_private_wage = yes
    education_access = 0.25
    consumption_mult = 1
    dependent_wage = 0.5
    unemployment = yes
    unemployment_wealth = 5
    can_always_hire = yes
    subsistence_income = yes
    ignores_employment_proportionality = yes
    is_slave = yes
    military = yes
    political_engagement_base = 0.5
    political_engagement_literacy_factor = 1.0
    political_engagement_mult = { value = 1 }
    qualifications = { }
    portrait_age = { value = 30 }
    portrait_pose = { value = 0 }
    portrait_is_female = { always = yes }
}
```

`strata =` is deprecated — do not use it. The defines `DEFAULT_POP_TYPE` and `SLAVE_POP_TYPE` must be updated if you replace the base professions.

Related: `common/ethnicities/` (weighted appearance lists), `common/dna_data/`, `common/genes/`, `common/culture_graphics/`.

## Technologies

**`common/technology/eras/`** and **`common/technology/technologies/`**.

```
era_2 = {
    technology_cost = 10000
}
```

```
nitroglycerin = {
    era = era_2
    texture = "gfx/interface/icons/invention_icons/nitroglycerin.dds"
    category = production                 # production / military / society
    unlocking_technologies = { intensive_agriculture prospecting }
    modifier = { country_resource_discovery_chance_mult = 0.25 }
    ai_weight = { value = 1 }
}
```

The technology key is also its localisation key. `add_era_researched = <era>` unlocks a whole era. Buildings, laws, PMs, and decrees unlock by naming the technology in their own lists, not the reverse.

## Cultures, Religions, Discrimination Traits

**`common/cultures/`**

```
mazanderani = {
    color = rgb{ 158 68 137 }
    religion = shiite
    heritage = heritage_iranian
    language = language_tabari
    traditions = { tradition_persianate }
    male_common_first_names = { }
    female_common_first_names = { }
    common_last_names = { }
    ethnicities = { 1 = arab }
    graphics = arabic
    obsessions = { }        # limited by MAX_NUM_OBSESSIONS
    taboos = { }            # overrides religion taboos
}
```

Name lists accept `common` / `noble` / `regal` variants for first and last names. Every entry is a localisation key without spaces.

**`common/religions/`**

```
hindu = {
    icon = "gfx/interface/icons/religion_icons/hindu.dds"
    heritage = heritage_dharmic
    color = { 0.8 0.2 0.3 }
    taboos = { meat }
}
```

**`common/discrimination_traits/`** — `type = heritage | language | tradition`, plus `trait_group` for heritage/language. Religions only use heritage traits.

## Modifiers and Modifier Types

**`common/static_modifiers/`** — reusable named modifier bundles applied by `add_modifier`.

**`common/modifier_type_definitions/`** — declares each modifier key:

```
country_institution_home_affairs_max_investment_add = {
    decimals = 0
    color = good
    game_data = { ai_value = 0 }
}
```

An undeclared key is ignored. Institution-specific modifiers follow the naming pattern `country_institution_<institution>_investment_add`, `country_institution_size_change_speed_<institution>_mult`, `country_institution_cost_<institution>_mult`.

## Character Templates and Traits

**`common/character_templates/`**

```
usa_rockefeller_character_template = {
    first_name = John
    last_name = Rockefeller
    historical = yes
    dna = dna_john_d_rockefeller
    culture = cu:yankee
    female = no
    religion = rel:protestant
    ideology = ideology_moderate
    interest_group = ig_industrialists
    birth_date = 1839.6.8
    traits = { ambitious persistent basic_entrepreneur }
    executive_usage = {
        country_trigger = { exists = c:USA this = c:USA }
        company_trigger = { is_company_type = company_type:company_standard_oil }
        earliest_usage_date = 1875.1.1
    }
}
```

Templates are used by `create_character` and can appear semi-randomly when a usage block is defined. Traits live in `common/character_traits/` and include personality, skill, and unique categories.

## Defines

**`common/defines/`** — per-define replacement, never a whole-file copy:

```
NCountry = {
    INCORPORATION_TIME_NO_MATCH = 100
}
```

Categories are prefixed with `N` in script (`NCountry`, `NEconomy`, `NPops`, `NEvents`, `NAI`, `NDiplomacy`, …) even though headings list them without the prefix. Defines are global and static; they cannot be set by script at runtime.

## Validation Checklist

- Every new definition has localisation for name (and description where the type generates one).
- Every icon path resolves to an existing `.dds` and matches the expected folder.
- Every modifier key is declared in `common/modifier_type_definitions`.
- New goods appear in a need, and that need appears in every relevant wealth buy package.
- New buildings reference existing PM groups; new PMs reference existing technologies/laws.
- New pop types have their portraits, qualifications, and wage settings set; base defines updated if a base profession is replaced.