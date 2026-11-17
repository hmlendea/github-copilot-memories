# Map, Galaxy Setup, and Defines

## Map Surface

| Need | Location |
|------|----------|
| Galaxy sizes and generation parameters | `map/setup_scenarios/*.txt` |
| Galaxy shapes | `map/galaxy/galaxy_shapes.txt` |
| Random name pools | `common/random_names/base/00_random_names.txt` |
| Predefined/unique systems, colonies, fleets, spawn weights | `common/solar_system_initializers/*.txt` (FIOS) |
| Prescripted empires | `prescripted_countries/*.txt` |
| Engine-level tunables | `common/defines/*.txt` |

## Galaxy Size (Setup Scenario)

Copy a vanilla file from `map/setup_scenarios/` into the mod at the same relative path, rename it unless replacing the original, and edit.

```
setup_scenario = {
    name = "my_huge"
    priority = 4
    num_stars = 1000
    radius = 450                        # hard cap 500; stay under ~460
    num_empires = { min = 0 max = 30 }
    num_empire_default = 15
    fallen_empire_default = 4
    fallen_empire_max = 5               # cannot exceed 5 in vanilla
    marauder_empire_default = 3
    marauder_empire_max = 3
    advanced_empire_default = 4
    colonizable_planet_odds = 1.0
    primitive_odds = 1.0
    crisis_strength = 1.5
    extra_crisis_strength = { 10 25 }

    cluster_count = { method = one_every_x_empire value = 1 max = 6 }
    cluster_radius = 150
    cluster_distance_from_core = 300
    max_hyperlane_distance = 50

    home_system_partitions = { max_systems = 15 min_systems = 8 min_bridges = 2 max_bridges = 4 method = breadth_first }
    open_space_partitions  = { max_systems = 10 min_systems = 4 min_bridges = 2 max_bridges = 4 method = depth_first }

    num_nebulas = 10
    nebula_size = 60
    nebula_min_dist = 200
    num_wormhole_pairs = { min = 0 max = 5 }
    num_wormhole_pairs_default = 1
    num_gateways = { min = 0 max = 5 }
    num_gateways_default = 1
    num_hyperlanes = { min = 0.5 max = 3 }
    num_hyperlanes_default = 1

    supports_shape = elliptical
    supports_shape = spiral_2
    supports_shape = spiral_4
    supports_shape = ring
    supports_shape = starburst
}
```

`supports_shape` is mandatory: a scenario without a matching shape is never selectable. Shape names come from `map/galaxy/galaxy_shapes.txt`.

Costs of scale: above roughly 1000 stars, generation time and turn latency degrade noticeably.

## Galaxy Shapes

`map/galaxy/galaxy_shapes.txt`. The file's own comments are the authoritative documentation; only a few parameters are exposed, and the core glow (`gfx/FX/galaxy_center.shader`, `gfx/map`) washes out stars placed near the centre.

## Static Galaxies

`static_galaxy_scenario` in `map/setup_scenarios/`. This replaces procedural generation entirely, so **you must define nearly everything**:
- Every system: `id`, `position` (`x`, `y`, optional `z`; ranges may be `{ min = … max = … }`), `initializer`, optional `name` and `spawn_weight`.
- Every hyperlane: `add_hyperlane = { from = "1" to = "2" }` when `random_hyperlanes = no`.
- Nebulae, gateways, wormhole pairs.

```
static_galaxy_scenario = {
    name = "MyGalaxy"
    priority = 10
    radius = 500
    num_empires = { min = 10 max = 30 }
    fallen_empire_max = 4
    random_hyperlanes = no
    core_radius = 0

    system = { id = "0" position = { x = 148 y = 121 } initializer = my_initializer_1 }
    system = { id = "1" position = { x = 148 y = 121 } initializer = my_initializer_1
               spawn_weight = { base = 0 modifier = { add = 10 has_country_flag = my_flag } } }
    system = { id = "2" position = { x = { min = 150 max = 200 } y = 121 } }
    system = { id = "3" position = { x = 148 y = 121 z = 3 } }

    add_hyperlane = { from = "0" to = "3" }
    add_hyperlane = { from = "1" to = "0" }

    nebula = { name = "Nebula" position = { x = 0 y = 0 } radius = 10 }
}
```

Known breakage in static galaxies: fallen empires may not spawn, precursors may not work, most origins and starting systems misbehave, some events break, and endgame crises may not trigger. Home-world climate in the initializer must match the generated planet, or pops spawn unhappy. State these limitations before promising a static-map mod.

## Solar System Initializers

`common/solar_system_initializers/*.txt` (FIOS). One entry per predefined or spawnable system: star class, planet orbits, planet classes, deposits, anomalies, and optional pre-placed countries, colonies, fleets, and megastructures.

Because the folder is FIOS, overriding a vanilla initializer requires a filename that sorts before it, e.g. `!!my_overrides.txt`.

## Random Names

`common/random_names/base/` and `common/species_names/` (**DUPL** / **MERGE**). Pools for ship, fleet, army, planet, and leader names. Files must be UTF-8 with BOM.

## Defines

Defines are engine-level constants, static and global, in:
`common/defines/00_defines.txt` (2000+ entries), `00_defines_additional_content.txt`, and `unchecked_defines/00_interface.txt`.

Override procedure:
1. Create `common/defines/` in the mod.
2. Copy `00_defines.txt` from the installation into it.
3. **Rename** the copy (e.g. `my_mod_defines.txt`). Leaving the name as `00_defines.txt` crashes the game.
4. Delete everything you do not change, then keep only the block and key lines you need.

```
NGameplay = {
    LEADER_POOL_SIZE = 4
    LEADER_POOL_LEAD_TIME = 5
    TECH_COST_MULT_NUM_POPS = 0.001
}

NSpecies = {
    MAX_ETHIC_POINTS = 5
    MAX_TRAIT_POINTS = 2
}
```

Rules:
- The block name must be included with every key; a bare `KEY = value` at file top level is ignored.
- `defines` is LIOS: a later file wins per key, so partial overrides are safe.
- Comments (`#`) are allowed.
- Some values are read only at startup; changing others at runtime has no effect until restart.

## Console Aids for Map Work

| Command | Use |
|---------|-----|
| `observe` | Run the simulation without playing an empire; reveal hidden traits and religions |
| `planet_size`, `survey`, `own` | Manipulate the current system while testing generation |
| `create_megastructure <key>` | Spawn a megastructure in the current system (orbital rings do not spawn correctly) |

## Validation Checklist

1. Every `supports_shape` name exists in `galaxy_shapes.txt`.
2. `radius ≤ 500`; star counts realistic for target hardware.
3. Static galaxies define hyperlanes for every connection when `random_hyperlanes = no`.
4. Every initializer referenced from a scenario exists and is FIOS-safe.
5. Defines file renamed, wrapped in its block, and limited to changed keys.
6. New game started from a clean save; compare `error.log` before and after.