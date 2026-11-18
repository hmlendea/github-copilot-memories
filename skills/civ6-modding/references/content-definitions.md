# Content Definitions

Civ6 content is a set of tables keyed by string. Add `Types`, then the content row, then the association rows, then the ability/modifier attachment, then text and icons.

## Naming

```
CIVILIZATION_<NAME>      LEADER_<NAME>          TRAIT_<NAME>
UNIT_<NAME>              UNIT_<CIV>_<NAME>      PROMOTION_CLASS_<NAME>
BUILDING_<NAME>          DISTRICT_<NAME>        IMPROVEMENT_<NAME>
RESOURCE_<NAME>          FEATURE_<NAME>         TERRAIN_<NAME>
POLICY_<NAME>            BELIEF_<NAME>          GOVERNMENT_<NAME>
TECH_<NAME>              CIVIC_<NAME>           PROJECT_<NAME>
GREAT_PERSON_<NAME>      GREAT_PERSON_CLASS_<NAME>
MODIFIER_<NAME>          REQUIREMENT_<NAME>     LOC_<OBJECT>_<FIELD>
```

`Type` strings are globally unique across all enabled mods. Prefix with the mod name — `BUILDING_MYMOD_LIBRARY`, never a bare `BUILDING_LIBRARY`. `LOC_*` keys must match the text rows in `UpdateText`.

## Civilizations

Registration chain: `Types` → `Civilizations` → `CivilizationTraits` (the association table, name **without** an underscore) → city names, colours, and start bias rows.

```sql
INSERT INTO Types (Type, Kind) VALUES ('CIVILIZATION_MYMOD', 'KIND_CIVILIZATION');

INSERT INTO Civilizations (CivilizationType, Name, Description, Adjective, StartingCivilizationLevelType,
                           RandomCityNameDepth, Ethnicity)
VALUES ('CIVILIZATION_MYMOD', 'LOC_CIVILIZATION_MYMOD_NAME', 'LOC_CIVILIZATION_MYMOD_DESCRIPTION',
        'LOC_CIVILIZATION_MYMOD_ADJECTIVE', 'CIVILIZATION_LEVEL_FULL_CIV', 10, 'ETHNICITY_EURO');

INSERT INTO CivilizationTraits (CivilizationType, TraitType)
VALUES ('CIVILIZATION_MYMOD', 'TRAIT_CIVILIZATION_MYMOD');

INSERT INTO Traits (TraitType, Name, Description)
VALUES ('TRAIT_CIVILIZATION_MYMOD', 'LOC_TRAIT_CIVILIZATION_MYMOD_NAME',
        'LOC_TRAIT_CIVILIZATION_MYMOD_DESCRIPTION');
```

Also required for a playable civilization:
- `CivilizationLeaders` (`CivilizationType`, `LeaderType`, `CapitalName`) — the leader-to-civilization link; without it the pair never appears in setup.
- `CityNames` (`CivilizationType`, `CityName`) — the UI reads them for city naming and the AI for expansion.
- `PlayerColors` (`Type`, `Usage`, `PrimaryColor`, `SecondaryColor`, `Alt1*`…`Alt3*`) — the `Type` is the leader or civilization, the colours are `COLOR_STANDARD_*` keys. Missing colours render placeholder colours.
- `Players` rows per expansion domain (`Players:Expansion1_Players`, `Players:Expansion2_Players`) for setup-screen presentation: icon, portrait, background, and the ability name/description/icon fields. A civ that loads but shows no leader ability text is missing these.
- `CivilizationInfo` (`CivilizationType`, `Header`, `Caption`, `SortIndex`) for the Civilopedia info block.
- `StartBias*` tables (`StartBiasTerrains`, `StartBiasFeatures`, `StartBiasResources`, `StartBiasRivers`) — optional, but a full civ usually names one.
- `Civilization_Religions` or a preferred religion where the design wants one.

## Leaders

Registration chain: `Types` → `Leaders` → `LeaderTraits` (leader ability, plus AI-flavour traits) → `CivilizationLeaders` → agendas and quotes.

```sql
INSERT INTO Types (Type, Kind) VALUES ('LEADER_MYMOD', 'KIND_LEADER');

INSERT INTO Leaders (LeaderType, Name, InheritFrom, SceneLayers, Sex)
VALUES ('LEADER_MYMOD', 'LOC_LEADER_MYMOD_NAME', 'LEADER_DEFAULT', '4', 'Male');

INSERT INTO CivilizationLeaders (CivilizationType, LeaderType, CapitalName)
VALUES ('CIVILIZATION_MYMOD', 'LEADER_MYMOD', 'LOC_CITY_NAME_MYMOD_CAPITAL');

INSERT INTO LeaderTraits (LeaderType, TraitType) VALUES ('LEADER_MYMOD', 'TRAIT_LEADER_MYMOD');
```

- `SceneLayers` is a numeric layer count (vanilla rows use values such as `4`), not a scene id string. Reuse a vanilla value unless custom art is authored (`ui-and-art.md`).
- `InheritFrom` shortens the row set by inheriting another leader's defaults; `LEADER_DEFAULT` is the usual base.
- A playable leader also needs AI-flavour traits in `LeaderTraits` (for example `TRAIT_LEADER_SCIENCE_MAJOR_CIV`, `TRAIT_LEADER_LOW_RELIGIOUS_PREFERENCE`); without them the AI has no agenda-driven behaviour and may not pick the leader.
- Agendas need `Types` (`KIND_TRAIT` for the agenda trait), `Agendas`, `AgendaModifiers`, and the matching `HistoricalAgendas` row for the AI to use them.
- `LeaderQuotes` supplies the first-meeting quote and its `QuoteAudio` key; absent rows mean silence, not an error.
- `MomentIllustrations` rows give the unique-unit/unique-building historical-moment images; absent rows mean the defaults.

## Traits and Abilities

A trait is the attachment point for modifiers:

```sql
INSERT INTO Types (Type, Kind) VALUES ('TRAIT_CIVILIZATION_MYMOD', 'KIND_TRAIT');
INSERT INTO Traits (TraitType, Name, Description)
VALUES ('TRAIT_CIVILIZATION_MYMOD', 'LOC_TRAIT_CIVILIZATION_MYMOD_NAME',
        'LOC_TRAIT_CIVILIZATION_MYMOD_DESCRIPTION');
INSERT INTO CivilizationTraits (CivilizationType, TraitType)
VALUES ('CIVILIZATION_MYMOD', 'TRAIT_CIVILIZATION_MYMOD');
```

`CivilizationTraits` strings are `TRAIT_*` values, association only. Do not confuse it with the similarly named `Traits` content table: the trait needs a row in `Traits` for its text, a row in `CivilizationTraits` or `LeaderTraits` to be granted, and rows in `TraitModifiers` to do anything (`modifiers-and-requirements.md`).

## Units

```sql
INSERT INTO Types (Type, Kind) VALUES ('UNIT_MYMOD_SCOUT', 'KIND_UNIT');
INSERT INTO Units (UnitType, Name, Description, Cost, Maintenance, Combat, RangedCombat, Range,
                   BaseMoves, BaseSightRange, Domain, FormationClass, PromotionClass, PrereqTech)
VALUES ('UNIT_MYMOD_SCOUT', 'LOC_UNIT_MYMOD_SCOUT_NAME', 'LOC_UNIT_MYMOD_SCOUT_DESCRIPTION',
        40, 1, 10, 0, 0, 3, 3, 'DOMAIN_LAND', 'FORMATION_CLASS_LAND_COMBAT',
        'PROMOTION_CLASS_RECON', 'TECH_ANIMAL_HUSBANDRY');

INSERT INTO TypeTags (Type, Tag) VALUES
  ('UNIT_MYMOD_SCOUT', 'CLASS_RECON'),
  ('UNIT_MYMOD_SCOUT', 'CLASS_LAND_CIVILIAN'); -- only if the design wants civilian treatment

INSERT INTO UnitAiInfos (UnitType, AiType) VALUES
  ('UNIT_MYMOD_SCOUT', 'UNITAI_COMBAT'),
  ('UNIT_MYMOD_SCOUT', 'UNITTYPE_LAND_COMBAT');
```

Supporting rows most unit designs need — verified against published content mods:

| Table | Purpose |
|-------|---------|
| `TypeTags` | Class membership (`CLASS_SIEGE`, `CLASS_RANGED`, `CLASS_RECON`, `CLASS_SUPPORT`, `CLASS_DRONE`, …); drives AI, filters, and promotion eligibility |
| `Tags` + `Vocabulary` | Declares a mod-specific `ABILITY_CLASS` tag before using it in `TypeTags` |
| `UnitAiInfos` | AI roles (`UNITAI_COMBAT`, `UNITTYPE_RANGED`, `UNITTYPE_SIEGE`, `UNITTYPE_SIEGE_SUPPORT`, …) |
| `UnitReplaces` | `CivUniqueUnitType` → `ReplacesUnitType` for unique units |
| `UnitUpgrades` | Upgrade path |
| `UnitAbilities` + `UnitAbilityModifiers` | Ability text and the modifiers the ability carries |
| `Units_XP2` | Gathering Storm fields (`CanEarnExperience`, `CanFormMilitaryFormation`, strategic-resource costs) |
| `Unit_BuildingPrereqs`, `Unit_BuildingPrereqs`-style rows | Requires a building |
| `MomentIllustrations` | Historical-moment image for a unique unit |

A unit with no `TypeTags` and no `UnitAiInfos` rows loads and can be spawned by script, yet the AI will never build or use it.

## Buildings and Districts

```sql
INSERT INTO Types (Type, Kind) VALUES ('BUILDING_MYMOD_LIBRARY', 'KIND_BUILDING');
INSERT INTO Buildings (BuildingType, Name, Description, Cost, PrereqDistrict, PrereqTech,
                       Maintenance, Housing, PurchaseYield, AdvisorType, TraitType)
VALUES ('BUILDING_MYMOD_LIBRARY', 'LOC_BUILDING_MYMOD_LIBRARY_NAME', 'LOC_BUILDING_MYMOD_LIBRARY_DESCRIPTION',
        120, 'DISTRICT_CITY_CENTER', 'TECH_WRITING', 1, 0, 'YIELD_GOLD', 'ADVISOR_GENERIC',
        'TRAIT_CIVILIZATION_BUILDING_MYMOD_LIBRARY');

INSERT INTO Building_YieldChanges (BuildingType, YieldType, YieldChange)
VALUES ('BUILDING_MYMOD_LIBRARY', 'YIELD_SCIENCE', 3);

INSERT INTO BuildingModifiers (BuildingType, ModifierId)
VALUES ('BUILDING_MYMOD_LIBRARY', 'MYMOD_LIBRARY_PRODUCTION_BONUS');
```

- `PrereqTech` **or** `PrereqCivic`, never both, plus `PrereqDistrict` to place it in a district; a new district needs its own `Districts` row (`KIND_DISTRICT`) plus trait, modifier, and adjacency rows whose exact names you must copy from a vanilla district.
- `TraitType` marks the building as a civilization-unique building; it must also be granted by a `TRAIT_CIVILIZATION_BUILDING_*` trait in `CivilizationTraits` and attached with `TraitModifiers` if it does anything.
- `MaxPlayerInstances` = `1` for national wonders, `InternalOnly` = `1` for hidden helper buildings, `RequiresPlacement` for district-placement requirements.
- Flat yields go in `Building_YieldChanges` (`YieldChange`); percentage or conditional yields go through modifiers.
- Buildings are also the carriers of wonders: a wonder is a `Buildings` row with the wonder flags and a `BuildingModifiers` payload.

## Improvements, Resources, Features, Terrain

Each has the same shape: `Types` row, content row, then association rows, then modifiers.

| Object | Content table | Association pattern |
|--------|---------------|---------------------|
| Improvement | `Improvements` | `<Object>_ValidTerrains`, `<Object>_ValidFeatures`, `<Object>_ValidResources`, `<Object>_YieldChanges`, `<Object>Modifiers` |
| Resource | `Resources` | visibility/terrain/feature associations plus per-ruleset rows |
| Feature | `Features` | terrain validity, yield changes, removal rules |
| Terrain | `Terrains` | yield changes, valid resources |

The pattern is consistent but the exact names have changed across patches and differ per ruleset, so copy the association rows from the vanilla object closest to yours rather than from any guide — including this one. A missing `<Object>_ValidTerrains` row usually means the improvement can never be built, and the UI shows no reason.

## Policies, Beliefs, Governments, Civics, Technologies

| Object | Tables |
|--------|--------|
| Technology | `Technologies` (`KIND_TECHNOLOGY`), prerequisite rows, modifier attachments, boost rows |
| Civic | `Civics` (`KIND_CIVIC`), prerequisite rows, modifier attachments, boost rows |
| Policy | `Policies` (`KIND_POLICY`), modifier attachments, building-prerequisite rows |
| Belief | `Beliefs` (`KIND_BELIEF`), modifier attachments |
| Government | `Governments` (`KIND_GOVERNMENT`), modifier attachments, slot-count rows |

Boost (Eureka/Inspiration) rows are the usual reason a new tech or civic feels unreachable: without one the game still allows research, but the UI shows an empty trigger and the AI weighting changes. Names again follow the `<Object>_<Association>` pattern; copy from vanilla.

## Great People

`GreatPersonIndividuals` rows (`KIND_GREAT_PERSON_INDIVIDUAL`) are attached to a great-person class and an era, and grant their effect through a great-person action modifier table. Birth modifiers and icon rows complete the presentation. Copy the whole vanilla row set for one individual and rename it; the table names are numerous and none of them are optional if the individual is to appear, be earned, and activate.

## Removing and Altering Vanilla Content

```sql
UPDATE Units SET Cost = 30 WHERE UnitType = 'UNIT_WARRIOR';
DELETE FROM Units WHERE UnitType = 'UNIT_MYMOD_SCOUT';
```

- Prefer `UPDATE` to disabling: leaving the row means the AI and UI keep working.
- Deleting a row does not delete its `Types` row; a dangling type confuses UI iteration and AI. Delete the `Types` row as well, or better, keep both and make the object unreachable through prerequisites.
- Never delete a `Types` row another vanilla row still references; that is exactly the dangling-key failure the logs report.
- Altering a vanilla ability means editing the attached `Modifiers`/`ModifierArguments`, not the content row.