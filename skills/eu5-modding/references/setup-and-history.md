# Setup Modding: Start Files, Managers, Country Setup, and Templates

Setup modding builds the "save file" the game opens at start. It lives in the `setup/` folders of the `main_menu` and `in_game` top folders.

## File Locations and Encoding

| Folder | Top Folder | Contents | Encoding |
|--------|-----------|----------|----------|
| `setup/start/` | `main_menu` | Start managers (pops, countries, wars, diplomacy, ...) | UTF-8 **without** BOM |
| `setup/countries/` | `in_game` | Country definitions (colours, cultures, religions, regnal names) | UTF-8 **with** BOM |
| `setup/templates/` | `main_menu` | Reusable country setup templates | UTF-8 **with** BOM |

Examples:
- `in_game/setup/countries/anatolia.txt`
- `main_menu/setup/templates/amerindian_monarchy.txt`
- `main_menu/setup/start/02_core.txt`

If `setup/start/` files are BOM-prefixed, the engine fails to read the top-level function calls. If `setup/countries/` or `setup/templates/` lack the BOM, some parsers skip them.

## Additive Consideration

Most managers in `setup/start/` merge additively: new keys add on top of vanilla. Removing a vanilla entry requires a **whole-file replacement**, not `INJECT:` or `REPLACE:`.

## Load Order Requirements

Some objects must be created in order:
- Dynasties used by characters in `character_db` must be created in `dynasty_manager` first.
- Characters referenced as `father`/`mother`/`spouse` must be created before their referencing entry.
- Advances must be defined before the advance that requires them, when using `requires`.

## Managers in `setup/start/`

### `institution_manager`

```
institution_manager = {
    institutions = {                    # required block
        feudalism = {
            active = no                 # can it spread or be embraced?
            birth_place = krakow        # origin location; guarantees presence + applies its origin static modifier
        }
    }
}
```

### `religion_manager`

```
religion_manager = {
    hanafi_school = {
        relation = {
            maturidi_school = kindred    # enemy / negative / neutral / positive / kindred
            maliki_school = kindred
        }
    }
    hanbali_school = {                    # shorthand equivalent to the above
        athari_school = kindred
        mutazili_school = enemy
    }
    catholic = {
        timed_modifier = { ... }         # timed modifier definition
        saint = {
            character = pol_saint_wojciech
            country = POL
        }
    }
}
```

### `market_manager`

```
market_manager = {
    add_market = lubeck
}
```

### `dynasty_manager`

```
dynasty_manager = {
    example_dynasty = {
        name = { name = bjalbo_atten_dynasty }   # localisation key on the right
        dynasty_name_type = location             # location / location_ancient / patronym / descendant
        home = linkoping
        male_names = { name_birger name_eric name_magnus name_waldemar }
        female_names = { name_catherine name_christine name_ingeborg name_rikissa }
    }
}
```

### `character_db`

```
character_db = {
    example_character = {
        first_name = { name = name_example }
        nickname = { name = example_nickname }
        last_name = { name = name_example_last_name }
        culture = swedish
        religion = catholic
        adm = 50
        dip = 60
        mil = 70
        birth_date = 1210.1.1
        death_date = 1266.10.21
        female = yes
        birth = vadstena
        ruler_trait = conqueror
        admiral_trait = buccaneer
        general_trait = master_of_arms
        cabinet_trait = influential
        health_trait = blind
        religious_figure_trait = efficient_administrator
        child_trait = gifted
        tag = SWE
        estate = nobles_estate
        dynasty = example_dynasty
        father = example_character_father
        mother = example_character_mother
        spouse = example_character_spouse
        has_patronym = yes
        timed_modifier = { ... }
        fertility = 100
        artist_skill = 0.85
        artist = writer
        artist_trait = adept
    }
}
```

Character skill ranges and traits come from `common/traits/` and related definitions.

### `locations`

Defines location population, institution spread, rank, and building templates.

```
locations = {
    stockholm = {
        define_pop = {
            culture = swedish
            religion = catholic
            type = nobles
            size = 1                   # 1 = 1000 people; 0.001 = 1 person
        }
        rank = town                    # omitted = lowest rank
        town_setup = important_scandinavian_town
        feudalism = yes                # starting institution presence
        timed_modifiers = {
            timed_modifiers = {
                {
                    modifier = herring_market
                    start_date = 1337.1.1
                    end_date = 1340.1.1
                    size = 1
                }
            }
        }
    }
}
```

Starting pop logic: defined pops are **not** final. Extra pops fill pop-type caps derived from buildings, RGOs, and country modifiers; excess moves to peasants; a monthly tick applies; foreign-building pop types are appended. `-leavepops` disables all recalculation for testing.

### `road_network`

```
road_network = {
    london = barking                   # pair of adjacent locations
}
```
Roads chain location by location; the earliest road is chosen by default.

### `countries`

```
countries = {
    countries = {                      # the second entry is required
        SWE = {
            own_control_core = { stockholm nykoping }
            our_cores_conquered_by_others = { laholm asbo }
            capital = stockholm
            country_rank = rank_kingdom
            accept_cultures = { finnish gutnish }
            tolerated_cultures = { tavastian karelian kvens }
            culture = swedish
            religion = catholic
            discovered_provinces = { gardr_province }
            discovered_areas = { celtic_sea_area }
            discovered_regions = { north_german_region }
            starting_technology_level = 3
            is_valid_for_release = no
            ai_advance_preference_tags = { exploration = 5 }
            currency_data = { gold = 10000 prestige = 50 }
            dynasty = bjalbo_atten_dynasty
            dynasty = aspenas_atten_dynasty
            type = location            # location / pop / building / army / navy
            include = "catholic_monarchy"
            include = "expl_scandinavia"
            government = { ... }
        }
    }
}
```

#### Location ownership forms

| Field | Integration | Sets Control | Sets Ownership |
|-------|-------------|--------------|----------------|
| `own_control_core` | core | yes | yes |
| `own_control_integrated` | integrated | yes | yes |
| `own_control_conquered` | conquered | yes | yes |
| `own_control_colony` | colony | yes | yes |
| `own_core` | integrated | no | yes |
| `own_integrated` | integrated | no | yes |
| `own_conquered` | conquered | no | yes |
| `own_colony` | colony | no | yes |
| `control_core` | core | yes | no |
| `control` | none | yes | no |
| `our_cores_conquered_by_others` | core | no | no |

Pop-based non-playable country:
```
NUE = {
    type = pop
    add_pops_from_locations = { matootonha pabaska ruhptare marapa pocasse }
}
```
Mixed settled/unsettled nation: combine `own_control_core` with `add_pops_from_locations`.

#### Government block

```
government = {
    ruler = random                       # or a character script key
    consort = arb_constanza_saluzzo
    heir = ver_alberto_ii_scala
    designated_heir_reason = infant_emperor
    active_regent = jap_oyama_hidetomo_spouse
    type = republic
    heir_selection = oligarchic_elective

    centralization_vs_decentralization = 100
    traditionalist_vs_innovative = -70

    reforms = { veche_republic merchant_republic }

    parliament = { parliament_type = council }

    privilege = { novgorod_ivans_hundred tysiatskii_privilege }

    laws = {
        censorship = limited_censorship
        republican_foundation_law = republicanism_policy
    }

    ruler_term = {
        character = zan_al_hassan_ibn_talut_mahdali
        start_date = 1277.1.1
        end_date = 1294.1.1
        regnal_number = 1
    }

    regnal_numbers = {
        name_chungnyeol = 1
        Chungsuk = 2
    }

    inherit_ruler_terms = YMT
}
```

### `work_of_art_manager`

```
work_of_art_manager = {
    painting = {
        location = london
        origin = canterbury
        quality = 75
        key = loc_key
        creation_date = 1330.6.1
        artist = character_key
    }
}
```

### `diplomacy_manager`

```
diplomacy_manager = {
    opinion = {
        first = SKE
        second = SWE
        type = opinion_bad_monarch
    }
    trust = { first = SKE second = SWE type = opinion_bad_monarch }
    rival = { first = TEU second = POL }

    scripted_oneway = { first = ENG second = SBL type = guarantee }
    # scripted_mutual = { ... }

    dependency = {
        first = ENG
        second = WLS
        subject_type = dominion
        start_date = 1283.1.1
    }
}
```

### `building_manager`

```
building_manager = {
    order_stronghold = {
        location = calatrava
        tag = CAS
        level = 1
    }
}
```

Town setups (`common/town_setups/`) are reusable building lists:
```
important_scandinavian_town = {
    brewery = 1
    temple = 1
    tools_guild = 1
}
```

### `development`

Development is additive across conditions:
```
development = {
    coastal = 1
    river = 2
    road = 3
    grasslands = -1
    tropical = -2
    flatland = -3
    city = 0.5
    scandinavian_region = 0.25
    svealand_area = 0.25
    uppland_province = 0.25
    stockholm = 0.25
}
```
Supported selectors: location, `province_definition`, area, region, `location_rank`, vegetation, topography, climate, `coastal`, `river`, road. Subcontinent and continent are not supported.

### `international_organization_manager`

```
international_organization_manager = {
    add_international_organization = {
        type = hre
        creation_date = 962.2.2
        map_color = rgb { 255 0 0 }
        members = { FRA ENG }
        leader = FRA
        regions = { france_region britain_region }
        areas = { wallonia_area }
        provinces = { roman_flanders_province }
        locations = { cassel }
        elector = { FRA ENG }
        laws = { only_imperial_religion_policy no_monetary_contribution }
        icon = daoism
        ruler_term = {
            character = ogk_otto_liudolfinger
            start_date = 962.2.2
            end_date = 967.12.25
            regnal_number = 1
        }
        variables = { var_1 = 20 var_2 = religion:catholic }
    }
}
```
If `leader` is omitted or absent from `members`, the first listed member becomes leader.

### `war_manager`

```
war_manager = {
    truce = {
        attacker = GRA
        attacker = MOR
        defender = CAS
        end_date = 1340.4.1
    }
    truce = {
        attacker = FRA
        defender = CAS
        start_date = 1335.6.1
        months = 60
    }

    war = {
        war_name = {
            name = localizable_key_for_war_name
            ordinal = 1
            first = { name = localizable_key_for_name }
            second = { name = localizable_key_for_name_2 }
        }
        start_date = 1331.5.4
        action = 1336.12.2
        take_province = {
            type = crusade_conquest
            casus_belli = cb_crusade
            location = vilnius
        }
        attacker = {
            country = TEU
            request = { reason = Instigator }
        }
        defender = {
            country = POL
            request = { reason = Target }
        }
    }

    civil_war = { ... }                # same shape as war
}
```
The first attacker / defender is the war leader for that side.

### `exploration_manager`

```
exploration_manager = {
    add_exploration_preference = {
        country = KUR
        modifier = 2
        continent = north_america
        sub_continent = india
        region = brazil_region
        area = lesser_antilles_area
        # provinces and locations are not supported
    }
}
```

### `disease_outbreak_manager`

```
disease_outbreak_manager = {
    add_disease_resistance = {
        type = bubonic_plague
        resistance = 0.1
        locations = { paris london }
        provinces = { south_holland_province north_holland_province }
        areas = { north_portugal_area south_portugal_area }
        regions = { italy_region }
        sub_continents = { eastern_europe }
        continents = { asia }
    }

    add_disease_outbreak = {
        type = influenza
        resistance = 0.1
        infected = 0.1
        origin = 1000
        regions = { italy_region }
    }
}
```
Both effects **set** values rather than adding. The engine also adds +5% resistance on top of the declared amount.

### `colony_manager`

```
colony_manager = {
    vasterbotten_province = {
        tag = SWE
        category = exclusive          # or same_religion
        reason = new_treaty
    }
}
```
Only `province_definition` keys are valid for colonial claims.

## Timed Modifiers

Reusable shape found across managers:
```
{
    modifier = herring_market
    start_date = 1111.1.1
    end_date = 1340.1.1
    size = 1                          # 1 = normal, 2 = double, 0.5 = half
}
```

## Country Definitions (`setup/countries/`)

Every tag used in `countries` must also be defined here. Definitions supply map colours, unit colours, default culture/religion, and regnal name pools.

```
TUR = {
    color = map_ottomans
    color2 = rgb { 126 203 120 }
    color3 = hsv { 100 100 100 }
    unit_color0 = rgb { 175 40 40 }
    unit_color1 = rgb { 76 78 114 }
    unit_color2 = rgb { 18 90 47 }
    culture_definition = turkish_culture
    religion_definition = sunni
    male_regnal_names = { name_key_1 name_key_2 }
    female_regnal_names = { name_key_3 name_key_4 }
    is_historic = yes                 # historical country; no cores, no starting existence
    description_category = military   # administrative / military / diplomatic
    difficulty = 1                    # 1 (very easy) to 5 (very hard); shown in country selection
}
```

## Templates (`setup/templates/`)

Templates store reusable country setup fields and are referenced with `include = "<template_key>"`. The template key is the **filename** (without `.txt`), unlike most script objects.

```
include = "subsaharan_tribe"

government = {
    laws = {
        marriage_law = muslim_marriage
        heir_religion_law = heir_same_religion
        legal_code_law = sharia_law_policy
    }
}
```

Templates are used only in country setup. Including a template is equivalent to pasting its blocks; explicit fields override template fields.

## Practical Rules

- Removing a vanilla entry requires replacing the whole file — no selective delete exists in setup.
- `location_templates.txt` religion/culture are placeholders; the actual pop culture/religion come from `06_pops.txt` (or this file, if no pops are defined for that location).
- Define dynasties before characters; define characters before referencing them as parents/spouses.
- Do not rely on setup-declared development, pops, or resistance as the final runtime values; they are re-derived on load.
- Keep setup "start" files ASCII-clean and UTF-8 without BOM, or initial parsing fails silently.