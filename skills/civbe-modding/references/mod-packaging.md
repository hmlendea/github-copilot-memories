# Mod Packaging, VFS, Actions, and Publishing

## Paths

| Purpose | Windows | Notes |
|---------|---------|-------|
| User data | `%USERPROFILE%\Documents\My Games\Sid Meier's Civilization Beyond Earth` | `config.ini`, `usersettings.ini`, `Logs`, `cache`, `MODS`, `ModUserData`, `Saves` |
| Installed mods | `<user data>\MODS\` | One folder per mod, each holding the mod-name folder and its `.modinfo` |
| Deployed mod | `<user data>\MODS\<Mod Name> (v N)\` | What ModBuddy writes; the `(v N)` folder name is generated |
| Logs | `<user data>\Logs\` | `Database.log`, `XML.log`, `Lua.log`, plus FireTuner output |
| Database snapshot | `<user data>\cache\` | SQLite; the merged result of all loaded XML/SQL |
| Persistent mod data | `<user data>\ModUserData\<name>.db` | Written by `Modding.OpenUserData(name, version)` |
| Game assets | `<steam>\steamapps\common\Sid Meier's Civilization Beyond Earth\assets\` | Read-only reference and the source of every table's schema |
| Packed art | `<steam>\...\Resource\dx11\` and `Resource\common\` | `.fpk` archives; extract with Dragon UnPACKer |

The macOS and Linux builds relocate user data (Aspyr prefix). Locate it by running the game once and searching for `Logs/Lua.log` rather than assuming a path. The SDK (and therefore ModBuddy) is Windows-only.

## ModBuddy

ModBuddy ships within the Steam tool *Sid Meier's Civilization: Beyond Earth SDK*. Install the SDK from `Steam → Library → Tools`, then launch it and select ModBuddy; if it requests Visual Studio components, install those first. ModBuddy is a Visual Studio isolated shell, and the forum thread `Microsoft VS 2010 for Modbuddy` documents that particular shell being required by some builds.

1. `File → New → Project` and pick the starter template; the scaffold already contains the correct action skeleton. The project name becomes the mod name; it must remain ASCII.
2. Right-click the project → **Properties** to set `Name`, `Teaser`, `Description`, `Authors`, `Supports Mac`, `AffectsSavedGames`, and the `Reload*System` flags.
3. The **Actions** page maps an event to an action and a file (see below).
4. The **Content** page declares entry points (`InGameUIAddin`, `Custom`, `Map`, `MapScript`, `CityViewUIAddin`, `DiplomacyUIAddin`).
5. Per-file properties (`F4`) hold **Import into VFS**. In some later ModBuddy builds the control is reported as absent while the underlying behaviour still applies; verify by inspecting the generated `.modinfo` rather than trusting the panel.
6. `Build → Build Solution` deploys into `<user data>\MODS\`.

Two build errors recur:

- `CivBEPath must be defined. Use the Project Properties window to set it to the location where Civilization Beyond Earth is installed.` — set `Tools → Options → Civilization Beyond Earth` with the installation path and the user-data path.
- A `SevenZip`/`MSB4018` exception during packaging is a Steam–ModBuddy handshake problem; fully exit Steam, launch the SDK executable directly, build, and log in again before uploading.

The project is plain MSBuild, so a mod can be built from the command line, which is how CI-friendly repositories handle it.

## Virtual File System

CivBE never reads a mod's files directly. It builds a VFS at load time from files marked for import, so a mod can supply a file at the vanilla relative path and win without touching the installation. The VFS is also the sandbox: nothing outside it can be opened by mod code.

The forum reference `File attributes/properties - Is that VFS, InGameUIAddin or UpdateDatabase?` provides the per-extension decision; the Civ5 skill's `mod-packaging.md` reproduces it in full. The classes that matter most:

| File class | Import? | Action / entry point |
|-----------|---------|----------------------|
| UI `Context` XML and its paired Lua | Yes | `InGameUIAddin` |
| Lua included by another file or loaded by a context | Yes | none |
| A Lua file that registers its own events or runs at startup | No | `InGameUIAddin` |
| Art (`.dds`, `.fxsxml`, `.gr2`, `.fsmxml`, `.ftsxml`, `.dge`), fonts (`.ggxml` with a same-named `.dds`) | Yes | `Reload Landmark System` / `Reload Unit System` where applicable |
| Gameplay XML / SQL consumed by `UpdateDatabase` | No | `OnModActivated` → `UpdateDatabase` |
| `Language_*` rows merged through `UpdateDatabase` | No | `OnModActivated` → `UpdateDatabase` |
| Map (`.civ5map`) | Stand-alone: Yes with a `Map` entry; scenario map: No | `Map` / `Custom` |
| Map script (`.lua`) | Yes | `MapScript` |
| Additional or replacement audio | Yes | `Reload Audio System` plus the audio define |

A file imported *and* declared as an entry point can execute more than once. When in doubt for assets, import; when in doubt for database inputs, do not.

## Actions

```xml
<Actions>
  <OnModActivated>
    <UpdateDatabase>XML/MySponsor.xml</UpdateDatabase>
    <UpdateDatabase>Language/Text.xml</UpdateDatabase>
  </OnModActivated>
</Actions>
```

- `OnModActivated` runs in file order as listed. When one file depends on another's rows, order them explicitly.
- **`UpdateDatabase` is the action to use.** Both gameplay XML/SQL and `Language_*` text route through it; the loader treats the `Language_*` tables as ordinary tables. Tutorials that mention only `UpdateDatabase` are correct.
- Every file listed must also appear under `<Files>` in the `.modinfo`; ModBuddy maintains that list with an `md5` and the import flag. A stale `md5` after an out-of-band edit causes a rebuild mismatch.

## Entry Points

```xml
<EntryPoints>
  <EntryPoint type="InGameUIAddin" file="UI/MyPanel.xml">
    <Name>MyPanel</Name>
    <Description>Adds the sponsor panel</Description>
  </EntryPoint>
  <EntryPoint type="MapScript" file="Maps/MyMap.lua">
    <Name>MyMap</Name>
    <Description>My map script</Description>
  </EntryPoint>
</EntryPoints>
```

- `InGameUIAddin` is the workhorse: pointing it at a `Context` XML loads that UI, and pointing it at a `.lua` runs the script at game start with the shared base context. An addin pointed at a `.lua` has no context of its own, so `ContextPtr` is the shared base context and creating controls from it is not supported — point at the XML for real UI.
- `MapScript` registers a map-generation script that appears in the map list.
- Multiple entry points are permitted; every one executes.

## Mod Compatibility and Load Order

- Enable order is user-controlled and matters. Later mods overwrite earlier ones at file level for anything replaced in the VFS; database actions apply in load order, which is why a `<Delete>` in one mod can break an `<Row>` in another.
- There is no dependency solver. `References` and `Dependencies` change what the launcher displays and permits, not what the game loads.
- Because UI replacement is whole-file, two mods that replace an identical vanilla UI file cannot both apply. Use community registration libraries rather than shipping a replacement.
- `Blocks` is the honest method of preventing a known-bad pairing: it makes the launcher refuse the combination rather than producing a subtly broken game.

## Saved Games

`AffectsSavedGames = 1` marks a mod as save-format-affecting. Adding or removing such a mod from an existing save is not supported and frequently corrupts it. Set the flag whenever the mod adds database rows that Lua or the engine persists by id, which is the usual case for a sponsor, unit, technology, affinity, or quest mod.

## Publishing

1. Build with ModBuddy and verify in game.
2. `ModBuddy → Tools → Publish` (or `Upload`) pushes to the Steam Workshop; the first upload creates the item and fixes the `id` in the `.modinfo`.
3. Update by uploading again; the `.modinfo` `id` binds the upload to the existing Workshop entry — never change it after publishing.
4. `Teaser` and `Description` accept the markup described in `references/localisation.md`.
5. State the Rising Tide requirement, the `AffectsSavedGames` behaviour, and any known mod conflict in the description rather than leaving them implicit.

## Troubleshooting Table

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Mod listed, nothing changes | XML never wired to `UpdateDatabase`, or no actions at all | Add the file to `OnModActivated` → `UpdateDatabase` |
| Sponsor absent from the sponsor-select screen | Incomplete row set, or no action | Add the leader link, free building classes, free techs, city names, and text; check the action |
| UI addin never runs | Lua/XML not declared as an entry point, or a syntax error | Check the first line of `Lua.log` for the file name |
| Entire XML file ignored | Foreign-key or duplicate-key error aborted it | `Database.log` names the file and the constraint |
| Icons missing or placeholder | `IconTextureAtlases` row absent for that size, or the file is not imported | Add every size the UI requests; set Import into VFS |
| Text displays as `TXT_KEY_...` | The `Language_en_US` row is absent, misspelled, or in an aborted file | Add the row; confirm the tag matches the column value exactly |
| Mod operates alone, breaks with another | Both replace an identical vanilla UI file or delete identical rows | Refactor to registration libraries; declare `Blocks` |
| Saved game will not load | `AffectsSavedGames` changed mid-game | Start a new game |
