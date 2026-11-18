# Interface, Localisation, Flags, Graphics, Fonts, and Audio

## Localisation

**Folder:** `<top_folder>/localization/<language>/`, filenames `<name>_l_<language>.yml`, **UTF-8 with BOM**.

- A `.yml` file without a BOM is ignored entirely.
- The folder name is `localization` with a **z**; the language subfolder uses the internal name (`english`, `braz_por`, `french`, `german`, `polish`, `russian`, `spanish`, `japanese`, `simp_chinese`, `korean`, `turkish`).
- Files load in **reverse alphabetical order** (Z → A), and later-loaded keys do **not** overwrite earlier ones. Prefix with `a` or `0` to apply last.
- `localization/<language>/replace/` overrides keys explicitly and reliably; this is the recommended way to patch vanilla text.

### Entry format

```
l_english:
 my_key: "Localized text"
 my_key_2:0 "Revised text"
```

- One leading space, key, colon, space, quoted string. A revision number after the colon is optional.
- `#` starts a comment outside quotation marks.
- Nesting keys with `$key$` substitutes another localisation value.

### Formatting

| Syntax | Effect |
|--------|--------|
| `#R`, `#N`, `#color_red` | Red |
| `#P`, `#G`, `#color_green` | Green |
| `#E`, `#color_concept` | Blue concept colour |
| `#V`, `#Z`, `#color_white` | White |
| `#color_pure_white`, `#color_yellow`, `#color_black`, `#color_gray`, `#F` (flavor), `#color_light_gray`, `#ZG` | Other palettes |
| `#bold`, `#italic` | Bold / italic |
| `#!` | Ends the current formatting rule (no space before it) |

Formatting nests; each nested rule needs its own `#!`. Rules can also be joined with a semicolon. Text formatting definitions live in `gui/textformatting.gui`; custom keys can be added with `textformatting` blocks in any `.gui` file.

Custom tooltip inline: `#TOOLTIP:<loc_key> <display_text>#!`.

### Text icons

`@key!` inserts a text icon: `@gold!`, `@time!`, `@legitimacy!`, `@adm!`, `@warning_icon!`, `@trigger_yes!`, `@trigger_no!`, `@laborers!`. Base icons live in `gui/shared/font_icons.gui`; new ones are declared in `texticon` blocks in any `.gui` file.

### Data functions

`[Function]` inserts a computed string. Chaining uses dots: `[Country.MakeScope.GetName]`. Arguments go in parentheses; game script keys are single-quoted, other functions are not: `[GetPopTypeByName('peasants').GetName]`, `[ScriptValue('my_value')]`.

String-returning functions include `GetName`, `GetNameWithFlag`, `GetAdjective`, `GetAdjectiveWithNoTooltip`, `GetFullName`, `GetAbilityTooltipAsRuler`, `GetLaw('law_key')`.

Functions starting with `Access` take and return const types; those starting with `Get` take and return non-const types.

Function format codes go after a pipe before the closing bracket:

| Code | Effect |
|------|--------|
| `=` | Force a sign |
| `+` | Green positive / red negative |
| `-` | Red positive / green negative |
| `D` | Abbreviate (1K, 1M, 1B) |
| `U` | Capitalise the first letter |
| `%` | Convert to percentage |
| `0-5` | Decimal places to display |

### Saved scopes in localisation

Save a scope with `save_scope_as` in an `immediate` block (or in related earlier content), then reference it:

```
my_desc: "The [usa_nation_scope.GetName] is a country."
my_desc_alt: "The [SCOPE.sCountry('usa_nation_scope').GetName] is a country."
my_ruler: "Our leader, [SCOPE.sCharacter('pru_leader').GetFullName], is pleased."
```

Timing matters: a scope saved in an event is valid only while that content is alive (for situations, for the duration of the situation).

### Variables in localisation

```
custom_tooltip = { text = "my_localization_string" }
```
```
my_localization_string: "The value is [SCOPE.GetLocalVariable('my_variable').GetValue]"
```

### Concepts

Concepts are declared in `main_menu/common/game_concepts/` and referenced with `[concept_key]` or `[concept_key|e]` (blue concept formatting). Each concept needs its own localisation key.

### Customizable localisation

**Folder:** `in_game/common/customizable_localization/`

Called **only** through `Custom('custom_localization_name')` in a localisation string; there is no automatic selection.

```
ruler_residence = {
    type = country               # country / character / building / ...
    random_valid = no            # first valid (default) or random valid

    text = {
        trigger = { government_type = government_type:monarchy }
        localization_key = custom_royal_palace
    }
    text = {
        trigger = { government_type = government_type:republic }
        localization_key = custom_presidential_palace
    }
    text = {
        trigger = { any_owned_location = { is_coastal = yes } }
        localization_key = custom_coastal_palace
    }
}
```

## GUI

**Folders:** `<top_folder>/gui/`, `in_game/gui/scripted_widgets/`, `main_menu/gui/`, and `loading_screen/data_binding/` for macros.

### Core concepts

| Element | Meaning |
|---------|---------|
| `template` | Reusable property container applied via `using = template_name` |
| `type` | Reusable widget or container definition; can be extended and overridden |
| `types` | Container holding `type` definitions; the container itself has no overwrite logic |
| `window` | Top-level UI entity |
| `widget` | Grouped UI elements that participate in layout |
| `block` / `blockoverride` | Named regions that types and templates can override |

### Defining a type

```
types my_types_general_naming {
    type example_base_type = widget {
        block "test_block" {
            size = { 100 100 }
        }
    }
}
```

Use it:
```
widget = {
    example_base_type = {}
}
```

### Creating a window

```
window = {
    name = "mymod_window"
    parentanchor = center
    size = { 100% 100% }
    alwaystransparent = yes
    visible = "[GetVariableSystem.Exists('mymod_window_open')]"
}
```

### Registering a scripted window

Create `in_game/gui/scripted_widgets/mymod_interface.txt` (UTF-8 BOM):
```
gui/mymod_interface.gui = mymod_window
```
Without this registration, the window can only be opened with `GUI.CreateWidget`.

### Opening and closing

| Method | Open | Close |
|--------|------|-------|
| Variable toggle (recommended) | `onclick = "[GetVariableSystem.Toggle('mymod_window_open')]"` | same toggle |
| Console | `onclick = "[ExecuteConsoleCommand('GUI.CreateWidget gui/mymod_interface.gui mymod_window')]"` | `onclick = "[ExecuteConsoleCommand('GUI.ClearWidgets mymod_window')]"` |

`gui.clearwidgets` closes all scripted windows.

### Buttons in existing panels

Define a button type extending a vanilla type, then add it to the panel in a modded copy of the vanilla `.gui` file:
```
types iv2_main_idea_button {
    type button_panel_tab_ideas = button_panel_tab_alt {
        ...
    }
}
```

Prefer adding new types over rewriting vanilla widgets; existing panels are edited in place and whole-window replacement is required.

### Tooltips

```
tooltipwidget = {
    using = my_tooltip_template
}
```
```
tooltipwidget = {
    using = my_tooltip_template
    blockoverride "tooltip_content" {
        using = action_tooltip_inner_content
    }
}
```

A generic action tooltip renders conditions and effects automatically when it references an action.

### GUI refresh gotcha

A script value displayed as **text** may not refresh when the value changes through an on_action or an invisible event; the UI may only update when a player-clicked event recalculates it. Progress bars update on the monthly tick. Design UI updates around event-click chains or variable changes that the UI observes.

## GUI Script

GUI script powers tooltips and dynamic UI text.

- Written in `PascalCase` / `UpperCamelCase`: `GetName`, `ShowRoadBuilder`, `Custom('name')`.
- Functions and promotes chain with dots: `[State.GetJobseekersDesc]`.
- Arguments are parenthesised: script keys in single quotes, other values bare, multiple arguments comma-separated.
- Global functions need no data type; everything else requires the correct data type in scope.
- `CFixedValue` is a 64-bit signed fixed-point number with 5 decimals; range ±92233720368547.75807.
- Names starting with `Access` are const; `Get` is non-const.

Regenerate the type and function lists with `dump_data_types` (`DumpDataTypes`).

## Flags and Coats of Arms

**Folder:** `main_menu/common/flag_definitions/`

```
ENG = {
    flag_definition = {
        coa = ENG
        subject_canton = ENG
        allow_overlord_canton = yes
        coa_with_overlord_canton = ENG_subject
        priority = 1
        trigger = { ... }
    }
    flag_definition = {
        coa = ENG_nordic
        subject_canton = ENG
        allow_overlord_canton = yes
        priority = 2
        trigger = {
            coa_def_christian_trigger = yes
            coa_def_nordic_trigger = yes
        }
    }
}
```

Resolution rules:
- A country's tag names its flag definition list. The `DEFAULT` list is always included.
- The valid definition with the highest `priority` whose `trigger` passes is used.
- With no list, the game searches for a coat of arms whose key equals the tag, then generates one randomly.
- `TAG_REVOLT` defines the rebel flag for that tag automatically.
- `allow_revolutionary_indicator`, `revolutionary_canton` control the revolutionary overlay (not currently in use).
- Flag definition triggers have three states (existing country, releasing a country, forming a country) with different saved scopes.
- `canton` mechanics: `subject_canton` is applied to this country's subjects; `allow_overlord_canton` and `coa_with_overlord_canton` place an overlord canton; `overlord_canton_offset` and `overlord_canton_scale` position it.

Coat of arms use `pattern`, `emblem`, `sub` layers, colour palettes in `common/named_colors/`, and coat-of-arms templates. Colours are also used by unit models; changing a colour definition changes both.

## Fonts, Models, Graphical Assets, and Audio

The EU5 wiki has no `Font modding`, `Model modding`, `Graphical asset modding`, `Music modding`, `Sound modding`, or `AI modding` pages yet. Treat the following as observed practice, not documented contract:

- **Fonts**: font assets are declared in `.asset` files under the `gui`/`gfx` tree; new font entries require matching `.ttf`/`.otf` and asset definitions. There is no documented mod-facing font override mechanism — verify in-game.
- **3D models**: export with the **Clausewitz Maya Exporter** (Paradox forums). Model locators live in `gfx/map/map_objects/`.
- **Graphical assets**: `.dds` textures, `.asset` definitions, and sprite/icon paths must match the define-driven directories (`*_ICON_PATH` defines). The community repo `Europa-Universalis-5-Modding-Co-op/graphical-assets` is the shared asset source.
- **Music and sound**: audio assets are referenced through `.asset` definitions. There is no wiki page; read vanilla `.asset` files before inventing paths.
- **Input actions**: defined with `input_action` entries and scancodes (see the wiki `Input action` page for the full scancode list). The GUI property `use_global_input_instance` was removed in 1.4; stale copies of upstream UI files may still contain it. A zoom/scroll widget copied from an older mod must omit it.

## Practical Rules

- Every displayed string must come from a localisation key. Raw keys render as-is and are flagged in the log.
- Keep the BOM when editing `.yml` files.
- Do not duplicate a key across files in the same language: the runtime reports duplicates, and the winner depends on load order, not on intent.
- GUI `type` and `template` definitions are last-mod-wins by playlist position; filename prefixes do not help.
- Whole-window `.gui` replacement is the only way to change existing windows; copy the current vanilla or the final downstream owner's file, never an outdated snapshot.