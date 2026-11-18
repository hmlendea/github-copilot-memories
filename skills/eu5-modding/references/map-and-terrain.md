# Map Data, Map Editor, Terrain, Rivers, and Map Objects

EU5's map is moddable either through the official map editor or direct file editing. **Image format deviations (RGB vs grayscale, wrong bit depth, extra layers, alpha channels) crash the game or the map editor.**

## Map Files

Located in `in_game/map_data/` unless noted.

| File | Purpose |
|------|---------|
| `locations.png` | Location map; each unique colour code is one location |
| `named_locations/00_default.txt` | `location_key = hexcolour` mapping; every colour in `locations.png` must be defined exactly once |
| `definitions.txt` | Hierarchy: continent → subcontinent → region → area → province → locations |
| `location_templates.txt` | Per-location topography, vegetation, climate, religion, culture, raw material, harbour suitability |
| `ports.csv` | Port coordinates for coastal land locations (semicolon separator) |
| `adjacencies.csv` | Straits and other non-contiguous connections (semicolon separator) |
| `default.map` | Sea zones, lakes, wastelands (`impasable_mountains`), corridors (`non_ownable`), earthquake and volcano zones, `equator_y` |
| `rivers.png` | River definitions |
| Heightmap | Terrain heights (map editor required) |
| Terrain textures | Baked texture layers (map editor required) |
| `gfx/map/map_objects/` | Locators for cities, units, and other map objects |

## The Map Editor

Launch with `-map_editor`:
- Steam → right-click EU5 → Properties → General → Launch Options → add `-map_editor`.
- Requires high resources, notably **32 GB RAM or more**.

Use the map editor for heightmap and terrain textures. It is not required for the location map or rivers.

When saving:
- Every red alert must be cleared.
- An output folder must be selected for every section, even unused ones.
- Choose **userdir** baking so generated files land in `Documents/Paradox Interactive/Europa Universalis V/baked_streaming_data/` rather than the mod folder. Copy them into the mod manually.

## Location Map (`locations.png`)

Rules:
- Every colour used must be defined exactly once in `named_locations/00_default.txt`.
- Every location key must be unique.
- Never use soft brushes, partial opacity, or anti-aliasing; they create colour variants that are impossible to track and crash the game.
- Minimum viable map: 256 land locations, 5 provinces, 1 sea location, 1 port.

Definition syntax:
```
stockholm = dda910
```
Hex colour, case-insensitive.

## Hierarchy (`definitions.txt`)

```
europe = {
    western_europe = {
        scandinavian_region = {
            svealand_area = {
                uppland_province = { stockholm norrtalje enkoping uppsala kastelholm tierp heby }
            }
        }
    }
}
```

Do not put sea locations into an area whose members are all land: all locations in that area will report as seazone on hover.

## Location Attributes (`location_templates.txt`)

```
stockholm = {
    topography = flatland
    vegetation = grasslands
    climate = continental
    religion = catholic
    culture = swedish
    raw_material = clay
    natural_harbor_suitability = 0.75
}
```
Base-game files write each location as one line; expanded form is valid.

- Religion and culture here are placeholders only; the actual starting pop culture/religion come from `setup/start/06_pops.txt`.
- If a location has no pop definition in `06_pops.txt`, the engine repopulates it with a single pop of the declared culture/religion.
- Removing religion/culture from `location_templates.txt` prevents that repopulation and allows genuinely uninhabited locations.
- Wastelands and corridors only take topography, vegetation, climate.
- Lakes and seas only take topography and climate.

## Ports (`ports.csv`)

Semicolon-separated, coastal land locations only:
```
<land_location_key>;<adjacent_sea_location_key>;<x>;<y>;x
```
- The coordinates must land on a pixel of the adjacent sea location, immediately touching the land location (not diagonal).
- Image editors measure `y` from the top; the game measures from the bottom: `EU5 y = WORLD_EXTENTS_Z - editor y`.
- Every coastal sea location must have at least one port.

## Adjacencies (`adjacencies.csv`)

Semicolon-separated, nine fields:
```
From;To;Type;Through;start_x;start_y;stop_x;stop_y;Comment
viborg;thisted;sea;limfjorden;8096;6745;8093;6748;Limfjord strait
```
- `From` / `To` are connected locations.
- `Type` is the adjacency type (`sea` is the only base-game example).
- `Through` is the location the edge crosses; `sea` adjacencies can be blockaded through it.
- Coordinates are pixel positions on `locations.png`.

## Sea Zones, Wastelands, Corridors (`default.map`)

`default.map` declares:
- `sea_zones` / lakes
- `impasable_mountains` (impassable deserts and forests also live here)
- `non_ownable` corridors
- `earthquake` and `volcano` zones
- `equator_y`

## Rivers (`rivers.png`)

Rivers are painted as a dedicated image layer; the engine places them onto the map itself. No text file needed for base placement.

## Map Objects and Locators

`gfx/map/map_objects/` holds locators that place city models, unit positions, and other graphical objects per location. Editing the map without updating locators produces `Map Objects locator` errors in `error.log`.

Locator workflows:
1. Create or edit the locator definition.
2. Place it in the map editor or by writing the coordinates.
3. Verify in `error.log` that no locator mismatch is reported.

## Heightmap, Terrain, Decals

- The heightmap is required for terrain relief and requires the map editor.
- Terrain textures combine topography, vegetation, climate, and mask files.
- Decals are placed in the map editor and baked to `baked_streaming_data/`.
- Base-game decals include the main heightmap and mountain decals; keep names consistent if replacing.

## Splines and Map Border Models

- Regenerating splines is required after major landmass edits; the map editor handles this.
- Map border models sit on region/area boundaries; a wrong mask or missing asset yields invisible or misaligned borders.

## Map Object Masks

To add a map object mask:
1. Create the mask texture.
2. Create the `.asset` file.
3. Create the placement mask.
4. Add the generator entry.

## Map Mode Modding

Map mode definitions live in `gfx/map/map_modes/`. Map modes are largely **hardcoded** and the wiki page is absent. Fields such as `pinned_by_default` have been observed to error (`Malformed token: yes`); keep `category` and `index` and let the UI handle pin state. Verify against the installed schema before writing any map mode fields.

## Practical Warnings

- Sea locations must average noticeably larger than coastal land locations, or ports become impossible to place.
- Province keys are used for colonial claims, development scoping, and wargoal targeting; keep them stable once published.
- Location keys are the primary script identifier for everything location-scoped; renaming breaks setups, actions, and script values.
- After any map change, run `-debug_mode`, inspect `error.log`, and verify locators, ports, adjacencies, and the location count minimums.