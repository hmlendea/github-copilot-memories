# XML Reference: Files, Schemas, Text, and Conventions

## How the XML Layer Works

XML in Civ4 is not a data format the engine interprets loosely — it is the serialised form of the engine's own info classes. Each file corresponds to one class, each entry in the file to one instance of that class, and each tag to one member. For this reason:

- **One file per table, and a mod's file replaces the whole table.** There is no row-level update. Changing one unit's cost means shipping a complete `CIV4UnitInfos.xml`.
- **Entry tags are position-sensitive.** The file is validated against its `*Schema.xml`, which is an ordered sequence; the loader stops at the first tag out of order, unknown, or duplicated.
- **Tag prefixes are typed.** `bXxx` is a boolean (`0`/`1`), `iXxx` an integer, `szXxx` a string, and an unprefixed tag is usually an enum `Type` name, a `TXT_KEY_`, or the entry's own `Type`. Those types are not documentation: they come from the schema's `dt:type` attributes, and a value outside the type aborts the file.
- **Empty list tags are self-closed**, as in `<FreeTechs/>`. Omitting the tag entirely is a load failure; an empty list is valid.
- **Enums are `Type` strings or short literal words**, both uppercase (`DOMAIN_LAND`, `UNITCOMBAT_MELEE`, `ARTSTYLE_EUROPEAN`).
- **`NONE` is a real value** and distinct from an empty tag. Where the schema accepts an optional reference, `NONE` means "not set".

## Encoding and Whitespace

Match the encoding of the file being copied. Base BtS tables declare `ISO-8859-1` in the XML declaration, and text files are commonly `ISO-8859-1` or Windows-1252. Writing `UTF-8` into a file whose declaration says otherwise, or vice versa, corrupts non-ASCII characters (accented leader and city names, the mana-like icons in the Civ4 font) and can abort the parse. Keeping the vanilla declaration and writing only ASCII is the safest default; use an explicit `UTF-8` declaration with a BOM for new text files that must carry non-ASCII characters on every platform.

Indentation is cosmetic except inside text values, where leading and trailing whitespace is preserved and displayed.

## File Index

`Assets\XML\` contains roughly 120 table files and their schemas, grouped by folder.

| Folder | Files |
|--------|-------|
| `XML\` (root) | `GlobalDefines.xml`, `GlobalDefinesAlt.xml`, `GlobalTypes.xml`, `PythonCallbackDefines.xml` |
| `XML\Art\` | `CIV4ArtDefines_Bonus`, `_Building`, `_Civilization`, `_Feature`, `_Improvement`, `_Interface`, `_Leaderhead`, `_Misc`, `_Movie`, `_Terrain`, `_Unit`; `CIV4MainMenus`; `CIV4RiverModelInfos`; `CIV4RouteModelInfos` |
| `XML\Audio\` | `Audio2DScripts`, `Audio3DScripts`, `AudioDefines`, `AudioSoundscapeScripts` |
| `XML\BasicInfos\` | `CIV4AttitudeInfos`, `CIV4BasicInfos`, `CIV4CalendarInfos`, `CIV4CityTabInfos`, `CIV4DenialInfos`, `CIV4DomainInfos`, `CIV4InvisibleInfos`, `CIV4MemoryInfos`, `CIV4MonthInfos`, `CIV4NewConceptInfos`, `CIV4SeasonInfos`, `CIV4UnitAIInfos`, `CIV4UnitCombatInfos` |
| `XML\Buildings\` | `CIV4BuildingClassInfos`, `CIV4BuildingInfos`, `CIV4CityLSystem`, `CIV4PlotLSystem`, `CIV4SpecialBuildingInfos` || `XML\Civilizations\` | `CIV4CivilizationInfos`, `CIV4LeaderHeadInfos`, `CIV4TraitInfos`, `CIV4UnitArtStyleTypeInfos` |
| `XML\Events\` | `CIV4EventInfos`, `CIV4EventTriggerInfos` |
| `XML\GameInfo\` | `CIV4CivicInfos`, `CIV4CivicOptionInfos`, `CIV4ClimateInfo`, `CIV4CommerceInfo`, `CIV4CorporationInfo`, `CIV4CultureLevelInfo`, `CIV4CursorInfo`, `CIV4DiplomacyInfos`, `CIV4EmphasizeInfos`, `CIV4EspionageMissionInfo`, `CIV4EraInfos`, `CIV4ForceControlInfos`, `CIV4GameOptionInfos`, `CIV4GameSpeedInfo`, `CIV4GoodyInfo`, `CIV4GraphicOptionInfos`, `CIV4HandicapInfo`, `CIV4Hints`, `CIV4HurryInfo`, `CIV4MPOptionInfos`, `CIV4PlayerOptionInfos`, `CIV4ProcessInfo`, `CIV4ProjectInfo`, `CIV4ReligionInfo`, `CIV4SeaLevelInfo`, `CIV4SpecialistInfos`, `CIV4TurnTimerInfo`, `CIV4UpKeepInfo`, `CIV4VictoryInfo`, `CIV4VoteInfo`, `CIV4VoteSourceInfos`, `CIV4WorldInfo` |
| `XML\Interface\` | `CIV4AdvisorInfos`, `CIV4CameraInfos`, `CIV4ColorVals`, `CIV4InterfaceModeInfos`, `CIV4PlayerColorInfos`, `CIV4SlideShowInfos`, `CIV4SlideShowRandomInfos`, `CIV4SpaceShipInfos`, `CIV4ThroneRoomInfos`, `CIV4ThroneRoomCameraInfos`, `CIV4ThroneRoomStyleInfos`, `CIV4WorldPickerInfos` |
| `XML\Misc\` | `CIV4AttachableInfos`, `CIV4CameraOverlayInfos`, `CIV4DetailManager`, `CIV4EffectInfos`, `CIV4QuestInfos`, `CIV4RiverInfos`, `CIV4RouteInfos`, `CIV4TerrainPlainInfos`, `CIV4TutorialInfos`, `CIV4WaterPlaneInfos` |
| `XML\Technologies\` | `CIV4TechInfos` |
| `XML\Terrain\` | `CIV4BonusClassInfos`, `CIV4BonusInfos`, `CIV4FeatureInfos`, `CIV4ImprovementInfos`, `CIV4SymbolMeshPaths`, `CIV4TerrainInfos`, `CIV4TerrainSettings`, `CIV4YieldInfos` |
| `XML\Units\` | `CIV4AnimationInfos`, `CIV4AnimationPathInfos`, `CIV4AutomateInfos`, `CIV4BuildInfos`, `CIV4CommandInfos`, `CIV4ControlInfos`, `CIV4EntityEventInfos`, `CIV4FormationInfos`, `CIV4MissionInfos`, `CIV4PromotionInfos`, `CIV4SpecialUnitInfos`, `CIV4UnitClassInfos`, `CIV4UnitInfos` |
| `XML\Text\` | every `*_CIV4GameText*.xml` and `*_CIV4GameTextInfos*.xml` file |
| Schemas | `CIV4GlobalDefinesSchema.xml`, `CIV4GlobalTypesSchema.xml`, `CIV4ArtDefinesSchema.xml`, `AudioDefinesSchema.xml`, `AudioScriptSchema.xml`, `CIV4BasicInfoSchema.xml`, `CIV4BuildingsSchema.xml`, `CIV4LSystemSchema.xml`, `CIV4CivilizationsSchema.xml`, `CIV4EventSchema.xml`, `CIV4GameInfoSchema.xml`, `CIV4InterfaceSchema.xml`, `CIV4MiscSchema.xml`, `CIV4TutorialSchema.xml`, `CIV4DetailManagerSchema.xml`, `CIV4TechnologiesSchema.xml`, `CIV4TerrainSchema.xml`, `CIV4FormationSchema.xml`, `CIV4UnitSchema.xml` |

`CIV4HurryInfo` defines the rush mechanics (`iGoldPerProduction`, `iProductionPerPopulation`, and the hurry type names) that the `Hurrys` lists on civics and buildings refer to. Builds vary in which auxiliary tables they ship, so treat the list above as the union Modiki documented and confirm against the install.

The Beyond the Sword additions — `CIV4CorporationInfo`, `CIV4EspionageMissionInfo`, `CIV4EventInfos`, `CIV4EventTriggerInfos`, `CIV4QuestInfos`, `CIV4UnitArtStyleTypeInfos`, `CIV4SpecialBuildingInfos` and their peers — must not be referenced by a mod intended for vanilla or Warlords. The engine loads only the files the installed expansion ships, so a reference to a BtS-only `Type` from a non-BtS mod dangles.

## Defines

`GlobalDefines.xml` and `GlobalDefinesAlt.xml` share one shape:

```xml
<Civ4Defines xmlns="x-schema:Civ4GlobalDefinesSchema.xml">
  <Define>
    <DefineName>MAX_NATIONAL_WONDERS_PER_CITY</DefineName>
    <iDefineIntVal>2</iDefineIntVal>
  </Define>
</Civ4Defines>
```

`GlobalDefinesXml` values are the engine's tuning constants: map limits, combat multipliers, growth thresholds, `MAX_NUM_UNITS_PER_PLOT`, and so on. `GlobalDefinesAlt.xml` exists specifically so a mod can override a handful of defines without owning `GlobalDefines.xml`, and the community convention is one `*_GlobalDefines.xml` per feature. A define that the engine does not read (a new name) is ignored; a define whose type is wrong (a string where an integer is expected) aborts the file.

`PythonCallbackDefines.xml` uses the same shape with `USE_*_CALLBACK` names and a `0`/`1` value.

## `GlobalTypes.xml`

Holds the enumerated type lists that other files reference by name: `ArtStyleTypes`, `UnitArtStyleTypes`, `CorporationTypes`, `EspionageMissionTypes` and the smaller fixed vocabularies. Adding a member here is how a new art style or a new corporation category is introduced, and the addition must precede every reference to it.

## `CIV4ArtDefines_*`

Each art-define file binds a `Type` to asset paths. Nothing renders until an object references one of these `Type` names.

```xml
<Civ4ArtDefines xmlns="x-schema:CIV4ArtDefinesSchema.xml">
  <UnitArtInfos>
    <UnitArtInfo>
      <Type>ART_DEF_UNIT_LION</Type>
      <Button>,Art/Interface/Buttons/Units/Lion.dds,Art/Interface/Buttons/Unit_Resource_Atlas.dds,6,5</Button>
      <fScale>0.61</fScale>
      <fInterfaceScale>1.3</fInterfaceScale>
      <bActAsLand>0</bActAsLand>
      <bActAsAir>0</bActAsAir>
      <NIF>Art/Units/Lion/Lion.nif</NIF>
      <KFM>Art/Units/Lion/Lion.kfm</KFM>
      <SHADERNIF>Art/Units/Lion/Lion_FX.nif</SHADERNIF>
      <ShadowDef>
        <ShadowNIF>Art/Units/01_UnitShadows/LionShadow.nif</ShadowNIF>
        <ShadowAttachNode>LionBip Spine1</ShadowAttachNode>
        <fShadowScale>1.0</fShadowScale>
      </ShadowDef>
      <fBattleDistance>0.35</fBattleDistance>
      <fRangedDeathTime>0.28</fRangedDeathTime>
      <bActAsRanged>0</bActAsRanged>
      <TrainSound>AS2D_UNIT_BUILD_UNIT</TrainSound>
      <AudioRunSounds>
        <AudioRunTypeLoop/>
        <AudioRunTypeEnd/>
      </AudioRunSounds>
    </UnitArtInfo>
  </UnitArtInfos>
</Civ4ArtDefines>
```

**The `Button` field is a five-part, comma-separated value** and it is the single most error-prone string in the game:

```
,Art/Interface/Buttons/Units/Lion.dds,Art/Interface/Buttons/Unit_Resource_Atlas.dds,6,5
 ^ 1: the button image (inline .dds)   ^ 3: atlas file   ^ 4: column  ^ 5: row
```

- The leading empty field is mandatory: the value begins with a comma.
- Field 1 is the standalone button; fields 2–1 are the atlas and the atlas cell `(column, row)`.
- The atlas is often the game font: `,Art/Interface/Buttons/...,Art/Interface/Buttons/Unit_Resource_Atlas.dds,6,5` names an atlas file, but a value of the form `,Art/.../Foo.dds,GameFont.tga,x,y` indexes the font sheet instead.

Other art-define families follow the same idea with different members: `CIV4ArtDefines_Building` (a `NIF` per era), `CIV4ArtDefines_Civilization` (flag `NIF` and decal), `CIV4ArtDefines_Leaderhead` (`NIF`, `KFM`, the background `NIF`, and the button), `CIV4ArtDefines_Improvement`, `CIV4ArtDefines_Bonus`, `CIV4ArtDefines_Feature`, `CIV4ArtDefines_Terrain`, `CIV4ArtDefines_Movie`, `CIV4ArtDefines_Interface` and `CIV4ArtDefines_Misc`. (Modiki's reference pages capitalise these `Civ4ArtDefines_*`; the shipped file names use `CIV4ArtDefines_*`.) A path is relative to the mounted asset root (`Art/...`), never absolute and never with a drive letter.

## Text

Civ4 text is not a separate row-per-language table; each entry carries every language inline, and the engine selects the column for the active language.

```xml
<Civ4GameText xmlns="http://www.firaxis.com">
  <TEXT>
    <Tag>TXT_KEY_UNIT_MYMOD_SWORDSMAN</Tag>
    <English>MyMod Swordsman</English>
    <French>Épéiste MyMod</French>
    <German>MyMod-Schwertkämpfer</German>
  </TEXT>
</Civ4GameText>
```

Rules and traps:

- Every file the engine reads under `Assets\XML\Text\` is loaded, so a mod can add its own `MyMod_CIV4GameText.xml` and never touch a vanilla text file. This is the one asset class where adding is as easy as editing.
- A missing language column falls back to `<English>`; if `<English>` is missing too, the literal `TXT_KEY_…` string is displayed.
- Tag names are global. Two files defining the same tag is a duplicate, and one wins.
- `Description`, `ShortDescription`, `Adjective`, `Civilopedia`, `Strategy`, `Help`, `Quote`, `Civilopedia` and popup strings throughout the XML tables are all `TXT_KEY_` references. Some fields (a `<City>` name, a `<UniqueName>`) accept either a literal string or a `TXT_KEY_`; a literal is not translated.
- The `[BOLD]`/`[\BOLD]` markup tags and the `%s1`, `%s2`, `%d1`, `%d2` placeholders in text rows are consumed by the engine and by Python; a wrong placeholder count is a formatting failure at display time, not at load, and the `%s`-style numbering is one-based.
- The Civ4 font carries a fixed set of icon glyphs addressable from text. Adding a new one means editing `GameFont.tga` and `GameFont_75.tga` together (see `references/interface-and-art.md`), which is why most mods reuse existing glyphs.

## Schema Validation

Every table file is validated against its `*Schema.xml` sibling. The schemas are written in **XML-Data** (`xmlns="urn:schemas-microsoft-com:xml-data"`, members typed with `dt:type="int"`, `"boolean"`, `"string"`), not XSD, and each declares its elements and the ordered sequence used for each entry. The practical consequences:

- **Order is enforced, not merely conventional.** `<Type>` first, then the text members, then the integers, then the booleans, then the lists — in the schema's declared order. Copying a vanilla entry preserves the order for free.
- **An unknown element is an error, not a warning.** A misspelled tag aborts the file.
- **A missing element is usually an error too.** Optional elements have schema defaults; everything else must be present, even if only as `0` or `NONE`.
- **Adding a new member requires an SDK change.** The schema must declare the element and the C++ info class must read and store it, so a new tag in the XML alone does nothing (`references/sdk-and-cpp.md`).

## Diagnostics for XML

- The loader logs to `<user dir>\Logs\init.log` and `Res.log`; a rejected file reports the file name and the offending line when logging is enabled.
- Because a rejected file leaves the table undefined, the in-game symptom is a missing unit, a `TXT_KEY_` in a tooltip, or an asset-less object rather than an error dialog.
- Third-party validators are widely used and recommended: an XML schema-aware editor catches tag order and spelling before the game is launched. Modiki's *Civ4 Useful Programs* page lists the community checkers and describes the community preference for a plain text editor over a specialised XML tool.
- When an XML edit seems to have no effect, first confirm the file is at the exact relative path the mod needs and that no earlier or later copy of the same table is shadowing it.
