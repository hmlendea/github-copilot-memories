# Interface, Fonts, and Art

## The Interface Layer

The interface is Python in `Assets\Python\Screens\` drawing into the engine's widget system. There is no declarative layout format: each screen is a script that constructs its widgets, positions them, and refreshes them from the game state. A mod that changes a screen ships the whole `Screens\*.py` file.

Shipped screens, from Modiki's `Civ4 Python` file list (BtS 3.19):

| Group | Files |
|-------|-------|
| Main loop | `CvMainInterface`, `CvScreen`, `CvScreenEnums`, `IconGrid`, `TechTree` |
| Advisors | `CvDomesticAdvisor`, `CvForeignAdvisor`, `CvExoticForeignAdvisor`, `CvMilitaryAdvisor`, `CvFinanceAdvisor`, `CvAdvisorScreen`, `CvEspionageAdvisor`, `CvCorporationAdvisor` |
| Civilopedia | `CvPediaMain`, `CvPediaScreen`, `CvPediaUnit`, `CvPediaUnitChart`, `CvPediaBuilding`, `CvPediaBonus`, `CvPediaCivic`, `CvPediaCivilization`, `CvPediaCorporation`, `CvPediaFeature`, `CvPediaHistory`, `CvPediaImprovement`, `CvPediaLeader`, `CvPediaProject`, `CvPediaPromotion`, `CvPediaReligion`, `CvPediaSpecialist`, `CvPediaTech`, `CvPediaTerrain` |
| Screens | `CvCivicsScreen`, `CvReligionScreen`, `CvSpaceShipScreen`, `CvVictoryScreen`, `CvOptionsScreen`, `CvInfoScreen`, `CvHallOfFameScreen`, `CvReplayScreen`, `CvTopCivs`, `CvDawnOfMan`, `CvDanQuayle` |
| Movies and transitions | `CvIntroMovieScreen`, `CvEraMovieScreen`, `CvVictoryMovieScreen`, `CvWonderMovieScreen`, `CvTechSplashScreen` |
| WorldBuilder | `CvWorldBuilderScreen`, `CvWorldBuilderDiplomacyScreen` |
| Other | `CvGFCScreen`, `CvDebugInfoScreen`, `CvTutorialQuestScreen`, `CvUNVictoryScreen`, `CvTechChooser` |

### Genre-interface patterns

- `CvMainInterface` is the in-game HUD: the plot list, the unit buttons, the research and culture bars, the minimap, the score table, and the end-turn button. Almost every "interface mod" is a modification of this file, which is exactly why two such mods cannot be combined.
- Screens are reached from `CvScreensInterface`, which maps an interface id to the screen module and its `showScreen`/`hideScreen`/`interfaceScreen` functions. A mod that adds a screen registers it here and in the interface-id enum in `CvScreenEnums`.
- Widget state is refreshed from `CvMainInterface.update*` functions called each frame from `onUpdate`, so a screen's drawing code must be cheap and a state lookup should be cached between refreshes.
- Input reaches the Python layer through `onKdbEvent` (keys `(eventType, key, mx, my, px, py)`) and `onMouseEvent` (mouse state plus the `interfaceConsumed` flag); the engine consumes input first and tells the handler whether the interface already handled it.
- Popups are created through `PyPopup`/`Popup.py` and routed back into `applyEvent`, which is the mechanism behind "choose an option" random events.
- `CyTranslator().getText` resolves text keys; the interface module loads its strings from the text tables rather than embedding them, which is what makes the screens translatable.

## Font Icons and `GameFont.tga`

Civ4 packs its small icons — yields, commerce, religion symbols, corporation symbols, unit-class glyphs, and the icons used inline in text — into `Assets\Res\Fonts\GameFont.tga` plus a smaller sibling `GameFont_75.tga`. The engine addresses them by index, and both sheets must agree.

- Each sheet is a fixed-resolution image holding the icon cells in a grid, and the sheets are indexed rather than searched: the engine addresses an icon purely by its index.
- The icon index is what a `Button` field or a text markup tag names. Because what is loaded is the whole sheet, **adding an icon means editing both `GameFont.tga` and `GameFont_75.tga`**, never one alone.
- The two sheets must keep the same index layout. An index that exists in `GameFont.tga` and not in `GameFont_75.tga` renders at one interface scale and mis-renders or blanks at the other.
- The shipped sheets are effectively full. Adding icons therefore means enlarging the sheet, with every index-derived consumer following it; this is why most mods reuse existing glyphs and why Modiki devotes multiple tutorials (`How To Edit GameFont.tga`, `How To Fix GameFont.tga`, `Working with GameFont.tga in Photoshop`) to the operation.
- The community tool `GameFont.tga Editor Utility` exists because a byte-level edit of the index rows and the palette is error-prone by hand.

## Art Definitions and Asset Types

Art is bound by `CIV4ArtDefines_*` files, which name paths; the engine loads the named file and nothing else. See `references/xml-reference.md` for the `Button` field's five-part comma-separated form, which is common to every art-define family.

| Asset | Format | Bound from |
|-------|--------|-----------|
| Unit model | `.nif` + `.kfm` (animation), with a `_FX` shaded variant | `Civ4ArtDefines_Unit` |
| Building model | one `.nif` per era | `Civ4ArtDefines_Building` |
| Improvement / feature / bonus / terrain mesh | `.nif`, terrain also needs its texture and `Civ4TerrainSettings` entry | the matching `Civ4ArtDefines_*` |
| Leaderhead | `.nif` models + `.kfm` animation + background + button | `Civ4ArtDefines_Leaderhead` |
| Civilization | flag and decal `.nif` | `Civ4ArtDefines_Civilization` |
| Interface art | `.dds` | `Civ4ArtDefines_Interface` |
| Buttons | a standalone `.dds`, or a cell of an atlas, or a `GameFont.tga` index | the object's `Button` field |
| Movies | `.bik`; a `Civ4ArtDefines_Movie` entry plus a `MovieDefineTag` on the object | `Civ4ArtDefines_Movie` |
| Audio | `.wav`/`.mp3`; named by an `AudioDefines` entry, referenced from `Audio2DScripts`/`Audio3DScripts` | the audio files |

Notes that determine whether an asset appears:

- **Gamebryo NIF version.** A `.nif` exported by a later NifTools than the engine's Gamebryo build fails to load; the model list in Modiki's `NifViewer Tutorial`, `3ds Max Importing/Exporting`, and `Merge Animations With Your Models` pages is built around keeping the export compatible.
- **Shaded and unshaded variants.** Civ4 uses a per-era shader path; a unit exported without its `_FX` model renders unlit and is the subject of the `Create Noshader Units from Units With Shaders` tutorial.
- **KFM animation binding.** A model with no animation file stands still; the KFM names the animation groups the engine plays.
- **An unreferenced asset is never loaded**, and a referenced path that does not exist is a missing model or a default placeholder rather than an error.
- **Button coordinates are (column, row)** into the atlas, and an out-of-range pair shifts or blanks the icon.

## Unit Art Styles

`Civ4UnitArtStyleTypeInfos.xml` (BtS) allows a civilization to render one unit class with a different model without touching `Civ4UnitInfos.xml`: each style is a list of `UNITCLASS_*` → `ART_DEF_UNIT_*` pairs, and a civilization names one via `UnitArtStyleType`. This is the supported way to give a civilization a distinctive look per class.

## DDS and Texture Conventions

- DDS is the universal texture format; the community toolchain is GIMP with the DDS plugin, DXTBmp, or Photoshop with the appropriate plugin.
- Button textures are small (typically 64×64 or 128×128) with an alpha channel; DXT compression and mipmaps must be generated, or the button renders as a solid block.
- Atlas textures are featureless grids; the object's `Button` field addresses a cell by column and row, so a reordered atlas invalidates every reference into it.

## The Interface/GUI Limits

- **No layout format, no theming layer.** Every change is a script change, and a script change is a whole-file replacement.
- **Two mods that touch the same screen cannot be combined.** The later one's file wins outright.
- **A screen's widget ids are private.** A mod that adds a widget to `CvMainInterface` must not assume the base widget ids are unchanged by another mod, and must handle its own widget being absent.
- **`onUpdate` runs every frame.** Anything costly there is a permanent frame cost.
- **The engine owns the input loop.** A Python handler sees the event after the engine has decided whether the interface consumed it.
- **The Civ4 interface is Python, unlike the expansion-era Civ5 engine's Lua**, so no Civ5 UI technique transfers.
