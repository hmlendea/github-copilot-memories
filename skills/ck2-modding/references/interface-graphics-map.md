# Interface, Graphics, Portraits, Coats of Arms, Map, Music and Sound

## Interface (`interface/*.gui`)

### Debugging the Interface

Press the console keys while still in the **main menu** (not in a campaign) to enable interface debug mode. Hovering an element then shows the defining file and line. Once a campaign has loaded, only `charinfo` debugging remains available.

### Main Files

| File | Screen |
|------|--------|
| `frontend.gui` | Lobby: era selection, character selection, multiplayer |
| `main.gui` | In-game shell: minimap, top bar, chat |
| `domestic_overview.gui` | Primary title tab |
| `domestic_dynastic.gui` | Character tab |
| `domestic_court.gui` | Councillors tab |
| `domestic_law.gui` | Laws tab |
| `domestic_technology.gui` | Technology tab |
| `domestic_military.gui` | Military tab |
| `domestic_plots.gui` | Intrigue tab |
| `domestic_factions.gui` | Factions tab |
| `domestic_religion.gui` | Religion and College of Cardinals tabs |
| `province.gui` | Province window |
| `focusview.gui` | Focus window |
| `combat.gui`, `waroverview.gui`, `unitpanel.gui` | Combat, warscore, army windows |
| `domestic_diplomacy.gui` | Diplomacy popup |
| `eventwindow.gui` | Event popups, all event types |

### Working Rules

- A `.gui` file at the same relative path replaces the vanilla file whole. There is no merge.
- Move or hide elements by editing `position` (push them off-screen with `{ x = -2000 y = -2000 }`) rather than deleting nodes, which commonly crashes.
- Button behaviour is hardcoded: existing buttons can be moved or hidden, not repurposed.
- Interfaces are hardcoded to vanilla religion groups; a new religion needs its own textures and, sometimes, a copied window (see papal succession below).
- New hotkeys are added with `shortcut = "<key>"` on an element; `priority_shortcut` fires before other handlers.

### Papal Succession Case Study

Using `succ_papal_succession` for a non-Catholic religion needs three coordinated edits:
1. Copy the succession law and widen its `potential` to include `d_<my_religion>`.
2. Copy the `domestic_religion_title_fraticelli_cardinal` window from `domestic_religion.gui` into `<my_religion>_domestic_religion.gui`, and rename `title_fraticelli_cardinal` to the new `common/religious_titles` entry.
3. Define that religious title.

Without step 2 the cardinal button exists and crashes to desktop on click.

### Adding a Focus

1. Increase `noOfFrames` in the `GFX_focusicons` `spriteType` in `focusview.gfx`.
2. Add `gfx/ambitions/<focus_name>.tga` and a `GFX_<focus_name>` `spriteType`.
3. In `focusview.gui`, add a further `iconType` and `positionType` entry and shift the existing positions.

## Graphics (`gfx/`, `interface/*.gfx`)

Two halves: assets in `gfx/`, and logical names starting with `GFX_` declared in `interface/*.gfx`.

Formats:
- `.tga` — uncompressed; used for flags, coats of arms, many interface elements.
- `.dds` — DXT-compressed; portraits, icons, modifier icons. GIMP and Photoshop need a DDS plug-in; Paint.NET does not.
- `.xac`/`.xsm` — licensed 3D model and animation format.
- `.mesh`/`.anim` — Paradox's own model format (since 2.2), convertible through JoroDox.

Sprite declaration:

```
spriteTypes = {
    spriteType = {
        name = "GFX_evt_custompic"
        texturefile = "gfx\\event_pictures\\custompic.tga"
    }
    spriteType = {
        name = "GFX_custom"
        texturefile = "gfx\\characters\\shared\\new_property.dds"
        noOfFrames = 2
        norefcount = yes
        can_be_lowres = yes
    }
}
```

Rules:
- `.gfx` files load alphabetically and the **last** definition of a name wins, so a `zz_` prefix overrides vanilla sprites.
- `noOfFrames` defines strip length; adding one frame shifts every later index in that strip.
- Only `interface/sound.sfx` is read; other `.sfx` files are ignored.
- Event pictures are 450×150. Title flags are 128×128, 24-bit, uncompressed `.tga`; deviating crashes the game.
- A missing flag shifts every later title's flag assignment.
- Modifier icons live in `gfx/interface/modifier_icons.dds` and are referenced by numeric index.
- Religion and trait icons are strips; extending a strip invalidates existing indices.
- Loading screens use `load_0.dds`, `load_1.dds`, … in `gfx/loadingscreens/`; the highest-numbered file has an outsized chance of appearing first.
- Event pictures can be overridden per culture or religion by defining `GFX_<picture>_<culture>` or `GFX_<picture>_<religion>`.

## Portraits (`interface/portrait*`, `gfx/characters/`)

### DNA

DNA is an 11-character string inherited from parents and fixed at birth. It can be set in character history and is visible in game through `charinfo`.

| Index | Feature |
|-------|---------|
| d0 | Neck |
| d1 | Chin |
| d2 | Mouth |
| d3 | Nose |
| d4 | Cheeks |
| d5 | Unused |
| d6 | Eyes |
| d7 | Ears |
| d8 | Hair colour |
| d9 | Eye colour |
| d10 | Unused |

Letters index frames (`a` = frame 1). Wraparound applies when the strip is shorter than the letter index, so a chin with four frames maps `a` and `e` to the same frame.

### Properties

Properties are up to 14 characters in vanilla, zero-padded when shorter. Only hair (`p1`) and beard (`p4`) are player-adjustable without the Customization Pack; everything else comes from `portrait_properties.txt` rules.

| Index | Layer | Index | Layer |
|-------|-------|-------|-------|
| p0 | Background | p10 | Blinded |
| p1 | Hair | p11 | Player marker |
| p2 | Base head | p12 | Mask |
| p3 | Clothes | p13 | Eyepatch |
| p4 | Beard | p17 | Immortality glow |
| p5 | Headgear | p20 | Freckles |
| p6 | Imprisoned | p21 | Physique |
| p7 | Scars I | p25–p26 | Scars II–III |
| p8 | Red dots | p27 | Blood splatter |
| p9 | Boils | p30 | Demon child |

Adding a property means declaring a `spriteType` (with `noOfFrames`) and configuring that property index in `portrait_properties.txt` with weighted options.

### Ethnicities and Portrait Types

1. `common/graphicalculturetypes/` gains `gothicgfx = { skin_tone = 0 }`.
2. The culture lists `graphical_cultures = { gothicgfx occitangfx }`. In sub-mods the **last** entry must be a vanilla base type (`occitangfx`, `muslimgfx`, `byzantinegfx`, `westerngfx`).
3. `interface/portraits_gothic.gfx` declares `PORTRAIT_<culturegfx>_{child,male,female}[1,2]` `spriteType`s and matching `portraitType`s.

A `portraitType` is a layer list; each entry names a sprite and optionally a property index and colour link:

```
portraitType = {
  name = "PORTRAIT_gothicgfx_female"
  effectFile = "gfx/FX/portrait.lua"
  layer = {
    "GFX_character_background:p0"
    "GFX_byzantine_female_clothes_behind:p3:c0"
    "GFX_norse_female_hair_behind:p1:h:y"
    "GFX_norse_female_base:p2"
    "GFX_norse_female_neck:d0"
    "GFX_norse_female_mouth:d2"
    "GFX_norse_female_nose:d3"
    "GFX_norse_female_chin:d1"
    "GFX_norse_female_cheeks:d4"
    "GFX_norse_female_eyes:d6"
    "GFX_character_scars:p7:y"
    "GFX_byzantine_female_clothes:p3:c2"
  }
}
```

Layer syntax is `GFX_NAME:[d|p]<index>[:colour link][:flags][:culture index]`. Order matters: behind-layers come before the base head, front-layers after.

Related files:
- `interface/portrait_offsets/` — external frame offsets.
- `interface/portrait_properties/` — dynamic rules selecting property values.
- `occluded = yes` on a character suppresses the hair layer for headgear.
- Static portraits and the `portrait` scope are used for rendering rules, not for characters.

## Coats of Arms (`common/dynasties`, `common/landed_titles`, `gfx/flags`, `interface/coats_of_arms.gfx`, `interface/coats_of_arms.txt`)

Three shield systems:

| Owner | Predefined source | Random |
|-------|-------------------|--------|
| Title, county and above | `gfx/flags/<title>.tga` | When the religion group sets `has_coa_on_barony_only = no` |
| Barony title | `coat_of_arms = { }` in landed titles | Default |
| Dynasty | `coat_of_arms = { }` in `common/dynasties` | Default |

Flag rules:
- Filename must be exactly `<title>.tga`, 128×128, 24-bit, uncompressed.
- One missing flag shifts every later flag assignment, so ship them all.
- Baronies never use `gfx/flags/`.

Layered definition:

```
coat_of_arms = {
    template = 0
    layer = {
        texture = 2
        texture_internal = 9
        emblem = 0
        color = 3
        color = 1
        color = 2
    }
    religion = "catholic"
}

coat_of_arms = {
    data = { 0 2 0 9 3 1 2 }
    religion = "catholic"
}
```

The shorthand order is `template texture emblem texture_internal color1 color2 color3`. All indices are zero-based.

Supporting files:
- `interface/coats_of_arms.gfx` declares `spriteType` entries plus `CoatOfArmsType` templates (`name`, `frame`, `mask`, `seal_overlay`, `effect`, per-layer `mask`, `center`, `scale`).
- `interface/coats_of_arms.txt` holds `culture`, `templates` (`"coa_party_per_pale:2"` with layer counts), `color` lists in 0–255 RGB, `banned_colors`, and `textures` per religion.
- Definitions may be split across files, but an existing definition cannot be appended to from another file.
- `pagan_coa = { }` on a title supplies alternative arms while a pagan holds it; `color = 0` inside a layer disables recolouring, which is how full-colour shields work.

## Map (`map/`)

| File | Contents |
|------|----------|
| `provinces.bmp` | Province shapes by exact RGB; 3072×2048 by default |
| `definition.csv` | One line per province: `id;r;g;b;Name;x` |
| `default.map` | `max_provinces`, `sea_zones`, `ocean_region`, `major_rivers`, `externals` |
| `adjacencies.csv` | Cross-water and cross-river connections |
| `positions.txt` | Unit and settlement positions per province |
| `rivers.bmp` | River paths |
| `terrain.bmp`, `terrain.txt` | Terrain types and their combat and movement effects |
| `trees.bmp`, `trees.txt` | Tree type, density, and size |
| `topology.bmp` | Height map |
| `colormap*.bmp`, `colormap.txt` | Seasonal map colouring |
| `climate.txt` | Climate zones |
| `world_normal_height.bmp` | Normal map for lighting |
| `statics/` | Frame size and fixed 3D map element positions, such as wonders |

Rules:
- `provinces.bmp` must use solid colours with no antialiasing, transparency, or colour-space metadata. Saving it as 24-bit R8G8B8 without colour space is required; anything else crashes on load.
- `max_provinces` must be the highest province ID plus one, or the last province is ignored.
- Each `sea_zones` entry takes exactly two IDs spanning a contiguous range; each zone is mutually navigable.
- A sea province with no sea neighbours is treated as a lake and generates no adjacent ports.
- `externals` are points outside every province, used as trade-route entry points.
- `sea_starts` is obsolete since 2.1.

Adding a province, in order:
1. Pick an unused RGB triple.
2. Paint solid colour in `provinces.bmp`.
3. Append the row to `definition.csv`.
4. Increment `max_provinces`.
5. Add `history/provinces/<id> - <Name>.txt`.
6. Add the county title in `common/landed_titles/`.
7. Add `history/titles/<title>.txt`.
8. Add `map/climate.txt` entry if needed.
9. Localise the province name and the title name and adjective.
10. Ship `gfx/flags/<title>.tga`.
11. Fix positions with the Nudge tool.

Troubleshooting:
- `Province xxx has no pixels in provinces.bmp` in `error.log` means a `definition.csv` row has no matching colour.
- Provinces missing from realm view usually means colour-space metadata survived the `.bmp` save.

## Music (`music/`)

- Audio must be Vorbis `.ogg`; `.mp3` is unsupported.
- Sample rate must be 44100 Hz since 2.7; other rates play scratchy or silently.
- Definitions live in `.txt` files inside `music/`, one `song` block each. All `.txt` files there are read.

```
song = {
    name = "englandanno1066.ogg"
    song_name = "England Anno 1066"
    chance = {
        factor = 2
        modifier = {
            factor = 0
            NOT = { culture = english }
            NOT = { culture = saxon }
        }
    }
    volume = 0.45
}
```

- `factor` is a relative weight; vanilla base songs use 1.
- `modifier` blocks multiply the factor under normal conditions, so `factor = 0` excludes a song.
- Conditions are ordinary script conditions, including date checks such as `real_month_of_year`.
- Adding songs to the vanilla playlist requires a definition file with a **different name** from `songs.txt` (for example `asongs.txt`), because a same-named file collides with the vanilla definition file. If the mod replaces the whole `music/` folder through `replace_path`, name the opening track `crusaderkings2_maintitle` and reference it from the mod's own definition file, or no music plays at start.

## Sound (`sound/`, `interface/sound.sfx`)

- Effects are `.wav` files with entries in `interface/sound.sfx`.
- Only `interface/sound.sfx` is loaded; additional `.sfx` files are ignored, so a mod that adds sounds must replace that file or be the only supplier.
- Events reference sounds with `sound = <sfx name>`.

## Localisation Ties

Every asset in this reference needs at least one key: `GFX_` names are not localised, but titles need `<title>` and `<title>_adj`, cultures and religions need `<id>`, and modifiers need `<modifier>` and `<modifier>_EXPLANATION`. See `references/localisation.md`.