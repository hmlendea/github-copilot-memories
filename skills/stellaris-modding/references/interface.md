# Interface: `.gui` Layouts and `.gfx` Sprite Libraries

## Folder Facts

- `interface/` is **LIOS** for both `.gui` and `.gfx`.
- `.gui` files define layout; `.gfx` files bind sprite names to textures.
- Add new files rather than editing vanilla ones; vanilla structural edits break on every patch and every conflicting UI mod.

## Debug Loop

| Command | Effect |
|---------|--------|
| `reload <file>.gui` | Re-parses one GUI file without restart; `.gui` only |
| `reload texture all` | Reloads all textures referenced by `.gfx`; a texture **size** change still needs a restart |
| `reload texture <name>` | Reloads one sprite |
| `guibounds` | Tooltip identifying the element under the cursor and its file |
| `debugtooltip` | Richer tooltips; `Ctrl+Alt+Right Click` opens or reloads the GUI file behind an element (3.7+) |

Some geometry and colours are controlled by `defines`, under the `interface` category.

## GUI File Structure

All elements live inside `guiTypes = { ... }`. `name` is the only mandatory attribute.

```
guiTypes = {
    containerWindowType = {
        name = "my_window"
        position = { x = 0 y = 100 }
        size = { width = 400 height = 200 }
        orientation = center_up
        origo = center_up
        background = {
            name = "background"
            spriteType = "GFX_tile_large_bg"
        }
    }
}
```

Element types in active use: `containerWindowType`, `buttonType`, `iconType`, `instantTextBoxType`, `effectButtonType`, `dropDownBoxType`, `listboxType`, `positionType`, `windowType`. Most are hardcoded: attributes can be modified, but adding or removing elements from a vanilla window commonly crashes the game.

## Attributes

Frequently used: `name`, `position` (`x`,`y`), `size` (`width`,`height`), `orientation`, `origo`, `centerPosition`, `background`, `spriteType`, `quadTextureSprite`, `frame`, `scale`, `mirror`, `alwaysTransparent`, `clipping`, `margin` (`top`,`bottom`,`left`,`right`), `verticalScrollbar`, `buttonFont`, `buttonText`, `multiline`, `pdx_tooltip`, `shortcut`, `clicksound`, `font`, `text`, `maxWidth`, `maxHeight`, `fixedSize`, `moveable`.

- `size` only works with `corneredTileSpriteType` sprites, referenced via `quadTextureSprite`.
- `origo` fixes the reference corner so resizing does not require repositioning.
- `alwaysTransparent = yes` removes the element from hit-testing and `guibounds`.

## Variables and Conditionals

```
@my_width = 50%
@my_background = "GFX_tile_large_center_bg"
```

`@` variables are single-assignment, declared anywhere in the file, and cannot traverse element nesting.

```
if_resolution = { min_width = 1920 min_height = 1080 ... }
if_scaled_resolution = { max_width = 1280 max_height = 720 ... }
```

`if_scaled_resolution` compares against the resolution after UI scaling (4K at 0.5 scaling tests as 1920×1080).

## Dynamic Text Limitation

Most UI text is hardcoded to internal values; bracket commands placed in ordinary elements render literally. The exception is `effectButtonType.buttonText`, which resolves bracket localisation and can therefore display script variables.

## Element Examples

```
containerWindowType = {                     # scrollable box
    name = "container"
    position = { x = 10 y = 10 }
    size = { width = 200 height = 200 }
    margin = { top = 5 bottom = 5 left = 5 right = 5 }
    verticalScrollbar = "right_vertical_slider"
    background = { name = "background" spriteType = "GFX_tiles_dark_area_cut_8" }
}

buttonType = {
    name = "button"
    spriteType = "GFX_standard_button_116_34"
    position = { x = 10 y = 10 }
    buttonFont = "cg_16b"
    buttonText = "DIPLOMACY"
    pdx_tooltip = "MY_BUTTON_TOOLTIP"
}

buttonType = {                              # resizable
    name = "button"
    quadTextureSprite = "GFX_interface_list_light"
    size = { x = 60 y = 48 }
    position = { x = -70 y = 51 }
    orientation = upper_right
    buttonFont = "cg_16b"
    buttonText = "APPLY_ON_EMPTY"
    multiline = yes
}

iconType = {
    name = "my_icon"
    position = { x = 25 y = 25 }
    spriteType = "icon_spritesheet"
    frame = 8
    scale = 0.65
    mirror = yes
}
```

## GFX Libraries

```
spriteTypes = {
    spriteType = {
        name = "GFX_my_mod_eventpicture_1"
        texturefile = "gfx/event_pictures/my_mod_event_1.dds"
    }
    corneredTileSpriteType = {
        name = "GFX_my_mod_tile_bg"
        texturefile = "gfx/interface/my_mod/tile_bg.dds"
        borderSize = { x = 80 y = 80 }
    }
}
```

Attributes: `name` (unique — always prefix with the mod token), `textureFile` (path relative to the installation root), `alwaystransparent`, `borderSize` (tile sprites only), `effectFile`, `masking_texture`, `noOfFrames`.

Sprite kinds: `spriteType` (static), `corneredTileSpriteType` (resizable/tileable), `portraitType`, `progressbarType`.

`textureFile` paths resolve relative to the game installation root, so a modded `.dds` at `<mod>/gfx/...` is referenced as `gfx/...`.

Animation layer for `spriteType`:

```
animation = {
    animationmaskfile = "gfx/mask/my_mask.dds"
    animationtexturefile = "gfx/animation/my_anim.dds"
    animationrotation = 90.0
    animationlooping = yes
    animationtime = 50.0
    animationdelay = 0.0
    animationblendmode = "multiply"
    animationtype = "scrolling"
    animationrotationoffset = { x = 0.0 y = 0.0 }
    animationtexturescale = { x = 1.0 y = 1.0 }
    animationframes = { 1 2 3 }
}
```

## Custom Windows From Event GUIs

There is no supported way to create a new top-level window. The workable approach reuses a diplomatic event window:
1. In the event: `diplomatic = yes` plus `custom_gui = "<containerWindowType name>"`.
2. The referenced `containerWindowType` name must match exactly; a mismatch crashes.
3. **Never delete** existing children — the game looks for them by name and crashes if absent. Hide them instead: `size = { width = 0 height = 0 }`, or move them off-screen with a large negative `position`.
4. Common children to hide: `portrait_background`, `portrait`, `alien_message_background`, `option_list`, `heading`.
5. Add extra `instantTextBoxType` / `iconType` elements with fresh names for custom content.
6. Preserve container ordering; reordering the logic of the original window breaks it.

```
listboxType = {                             # hide the option list
    name = "option_list"
    position = { x = 11450 y = 11175 }
    backGround = ""
    size = { x = 0 y = 0 }
    spacing = 1
    scrollbartype = "standardlistbox_slider"
    borderSize = { x = 0 y = 0 }
    orientation = "UPPER_LEFT"
}
```

`custom_gui_option` replaces every option button in the window; `custom_gui` inside a single `option` replaces only that button and takes precedence.

## Compatibility Rules

1. Never edit a vanilla `.gui` unless the mod is explicitly a UI overhaul; instead register new elements plus a patch mod that applies attribute-only edits.
2. All `.gfx` sprite names must be globally unique — collisions produce the wrong art or an override, not an error.
3. Keep UI edits attribute-level (position, size, sprite, text). Structural edits crash.
4. Provide a load-order note for UI submods; they must sit below their base mod.
5. Validate in-game with `guibounds` and `debugtooltip`, then confirm `error.log` is clean.

## Event Pictures and Icons

- Event art: `gfx/event_pictures/*.dds`, referenced by a `GFX_*` sprite in `interface/*.gfx`.
- Interface icons: `gfx/interface/icons/<category>/<key>.dds`, with categories such as `buildings`, `districts`, `jobs`, `resources`, `technologies`, `modifiers`, `traits`, `edicts`, `decisions`, `armies`, `ship_parts`.
- Buildings prefer `icon = <key>`, but the game still logs an error when `gfx/interface/icons/buildings/<key>.dds` is missing even if `icon` points elsewhere.
- Flags: `flags/*.dds` plus masks under `gfx/interface/flags/`.