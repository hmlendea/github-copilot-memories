# Content Definitions

CivBE content is a graph of `Type` strings and association tables, exactly as in Civ5. Add the class row, then the object row, then the associations, then the text and the icons. Column lists below are the ones the shipped files and the community tutorials confirm; treat any column not shown here as present in the vanilla row and copy it from the analogue.

## Naming

```
CIVILIZATION_<NAME>     BUILDINGCLASS_<NAME>     BUILDING_<NAME>
LEADER_<NAME>           UNITCLASS_<NAME>         UNIT_<CIV>_<NAME>
TRAIT_<NAME>            VIRTUE_<NAME>            AFFINITY_<NAME>
TECH_<NAME>             RESOURCE_<NAME>          IMPROVEMENT_<NAME>
QUEST_<NAME>            ARTIFACT_<NAME>          COVERT_OPERATION_<NAME>
MARVEL_<NAME>           SATELLITE_<NAME>         ORBITAL_<NAME>
PROMOTION_<NAME>        PLAYERCOLOR_<NAME>       TXT_KEY_<OBJECT>_<FIELD>
```

`Type` values are globally unique across all enabled mods. Prefix with the mod or sponsor name — `BUILDING_MYMOD_LAB`, never a bare `BUILDING_LAB`. Never reuse a vanilla `Type` to "override" it; that is `<Update>`/`<Replace>`'s job and an `INSERT` collision silently aborts that part of the file.

## Sponsors

A sponsor is CivBE's civilization. The community tutorial `Custom Sponsor Tutorial` lists the full row set needed for one to appear on the sponsor-select screen; the annotation thread `Fully Commented/Annotated Sponsor files` publishes a fully commented example.

```xml
<GameData>
  <Civilizations>
    <Row>
      <Type>CIVILIZATION_MYMOD</Type>
      <Description>TXT_KEY_CIV_MYMOD_DESC</Description>
      <ShortDescription>TXT_KEY_CIV_MYMOD_SHORT_DESC</ShortDescription>
      <Adjective>TXT_KEY_CIV_MYMOD_ADJECTIVE</Adjective>
      <CivilopediaTag>TXT_KEY_CIV_MYMOD</CivilopediaTag>
      <DefaultPlayerColor>PLAYERCOLOR_ARC</DefaultPlayerColor>
      <ArtDefineTag>ART_DEF_CIVILIZATION_ARC</ArtDefineTag>
      <ArtStyleType>ARTSTYLE_ASIAN</ArtStyleType>
      <PortraitIndex>0</PortraitIndex>
      <IconAtlas>CIV_COLOR_ATLAS_MYMOD</IconAtlas>
      <AlphaIconAtlas>CIV_ALPHA_ATLAS_MYMOD</AlphaIconAtlas>
      <GradientIconAtlas>CIV_GRADIENT_ATLAS</GradientIconAtlas>
      <GlowIconAtlas>CIV_GLOW_ATLAS</GlowIconAtlas>
      <MapImage/>
      <ArtStyleSuffix>_ASIA</ArtStyleSuffix>
      <ArtStylePrefix>ASIAN </ArtStylePrefix>
      <IntroductionQuote>TXT_KEY_CIV_INTRO_MYMOD_TEXT_%</IntroductionQuote>
      <IntroductionImage>DOM_MyMod.dds</IntroductionImage>
      <IntroductionAudio>AS2D_DOM_SPEECH_UNITED_STATES</IntroductionAudio>
      <Personality>PERSONALITY_BRASILIA</Personality>
    </Row>
  </Civilizations>
  <Civilization_CityNames>
    <Row><CivilizationType>CIVILIZATION_MYMOD</CivilizationType><CityName>TXT_KEY_CITY_NAME_MYMOD_1</CityName></Row>
  </Civilization_CityNames>
  <Civilization_FreeBuildingClasses>
    <Row><CivilizationType>CIVILIZATION_MYMOD</CivilizationType><BuildingClassType>BUILDINGCLASS_HEADQUARTERS</BuildingClassType></Row>
  </Civilization_FreeBuildingClasses>
  <Civilization_FreeTechs>
    <Row><CivilizationType>CIVILIZATION_MYMOD</CivilizationType><TechType>TECH_HABITATION</TechType></Row>
  </Civilization_FreeTechs>
  <Civilization_Leaders>
    <Row><CivilizationType>CIVILIZATION_MYMOD</CivilizationType><LeaderheadType>LEADER_ARC</LeaderheadType></Row>
  </Civilization_Leaders>
  <Civilization_SpyNames>
    <Row><CivilizationType>CIVILIZATION_MYMOD</CivilizationType><SpyName>TXT_KEY_SPY_NAME_MYMOD_0</SpyName></Row>
  </Civilization_SpyNames>
  <Civilization_UnitClassOverrides>
    <Row><CivilizationType>CIVILIZATION_MYMOD</CivilizationType><UnitClassType>UNITCLASS_ALIEN_FLYER</UnitClassType><UnitType/></Row>
  </Civilization_UnitClassOverrides>
</GameData>
```

Field notes, as documented by the tutorial author:

| Column | Meaning and caution |
|--------|---------------------|
| `Type` | The key every other table references. |
| `Description` / `ShortDescription` / `Adjective` | `TXT_KEY_*` keys, never literal text. The adjective is applied to units. |
| `CivilopediaTag` | The Civilopedia entry key. |
| `DefaultPlayerColor` | A `PLAYERCOLOR_*` key. Reusing a vanilla one is the fast path; a custom set needs its own row and icons. |
| `ArtDefineTag` | The art definition used for interface art. An unknown value produces default or missing art, not an error. |
| `IconAtlas` / `AlphaIconAtlas` | Keys defined by the mod's `IconTextureAtlases` rows. The alpha atlas is the recoloured variant the UI uses in some places. |
| `GradientIconAtlas` / `GlowIconAtlas` / `MapImage` | Reported as unused or vestigial; the tutorial author set them to vanilla values and saw no effect. |
| `IntroductionQuote` with `%` | The `%` is substituted with an index, so the game looks up `..._0`, `..._1`, and so on. This is how multiple greetings per event are authored. |
| `IntroductionImage` / `IntroductionAudio` | The load-screen image and audio. Vanilla sponsors are largely silent, so a vanilla `AS2D_*` key is the safe value. |
| `Personality` | Present here, but the author reports the effective personality is set elsewhere; verify before relying on it. |

Also required, and simple to overlook:

- **The leader link determines the ability.** Sponsor abilities in the shipped game are attached to the leader, so a sponsor reusing `LEADER_ARC` will show ARC's ability regardless of its own rows. Author a leader, or override the trait deliberately.
- **The free building and free tech rows are mandatory even when the sponsor grants nothing**, because every sponsor starts with a headquarters building and the central Habitation technology.
- **City names: supply approximately twenty.** Vanilla sponsors carry nineteen or twenty.
- **Spy names** feed covert operations (and, in Rising Tide, the expanded covert system).
- **`Civilization_UnitClassOverrides` with an empty `UnitType`** is how vanilla sponsors are prevented from spawning the alien flyer.

## Leaders

Leaders are the source of the sponsor ability and of the greeting and load-screen text. The trait that carries the ability is the part that matters mechanically:

```xml
<LeaderheadArtInfo>...</LeaderheadArtInfo>
<Traits>
  <Row><Type>TRAIT_MYMOD_ABILITY</Type><Description>TXT_KEY_TRAIT_MYMOD</Description><ShortDescription>TXT_KEY_TRAIT_MYMOD_SHORT</ShortDescription></Row>
</Traits>
```

Attach the trait to the leader through the leader's own row set, and prefer reusing a vanilla leaderhead when custom art is not in scope (`ui-and-art.md`).

## Units

Two tables, in order.

```xml
<GameData>
  <UnitClasses>
    <Row>
      <Type>UNITCLASS_MYMOD_SCOUT</Type>
      <Description>TXT_KEY_UNIT_MYMOD_SCOUT_DESC</Description>
      <DefaultUnit>UNIT_MYMOD_SCOUT</DefaultUnit>
    </Row>
  </UnitClasses>
  <Units>
    <Row>
      <Type>UNIT_MYMOD_SCOUT</Type>
      <Class>UNITCLASS_MYMOD_SCOUT</Class>
      <Combat>3</Combat>
      <Cost>25</Cost>
      <PrereqTech>TECH_HABITATION</PrereqTech>
      <Description>TXT_KEY_UNIT_MYMOD_SCOUT_DESC</Description>
      <Civilopedia>TXT_KEY_UNIT_MYMOD_PEDIA</Civilopedia>
      <Help>TXT_KEY_UNIT_MYMOD_HELP</Help>
      <Moves>2</Moves>
      <CombatClass>UNITCOMBAT_MELEE</CombatClass>
      <Domain>DOMAIN_LAND</Domain>
      <DefaultUnitAI>UNITAI_ATTACK</DefaultUnitAI>
      <MilitarySupport>true</MilitarySupport>
      <MilitaryProduction>true</MilitaryProduction>
      <Pillage>true</Pillage>
      <AdvancedStartCost>25</AdvancedStartCost>
      <XPValueAttack>1</XPValueAttack>
      <XPValueDefense>1</XPValueDefense>
      <Conscription>1</Conscription>
      <UnitArtInfo>ART_DEF_UNIT_LEV_DESTROYER</UnitArtInfo>
      <MoveRate>WHEELED</MoveRate>
    </Row>
  </Units>
</GameData>
```

The Fandom *How to Create Units* tutorial is the worked example, and it also records two follow-up answers worth keeping:

- **Ranged units** add `<Range>` (the reach) and `<RangedCombat>` (the ranged strength).
- **Hover units** use `DOMAIN_HOVER` in place of `DOMAIN_LAND`. CivBE's `DOMAIN_*` vocabulary is the base-game one plus the Beyond-Earth additions; confirm the value against the shipped `CivBEUnits.xml` rather than guessing.
- `UnitArtInfo` names an art definition; reuse a vanilla one unless you are authoring models.

`UnitClass` must exist before `Units` references it, and a unit added to a vanilla class requires `<Civilization_UnitClassOverrides>` or a replacement row to become buildable by a given sponsor.

## Buildings, Technologies, and the Tech Web

- **Buildings** follow the Civ5 shape: `BuildingClasses` before `Buildings`, with `PrereqTech` pointing into the tech web. A building with no reachable prerequisite never appears in the build list.
- **Technologies** are the tech web. Beyond the Civ5 columns, the web's layout matters: each technology declares its position and its links, so a new technology that is not connected to a parent is unreachable. Copy a vanilla technology from the same ring and edit the link values.
- **Affinities** (Harmony, Purity, Supremacy) are tracked per player and gate units, buildings, and upgrades. Content can require an affinity level; the affinity tables define the thresholds and the names the UI displays.
- **Virtues** replace Civ5's social policies and have their own tree and depth structure. The deletion hazard applies in full: removing a virtue row gaps the tree and hides everything after it.

## Colonists, Cargo, and Spacecraft

The starting loadout is a first-class system, not a Civ5 starting-unit list: **colonists** supply the initial population mix, **cargo** supplies the starting bonus, and **spacecraft** supplies the map-level advantage. Each is its own table set with its own text and icons, and a sponsor's identity is largely expressed through which of these it improves. Add a new colonist, cargo option, or spacecraft by copying the vanilla row of the nearest analogue and supplying every referenced key.

## Quests, Artifacts, and Marvels

- **Quests** are the random and scripted objectives, each with its own definition rows and its Lua hooks (`lua-scripting.md`). A quest needs its trigger, its text in every state, and its reward.
- **Artifacts** are the collectible rewards carried over from Civ5's archaeology pattern and expanded in Rising Tide, where they become a resource to be spent in the artifact system.
- **Marvels** are Rising Tide content: multi-stage constructions that require contributions from several civilizations. Anything built on the marvel tables fails without Rising Tide.

## Covert Operations, Satellites, and Orbital Units

- **Covert operations** (spying) are defined by their own operation table set with costs, durations, and effects; the *Enhanced Covert Ops* mod is the worked example of extending them.
- **Satellites and orbital units** occupy the orbital layer and need the orbital-specific domain and layer columns, plus their own launch and duration values. Confirm the exact column names against the shipped files; the community coverage of this system is the thinnest of any CivBE feature.

## Resources, Terrains, Biomes, and Improvements

- **Resources** need their `ResourceClass` and the yield columns, plus the reveal technology.
- **Terrains and features** include the Beyond-Earth additions (miasma is a feature with its own damage and affinity interaction) and the biome variants. Editing them affects every map, so a mod that changes a terrain is incompatible with another that does.
- **Improvements** need their tech prerequisite and their builder unit's capability. Miasma repulsion, terrascapes, and the affinity-specific improvements all follow the same pattern.

## Yields

CivBE's yields are Energy, Science, Culture, Food, Production, Health, and (in Rising Tide) Diplomatic Capital. A new yield cannot be invented in data — the engine knows a fixed set — so content adds or converts existing yields rather than defining new ones.
