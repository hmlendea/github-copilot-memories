# Interface, Audio, Localisation, and Image Formats

## Where UI Text Comes From

Three separate systems, and a string lives in exactly one of them:

| Source | Path | Covers |
|--------|------|--------|
| Data text files | `data/text/*.txt` | Units, buildings, traits, ancillaries, regions, settlements, events, menu, tooltips, advice |
| Feral UI strings | `Contents/Resources/<lang>.lproj/Localizable_Game.strings` | Buttons, main-menu items, launcher-adjacent labels |
| Building condition aliases | `display_string <key>` in EDB, text in `expanded_bi.txt` | Custom requirement explanations |

Override the Feral layer by shipping `data/string_overrides/<language code>.strings` — `en.strings` for English, and the equivalent code per language. Files are named after the language, not the original filename.

### Data text files

`export_units.txt`, `export_buildings.txt`, `export_ancillaries.txt`, `export_vnvs.txt`, `expanded_bi.txt`, `strat.txt`, `tooltip.txt`, `shared.txt`, `menu_english.txt`, `event_strings.txt`, `event_titles.txt`, `battle_descriptions.txt`, `historic_battles_subtitles.txt`, `FactionIntroSubTitles.txt`, `quotes.txt`, `campaign_name_regions_and_settlement_names.txt`, `date_format.txt`, `descr_shortcuts.txt`, `shortcut.txt`.

Format is `{key}<tab>value`. Keys are referenced from data files, not from code.

**Multi-language layout.** Remastered ships every language in one installation, so a mod that renames content must ship a variant per language or accept the English fallback. The convention the example mod uses:

```
data/text/imperial_campaign_regions_and_settlement_names.txt          ; English
data/text/imperial_campaign_regions_and_settlement_names_mac_de.txt
data/text/imperial_campaign_regions_and_settlement_names_mac_es.txt
data/text/imperial_campaign_regions_and_settlement_names_mac_fr.txt
data/text/imperial_campaign_regions_and_settlement_names_mac_it.txt
data/text/imperial_campaign_regions_and_settlement_names_mac_ru.txt
data/text/imperial_campaign_regions_and_settlement_names_mac_zh_cn.txt
```

A missing localised file falls back to the base name. Supply the languages you can and let the rest fall back rather than shipping stale copies.

`data/text/expanded_bi.txt` carries the senate office titles and descriptions, the custom EDB condition strings, and campaign event strings.

## `.pos` UI Overrides

Campaign and battle UI is data-driven through `data/ui_overrides/*.pos` (for example `battleui.pos`) plus `FeralUI.Anims` for animation. The main menu is a separate, largely asset-driven layer.

A `.pos` file has a `frames` array and a `list` array. Frames are background panels; list entries are the interactive and text elements. Both are JSON-like with `//` comments.

```json
{
	"position": { "x": -2, "y": -40 },
	"size": { "width": 320, "height": 72 },
	"priority": 2,
	"anchor": "TC",
	"align": "TC",
	"fill": "black_curved"
}
```

### Frame keys

`name`, `notch%`, `corner_avoid%`, `base_override`, `bi_override`, `alex_override`, `ignore_scale`, `ignore_aspect_ratio`, `position`, `lock_left`, `lock_right`, `scale_width`, `fill_left`, `fill_right`, `offset_left`, `offset_right`, `scale_x_pos`, `priority`, `fill`, `anim_id`, `ignore_mouse`, `steal_input`, `collapsed_size`, `anim_children`, `annotation_id`, `tags`, `additional_clipping`.

`anchor` and `align` accept `TC`, `TR`, `CL`, `C`, `CR`, `BL`, `BC`, `BR`, `RIGHT_PNL`, `LEFT_PNL`; the anchor is the screen point, the align is the point on the element that lands there. When an element is a child, the parent replaces the screen.

`fill` accepts `clear`, `black`, `black_curved`, `invisible`, `clear_thick`, `gold_border`, `decorated`, `black_curved_close_embedded`, `decorated_close_embedded`, `interlocking` — several of these also change behaviour, not just visuals.

### List keys

`name`, `ignore_scale`, `ignore_aspect_ratio`, `reference`, `notch%`, `corner_avoid%`, `ar_correct_height%`, `base_override`, `bi_override`, `alex_override`, `x`, `y`, `x%`, `y%`, `size`, `hidden`, `priority`, `align`, `fill_left`, `fill_right`, `offset_left`, `offset_right`, `scale_x_pos`, `scale_width`, `scale_width_ar_correct`, `fill_left_ar_correct`, `fill_right_ar_correct`, `hitbox`, `anchor`, `font`, `font_colour`, `max_lines`, `max_resizes`, `max_text_width`, `text_justification`, `tags`, `triggers`, `triggers_show`, `triggers_hide`, `triggers_toggle`, `annotation_id`, `anim_id`, `anim_children`, `ignore_mouse`, `additional_clipping`, `outside_slider`, `slider_gap`, `use_label_width`.

`triggers*` wire one element's selection to other elements' visibility — this is how panels swap content without duplicated layouts.

### Fonts and colours

Fonts: `tnr`, `tnr_lrg`, `tnr_med`, `tnr_sml`, `verdana*`, `feral_sml_med`, `feral_lrg_sml`, `verdana_bold`, `verdana_med_bold`, plus the `cinzel` family (`cinzel`, `cinzel_bold`, `cinzel_med`, `cinzel_med_bold`, `cinzel_sml`, `cinzel_sml_bold`, `cinzel_sml_med`, `cinzel_sml_med_bold`, `cinzel_lrg`, `cinzel_lrg_bold`, `cinzel_huge`, `cinzel_huge_bold`) and `verdana_med_bold_italic`, `verdana_sml_bold`.

Colours: `white`, `black`, `gold`, `khaki`, `enemy_red`, `ally_yellow`, `dark_brown`, `own_faction_blue`, `grey`, or a hex literal such as `"#FFFFFF"` (2.0.4).

Font definitions live in `descr_font_db.txt` and reference `.ttf` templates (the `tnr`, `verdana`, and `feral` families all come from `notoserif-regular.ttf`; `cinzel` from `cinzel-regular.ttf`).

### Tags and animations

The tag system keeps elements hidden until code activates their tag. Mods **cannot add tags** — only change what existing tags reveal. An element without tags is always visible.

`FeralUI.Anims` keys: `end_pos`, `ignore_scale`, `scale_x_pos`, `relative`, `anchor`, `duration`, `timeout` (`-1` disables), `start_actions`, `end_actions`. Actions are `show`, `hide`, `resize (duration, width, width%, height)`.

Author at 120% UI scaling: an element that fits at 100% may not fit at 120%.

UI mods are usually compatible with gameplay mods because they touch different files; two UI mods editing the same `.pos` conflict wholesale.

## Images

| Asset | Format | Size |
|-------|--------|------|
| Faction icons | `.tga` 32-bit | 512×512, 1:1 |
| Unit cards | `.tga` 32-bit + alpha | 164×224, 4:3 |
| Large unit image | `.tga` 32-bit + alpha | 328×448, 4:3 |
| Building cards | `.tga` 32-bit + alpha | 128×102 |
| News banners | `.tga` 24-bit | various |
| UI textures | `.tga` 32-bit | various |
| Loading screens | `.dds` DXT5, mip-mapped | 16:9 or 64:27; other ratios can crash |
| Unit/building 3D textures | `.dds` | 2048² typical |
| Hair | `.dds` DXT5, mip-mapped | 9216×1024 |
| Vegetation | `.dds`, mip-mapped | 2048×1024, power-of-two edges |

Compression for 3D textures: diffuse BC1 (4 bpp), diffuse+alpha BC3 (8 bpp), normal BC5 (8 bpp), greyscale BC4 (4 bpp). Original assets were compressed with Intel Texture Works 1.0.4 and then LZ4.

`.tga.dds` is a `.dds` whose name ends in `.tga` so that data files can keep the RTW-era `.tga` reference. Textures may be LZ4-compressed with an extra header; IWTE can bulk-decompress a directory. DX10-format textures need Texconv or a current Photoshop DDS plug-in to inspect.

PBR packaging differs by asset class:

- **Units**: `_pbr` texture is RGBA — R+G normal, B metallic, A roughness. Skin atlases ignore the blue channel.
- **Buildings**: separate maps — `_n` normal, `_s` smoothness/roughness (greyscale: white darkens in wet weather, dark shines in sun), `_m` metallic, `_e` emissive (unreliable in practice).
- **Hair**: single texture with normal in red/green, diffuse brightness in blue, alpha in alpha.

Files with transparency in building sets conventionally start with `##` or `#&`.

## Audio

`data/descr_sounds.txt` is the legacy entry point and is bypassed by the index files under `data/sounds/descrs/`. That folder reorganises the original subsidiary files into three families: `descr_enum_sounds.txt` (UI and generic effects), `descr_misc_sounds.txt` (weapon handling, engines, animals, chanting, narration), and `descr_bank_sounds.txt` plus per-bank descriptor files.

Human voice narration uses `.opus`, not `.mp3`. Bank content is packed into `.feral.dat`; the **Audio Packer** tool unpacks and repacks them.

Campaign and battle music is driven by state machines described in `sounds/descrs/banks/descr_soundbank_*_music*.txt`. Script can change music with `set_music_state`, which in Remastered requires the mode first (`battle` or `strat`/`custom`) before the state (`tension`, `mobilise`, `battle`).

## Movies

Front-end video moved from `.mpg` to `.webm`. Historical-battle intros, faction intro subtitles (`descr_subtitle.txt`), and faction victory and defeat movies (`descr_sm_factions.txt`) are the data hooks; `descr_fmv.txt` is unreliable and should not be relied on.

## Fonts

`descr_font_db.txt` maps font names to `.ttf` templates and sizes. `descr_font_db_ru.txt` and `descr_font_db_zh_cn.txt` load only for those locales. Hex colour values in `.pos` files are new in 2.0.4.

## Enhanced Tweaks Folder

`data/enhanced_tweaks/*.json` carries graphics overrides exported from the in-game overlay. The engine reads every file in the folder regardless of extension, so delete experiments before shipping, and strip resolution and quality entries so the mod does not force them on other players.