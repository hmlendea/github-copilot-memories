# UI and Art

Civ5 UI is declarative XML (`Context` trees) plus imperative Lua that manipulates the resulting controls. XML defines structure and appearance; every behaviour is registered in Lua with `RegisterCallback`.

```xml
<Context Name="MyModPanel">
    <Container ID="RootContainer" Anchor="L,T" Size="400,300" Offset="100,100" Hidden="0">
        <Label ID="Title" String="[COLOR_POSITIVE_TEXT]MyMod[ENDCOLOR]" Font="TwCenMT20" />
        <Button ID="ActionButton" Anchor="L,T" Offset="10,10" Size="120,40"
                Texture="Art/MyButton.dds" />
    </Container>
</Context>
```

```lua
local function OnActionClicked()
    print("MyMod: button clicked")
end

Controls.ActionButton:RegisterCallback(Mouse.eLClick, OnActionClicked)
```

`Mouse.eLClick`, `Mouse.eRClick`, and the other `Mouse` enum members are the event constants passed to `RegisterCallback`. Register from the context's own script scope; a renamed control fails at the registration line, not at click time.

## Context Rules

- The root element is `<Context Name="...">`. Every ID'd control appears in `Controls.<Id>` in that file's Lua scope; controls without an `ID` cannot be reached from Lua.
- `<LuaContext FileName="..." ID="..."/>` nests another context file as a control of this one. Children contexts see their parent's instances, but globals are isolated per context; `LuaEvents` is the only supported cross-context channel.
- One global Lua object, `ContextPtr`, belongs to the current context. `ContextPtr:SetHide`, `ContextPtr:SetUpdate`, and the other context methods operate on the whole tree.
- `Instance` blocks are re-usable control templates for `InstanceManager`; they are not rendered until instanced.
- Contexts are isolation scopes for API objects too: the same `Player` wrapped in two contexts compares unequal, although primitive getters agree. Compare ids, not objects, across contexts.

## Registration

Declarative pointing:

```xml
<EntryPoint type="InGameUIAddin" file="UI/MyModPanel.xml">
    <Name>MyModPanel</Name>
    <Description>My mod panel</Description>
</EntryPoint>
```

Pointing at XML loads that UI context at game start. Pointing at `.lua` loads Lua in the shared context with `ContextPtr` available but no dedicated UI tree, so a `.lua`-only addin is for gameplay logic and for message popups raised through `Events.SerialEventGameMessagePopup` — not for new windows.

The `InGameUIAddin` pattern means **whole-file replacement** when it targets a vanilla context file: two mods doing so conflict, and only the last loaded wins. Community registration libraries (custom notifications, minimap overlays, summary bar, diplo corner) exist exactly to add without replacing; prefer them. A new, uniquely named context file of your own does not conflict with anything.

## Common UI Properties

Civ5 UI attributes follow an olive-drab naming style (`Anchor`, `Offset`, `Size`, `ConsumeMouseButton`, `Hidden`, `Texture`, `Font`, `ColorSet`, `FontStyle`, `Void1`, `Void2`, `AnimSpeed`, `AnimationCallback`). Callback function names in Lua match the control's registered signature exactly; mismatched names silently do nothing rather than erroring.

Fonts are limited to `TwCenMT14`/`16`/`18`/`20`/`22`/`24` in common vanilla usage, with styles `Base`, `Shadow`, `SoftShadow`, `Stroke`.

## Markup and Icons in Text

Text keys and UI strings accept the documented markup:

| Markup | Effect |
|--------|--------|
| `[NEWLINE]` | line break |
| `[TAB]` | tab |
| `[SPACE]` | space |
| `[COLOR_RED]` / `[ENDCOLOR]` | colored span (`COLOR_POSITIVE_TEXT`, `COLOR_NEGATIVE_TEXT`, `COLOR_YIELD_GOLD`, `COLOR_PLAYER_ORANGE`, …) |
| `[ICON_BULLET]`, `[ICON_FOOD]`, `[ICON_GOLD]`, `[ICON_UNIT_INFANTRY]` | 22×22 px icons from `IconFontMapping` |
| `[LINK=IMPROVEMENT_TRADING_POST]text[/LINK]` | Civilopedia entry link |
| `{1_Key}` / `{1_Key[2]}` | insertion, or a specific form of a multi-form text row |
| `{1 ^ 'feminine:trait_three'}` | insert the form matching a gender |
| `{1:plural 1?one; other?many;}` | plurals |
| `{1_Num}` / `{1_Num:number}` | engine-supplied numeric substitution |

Markup is square-bracketed and applies in XML and Lua alike, including mod descriptions. Gender/plural selection requires the referenced row to declare `<Gender>`/`<Plurality>`; a plain key with no forms cannot be pluralised, and a number that reaches the string as bare text (`{1_Num}`) always resolves to the first plural case. Details in `references/localisation.md`.

## Art Pipeline

| Layer | Format | Convention |
|-------|--------|------------|
| Building / unit / resource / wonder icons | `.dds`, uncompressed or DXT5 alpha, mipmaps off | named `<Mod>_<Atlas>_<Size>.dds` |
| Civilization colour atlas | `.dds` | `<Mod>_COLOR_ATLAS` |
| Civilization emblem (alpha) atlas | `.dds` | `<Mod>_ALPHA_ATLAS` |
| Map preview image | `.dds` | `Map<Mod>360x410.dds` |
| Dawn of Man splash | `.dds` | `DOM_<Mod>.dds` |
| Unit art | `.dds` + `.fxsxml` + `.gr2` (+ `_sref.dds`) | Nexus pipeline; whole-table replacement |

Table-level replacement means `UnitMemberArtInfos` and `UnitArtInfos` are replaced wholesale, so two unit-art mods conflict; this is why the overwhelming majority of mod civilizations ship a 2D leader screen plus an existing 3D model.

## Model Limitations

- **No audio can be added.** A mod cannot ship its own sound files; only asset names the engine already declares can be referenced, so a custom leader has no voice and a custom unit no unique sound.
- **3D leader scenes are effectively closed.** They use a proprietary format with no public reader or writer tooling, so a new animated leader screen is not achievable; a 2D leader screen is the supported outcome.
- Terrain and plot changes that alter the 3D mesh do not redraw until the game is reloaded; there is no runtime terraforming.
- No hotkeys can be added from a mod.
- UI modularity is weak: most UI mods must replace a whole vanilla Lua/XML file, so only one such mod can win. Use the community registration libraries (custom notifications, minimap overlays, summary bar, diplo corner) to add entries without replacing a file.
- A `PlayerColor` row must exist before any `Civilizations.DefaultPlayerColor` names it, or the civilization is unusable.