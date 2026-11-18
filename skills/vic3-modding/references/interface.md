# Interface: GUI Script, Templates, Types, Scripted Widgets, and Scripted GUIs

The Victoria 3 interface is written in a bespoke markup language called **GUIscript** (the community name; it is not an official term). It lives in `gui/` in the game and in `<mod>/gui/` in a mod. It is **not** PDXscript: no effects, no triggers, no scopes — just widget trees whose properties are strings evaluated by the GUI scripting runtime.

Reference: `Interface_modding`, `Data_types` (GUI script), `Scripted_gui`, `List of GUI script functions`, and the in-console `DumpDataTypes` dump for the installed build.

## Files and Loading

- Source folders: `game/gui/` (vanilla) and `jomini/gui/` (engine framework).
- A mod's `gui/` mirrors these paths. Files are plain text and can be edited with any editor.
- `.gui` files hotload every time they are saved while `-debug_mode` is active — no restart.
- `common/scripted_guis/*.txt` is **not** hotloaded. Any change there requires a restart.
- Related art: `.dds` textures in `gfx/`. `.png` is accepted by the engine in most places but is less efficient. Compressed DDS resolutions must be divisible by 4.

## Contexts, Promotes, and Functions

GUI script runs against a **context** (a data type, analogous to a PDXscript scope). Two operations navigate contexts:

- **Promote** — returns a game object, e.g. `Country.GetCapital` promotes a `Country` context to a `State` context.
- **Function** — returns a number, string, or boolean, e.g. `Country.GetArmyPowerProjection`.

Everything is PascalCase, inside square brackets, dot-chained:

```
[GetPlayer.GetCountry.GetCapital.GetName]
[GetScriptedGui('my_gui').IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).End)]
```

Arguments are parenthesised and comma-separated. Script objects are single-quoted; nested function results are not.

Const vs non-const: `Access*` functions and promotes operate on and return `const` types; `Get*` functions and promotes return non-const types and require a non-const receiver. `GetTechnology('key')` is a documented exception that returns a const.

## Templates and Types

A **template** is a named set of properties and widgets copied into the caller. A **type** is a widget or container that can itself be extended and have named `block` sections overridden.

```
template my_wide_panel {
    size = { 100% 100% }
}

types my_types {
    type my_base_panel = widget {
        block "frame" {
            background = { texture = "gfx/interface/panels/bg.dds" }
        }
    }
    type my_dark_panel = my_base_panel {
        blockoverride "frame" {
            background = { texture = "gfx/interface/panels/bg_dark.dds" }
        }
    }
}

widget = {
    using = my_wide_panel
    my_dark_panel = {
        blockoverride "frame" { }
    }
}
```

- `using = <template>` applies a template.
- Any type can be used as a widget name inside another widget.
- `blockoverride "<block>"` replaces a named block; define `block "<name>"` in the base type to expose it.

### First-loaded-wins rule

GUI `type` and `template` definitions are **first loaded wins** — they cannot be overridden by a later file. `types` containers themselves have no overriding logic and may be repeated freely. To override a vanilla type or template, ship a file whose name sorts **before** the vanilla one (e.g. `00_my_overrides.gui`).

## Core Widgets

| Widget | Purpose |
|--------|---------|
| `widget` | Generic container; layout is manual or via a child layout widget |
| `container` | Container with `layoutpolicy_horizontal` / `layoutpolicy_vertical` |
| `vbox` / `hbox` | Vertical / horizontal stack with margins and expanding children |
| `flowcontainer` | Wraps children when the row or column fills |
| `fixedgridbox` | Fixed `slotsize` grid |
| `button` | Interactive widget; `onclick`, `enabled`, `visible`, `tooltip` |
| `icon` | Texture display via `sprite` |
| `text` | Localisation key or data function, with `fontsize`, `maxwidth` |
| `progressbar` | Value bar with `min` / `max` |
| `scrollbox` / `scrollarea` | Scrollable content |
| `window` / `blockwindow` / `title_window` | Frame, close button, drag behaviour |

Common properties: `size`, `position`, `parentanchor`, `margin_left/right/top/bottom`, `layoutpolicy_horizontal/vertical`, `background`, `sprite`, `texture`, `alpha`, `visible`, `enabled`, `tooltip`, `text`, `fontsize`, `onclick`, `on_finish`.

Visibility and enablement accept GUI-script expressions in square brackets, evaluated on refresh:

```
visible = "[GetVariableSystem.HasValue('mymod_open_window', 'main')]"
enabled = "[ScriptedGui.IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
```

## Animation States

A widget can declare `state = { name = <state> ... }` blocks inside an `animation_state_block` (or an animation states container) that fire on show or hide:

```
blockoverride "animation_state_block" {
    state = {
        name = _show
        on_finish = "[InformationPanelBar.ClosePanel]"
        on_finish = "[MapListPanelManager.CloseCurrentPanel]"
    }
}
```

Close competing vanilla panels in your `_show` state, otherwise your window can be overlapped or refuse focus.

## Scripted Widgets and Windows

To create a window, define a `type` based on `default_block_window` (side panel) or `fullscreen_block_window` (full-screen):

```
type my_mod_side_panel = default_block_window {
    layer = layer_ingame_menu
    visible = "[GetVariableSystem.HasValue('mymod_open_window', 'side_panel')]"

    blockoverride "animation_state_block" {
        state = {
            name = _show
            on_finish = "[InformationPanelBar.ClosePanel]"
        }
    }
}
```

Then add the panel to the HUD via a **scripted widget** payload:

```
widget = {
    name = my_mod_panels
    layer = layer_ingame_menu
    size = { 100% 100% }

    vbox = {
        parentanchor = top|left
        layoutpolicy_horizontal = expanding
        layoutpolicy_vertical = expanding
        margin_top = 85            # clear the vanilla top bar

        widget = {
            layoutpolicy_horizontal = expanding
            layoutpolicy_vertical = expanding
            hbox = {
                # your buttons living here
            }
        }
    }
}
```

Full-screen replacements need to hide vanilla HUD panels too. The community `Community Mod Framework` documents the exact panel names; without it, override the specific vanilla `.gui` host widget.

## Scripted GUIs

`common/scripted_guis/*.txt` is the bridge from GUIscript to PDXscript. It is a registry of named contexts that `gui/` code may *use*; nothing in it executes on its own.

```
give_journal_entry_scriptedgui = {
    scope = country                    # root scope the script runs in
    saved_scopes = {
        saved_gdp                      # named scopes passed from the GUI
    }

    is_shown = { always = yes }         # visibility context
    is_valid = { always = yes }         # enablement / player usability context
    ai_is_valid = { always = yes }       # AI usability context; disabled by default

    effect = {                          # runs on click
        custom_tooltip = "I am the tooltip"
        add_treasury = scope:saved_gdp
    }
}
```

Invoke from `.gui`:

```
button = {
    using = default_button_action
    datacontext = "[GetScriptedGui('give_journal_entry_scriptedgui')]"
    visible = "[ScriptedGui.IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
    enabled = "[ScriptedGui.IsValid(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
    tooltip = "[ScriptedGui.BuildTooltip(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
    onclick = "[ScriptedGui.Execute(GuiScope.SetRoot(GetPlayer.MakeScope).AddScope('saved_gdp', MakeScopeValue(GetPlayer.GetGDP)).End)]"
    text = "MY_MOD_BUTTON"
    size = { 250 50 }
}
```

You can skip `GetScriptedGui` and use a `datacontext` of your own:

```
button = {
    datacontext = "[GetScriptedGui('my_scripted_gui')]"
    visible = "[ScriptedGui.IsShown(GuiScope.SetRoot(GetPlayer.MakeScope).End)]"
}
```

`GuiScope` chain methods: `SetRoot(scope)`, `AddScope('name', scope|value)`, `AddScopeValue('name', value)`, `End`. `MakeScopeValue(x)` wraps a number; `MakeScope('x')` wraps a stored game scope.

Access to PDXscript from GUIscript is read-only apart from `ScriptedGui.Execute`.

## GUI Editor and Debugging

In debug mode:

- `gui_editor` opened the GUI editor in pre-1.9 builds; modern builds reach it from the debug menus.
- `GUI.CreateWidget` / `GUI.CreateDockable` spawn dummy widgets from `gui/test_gui.gui` (`test_window` by default), which gives a fast iteration loop with a live widget tree.
- `GUI.AnimationTimeline.LogStats` dumps animation timeline statistics.
- `Dockables.*` save, load, and manage dockable layouts — useful for inspecting a live UI tree.
- `gfx.reloadtexture` reloads textures without a restart.

Limits: you cannot add hotkeys from GUIscript, cannot display data that no data function exposes, and cannot add a new top-level window outside the existing HUD/panel host widgets. Use `INJECT`-style layering (a new panel added to an existing host) rather than replacing the host.
