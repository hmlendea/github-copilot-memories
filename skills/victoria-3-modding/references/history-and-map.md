# History, State Setup, and Map Modding

## History Files

**Folder:** `common/history/`. Files and subfolders may be named arbitrarily; only the top-level history keys matter.

Victoria 3 executes history keys in a fixed order. Each key is an effect block with no inherent scope, so every effect inside must scope explicitly.

| Order | Key | Folder |
|-------|-----|--------|
| 1 | `STATES` | `common/history/states` |
| 2 | `COUNTRIES` | `common/history/countries` |
| 3 | `POPS` | `common/history/pops` |
| 4 | `DIPLOMACY` | `common/history/diplomacy` |
| 5 | `POPULATION` | `common/history/population` |
| 6 | `POWER_BLOCS` | `common/history/power_blocs` |
| 7 | `INTERESTS` | `common/history/interests` |
| 8 | `BUILDINGS` | `common/history/buildings` |
| 9 | `PRODUCTION_METHODS` | `common/history/production_methods` |
| 10 | `MILITARY_FORMATIONS` | `common/history/military_formations` |
| 11 | `AI` | `common/history/ai` |
| 12 | `TREATIES` | `common/history/treaties` |
| 13 | `LOBBIES` | `common/history/lobbies` |
| 14 | `DIPLOMATIC_PLAYS` | `common/history/diplomatic_plays` |
| 15 | `TRADE` | `common/history/trade` |
| 16 | `GLOBAL` | `common/history/global` |
| 17 | `POLITICAL_MOVEMENTS` | `common/history/political_movements` |
| 18 | `CHARACTERS` | `common/history/characters` |
| 19 | `GOVERNMENT` | `common/history/government` |
| 20 | `GOVERNMENT_SETUP` | `common/history/government_setup` |
| 21 | `MILITARY_DEPLOYMENTS` | `common/history/military_deployments` |

History only sets starting state for new games. It never changes mechanics, and it has no effect on saves already in progress.

### States History

Creates the actual states inside state regions and the countries that own them. A country with no state here does not exist at game start.

```
STATES = {
    s:STATE_IDAHO = {
        create_state = {
            country = c:ORG
            owned_provinces = { x4B49F2 xE836AA xB94979 }
            state_type = unincorporated      # optional; default is incorporated
        }
        create_state = {
            country = c:BNN
            owned_provinces = { x87941A xE65BC2 }
        }
        add_homeland = cu:nez_perce
        add_homeland = cu:paiute
        add_claim = c:ORG
    }
}
```

Provinces are declared in `map_data/state_regions/`, not here. `treaty_port` is the other alternative `state_type`.

### Countries History

Sets government, laws, technologies, institutions, taxation, and election timing. Only countries and their empty states exist at this point — no pops, buildings, or goods.

```
COUNTRIES = {
    c:GBR ?= {
        set_next_election_date = 1836.2.1
        ig:ig_intelligentsia = { add_ruling_interest_group = yes }
        set_tariffs_import_priority = g:fabric
        effect_starting_technology_tier_1_tech = yes
        add_technology_researched = labor_movement
        set_tax_level = medium
        add_taxed_goods = g:liquor
        activate_law = law_type:law_monarchy
        set_institution_investment_level = {
            institution = institution_colonial_affairs
            level = 2
        }
    }
}
```

Use `c:TAG ?= { }` so a disqualified country does not log an error.

### Pops History

Creates pops per state with `create_pop` inside a state scope. Scope into a split state either way:

```
s:STATE_MINSK = { region_state:RUS = { } }
s:STATE_MINSK.region_state:RUS = { }
```

```
POPS = {
    s:STATE_GUATEMALA = {
        region_state:UCA = {
            kill_population_percent_in_state = { percent = 1 }
        }
        region_state:GOK = {
            create_pop = { culture = orcish size = 200000 }
            create_pop = {
                pop_type = slaves
                culture = central_american
                size = 164404
            }
        }
    }
}
```

Omitted `pop_type` defaults to laborers; omitted `religion` inherits from the culture.

### Diplomacy History

```
DIPLOMACY = {
    c:SPA ?= {
        create_diplomatic_pact = { country = c:CUB type = colony }
    }
    c:NET ?= {
        create_bidirectional_truce = { country = c:BEL months = 40 }
    }
}
```

### Building, Production Method, Character, and Military History

- `BUILDINGS` uses `create_building` in state scope with the building key, level, reserves, and active production methods.
- `PRODUCTION_METHODS` adjusts starting PMs per building.
- `CHARACTERS` defines and places starting characters, referencing templates or explicit blocks.
- `MILITARY_FORMATIONS` and `MILITARY_DEPLOYMENTS` create armies, fleets, and their stationing.
- `AI` sets starting strategies and secret goals; `TREATIES`, `LOBBIES`, `DIPLOMATIC_PLAYS`, `TRADE`, and `POLITICAL_MOVEMENTS` set up their systems.
- `GLOBAL` and `POPULATION` handle global and population-level state.

## State Regions

**Folder:** `map_data/state_regions/<file>.txt`. Files here load wholesale, so use uniquely named files.

```
STATE_SINGAPORE = {
    id = 800
    subsistence_building = "building_subsistence_rice_paddies"
    provinces = { "xC00130" }
    city = "xC00130"
    port = "xC00130"
    farm = "xC00130"
    mine = "xC00130"
    wood = "xC00130"
    arable_land = 4
    arable_resources = { "bg_rice_farms" "bg_livestock_ranches" }
    capped_resources = {
        bg_logging = 1
        bg_fishing = 12
    }
    resource = {
        type = "bg_rubber"
        undiscovered_amount = 40
    }
    naval_exit_id = 3052
}
```

- `id` must be unique across all state regions.
- Every province belongs to exactly one state region; moving a province means removing it from the old block and adding it to the new one, including its hub assignments.
- Province IDs come from hovering land in debug mode, or from the hex colours in `map_data/provinces.png`.
- `arable_resources` lists allowed farm building groups; `capped_resources` fixes non-arable resource caps; `resource` declares discoverable deposits.

State regions are grouped into strategic regions in `common/strategic_regions/`:

```
region_indochina = {
    graphical_culture = "asian"
    capital_province = x5C3070
    map_color = { 0.9 0.1 0.1 }
    states = {
        STATE_CAMBODIA STATE_MEKONG STATE_SINGAPORE
    }
}
```

Restating an existing strategic region replaces it, so prefer appending to the list.

## Overwriting an Existing State

Adding a state region alone does not repartition the world. The full procedure:

1. **`common/history/states`** — create the new split state with all provinces except one per existing owner, so the original states remain valid.
2. **`common/history/pops`** — kill the original populations for the affected split states, then recreate the intended pops. Skipping this leaves buildings without workers at game start.
3. **`common/history/buildings`** — create or repartition buildings in the new state.
4. **`common/on_actions`** — annex the leftover provinces in `on_game_started` through a custom on action:

```
on_game_started = {
    on_actions = { my_mod_history_setup }
}

my_mod_history_setup = {
    effect = {
        s:STATE_GUATEMALA = {
            set_owner_of_provinces = {
                country = c:GOK
                provinces = { xDEC8D3 xD0B040 }
            }
        }
    }
}
```

5. **Localisation** — `localization/english/map/<file>_l_english.yml` containing `STATE_SINGAPORE:0 "Singapore"`.

Never overwrite a base game history file; new files merge by content, not by filename.

## Province Map and Map Editor

- Launch the editor with `-map editor` in Steam launch options (or the `map_editor` console command in debug mode). It edits the map of the mod selected in the launcher.
- The **heightmap** is a greyscale image where black is the lowest elevation and white the highest; it drives the non-paper map.
- The **province map** is `map_data/provinces.png`, where each distinct colour is a province and that colour is its hex province ID.
- **Rivers**, **lakes**, **hubs and locators**, and the **paper map** are edited inside the editor; exported river maps must use the documented reference colours.
- Large heightmap or province-map changes require a restart; they are not hotloadable.

## Map-Adjacent Definitions

- **`common/geographic_regions/`** — scripted groups of strategic and state regions with a `short_key`, used for cheap iteration and map highlighting in localisation.
- **`common/terrain/`**, **`common/terrain_manipulators/`**, **`common/state_traits/`** — terrain kinds, graphical manipulation, and state-level traits.
- **`common/harvest_condition_types/`** — regional harvest conditions that alter production.
- **`common/strategic_regions/`** — the strategic layer grouping state regions.

## Adding a New Country

1. Pick an unused three-letter tag (search vanilla `common/country_definitions`).
2. Add the definition in `common/country_definitions/` with colour, type, tier, cultures, and capital.
3. Add at least one `create_state` in `common/history/states`, or the country will not exist at game start.
4. Add `COUNTRIES` history for laws, government, and technology.
5. Add pops, buildings, and characters as needed.
6. Localise the tag, its adjective (`TAG`, `TAG_ADJ`), and any dynamic names.
7. Optionally add a `common/flag_definitions/` entry and a coat of arms.

## Validation Checklist

- Every province appears exactly once across all state regions.
- Every hub references a province inside its own state region.
- New state region `id` values are unique and unused.
- Split-state edits repartition pops and buildings, not just provinces.
- History changes are verified on a fresh game start, never on an existing save.
- Map or province changes are verified after a full restart, not by hotloading.