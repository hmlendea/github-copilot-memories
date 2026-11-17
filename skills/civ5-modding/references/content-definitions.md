# Content Definitions

Civ5 content is a graph of `Type` strings and association tables. Add the class row, then the object row, then the associations, then the text and icons.

## Naming

```
CIVILIZATION_<NAME>     BUILDINGCLASS_<NAME>     BUILDING_<NAME>
LEADER_<NAME>           UNITCLASS_<NAME>         UNIT_<CIV>_<NAME>
TRAIT_<NAME>            POLICY_<NAME>            POLICY_BRANCH_<NAME>
TECH_<NAME>             ERA_<NAME>               RESOURCE_<NAME>
IMPROVEMENT_<NAME>      PROMOTION_<NAME>         BELIEF_<NAME>
PROJECT_<NAME>          PROCESS_<NAME>           SPECIALIST_<NAME>
MINOR_CIVILIZATION_<NAME>   FEATURE_<NAME>       TERRAIN_<NAME>
PLAYERCOLOR_<NAME>      TXT_KEY_<OBJECT>_<FIELD>
```

`Type` values are globally unique across all mods. Prefix with the mod or civ name — `BUILDING_MYMOD_LIBRARY`, not `BUILDING_LIBRARY2`. Never reuse a vanilla `Type` to "override" it; that is `<Update>`/`<Replace>`'s job and an `INSERT` collision silently aborts the file.

## Civilizations

```xml
<Civilizations>
  <Row>
    <Type>CIVILIZATION_MYMOD</Type>
    <Description>TXT_KEY_CIV_MYMOD_DESC</Description>
    <ShortDescription>TXT_KEY_CIV_MYMOD_SHORT_DESC</ShortDescription>
    <Adjective>TXT_KEY_CIV_MYMOD_ADJECTIVE</Adjective>
    <CivilopediaTag>TXT_KEY_CIV5_MYMOD</CivilopediaTag>
    <DefaultPlayerColor>PLAYERCOLOR_MYMOD</DefaultPlayerColor>
    <ArtStyleType>ARTSTYLE_EUROPEAN</ArtStyleType>
    <ArtStyleSuffix>_EURO</ArtStyleSuffix>
    <ArtStylePrefix>EUROPEAN</ArtStylePrefix>
    <PortraitIndex>0</PortraitIndex>
    <IconAtlas>MYMOD_CIV_COLOR_ATLAS</IconAtlas>
    <AlphaIconAtlas>MYMOD_CIV_ALPHA_ATLAS</AlphaIconAtlas>
    <MapImage>MapMyMod360x410.dds</MapImage>
    <DawnOfManQuote>TXT_KEY_CIV5_DAWN_MYMOD_TEXT</DawnOfManQuote>
    <DawnOfManImage>DOM_MYMOD.dds</DawnOfManImage>
    <DawnOfManAudio>AS2D_DOM_SPEECH_AMERICA</DawnOfManAudio>
    <Playable>true</Playable>
    <AIPlayable>true</AIPlayable>
  </Row>
</Civilizations>
```

Companion tables, all keyed by `CivilizationType`:

| Table | Purpose | Required |
|-------|---------|----------|
| `Civilization_Leaders` | `LeaderheadType` | Yes |
| `Civilization_CityNames` | `CityName` text keys, one per city | Yes, in practice |
| `Civilization_SpyNames` | `SpyName` text keys | Yes for BNW — a spy screen with no names stalls |
| `Civilization_FreeBuildingClasses` | typically `BUILDINGCLASS_PALACE` | Yes |
| `Civilization_FreeTechs` | typically `TECH_AGRICULTURE` | Yes |
| `Civilization_FreeUnits` | `UnitClassType`, `UnitAIType`, `Count` | Recommended |
| `Civilization_UnitClassOverrides` | `UnitClassType` → `UnitType` | ≥ 2 overrides total |
| `Civilization_BuildingClassOverrides` | `BuildingClassType` → `BuildingType` | ≥ 2 overrides total |
| `Civilization_Religions` | default preferred religion | Optional |
| `Civilization_Start_Along_Ocean` / `_Along_River` | start bias toggle | Optional |
| `Civilization_Start_Region_Priority` / `_Avoid` | `RegionType` bias | Optional |
| `Civilization_DisableTechs` | `TechType` | Optional |

`RegionType` values used for start bias: `REGION_GRASS`, `REGION_PLAINS`, `REGION_FOREST`, `REGION_JUNGLE`, `REGION_DESERT`, `REGION_TUNDRA`, plus `REGION_HILLS`, `REGION_SEA` in expansion data. An unsatisfiable combination (for example a priority region that the map generator cannot supply) produces a generated map with no start and an immediate ending.

A civilization with fewer than two overrides does not appear in the selection screen. A second `Civilization_Leaders` row is ignored by the setup screen; one leader per civilization is a hard UI behaviour.

City names are text keys, not literals: `TXT_KEY_CITY_NAME_MYMOD_CAPITAL` resolves through `Language_*`. Missing names silently borrow another civilization's.

## Leaders and AI Biases

```xml
<Leaders>
  <Row>
    <Type>LEADER_MYMOD</Type>
    <Description>TXT_KEY_LEADER_MYMOD</Description>
    <Civilopedia>TXT_KEY_LEADER_MYMOD_TEXT</Civilopedia>
    <CivilopediaTag>TXT_KEY_CIV5_LEADER_MYMOD</CivilopediaTag>
    <VictoryCompetitiveness>5</VictoryCompetitiveness>
    <WonderCompetitiveness>5</WonderCompetitiveness>
    <MinorCivCompetitiveness>5</MinorCivCompetitiveness>
    <Boldness>5</Boldness>
    <DiploBalance>5</DiploBalance>
    <WarmongerHate>5</WarmongerHate>
    <DenounceWillingness>5</DenounceWillingness>
    <DoFWillingness>5</DoFWillingness>
    <Loyalty>5</Loyalty>
    <Neediness>5</Neediness>
    <Forgiveness>5</Forgiveness>
    <Chattiness>5</Chattiness>
    <Meanness>5</Meanness>
    <PortraitIndex>22</PortraitIndex>
    <IconAtlas>MYMOD_LEADER_ATLAS</IconAtlas>
  </Row>
</Leaders>
<Leader_Traits>
  <Row><LeaderType>LEADER_MYMOD</LeaderType><TraitType>TRAIT_MYMOD</TraitType></Row>
</Leader_Traits>
```

`Leader_Flavors` (`FlavorType`, `Flavor` 0–10) and the approach-bias tables shape AI behaviour. Flavour keys in common use:

`FLAVOR_OFFENSE`, `FLAVOR_DEFENSE`, `FLAVOR_CITY_DEFENSE`, `FLAVOR_MILITARY_TRAINING`, `FLAVOR_RECON`, `FLAVOR_RANGED`, `FLAVOR_MOBILE`, `FLAVOR_NAVAL`, `FLAVOR_NAVAL_RECON`, `FLAVOR_NAVAL_GROWTH`, `FLAVOR_NAVAL_TILE_IMPROVEMENTS`, `FLAVOR_AIR`, `FLAVOR_EXPANSION`, `FLAVOR_GROWTH`, `FLAVOR_TILE_IMPROVEMENTS`, `FLAVOR_INFRASTRUCTURE`, `FLAVOR_PRODUCTION`, `FLAVOR_GOLD`, `FLAVOR_SCIENCE`, `FLAVOR_CULTURE`, `FLAVOR_HAPPINESS`, `FLAVOR_GREAT_PEOPLE`, `FLAVOR_WONDER`, `FLAVOR_RELIGION`, `FLAVOR_DIPLOMACY`, `FLAVOR_SPACESHIP`, `FLAVOR_NUKE`, `FLAVOR_USE_NUKE`, `FLAVOR_ESPIONAGE`, `FLAVOR_ANTIAIR`, `FLAVOR_AIR_CARRIER`.

**Custom content needs custom flavours.** A new `Unit` or `Building` with no `*_Flavors` row is invisible to AI valuation, so AI civs never build it. Add `Unit_Flavors` / `Building_Flavors` / `Improvement_Flavors` / `Policy_Flavors` rows alongside the object.

Approach biases: `Leader_MajorCivApproachBiases` (`MAJOR_CIV_APPROACH_WAR`, `_HOSTILE`, `_GUARDED`, `_DECEPTIVE`, `_FRIENDLY`, `_NEUTRAL`, `_AFRAID`) and `Leader_MinorCivApproachBiases` (`MINOR_CIV_APPROACH_IGNORE`, `_FRIENDLY`, `_PROTECTIVE`, `_CONQUEST`, `_BULLY`), both with `Bias`.

## Traits

`Traits` carries the aggregate modifiers (`Description`, `ShortDescription`, plus columns such as `GreatPeopleRateModifier`, `CityUnhappinessModifier`, `PolicyCostModifier`, `PlotBuyCostModifier`, `CultureFromKills`, `TradeRouteChange`, `WonderProductionModifier`, `PlunderModifier`, `CityStateFriendshipModifier`, `LandBarbarianConversionPercent`). Association tables cover the rest: `Trait_YieldChangesStrategicResources`, `Trait_ImprovementYieldChanges`, `Trait_SpecialistYieldChanges`, `Trait_FreePromotionUnitCombats`, `Trait_FreeBuildingClasses`, `Trait_UnitCombatFreeExperiences`.

Anything a trait cannot express is Lua keyed on `player:GetCivilizationType()` or a hidden building. The conventional pattern is a **dummy building** granted to the capital and updated by Lua: it persists through saves, needs no per-turn handler for its passive yields, and is inspectable with IGE.

## Units

```xml
<UnitClasses>
  <Row><Type>UNITCLASS_MYMOD_LONGBOW</Type><Description>TXT_KEY_UNIT_MYMOD_LONGBOW</Description><DefaultUnit>UNIT_MYMOD_LONGBOW</DefaultUnit></Row>
</UnitClasses>
<Units>
  <Row>
    <Type>UNIT_MYMOD_LONGBOW</Type>
    <Class>UNITCLASS_MYMOD_LONGBOW</Class>
    <Combat>12</Combat>
    <RangedCombat>18</RangedCombat>
    <Range>2</Range>
    <Cost>120</Cost>
    <Moves>2</Moves>
    <PrereqTech>TECH_MACHINERY</PrereqTech>
    <Description>TXT_KEY_UNIT_MYMOD_LONGBOW</Description>
    <Civilopedia>TXT_KEY_UNIT_MYMOD_LONGBOW_TEXT</Civilopedia>
    <Strategy>TXT_KEY_UNIT_MYMOD_LONGBOW_STRATEGY</Strategy>
    <Help>TXT_KEY_UNIT_MYMOD_LONGBOW_HELP</Help>
    <UnitArtInfo>ART_DEF_UNIT_ARCHER</UnitArtInfo>
    <UnitFlagAtlas>MYMOD_FLAG_ATLAS</UnitFlagAtlas>
    <UnitFlagIconOffset>0</UnitFlagIconOffset>
    <PortraitIndex>0</PortraitIndex>
    <IconAtlas>MYMOD_UNIT_ATLAS</IconAtlas>
  </Row>
</Units>
```

Association tables: `Unit_AITypes`, `Unit_NotAITypes`, `Unit_Builds`, `Unit_ClassUpgrades`, `Unit_FreePromotions`, `Unit_Flavors`, `Unit_GreatPersons`, `Unit_ResourceQuantityRequirements`, `Unit_UniqueNames`, `Unit_Buildings`, `Unit_BuildingClassRequireds`, `Unit_ProductionModifierBuildings`, `Unit_ProductionTraits`, `Unit_TechTypes`.

- `Class` must exactly match a `UnitClasses.Type`; a mismatch is a load-time crash or an unbuildable unit.
- `PrereqTech` must be a real tree node. A tech that exists as a row but is not wired into the tree (no `Technology_PrereqTechs` path from a starting tech) leaves the unit permanently unbuildable and the production panel may appear empty.
- Reuse existing `UnitArtInfo` unless you ship real 3D art. `UnitArtInfo`/`UnitMemberArtInfo` replacement is whole-table, so unit-art mods conflict.
- Promotions: `UnitPromotions` plus `UnitPromotionPrereq`/`Unit_FreePromotions` as needed. The vanilla 200-promotion ceiling was lifted in a 2012 patch; do not rely on either the old or new limit without checking the installed build.
- Civ5 has **no API to set a unit's religion**; do not promise religious units.

## Buildings

```xml
<BuildingClasses>
  <Row>
    <Type>BUILDINGCLASS_MYMOD_LIBRARY</Type>
    <DefaultBuilding>BUILDING_MYMOD_LIBRARY</DefaultBuilding>
    <Description>TXT_KEY_BUILDING_MYMOD_LIBRARY</Description>
    <MaxPlayerInstances>1</MaxPlayerInstances>
  </Row>
</BuildingClasses>
<Buildings>
  <Row>
    <Type>BUILDING_MYMOD_LIBRARY</Type>
    <BuildingClass>BUILDINGCLASS_MYMOD_LIBRARY</BuildingClass>
    <Cost>75</Cost>
    <PrereqTech>TECH_WRITING</PrereqTech>
    <Description>TXT_KEY_BUILDING_MYMOD_LIBRARY</Description>
    <Help>TXT_KEY_BUILDING_MYMOD_LIBRARY_HELP</Help>
    <Strategy>TXT_KEY_BUILDING_MYMOD_LIBRARY_STRATEGY</Strategy>
    <Civilopedia>TXT_KEY_BUILDING_MYMOD_LIBRARY_TEXT</Civilopedia>
    <NukeImmune>true</NukeImmune>
    <MinAreaSize>-1</MinAreaSize>
    <HurryCostModifier>-1</HurryCostModifier>
    <IconAtlas>MYMOD_BUILDING_ATLAS</IconAtlas>
    <PortraitIndex>3</PortraitIndex>
  </Row>
</Buildings>
```

`BuildingClasses.DefaultBuilding` must name a `Buildings.Type` that exists; a class with no default building is a start-up crash. `Buildings.BuildingClass` must name an existing class.

Placement conditions are boolean columns on `Buildings`: `Water`, `River`, `FreshWater`, `Mountain`, `NearbyMountainRequired`, `Hill`, `Flat`, `Capital`, `GoldenAge`, `AllowsWaterRoutes`, `TeamShare`, `NeverCapture`, `BorderObstacle`, `NukeImmune`, `IsReligious`, `FoundsReligion`. `MaxPlayerInstances`/`MaxGlobalInstances` make a National/World Wonder; `NumCityCostMod` scales cost with city count.

Association tables: `Building_YieldChanges`, `Building_YieldModifiers`, `Building_AreaYieldModifiers`, `Building_GlobalYieldModifiers`, `Building_BuildingClassHappiness`, `Building_BuildingClassYieldChanges`, `Building_ClassesNeededInCity`, `Building_PrereqBuildingClasses`, `Building_FreeUnits`, `Building_DomainFreeExperiences`, `Building_DomainFreeExperiencePerGreatWork`, `Building_DomainProductionModifiers`, `Building_FreeSpecialistCounts`, `Building_Flavors`, `Building_HurryModifiers`, `Building_LocalResourceAnds`, `Building_LocalResourceOrs`, `Building_ResourceQuantity`, `Building_SpecialistSlotChange`.

A "dummy building" is a normal building with cost 0, no `PrereqTech`, `MaxPlayerInstances` set appropriately, and no icon use; grant it from Lua with `city:SetNumRealBuilding(buildingID, 1)` and read its yields as your data carrier.

## Improvements, Routes, Resources

`Improvements` (with `Improvement_ValidTerrains`, `Improvement_ValidFeatures`, `Improvement_ResourceTypes`, `Improvement_Yields`, `Improvement_TechYieldChanges`, `Improvement_Flavors`, `Improvement_RouteYieldChanges`, and the terrain-conditional yield tables) must be paired with a `Builds` row so a worker can construct them, and with `Improvement_ResourceTypes` when they are required to hook a resource. Goody huts, city ruins, and barbarian camps are themselves improvements.

`Resources` (`ResourceClassType`, `ResourceType`, `TechReveal`, `TechCityTrade`, `AIObjective`, happiness and yield fields) needs `Resource_YieldChanges` for its tile yield, `Resource_TerrainBooleans`/`Resource_FeatureBooleans`/`Resource_FeatureTerrainBooleans` for placement, and `Resource_QuantityTypes` for quantity per tile/improvement. A resource must have a matching `Improvement_ResourceTypes` entry or it will never be improved and never count as connected.

`Resource_Flavors` matters as much as `Building_Flavors`: an unflavoured resource is not valued by AI.

## Policies and Beliefs

`Policies` requires a `PolicyBranchTypes` row. The social-policy screen has a fixed number of trees and positions; adding a branch needs `GridX`/`GridY` inside a tree that exists, and adding a whole tree needs UI work plus ideology Lua — otherwise the policy is unreachable. AI does not select modded ideologies.

`Policy_CityYieldChanges`, `_CapitalYieldChanges`, `_CapitalYieldModifiers`, `_CoastalCityYieldChanges`, `_YieldModifiers`, `_BuildingClassYieldModifiers`, `_BuildingClassCultureChanges`, `_BuildingClassHappiness`, `_ImprovementYieldChanges`, `_SpecialistExtraYields`, `_FreePromotions`, `_FreePromotionUnitCombats`, `_UnitCombatFreeExperiences`, `_UnitCombatProductionModifiers`, `_FreeUnitClasses`, `_Disables`, `_PrereqPolicies`, `_PrereqORPolicies`, `_ValidSpecialists`, `_Flavors`, `_HurryModifiers`.

Beliefs (`Beliefs`, `Belief_BuildingClassFaithPurchase`, `Belief_BuildingClassHappiness`, `Belief_BuildingClassYieldChanges`, `Belief_YieldChangePerForeignCity`, …) are gated by `Follower`, `Founder`, `Enhancer`, `Reformation` booleans on the row. Effects are keyed to the *belief category*, not the founder: a `Belief_BuildingClassFaithPurchase` entry applies in every city of the religion, which is why the Jesuit Reformation belief grants buildings in foreign cities.

## Technologies, Eras, Projects, Processes, Specialists

`Technologies` (`Era`, `Cost`, `GridX`, `GridY`, `Quote`, `PortraitIndex`, `IconAtlas`) must be reachable through `Technology_PrereqTechs` and placed on the tech-tree grid without overlapping another node. `Technology_Flavors` shapes AI research; `Technology_DomainFreeExperiences`, `Technology_UnitCombatFreeExperiences`, `Technology_ProvidesFreeTechs` carry the effects.

`Eras` (`TechCostMultiplier`, `ResearchAgreementCost`, `PortraitIndex`, `IconAtlas`) reorder the tech cost curve; changing an existing era is a large, save-breaking decision.

`Projects` (`Cost`, `PrereqTech`, `MaxPlayerInstances`, `PortraitIndex`, `IconAtlas`, plus `Project_Flavors` and `Project_PrereqProjects`) is how World Congress and spaceship-style goals are expressed. A project referenced by a World Congress resolution needs the corresponding congress tables or the resolution never becomes available.

`Processes` (`ProductionToYieldModifier`, `PrereqTech`) with `Process_Flavors` and `Process_ProductionYields` are the "convert production" options. `Specialists` (`GreatPeopleRateChange`, `YieldChanges`, `PortraitIndex`, `IconAtlas`) needs `Specialist_Flavors` and a matching slot on some building's `Building_SpecialistSlotChange`; a specialist with no slot is dead data.

## City-States and Natural Wonders

`MinorCivilizations` (`DefaultPlayerColor`, `ArtStyleType`, `ArtStyleSuffix`, `ArtStylePrefix`, `MinorCivTrait`, `PortraitIndex`, `IconAtlas`, `AlphaIconAtlas`) plus `MinorCivTraits` entries; city names, spy names, and start bias follow the same tables as major civilizations. `MINOR_CIV_TRAIT_MARITIME`, `_MERCANTILE`, `_CULTURAL`, `_MILITARISTIC`, `_RELIGIOUS`, `_CULTURED` (expansion set varies) determine the unique bonus.

Natural wonders are `Features` (`NaturalWonder`, `Influence`, `RequiresTech`, `PortraitIndex`, `IconAtlas`) with `Feature_YieldChanges` and art/placement rules; placement is orchestrated by `AssignStartingPlots` in Lua and replacing those functions collides with every other map mod.

## Icons and Atlases

Every icon comes from an atlas row plus a `PortraitIndex` on the object:

```xml
<IconTextureAtlases>
  <Row><Atlas>MYMOD_BUILDING_ATLAS</Atlas><IconSize>256</IconSize><Filename>MyMod_Atlas_256.dds</Filename><IconsPerRow>8</IconsPerRow><IconsPerColumn>8</IconsPerColumn></Row>
  <Row><Atlas>MYMOD_BUILDING_ATLAS</Atlas><IconSize>128</IconSize><Filename>MyMod_Atlas_128.dds</Filename><IconsPerRow>8</IconsPerRow><IconsPerColumn>8</IconsPerColumn></Row>
</IconTextureAtlases>
```

- Civ5 requests the size it needs at each zoom level; ship 256, 128, 80, 64, 45, and 32 for anything that appears in multiple places.
- `PortraitIndex` is zero-based within the sheet, row-major.
- The `.dds` must be uncompressed (or DXT5 for alpha), with mipmaps **off** for UI atlases. GIMP, Paint.NET, and the DDS Converter/NVidia tools all produce acceptable output.
- Civilizations need both a colour atlas and an alpha (emblem) atlas; the alpha sheet is what the game tints with `PlayerColor`.
- Font icons are separate: `IconFontMapping` maps `[ICON_...]` tags to atlas coordinates and is what `references/localisation.md` markup consumes.