# UI and Art

Civ6 UI is XML layout plus a paired Lua script loaded into a named *context*. Art is DDS icon atlases registered through `IconTextureAtlases`/`IconDefinitions`, and 3D models authored in the Asset Editor.

## Contexts and Files

`AddUserInterfaces` loads a UI XML file; the XML names its Lua in a `Context` element, and that Lua must be in the mod's file set (`ImportFiles` and `<Files>`) because the context loads it by path.

```xml
<!-- MyModPanel.xml -->
<Context Name="MyModPanel">
  <Instance Name="MyModPanelInstance">
    <Container ID="Root" Size="300,120">
      <Label Anchor="L,T" Offset="0,0" String="LOC_MYMOD_PANEL_TITLE"/>
      <Button Anchor="L,T" Offset="0,30" ID="MyModButton" Text="LOC_MYMOD_BUTTON"/>
    </Container>
  </Instance>
  <LuaContext Name="MyModPanel" FileName="MyModPanel"/>
</Context>
```

```lua
-- MyModPanel.lua
local m_Root = Controls.Root        -- resolves inside the context
local m_Button = Controls.MyModButton
m_Button:RegisterCallback(Mouse.eLClick, function() print("clicked") end)

function OnContextInitialized()
    m_Root:SetHide(false)
end
```

- `Controls` resolves element ids inside the current context; `ContextPtr` is available for nested contexts and popups.
- `AddUserInterfaces` contexts used in practice: `InGame` and `FrontEnd`. A file needed in both must be listed in `FrontEndActions` and `InGameActions`; a file listing gameplay managers under `FrontEnd` fails at the main menu.
- `ReplaceUIScript` replaces a vanilla context's Lua wholesale:

```xml
<ReplaceUIScript id="MyReplace">
  <Properties>
    <LoadOrder>99999</LoadOrder>
    <LuaContext>ReportsList</LuaContext>
    <LuaReplace>MyReportsList.lua</LuaReplace>
  </Properties>
</ReplaceUIScript>
```

Two mods cannot both replace the same context; `LoadOrder` decides the winner. Prefer adding a control or hooking a `LuaEvents` callback over replacing a large vanilla file.

## Art Pipeline Overview

| Art class | Files | Tooling |
|-----------|-------|---------|
| 2D icons | `.dds` atlases + `IconTextureAtlases`/`IconDefinitions` XML in an `UpdateIcons` action | Any DDS-capable exporter, then SQL/XML |
| Colours | `GameInfo` XML with `<Colors>`/`<PlayerColors>` rows | none — plain XML in an `UpdateColors` action |
| Art defines | `.artdef` — `Civilizations`, `Leaders`, `FallbackLeaders`, `Cultures`, `Units`, `Overlay`, `StrategicView`, `Landmarks`, `Buildings`, `Improvements` | Asset Editor |
| Cooked sources | `.xlp` (art definition lists), `.ast`, `.geo`/`.fgx`/`.wig` geometry, `.mat` materials | Asset Editor and the shipped exporters |
| Cooked output | `Cooked/ArtDefs/*.artdef`, `.blp` packages, `.dep` dependency descriptor | Pantry build |
| Art package registration | one `.dep` per mod, loaded with `UpdateArt` | Asset Editor |
| Audio | Wwise `.bnk` bank + `.wem` events + `.ini` listing, `Platforms/Windows/Audio/` | Wwise, loaded with `UpdateAudio` |

A `.dep` is plain XML describing which art libraries the mod consumes and which `.artdef` files it provides:

```xml
<AssetObjects..GameDependencyData>
  <ID><name text="MyMod"/><id text="MOD-GUID"/></ID>
  <SystemDependencies>
    <Element>
      <ConsumerName text="Units"/>
      <ArtDefDependencyPaths>
        <Element text="Units.artdef"/>
        <Element text="Cultures.artdef"/>
      </ArtDefDependencyPaths>
      <LibraryDependencies>
        <Element text="Unit"/>
        <Element text="VFX"/>
        <Element text="Light"/>
      </LibraryDependencies>
      <LoadsLibraries>true</LoadsLibraries>
    </Element>
  </SystemDependencies>
</AssetObjects..GameDependencyData>
```

The `.dep` name, the `ID/name`, the art-def paths, and the `Files` list must all agree with the deployed folder contents; a missing `.dep` entry means the object loads but renders with the fallback art.

Without the *Development Assets* pack, ModBuddy fails with `The "GeneratePantryPaths" task was not given a value for the required parameter "AssetsPath"`.

## Icon Atlases and Definitions

```xml
<!-- Icons/MyMod_Icons.xml, loaded with UpdateIcons -->
<GameInfo>
  <IconTextureAtlases>
    <Row Name="ICON_ATLAS_MYMOD_BUILDINGS" IconSize="32"  IconsPerRow="8" IconsPerColumn="8" Filename="MyMod_Buildings32.dds"/>
    <Row Name="ICON_ATLAS_MYMOD_BUILDINGS" IconSize="50"  IconsPerRow="8" IconsPerColumn="8" Filename="MyMod_Buildings50.dds"/>
    <Row Name="ICON_ATLAS_MYMOD_BUILDINGS" IconSize="256" IconsPerRow="8" IconsPerColumn="8" Filename="MyMod_Buildings256.dds"/>
  </IconTextureAtlases>
  <IconDefinitions>
    <Row Name="ICON_BUILDING_MYMOD_LIBRARY" Atlas="ICON_ATLAS_MYMOD_BUILDINGS" Index="0"/>
  </IconDefinitions>
</GameInfo>
```

- One `IconTextureAtlases` row per (atlas, size). Supply every size the UI asks for — 32, 38, 50, 80, 128, 256 in vanilla — because a missing size renders an empty or fallback icon.
- `Index` is the cell within the atlas grid, row-major, and must match the position of the icon in the DDS.
- The DDS files go through `ImportFiles`; the XML goes through `UpdateIcons`.
- Icon names follow the game's convention (`ICON_BUILDING_*`, `ICON_UNIT_*`, `ICON_TECH_*`, `ICON_CIVILIZATION_*`, `ICON_DISTRICT_*`); the content row's `Name`/`Description` keys do not need an icon row, but the UI frequently looks one up by convention.
- For icons drawn as text markup (`[ICON_Faith]`, `[ICON_Gold]`), a mod can add font icons by importing a font atlas DDS and registering it with `UpdateIcons` as vanilla does.

## 3D Models and Improvements

Adding a model-backed object means: build the geometry, define it in `.artdef` files, run the Asset Editor's Pantry/cook step, and reference the result from the object's art define. Practical guidance that holds across patches:
- Start by cloning a vanilla `.artdef` entry set for the closest object (a monument-like building, a farm-like improvement) and editing the asset name and attachments.
- The `.ast`, `.fgx`, `.geo`, and `.wig` files must be generated by the shipped exporter versions; a mismatched exporter produces a model that loads but renders invisible or untextured.
- Leader scenes reference `.blp` packages under `Platforms/Windows/BLPs/` (for example `leaders/leader_<name>.blp`, `UI_LeaderScenes.blp`, `light_rigs.blp`); cloning a vanilla set and swapping the texture is the realistic path.
- Improvement placement rules are data (`Improvements` and its association tables), while the visual is art; a missing art define leaves a functional but invisible improvement.
- Leader art is the most expensive item in the pipeline. Reuse a vanilla `Leaders.SceneLayers` value (a numeric layer count) and accept the fallback leader for an initial release.
- Keep the `Cooked/` output folder in the project; ModBuddy needs it for the Pantry build, and the deployed mod must contain `Cooked/ArtDefs/` plus the `.dep`.
- Player and civilization colours are cheap to add and easy to forget: `UpdateColors` with `Colors`/`PlayerColors` rows, otherwise the civ renders with placeholder colours.

## Map and Scenario Content
- The WorldBuilder (part of the SDK) produces `.Civ6Map` files containing the plot and player data; ship them through the map action in the SDK's own starter template rather than guessing the action name. Community generators write the same format outside the SDK.
- A scenario's setup lives in the map plus the `Players`/`PlayerItems`-style tables; verify the exact table names against a vanilla scenario.
- Maps are the content type with the least art dependency; no model pipeline is required.

## Verification Steps for UI and Art Work

1. Delete `Cache/`, launch, and confirm each action ran in `modding.log`.
2. Confirm no XML/SQL error in `Database.log` for the icon XML.
3. Confirm the icon names appear in `DebugGameplay.sqlite`:

```sql
SELECT * FROM IconTextureAtlases WHERE Name LIKE '%MYMOD%';
SELECT * FROM IconDefinitions WHERE Name LIKE '%MYMOD%';
```

4. In game, open the screen that shows the icon at each size (build queue, city panel, Civilopedia) — a missing size shows only at one of them.
5. For UI: `Lua.log` shows a load error if the context's Lua is not imported; a `nil` `Controls.X` is the usual symptom of an id typo.
6. For models: check the art define is present and the cooked assets are in the deployed mod folder under `Cooked/`.