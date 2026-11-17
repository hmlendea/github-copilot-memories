---
name: civ5-modding
description: Use when creating or editing a Civilization V mod, or when working with its ModBuddy project (.civ5proj), mod descriptor (.modinfo), XML/SQL database updates (GameData Row, Update, Delete, Replace, Table, Column), Virtual File System import, content tables (civilizations, leaders, traits, units, buildings, improvements, resources, policies, beliefs, technologies, projects, processes, promotions, specialists, city-states, natural wonders), Lua 5.1 engine scripting (Events, GameEvents, LuaEvents, Modding, DB, GameInfoTypes, persistence), UI contexts and In-Game UI addins, DDS icon atlases and art defines, localisation rows and text markup, or the SDK, FireTuner, database snapshots, logs, and common load failures. Covers Steam Workshop publishing, mod compatibility and load order, and what cannot be modded.
---

# Civilization V Modding

Apply when authoring or reviewing content for **Sid Meier's Civilization V** (Firaxis Games, 2010; Gods & Kings and Brave New World expansions). Civ5 has no script language of its own for gameplay data: everything gameplay-facing is SQLite tables written through XML or SQL, all behaviour beyond the tables is Lua 5.1 running inside the engine, and the remainder is art.

Source material: [Modding (Civ5)](https://civilization.fandom.com/wiki/Modding_(Civ5)), the [Modding Guides](https://civilization-v-customisation.fandom.com/wiki/Modding_Guides), the [Civ5 modding article on NamuWiki](https://en.namu.wiki/w/%EB%AC%B8%EB%AA%85%205/%EB%AA%A8%EB%94%A9), and [Modiki](https://modiki.civfanatics.com/index.php/Main_Page) pages `Civ5 Modding Tutorials`, `Civ5 XML Reference`, the per-table pages (`CIV5Units`, `CIV5Buildings`, `CIV5Policies`, `CIV5Technologies`, `CIV5Civilizations`, `CIV5Traits`, `CIV5Improvements`, `CIV5Resources`, `CIV5Projects`, `CIV5IconTextureAtlases`, `CIV5IconFontMapping`), `XML-SQL Cheat Sheet (Civ5)`, `VFS (Civ5)`, `Localization Tutorial (Civ5)`, `Text icons and markups (Civ5)`, `Lua and UI Reference`, `Lua Game Events`, `Lua Game Objects`, `Lua introduction for confirmed developers`, `Specificities of the Lua implementation in Civ5`, `Persisting data (Civ5)`, `Map and terrain (Civ5)`, `Modding Limits and Issues (Civ5)`, `Debugging (Civ5)`, `Civ5 Useful Programs`, `Civ5 API FAQ`, and `Basic DLL tasks`. Modiki is largely frozen at the 2012–2013 state; treat anything about BNW-era UI, new tables, or "will be fixed in a patch" as needing verification against the installed `Assets/` files and the generated database snapshot.

## Non-Negotiable Build Rules

1. **Never edit game files.** Everything goes in a mod folder built by ModBuddy; Steam file verification and expansion updates overwrite `Assets/`. Treat `Assets/DLC/Expansion2/Gameplay/XML/...` as read-only reference material.
2. **Nothing appears in game unless it is wired to an action.** XML/SQL is inert until listed under `<Actions><OnModActivated>` as `UpdateDatabase`, and a Lua UI file is inert until declared as an `<EntryPoint type="InGameUIAddin">`. This is the single most common "my mod does nothing" cause.
3. **Files the game must read at runtime must be imported into the VFS** (`ImportIntoVFS` in the project, `import="1"` in `.modinfo`): UI XML, Lua files loaded by other files, art, and the DLL. Files consumed only through the database/text actions should not be imported.
4. **XML is not a data format, it is SQL.** `<Row>` is `INSERT`, `<Update>` is `UPDATE`, `<Delete>` is `DELETE`, `<Replace>` is insert-or-replace, `<Table>`/`<Column>` are DDL. A second `INSERT` of an existing `Type` fails on the primary key and is only reported in `Database.log` — it does not override. Modify existing rows with `<Update>`; fully replace them with `<Replace>`.
5. **Never gap a primary key.** Deleting a row from a table the UI iterates (notably `Policies`) leaves an `ID` hole and every later row becomes invisible to the UI. Disable content (`<Replace>` with a null/blocked value, or an `UPDATE ... SET` guard) rather than deleting it.
6. **Do not edit schema files, and do not add columns to vanilla tables** unless the change is only consumed by your own code. Vanilla columns come from the engine's schema; a new column is invisible to the DLL unless it is patched, and the official, safe route for new data is the mod's own `DB.Query` tables.
7. **Expansion dependency must be declared.** BNW-only tables (`Beliefs`, tourism, ideologies, `Corporations` in CBP) fail silently or abort the file without the DLC dependency. Add the DLC dependency in ModBuddy rather than hand-writing its GUID; BNW's is `6DA07636-4123-4018-B643-6575B4EC336B`.
8. **A civilization needs at least two unique overrides** (units or buildings) or it is filtered out of the civilization-selection screen, and **only one leader per civilization displays** in the setup screen. Both are engine behaviour, not user error.
9. **Enable logging before the first test.** `config.ini`: `LoggingEnabled = 1`, `ValidateGameDatabase = 1`, `EnableTuner = 1`, `EnableLuaDebugLibrary = 1`; `usersettings.ini`: `DebugMode = 1`. Without them, a failed XML file and a failed Lua file are indistinguishable from a design mistake.
10. **A Lua syntax error kills the whole file; a runtime error kills the rest of the chunk.** In both cases the game keeps running, so a silent no-op is usually `Lua.log`/`Database.log`, not the design.

## Layout

```
MyMod/                          # ModBuddy solution directory
  MyMod.civ5proj                # project: Properties, Dependencies, References, Blocks, content items
  XML/                          # database files (UpdateDatabase action, ImportIntoVFS = False)
  SQL/                          # DDL and bulk updates (UpdateDatabase action)
  Lua/                          # gameplay scripts (InGameUIAddin or included from one)
  UI/                           # Context XML + paired Lua (InGameUIAddin, ImportIntoVFS = True)
  Art/                          # .dds atlases, leader art, 3D .fxsxml/.gr2 (ImportIntoVFS = True)
  Language/                     # Language_en_US rows if kept separate from XML/
Build/                          # deploy output ModBuddy writes into the game's MODS folder
  MyMod (v 1)/MyMod (v 1).modinfo
```

Generated `.modinfo` structure (written by ModBuddy; hand-editing is supported but re-check after any UI change):

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
| ModBuddy, `.modinfo`, VFS import rules, actions and entry points, install paths, Workshop, load order, compatibility, troubleshooting | `.civ5proj`, `.modinfo` | `references/mod-packaging.md` |
| XML `GameData` semantics, SQL equivalents, schema and foreign keys, ordering, deletion hazards, custom tables | `XML/`, `SQL/` | `references/database-xml-sql.md` |
| Civilizations, leaders and AI flavours, traits, units, promotions, buildings, improvements, resources, policies, beliefs, technologies, projects, processes, specialists, city-states, natural wonders | `XML/` tables | `references/content-definitions.md` |
| Lua sandbox, `include`, `Events`/`GameEvents`/`LuaEvents`, `GameInfoTypes`, persistence, dummy-object patterns, performance | `Lua/` | `references/lua-scripting.md` |
| `Context` XML, `LuaContext`, `Controls`, callbacks, popups, UI overrides, DDS atlases, art defines, leader scenes | `UI/`, `Art/` | `references/ui-and-art.md` |
| `Language_*` rows, `TXT_KEY` naming, lookups, gender/plural/forms, markup, icon tags | `Language/`, text XML | `references/localisation.md` |
| `config.ini` and `usersettings.ini`, `Database.log`, `Lua.log`, `XML.log`, FireTuner, `Civ5DebugDatabase.db`, IGE, SDK, DLL, failure catalogue | — | `references/debugging-and-tools.md` |

Open only the reference needed for the task.

## Working Method

1. **Decide the layer first.** Pure data (a building, a unit, a policy) belongs in XML/SQL; anything conditional or reactive belongs in Lua; anything visual belongs in `UI/` + `Art/`. A gameplay rule expressed in Lua that could be a table column is a performance and compatibility liability.
2. **Copy the vanilla declaration, do not write from memory.** Open the matching file under `Assets/Gameplay/XML/...` (or `Assets/DLC/Expansion2/Gameplay/XML/...` for BNW), copy the block for the closest similar object, then rename and trim. Civ5's columns are numerous and undocumented outside the schema; a missing mandatory column fails the whole file.
3. **Every new `Type` needs a full dependency chain**: `BuildingClass` before `Building`, `UnitClass` before `Unit`, `PolicyBranchType` before `Policy`, `ResourceClass` before `Resource`, `PlayerColor` before `Civilization`, `Leader` before `Civilization_Leaders`, plus `Language_*` rows for `Description`/`ShortDescription`/`Help`/`Strategy` and `IconTextureAtlases` rows for every icon size used.
4. **Choose the delivery mechanism for effects deliberately.** Passive, unconditional yields belong in a hidden ("dummy") building or a trait/policy column applied by XML. Conditional effects (per era, per war state, per player action) belong in Lua on `GameEvents`. Prefer the table: dummy buildings survive save/load and cost nothing per turn.
5. **Register Lua once, and re-register on load.** `GameEvents`/`Events` handlers registered only at file scope are widely reported to stop firing after loading a save; re-add them from `Events.LoadScreenClose` or `Events.SequenceGameInitComplete` and verify with a `print`.
6. **Guard every index.** `Players[i]`, `GameInfoTypes[...]`, and `GameInfo.Xxx[typeID]` all return `nil` for ids that are absent (DLC missing, typo, deleted row). A `nil` dereference is a runtime error that silently truncates the rest of that chunk.
7. **Check the database snapshot, not the XML.** Each game start writes `cache/Civ5DebugDatabase.db`; query it to see what your rows actually became after all mods merged. This is the only reliable way to debug a foreign-key or duplicate-key failure.
8. **Validate in game**: launch with logging enabled, watch `Logs/Database.log` and `Logs/Lua.log`, use FireTuner for live state and `print`, and use IGE to jump to the state you need to test.
9. **Re-verify keys after each expansion or update.** Modiki's tables are pre-BNW in places; the shipped XML and the snapshot are authoritative.

## Honest Limits

- **Audio files cannot be added** by a mod (documented Civ5 limit). Sound is limited to what the vanilla asset definitions already name.
- **3D leader scenes are effectively closed.** `fxsxml`/`gr2` with Nexus works but is fragile and tool-version-bound; the overwhelming majority of modded civilizations ship a 2D leader screen and an existing 3D unit model.
- **Combat resolution and most AI are in the DLL.** Triggering, preventing, or replacing standard AI behaviour from Lua is not supported; the API exposes almost no hooks. AI can be biased through flavours and biases tables, not rewritten.
- **UI modularity is weak.** Most UI work requires replacing a whole vanilla Lua/XML file, so only one such mod can win. Use the community registration libraries (custom notifications, minimap overlays, summary bar) instead of shipping your own replacement of the same file.
- **`UnitArtInfos` and `UnitMemberArtInfos` must be replaced wholesale**, which is why unit art mods conflict with each other.
- **Removing a feature that changes terrain or plot type does not refresh the 3D mesh** until the game is reloaded; there is no runtime terraforming.
- **New social-policy branches need UI work** and AI does not select added ideologies; new branches without UI changes are unreachable for the player.
- **`include()` has real traps**: only VFS-imported files load, only the first eight characters of a name are compared in some paths, and calling it from a UI event handler can silently report success without importing globals.
- **Persistence is string-based and slow.** `ModData` is a SQLite-backed key/value store; per-turn writes are measurably expensive. Cache locally, write on change, and never treat `ScriptData` as private — it is shared with every other mod.
- **A runtime error in an event handler aborts the rest of that chunk, not the game**, so partial effects are the normal symptom of a Lua bug.
- **Mods with `AffectsSavedGames = 1` cannot be added to or removed from an existing save** without risking corruption; state that plainly when publishing.
- Multiplayer requires every player to run an identical mod set; DLL-changing mods must be distributed consistently or the game desyncs.