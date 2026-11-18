# Politics, Diplomacy, and AI Content

All paths below are relative to the mod folder (mirroring `Victoria 3/game`). Every folder listed here supports `INJECT:` / `REPLACE:` unless stated otherwise.

## Countries

**`common/country_definitions/`**

```
GER = {
    color = { 147 130 110 }        # rgb 0-255, or hsv{ ... } / hsv360{ ... }
    country_type = recognized      # recognized / unrecognized / decentralized / colonial
    tier = empire                  # city_state / principality / grand_principality / kingdom / empire / hegemony
    cultures = { north_german south_german }
    religion = protestant          # optional; defaults to first culture's religion
    capital = STATE_BRANDENBURG
    is_named_from_capital = yes    # optional
    social_hierarchy = british_indian_caste_system
    primary_unit_color = { 20 20 120 }
}
```

- The tag is the block key: three letters, unique across the game.
- Scripted characteristics revert to these values if the country is destroyed and later released.

**`common/country_formation/`** — unifications. Requires either an explicit `states = { ... }` list or `use_culture_states = yes`. Supports `required_states_fraction` (default 0.75), `possible`, `ai_will_do`, `max_num_formation_candidates` (default 3), `can_be_formation_candidate`, `can_be_unification_target`.

**`common/country_creation/`** — dynamic country creation rules used by `create_country`-style effects.

**`common/country_types/`**, **`common/country_ranks/`** — recognised/decentralized types and prestige ranks; `rank_value:great_power` and friends are referenced from `country_rank =` triggers.

**`common/dynamic_country_names/`**, **`common/dynamic_country_map_colors/`** — conditional name and colour overrides.

## Laws

**`common/law_groups/`** and **`common/laws/`**.

```
lawgroup_health_system = {
    base_enactment_days = 30
    enactment_approval_mult = 1.0
    affected_by_regime_change = no
    change_allowed_trigger = { always = yes }
    linked_social_hierarchy = <key>       # optional
}
```

```
law_no_health_system = {
    group = lawgroup_health_system
    icon = "gfx/interface/icons/law_icons/no_health_system.dds"
    progressiveness = 0
    ai_will_do = { always = no }
    ai_enact_weight_modifier = { value = 0 }
}
```

Law elements: `modifier`, `institution`, `institution_modifier`, `unlocking_technologies`, `unlocking_laws`, `requires_law_or`, `disallowing_laws`, `can_enact`, `parent` (variant law), `is_visible`, `on_enact`, `on_activate`, `on_deactivate`, `tax_modifier_<very_low|low|medium|high|very_high>`, `can_impose`, `ai_impose_chance`.

The script name generates the localisation keys `<name>` and `<name>_desc`.

## Interest Groups, Traits, Parties, Ideologies

**`common/interest_groups/`**

```
ig_example = {
    color = hsv{ 0.09 0.29 0.39 }
    texture = "gfx/interface/icons/ig_icons/armed_forces.dds"
    layer = "revolution_dynamic_armed_forces"
    index = 0                                # unique, ordering in UI
    ideologies = { ideology_jingoist ideology_loyalist ideology_patriotic }
    character_ideologies = { ideology_moderate }
    enable = { always = yes }                # country scope, re-evaluated monthly
    traits = { ig_trait_patriotic_fervor }   # deprecated; prefer on_enable assignment
    on_enable = { }
    on_disable = { }
    priority_cultures = { rule = { trigger = { } cultures = { } } }
    on_character_ig_membership = { }
}
```

- `enable` is re-evaluated monthly; dynamic triggers mean the IG may be missing at game start.
- Traits live in `common/interest_group_traits/` and modify approval or political strength.

**`common/parties/`**, **`common/ideologies/`** — parties aggregate IGs; ideologies supply law stances used by characters, IGs, and movements.

**`common/discrimination_traits/`**, **`common/discrimination_trait_groups/`** — `type = heritage | language | tradition`; religions may only use heritage traits.

**`common/social_hierarchies/`**, **`common/social_classes/`** — stratification models referenced by country definitions and laws.

## Institutions

**`common/institutions/`**

```
institution_home_affairs = {
    icon = "gfx/interface/icons/institution_icons/home_affairs.dds"
    background_texture = "gfx/interface/illustrations/institutions/home_affairs.dds"
    modifier = {
        country_revolution_progress_mult = -0.1
    }
}
```

- Level bounds come from the defines `MIN_INSTITUTION_INVESTMENT` / `MAX_INSTITUTION_INVESTMENT`.
- Maximum level can be raised by the modifier `country_<institution>_investment_add`, which must be declared in `common/modifier_type_definitions`.
- Change speed: defines `DAILY_INSTITUTION_SIZE_CHANGE`, modifiers `country_institution_size_change_speed_mult` and `country_institution_size_change_speed_<name>_mult`.
- Bureaucracy cost scales with `STATE_BUREAUCRACY_POP_MULTIPLE`, floored by `MINIMUM_INVESTMENT_COST`; modifiers `country_bureaucracy_investment_cost_factor_mult` and `country_institution_cost_<name>_mult`.

## Decrees

**`common/decrees/`**

```
decree_promote_social_mobility = {
    texture = "gfx/interface/icons/decree/decree_promote_social_mobility.dds"
    modifier = {
        state_education_access_add = 0.25
        state_pop_qualifications_mult = 0.25
    }
    cost = 100                    # authority
    ai_weight = { value = 0 }     # state scope
}
```

Optional: `unlocking_technologies`, `unlocking_laws`, `country_trigger`, `state_trigger`. Cost is scaled by `country_decree_cost_mult` and floored by `MIN_DECREE_COST`. Script name generates `<name>` and `<name>_desc` localisation keys.

## Power Blocs

**`common/power_bloc_identities/`**, **`common/power_bloc_principles/`**, **`common/power_bloc_principle_groups/`**, **`common/power_bloc_names/`**. Identities define cohesion, mandate progress, and bloc-wide modifiers.

DLC gating is mandatory when replicating DLC content: wrap the feature in `has_dlc_feature = power_bloc_features` (Sphere of Influence) or the specific expansion key. New identities and principles that do not replicate DLC content need no gate.

## Diplomacy

- **`common/diplomatic_actions/`** — one file per action; defines availability, AI acceptance, and effects.
- **`common/diplomatic_plays/`** — play types, wargoal availability, and escalation.
- **`common/war_goal_types/`** — wargoals usable in plays; `common/subject_types/` defines overlord/subject relationships.
- **`common/treaty_articles/`**, `common/diplomatic_catalysts/`, `common/diplomatic_catalyst_categories/`, `common/proposal_types/` — treaty framework and relations modifiers.
- Secret goals set from AI or effects: `antagonize`, `befriend`, `conquer`, `dominate`, `none`, `protect` via `set_secret_goal` / `set_mutual_secret_goal`.

## Political Movements

**`common/political_movements/`**, plus `common/political_movement_categories/` and `common/political_movement_pop_support/`.

```
movement_example = {
    category = <category_key>
    ideology = <ideology_key>
    character_ideologies = { }
    creation_trigger = { }        # country scope
    creation_weight = { value = 100 }
    on_created = { }              # political movement scope
    culture_selection_trigger = { }   # root = culture, scope:country
    culture_selection_weight = { }
    religion_selection_trigger = { }
    religion_selection_weight = { }
}
```

## Lobbies, Amendments, Companies

- **`common/political_lobbies/`** + `common/political_lobby_appeasement` — foreign-policy lobbies and their appeasement reasons/factors.
- **`common/amendments/`** — law amendments; repeal handled by `on_amendment_repealed`.
- **`common/company_types/`**, `common/company_charter_types/`, `common/dynamic_company_names/` — companies, charters, and generation rules.

## AI

**`common/ai_strategies/`** holds strategy definitions. Key blocks:

- `possible` (per strategy, defaults to `always = no`), `weight` (default 0), `icon`.
- Budget/law behaviour: `desired_tax_level`, `min_tax_level`, `max_tax_level`, `change_law_chance`, `min_law_chance_to_pass`, `max_progressiveness`, `max_regressiveness`, `revolution_aversion`.
- Interest groups: `pro_interest_groups`, `anti_interest_groups`, `pro_movements`, `anti_movements`.
- Diplomacy: `diplomatic_play_support`, `wargoal_scores`, `wargoal_weights`, `secret_goals`, `treaties`, `obligation_value`, `ideological_opinion_effect_mult`, `nationalization_desire`.
- Economy: `building_blocks`, `building_group_weights`, `subsidies`, `wanted` blocks, `goods` blocks.
- Military: `military_blocks`, `combat_unit_groups`.
- Geography: `strategic_region_scores`, `colonial_interest_ratio`.
- Power blocs: `will_form_power_bloc`.

`ai_strategy_default` in `00_default_strategy` supplies the fallback values; `INJECT:` into it (or into another strategy) to change one block without restating the whole strategy.

`common/ai_goals/` and `common/ai_strategies/` are debugged with the console: `ai.debug <tag>`, `ai.goal <tag> <goal>`, and the `ai_evaluate_*` family.

## Cross-Cutting Rules

- Every scripted key must also have localisation: laws, decrees, institutions, IG traits, and movements all derive keys from the script name.
- Modifier keys must exist in `common/modifier_type_definitions`, otherwise the game ignores them silently.
- Anything gated by DLC must be wrapped in `has_dlc_feature = ...`; mods cannot unlock DLC.
- Referencing a law requires `law_type:<key>`; referencing an enacted law uses `has_law_or_variant` when variants matter.
- `INJECT:` cannot enter sub-blocks: a law's `is_visible`, an IG's `enable`, and an AI strategy's nested blocks can only be added when absent, or replaced wholesale.