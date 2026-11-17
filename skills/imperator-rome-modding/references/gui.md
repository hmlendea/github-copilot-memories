# GUI and Graphics

## What Is and Is Not Moddable

Possible: restyle the interface, make windows movable/resizable, add or remove elements, add buttons, surface more scripted data.

Not possible: new hotkeys (only reuse existing ones), two windows visible at once (e.g. Treasury and Trade), and showing data from one window in another unless the developers pre-configured it.

Any UI change disables achievements — players could otherwise cheat through the UI.

## Files and Tooling

- Layout: `gui/*.gui` (HTML-like), textures `gfx/**/*.dds`.
- Templates live in `gui/shared/standard.gui` and `gui/defaults.gui`. Requiring `defaults.gui` in your mod creates cross-mod conflicts — copy individual elements instead.
- Launch with `-debug_mode -develop` for the console and the GUI editor.
- `reload gui` reloads `.gui` changes; `reload texture` reloads `.dds` changes. Both are noisy — mute the game when iterating.
- `.dds` authoring: Photoshop + Intel plugin, GIMP + DDS plugin, or Paint.NET 4.2.2+. Export as **alpha, no compression**.
- Debug mode changes the checksum; never load an ironman save with it.

## GUI Editor

Open with `Ctrl+F8`, through **2D Tools → GUI Editor** in the console, or by typing `gui_editor`. It may freeze on first load.

- **Edit mode** (hotkey `E`) behaves like a browser inspector: game input is disabled, elements become selectable.
- `L` toggles all element borders; the wheel cycles elements; **Show Hierarchy** narrows the view.
- Right mouse drag moves the selected element. `Ctrl+Z`/`Ctrl+Y` undo/redo. `Ctrl+S` writes the `.gui`.
- Windows: **UI Components** (drag-in palette from `standard.gui`/`defaults.gui`), **Registered Data Types** (available data functions; the corner button or `DumpDataTypes` writes `data_types.log`).

Guardrails:

- **Confirm which `.gui` is selected** (shown in yellow in the Outliner). If the file is not in your mod, the editor writes into the **game files**. Recover with Steam → Properties → Local Files → Verify Integrity.
- A properties header starting `Type:` marks a **template**; editing it changes every instance. Do not touch it unless intended.
- Manual text editing and using the editor are mutually exclusive in practice: manual edits frequently crash the editor.
- Cannot copy elements with their properties, and cannot add working `onclick` handlers in the editor.

## Layout Basics

Every element is `element = { ... }` with children nested. Closing brace must align with the opening line's column. Order in the file determines draw order: later elements draw on top. Child elements are clipped by their parent.

`Use "outside parent"` in the Outliner to highlight elements that overflow their parent — the usual cause of half-clickable buttons.

```
icon = {
    using = icon_popularity
    scale = 0.7
}
```

Common properties: `name`, `position = { x y }`, `size = { w h }`, `visible`, `enabled`, `scale`, `texture`, `spriteType`, `spriteborder`, `font`, `fontsize`, `fontcolor`, `autoresize`, `widgetanchor`, `tooltip`, `datacontext`, `onclick`, `text`, `using`, `blockoverride`.

Containers used by vanilla: `window`, `widget`, `container`, `hbox`, `vbox`, `flowcontainer`, `icon`, `textbox`, `button`, `scrollarea`/data lists.

A `flowcontainer` ignores child positions and orders them automatically — add spacing with an empty `widget` and an explicit width.

## Data Functions

Each window exposes its own function set (see `data_types.log`). A function from one window does not work in another; start with the window's promote, e.g. `InGameTopbar.`, `ProvinceWindow.`, `CharacterWindow.`, `DiplomaticView.`, `ViewPopsWindow.`, `GovernmentView.`, `Player`.

Functions chain: `[ViewPopsWindow.GetProvince.GetPopActivity('growing_pop').GetPop.GetCulture.GetName]`.

Global promotes usable anywhere: `Player`, `GetChristianDateString`, `SCOPE`, `GuiScope`, `ScriptedGui`, `PdxGuiWidget`, and comparison helpers such as `GreaterThanInt32`, `Not`.

Templates use `datamodel` / `datacontext` to establish the scope for all children:

```
datamodel = "[GovernmentView.GetOfficeHolders]"
...
text = "[OfficeHolderItem.GetName]"
```

Numbers: `|0`, `|1`, `|2` set displayed decimals and **truncate** rather than round. `|Y`, `|G`, `|R` apply colour codes; `|+=2` formats with a sign.

### Common snippets

```
# value of a numeric variable on the currently selected province
text = "[ProvinceWindow.GetProvince.MakeScope.Var('religious_prestige').GetValue|0]"

# variable on the player country, usable in any window
text = "[Player.MakeScope.Var('religious_centralization').GetValue|0]"

# script value
text = "[GuiScope.SetRoot(Player.MakeScope).ScriptValue('tribal_unity')|0]"

# flag test on a numeric variable
visible = "[GreaterThanInt32(ProvinceWindow.GetProvince.MakeScope.Var('has_ships_in_port').GetValue, 1)]"

# date in Gregorian form (vanilla uses CURRENT_DATE -> GetDat...)
text = "[GetChristianDateString]"
```

## Scripted GUIs

A scripted GUI is effectively a hidden event fired from the UI. Files live in `common/scripted_guis/*.txt` and **cannot be reloaded in-game** — restart after editing.

```
gui_name = {
    scope = country            # root scope targeted by the effects
    saved_scopes = { gifter }  # additional named targets

    is_shown = { }             # when is it visible
    ai_is_valid = { }          # is the AI allowed to use it
    is_valid = { }             # when may the player use it

    effect = {
        custom_tooltip = "KEY"
        hidden_effect = { }    # excluded from the built tooltip
    }
}
```

Binding in `.gui`:

```
datacontext = "[GetScriptedGui('gui_name')]"
onclick     = "[ScriptedGui.Execute( GuiScope.SetRoot( Player.MakeScope ).End )]"
visible     = "[ScriptedGui.IsShown( GuiScope.SetRoot( Player.MakeScope ).End )]"
enabled     = "[ScriptedGui.IsValid( GuiScope.SetRoot( ProvinceWindow.GetState.MakeScope ).End )]"
tooltip     = "[ScriptedGui.BuildTooltip( GuiScope.SetRoot( CharacterWindow.GetCharacter.MakeScope ).AddScope('player', Player.MakeScope ).End )]"
```

Whitespace rule: never put a space before a dot or an opening parenthesis — `Execute(` is valid, `Execute (` is not.

Example with a saved scope (gift gold to the diplomatic target, paid by the player):

```
gift_button = {
    scope = country
    saved_scopes = { gifter }

    ai_is_valid = { always = no }

    is_valid = { scope:gifter = { treasury > 100 } }

    effect = {
        add_treasury = 100
        scope:gifter = { add_treasury = -100 }
    }
}
```

```
onclick = "[ScriptedGui.Execute( GuiScope.SetRoot( DiplomaticView.GetTargetCountry.MakeScope ).AddScope('gifter', Player.MakeScope ).End )]"
enabled = "[ScriptedGui.IsValid( GuiScope.SetRoot( DiplomaticView.GetTargetCountry.MakeScope ).AddScope('gifter', Player.MakeScope ).End )]"
```

A scripted GUI may contain only `scope` and `is_shown` when it exists purely to hide or reveal elements.

Scripted-GUI tooltips can reference variables and saved scopes from localisation:

```
TOTAL_PRESTIGE_DISPLAY:0 "[SCOPE.sP('target_religion').MakeScope.Var('total_prestige').GetValue|0]"
REL_PRESTIGE_CITIZEN_TT:0 "Citizen: #G +[SCOPE.GetRootScope.GetProvince.MakeScope.Var('citizen_num').GetValue|2]#!"
[ScriptedGui.BuildTooltip(...)] used as `text = "1. [ScriptedGui.BuildTooltip(...)]"`
```

## Toggles Without Scripted GUIs

`PdxGuiWidget` hides and reveals named elements by walking parents:

```
container = {
  button = {
    name = "show submenu"
    onclick = "[PdxGuiWidget.AccessParent.FindChild('submenu').Show]"
    onclick = "[PdxGuiWidget.AccessParent.FindChild('hide submenu').Show]"
    onclick = "[PdxGuiWidget.Hide]"
  }
  button = {
    name = "hide submenu"
    visible = no
    onclick = "[PdxGuiWidget.AccessParent.FindChild('submenu').Hide]"
    onclick = "[PdxGuiWidget.AccessParent.FindChild('show submenu').Show]"
    onclick = "[PdxGuiWidget.Hide]"
  }
  widget = { name = "submenu" visible = no }
}
```

Walk further with repeated `.AccessParent`. This method is not persisted across saves, and deep hierarchies require long `AccessParent` chains; prefer scripted GUIs for persisted toggles.

## Data Lists

A GUI list is backed by a script variable list:

1. Create and fill the variable list in script **before** the window opens (a scripted GUI is a convenient trigger point).
2. Render it with `GetList` in the `.gui`.
3. Clear the list when the window closes or the data becomes stale, again from script.

## Graphics

- Textures: `.dds` in `gfx/`, alpha, no compression.
- Fonts, particles, shaders, and 3D unit models are separate modding domains with their own conventions; the Clausewitz Maya Exporter produces unit models.
- Coat of arms art lives in `gfx/coat_of_arms/` (see `setup-and-entities.md`).