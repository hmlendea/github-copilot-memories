# WorldBuilder, WBS Scenarios, and Maps

## Three Separate Things

Civ4 has three unrelated map mechanisms, and conflating them causes most scenario confusion:

| Mechanism | What it is | Where it lives |
|-----------|-----------|----------------|
| WorldBuilder | An in-game editor that edits the current map and can save it as a scenario | Opened in game; results saved into the game's WorldBuilder saves |
| WBS file | The text format a WorldBuilder save uses: `.CivBeyondSwordWBSave` and its older siblings | `Saves\WorldBuilder\`, then distributed into `PublicMaps\` |
| Map script | A Python module that generates a map procedurally | `PublicMaps\`, selected from the map list |

A scenario is a map with a `BeginPlayer`/`BeginTeam` block; a map script is code. A scenario can also be produced by a map script, but the two formats do not share a file.

## The WBS Format

A WBS save is a line-oriented text file parsed by tags. The top-level sections, each a `Begin…`/`End…` pair, with Modiki's `Civ4 World Builder` reference as the source:

### `BeginGame` — the game setup

The options a player would otherwise choose on the custom-game screen: `Tutorial`, `Era`, `Speed`, `Calendar`, `Option`, `MPOption`, `ForceControl`, `Victory`, `GameTurn`, `MaxTurns`, `MaxCityElimination`, `TargetScore`, `StartYear`, `Description`, `ModPath`.

`ModPath` names the mod the scenario expects; a scenario that depends on a mod loads the mod, and a scenario whose `ModPath` is wrong loads with vanilla content.

### `BeginTeam` — one block per team

`Tech`, `ContactWithTeam`, `AtWar`, `PermanentWarPeace`, `OpenBordersWithTeam`, `DefensivePactWithTeam`, `ProjectType`, `RevealMap`. Every player must belong to a team even if alone; a scenario with a team block per player rather than per team desynchronises.

### `BeginPlayer` — one block per player

`CivDesc`, `CivShortDesc`, `LeaderName`, `CivAdjective`, `FlagDecal`, `WhiteFlag`, `LeaderType`, `CivType`, `Team`, `Handicap`, `Color`, `ArtStyle`, `PlayableCiv`, `MinorNationStatus`, `StartingGold`, `StartingX`, `StartingY`, `StateReligion`, `StartingEra`, `CivicOption`/`Civic`, `AttitudePlayer`/`AttitudeExtra`, `CityList`.

There must be one `BeginPlayer` per player in the game, and `CivType`/`LeaderType` must name `Type` strings that exist in the installed content.

### `BeginMap` — the map header

`grid width`, `grid height`, `top latitude`, `bottom latitude`, `wrap X`, `wrap Y`, `world size`, `climate`, `sealevel`, `num plots written`. `num plots written` must agree with the number of `BeginPlot` sections or the map loads partially.

### `BeginPlot` — one block per plot

This is the bulk of the file. Each plot carries `x`, `y`, `Landmark`, `ScriptData`, `isNOfRiver`/`isWOfRiver`, `RiverNSDirection`/`RiverWEDirection`, `StartingPlot`, `BonusType`, `ImprovementType`, `FeatureType`/`FeatureVariety`, `RouteType`, `TerrainType`, `PlotType`, and can nest `BeginUnit`, `BeginCity`, and `TeamReveal` blocks.

- `TerrainType` and `PlotType` are mandatory per plot; a plot with neither is a hole in the map.
- River flags are directional: a river edge is `isNOfRiver`/`isWOfRiver` on the plot plus the `RiverNSDirection`/`RiverWEDirection` that give it shape, and an inconsistent pair produces a broken river.
- `ScriptData` on a plot is free-form text that Python can read and write — the persistence slot for scenario scripting (`references/python-scripting.md`).
- Python's `onUnitSetXY`, `onPlotPicked`, and the WorldBuilder events are how a scenario's Python reacts while a WBS is loaded.

## Authoring a Scenario

1. Start the game with the intended mod and rules, then open the WorldBuilder (the standard in-game shortcut is `Ctrl+W`, and `Alt+W` in some builds; verify in the install).
2. Edit the map: terrain, features, rivers, bonus placement, improvements, routes, units, cities, players, teams, and starting plots.
3. Save from the WorldBuilder; the file lands in `Saves\WorldBuilder\` with the `.CivBeyondSwordWBSave` extension.
4. Move the file into `PublicMaps\` (with `AllowPublicMaps = 1` in the mod's ini) to ship it, or into the user directory to keep it local.
5. Hand-edit the `BeginGame` and `BeginPlayer` blocks to set `ModPath`, `PlayableCiv`, `PlayableCiv` roles, starting gold, and attitudes — the WorldBuilder sets some of these and not others.
6. Load it from the scenario list and confirm `num plots written` matches, no plot is missing a terrain, and every `CivType`/`LeaderType` resolves.

**Hand-editing a WBS is legitimate and common** — it is plain text and the community toolchain (`BMP To WorldBuilderSave Converter`, `Civ4 Save/Scenario/Map Editor`) exists to move between a bitmap and a WBS. The two failure modes are a plot count mismatch and a dangling `Type` reference, and both appear as a truncated or empty map.

## Map Scripts

A map script is a Python module in `PublicMaps\` that builds the plot types, terrain, features, and bonuses. It is *not* a `Screens` module and not a scenario. The engine calls a fixed set of module-level functions:

```python
from CvPythonExtensions import *
import CvUtil
import CvMapGeneratorUtil
from CvMapGeneratorUtil import FractalWorld, TerrainGenerator, FeatureGenerator

def getDescription():          # the name shown in the map list
def isAdvancedMap():           # 0 hides it in simple mode
def isRandomMap():             # whether it is offered as a random candidate
def getNumCustomMapOptions():  # how many option rows the setup screen shows
def getCustomMapOptionName(argsList):     # [iOption] -> TXT_KEY_
def getCustomMapOptionDescAt(argsList):   # [iOption, iSelection] -> TXT_KEY_
def getCustomMapOptionDefault(argsList):  # [iOption] -> default selection
def generatePlotTypes():       # builds the land/water grid
def generateTerrainTypes(argsList):
def addFeatures():
```

The generator classes from `CvMapGeneratorUtil` are the intended building blocks:

- `FractalWorld` / `FractalWorld`-derived classes produce the continental layout from a fractal seed and the map-size/climate/sea-level settings.
- `TerrainGenerator` turns plot types into terrain using latitude bands and the climate.
- `FeatureGenerator` places forests, jungles, flood plains, and oasis.
- `BonusGenerator` places resources; `CvMapGeneratorUtil` also exposes the terrain/feature/plot validators and the yield helpers.

`argsList` is always a list; the description functions return translated text (`CyTranslator().getText(...)`) rather than raw strings, so the option names ship as `TXT_KEY_` rows.

## WorldBuilder Python Hooks

The event manager's `_event*` handlers (`_eventCityNameBegin`, `_eventCityNameApply`, `_eventEditCityBegin`, `_eventEditCityApply`, `_eventPlaceObjectBegin`, `_eventPlaceObjectApply`, `_eventAwardTechsAndGoldBegin`, `_eventAwardTechsAndGoldApply`) are the WorldBuilder's own dialogs routed through Python. A mod that adds a WorldBuilder action wraps one of these and calls the base implementation, because the engine's own dialog is what actually performs the edit.

`CvWorldBuilderScreen.py` and `CvWorldBuilderDiplomacyScreen.py` are the WorldBuilder's Python side; `CvWBInterface`, `CvWBDesc`, and `CvWBPopups` are the entry point, the WBS description parser, and the popups. The parser is the reference for how a WBS is read if a mod must read one itself.

## Map and Scenario Distribution

- A shipped scenario goes in `PublicMaps\` (with the mod's ini allowing public maps) or in the mod's own folder with the `ModPath` pointing at the mod.
- A scenario that relies on a mod's `Type` strings must set `ModPath`; without it the content references dangle and the scenario loads with missing objects.
- A scenario saved by a modded game can be loaded by a vanilla game if it references no modded content, and vice versa; the `ModPath` field is the only guard, and it is advisory.
- A map script is available to every game a player starts, not only to the mod that shipped it, if it is installed in the shared `PublicMaps\`.
