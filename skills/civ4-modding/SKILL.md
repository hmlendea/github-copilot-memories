---
name: civ4-modding
description: "Use when creating or editing a Civilization IV mod (vanilla, Warlords, or Beyond the Sword 3.19), or when working with its mod folder and Mods/<Mod>.ini configuration, modular XML loading (Assets/Modules), the XML data files under Assets/XML (CIV4UnitInfos, CIV4BuildingInfos, CIV4CivilizationInfos, CIV4LeaderHeadInfos, CIV4TechInfos, CIV4CivicInfos, CIV4PromotionInfos, CIV4ImprovementInfos, CIV4BonusInfos, CIV4EventInfos, CIV4EventTriggerInfos, CIV4ArtDefines_*), XML schemas and mandatory tag order, TXT_KEY localisation, Python 2 scripting (CvEventManager, CvGameUtils, PythonCallbackDefines, CvPythonExtensions, EntryPoints, Screens), game fonts and DDS/NIF/KFM art, WorldBuilder and WBS scenarios, map scripts in PublicMaps, or the CvGameCoreDLL SDK in C++. Covers load order, modular merging, saved-game and multiplayer compatibility, packaging and installation, and what cannot be modded. The bundled references hold the full detail and load on demand."
---

# Civilization IV Modding

Apply when authoring or reviewing content for **Sid Meier's Civilization IV** (Firaxis Games, 2005; *Warlords* and *Beyond the Sword*, with BtS 3.19 as the de facto modding baseline). Civ4 predates the Civ5 engine and shares nothing with it: gameplay data is declarative XML read into the C++ engine at start-up, behaviour beyond the tables is Python 2 running inside the engine and reached through the SWIG-generated `CvPythonExtensions` module, everything the Python layer cannot express is the `CvGameCoreDLL` SDK in C++, and the remainder is Gamebryo art.

Source material: [Modiki](https://modiki.civfanatics.com/index.php/Main_Page) pages `Civ4 Modding Tutorials`, `Civ4 Python`, `Civ4 SDK`, `Civ4 World Builder`, `Civ4 Useful Programs`, `CvEventManager`, `PythonCallbackDefines`, and the per-file XML references (`Civ4UnitInfos`, `Civ4UnitClassInfos`, `Civ4BuildInfos`, `Civ4PromotionInfos`, `Civ4BuildingInfos`, `Civ4TechInfos`, `Civ4CivilizationInfos`, `Civ4LeaderHeadInfos`, `Civ4TraitInfos`, `Civ4CivicInfos`, `Civ4ImprovementInfos`, `Civ4BonusInfos`, `Civ4FeatureInfos`, `Civ4TerrainInfos`, `Civ4RouteInfos`, `Civ4EraInfos`, `Civ4GameSpeedInfo`, `Civ4HandicapInfo`, `Civ4SpecialistInfos`, `Civ4CorporationInfo`, `Civ4EspionageMissionInfo`, `Civ4EventInfos`, `Civ4EventTriggerInfos`, `GlobalTypes`, `Civ4PlayerColorInfos`, and the `CIV4ArtDefines_*` set), the [Civ4 modding page on StrategyWiki](https://strategywiki.org/wiki/Civilization_IV/Modding), the [Civ4 modding tutorial on Wikibooks](https://en.wikibooks.org/wiki/Civ/Civilization_IV/Modding/Tutorials/Getting_Started), and the CivFanatics forums [Civ4 - Modding Tutorials & Reference](https://forums.civfanatics.com/forums/civ4-modding-tutorials-reference.177/) together with its *Utility Programs* subforum. Modiki is largely frozen at the BtS 3.17–3.19 era and several pages are stubs, so treat every column name, default, and stated limit as needing confirmation against the installed `Assets/` files, the shipped `*Schema.xml`, and the loader logs.

The three layers are not interchangeable, and the distinction drives almost every design decision:

| Layer | Expresses | Cost |
|-------|-----------|------|
| XML | content and its static numbers: units, buildings, techs, civics, promotions, terrain, art bindings, text | free at run time; fixed at load; cannot branch |
| Python | interface, event reactions, random-event consequences, rules the tables cannot hold | slow, interpreted, single-threaded, interface-oriented |
| SDK (C++) | new calculations, new XML columns, changed AI, anything hot | needs a compiler and a matching toolchain; forks the engine |

## Non-Negotiable Build Rules

1. **Never edit the game's own `Assets/`, and never edit `Assets/XML` in place.** Everything belongs in `Mods\<ModName>\`, which shadows the base tree; a patch, a Steam file verification, or an expansion install overwrites the base copy. Read the base tree as reference material only.
2. **A mod is only loaded when the launcher or the ini names it.** `Mods\<Mod>\<Mod>.ini` is the mod's own configuration and its `Name` field is what the in-game *Advanced → Load a Mod* list displays. A mod folder with no `.ini` still loads, but nothing about the mod is configurable, and the ini is where `ModularLoading` and `AllowPublicMaps` are set.
3. **XML is declarative, not SQL.** There is no `Update`/`Delete`/`Replace`: a mod's XML file *replaces the whole vanilla file of the same relative path*, and the engine then loads it as the definition of that table. Changing one row therefore requires copying the entire vanilla file into the mod and editing the copy. The only way to add content without owning the whole file is **modular loading**.
4. **Modular loading is the supported add-without-replace mechanism, and it is off by default.** Set `ModularLoading = 1` in `<Mod>.ini`, then place files under `Assets\Modules\`. The convention is one folder per contributor and one per added civilization (`Assets\Modules\MyMod\`, then `.../Aborigines/Nulla Nulla/`), with files named `<Owner>_CIV4<Table>.xml` and a renamed copy of the matching schema beside each one, bound by the file's own `xmlns="x-schema:<name>_CIV4<Table>Schema.xml"`. The root and entry elements must match the target table exactly (`<Civ4UnitInfos><UnitInfos><UnitInfo>`), and the schema resolves relative to the modular file, which is how a module can extend the vocabulary. A module whose scoped schema is missing or misnamed does not load. Vanilla and Warlords have no modular loading.
5. **Tag order inside every XML entry is mandatory.** Each file is validated against its `*Schema.xml`, which is an ordered sequence definition; a tag written in the wrong position, or an unknown tag, aborts the load of that file and the error appears in the loader log rather than on screen. Copy the vanilla entry and edit values; never write an entry from memory.
6. **Every `Type` is a global, unique, case-sensitive identifier.** `CIVILIZATION_MYMOD`, `UNIT_MYMOD_SWORDSMAN`, `BUILDING_MYMOD_LIBRARY`. Re-declaring a vanilla `Type` while owning the whole file is a duplicate-key abort, and referencing a `Type` that no file declares (missing class, missing art define, missing text key) loads the object with the part silently absent.
7. **The dependency chain must be complete before the object loads**: `UNITCLASS_*` before `UNIT_*`, `BUILDINGCLASS_*` before `BUILDING_*`, `PROMOTION_*` before any unit that grants it, `ART_DEF_*` before any art binding, `PLAYERCOLOR_*` and `ART_DEF_CIVILIZATION_*` before a civilization, `TXT_KEY_*` rows in `Assets\XML\Text\` before any `Description`, and a `Button` or font-index entry before any icon. A missing link is usually a silent absence, not a crash.
8. **Python in Civ4 is Python 2.** No f-strings, no `logging`, no guaranteed dict ordering, and integer division by default; `print` is a statement and strings are bytes unless wrapped in `unicode(...)`. In-language syntax errors kill the file; a `SyntaxError` or `ImportError` surfaces in `PythonErr.log`, not on screen.
9. **Several engine callbacks are disabled by default in BtS for performance.** `Assets\XML\PythonCallbackDefines.xml` carries 41 `USE_*_CALLBACK` switches, all `0` in the shipped file — the `CvGameUtils` legality questions (`USE_CAN_TRAIN_CALLBACK`, `USE_CAN_BUILD_CALLBACK`, `USE_CAN_CONSTRUCT_CALLBACK`, `USE_UNIT_CANNOT_MOVE_INTO_CALLBACK`, `USE_CANNOT_FOUND_CITY_CALLBACK`, `USE_CAN_RESEARCH_CALLBACK`, `USE_CAN_DO_CIVIC_CALLBACK`, `USE_CAN_DECLARE_WAR_CALLBACK`), the engine-internal `do*` replacement points, and the `USE_AI_*` and `USE_ON_*` entries. Answering *yes* to a callback whose switch is 0 is not merely unused: nothing runs. Turn the switch on in the mod's copy of the file and accept the per-call cost; a `do*` or `AI_*` switch is a far larger commitment than a `can*` one, because it replaces the engine's own calculation.
10. **Enable logging before the first test.** In `Civ4.ini` (BtS: `Beyond the Sword\Civ4.ini`, in the user directory) set `LoggingEnabled = 1` and, when needed, `SynchLog`, `RandLog`, `MessageLog`, `OverwriteLogs`, and `EnablePythonConsole`. The logs land in the same user directory. Without them, a failed XML file and a failed Python file are both indistinguishable from a design mistake.

## Layout

```
Beyond the Sword\Mods\MyMod\
  MyMod.ini                     # mod configuration: ModularLoading, AllowPublicMaps, Name, ...
  CvGameCoreDLL.dll             # only when the mod ships a rebuilt engine
  Assets\
    XML\                        # whole-file replacements of the base tables
      Units\CIV4UnitInfos.xml
      Civilizations\CIV4CivilizationInfos.xml
      Text\MyMod_CIV4GameText.xml
      PythonCallbackDefines.xml  # re-enable the callbacks the mod needs
    Modules\                    # modular loading: files merged into the target table
      MyMod\MyMod_CIV4UnitInfos.xml
      MyMod\MyMod_CIV4UnitSchema.xml   # scoped schema copy the module's xmlns names
    Python\
      CvEventManager.py         # whole-file replacement of the event handler
      EntryPoints\              # CvEventInterface, CvGameInterface, CvScreensInterface, ...
      Screens\                  # CvMainInterface and the other GUI screens
      MyModUtils.py             # the mod's own modules
    Art\                        # .dds buttons, .nif/.kfm models, leaderheads
    Res\Fonts\GameFont.tga      # only when the mod adds font icons
    Config\                     # per-mod runtime configuration XML
  PublicMaps\                   # map scripts and scenarios
```

A file written at the same relative path as a base file replaces it. A file under `Assets\Modules\` is merged instead, provided the target table exists and the file matches its shape.

## Domain Map

| Need | Where | Reference |
|------|-------|-----------|
| Mod folder and `.ini`, launcher, install paths, modular loading, load order, merging, packaging, troubleshooting | `<Mod>.ini`, `Assets\Modules\` | `references/mod-packaging.md` |
| XML semantics, schema validation and tag order, per-file index, text rows, button fields, encoding | `Assets\XML\` | `references/xml-reference.md` |
| Civilizations, leaders, traits, units, unit classes, buildings, techs, civics, promotions, improvements, bonuses, features, routes, specialists, corporations, projects | `Assets\XML\` tables | `references/content-definitions.md` |
| `CvEventManager`, `CvGameUtils`, `PythonCallbackDefines`, `CvPythonExtensions`, `EntryPoints`, persistence, random events and triggers, map scripts | `Assets\Python\`, `PublicMaps\` | `references/python-scripting.md` |
| `Screens\` GUI, `CvMainInterface`, `GameFont.tga`, DDS/NIF/KFM art, `CIV4ArtDefines_*`, leaderheads, unit art styles | `Assets\Python\Screens\`, `Assets\Art\`, `Assets\Res\` | `references/interface-and-art.md` |
| WorldBuilder, WBS scenario format, `PublicMaps` map scripts, map generation modules | `PublicMaps\`, `Assets\Python\` | `references/world-builder-and-maps.md` |
| `CvGameCoreDLL`: toolchain, sources, `CvInfos`/`CvEnums`, adding XML columns, exposing functions to Python | `CvGameCoreDLL\` | `references/sdk-and-cpp.md` |
| Logging ini, `PythonErr.log`, `init.log`, the loader logs, in-game tools, third-party checkers, failure catalogue | — | `references/debugging-and-tools.md` |

Open only the reference needed for the task.

## Working Method

1. **Choose the layer deliberately.** Static content and its numbers belong in XML; interface behaviour and reactions belong in Python; a new computation or a hot rule belongs in the SDK. A rule expressed in Python that could be a static XML number is a per-turn cost with no benefit, and a rule expressed in XML that needs to branch is not expressible at all.
2. **Copy the vanilla file, then edit the copy.** Because a mod's XML replaces the whole table, the workflow is always: copy `Assets\XML\...\<File>.xml` from the base tree into the mod at the identical relative path, edit the copy, and keep the file's version banner. Never hand-write a table file.
3. **Prefer modular files for additions.** A single added unit or civilization is one small file under `Assets\Modules\` instead of a fork of the whole table, which keeps the mod compatible with other mods and with patches. Reserve whole-file replacement for edits to vanilla entries.
4. **Walk the dependency chain in order** (rule 7 above) and add the text keys and art defines in the same pass as the object.
5. **Remember the icon budget.** Every new unit, building, or promotion button is an index into `GameFont.tga` or a DDS atlas; a wrong index shows a wrong picture or crashes, and the vanilla font sheets are full (see `references/interface-and-art.md`).
6. **Turn on every callback you need** in `PythonCallbackDefines.xml` before concluding that a `CvGameUtils` answer is ignored.
7. **Test in the order XML → Python → SDK.** A Python error masks an XML error and a DLL mismatch masks both; confirm each layer with the loader logs before adding the next.
8. **Re-check after any patch or expansion change.** BtS 3.17/3.19 added tables and changed defaults; a mod's copied XML files silently pin the old definitions unless they are refreshed.
9. **State saved-game and multiplayer consequences.** A mod that changes the tables a save stores by index cannot be added to or removed from an existing save safely, and every player in a multiplayer game must run an identical mod set.

## Honest Limits

- **XML cannot be partial.** There is no update or delete syntax; a mod that changes one vanilla number ships the whole table, and two mods that both ship the same table conflict — the later one in load order wins outright.
- **Load order is the user's, and there is no dependency solver.** `Mods` is loaded in the order the ini or the launcher establishes; `ModularLoading = 1` merges module files in an order the engine decides, and a `Type` collision between two modules is not repaired.
- **Python is slow and interface-oriented.** The shipped documentation points at the SDK for anything that runs every turn or per unit and describes Civ4's Python as suitable for simple scripting and interface work; a per-turn Python loop over cities is a measurable frame cost.
- **Python 2 only**, and the embedded interpreter exposes the engine through `CvPythonExtensions` — a SWIG surface that covers what the engine chose to expose, not the whole game. Anything absent from it needs an SDK change.
- **`GameFont.tga` is a hard limit.** Font icons live in two fixed-resolution sheets, `GameFont.tga` and `GameFont_75.tga`, addressed by index, and the shipped sheets are effectively full. Adding an icon means enlarging both and keeping their index layouts in step; the community ships a dedicated editor and several tutorials for exactly this operation.
- **The SDK forks the engine.** A mod shipping `CvGameCoreDLL.dll` must match the player's expansion and patch level, must be rebuilt for any other DLL-shipping mod, and cannot be combined with an incompatible second DLL mod.
- **Segmented per-turn Python callbacks bypass the normal engine path**, so ordering assumptions that hold for XML-defined content need not hold inside them.
- **Warlords and vanilla lack BtS-only tables and features**: the event and trigger system, espionage, corporations, and modular loading are BtS. A mod that uses them does not load at all under another expansion.
- **Interface mods replace whole screens.** Most GUI work means shipping a modified `CvMainInterface.py` or another `Screens\` file, so two mods that both modify the same screen cannot be combined cleanly.
- **Saved games record content by index.** Inserting rows into a table that a save references shifts indices and corrupts the save; that is also why a mod cannot be added to or removed from an existing game.
- **Assets that merely exist do not load.** A NIF, DDS, or WAV is inert until an `CIV4ArtDefines_*` entry names it and the object references that entry.
- **The engine silently ignores an unparseable file**, so a missing object is diagnosed from the logs, never from the symptom.
- **Multiplayer requires identical mod sets**; a divergent mod list desynchronises the game.
