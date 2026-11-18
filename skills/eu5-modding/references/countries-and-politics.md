# Countries, Governments, Laws, Estates, International Organizations, Subject Types, Casus Belli, and Peace Treaties

## Country Definition (`in_game/setup/countries/`)

Countries require both a definition and a setup entry.

```
YEM = {
    color = color_culture_yemeni
    color2 = rgb { 16 41 202 }
    culture_definition = yemeni_culture
    religion_definition = sunni

    color3 = hsv { 100 100 100 }
    unit_color0 = rgb { 175 40 40 }
    male_regnal_names = { name_key_1 name_key_2 }
    female_regnal_names = { name_key_3 }
    is_historic = yes
    description_category = military       # administrative / diplomatic / military
    difficulty = 1                        # 1..5
}
```

Full field reference: `references/setup-and-history.md`.

## Country Setup (`main_menu/setup/start/`, `in_game/setup/countries/`)

Country setup supplies ownership, cores, capital, rank, government, technology level, culture, religion, and currency. Full reference: `references/setup-and-history.md`.

Key rules:
- The `countries = { countries = { ... } }` double wrapper is mandatory.
- Ownership helpers set integration level and control together; `control*` helpers set control only.
- `type = pop | building | army | navy` marks non-playable entities.
- Every tag used must also exist in a country definition file.

## Governments

**Folders:** `common/government_types/`, `common/government_reforms/`, `common/heir_selections/`.

Government types declare:
- Applicability and `potential` conditions.
- Succession/heir selection options (`oligarchic_elective`, etc.).
- Estate and power structure defaults.
- Reform slots and unavailable reforms.

Reforms (`common/government_reforms/`) are discrete modifiers with:
- `potential` and `allow`.
- `country_modifier`.
- Optional estate opinion effects and age restrictions.

## Laws

**Folder:** `common/laws/`

```
law_group_name = {
    law_category = administrative         # UI grouping
    law_gov_group = monarchy              # government restriction

    potential = {
        government_type = government_type:monarchy
    }

    option_name = {
        unique = yes                      # only one country may hold this option
        potential = { tag = XXX }
        allow = { current_age = age_5_absolutism }

        country_modifier = {
            monthly_legitimacy = 0.05
            stability_investment = small_stability_investment
        }

        estate_preferences = {
            clergy_estate
            nobles_estate
        }

        years = 2                         # cooldown before changing again
    }
}
```

Set starting laws in country setup: `government = { laws = { censorship = limited_censorship } }`.

## Estates

**Folder:** `common/estates/`

```
estate_name = {
    color = estate_color

    power_per_pop = 25
    tax_per_pop = 150

    rival = -0.01                    # rivalry factor with other estates
    alliance = 0.01                  # alliance factor

    revolt_court_language = court_language   # court_language / common_language / liturgical_language

    characters_have_dynasty = always  # always / sometimes / never
    can_spawn_random_characters = yes
    can_generate_mercenary_leaders = yes
    use_diminutive = no

    bank = yes                        # can provide loans
    ruler = yes                       # crown estate marker
    priority_for_dynasty_head = yes

    satisfaction = {                  # scaled by (satisfaction - LOW_SATISFACTION_THRESHOLD)
        counter_espionage = 0.2
        monthly_prestige = 0.2
    }

    high_power = { ... }              # applied when relative power above threshold
    low_power = { ... }               # applied when relative power below threshold
    power = { ... }                   # scaled by estate power

    opinion = {
        add = {
            desc = "ESTATE_OPINION_BASE"
            value = "opinion(scope:target)"
            multiply = 0.05
        }
    }
}
```

Base-game estates: `crown_estate`, `nobles_estate`, `clergy_estate`, `burghers_estate`, `peasants_estate`.

### Estate membership

Keep four layers distinct when tracing which pops belong to an estate:
1. `common/estates` defines the estate type and its mechanics.
2. `common/pop_types` plus a pop-scoped trigger decide membership (e.g. `dhimmi_estate = { is_dhimmi = yes }`).
3. `country_has_estate = estate_type:<key>` tests presence at runtime.
4. Setup-template `government.privilege` entries only grant starting privileges; they do not define membership.

A scripted estate trigger's valid entry scope is determined by its whole body, not one nested condition. Vanilla `is_gaelic_clans` starts in pop scope and later follows `owner` to country scope, so calling it directly from country scope makes the `owner` link invalid.

### Estate privileges

**Folder:** `common/estate_privileges/`. Privileges grant modifiers, are granted and revoked through effects, and appear in country setup `government = { privilege = { ... } }`.

## International Organizations

**Folder:** `common/international_organizations/`

```
organization_name = {
    has_target = no

    has_leader_country = yes
    leader_title_key = "LEADER_TITLE"
    use_regnal_number = yes
    leader_type = character              # character / country
    leader_change_trigger_type = rulerchange
    leader_change_method = vote
    disband_if_no_leader = no

    has_parliament = yes
    parliament_type = assembly_type
    resolution_widget = parliament
    has_dynastic_power = yes

    only_leader_country_joins_defensive_wars = yes
    gives_military_access_to_all_when_at_war = yes

    join_defensive_wars_always = { ... }
    join_defensive_wars_auto_call = { ... }
    can_declare_war = { ... }

    modifier = { block_from_change_to_kingdom_rank = yes }
    leader_modifier = { diplomatic_capacity = 1 }
    international_organization_modifier = { max_elector = 4 }

    create_visible_trigger = { ... }
    invite_visible_trigger = { ... }
    can_lead_trigger = { ... }
    can_join_trigger = { ... }
    can_leave_trigger = { ... }
    auto_leave_trigger = { ... }
    auto_disband_trigger = { ... }
    can_vote_in_parliament = { ... }

    on_joined = { ... }
    on_left = { ... }
    monthly_effect = { ... }

    variables = { ... }
}
```

Starting IOs are created through `main_menu/setup/start` with `international_organization_manager`.

## Subject Types

**Folder:** `common/subject_types/`

```
subject_type_name = {
    subject_pays = subject_pays_vassal
    color = subject_vassal
    level = 2

    visible_through_diplomacy = { ... }
    visible_through_treaty = { ... }
    creation_visible = { ... }

    join_offensive_wars_always = { ... }
    join_offensive_wars_can_call = { ... }
    join_defensive_wars_always = { ... }

    diplomatic_capacity_cost_scale = 1.0
    strength_vs_overlord = -0.5
    ...
}
```

## Casus Belli

**Folder:** `common/casus_belli/`

```
cb_dissolve_tatar_yoke = {
    visible = {
        international_organization:tatar_yoke ?= {
            country_has_special_status = {
                type = special_status:tatar_tax_collector
                country = root
            }
        }
        scope:target = c:GLH
    }
    allow_creation = {
        country_rank = country_rank:rank_kingdom
    }
    war_goal_type = dissolve_tatar_yoke_wargoal
}
```

- `visible` and `allow_creation` receive `ROOT` = fabricating country, `scope:target` = target country.
- `speed = <float>` defines acquisition progress speed; without it the game falls back to a very low minimum.
- `can_expire = no` makes the CB permanent; otherwise `years`, `months`, `weeks`, `days` accept script values (ROOT = receiver, `scope:target` = target). Without either, the `CASUS_BELLI_MONTHS` define controls duration.
- Every casus belli requires a `war_goal_type`.

## Wargoals

**Folder:** `common/wargoals/`

Required localisation: `war_goal_<key>` and `war_goal_<key>_desc`.
Icon: `<WARGOAL_ICON_PATH define>/<wargoal key>.dds`, falling back to `ICON_DEFAULT_NAME`.

## Peace Treaties

**Folder:** `common/peace_treaties/`

```
disband_kontor = {
    cost = {
        add = {
            desc = "DIPLOREASON_BASE"
            value = "scope:target.location_peace_cost(scope:loser|scope:winner)"
            multiply = 0.75
        }
    }
    base_antagonism = 1
    antagonism_type = antagonism_disband_kontor
    category = location

    potential = {
        scope:war = {
            OR = {
                has_casus_belli = no
                casus_belli = { is_trade_cb = no }
            }
        }
    }
    allow = { ... }

    select_trigger = {
        looking_for_a = location
        source = recipient
        target_flag = target
        visible = {
            location_building_level = {
                building_type = building_type:hanseatic_kontor
                value > 0
                owner = scope:recipient
            }
        }
    }

    effect = {
        scope:target = {
            destroy_building = "building(building_type:hanseatic_kontor|scope:recipient)"
        }
    }

    ai_desire = { value = 10 }
}
```

- `potential` and `allow` receive only `scope:winner`, `scope:loser`, `scope:war`.
- `effect` receives the full scope set, including any `select_trigger` targets.
- `category` values: `country`, `location`, `province`, `area`, `dismantlefort`, `cores`, `releasecountry`, `cancelsubject`, `seizeland`, `misc` (default). If omitted, the category is inferred from `looking_for_a`.
- `cost` is a script value for warscore cost; `ai_desire` is a script value for AI weighting; `antagonism_type` sets the antagonism classification.

## War Setup at Start

`main_menu/setup/start` `war_manager` supports `war`, `civil_war`, and `truce` entries. Full reference: `references/setup-and-history.md`. The first listed attacker/defender becomes the war leader on that side.

## Practical Rules

- Every `government_type:`, `law` policy, `reform`, and `special_status:` reference must resolve, or the effect silently aborts.
- Modifiers inside estates, laws, and reforms must exist in `common/modifier_type_definitions`.
- International organization keys are referenced as `international_organization:<key>`; the scope is valid even when the organization has no members.
- Subject type changes are scripted through effects; there is no automatic conversion.
- Adding a law option requires localisation for the option key and its description; missing keys render raw identifiers.