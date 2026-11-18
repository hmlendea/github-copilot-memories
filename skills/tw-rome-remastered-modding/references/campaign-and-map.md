# Campaign Data, History Setup, and the Map

## Campaign Files

`data/world/maps/campaign/<campaign>/` holds one folder per campaign. The folder name must match `folder` in `data/descr_campaigns.txt` and the `terrain/campaign/<campaign>/` folder.

| File | Role |
|------|------|
| `descr_strat.txt` | Everything the campaign starts with: factions, settlements, armies, resources, diplomacy, script hook |
| `descr_win_conditions.txt` | Per-faction victory and defeat conditions |
| `descr_mercenaries.txt` | Mercenary pools by region |
| `descr_events.txt` | Scripted historic events; may be blank **with a comment line** |
| `descr_disasters.txt` | Disaster schedule; may be blank with a comment line |
| `map.rwm` | Compiled map; regenerate rather than hand-edit |
| `feral_radar_map.tga` / `_winter` | 1024×624 minimap |
| `feral_map.tga.dds` | Large 2D overview map |
| `description.txt`, `leader_pic_*` | Campaign description and leader art |
| `<campaign>_script.txt` | Background script, named in `descr_strat.txt` |

`data/world/maps/base/` holds the functional map shared by campaigns; copy its files into a campaign folder when a campaign needs its own map.

## `descr_strat.txt`

Section order is fixed and the parser is positional. The blocks are `factions`/`playable`, `unlockable`, `nonplayable`, `start_date`/`end_date`, per-faction blocks with `settlement` and `character` entries, `diplomacy`/`core_attitudes`, `resource` lists, and the trailing script reference.

Two Remastered-specific requirements:

1. **Every character name must exist for that faction in `descr_names.txt` and `data/text/names.txt`.** An unknown name is a crash to desktop, not a log warning.
2. **Resources carry a quantity** before the coordinates: `resource marble, 1, 56, 62`. The shipped "remastered" file uses the four-field form and the original-rules variant lives in `original_overrides/`.

Also accepted: `set_major_event_enabled <event>, false`, `trigger_status <event>, [faction,] true|false`, per-faction `religion` overrides in a settlement block, faction aggression, and super-faction options.

AI personalities must be written with underscores (`comfortable_caesar`); see `references/buildings-and-factions.md`.

## `descr_win_conditions.txt`

`hold_regions`, `take_regions`, `outlive`, and the faction-specific lines. Two traps:

- `hold_regions` takes **settlement** names, not region names.
- Alexander's victory condition is `alexander_lives`, which replaced `alexander`.

## `descr_regions.txt`

Positional, one block per region:

```
Illyria
	Epidamnus
	germans
	Gepids
	232 41 55
	none
	5
	3
	hellenism 10 paganism 90
```

Order: region name, settlement name, faction owner, rebel faction, RGB colour matching `map_regions.tga`, resource list (`none` or comma-separated including hidden resources), city tier, farm level, then religion commitments in `<name> <percent>` pairs.

The trailing religion line is fragile: the parser treats an unrecognised token as the start of the next settlement block, so a missing line produces `settlement '' not found in stringtable` for everything after it.

## Functional Map Files

In `data/world/maps/base/`:

| File | Size | Note |
|------|------|------|
| `map_regions.tga` | base size | Sets the size of everything else; 510 px original limit lifted, 1020 px proven working |
| `map_heights.tga` | 2 × regions + 1 | Playable land, sea, and battle-map heights |
| `map_ground_types.tga` | 2 × regions + 1 | Ground types for battle maps and pathing |
| `map_climates.tga` | 2 × regions + 1 | Climate for battle maps |
| `map_features.tga` | regions size | Rivers and cliffs; also bends region borders |
| `map_roughness.tga` | 2 × regions | Required, unused |
| `map_trade_routes.tga` | regions size | Required, vestigial — no AI or pathing reads the flag |
| `map_heights.hgt` | — | Optional finer detail; if the map matches vanilla size, ship one or delete the vanilla file |
| `map_FE.tga` | variable | Feature edges |
| `water_surface.tga` | 256×256 | Unused in Remastered |
| `descr_terrain.txt` | — | Must declare the `map_regions.tga` width and height |
| `descr_regions.txt` | — | Region and settlement database |
| `descr_disasters.txt` | — | Can be blank with comments only |

`map.rwm` is generated when missing. Deleting it is the normal way to force a rebuild after map edits.

Beyond about 510 px the practical ceiling is memory, not a constant; coordinate values in `descr_quick_battle_locations.txt` map 1:1 to `map_regions.tga` pixels.

## Two-Map Model

The **functional** map still comes from the TGAs and text files, and still controls settlement and port coordinates, region borders, land/sea classification, feature positions, and the heights, ground types, and climates used to build battle maps.

The **visible** campaign map is authored geometry, entirely separate:

| Component | Location |
|-----------|----------|
| Map mesh pieces | `.cas` files listed in `terrain/campaign/<campaign>/descr_map_tiles.txt` |
| Coastline | `coastline/coastline.cas`, listed in `descr_map_coastlines.txt` |
| Rivers | `river_mesh.cas` (hard-coded name and location) |
| 3D frame | `frame/` with `.cas` and textures named inside the model |
| Heightmap bins | `heightmap/*.bin`, one per mesh piece, 40,401 floats each |
| Tile textures | Referenced per piece from `descr_map_tiles.txt` |

Consequences:

- Editing the TGAs alone leaves the old mesh on screen; a mismatch shows sea where the functional map has land.
- Heightmap `.bin` files are generated from the mesh on first load when the requested names do not exist. Provide an empty `heightmap/` folder in the mod, or the bins are written into the game installation.
- All mesh pieces must be rectangular and identical in size for the bins to line up.
- Bridge heights come from `map_heights.tga`/`.hgt`, **not** from the mesh, so a mismatched mesh misplaces bridges.
- A non-matched mesh that is too much larger than the functional land area can crash on load with no message.
- Rivers cannot be aligned with region borders; the border follows `map_features.tga`, and `descr_aerial_map_tile_models.txt` can be adjusted to prefer straight sections.
- Textures are `.dds` with optional mip-maps; the graphics quality setting decides which mip level the game starts at, so a 2048² texture on Low shows only the 256² level.

Authoring routes: Feral's Blender-based campaign map tool (mesh sectioning and conversion), or IWTE, which generates mesh pieces and textures from the `map_*.tga` files (Beta).

## Radar and 2D Overview

`feral_radar_map.tga` and `feral_radar_map_winter.tga` are 1024×624. `feral_map.tga.dds` is the base image under the scrolling 2D view; the overlays (borders, ownership, trade) are drawn by the engine from the functional map. A radar `.pvr` also exists and needs PVRTexTool or comparable to open.

## Campaign Triggers and Events

`descr_events.txt` can additionally fire earthquakes, storms, floods, and riots with explicit coordinates and severity, plus `emergent_faction` at a named region, and can set visibility to `everyone`, `visible`, `harmed`, or `hidden`.

`descr_disasters.txt` fires within 75–125% of the configured year, warns one turn ahead (volcano only), and the engine caps severity: earthquake, flood, and volcano at 9, storm at 13.

## Scripted Camera and Movies

`move_to_settlement`, `snap_to_settlement`, `point_at_agent_hub`, and `set_strat_camera_speed` drive the camera from script. `movie_cam` and the historical-battle replay system are launch modes, not data.

## Pathfinding Reference

Campaign pathfinding reads `map_heights.tga`, `map_ground_types.tga`, and `map.rwm`, and is covered in `documentation/feature_guides/Campaign_Map_Pathfinding.md`. Movement costs change with ground type and with `feral_descr_movement_multipliers.txt` when `type_specific_movement_point_modifiers` is enabled; that file is the only way to make light infantry faster than heavy infantry.

Roads, not `map_trade_routes.tga`, drive AI trade behaviour.