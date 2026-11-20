# Content Definitions

Civ4 content is a graph of `Type` strings. Add the class row, then the object row, then its lists, then the text keys, then the art define.

## Naming

```
UNIT_<CIV>_<NAME>          UNITCLASS_<NAME>        UNITCOMBAT_<NAME>
BUILDING_<CIV>_<NAME>      BUILDINGCLASS_<NAME>    PROMOTION_<NAME>
CIVILIZATION_<NAME>        LEADER_<NAME>           TRAIT_<NAME>
TECH_<NAME>                ERA_<NAME>              CIVIC_<NAME>
BONUS_<NAME>               IMPROVEMENT_<NAME>      FEATURE_<NAME>
TERRAIN_<NAME>             ROUTE_<NAME>            SPECIALIST_<NAME>
PROJECT_<NAME>             CORPORATION_<NAME>      RELIGION_<NAME>
ART_DEF_<OBJECT>_<NAME>    PLAYERCOLOR_<NAME>      TXT_KEY_<OBJECT>_<NAME>
```

`Type` values are global, unique, and case-sensitive, and are referenced by every other file. Prefix with the mod or the civilization — `UNIT_MYMOD_LONGBOW`, not `UNIT_LONGBOW2`. A `Type` declared twice in the loaded set is a duplicate, and re-using a vanilla `Type` inside a whole-file replacement is a duplicate as well.

**Ordering inside an entry is mandatory** (`references/xml-reference.md`). Copy a vanilla entry for a similar object and edit it; do not write an entry from scratch.

## Dependency Chains

| Object | Requires, in order |
|--------|-------------------|
| Unit | `UNITCLASS_*` → `UNIT_*` → `ART_DEF_UNIT_*` → `TXT_KEY_*` → (button/atlas) |
| Building | `BUILDINGCLASS_*` → `BUILDING_*` → `ART_DEF_BUILDING_*` → `TXT_KEY_*` |
| Civilization | `LEADER_*`, `PLAYERCOLOR_*`, `ART_DEF_CIVILIZATION_*`, `UNIT_ARTSTYLE_*` → `CIVILIZATION_*` → its unique `UNIT_*`/`BUILDING_*` |
| Promotion | `PROMOTION_*` → referenced from `UNIT_*` or a free-promotion list |
| Improvement | `IMPROVEMENT_*` → `BUILD_*` (so a worker may construct it) → `ART_DEF_IMPROVEMENT_*` |
| Religion / Corporation | `RELIGION_*` / `CORPORATION_*` → art define → text → free-mission missionary unit |
| Event | `EVENTTRIGGER_*` → `EVENT_*` → text rows → optional Python callbacks |

A missing link is silent: the object loads without the missing part.

## Units

`CIV4UnitInfos.xml` — root `<UnitInfos>`, entry `<UnitInfo>`.

| Tag | Meaning |
|-----|---------|
| `Class`, `Type` | The unit's id and its `UNITCLASS_*`; a civilization may field only one unit per class |
| `Combat`, `Domain` | `UNITCOMBAT_*` (melee, archer, mounted, gun, siege, naval, air, helicopter) and `DOMAIN_LAND`/`_SEA`/`_AIR` |
| `DefaultUnitAI` | Which AI routine drives the unit, e.g. `UNITAI_ATTACK`, `UNITAI_SETTLE`, `UNITAI_WORKER`; supplemented by the `UnitAIs`/`NotUnitAIs` lists of `UnitAIType` + `bUnitAI` pairs |
| `iMoves`, `iCost`, `iHurryCostModifier`, `iHurryMultiplier` | Movement, hammers, rush cost |
| `PrereqTech`, `TechTypes`, `PrereqBuilding`, `PrereqReligion`, `PrereqCorporation`, `PrereqBonuses`/`bPrereqBonuses`, `BonusType` | Build prerequisites |
| `iCombat`, `iAirCombat`, `iAirRange`, `iAirCombatLimit`, `iAirUnitCap`, `iInterceptionProbability`, `iEvasionProbability` | Air and interception numbers |
| `iCityAttack`, `iCityDefense`, `iHillsAttack`, `iHillsDefense`, `iAnimalCombat`, `iWithdrawalProb`, `iCombatLimit` | Combat modifiers, all percentages except where noted |
| `iFirstStrikes`, `iChanceFirstStrikes`, `iCollateralDamage`, `iCollateralDamageLimit`, `iCollateralDamageMaxUnits`, `iBombardRate`, `iBombRate` | First strikes, collateral, bombardment |
| `iCargo`, `SpecialCargo`, `DomainCargo`, `iAirUnitCap`, `iNukeRange`, `iDropRange`, `iMinAreaSize` | Transport, capacity, nuclear, paradrop, sea-area minimum |
| `iWorkRate`, `iBaseDiscover`, `iDiscoverMultiplier`, `iBaseTrade`, `iTradeMultiplier`, `iBaseHurry`, `iHurryMultiplier` | Worker rate, great-person discovery and trade missions |
| `iXPValueAttack`, `iXPValueDefense`, `LeaderPromotion`, `iLeaderExperience`, `iGreatWorkCulture`, `iEspionagePoints`, `iConscription`, `iCultureGarrison` | Experience, great works, espionage, drafting, garrison suppression |
| `iAsset`, `iPower`, `iAIWeight` | Score and AI valuation |
| `Invisible`, `SeeInvisible` | `NONE`, `INVISIBLE_STEALTH`, `INVISIBLE_SUBMARINE` |
| `UniqueNames` | Alternate display names; a `UnitName` list of text tags |
| `Flavors` | `FlavorType` + `iFlavor` pairs; an unflavoured unit is invisible to AI valuation |
| `FreePromotions`, `UnitClassUpgrades`, `UnitClassTargets`, `ProductionTraits` | Promotions granted, upgrade targets, trait production modifiers |
| `UnitMeshGroups` | `iGroupSize`, `fMaxSpeed`, `fPadTime`, `iMeleeWaveSize`, `iRangedWaveSize`, and the `UnitMeshGroup` entries (`iRequired` + `EarlyArtDefineTag`) that bind models to the unit |
| `Capture`, `Special`, `ReligionType`, `StateReligion`, `HolyCity`, `bFound`, `bGoldenAge`, `bSpy`, `bHiddenNationality`, `bAlwaysHostile` | Capture result, special-unit class, religion and role flags |

The unit's class comes first: `CIV4UnitClassInfos.xml` declares `UNITCLASS_<NAME>` with a `Description`, the instance caps `iMaxGlobalInstances`/`iMaxTeamInstances`/`iMaxPlayerInstances`, `iInstanceCostModifier`, and a `DefaultUnit`. A unit whose `Class` names a missing class is a load failure; a class whose `DefaultUnit` names a missing unit leaves the class unusable.

**The unit does not name its own model.** Art comes from the `UnitMeshGroup` entries inside `UnitMeshGroups` (`iRequired` units of the group plus an `EarlyArtDefineTag` naming an `ART_DEF_UNIT_*`), and a civilization's `CIV4UnitArtStyleTypeInfos.xml` entry can substitute a different art define per unit class. A unit with no mesh group renders as a placeholder.

`CIV4BuildInfos.xml` defines worker orders (chop, mine, road, fort, and any modded build), `CIV4PromotionInfos.xml` the promotions, `CIV4MissionInfos.xml` and `CIV4CommandInfos.xml` the unit orders the interface offers, and `CIV4InvisibleInfos.xml` / `CIV4UnitCombatInfos.xml` / `CIV4UnitAIInfos.xml` the vocabularies those files reference.

### Promotions

`<PromotionInfo>` carries `Type`, `Description`, `Sound`, `LayerAnimationPath`, `PromotionPrereq`, `PromotionPrereqOr1`/`Or2`/`Or3`, `TechPrereq`, `StateReligionPrereq`, `Button`, the boolean capabilities `bLeader`, `bBlitz`, `bAmphib`, `bRiver`, `bEnemyRoute`, `bAlwaysHeal`, `bHillsDoubleMove`, `bImmuneToFirstStrikes`, and a long list of `i*Change` deltas: `iVisibilityChange`, `iMovesChange`, `iMoveDiscountChange`, `iAirRangeChange`, `iInterceptChange`, `iEvasionChange`, `iWithdrawalChange`, `iCargoChange`, `iCollateralDamageChange`, `iBombardRateChange`, `iFirstStrikesChange`, `iChanceFirstStrikesChange`, `iEnemyHealChange`, `iNeutralHealChange`, `iFriendlyHealChange`, `iSameTileHealChange`, `iCombatPercent`, `iCityAttack`, `iCityDefense`, `iHillsAttack`, `iHillsDefense`, `iKamikazePercent`, `iRevoltProtection`, `iCollateralDamageProtection`, `iPillageChange`, `iUpgradeDiscount`, `iExperiencePercent`, plus `TerrainAttacks`, `TerrainDefenses`, `FeatureAttacks`, `FeatureDefenses`, `UnitCombatMods`, `DomainMods`, `TerrainDoubleMoves`, `FeatureDoubleMoves`, and the `UnitCombats` selection list. A promotion with an empty effect list is legal and useless; a promotion referenced by a unit but not declared is a load failure.

The `UnitCombats` list is what restricts a promotion to a category such as `UNITCOMBAT_MELEE`, and a reward programme that grants a promotion to the wrong category is silent because the promotion simply is not offered.

## Buildings

`CIV4BuildingClassInfos.xml` then `CIV4BuildingInfos.xml`.

Class fields: `Type`, `Description`, the instance caps `iMaxGlobalInstances`, `iMaxTeamInstances`, `iMaxPlayerInstances`, `iExtraPlayerInstances`, the flags `bNoLimit` and `bMonument`, `DefaultBuilding`, and `VictoryThresholds`. Anything with a non-default cap is a Wonder or a National Wonder, and `CIV4SpecialBuildingInfos.xml` carries the extra semantics those need. `VictoryThresholds` is how a wonder gates a victory condition; a class declared there without a matching `CIV4VictoryInfo.xml` entry does nothing.

Entry fields, by group:

| Group | Tags |
|-------|------|
| Identity | `BuildingClass`, `Type`, `SpecialBuildingType`, `Description`, `Civilopedia`, `Strategy`, `Advisor`, `ArtDefineTag`, `MovieDefineTag`, `ConstructSound` |
| Cost and prerequisites | `iCost`, `iHurryCostModifier`, `iAdvancedStartCost`, `iAdvancedStartCostIncrease`, `PrereqTech`, `ObsoleteTech`, `PrereqBonuses`, `Bonus` (production accelerator), `PrereqReligion`, `ReligionType`, `StateReligion`, `bPrereqReligion`, `PrereqCorporation`, `iCitiesPrereq`, `iTeamsPrereq`, `iLevelPrereq`, `iMinAreaSize`, `iMinLatitude`, `iMaxLatitude`, `PrereqBuildingClasses`, `BuildingClassNeededs`, `FreeStartEra`, `MaxStartEra`, `VictoryPrereq`, `DiploVoteType` |
| Yields and commerce | `YieldChanges`, `CommerceChanges`, `CommerceModifiers`, `GlobalCommerceModifiers`, `CommerceChangeDoubleTimes`, `CommerceChangeOriginalOwners`, `CommerceFlexibles`, `CommerceHappinesses`, `ObsoleteSafeCommerceChanges`, `BonusYieldModifiers`, `SeaPlotYieldChanges`, `RiverPlotYieldChanges`, `GlobalSeaPlotYieldChanges`, `SpecialistExtraCommerces`, `StateReligionCommerces`, `ReligionChanges` |
| Happiness and health | `iHappiness`, `iAreaHappiness`, `iGlobalHappiness`, `iStateReligionHappiness`, `iHealth`, `iAreaHealth`, `iGlobalHealth`, `iUnhealthyPopulationModifier`, `bBuildingOnlyHealthy`, `BonusHappinessChanges`, `BonusHealthChanges`, `BuildingHappinessChanges` |
| Specialists and great people | `iFreeSpecialist`, `iAreaFreeSpecialist`, `iGlobalFreeSpecialist`, `FreeSpecialistCounts`, `SpecialistCounts`, `iGreatPeopleRateChange`, `iGreatPeopleRateModifier`, `iGlobalGreatPeopleRateModifier`, `iGreatGeneralRateModifier`, `iDomesticGreatGeneralRateModifier`, `GreatPeopleUnitClass`, `SpecialistYieldChanges`, `ImprovementFreeSpecialists`, `FreePromotion`, `UnitCombatFreeExperiences`, `DomainFreeExperiences`, `DomainProductionModifiers` |
| Trade, production, defence | `iTradeRoutes`, `iCoastalTradeRoutes`, `iGlobalTradeRoutes`, `iTradeRouteModifier`, `iForeignTradeRouteModifier`, `iMilitaryProductionModifier`, `iSpaceProductionModifier`, `iGlobalSpaceProductionModifier`, `iExperience`, `iGlobalExperience`, `iDefense`, `iAllCityDefense`, `iBombardDefense`, `iEspionageDefense`, `iAirModifier`, `iAirUnitCapacity`, `iNukeModifier`, `iNukeExplosionRand`, `iAirlift`, `iHealRateChange`, `iConquestProb`, `iMaintenanceModifier`, `iAnarchyModifier`, `iGlobalHurryModifier`, `iWarWearinessModifier`, `iGlobalWarWearinessModifier`, `iEnemyWarWearinessModifier`, `iGlobalPopulationChange`, `iWorkerSpeedModifier`, `iGoldenAgeModifier`, `iHurryAngerModifier`, `iAsset`, `iPower`, `iAIWeight`, `fVisibilityPriority` |
| Effects on other content | `FreeBuilding`, `FreeBonus`, `iNumFreeBonuses`, `iFreeTechs`, `CivicOption` (free civics), `NoBonus`, `PowerBonus` (provides power), `FreeStartEra`, `bWater`, `bRiver`, `bCapital`, `bGovernmentCenter`, `bGoldenAge`, `bAllowsNukes`, `bMapCentering`, `bNoUnhappiness`, `bNeverCapture`, `bNukeImmune`, `bTeamShare`, `bBorderObstacle`, `bCenterInCity`, `bForceTeamVoteEligible`, `HotKey`, `Flavors` |

Beyond the Sword adds corporations and espionage: `CorporationType`, corporation-related commerce and `iEspionageDefense`, with the corporation tables in `CIV4CorporationInfo.xml`.

A building whose `BuildingClass` is missing, or whose class's `DefaultBuilding` is missing, is a load failure or an unusable class. `NoBonus` blocks a resource in the city (the National Park pattern), and `PowerBonus` is how a plant supplies power — both are frequently mis-set.

## Technologies, Eras, and the Tech Tree

`CIV4TechInfos.xml` — root `<TechInfos>`, entry `<TechInfo>`.

- Identity and presentation: `Type` (first), `Description`, `Civilopedia`, `Help`, `Strategy`, `Quote`, `Sound`, `SoundMP`, `Advisor`, `Era`, `Button`.
- Placement: `iGridX`, `iGridY` place the node in the tree; a tech that no other tech requires and that requires nothing is unreachable from the start of the tree.
- Prerequisites: `AndPreReqs` and `OrPreReqs`, each a list of `PrereqTech` entries. `AndPreReqs` requires all of them, `OrPreReqs` any one of them.
- Cost and score: `iCost`, `iAsset`, `iPower`, `iAIWeight`, `iAITradeModifier`, `iAdvancedStartCost`, `iAdvancedStartCostIncrease`, `iFeatureProductionModifier`, `iWorkerSpeedModifier`, `iTradeRoutes`, `iHappiness`, `iHealth`.
- Unlock flags: `bTrade`, `bTechTrading`, `bGoldTrading`, `bOpenBordersTrading`, `bDefensivePactTrading`, `bPermanentAllianceTrading`, `bVassalTrading`, `bBridgeBuilding`, `bIrrigation`, `bIgnoreIrrigation`, `bRiverTrade`, `bWaterWork`, `bMapCentering`, `bMapVisible`, `bMapTrading`, `bGoodyTech`, `bRepeat`, `bDisable`.
- Grants and lists: `FirstFreeUnitClass`, `iFirstFreeTechs`, `DomainExtraMoves`, `CommerceFlexible`, `TerrainTrades`, `Flavors`.

`CIV4EraInfos.xml` defines the eras with their art style, movie, and era-level modifiers; `iGridX`/`iGridY` in the tech file are interpreted within the era the tech names, so a moder moves a tech between eras by changing both files.

## Civilizations

`CIV4CivilizationInfos.xml` — entry `<CivilizationInfo>`.

| Tag | Meaning |
|-----|---------|
| `Type`, `Description`, `ShortDescription`, `Adjective`, `Civilopedia` | Identity and text keys |
| `DefaultPlayerColor` | A `PLAYERCOLOR_*` from `CIV4PlayerColorInfos.xml` |
| `ArtDefineTag` | An `ART_DEF_CIVILIZATION_*` for the flag and colour decals |
| `ArtStyleType`, `UnitArtStyleType` | City-set style (`ARTSTYLE_*` from `GlobalTypes.xml`) and the unit art style (`UNIT_ARTSTYLE_*` from `CIV4UnitArtStyleTypeInfos.xml`, BtS) |
| `bPlayable`, `bAIPlayable` | `0` for minor and barbarian civilizations, `1` for the rest |
| `DerivativeCiv` | Which civilization a colony from this one prefers to become, or `NONE` |
| `DescriptionUniquePower` | The unique-power blurb, present in BtS-era files |
| `CivilizationSelectionSound`, `CivilizationActionSound` | Sound scripts from `Audio3DScripts.xml` |
| `Leaders` | A list of `Leader` entries, each with `LeaderName` and `bLeaderAvailability` |
| `Cities` | An ordered list of `City` names; each is a literal or a `TXT_KEY_` |
| `Buildings` | Unique-building overrides, each a `Building` with `BuildingClassType` → `BuildingType` |
| `Units` | Unique-unit overrides, each a `Unit` with `UnitClassType` → `UnitType` |
| `FreeBuildingClasses` | Starting buildings: `BuildingClassType` + `bFreeBuildingClass` |
| `FreeTechs` | Starting technologies: `TechType` + `bFreeTech` |
| `FreeUnitClasses` | Starting units: `UnitClassType` + `iFreeUnits` |
| `InitialCivics` | Starting civics, referencing `CivicType` |
| `DisableTechs` | Technologies the civilization can never research |

`CIV4UnitArtStyleTypeInfos.xml` maps a unit class to a per-civilization art define, which is how a unique unit's model is given to the right civilization without changing `CIV4UnitInfos.xml`.

## Leaders and Traits

`CIV4LeaderHeadInfos.xml` — entry `<LeaderHeadInfo>`:

- Identity: `Type`, `Description`, `Civilopedia`, `ArtDefineTag` (`ART_DEF_LEADER_*`), and the diplomacy audio block (`DiplomacyIntroMusicPeace`, `DiploMusicPeaceEra`, `EraType`, `DiplomacyMusicPeace`, `DiploScriptId`, `DiplomacyIntroMusicWar`, `DiploMusicWarEra`, `DiplomacyMusicWar`).
- Personality integers, each with a designed range: `iWonderConstructRand` (0 reluctant, 50 eager), `iBaseAttitude` (−1 unfriendly, 2 friendly), `iBasePeaceWeight` (0 warmonger, 10 peace lover) with `iPeaceWeightRand`, `iWarmongerRespect`, `iEspionageWeight` (50 reluctant, 150 eager, most leaders 90–120), `iRefuseToTalkWarThreshold`, `iNoTechTradeThreshold` (5 stops trading soon, 20 late), `iTechTradeKnownPercent` (0 shares readily, 100 monopoly), `iMaxGoldTradePercent`, `iMaxGoldPerTurnTradePercent`.
- Victory preference and war appetite: `iCultureVictoryWeight`, `iSpaceVictoryWeight`, `iConquestVictoryWeight`, `iDominationVictoryWeight`, `iDiplomacyVictoryWeight`; `iMaxWarRand` (50 eager, 400 reluctant), `iMaxWarNearbyPowerRatio`, `iMaxWarDistantPowerRatio`, `iMaxWarMinAdjacentLandPercent`, `iLimitedWarRand`, `iLimitedWarPowerRatio` (40 eager, 200 reluctant), `iDogpileWarRand`, `iMakePeaceRand`, `iDeclareWarTradeRand`, `iDemandRebukedSneakProb`, `iDemandRebukedWarProb`, `iRazeCityProb`, `iBuildUnitProb`, `iBaseAttackOddsChange`, `iAttackOddsChangeRand`.
- Attitude drift: the `i*AttitudeChange`/`i*AttitudeDivisor`/`i*AttitudeChangeLimit` triples for rank difference, closed borders, lost wars, war and peace duration, same and different religion, bonus trade, open borders, defensive pacts, shared war, and the favourite civic; then the `*AttitudeThreshold`/`*RefuseAttitudeThreshold` gates that decide when the leader will trade, help, or sign an agreement; then `iVassalPowerModifier`, `iFreedomAppreciation`, `FavoriteCivic`, `FavoriteReligion`.
- Lists and tables: `Traits` (the leader's trait type names), `Flavors`, `ContactRands`, `ContactDelays`, `MemoryDecays`, `MemoryAttitudePercents`, `NoWarAttitudeProbs`, `UnitAIWeightModifiers`, `ImprovementWeightModifiers`.

A leader must be referenced from a civilization's `Leaders` list to appear, and the leader's `ArtDefineTag` and button must exist or the leader has a blank portrait. A trait is a small bundle of civilization-wide modifiers: `Type`, `Description`, `ShortDescription`, then the effects — `iHealth`, `iHappiness`, `iMaxAnarchy`, `iUpkeepModifier`, `iLevelExperienceModifier`, `iGreatPeopleRateModifier`, `iGreatGeneralRateModifier`, `iDomesticGreatGeneralRateModifier`, `iMaxGlobalBuildingProductionModifier`, `iMaxTeamBuildingProductionModifier`, `iMaxPlayerBuildingProductionModifier`, `iDistanceMaintenanceModifier`, `iBonusValueModifier` — followed by the list groups `ExtraYieldThresholds`, `TradeYieldModifiers`, `CommerceChanges`, `CommerceModifiers`, `FreeCommerce`, `FreePromotions`, and `FreePromotionUnitCombats`.

The trait field list is narrower than a Civ5 player expects: a trait carries no city-growth modifier and no worker-speed modifier in this engine, and anything a trait cannot express is either a free promotion, free commerce, or Python keyed on the leader type. A trait takes effect only through the `Traits` list on a leader.

## Civics, Religions, Corporations

- `CIV4CivicOptionInfos.xml` declares the civic categories (Government, Legal, Labour, Economy, Religion). `CIV4CivicInfos.xml` declares each civic with `CivicOptionType` first, then `Type`, `Description`, `Civilopedia`, `Strategy`, `Button`, `TechPrereq`, the cost fields `Upkeep`, `iAnarchyLength`, `iAIWeight`, and a long block of national modifiers (`iGreatPeopleRateModifier`, `iDistanceMaintenanceModifier`, `iNumCitiesMaintenanceModifier`, `iCorporationMaintenanceModifier`, `iExtraHealth`, `iFreeExperience`, `iWorkerSpeedModifier`, `iImprovementUpgradeRateModifier`, `iMilitaryProductionModifier`, `iGoldPerUnit`, `iGoldPerMilitaryUnit`, `iHappyPerMilitaryUnit`, `iBaseFreeUnits`, `iBaseFreeMilitaryUnits`, `iFreeUnitsPopulationPercent`, `iFreeMilitaryUnitsPopulationPercent`, `iLargestCityHappiness`, `iWarWearinessModifier`, `iFreeSpecialist`, `iTradeRoutes`, `iCivicPercentAnger`, `iMaxConscript`), the state-religion block (`bStateReligion`, `bNoNonStateReligionSpread`, `iStateReligionHappiness`, `iNonStateReligionHappiness`, `iStateReligionUnitProductionModifier`, `iStateReligionBuildingProductionModifier`, `iStateReligionFreeExperience`, `iStateReligionGreatPeopleRateModifier`), the prohibition flags (`bNoForeignTrade`, `bNoCorporations`, `bNoForeignCorporations`, `bNoUnhealthyPopulation`, `bBuildingOnlyHealthy`, `bMilitaryFoodProduction`), and the yield and happiness list groups (`YieldModifiers`, `ExtraYields`, `CapitalYieldModifiers`, `TradeYieldModifiers`, `CommerceModifiers`, `CapitalCommerceModifiers`, `SpecialistExtraCommerces`, `Hurrys`, `SpecialBuildingNotRequireds`, `SpecialistValids`, `BuildingHappinessChanges`, `BuildingHealthChanges`, `FeatureHappinessChanges`, `ImprovementYieldChanges`, `WeLoveTheKing`). A civic whose `CivicOptionType` is missing never appears.
- `CIV4ReligionInfo.xml` declares each religion with `Type`, `Description`, `Adjective`, `Civilopedia`, `TechPrereq`, the missionary grant `FreeUnitClass` + `iFreeUnits`, `iSpreadFactor`, the commerce lists `GlobalReligionCommerces`, `HolyCityCommerces`, `StateReligionCommerces` (each an `i*Commerce` per commerce type), and the presentation fields `Button`, `TechButton`, `GenericTechButton`, `MovieFile`, `MovieSound`, `Sound`. A religion needs a missionary unit class, a shrine building, and its `HolyCity` plumbing to be playable, and it has no art-define reference of its own — the icons come from the button fields.
- `CIV4CorporationInfo.xml` (BtS): `Type`, `Description`, `Civilopedia`, `TechPrereq`, `FreeUnitClass` (the free corporation executive the founder receives), `iSpreadFactor`, `iSpreadCost`, `iMaintenance`, `bCoastal`, `PrereqBonuses`/`BonusType` (the resources it consumes), the `HeadquarterCommerces`/`CommercesProduced`/`YieldsProduced` lists, and the presentation fields `Button`, `MovieFile`, `MovieSound`, `Sound`. The consumed-bonus list and the produced-commerce list are the whole economic definition of a corporation; a corporation with no consumed resource never spreads.

## Terrain, Features, Improvements, Routes, Bonuses

- `CIV4TerrainInfos.xml`: `Type`, `Description`, `Civilopedia`, `ArtDefineTag` (`ART_DEF_TERRAIN_*`), the `Yields` list (`iYield` per type) with the modifiers `RiverYieldChange` and `HillsYieldChange`, the flags `bWater`, `bImpassable`, `bFound`, `bFoundCoast`, `bFoundFreshWater`, `bGraphicalOnly`, the integers `iMovement`, `iSeeFrom`, `iSeeThrough`, `iBuildModifier`, `iDefense`, and the presentation fields `Button`, `FootstepSounds`/`FootstepSound`/`FootstepAudioType`/`FootstepAudioScript`, `WorldSoundscapeAudioScript`. Terrain art is a mesh plus texture; a new terrain needs both.
- `CIV4FeatureInfos.xml`: forests, jungles, flood plains, oasis, ice. Fields include `ArtDefineTag`, `YieldChanges`/`RiverYieldChange`/`HillsYieldChange`, `iMovement`, `iSeeThrough`, `iHealthPercent`, `iDefense`, the growth pair `iAppearance`/`iDisappearance`/`iGrowth`, `iTurnDamage` and `iWarmingDefense` (the feature-damage and global-warming behaviour), the placement flags `bNoCoast`, `bNoRiver`, `bNoAdjacent`, `bRequiresFlatlands`, `bRequiresRiver`, `bAddsFreshWater`, `bImpassable`, `bNoCity`, `bNoImprovement`, `bVisibleAlways`, `bNukeImmune`, the `TerrainBooleans` validity list, the footstep and soundscape fields, `OnUnitChangeTo` plus `EffectType`/`iEffectProbability` for the effect played on a unit in the feature, and `iAdvancedStartRemoveCost`.
- `CIV4ImprovementInfos.xml`: `Type`, `Description`, `Civilopedia`, `ArtDefineTag`, `WorldSoundscapeAudioScript`; placement booleans `bActsAsCity`, `bHillsMakesValid`, `bFreshWaterMakesValid`, `bRiverSideMakesValid`, `bNoFreshWater`, `bRequiresFlatlands`, `bRequiresRiverSide`, `bRequiresIrrigation`, `bCarriesIrrigation`, `bRequiresFeature`, `bWater`, `bGoody`, `bPermanent`, `bOutsideBorders`, `bGraphicalOnly`; integers `iAdvancedStartCost`, `iAdvancedStartCostIncrease`, `iTilesPerGoody`, `iGoodyRange`, `iFeatureGrowth`, `iUpgradeTime`, `iAirBombDefense`, `iDefenseModifier`, `iHappiness`, `iPillageGold`; and the list groups `TerrainMakesValids`, `FeatureMakesValids`, `ImprovementPillage`, `ImprovementUpgrade`, `TechYieldChanges`, `RouteYieldChanges`.
  - **Every improvement a worker may build also needs a `BUILD_*` row in `CIV4BuildInfos.xml`**, plus a button and an AI weight; without the build, a worker has no order for it.
  - An improvement that should improve a resource must be listed in the resource's improvement reference or it will not hook.
- `CIV4RouteInfos.xml`: roads, railroads and modded routes — art, movement cost, `iGoldChange`/commerce, and the `PrereqTech`-style gate.
- `CIV4BonusInfos.xml`: resources. `Type`, `Description`, `Civilopedia`, `BonusClassType` (`CIV4BonusClassInfos.xml`), `ArtDefineTag`, `TechReveal`, `TechCityTrade`, `TechObsolete`, `YieldChanges`/`iYieldChange`, `iAITradeModifier`, `iHealth`, `iHappiness`, the placement weights `iPlacementOrder`, `iConstAppearance`, `iMinAreaSize`, `iMinLatitude`, `iMaxLatitude`, `iUnique`, `iTilesPer`, `iMinLandPercent`, `iGroupRange`, `iGroupRand` and the `Rands` entries inside them, the area/terrain booleans `bArea`, `bHills`, `bFlatlands`, `bNoRiverSide`, `bNormalize`, and the validity lists `TerrainBooleans`, `FeatureBooleans`, `FeatureTerrainBooleans`. A resource with no `ArtDefineTag` is invisible on the map; a resource with no improving improvement is never improved.

## Specialists, Great People, Projects

- `CIV4SpecialistInfos.xml`: each specialist's `Type`, `Description`, `Civilopedia`, `Strategy`, `Help`, `Texture`, `bVisible`, `GreatPeopleUnitClass` (the great person it produces), `iGreatPeopleRateChange`, the `Yields` list (`iYield` per type) and the `Commerces` list (`iCommerce` per type), `iExperience`, `iHappiness`, and `Flavors`/`Button`/`HotKey`.
- `CIV4ProcessInfo.xml`: the conversion projects every city always has (research, culture, wealth). `Type`, `Description`, `Strategy`, `TechPrereq`, the `ProductionToCommerceModifiers` list (`iProductionToCommerceModifier` per commerce type), and `Button`.
- `CIV4ProjectInfo.xml`: the spaceship parts and the Apollo/Manhattan-style projects: `Type`, `Description`, `Civilopedia`, `Strategy`, `TechPrereq`/`TechPrereq2`, `AnyonePrereqProject`, `PrereqProjects`, `VictoryPrereq`/`VictoryThresholds`/`VictoryMinThresholds`/`iVictoryDelayPercent`, the instance caps `iMaxGlobalInstances`/`iMaxTeamInstances`, `iCost`, the flags `bSpaceship`/`bAllowsNukes`, the espionage and sharing numbers `iNukeInterception`/`iTechShare`, `EveryoneSpecialUnit`/`EveryoneSpecialBuilding`, `iSuccessRate`, the `BonusProductionModifiers` list (`BonusType` + the shipped `iProductonModifier` spelling), and the presentation fields `Button`, `CreateSound`, `MovieDefineTag`. `bSpaceship` is what makes a project count as a spaceship part, and it must agree with the victory definition in `CIV4VictoryInfo.xml`.

## Espionage and Corporations (BtS Only)

`CIV4EspionageMissionInfo.xml` declares each espionage mission: `Type`, `Description`, `iCost`, `PrereqTech`, and the flags that decide what the mission is — `bIsPassive`, `bIsTwoPhases`, `bTargetsCity`, `bSelectPlot`, `bInvestigateCity`, `bSeeDemographics`, `bSeeResearch`, `bNoActiveMissions`, `bDestroyImprovement` — followed by `iVisibilityLevel` and a set of `i*CostFactor` and `i*Counter` fields for each effect (destroy building, unit, project, production; buy unit or city; steal treasury; insert culture; poison water; unhappiness; revolt; buy tech; switch civic; switch religion; player anarchy; counterespionage turns and modifier). A mission's `Type` is referenced from the espionage interface and from Python.

## Events and Quests (BtS Only)

Two files cooperate:

`CIV4EventTriggerInfos.xml` — entry `<EventTriggerInfo>` — is the *set of conditions* under which an event may fire. It carries `Type` (`EVENTTRIGGER_*`), `WorldNewsTexts`, `Text`/`TriggerTexts`, `Era`, `bSinglePlayer`, and the activation gates `iPercentGamesActive` (0–100, the chance the trigger exists in a given game), `iWeight` (relative firing weight; `-1` forces it whenever the other conditions hold, the convention for quest-completion triggers), `bRecurring`, `bTeam`, `bGlobal`; the population, landmass, difficulty and civic gates (`iMinPopulation`/`iMaxPopulation`, `iMinMapLandmass`/`iMinOurLandmass`/`iMaxOurLandmass`, `MinDifficulty`, `Civic`, `iMinTreasury`); the unit, building, plot, feature, terrain, improvement, bonus, route, religion and corporation requirements with their counts and weights; the `Events` list of `Event` ids plus `PrereqEvents` and the `OrPreReqs`/`AndPreReqs` technology gates; the BtS other-player gates (`bOtherPlayerWar`, `bOtherPlayerHasReligion`, `bOtherPlayerHasOtherReligion`, `bOtherPlayerAI`, `iOtherPlayerShareBorders`, `OtherPlayerHasTech`, `bPickCity`, `bPickOtherPlayerCity`, `bShowPlot`); and the BtS Python hooks `PythonCanDo`, `PythonCanDoCity`, `PythonCanDoUnit` (eligibility checks) and `PythonCallback`.

`CIV4EventInfos.xml` — entry `<EventInfo>` — is the *event and its consequences*: the event's choices. `Type` (`EVENT_*`), `Description`, `LocalInfoText`, `WorldNewsTexts`, `OtherPlayerPopup`, `QuestFailText`, and the BtS flags `bQuest`, `bGlobal`, `bTeam`, `bPickCity`, `bPickOtherPlayerCity`, `bDeclareWar`, `bGoldenAge`, `bDisbandUnit`. The consequences are a long field set: gold and culture (`iGold`, `bGoldToPlayer`, `iRandomGold`, `iCulture`, `iEspionagePoints`, `iFreeUnitSupport`, `iInflationMod`, `iSpaceProductionMod`), tech (`Tech`, `TechFlavors`, `iTechPercent`, `iTechCostPercent`, `iTechMinTurnsLeft`, `PrereqTech`), units (`UnitClass`, `iNumFreeUnits`, `iUnitExperience`, `iUnitImmobileTurns`, `UnitPromotion`, `UnitName`, `UnitCombatPromotions`, `UnitClassPromotions`), buildings (`BuildingClass`, `iBuildingChange`, `BuildingExtraYields`, `BuildingExtraCommerces`, `BuildingExtraHappies`, `BuildingExtraHealths`), city state (`iHappy`, `iHealth`, `iHurryAnger`, `iHappyTurns`, `iRevoltTurns`, `iFood`, `iFoodPercent`, `FreeSpecialistCounts`), plot state (`FeatureType`/`iFeatureChange`, `ImprovementType`/`iImprovementChange`, `BonusType`/`iBonusChange`, `RouteType`/`iRouteChange`, `BonusRevealed`, `BonusGift`, `PlotExtraYields`), diplomacy and population (`iConvertOwnCities`, `iConvertOtherCities`, `iOurAttitudeModifier`, `iAttitudeModifier`, `iTheirEnemyAttitudeModifier`, `iPopulationChange`), the follow-up chain (`AdditionalEvents`, `EventTimes`, `ClearEvents`), and the Python and presentation fields `PythonCallback`, `PythonExpireCheck`, `PythonCanDo`, `PythonHelp`, `Button`, `iAIValue`.

Design notes:

- `PythonCallback` in `Civ4EventInfos.xml` is the function called when the event happens; `PythonCallback` in `Civ4EventTriggerInfos.xml` is a different hook (fired when the trigger activates) and is unused by the shipped content. Do not conflate them.
- Choices that only one player may take, or that require a technology, are expressed as `PrereqTech` on the choice, so the player sees the option greyed rather than absent.
- The trigger's Python eligibility functions live in the module named by `Assets\Python\EntryPoints\CvRandomEventInterface.py`, which the mod replaces if it adds events.
- Quests are ordinary events with a `QuestFailText` and a forced-completion trigger; the quest-start and quest-complete triggers are matched by a shared quest id in the Python side.

## Saved-Game and Compatibility Consequences

- Content is referenced by index in a save. Inserting rows into a table that saves reference — units, buildings, techs, and the game-info tables generally — shifts indices and corrupts existing saves. Adding entries at the *end* of a table is the safest pattern, and even that is not guaranteed.
- Adding a leader, unit, or building to a civilization changes the set the save expects; adding the content to an existing game is unsupported.
- A mod that only replaces art or text rows is compatible with an existing save.
- Multiplayer requires the same mod set on every client; divergent content desynchronises the game.
