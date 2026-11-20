# Python Scripting

## What Python Is For

Civ4 embeds a Python 2 interpreter. The engine calls into it at fixed points, and the mod's Python replaces the shipped modules. Python is the interface and reaction layer: screens, advisors, popups, random-event consequences, and the `CvGameUtils` answers the engine consults when the SDK calls them. It is not the place for per-unit or per-turn arithmetic — the shipped documentation says plainly that a computation heavy enough to need a real development environment belongs in the SDK instead.

Three properties constrain everything written here:

1. **Python 2.** Integer division truncates, `print` is a statement, strings are bytes unless declared as `unicode(...)`, and there is no `logging`, no f-string, and no guaranteed dict order.
2. **A whole-file replacement model.** A mod ships entire `.py` files that shadow the base ones. Two mods that both ship `CvEventManager.py` cannot be combined.
3. **The engine surface is `CvPythonExtensions`.** Everything the interpreter can reach is exposed through that SWIG module: `CyGame`, `CyPlayer`, `CyUnit`, `CyPlot`, `CyCity`, `CyTeam`, `CyArea`, `CyMap`, `CyGlobalContext`, `CyMessageControl`, `CyTranslator`, and the info interfaces (`CyInfoInterface1`…`3`, `CyEnumsInterface`).

## Files and Folders

`Assets\Python\`:

| Path | Contents |
|------|----------|
| `CvEventManager.py` | The event dispatcher — the single most important file for a mod that reacts to the game |
| `CvGameUtils.py` | The callback answers the engine asks for (can-train, can-build, can-construct, and the rest) |
| `CvUtil.py`, `PyHelpers.py`, `DomPyHelpers.py` | Utility modules: logging, popups, helpers around the `Cy*` objects |
| `CvAdvisorUtils.py`, `CvDiplomacy.py`, `CvCameraControls.py`, `CvScreenUtils.py`, `CvDefineEditor.py`, `CvMagGeneratorUtil.py`, `CvPerfTest.py`, `CvQuestManager.py`, `CvDebugTools.py` | Supporting modules |
| `pyHelper\` , `pyUnit\`, `pyWB\` | Popup, unit-controller, and WorldBuilder helper packages |
| `EntryPoints\` | The modules the engine invokes by name (see below) |
| `Screens\` | The interface screens (see `references/interface-and-art.md`) |
| `PitBoss\` | Pitboss server administration |
| `_DebugTools\` | Debug-only helpers |
| `System\` | The bundled Python standard library and compiled modules; treated as read-only |

`EntryPoints\` modules are the engine's named entry points: `CvEventInterface` (instantiates and routes to `CvEventManager`), `CvGameInterface` (routes to `CvGameUtils`), `CvScreensInterface`, `CvAppInterface`, `CvDebugInterface`, `CvDiplomacyInterface`, `CvRandomEventInterface`, `CvPopupInterface`, `CvMapScriptInterface`, `CvOptionScreenCallbackInterface`, `CvUnitControlInterface`, `CvWBInterface`, `CvScreenUtilsInterface`, `CvTranslator`, `PbMain`, and their peers. A mod that wants to redirect one of these replaces the file; a mod that wants an additional module adds its own file and imports it from a replaced entry point.

## The Event Manager

`CvEventManager` holds a single instance whose `handleEvent` is the engine's `EventManager` entry point; each event name is dispatched to an `on*` method. The shipped set, from Modiki's `CvEventManager` page:

| Group | Handlers |
|-------|----------|
| Lifecycle | `onInit`, `onUpdate` (`fDeltaTime`, every frame), `onWindowActivation`, `onUnInit`, `onPreSave`, `onSaveGame`, `onLoadGame`, `onGameStart`, `onGameEnd` |
| Turns | `onBeginGameTurn`, `onEndGameTurn`, `onBeginPlayerTurn`, `onEndPlayerTurn`, `onEndTurnReady`, `onGameUpdate` |
| Teams and diplomacy | `onFirstContact`, `onChangeWar`, `onChat`, `onSetPlayerAlive`, `onPlayerChangeStateReligion`, `onPlayerGoldTrade`, `onVassalState`, `onVictory`, `onModNetMessage` |
| Units | `onUnitMove`, `onUnitSetXY`, `onUnitCreated`, `onUnitBuilt`, `onUnitKilled`, `onUnitLost`, `onUnitPromoted`, `onUnitSelected`, `onUnitRename`, `onUnitPillage`, `onUnitSpreadReligionAttempt`, `onUnitGifted`, `onUnitBuildImprovement`, `onSelectionGroupPushMission` |
| Cities | `onCityBuilt`, `onCityRazed`, `onCityAcquired`, `onCityAcquiredAndKept`, `onCityLost`, `onCultureExpansion`, `onCityGrowth`, `onCityDoTurn`, `onCityBuildingUnit`, `onCityBuildingBuilding`, `onCityRename`, `onCityHurry`, `onBuildingBuilt`, `onProjectBuilt` |
| Combat and terrain | `onCombatResult`, `onCombatLogCalc`, `onCombatLogHit`, `onImprovementBuilt`, `onImprovementDestroyed`, `onRouteBuilt`, `onPlotRevealed`, `onPlotFeatureRemoved`, `onPlotPicked`, `onNukeExplosion`, `onGotoPlotSet`, `onGoodyReceived` |
| Religion, corporations, techs, great people | `onReligionFounded`, `onReligionSpread`, `onReligionRemove`, `onCorporationFounded`, `onCorporationSpread`, `onCorporationRemove`, `onTechAcquired`, `onTechSelected`, `onGreatPersonBorn`, `onGoldenAge`, `onEndGoldenAge` |
| Input and interface | `onKdbEvent`, `onMouseEvent`, `applyEvent`, `beginEvent`, `reportEvent` |
| WorldBuilder internals | `_eventCityNameBegin`, `_eventCityNameApply`, `_eventEditCityBegin`, `_eventEditCityApply`, `_eventPlaceObjectBegin`, `_eventPlaceObjectApply`, `_eventAwardTechsAndGoldBegin`, `_eventAwardTechsAndGoldApply` |

`reportEvent` writes to the event log; `beginEvent`/`applyEvent` are the popup-driven path used by events that ask the player to choose.

A handler receives a single `argsList` tuple whose contents are event-specific — the BtS `onUnitBuilt` passes `(city, unit, player)`, `onCombatResult` passes `(winner, loser)` unit objects, `onCityDoTurn` passes `(city, player)`, `onTechAcquired` passes `(iTechType, iTeam, iPlayer, bAnnounce)`. Treat the argument list as documented per handler, not as uniform. The convention is:

```python
def onUnitBuilt(self, argsList):
	'Unit completed'
	city, unit, player = argsList
	if unit.getUnitType() == gc.getInfoTypeForString("UNIT_MYMOD_LONGBOW"):
		# ...
```

`gc` is the module-level `CyGlobalContext()` — the standard handle for `getInfoTypeForString`, `getPlayer`, the info interfaces, and the game object.

## `CvGameUtils` and the Callback Switches

`CvGameUtils` answers the questions the engine asks when it wants a mod to participate in a decision or to replace the engine's own calculation. Each is gated by a switch in `Assets\XML\PythonCallbackDefines.xml`:

| Callback group | Methods | Switch names |
|----------------|---------|--------------|
| Victory and research | `isVictoryTest`, `isVictory`, `isPlayerResearch`, `canResearch`, `cannotResearch`, `getFirstRecommendedTech`, `getSecondRecommendedTech`, `showTechChooserButton`, `skipResearchPopup` | `USE_IS_PLAYER_RESEARCH_CALLBACK`, `USE_CAN_RESEARCH_CALLBACK`, `USE_CANNOT_RESEARCH_CALLBACK`, `USE_AI_CHOOSE_TECH_CALLBACK` |
| Costs and value | `getExtraCost`, `getUnitCostMod`, `getBuildingCostMod`, `getCityFoundValue`, `getUpgradePriceOverride`, `canUpgradeAnywhere` | `USE_GET_UNIT_COST_MOD_CALLBACK`, `USE_GET_BUILDING_COST_MOD_CALLBACK`, `USE_GET_CITY_FOUND_VALUE_CALLBACK`, `USE_UNIT_UPGRADE_PRICE_CALLBACK` |
| Cities | `cannotFoundCity`, `canFoundCitiesOnWater`, `canRazeCity`, `citiesDestroyFeatures`, `canPickPlot`, `showExamineCityButton` | `USE_CANNOT_FOUND_CITY_CALLBACK`, `USE_CAN_FOUND_CITIES_ON_WATER_CALLBACK` |
| Civics, war, movement, actions | `canDoCivic`, `cannotDoCivic`, `canDeclareWar`, `unitCannotMoveInto`, `cannotHandleAction`, `cannotDoControl`, `cannotSelectionListMove`, `cannotSelectionListGameNetMessage` | `USE_CAN_DO_CIVIC_CALLBACK`, `USE_CANNOT_DO_CIVIC_CALLBACK`, `USE_CAN_DECLARE_WAR_CALLBACK`, `USE_UNIT_CANNOT_MOVE_INTO_CALLBACK`, `USE_CANNOT_HANDLE_ACTION_CALLBACK` |
| Production and creation | `canTrain`, `cannotTrain`, `canConstruct`, `cannotConstruct`, `canBuild`, `canCreate`, `cannotCreate`, `canMaintain`, `cannotMaintain`, `getRecommendedUnit`, `getRecommendedBuilding`, `isActionRecommended`, `skipProductionPopup`, `getWidgetHelp` | `USE_CAN_TRAIN_CALLBACK`, `USE_CANNOT_TRAIN_CALLBACK`, `USE_CAN_CONSTRUCT_CALLBACK`, `USE_CANNOT_CONSTRUCT_CALLBACK`, `USE_CAN_BUILD_CALLBACK` |
| Engine-internal replacement | `calculateScore`, `doGold`, `doResearch`, `doGoody`, `doGrowth`, `doProduction`, `doCulture`, `doPlotCulture`, `doReligion`, `doGreatPeople`, `doMeltdown`, `doPillageGold`, `doCityCaptureGold`, `doHolyCity`, `doHolyCityTech`, `doReviveActivePlayer`, `doCombat`, `cannotSpreadReligion`, `getConscriptUnitType`, `getExperienceNeeded`, `createBarbarianCities`, `createBarbarianUnits`, `updateColoredPlots` | `USE_DO_GROWTH_CALLBACK`, `USE_DO_CULTURE_CALLBACK`, `USE_DO_PLOT_CULTURE_CALLBACK`, `USE_DO_PRODUCTION_CALLBACK`, `USE_DO_RELIGION_CALLBACK`, `USE_DO_GREAT_PEOPLE_CALLBACK`, `USE_DO_MELTDOWN_CALLBACK`, `USE_DO_PILLAGE_GOLD_CALLBACK`, `USE_DO_COMBAT_CALLBACK`, `USE_GET_EXPERIENCE_NEEDED_CALLBACK`, `USE_CANNOT_SPREAD_RELIGION_CALLBACK`, `USE_FINISH_TEXT_CALLBACK` |
| AI replacement | `AI_chooseTech`, `AI_chooseProduction`, `AI_unitUpdate`, `AI_doWar`, `AI_doDiplo` | `USE_AI_CHOOSE_TECH_CALLBACK`, `USE_AI_CHOOSE_PRODUCTION_CALLBACK`, `USE_AI_UNIT_UPDATE_CALLBACK`, `USE_AI_DO_WAR_CALLBACK`, `USE_AI_DO_DIPLO_CALLBACK` |
| Event-manager entry switches | `onUnitSetXY`, `onUnitSelected`, `onUpdate`, `onUnitCreated`, `onUnitLost` | `USE_ON_UNIT_SET_XY_CALLBACK`, `USE_ON_UNIT_SELECTED_CALLBACK`, `USE_ON_UPDATE_CALLBACK`, `USE_ON_UNIT_CREATED_CALLBACK`, `USE_ON_UNIT_LOST_CALLBACK` |

The `do*` methods in the third group are not legality questions: switching one on **replaces** the engine's own calculation, so the mod must reimplement it. They are the most expensive category and the one that most often breaks a game subtly.

`PythonCallbackDefines.xml` holds all 41 of these switches, every one set to `0` in the shipped BtS file. The shape is:

```xml
<Civ4Defines xmlns="x-schema:CIV4GlobalDefinesSchema.xml">
  <Define>
    <DefineName>USE_CAN_TRAIN_CALLBACK</DefineName>
    <iDefineIntVal>0</iDefineIntVal>
  </Define>
</Civ4Defines>
```

**A callback that is not switched on is not called.** The mod ships its own `PythonCallbackDefines.xml` with the needed switches set to `1`, and accepts the cost: every switched-on callback is a Python call, and the reason the switches exist is that they are expensive. A `1` on a `do*` or `AI_*` switch is a far larger commitment than a `1` on a `can*` switch.

### Dispatch

The engine calls into `Assets\Python\EntryPoints\CvGameInterface.py`, whose header states that modifying the function names of that file is prohibited because the application calls the functions by name. Each function there delegates to `CvGameInterfaceFile.py`'s `GameUtils`, which by default is the shipped `CvGameUtils` class:

```python
import CvGameUtils
import CvGameInterfaceFile
normalGameUtils = CvGameInterfaceFile.GameUtils

def gameUtils():
	' replace normalGameUtils with your mod version '
	return normalGameUtils
```

The supported pattern is therefore **not** to edit the delegating functions but to point the reference at the mod's own class — the header says so explicitly ("If you create a GameUtils file, update the CvGameInterfaceFile reference to point to your new file"), and the mod can then subclass or replace the shipped `CvGameUtils` and keep the engine's call graph intact.

## The `Cy*` API

The engine surface is a set of wrapper classes, one per engine concept, with getters and setters. The interfaces a modder actually uses:

| Interface | Methods |
|-----------|---------|
| `CyGlobalContext` | `getGame`, `getMap`, `getPlayer(i)`, `getTeam(i)`, `getActivePlayer`, `getInfoTypeForString(type)`, `getInfoTypeForStringType`, the `get*Info` accessors, and the era/handicap/victory info interfaces |
| `CyGame` | Turn, era, game speed, options, `getPlayer`, `getTeam`, `setWinner`, `getCyUnit`, `getCyCity`, `getPlot`, `getSorenRandNum`, active player access, `getEspionageMission`-family accessors |
| `CyPlayer` | `isAlive`, `isHuman`, `getCivilizationType`, `getTeam`, `getCapitalCity`, `getNumCities`, `getCity(i)`, `getUnit(i)`, `getNumUnits`, `getGold`, `setGold`, `getResearchQueue`, `canResearch`, `getCurrentResearch`, `getCivics`, `getStateReligion`, `getNumBuildings`, `getEspionagePointsAgainstTeam`, and the diplomacy accessors |
| `CyUnit` | `getUnitType`, `getOwner`, `getPlot`, `setXY`, `move`, `getMoves`, `setMoves`, `getDamage`, `setDamage`, `getExperience`, `setExperience`, `getPromotionCount`, `getUnitAIType`, `isHasPromotion`, `setHasPromotion`, `getFortifyTurns`, `canMoveInto` |
| `CyCity` | `getName`, `getOwner`, `getPopulation`, `setPopulation`, `getProduction`, `setProduction`, `getYieldRate(yield)`, `getCommerceRate`, `isHasBuilding`, `getNumBuilding`, `getBuildingProduction`, `isWorkingPlot`, `getCulture`, `setCulture`, `getReligionCount`, `isHasReligion`, `isConnectedTo`, `getSpecialistCount`, `setNumRealBuilding`, `getScriptData`, `setScriptData` |
| `CyPlot` | `getX`, `getY`, `getTerrainType`, `getFeatureType`, `getBonusType`, `getImprovementType`, `getRouteType`, `getOwner`, `getTeam`, `getPlotType` (`PLOT_LAND`/`PLOT_WATER`), `isWater`, `getCity`, `getUnit`, `getNumUnits`, `setScriptData` |
| `CyTeam` | `getPlayerList`, `isAtWar`, `isHasMet`, `canDeclareWar`, `getNumMembers`, `getVassal`, `getMaster` |
| `CyArea` | `getNumTiles`, `getNumCities`, `getCity`, `getUnitsPerPlayer`, `getNumUnits`, `isWater`, and the area-yield accessors |
| `CyMessageControl` | `sendModNetMessage(iData1..iData5)` — the multiplayer hook that reaches `onModNetMessage` |
| `CyTranslator` | `getText(key, args)` — resolves a `TXT_KEY_` in the active language |
| `CyInfoInterface1/2/3` | Per-table infos reached from their type integer |
| `CyEnumsInterface` | The enumerations (`DomainTypes`, `YieldTypes`, `CommerceTypes`, `UnitCombatTypes`, and so on) as attributes |

Everything returns an integer type id for `Type` references, which is why `gc.getInfoTypeForString("UNIT_MYMOD_LONGBOW")` is the universal bridge from the XML `Type` string to the engine handle. A missing type resolves to `-1`; a `-1` passed to a getter is an invalid argument and commonly raises rather than returning `None`.

## Utility Conventions

- `CvUtil.py` is the standard logging and helper module: the community convention is `CvUtil.pyPrint(message)`, which both prints to the Python console and writes to `PythonDbg.log` when logging is enabled, and `CvUtil.convertToStr`/`PyHelpers` for safe string handling.
- `PyHelpers.py` wraps the `Cy*` objects in friendlier accessors and is imported by most large interface mods.
- The resource/shared-value pattern used by the shipped screens is a module-level dictionary plus accessor functions, e.g. `g_*` globals, because the interpreter has no persistent per-object state of its own.
- `CvTranslator().getText(key, args)` resolves text; a mod that adds text rows calls this rather than embedding displayed strings.

## Persistence

The engine gives Python two string slots: `CyGame().getScriptData()`/`setScriptData()`, and each city's and unit's `getScriptData`/`setScriptData` (the latter also surfaced in the WorldBuilder save). Everything a mod wants to survive a save must be serialised into one of these as text.

- `ScriptData` is a single string; the convention is a delimited record (`"key1=value1;key2=value2"`) reassembled on `onLoadGame`.
- The stored data belongs to the whole game, so a value another mod also writes can be clobbered. Prefix keys with the mod name.
- `onPreSave` is the last reliable point to write; `onLoadGame` is the first to read. `onGameStart` fires for a new game only.
- Data written from Python is text, so a numeric value must be parsed back with explicit error handling; a malformed record is a silent reset, not an exception at load.

## Random Events and Quests

An event's Python lives in `Assets\Python\EntryPoints\CvRandomEventInterface.py` (or the module the trigger names). The trigger's `PythonCanDo`, `PythonCanDoCity`, and `PythonCanDoUnit` functions return whether the event is eligible; the event's `PythonCallback`/`PythonHelp` run when it fires or when its help is required. Argument shapes and the quest-start/quest-complete pairing are documented in `references/content-definitions.md`; the practical rule is that these functions are looked up **by bare name in the entry-point module**, so the function must exist there even if it delegates elsewhere.

## Map Scripts

A map script is a standalone module in `PublicMaps\` — not a `Screens` file — that the engine loads when generating a map. It exposes a fixed set of module-level functions the engine calls:

```python
from CvPythonExtensions import *
import CvUtil
import CvMapGeneratorUtil
from CvMapGeneratorUtil import FractalWorld, TerrainGenerator, FeatureGenerator

def getDescription():
	return "A modified Big and Small."

def isAdvancedMap():
	return 0

def getNumCustomMapOptions():
	return 2

def getCustomMapOptionName(argsList):
	[iOption] = argsList
	option_names = { 0: "TXT_KEY_MAP_SCRIPT_CONTINENTS_SIZE" }
	return unicode(CyTranslator().getText(option_names[iOption], ()))

def getCustomMapOptionDescAt(argsList):
	[iOption, iSelection] = argsList
	# ...

def getCustomMapOptionDefault(argsList):
	[iOption] = argsList
	# ...

def isRandomMap():
	# ...

def generatePlotTypes():
	# builds and returns the plot-type grid
	# ...

def generateTerrainTypes(argsList):
	# ...

def addFeatures():
	# ...
```

`CvMapGeneratorUtil` supplies the `FractalWorld`, `TerrainGenerator`, `FeatureGenerator` and `BonusGenerator` classes the script composes; arguments arrive as lists (`[iOption]`, `[iOption, iSelection]`), and the description functions return translated text via `CyTranslator().getText`. A map script is selected from the map list, not the mod list, and it does not affect a running game's content.

## Failure Modes

- `SyntaxError` and `ImportError` in a module the engine loads stop that module; the error is in `PythonErr.log`, and the game continues with the base behaviour or with the feature absent.
- A runtime exception inside an event handler aborts the rest of that handler. The partial effect — a building built but no gold awarded — is the normal symptom of a Python bug.
- A callback that is switched off does not raise; it simply never runs. Check `PythonCallbackDefines.xml` before concluding the answer is ignored.
- Replacing a module that another mod also replaces has no reconciliation. Ship the smallest module that carries the change, and prefer importing a small helper from a replaced entry point over replacing the entry point itself.
- Python performance is bounded by the interpreter and the SWIG boundary. A per-turn loop over every plot is a visible frame cost in the modern game with large maps; batch work into one handler and cache lookups (`gc.getInfoTypeForString` is not free).
- The interpreter is a single instance: no threading, no background work, and no safe way to spend time off the main loop.
