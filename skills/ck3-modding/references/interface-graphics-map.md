# Interface, Graphics, and Map

## GUI Files

CK3's interface is built from `.gui` files in `gui/`. They are similar to HTML, edited with any text editor, and hot-reloaded with `-debug_mode -develop` plus `-mapeditor` for map work.

Textures: `.dds`, also `.png` in many places, inside `gfx/`. DDS authoring: Photoshop with the Intel plugin, or GIMP with the DDS plugin.

### Inspecting the Live UI

1. Set `pdx_settings.txt` (in the CK3 user directory) to point at the editor: search for `editor`, set its value to the `.exe` path, and set `editor_postfix` to `:$ -rg` for VS Code (or `:$:1` for Pulsar and Notepad++).
2. Run `tweak gui.debug` (tweaker menu → check `gui.debug`) to highlight elements under the cursor and reveal exact file and line.
3. Run `gui_editor` (Ctrl+F8) for the built-in GUI editor; it is limited but can edit in place.
4. `dump_data_types` generates `data_types*.log` into `logs/data_types/`. Merge for searching with `type *.txt > ALL_DATA_TYPES.txt` (Windows); use `data_types_explorer` in-game to browse.
5. `release_mode` toggles the Errorhoof error counter and is the fastest feedback loop for a UI mistake.
6. Optional hot reload for `.gui` (not usually needed): `reload gui` or `reload gui/frontend_main.gui`, and for textures `reload texture all` or `reload texture flatmap.dds`.

### Editing Rules

- To edit a vanilla window, copy the exact `.gui` file into the mod and edit it there; windows are whole-file replaced.
- Types and templates follow FIOS: first loaded wins, so name the file earlier in ASCIIbetical order, e.g. `00_my_buttons.gui`. Replace a type by first declaring a group with any name, then the type inside it; declare a template with no group wrapper.

```
types SmallButton {
  type button_standard_small = button_standard
    {
        size = { 40 25 }
    }
}
```

- The in-game GUI editor exists but lacks functionality; use it for inspection and layout, not for authoring.
- New windows: spawn them as a scripted widget, or open them from a decision, event or interaction. A new HUD button in a shared vanilla file conflicts with other UI mods — that is the documented difficulty with UI-mod compatibility.

### Known crash reasons

- Setting 100% size on hboxes/vboxes, or placing an hbox/vbox inside a flowcontainer.
- `resizeparent = yes` on multiple children of one parent, even if only one is visible.
- A type that references itself (endless loading until the machine runs out of RAM).
- Syntax errors: missing brackets or missing quotes. Count `{` against `}`; enable regex search for `= \[` / `\]\n` to find unquoted square brackets.

### Scripted GUIs

`common/scripted_guis/*.txt` holds hidden events invoked from the UI. See `references/scripting.md`. The canonical call uses bracket syntax in an `.gui` file:

```
onclick = "[GetScriptedGui('my_sgui').Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
```

`visible` / `enabled` / `tooltip` read `ScriptedGui.IsShown|IsValid|BuildTooltip` against the same scope expression.

### Data Types in Text

`[ROOT.Char.GetName]` and friends are how UI and text show live data. Promotes return scopes; functions return values. `GetPlayer.MakeScope`, `CharacterWindow.GetCharacter.MakeScope` and `HoldingView.GetProvince` are the standard starting scopes; `SetRoot(...)` and `AddScope('name', ...)` feed them into a script value or scripted GUI call.

## Coat of Arms

Vanilla CoAs are scripted in `common/coat_of_arms/coat_of_arms`. Emblem art lives in `gfx/coat_of_arms/`.

| Keyword | Purpose |
|---------|---------|
| `parent` | Inheritance, e.g. `parent = k_england` |
| `pattern` | Background pattern filename from `gfx/coat_of_arms/patterns/`; include a pattern when using textured emblems, to avoid masking artefacts |
| `color1` … `color5` | Pattern colours or references to `common/named_colors`. Formats: `"white"`, `hsv { 1.0 1.0 1.0 }`, `hsv360 { 360 50 50 }`, `rgb { 255 255 255 }`, `hex { aabbccdd }` |
| `textured_emblem` | One or more; keys `texture` (path under `gfx/coat_of_arms/textured_emblems/`), `mask = { a b }`, `instance = { scale = { x y } position = { x y } rotation = n depth = n }` |
| `colored_emblem` | One or more; same instance fields, plus `color1` (base), `color2` (green channel of the texture), `color3` (currently unavailable, renders white) |
| `sub` | Multiple complete CoA objects, each with all fields except nesting another `sub` |

### Dynamic CoAs

`common/coat_of_arms/dynamic_definitions/`. The top-level name must match a landed title. Items carry a `trigger` (root is the title) and a `coat_of_arms` reference; the first valid item is used.

```
title_name = {
	item = {
		trigger = { <trigger> }
		coat_of_arms = name
	}
}
```

Re-evaluate with `update_dynamic_coa = yes` in the title scope. Vanilla already calls it on `on_character_culture_change` and `on_character_faith_change`; wire any other circumstance to an on_action manually.

### Emblems in the Designer

- Emblem DDS must be "8.8.8.8 ARGB 32bpp / Unsigned", also known as "B8G8R8A8 (Linear, A8R8G8B8)". Mip maps are optional.
- Use exactly three colours: `0x000084` (blue) = colour 1, `0x00FF94` (light green) = colour 2, `0xFF0084` (magenta) = colour 3 (see `gfx/coat_of_arms/textured_emblems/`). The game matches deviating colours against those three imperfectly, so use the exact values.
- Declare each emblem in a UTF-8-BOM text file placed alongside the textures:

```
<pic_name>.dds = { colors = <1|2|3> category = <string> }
```

The text-file name must match the image file name exactly.
- Default categories: `animals`, `circles_spirals`, `crosses_and_knots`, `faiths`, `manmade`, `nature`, `patterns`, `tribal_seal`, `writing`, `figures`. Any other string creates a new selectable category, which needs localisation `COA_DESIGNER_CATEGORY_<category>:0 "<Name>"`.
- Setting `colors` higher than the number actually used leaves a dead option; setting it lower makes the extra colours collapse to one, or fall back to an unchangeable reddish-brown.

### Portrait palettes

`common/named_colors/` carries named colour sets used by the above; portrait palettes for DNA shading live under `gfx/portraits/`. See the Graphical assets and 3D models pages for the full palette and gene workflow.

## 3D Models

- The Clausewitz Maya exporter is the official path; the Exporters page documents Maya and Photoshop setup. Blender models are exported through the same pipeline.
- Prepare the model, apply textures in the channel layout the engine expects, and place the result under `gfx/models/` with the referencing `.entity`/`.mesh` entries.
- Holding-specific models are attached through the `asset` block of a building (see `references/common-definitions.md`).

## Graphical Assets

`gfx/` subfolders hold icons, illustrations, portraits, unit models and interface art. The Graphical assets page documents the portrait palettes and the conventions for reusing vanilla texture sets; icons referenced by script must exist at the path the consuming object documents (for example `gfx/interface/icons/traits/<trait>.dds`).

## Map Modding

The map editor opens with `-mapeditor` (or via the launcher).

### Heightmap

- `map_data/heightmap.png` is 16-bit greyscale: black is lowest, white highest.
- Dimensions must match `original_heightmap_size` in `map_data/heightmap.heightmap`.
- Also generated: `indirection_heightmap.png` and `packed_heightmap.png`. Regenerate them by repacking in the map editor after every heightmap change; "the terrain doesn't obey my heightmap" is almost always a missing repack.

### River map

- Defines coasts, rivers and river crossings for pathing. Not for navigation rules.
- Must be an indexed RGB image using only the vanilla palette. Any other colour, including antialiasing or transparency, crashes the game.
- Start from the vanilla `game/map_data/rivers.png`. If GIMP refuses the export, close GIMP, copy the vanilla river map into the mod, open it keeping the colour profile (Rendering Intent: Absolute colorimetric), then overwrite `rivers.png` on export.

### Province map

- Each barony and sea region is a unique colour; counties and above are defined in `common/landed_titles/`, not here.
- Save as 8-bit or 24-bit RGB. Anything else CTDs. 8-bit caps the map at 255 provinces/baronies because black is reserved.
- Never let an editor colour-reduce the image; it merges colours the game treats as distinct.

### Titles, baronies, holdings

1. Map colours to barony IDs in `map_data/definition.csv`:

```
[ID];[RED];[GREEN];[BLUE];[Barony Name];x;
2333;128;183;194;PARIS;x;
```

**IDs must be sequential, or the game crashes.**

2. Set each barony's holding, religion, culture and development in `history/provinces/<kingdom>.txt`. Holding types: `none`, `tribal_holding`, `castle_holding`, `city_holding`, `church_holding`. The first barony in a county becomes its castle and decides the county government type; the game fills omitted slots automatically in a fixed order, so define explicitly when the order matters.
3. Define the title hierarchy in `common/landed_titles/`:

```
e_empire_tier = {
	color = { 0 0 0 }
	capital = c_county_tier
	k_kingdom_tier = {
		color = { 0 0 0 }
		capital = c_county_tier
		d_duchy_tier = {
			color = { 0 0 0 }
			capital = c_county_tier
			c_county_tier = {
				color = { 0 0 0 }
				b_barony_tier = {
					color = { 0 0 0 }
					province = 1234
				}
			}
		}
	}
}
```

The first barony listed in a county is its capital and cannot be moved; culture and religion come from the capital barony's province history. Baronies cannot be titular, and counties cannot exist outside a duchy's scope, so the hierarchy must be complete.

4. Provide localisation (`<title>` and `<title>_adj`) and, if needed, cultural name lists.

### Terrain

- Per-province assignment: `common/province_terrain/00_province_terrain.txt` with one `[prov_id]=[terrain]` per line. Valid terrains: `plains`, `farmlands`, `hills`, `mountains`, `desert`, `desert_mountains`, `oasis`, `jungle`, `forest`, `taiga`, `wetlands`, `steppe`, `floodplains`, `drylands`. Changes take effect immediately.
- Terrain types themselves: `common/terrain_types/`, with `attacker_combat_effects` / `defender_combat_effects` referencing combat effects.

### Map locators

Locators position the building, raised army, combat and siege objects per barony:

- `gfx/map/map_object_data/` holds `building_locators.txt`, `combat_locators.txt`, `player_stack_locators.txt` and `siege_locators.txt`.
- Each barony is an `instances = { { id = n position = { x 0 y } rotation = { ... } scale = { 1 1 1 } } }` entry.
- Sea raised-army positions drive land/sea pathfinding; bad locators silently break movement.
- Fix invalid spawns in the Map Objects Editor, or the auto-nudge tool (dice button on the object placement mode) after selecting provinces. Invalid positions paint red stripes; re-nudge or drag the object manually.
- If the locators are broken, `error.log` reports that generated files exist under `<user>\generated`; copy them into `gfx/map/map_object_data/`, overwrite, and restart the editor.

### Adjacencies

`map_data/adjacencies.csv` connects baronies that do not touch:

```
ID From;ID To;Type;ID Through;start_x;start_y;stop_x;stop_y;Comment
1527;1526;river_large;629;948;2791;-1;-1;London-Southwark
-1;-1;;-1;-1;-1;-1;-1;
```

- `ID From`, `ID To`, `ID Through` are `definition.csv` IDs; From/To are baronies, Through is a sea or navigable river.
- `Type` is `sea` or `river_large`. Embark/disembark coordinates may be `-1` to default to the barony's normal army placement.
- **Preserve the trailing `-1;-1;;-1;-1;-1;-1;-1;` line even if nothing else follows it**; removing it produces an infinite loading screen.

### Custom resolution and terrain textures

- Custom resolution changes the heightmap, province map, river map, all locator files and the `common/defines` map dimensions together; also set `common/defines/graphic/00_graphics.txt` (`PANNING_WIDTH`).
- Terrain textures: copy `game/gfx/map/terrain` into the mod, then provide the diffuse, normal, properties textures and a `mask.bmp` the same size as `heightmap.bmp`, and register the layer in `material.settings`. Global behaviour lives in `settings.terrain`.
- Channel layout (Metalness-Roughness PBR): Diffuse A is the material heightmap; Normal B is emissive, Normal A is Normal G; Properties G is specular, B is metalness, A is roughness. Work per channel, not per layer, or the map looks washed out.
- After adding a texture, re-export the map so the optimised detail maps refresh; otherwise terrain offsets and biomes appear in the wrong places.
