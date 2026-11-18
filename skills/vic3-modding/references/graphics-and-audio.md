# Graphics and Audio: Coats of Arms, Flags, Textures, Models, and FMOD Sound

## Coats of Arms and Flags

A country's flag is not an image file; it is a scripted **coat of arms (CoA)** composed of layered vector-like elements. Two folders matter:

| Path | Contents |
|------|----------|
| `common/coat_of_arms/coat_of_arms/` | CoA definitions (`*_subs.txt`, country files) |
| `common/coat_of_arms/template_lists/` and `coa_templates/` | List-based CoA templates |
| `common/flag_definitions/` | Which CoA a country uses, under which trigger |
| `common/named_colors/` | Named colours (HSV or decimal RGB) |
| `gfx/coat_of_arms/patterns/` | Pattern masks (`.tga` / `.dds`) |
| `gfx/coat_of_arms/colored_emblems/` | Recolourable emblem masks |
| `gfx/coat_of_arms/textured_emblems/` | Full-colour emblems |

CoA element canvas is 768×512 pixels (some emblems are 256×256).

### Element types

- **pattern** — mandatory base layer, exactly one per CoA. Red pixels are replaced by `color1`, yellow by `color2`, and (in some patterns) white by `color3`. Patterns also mask emblems and subs.
- **colored_emblem** — mask recoloured by `color1`/`color2`/`color3`. Encoding: blue channel is brightness; adding green selects `color2`; adding red selects `color3`. Example `color1` pixel ≈ R0 G0 B128.
- **textured_emblem** — full-colour image; always drawn above colored emblems.
- **sub** — a reference to another CoA (`parent = "sub_name"`), with its own transform.

Layer order is definition order, and textured emblems always sit above colored emblems.

```
SCA = {
    pattern = "pattern_solid.tga"
    color1 = "red"
    color2 = "red"

    colored_emblem = {
        texture = "ce_bicolor_bottom.dds"
        color1 = "blue"
        color2 = "blue"
    }

    colored_emblem = {
        texture = "ce_cross_denmark.dds"
        color1 = "white"
        color2 = "white"
        instance = { scale = { 1.6 1.6 } position = { 0.6 0.5 } }
    }
}
```

`instance` supports `scale`, `position`, `rotation`, and `mask`. `@` values (e.g. `@[1/5]`) are commonly used for fractional scales.

The first three colours also tint the country's unit models unless `primary_unit_color`, `secondary_unit_color`, `tertiary_unit_color` are set in the country definition.

### Flag definitions

`common/flag_definitions/` selects which CoA a country displays:

```
ALD = {
    flag_definition = {
        coa = ALD
        subject_canton = ALD
        allow_overlord_canton = yes
        coa_with_overlord_canton = ALD_subject
        priority = 1
    }
    flag_definition = {
        coa = ALD_republic
        subject_canton = ALD_republic
        priority = 10
        trigger = { coa_def_republic_flag_trigger = yes }
    }
}
```

- The highest `priority` whose `trigger` passes wins.
- Without a scripted list, the game falls back to a CoA keyed exactly as the country TAG, then to a generated random flag.
- The `DEFAULT` list applies to all countries and is the normal home for revolutionary and dynamically created subject flags.
- `allow_revolutionary_indicator` (default yes) and `revolutionary_canton` control the temporary revolutionary overlay.

Flag definitions are `INJECT`-able, so new variants can be appended without restating the vanilla list:

```
INJECT:ALD = {
    flag_definition = {
        coa = ALD_cool_new_flag
        priority = 11
        trigger = {
            coa_def_republic_flag_trigger = yes
            has_variable = ALD_chose_new_flag
        }
    }
}
```

Use `REPLACE:` when an existing entry must be removed.

Trigger scope rules apply: flag definition triggers run in country scope, so use country-scope triggers only. `coa <>` values may name a template list rather than a single CoA.

### Power bloc emblems and templates

Power bloc emblems use the same element model but a square (1:1) canvas rather than the 3:2 flag canvas, and live in `common/coat_of_arms/template_lists/` as `template_power_bloc_*` definitions. They may use `list "..."` values in place of literal textures and colours, resolved from `coa_templates/`:

```
template_power_bloc_1 = {
    pattern = "pattern_solid.tga"
    color1 = { 0.0 0.0 0.0 0.0 }

    colored_emblem = {
        texture = list "power_bloc_shield"
        color1 = list "power_bloc_colors"
        color2 = list "power_bloc_colors"
        instance = { scale = { 0.72 0.72 } position = { 0.49 0.6 } }
    }
}
```

Layer order for power bloc emblems is also referenced from `NGraphics::NPowerBlocCoa::PIECE_LAYERS_ORDER` and `NPowerBlocCoa` in `00_defines.txt`; changing the order in script without matching both breaks rendering. Mods can add bloc identities and principles with their own emblem sets, but keep the element count low: every bloc emblem is rendered in the bloc overview.

## Textures

- Format: **DirectDraw Surface** (`.dds`). `.png` is accepted by the engine in most cases but is larger and slower.
- Compressed (BC7 / DXT5) textures must have dimensions divisible by 4, otherwise the UI scales incorrectly and logs an error.
- Export settings that work:
  - Paint.NET: `BC7 (sRGB, DX 11+)`, *Generate Mip Maps*, Bicubic interpolation.
  - Paint.NET uncompressed: `B8G8R8A8 (Linear, A8R8G8B8)`, with mip maps.
  - GIMP: `BC3 / DXT5`, mip maps on for everything except event pictures, Kaiser filter.
- Always generate mip maps. Without them, icons look crunchy when downscaled.

### Icon paths by type

| Type | Expected path |
|------|---------------|
| Event icons | `gfx/interface/icons/event_icons/` |
| Invention / technology icons | `gfx/interface/icons/invention_icons/` |
| Law icons | `gfx/interface/icons/law_icons/` |
| Decree icons | `gfx/interface/icons/decree/` |
| Building icons | `gfx/interface/icons/building_icons/` |
| Religion icons | `gfx/interface/icons/religion_icons/` |
| Timed modifier icons | `gfx/interface/icons/timed_modifier_icons/` |
| Event pictures | `gfx/event_pictures/` |
| Coat of arms parts | `gfx/coat_of_arms/{patterns,colored_emblems,textured_emblems}/` |

Sprites are declared in `.gfx` files (`interface/*.gfx` or `gfx/`-relative `*.gfx`). A texture without a sprite definition is not reachable from `.gui`, though script types that take a raw `texture = "path.dds"` (icons, modifiers, laws, decrees) bypass that.

### Event images

Two forms:

```
event_image = { video = "media_alias_name" }          # .bk2 Bink video, aliased in gfx/media_aliases/media_aliases.txt
event_image = { texture = "gfx/event_pictures/x.dds" } # still image
```

Character-portrait events use `gui_window` plus `left_icon` / `right_icon` (character scopes), or `minor_left_icon` / `minor_right_icon` (country scope shows the flag, character scope shows a small portrait). Vanilla `event_window` definitions live in `gui/eventwindow.gui`.

## 3D Models

A model lives in a folder under `gfx/models/` and consists of three file kinds:

| File | Role |
|------|------|
| `.asset` | Declares how the engine identifies and uses the model — the bridge between `.mesh` and rendering. Text file; **must use LF line endings**, CRLF breaks it |
| `.mesh` | The geometry itself; the file you edit |
| `.dds` | The model's textures |

Workflow:

1. Find the vanilla model (e.g. `gfx/models/buildings/european/city_urban_center_01/`).
2. Replicate that exact folder path inside the mod and copy the files there. Never edit the game installation's copy.
3. Import the `.mesh` in a 3D editor with Paradox mesh support — Blender plus the PDX Blender Tools, or IO PDX Tools by Ross G.
4. Edit `LOD_0_mesh_mesh` for normal work. Each `.mesh` contains three objects (`decal_decal`, `mesh_mesh`, `worlddecal_worlddecal`) duplicated across four LOD levels; LOD_0 is the highest detail and usually the only one worth editing, while LOD 1-3 are lower-detail copies used by distance and graphics settings.
   - `decal_decal` is a ground-plane decal — do not modify it.
   - `worlddecal_worlddecal` marks the model's footprint on the shared city grid — do not modify it, and never make the model larger than it.
5. Export back to `.mesh`, then adjust the mod's `.asset` only if the identifier needs changing.

Registration: unit models, building map models, and map objects are referenced from the relevant `common/` definition (building definitions carry `map_models`), not from `.gui`. There is no supported pipeline for adding new character body meshes — character appearance is driven by `dna`, ethnicities, culture graphics, and textures.

`Model modding` on the wiki is marked version-unknown and incomplete (`TODO` sections remain); verify against the shipped files rather than trusting it as complete. The Clausewitz Maya Exporter listed on the `Modding` page exists for other Clausewitz titles and is not the documented Victoria 3 path.

## Audio and FMOD

All sound goes through **FMOD Studio**. Use **version 2.02.03** — the version recommended by the developers and confirmed by modders.

### Project setup

1. Create a project. Use the community FMOD template if available; it predefines the vanilla groups and VCAs.
2. **Delete the template's provided master bank.** Shipping it breaks every other sound mod that also fails to delete it.
3. Create your own master bank and name it so it sorts **after** `VFX`; a bank that loads ahead of vanilla sound banks can break vanilla audio.
4. For every vanilla group or VCA you reuse (`bus:/`, `bus:/MUSIC`, `bus:/MUSIC/Mood`, `vca:/MUSIC`), copy the GUID from `<game>/sound/GUIDs.txt` into your project's `Metadata/` files. Close FMOD before rewriting GUIDs, reopen, then build.
5. Build, then copy the produced bank files into `<mod>/sound/banks/` — `sound` is singular and `banks` is plural.

### Importing sounds

1. Drag assets into the **Assets** tab (WAV, MP3, OGG, AIFF, WMA, FLAC accepted).
2. Right-click → **Create Event** (2D Timeline is fine for UI sounds).
3. Assign the event to your master bank.
4. Route through the correct VCA so vanilla volume sliders affect it.
5. Build and copy the banks.

### Playing sounds from script and GUI

- Events: `on_opened_soundeffect = "event:/SFX/UI/Alerts/event_appear"`.
- Anywhere an effect or GUI property accepts a sound, use the full FMOD event path `event:/...`.
- Music is selected through the music system, not by playing an event directly: use `Music.PlayTrack <track>` for testing and define music entries in `common/`/`sound/` playlists for shipping.

Vanilla event sound paths are worth copying verbatim; inventing a path that does not exist produces silence with only a log line.

## Validation Checklist

- [ ] Every `.dds` is divisible by 4 on both axes and has mip maps.
- [ ] Every sprite referenced in `.gui` exists in a `.gfx` file and its texture path resolves.
- [ ] Every `texture = "..."` in a script type points at an existing file with the right extension and casing.
- [ ] Coat of arms elements reference textures under `gfx/coat_of_arms/`, and each CoA has exactly one `pattern`.
- [ ] Flag definitions resolve: the TAG exists in `common/country_definitions`, and each `coa` key exists.
- [ ] The FMOD master bank is not the template bank, sorts after `VFX`, and is present in `sound/banks/`.
- [ ] No vanilla GUIDs were left mismatched (vanilla groups stay audible after enabling the mod).