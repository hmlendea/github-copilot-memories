---
name: civ6-modding
description: Use when creating or editing a Civilization VI mod, or when working with its ModBuddy project (.modinfo, FrontEndActions, InGameActions, ActionCriteria, criteria such as GameCoreInUse, RuleSetInUse, ModInUse and LeaderPlayable, Dependencies, References, Blocks), the UpdateDatabase, UpdateText, UpdateIcons, UpdateArt, UpdateColors, UpdateAudio, ImportFiles, AddGameplayScripts, AddUserInterfaces and ReplaceUIScript actions, SQLite database updates (SQL and GameData XML), the Types and Kinds registry, content tables (civilizations, leaders, traits, units, districts, buildings, improvements, resources, policies, beliefs, technologies, civics, great people), the modifier and requirement system (Modifiers, ModifierArguments, DynamicModifiers, EffectType and CollectionType, RequirementSets, RequirementSetRequirements, Requirements, RequirementArguments), gameplay and UI Lua (GameEvents, Events, LuaEvents, ExposedMembers, GameInfo, GlobalParameters, ContextPtr, Controls), icon atlases and art defines, localisation keys, WorldBuilder and the Asset Editor, the Cache database snapshots, log files, FireTuner, and common load failures. Covers Steam Workshop publishing, ruleset and expansion compatibility, load order, and what cannot be modded.
---

# Civilization VI Modding

Apply when authoring or reviewing content for **Sid Meier's Civilization VI** (Firaxis Games, 2016; Rise and Fall and Gathering Storm expansions). Civ6 replaced Civ5's integer `Type`/`ID` indirection with string keys throughout, split gameplay data and text into two SQLite databases, and moved almost all behaviour out of Lua into a data-driven **modifier and requirement system**. A Civ6 mod is therefore mostly rows, plus a small amount of Lua for what rows cannot express.

Source material: [Modding (Civ6)](https://civilization.fandom.com/wiki/Modding_(Civ6)) and its subpages (`Basics of Mod Creation`, `Advanced Modbuddy Concepts`, `How to Alter Base Game Content`, `How to Remove Base Game Content`, `Basic Mod/DLC Compatibility`, `How to Create a Civilization`, `How to Create a Unit`, `How to Create a Building`, `How to Create a Leader`, `How to Create a Technology or Civic`, `How to Create a Great Person`), the [Civ 6 Modding Wiki](https://sukritact.github.io/civilization-modding-wiki/civ-6/civ-6-index-database/) (an index of effect, requirement, and database articles, last updated in 2022), the [Civilization VI Modding Wiki by Jonathan Turnock](https://jonathanturnock.github.io/civ-vi-modding/docs/) (`SDK Installation`, `SDK Overview`, `FireTuner - Setup`, `Hello World Lua Mod`, `Lua Reference`), the Steam guide [Civilization VI - SQLite Modding](https://steamcommunity.com/sharedfiles/filedetails/?id=1968580787), and [Modiki](https://modiki.civfanatics.com/index.php?title=Main_Page). Treat Modiki as Civ5-era material: it documents the shared Civilisation modding vocabulary, not Civ6 tables. All of these sources predate the final patches; the shipped `Base/`, `DLC/Expansion1/`, and `DLC/Expansion2/` assets and the generated `Cache/DebugGameplay.sqlite` snapshot are authoritative whenever they disagree.

## Non-Negotiable Build Rules

1. **Never edit game files.** A mod is a folder under `Documents\My Games\Sid Meier's Civilization VI\Mods\<ModName>\` containing its own `.modinfo`. Anything written into `steamapps/common/Sid Meier's Civilization VI/` is destroyed by file verification and expansion patches; read those files as reference only.
2. **Nothing runs unless an action declares it.** Data needs `UpdateDatabase`, text needs `UpdateText`, icons need `UpdateIcons`, runtime files (UI Lua, DDS) need `ImportFiles`, cooked art needs `UpdateArt`, gameplay Lua needs `AddGameplayScripts`, and UI needs `AddUserInterfaces`. A file that exists in the mod folder but appears in no action is dead weight. `AddGameplayScripts` alone is also not enough: the file must additionally be listed in `<Files>`.
3. **Every action can be gated by a criteria.** An action with no `criteria` attribute or `<Criteria>` child runs under every game core and ruleset; an action bound to a criteria that does not match the running game never runs, silently. `GameCoreInUse` names the installed core (`Expansion1`, `Expansion2`), `RuleSetInUse` the active ruleset (`RULESET_EXPANSION_1`, `RULESET_EXPANSION_2`), and `ModInUse` another mod's GUID. This is the mechanism that replaces Civ5's DLC dependency for expansion-only content, and a mismatch is silent.
4. **Every object must be registered in `Types`.** `Types(Type, Kind)` is the root registry; a `Buildings` row whose `BuildingType` is absent from `Types` is invisible to the game. `Tags`/`TypeTags` additionally drive AI and UI classification for some kinds. Copy the vanilla `Kind` string rather than guessing.
5. **Register before you reference, and never duplicate an existing key.** Civ6 keys are strings with primary-key constraints; a plain `INSERT` of an existing key fails the statement and, depending on the engine path, the rest of the file. Use `UPDATE` to change a vanilla row, `INSERT OR REPLACE` to own it outright, and `DELETE` to remove it. Doubled definitions across mods are resolved by load order, last writer wins. Association tables are named after the owner ("CivilizationTraits", `LeaderTraits`, `BuildingModifiers`, `TraitModifiers") and their name is what matters — do not invent an underscore variant.
6. **Behaviour belongs in modifiers, not Lua.** `Modifiers` + `ModifierArguments` + `RequirementSets`/`Requirements` express conditions, yields, combat changes, grants, and adjacency, and they survive save/load, run on all clients, and appear in the UI. Reach for Lua only when the effect depends on state the modifier system cannot express.
7. **Text lives in a different database.** `LocalizedText` is not in the gameplay database, so adding text through `UpdateDatabase` does nothing useful. Ship it through `UpdateText`, one row per language, and use the `LOC_*` keys that the gameplay row names.
8. **Delete the `Cache` folder before judging a database change.** `DebugGameplay.sqlite` and `DebugLocalization.sqlite` are rebuilt at startup from the base data plus enabled mods; a stale snapshot is indistinguishable from a broken mod.
9. **Enable the tuner and read four logs.** In `AppOptions.txt` set `FullScreen 0` and `EnableTuner 1`. Then `modding.log` (loading, order, criteria), `Database.log` (SQL errors), `GameEffects.log` (modifier and requirement errors), and `Lua.log` (script output) explain nearly every failure; without them a design mistake and a wiring mistake look identical. Paths are `<user data>\Logs\`.
10. **State the ruleset and expansion requirements in the mod description.** Content built on `_XP1`/`_XP2` tables, or on vanilla rows that only exist in an expansion, produces load failures or silent gaps in the base game and in the other expansion.

## Layout

```
MyMod/
  MyMod.modinfo          # generated by ModBuddy; hand-editable, re-check after UI changes
  Data/                  # .sql or GameData .xml files        -> UpdateDatabase / UpdateColors
  Text/                  # LocalizedText rows (SQL or XML)    -> UpdateText
  Scripts/               # gameplay Lua                       -> AddGameplayScripts (+ Files)
  UI/                    # UI .xml + paired .lua             -> AddUserInterfaces, ImportFiles, ReplaceUIScript
  Icons/                 # .dds atlases + icon definition XML -> UpdateIcons, ImportFiles
  ArtDefs/               # .artdef asset definitions          -> cooked by the Asset Editor
  XLPs/, Geometries/     # art sources                        -> cooked output
  Platforms/Windows/     # BLPs and Wwise audio banks         -> UpdateArt, UpdateAudio
  Cooked/                # cooked art output                  -> referenced by the .dep
  MyMod.dep              # game dependency data listing art   -> UpdateArt
Build/                   # deploy output copied into the game's Mods folder
```

Generated `.modinfo` structure (ModBuddy writes it; the action list is the part that matters):

```xml
<Mod id="GUID" version="1">
  <Properties>
    <Name>LOC_MOD_MYMOD_NAME</Name>
    <Description>LOC_MOD_MYMOD_DESCRIPTION</Description>
    <Teaser>LOC_MOD_MYMOD_TEASER</Teaser>
    <Authors>…</Authors>
    <CompatibleVersions>1.2,2.0</CompatibleVersions>
    <AffectsSavedGames>1</AffectsSavedGames>
  </Properties>
  <ActionCriteria>
    <Criteria id="Expansion1"><GameCoreInUse>Expansion1</GameCoreInUse></Criteria>
    <Criteria id="Expansion2"><GameCoreInUse>Expansion2</GameCoreInUse></Criteria>
  </ActionCriteria>
  <Dependencies><Mod id="other-mod-guid" title="..."/></Dependencies>
  <References><Mod id="optional-mod-guid" title="..."/></References>
  <Blocks/>
  <FrontEndActions>
    <UpdateDatabase id="Setup"><File>Data/MyMod.sql</File></UpdateDatabase>
  </FrontEndActions>
  <InGameActions>
    <UpdateDatabase id="Data"><File>Data/MyMod.sql</File></UpdateDatabase>
    <UpdateDatabase id="DataXP2" criteria="Expansion2"><File>Data/MyMod_XP2.sql</File></UpdateDatabase>
    <UpdateText id="Text"><File>Text/MyMod_Text.xml</File></UpdateText>
    <UpdateIcons id="Icons"><File>Icons/MyMod_Icons.xml</File></UpdateIcons>
    <ImportFiles id="Runtime">
      <File>Icons/MyMod_Icons32.dds</File>
      <File>UI/MyPanel.lua</File>
    </ImportFiles>
    <AddGameplayScripts id="Scripts"><File>Scripts/MyMod.lua</File></AddGameplayScripts>
    <AddUserInterfaces id="UI">
      <Properties><Context>InGame</Context></Properties>
      <File>UI/MyPanel.xml</File>
    </AddUserInterfaces>
    <!-- optional: cooked art package, Wwise bank, colours, Lua context replacement -->
    <UpdateArt id="Art"><File>MyMod.dep</File></UpdateArt>
    <UpdateAudio id="Audio"><File>Platforms/Windows/Audio/MyModBanks.ini</File></UpdateAudio>
    <UpdateColors id="Colors"><File>Data/MyMod_Colors.xml</File></UpdateColors>
    <ReplaceUIScript id="ReplaceReports">
      <Properties><LoadOrder>99999</LoadOrder><LuaContext>ReportsList</LuaContext><LuaReplace>UI/MyReportsList.lua</LuaReplace></Properties>
    </ReplaceUIScript>
  </InGameActions>
  <LocalizedText>
    <Text id="LOC_MOD_MYMOD_NAME"><en_US>My Mod</en_US></Text>
  </LocalizedText>
  <Files>
    <File>Data/MyMod.sql</File>
    <File>Text/MyMod_Text.xml</File>
    <File>Scripts/MyMod.lua</File>
    <File>UI/MyPanel.xml</File>
    <File>UI/MyPanel.lua</File>
  </Files>
</Mod>
```

## Domain Map

| Need | Where | Reference |
|------|-------|-----------|
| SDK and ModBuddy, `.modinfo` action types, criteria and rulesets, dependencies and blocks, install paths, deployment, Workshop, load order, compatibility, failure catalogue | `MyMod.modinfo`, ModBuddy properties | `references/mod-packaging.md` |
| Gameplay and localisation databases, `Types` and `Kinds`, SQL and `GameData` XML semantics, update versus insert versus delete, cache snapshots, conflict queries, custom tables | `Data/` | `references/database-xml-sql.md` |
| Civilizations, leaders, traits, units, districts, buildings, improvements, resources, policies, beliefs, technologies, civics, boosts, great people, colours, city names | `Data/` tables | `references/content-definitions.md` |
| `Modifiers`, `ModifierArguments`, `DynamicModifiers`, attachment tables, `RequirementSets`, `Requirements`, effect and collection naming, diagnosing no-effect modifiers | `Data/` tables | `references/modifiers-and-requirements.md` |
| Gameplay versus UI Lua, `GameEvents`, `Events`, `LuaEvents`, `ExposedMembers`, `GameInfo`, `GlobalParameters`, `Modding.IsModActive`, `DB.Query`, object lookups, persistence, per-turn cost | `Scripts/`, `UI/` | `references/lua-scripting.md` |
| UI contexts, XML controls, `ContextPtr` and `Controls`, `InstanceManager`, UI file pairing, `ImportFiles`, `ReplaceUIScript`, icon atlases and `IconDefinitions`, `.artdef` and `.dep` art, DDS rules, models and leader scenes | `UI/`, `Icons/`, `ArtDefs/` | `references/ui-and-art.md` |
| `LocalizedText` rows, `LOC_*` key conventions, `UpdateText`, language coverage, text markup, escaping and duplicate-key errors | `Text/` | `references/localisation.md` |
| `AppOptions.txt`, log files, cache files, FireTuner and panels, SQLite Browser, WorldBuilder, Asset Editor, Workshop upload, symptom-to-cause catalogue | — | `references/debugging-and-tools.md` |

Open only the reference needed for the task.

## Working Method

1. **Decide the layer first.** Static data is a table row; conditional behaviour is a modifier plus a requirement set; stateful or engine-query logic is Lua; anything visible is UI plus art. A rule encoded in Lua that a modifier could express is a compatibility and save-game liability.
2. **Copy the vanilla row set, do not write from memory.** Open the closest analogue under `Base/Assets/Gameplay/Data/` (or `DLC/Expansion2/` for Gathering Storm) and copy every row that references it: `Types`, the content row, association rows, ability/modifier attachments, prerequisites, text, and icon definitions. Civ6 tables have many columns with defaults that only matter when absent.
3. **Follow the registration chain.** `Types` → content table → association and prerequisite tables → modifier attachment → `Modifiers`/`ModifierArguments` → `RequirementSets`/`Requirements`/`RequirementArguments` → `LocalizedText` → `IconTextureAtlases`/`IconDefinitions`. Break the chain anywhere and the object loads without the part that was missing, usually without an error.
4. **Choose the cheapest mechanism that expresses the rule.** Yields, combat strength, movement, cost changes, grants, and adjacency are modifiers. "Only when at war", "only in the capital", "only on this feature" are requirement sets. A per-turn scan over every city in Lua for something a requirement could express is both slower and multiplayer-unsafe.
5. **Test both rulesets when claiming base compatibility.** Enable only the base game, then only Rise and Fall, then Gathering Storm. An action without a criteria runs everywhere, so it must reference only rows that exist everywhere.
6. **Inspect the merged database, not the source.** After startup, query `Documents\My Games\Sid Meier's Civilization VI\Cache\DebugGameplay.sqlite` to see the final rows after all enabled mods applied in order, and `DebugLocalization.sqlite` for text.
7. **Validate in game.** Watch `modding.log` for whether the mod and each action ran, `Database.log` for the first failing statement, `GameEffects.log` for unresolved modifier types or requirement arguments, and `Lua.log` for script errors. Use FireTuner to print live state and to iterate without a restart.
8. **Re-check after each patch.** Firaxis has changed table columns and the art pipeline across patches, and the mod's `CompatibleVersions` is advisory only; a patch that adds a column can invalidate a copied row set.

## Honest Limits

- **The SDK is Windows-only.** Mods run on macOS and Linux, but ModBuddy, FireTuner, the Asset Editor, and the WorldBuilder do not; cross-platform authors need a Windows machine or VM for the tooling steps.
- **There is no DLL source and no gameplay code access.** Unlike Civ5, combat, AI, and core rules cannot be replaced. Behaviour is limited to what modifiers, requirements, and the exposed Lua API allow.
- **Custom 3D art and leader scenes are the expensive frontier.** Units, districts, and buildings with new models need the Asset Editor plus `.artdef`/`.fgx`/`.geo`/`.mat` work and a generated Pantry; most mods reuse vanilla art and a fallback leader scene.
- **UI mods replace whole files.** Two mods shipping the same vanilla UI file cannot both win; the later load order takes it. Prefer adding a control from an existing context or hooking an exposed event over replacing a large file.
- **Modifier behaviour is only as good as its attachment.** A correctly defined modifier that is attached to nothing, attached through the wrong table, or filtered by an unmet requirement set does nothing and reports nothing in the UI.
- **Requirement sets are a fixed vocabulary.** Conditions outside the shipped `REQUIREMENT_*` types cannot be invented in data; they need a modifier with a different effect or a Lua workaround.
- **Database errors are per statement, not per mod.** A duplicate key or a missing column aborts that statement and the game continues, so a partially applied mod is the normal symptom of a broken file.
- **Text is per language.** A key defined only for `en_US` renders as the raw tag for a player running another language, and expansion patches rename some vanilla keys.
- **Changing the database invalidates saves.** Adding or removing types, and toggling mods, can break an in-progress game; say so plainly on the Workshop page rather than implying compatibility.
- **Multiplayer requires an identical mod set.** Ruleset criteria, load order, and dependency declarations must match on every client or the game desynchronises.
- **FireTuner is a development aid, not a shipped feature.** Never design a mod whose behaviour depends on a tuner connection.
- **The community references are ageing.** The Sukritact index, the Turnock wiki, and the Steam SQL guide all stop before the last patches; use them for concepts and vocabulary, then confirm table and column names against the installed files and the cache snapshot.