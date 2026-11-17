# Economy, Planets, Buildings, Districts, Jobs, Decisions

## Resources

Defined in `common/strategic_resources/*.txt` (**DUPL**).

```
minerals = {
    tradable = yes
    market_amount = 100
    market_price = 100
    max = 15000
    deficit_modifier = minerals_deficit      # static modifier applied while in deficit
    prerequisites = { "tech_mine_volatile_motes" }
    visibility_prerequisite = { always = yes }
    tooltip_decimals = 0
    fixed_max_amount = no
    ai_weight = { weight = 1 }
    ai_wants = { base = 1000 }
}
```

To make a resource visible, add it to an existing group in `interface/resource_groups/*.txt`. A **new** group additionally requires editing `interface/main.gui`.

## Economy Units

Most definitions declare cost, upkeep, and production with an economy unit:

```
resources = {
    category = planet_researchers
    produces = {
        physics_research = 4
        engineering_research = 4
        society_research = 4
    }
    produces = {
        trigger = { exists = owner owner = { has_valid_civic = civic_technocracy } }
        unity = 1
    }
    upkeep = { consumer_goods = 2 }
    cost = { minerals = 100 }
}
```

`category` binds the unit to a modifier namespace: `planet_researchers_produces_mult` and friends are auto-generated per category.

## Economy Categories

`common/economic_categories/*.txt` (LIOS).

```
rare_edicts = {
    use_for_ai_budget = yes
    parent = edicts
    generate_mult_modifiers = { cost }
}
```

`generate_mult_modifiers` produces modifiers that scale the cost of every unit in the category. `parent` nests the category for AI budget purposes.

## Buildings

`common/buildings/*.txt` (LIOS since 3.3). Requires a matching localisation key pair (`<key>` and `<key>_desc`) and, for a custom icon, `gfx/interface/icons/buildings/<key>.dds` plus an explicit `icon = <key>` (otherwise a generic icon is used).

```
building_my_monument = {
    base_buildtime = 480
    category = unity                    # pop_assembly government resource manufacturing research trade amenity unity army
    icon = building_my_monument
    capital = no
    can_build = yes
    can_demolish = yes
    can_be_disabled = yes
    can_be_ruined = yes
    position_priority = 200
    base_cap_amount = 1
    is_capped_by_modifier = no          # generates <key>_max_add
    prerequisites = { "tech_my_tech" }
    show_tech_unlock_if = { ... }
    upgrades = { building_my_monument_2 }
    potential = { ... }                 # hidden if false
    allow = { ... }                     # shown but disabled if false
    abort_trigger = { ... }
    ruined_trigger = { ... }
    destroy_trigger = { ... }
    convert_to = { building_other }
    planet_modifier = { ... }
    triggered_planet_modifier = { potential = { ... } ... }
    country_modifier = { ... }
    triggered_country_modifier = { potential = { ... } ... }
    resources = { category = ... cost = { ... } upkeep = { ... } }
    triggered_desc = { trigger = { ... } text = "loc_key" }
    on_queued = { ... }  on_unqueued = { ... }  on_built = { ... }  on_destroy = { ... }
    ai_weight = { ... }
    ai_resource_production = { ... }
}
```

Buildings normally provide **jobs**, not resources: add a `pop_jobs` entry and have the building add those jobs.

`position_priority`: `0` = capitals, `100` = strongholds/fortresses/planetary shield generators and some civic buildings, default `200`.

`hidden_trigger = { OR = { owner = { is_ai = no } <extra> } }` inside `allow` gives the AI a stricter or looser rule than the player.

## Districts

`common/districts/*.txt` (LIOS since 3.3). Districts are also zone hosts in 4.0+.

```
district_my_generator = {
    base_buildtime = 240
    is_capped_by_modifier = yes         # default yes; generates <key>_max_add
    potential = { ... }                 # false ⇒ removed or converted
    show_on_uncolonized = { ... }       # planet or FROM scope
    allow = { ... }
    conversion_ratio = 0.5
    convert_to = { district_city }
    resources = { category = ... cost = { ... } upkeep = { ... } }
    planet_modifier = { ... }
    triggered_desc = { ... }
}
```

In `potential`, test the planet type with `uses_district_set`, never `is_planet_class`.

## 4.0 (Phoenix) Zones and Zone Slots

4.0 replaced per-district building slots with **zone slots** and **zones** (district specialisations), and introduced the concept of a **primary** district.

Migration checklist for custom districts:
1. Mark the primary district of each set with `default_starting_district = yes`.
2. Give the primary district three slots (`slot_city_government`, `slot_city_01`, `slot_city_02`, or custom equivalents).
3. Specify a zone slot for **every** district.
4. Reduce district sets from five districts to four; production that used to come from a fifth district now comes from zones attached to the primary district.
5. Every 4.0 building must belong to a building set.

Zones live in `common/zones/`; see `common/zones/99_HOW_TO_ZONE.txt` in the installation for the authoritative schema. Zone and district-slot modding has known cross-mod compatibility problems; state that limitation when a mod touches them.

Reference: `gfx/interface/icons/buildings`, `gfx/interface/icons/districts`, `gfx/interface/icons/jobs`.

## Jobs

`common/pop_jobs/*.txt` (LIOS since 3.3). A job declares category, weight in the pop job selection, and an economy unit.

```
job_my_researcher = {
    category = specialist
    condition = { ... }             # planet scope; whether the job exists
    weight = 10
    building_icon = building_my_lab
    possible_pre_triggers = { has_owner = yes is_robotic = no }
    resources = { ... }
}
```

Job categories and subcategories come from `common/economic_categories/*` and decide which modifiers apply to which jobs.

## Pop Categories and Groups

`common/pop_categories/*.txt` (LIOS). Job assignment, happiness, and political power keys hang off categories. In 4.0+ pops are grouped (`pop_group` scope) and the former per-pop modifiers, ethics attraction, and living standards are expressed through pop groups.

## Decisions

`common/decisions/*.txt` (LIOS). Requires `<key>`, `<key>_desc`, and usually `<key>_tooltip` localisation.

```
decision_my_decision = {
    icon = decision_my_decision
    picture = GFX_evt_my_picture
    potential = { ... }             # country scope; hidden if false
    allow = { ... }                 # visible but disabled if false
    effect = { ... }
    ai_check_interval = 12          # months; 0 disables AI use
    ai_weight = { weight = 10 }
}
```

## Edicts

`common/edicts/*.txt` (LIOS). Economy unit for cost, `potential`/`allow`, `modifier`, and AI weight.

## Policies

`common/policies/*.txt` (LIOS). Option groups with `trigger` and `modifier` per option. Policy option keys are referenced from `game_rules` and ethics attraction.

## Situations

`common/situations/*.txt` (LIOS, 3.3+). Situation types declare `target`, progress blocks (`progress = { ... }`), `on_start`, `on_finish`, and monthly/period effects. Situations present in-scope UI and can call events.

## Terraforming

`common/terraform/*.txt` (**DUPL**). One entry per valid planet-class pair, with cost, duration, and conditions.

## Deposits and Planet Modifiers

- `common/deposits/*.txt` (LIOS): orbital deposits, planetary features, blockers. `deposit_categories` lists allowable categories.
- `common/planet_modifiers/*.txt` (LIOS): permanent planet-level modifiers applied by deposits, buildings, or events.
- `common/static_modifiers/*.txt` (LIOS): named reusable modifier blocks, including `deficit` modifiers for resources.

## Validation Checklist

1. Every new resource appears in a resource group in `interface/resource_groups/`.
2. Every building/district/job has an icon `.dds`; a building also needs `icon =` set explicitly.
3. Every `<key>` string pair exists: `<key>` and `<key>_desc` for buildings and districts, `<key>_desc` and tooltip keys for decisions.
4. `potential` uses `uses_district_set` for districts.
5. Generated modifiers (`<key>_max_add`) are only expected where `is_capped_by_modifier = yes`.
6. `error.log` clean after opening the planet view, the decision list, and the edict list.