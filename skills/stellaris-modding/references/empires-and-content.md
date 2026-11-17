# Empires, Species, Leaders, Ships, Starbases, War, Espionage

## Government and Empire Definition Chain

| Definition | Folder | Type | Used by |
|-----------|--------|------|---------|
| `ethics` | `common/ethics/` | LIOS | Ethics and ethic attraction |
| `authorities` | `common/governments/authorities/` | FIOS | Authority (democratic, imperial, hive, machine) |
| `civics` / `origins` | `common/governments/civics/` | LIOS | Empire traits; origins are civics with `is_origin` |
| `governments` | `common/governments/` | LIOS | Government forms, ruler titles, election weights |
| `country_types` | `common/country_types/` | LIOS | Empire rules, enclaves, crises |
| `traits` | `common/traits/` | DUPL/FIOS | Species and leader traits; whole-file override only |
| `species_classes`, `species_archetypes` | `common/species_classes/`, `common/species_archetypes/` | LIOS | Species class graphics and archetypes |
| `species_names`, `name_lists` | `common/species_names/`, `common/name_lists/` | MERGE/DUPL, DUPL | Random name pools |
| `personalities` | `common/personalities/` | LIOS | AI personality archetypes |
| `attitudes` | `common/attitudes/` | LIOS | AI attitudes toward other empires |

A new empire-facing gameplay element generally touches at least four files: the `common/` definition, a localisation pair, an icon in `gfx/interface/icons/`, and a `.gfx` sprite entry when the icon is referenced by name.

## Prescripted Empires

`prescripted_countries/*.txt`. These populate the empire-selection list; file order is list order.

```
my_empire = {
    name = "my_empire"
    adjective = "PRESCRIPTED_adjective_my_empire"
    spawn_enabled = yes                  # yes / no / always

    ship_prefix = "PRESCRIPTED_ship_prefix_my_empire"

    species = {
        class = "REP"
        portrait = "rep9"
        name = "PRESCRIPTED_species_name_my_empire"
        plural = "PRESCRIPTED_species_plural_my_empire"
        adjective = "PRESCRIPTED_species_adjective_my_empire"
        name_list = "REP1"
        trait = "trait_strong"
        trait = "trait_nonadaptive"
    }

    room = "personality_slaving_despots_room"
    authority = "auth_imperial"
    civics = { "civic_police_state" "civic_slaver_guilds" }
    government = gov_star_empire
    ethic = "ethic_authoritarian"
    ethic = "ethic_fanatic_militarist"

    planet_name = "PRESCRIPTED_planet_name_my_empire"
    planet_class = "pc_desert"
    system_name = "PRESCRIPTED_system_name_my_empire"

    graphical_culture = "reptilian_01"
    city_graphical_culture = "reptilian_01"

    empire_flag = {
        icon = { category = "pointy" file = "flag_pointy_2.dds" }
        background = { category = "backgrounds" file = "v.dds" }
        colors = { "red" "black" "null" "null" }
    }

    ruler = {
        name = "PRESCRIPTED_ruler_name_my_empire"
        gender = male
        portrait = "rep9"
        texture = 1
        clothes = 4
    }
}
```

`spawn_enabled = always` forces presence; `no` hides from random generation but keeps it selectable.

## Ethics, Civics, and Origins

Civics and origins share one definition folder. An origin declares `is_origin = yes`, is limited to one per empire, and usually gates its effects through `potential` (which ethic/authority combinations may take it) plus `modifier` for the passive effect.

Ethics changes carry a warning: multiple vanilla ethics files mean partial overrides can break random empire generation, so replacing the ethics file wholesale is the reliable path.

## Leaders

`common/leader_classes/*.txt` (LIOS) define **shell classes**; the six hardcoded classes (Ruler, Governor, Scientist, Admiral, General, Envoy) cannot be added to or removed.

```
leader_class_my_class = {
    max_trait_points = 1
    default_category = scientist
    can_research = yes
    can_govern_planet = yes
    can_lead_navy = no
    can_lead_army = no
    can_rule_empire = no
    can_be_envoy = no
    resources = { category = leaders cost = { energy = 100 } upkeep = { energy = 2 } }
}
```

Adding shell classes is pointless — the engine never generates them by name. Modifying trait points and assigning cross-category permissions are the realistic edits.

Leader traits are grouped per class in `common/traits/`; a leader that changes class adopts that class's trait set.

## Ships

A ship is assembled from four layers:
1. `ship_size` — `common/ship_sizes/` (LIOS)
2. `section_template` — `common/section_templates/` (DUPL/FIOS)
3. `component_template` + `component_slot_template` + `component_sets` — `common/`
4. `ship_design` — designed in-game or defined as `global_ship_designs` (FIOS)

`ship_size` essentials: `graphical_culture` list, `entity`, `max_hitpoints`, `max_speed`, `acceleration`, `rotation_speed`, `collision_radius`, `size_multiplier` (command points and build-window placement), `combat_size_multiplier`, `fleet_slot_size`, `formation_priority`, `modifier` (a restricted allow-list of hull/armour/shield/weapon/upkeep modifiers), `ship_modifier` (fire-rate and range style modifiers), plus the role flags `is_civilian`, `is_space_station`, `valid_target_aggressive_stance`, `build_block_radius`.

Graphics naming is contractual:
- Core entity: `<gfx_culture>_<ship_size>_entity`, holding `part1`, `part2`, … locators matching the `ship_size` slot names.
- Section entity: `<gfx_culture>_<entity declared in section_template>_entity`, attached to the slot locator.
- Weapon entity: `<gfx_culture>_<entity from component_template>_entity`, with a `turret_muzzle_01` locator (name defined by `NGraphics::SHIP_TURRET_PROJECTILE_SPAWN_LOCATOR`).

Components are restricted by `slot_type` — weapons only fit weapon slots, utilities only utility slots.

`countries_limits/` (LIOS) caps ships per country type through `ship_of_size_limits` and `ownership_limits`; a new limit definition has no effect unless a `country_type` invokes it.

## Starbases

- `common/starbase_levels/` (LIOS): `ship_size`, `next_level`, `level_weight`, `show_in_outliner`, `display_map_icon`, `display_empire_shield`, `potential_home_base`, `ai_weight`.
- `common/starbase_modules/` (LIOS): `icon` (a GFX key, not a path), `section` (a section template attached to the starbase hull), `construction_days`, `potential`, `possible`, `initial` (granted to every empire's first starbase), plus an economy unit and modifiers.
- `common/starbase_buildings/` (LIOS): same shape as modules, for buildings.

## Armies

`common/armies/*.txt` (LIOS).

```
assault_army = {
    damage = 1.00
    health = 1.00
    morale = 1.00
    morale_damage = 1.00
    collateral_damage = 1.00
    war_exhaustion = 1.00
    time = 90
    icon_frame = 2
    prerequisites = { "tech_assault_armies" }
    resources = { category = armies cost = { minerals = 100 } upkeep = { energy = 1 } }
    potential = { ... }
    allow = { ... }
}
```

Final values are multiplied: damage `1.5–3.0 × damage`, health `200 × health`, morale `200 × morale`, morale damage `1.5–3.0 × damage × morale_damage`.

Flags: `has_species` (counts toward the assault-army/pop clause), `pop_limited` (exempt from that clause), `defensive` (cannot be transported), `is_pop_spawned` (spawned by jobs, never built), `occupation` (spawned on captured planets), `rebel`.

`icon_frame` indexes the shared `gfx/interface/planetview/army_icon.dds` spritesheet.

## War

- `common/casus_belli/` (LIOS): `show_in_diplomacy`, `show_notification`, `aggregated_message_key`, `potential` (`ROOT` = owner, `FROM` = target), `is_valid` (re-evaluated daily for automatic grants), `destroy_if`.
- `common/war_goals/` (LIOS): war-goal definitions, surrender/pressure conditions, and AI weights.

Both need localisation keys and, where shown, icons registered in a `.gfx` file.

## Diplomacy and Subjects

- `common/diplomatic_actions/`, `common/diplomatic_economy/` (LIOS): action conditions and costs.
- `common/agreement_presets/`, `agreement_terms/`, `agreement_resources/`, `agreement_term_values/` (LIOS, 3.4+): subject agreement types and negotiable terms.
- `common/federation_types/`, `federation_laws/`, `federation_perks/`, `federation_law_categories/` (LIOS).
- `common/opinion_modifiers/`, `common/diplo_phrases/` (DUPL/LIOS).

## Espionage

- `common/espionage_operation_types/` and `espionage_operation_categories/` (LIOS): operation definitions; some fields require whole-file replacement.
- `common/espionage_assets/` (LIOS): asset definitions, whole-file override only.
- `common/ai_espionage/` with `operations/` and `spynetworks/` (LIOS), with an initialisation-order dependency between them.

## Ascension Perks, Traditions, Technologies

- `common/ascension_perks/`, `ascension_perk_categories/`: LIOS. Categories drive which UI tab a perk appears in.
- `common/traditions/` and `tradition_categories/`: LIOS. Adoption and finisher effects are separate entries; effect tooltips are authored independently of the effects.
- `common/technology/` (nested under `technology/` with `tier/`): LIOS*, with the quirk that a replacement omitting `potential` inherits the original's `potential`. Textures live in `gfx/interface/icons/technologies/`.

## Relics, Artifacts, Archaeological Sites

- `common/relics/` (LIOS): `activation_duration`, `portrait` (a GFX key declared in `interface/relics_view.gfx`), `sound`, `resources`, `triggered_country_modifier` (passive effect), `active_effect`, `possible`, `score`, `ai_weight`.
- `common/artifact_actions/` (LIOS): minor-artifact actions and their effects.
- `common/archaeological_site_types/` (LIOS): dig sites, stages, and rewards.

## Agendas, Banners, Bombardment

- `common/council_agendas/` (LIOS, renamed in 3.7): agenda definitions and weights; graphics are sprite entries with a defined name pattern.
- `common/bombardment_stances/` (LIOS): stance conditions, damage multipliers, and animation keys.
- `common/bypass/` (LIOS): gateway, wormhole, and L-gate types. Placing a bypass requires both the definition and a spawn path (megastructure or `solar_system_initializers`).

## AI Customisation

- `common/ai_budget/`, `common/economic_plans/` (LIOS): how AI splits income.
- `common/personalities/` (LIOS): behaviour mix, aggression, and modifier block.
- `ai_weight` blocks on any definition with `modifier`/`weight`/`factor` shape: used whenever the AI has no overriding economic plan.
- `hidden_trigger` inside `allow` gives the AI extra constraints beyond the player-facing rule.

## Assets and Presentation

- Flags: `flags/*.dds` plus `flags/colors.txt` for palette and randomisation; emblems need a category and mask.
- Portraits: `gfx/models/portraits` meshes plus `gfx/portraits/portraits/*.txt` assignment and `portrait_sets` grouping.
- Music: `music/*.ogg` with `songs.asset` (track listing and volume) and optional `songs.txt` overrides.
- Sound: `sound/*.wav` with an `.asset` definition.
- Fonts: `fonts/fonts.asset` plus bitmaps in `gfx/fonts/`.

Asset replacement (flags, portraits, shipsets, music, fonts) is the least risky category for achievement compatibility, but no mod that changes checksum-relevant content can guarantee it.