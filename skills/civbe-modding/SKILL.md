---
name: civbe-modding
description: Use when creating or editing a Civilization: Beyond Earth mod, or when working with its ModBuddy project and mod descriptor (.modinfo), OnModActivated and UpdateDatabase actions, Virtual File System import, XML/SQL database updates (GameData Row, Update, Delete, Replace, Table, Column), content tables (sponsors, leaders, colonists, cargo, spacecraft, units, buildings, technologies, affinities, virtues, quests, covert operations, artifacts, marvels, orbital units, satellites, biomes, resources, tile improvements), Lua scripting (Events, GameEvents, LuaEvents, GameInfoTypes, persistence), UI contexts and In-Game UI addins, DDS icon atlases and art defines, localisation rows and text markup, or FireTuner, log files, and prevalent load failures. Covers Rising Tide expansion differences, Steam Workshop publishing, mod compatibility and load order, and what cannot be modded.
---

# Civilization: Beyond Earth Modding

Apply when authoring or reviewing content for **Sid Meier's Civilization: Beyond Earth** (Firaxis Games, 2014; the *Rising Tide* expansion). CivBE is built on the Civ5 engine, so its mod format is Civ5's: gameplay data is SQLite tables written through XML or SQL, gameplay logic beyond the tables is Lua running within the engine, and the remainder is art. The content vocabulary, however, is not Civ5's — sponsors replace civilizations, colonists and cargo replace the starting-unit package, the tech web replaces the tech tree, and affinity, virtues, quests, artifacts, and (in Rising Tide) the marvel system have no Civ5 equivalent.

Source material: [Mods (CivBE)](https://civilization.fandom.com/wiki/Mods_(CivBE)) and its *How to Create Units* guide, the CivFanatics forums [CivBE - Modding Help & Mod Creation](https://forums.civfanatics.com/forums/civbe-modding-help-mod-creation.512/) and [CivBE - Tutorials and References](https://forums.civfanatics.com/forums/civbe-tutorials-and-references.513/) together with the threads `Beginner's Guide to the CivBE Mod Development Process`, `Custom Sponsor Tutorial`, `Fully Commented/Annotated Sponsor files`, `File attributes/properties - Is that VFS, InGameUIAddin or UpdateDatabase?`, `Extracting art assets`, `Info about UI image files in CBE`, `Reference - Font Icons`, `Reference - UI Controls - comparison with CivV`, and `PSD template for sponsors' icons`. The Fandom page states plainly that the game "uses XML and Lua files for mods, just like Civilization V, so the links in the Modding (Civ5) article are largely valid with Beyond Earth as well": the shared table semantics, VFS rules, action types, Lua sandbox, and debugging tools documented for Civ5 apply here unchanged, and the Civ5 skill should be consulted for those mechanics. What is Beyond-Earth-specific is the content schema, and that is only authoritatively documented in the shipped `assets/Gameplay/XML/...` files. Community coverage is thin and predominantly written within months of release; treat every tutorial as a starting point and confirm column names, table names, and defaults against the installed files and the generated database snapshot.

## Non-Negotiable Build Rules

1. **Never edit game files.** Everything lives in a mod folder built by ModBuddy; Steam file verification and patches overwrite `assets/`. Read `assets/Gameplay/XML/...` (and the Rising Tide equivalents) as reference material only.
2. **Nothing appears in game unless it is wired to an action.** XML/SQL is inert until listed under ModBuddy's *Actions* as `OnModActivated` → `UpdateDatabase`; a Lua or `Context` XML file is inert until declared as a content entry point (`InGameUIAddin`). A tutorial that concludes at "build the solution" is incomplete, and a mod that appears in the Mods list but changes nothing is almost invariably missing the action.
3. **Files the game must read at runtime must be imported into the VFS** (`Import into VFS`, `import="1"` in `.modinfo`): UI XML, Lua loaded by other files or by a context, art, fonts, and audio. Files consumed only through the database action must not be imported. The tutorial set documents this per extension; when in doubt for an asset, import, and when in doubt for a database input, do not.
4. **XML is not a data format, it is SQL.** `<Row>` is `INSERT`, `<Update>` is `UPDATE`, `<Delete>` is `DELETE`, `<Replace>` is insert-or-replace, `<Table>`/`<Column>` are DDL. A second `INSERT` of an existing key fails on the primary key and is reported only in `Database.log` — it does not override. Modify vanilla rows with `<Update>`; own a key outright with `<Replace>`.
5. **Register before you reference and follow the full dependency chain.** A unit requires its `UnitClass` first; a sponsor requires its leader, free building classes, free techs, and city-name rows; new text requires `TXT_KEY_*` rows in every shipped language; every icon size the UI requests requires an `IconTextureAtlases` row. Omit a link in the chain and the object loads without the missing part, usually silently.
6. **Never gap a primary key.** Deleting a row from a table the UI iterates leaves an `ID` hole and every later row becomes invisible. Disable content with an `<Update>`/`<Replace>` guard rather than deleting it.
7. **Do not edit schema files, and do not add columns to vanilla tables** unless the change is consumed only by your own code. Vanilla columns come from the engine's schema; a new column is invisible to the DLL. The supported route for extra data is the mod's own `DB.Query` tables.
8. **State the Rising Tide requirement in the mod description and enforce it.** Anything built on Rising Tide-only tables (marvels, aquatic cities and gameplay, diplomatic capital, the updated artifact and quest systems) fails silently or aborts the file without the expansion. Declare the dependency in ModBuddy rather than implying compatibility.
9. **Enable logging before the first test.** `config.ini`: `LoggingEnabled = 1`, `ValidateGameDatabase = 1`, `EnableTuner = 1`, `EnableLuaDebugLibrary = 1`; `usersettings.ini`: `DebugMode = 1`. Without them a failed XML file and a failed Lua file are indistinguishable from a design mistake. Recent reports also note that Lua's standard debug library is not exposed to mod scripts by default, so `print` plus the log is the working debug channel.
10. **A Lua syntax error kills the entire file; a runtime error kills the rest of the chunk.** The game continues running in both cases, so a silent no-op is usually `Lua.log` or `Database.log`, not the design.

## Layout

```
MyMod/                          # ModBuddy solution directory
  MyMod.civ5proj                # project: Properties, Actions, Content, per-file VFS flag
  XML/                          # database files (UpdateDatabase action, import = False)
  SQL/                          # DDL and bulk updates (UpdateDatabase action, import = False)
  Lua/                          # gameplay scripts (imported, or driven by an InGameUIAddin)
  UI/                           # Context XML + paired Lua (InGameUIAddin, import = True)
  Art/                          # .dds atlases, unit art, leader art, 3D .fxsxml/.gr2 (import = True)
  Language/                     # en_US rows if kept separate from XML/
Build/                          # deploy output ModBuddy writes into the game's MODS folder
  MyMod (v 1)/MyMod (v 1).modinfo
```

Generated `.modinfo` structure (written by ModBuddy; hand-editing works but re-check after any UI change):

```xml
<Mod id="GUID" version="1">
  <Properties>Name, Teaser, Description, Authors, SupportsMac, AffectsSavedGames, Reload*System</Properties>
  <Dependencies><Dlc id="..." minversion="0" maxversion="999"/></Dependencies>
  <References/> <Blocks><!-- mods this one is incompatible with --></Blocks>
  <Files><File md5="..." import="1">UI/TopPanel.lua</File></Files>
  <Actions><OnModActivated><UpdateDatabase>XML/MyMod.xml</UpdateDatabase></OnModActivated></Actions>
  <EntryPoints><EntryPoint type="InGameUIAddin" file="UI/MyMod.xml">...</EntryPoint></EntryPoints>
</Mod>
```

## Domain Map

| Need | Where | Reference |
|------|-------|-----------|
| SDK and ModBuddy, `.modinfo`, VFS import rules per file type, actions and entry points, install paths, Workshop publishing, load order, compatibility, troubleshooting | `.civ5proj`, `.modinfo` | `references/mod-packaging.md` |
| XML `GameData` semantics, SQL equivalents, schema and foreign keys, ordering, deletion hazards, generated database snapshot, custom tables | `XML/`, `SQL/` | `references/database-xml-sql.md` |
| Sponsors, leaders, colonists, cargo, spacecraft, units, unit classes, buildings, technologies (tech web), affinities, virtues, quests, covert operations, artifacts, marvels, orbital units and satellites, biomes, terrains, resources, improvements, yields | `XML/` tables | `references/content-definitions.md` |
| Lua sandbox, `include`, `Events`/`GameEvents`/`LuaEvents`, `GameInfoTypes`, persistence, per-turn cost, affinity and quest scripting | `Lua/` | `references/lua-scripting.md` |
| `Context` XML, `Controls`, callbacks, the sponsor-select and load screens, UI overrides, DDS atlases, icon definitions, art defines, unit and leader art | `UI/`, `Art/` | `references/ui-and-art.md` |
| `Language_*` rows, `TXT_KEY_*` naming, language attribute behaviour, `%` text variation, markup, icon tags, font icons | `Language/`, text XML | `references/localisation.md` |
| `config.ini` and `usersettings.ini`, `Database.log`, `Lua.log`, `XML.log`, FireTuner, database snapshot, FPK extraction, failure catalogue | — | `references/debugging-and-tools.md` |

Open only the reference required for the task.

## Working Method

1. **Decide the layer first.** Pure data (a unit, a building, a virtue, a sponsor) belongs in XML/SQL; anything conditional or reactive belongs in Lua; anything visual belongs in `UI/` + `Art/`. A gameplay rule expressed in Lua that could be a table column is a performance and compatibility liability.
2. **Copy the vanilla declaration, do not write from memory.** Open the matching file under `assets/Gameplay/XML/...` (for example `Units/CivBEUnits.xml` and `Units/CivBEUnitClasses.xml`), copy the block for the closest similar object, then rename and trim. CivBE's columns are numerous and undocumented outside the schema; a missing mandatory column fails the entire file.
3. **Follow the full dependency chain for the object type.** A sponsor requires `Civilizations`, `Civilization_CityNames`, `Civilization_FreeBuildingClasses`, `Civilization_FreeTechs`, `Civilization_Leaders`, `Civilization_SpyNames`, and the alien unit-class overrides, plus `LocalizedText` for each `TXT_KEY_*` it names. A unit requires `UnitClasses` before `Units`, plus text and icons. An affinity, virtue, technology, or quest requires its own registration and association tables.
4. **Select the delivery mechanism for effects deliberately.** Passive, unconditional yields belong in a hidden ("dummy") building or a sponsor trait column applied by XML. Conditional effects (per affinity level, per era, per player action, per quest outcome) belong in Lua on `GameEvents`. Prefer the table: dummy buildings survive save/load and cost nothing per turn.
5. **Register Lua once, and re-register on load.** `GameEvents`/`Events` handlers registered only at file scope are widely reported to cease firing after loading a save; re-add them from `Events.LoadScreenClose` or `Events.SequenceGameInitComplete` and verify with a `print`.
6. **Guard every index.** `Players[i]`, `GameInfoTypes[...]`, and `GameInfo.Xxx[typeID]` all return `nil` for ids that are absent (expansion missing, typo, deleted row). A `nil` dereference is a runtime error that silently truncates the rest of that fragment.
7. **Check the database snapshot, not the XML.** Each game start writes the merged debug database; query it to observe what your rows actually became after all mods merged. This is the only reliable method to debug a foreign-key, duplicate-key, or silently dropped row.
8. **Validate in game**: launch with logging enabled, watch `Database.log` and `Lua.log`, use FireTuner for live state and `print`, and iterate on the state you require to test.
9. **Re-verify keys after each patch or expansion switch.** Published guides and the Fandom article cease at the base-game or early Rising Tide state; the shipped XML and the snapshot are authoritative whenever they disagree.

## Honest Limits

- **Audio files cannot be added** roughly as in Civ5; sound is limited to what the vanilla asset definitions already name. State this plainly rather than promising audio.
- **3D leader and unit art is the expensive frontier.** `fxsxml`/`gr2` with Nexus works but is fragile and tool-version-bound, and case reports note the engine disliking repeated in-place edits of an identical model or texture — export under a novel name each time and revise the reference. Most modded sponsors ship a 2D portrait and an existing unit model.
- **Textures and 3D model textures are packed in FPK archives**, and the packed DDS entries are run-length encoded, so they are unreadable until decompressed; only some are viewable after extraction, and some are DXT4, which most viewers and GIMP render blank. Budget for the art toolchain before promising art.
- **Combat resolution and most AI are in the engine, not in a shipped DLL the user can recompile.** Triggering, preventing, or replacing standard behaviour from Lua is not supported; AI can be biased through flavours and biases tables, not rewritten. Alien aggression behaves as a documented set of engine rules, not as a moddable script.
- **UI modularity is weak.** Most UI work requires replacing an entire vanilla Lua/XML file, so only one such mod can win. Use community registration libraries rather than shipping your own replacement of the identical file.
- **`UnitArtInfos` and `UnitMemberArtInfos` must be replaced wholesale**, which is why unit-art mods conflict with each other.
- **Removing a feature that changes terrain or plot type does not refresh the 3D mesh** until the game is reloaded; there is no runtime terraforming.
- **A runtime error in an event handler aborts the rest of that fragment, not the game**, so partial effects are the normal symptom of a Lua bug.
- **Mods with `AffectsSavedGames = 1` cannot be added to or removed from an existing save** without risking corruption; state that plainly when publishing.
- **Multiplayer requires every player to run an identical mod set**, and a mod that changes the database must be distributed consistently or the game desynchronises.
- **The documentation is thin and uneven.** There is no CivBE equivalent of Civ5's Modiki or Civ6's modding wikis; the Fandom page points at Civ5 material, the forum tutorials are few and partly unfinished, and several tutorials describe a `VFS` control that ceased appearing in newer ModBuddy builds while still being required. Verify every mechanical claim against the shipped files.
