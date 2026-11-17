# Mod Packaging, VFS, Actions, Load Order, and Publishing

## Paths

| Purpose | Windows | Notes |
|---------|---------|-------|
| User data | `%USERPROFILE%\Documents\My Games\Sid Meier's Civilization 5` | `config.ini`, `usersettings.ini`, `Logs`, `cache`, `MODS`, `ModUserData`, `Saves` |
| Installed mods | `<user data>\MODS\` | One folder per mod, each holding the mod name folder and its `.modinfo` |
| Deployed mod | `<user data>\MODS\<Mod Name> (v N)\` | What ModBuddy writes; the `(v N)` folder name is generated |
| Logs | `<user data>\Logs\` | `Database.log`, `XML.log`, `Lua.log`, plus `FireTuner` output |
| Database snapshot | `<user data>\cache\Civ5DebugDatabase.db` | SQLite; the merged result of all loaded XML/SQL |
| Persistent mod data | `<user data>\ModUserData\<name>.db` | Written by `Modding.OpenUserData(name, version)` |
| Game assets | `<steam>\steamapps\common\Sid Meier's Civilization V\Assets\` | Read-only reference and the source of every table's schema |

Aspyr's macOS and Linux ports relocate user data (for the Mac build, conventionally `~/Documents/Aspyr/Sid Meier's Civilization 5`, and the Linux build under its own Aspyr prefix). Locate it by running the game once and searching for `Logs/Lua.log` rather than assuming a path.

The `.civ5proj` and `.modinfo` both live in the same tree as the content; ModBuddy builds into `MODS`, and Steam Workshop uploads from the built copy.

## ModBuddy

ModBuddy ships with the Civilization V SDK (a Steam tool). It is a Visual Studio 2010 isolated shell; the SDK installer pulls the shell redistributable when missing.

1. `File → New → Project → Empty Mod`.
2. Project name becomes the mod name; keep it ASCII and free of path-hostile characters.
3. Right-click the project → **Properties** to set `Name`, `Teaser`, `Description`, `Authors`, `SpecialThanks`, `Homepage`, `AffectsSavedGames`, `Supports*`, `Reload*System`.
4. **Dependencies** tab for expansion/DLC requirements; **References** for soft requirements; **Blocks** for declared incompatibilities.
5. **Actions** tab for database/text actions; **Content** tab for entry points.
6. Per-file properties (`F4`) hold `ImportIntoVFS`.

`MSB4018` / SevenZip exception during build is a Steam–ModBuddy handshake problem: fully exit Steam, launch `Sid Meier's Civilization V SDK.exe` and build; log in to Steam again before uploading.

The project is plain MSBuild; `Civ5Mod.targets` provides `Package Only` and `Deploy Only` configurations, and a mod can be built from the command line with `msbuild`, which is how CI-friendly repositories handle it.

## Virtual File System

Civ5 never reads a mod's files directly. It builds a VFS at load time from files marked for import, so a mod can supply a file at the vanilla relative path and win without touching the installation. The VFS is also the sandbox: nothing outside it can be opened by mod code.

| File class | Import? | Why |
|-----------|---------|-----|
| UI `Context` XML and its Lua | **Yes** | Loaded by name at runtime and by `LuaContext` |
| Lua files loaded by `include()` or by another context | **Yes** | `include` only sees VFS |
| Art (`.dds`, `.fxsxml`, `.gr2`), fonts | **Yes** | Referenced by path from art defines and UI |
| A replacement DLL | **Yes** | The engine swaps it in at load |
| Gameplay XML / SQL consumed by `UpdateDatabase` | No | Read once at startup by the action, not at runtime |
| `Language_*.xml` merged via `UpdateDatabase` | No | Same |
| A Lua file declared directly as an `EntryPoint` | No | The entry point loads it itself; importing duplicates execution |

A file imported *and* declared as an entry point can execute more than once. When in doubt for assets, import; when in doubt for database inputs, do not.

Consequence of the `include` path handling: names are matched loosely and, on some paths, only the first eight characters are compared, so `MapScannerA.lua` and `MapScannerB.lua` are ambiguous. Give included files names that differ early and include them with explicit relative paths.

## Actions

`<Actions>` holds element groups; the useful ones are:

```xml
<Actions>
  <OnModActivated>
    <UpdateDatabase>XML/Buildings.xml</UpdateDatabase>
    <UpdateDatabase>Language/Text.xml</UpdateDatabase>
  </OnModActivated>
  <OnGetDLLPath>
    <SetDllPath>CvGameCore_Expansion2.dll</SetDllPath>
  </OnGetDLLPath>
</Actions>
```

- `OnModActivated` runs in file order as listed. When one file depends on another's rows, order them explicitly.
- **`UpdateDatabase` is the action you should use.** Every large published mod inspected (Corporations, Community Patch/Vox Populi, Scottish Distilleries, No More Turns) routes *both* XML/SQL data and `Language_*` text through it; the loader treats `Language_*` tables the same way as any other table. `UpdateText`, `UpdateIcons`, and `UpdateColors` appear in older ModBuddy documentation and templates; if a file is not being applied, add it as `UpdateDatabase` rather than assuming a missing specialised action tag.
- `SetDllPath` selects which of the shipped DLL names your replacement occupies (vanilla, `_Expansion`, `_Expansion2`). It must match the build you compiled.
- Every file listed must also appear under `<Files>`; ModBuddy maintains that list with an `md5` and the import flag. A stale `md5` after an out-of-band edit causes a rebuild mismatch.

## Entry Points

```xml
<EntryPoints>
  <EntryPoint type="InGameUIAddin" file="UI/MyAddin.lua">
    <Name>MyAddin</Name>
    <Description>Adds the panel</Description>
  </EntryPoint>
  <EntryPoint type="MapScript" file="Maps/MyMap.lua">
    <Name>MyMap</Name>
    <Description>My map script</Description>
  </EntryPoint>
</EntryPoints>
```

- `InGameUIAddin` is the workhorse: it runs the Lua at game start with `ContextPtr`/`Context` available and is the standard way to attach gameplay Lua. Pointing it at a `Context` XML loads that UI instead.
- `MapScript` registers a map-generation script that appears in the map list.
- Multiple entry points are allowed; every one executes.
- An addin pointed at a `.lua` gets no context of its own — `ContextPtr` is the shared base context, and creating controls from it is not supported. For real UI, point at the XML.

## Mod Compatibility and Load Order

- Enable order is user-controlled and matters. Later mods overwrite earlier ones at file level for anything replaced in the VFS; database actions apply in load order, which is why a delete in one mod can break an insert in another.
- There is no dependency solver. `References` and `Dependencies` change what the launcher shows and allows, not what the game loads.
- Because UI replacement is whole-file, two mods that replace the same vanilla UI file cannot both apply. Use the community registration libraries instead of shipping a replacement.
- `Blocks` is the honest way to prevent a known-bad pairing: it makes the launcher refuse the combination rather than producing a subtly broken game.

## Saved Games

`AffectsSavedGames = 1` marks a mod as save-format-affecting. Adding or removing such a mod from an existing save is not supported and frequently corrupts it. Set the flag whenever the mod adds database rows that Lua or the engine persists by id.

`MinCompatibleSaveVersion` is compared against the save's recorded mod version; bumping the mod version past it can invalidate saves that the mod would otherwise load.

## Publishing

1. Build with ModBuddy and verify in game.
2. `ModBuddy → Tools → Publish` (or `Upload`) to push to the Steam Workshop; the first upload creates the item and fixes the `id` in the `.modinfo`.
3. Update by uploading again; the `.modinfo` `id` is what binds the upload to the existing Workshop entry — never change it after publishing.
4. `Teaser` and `Description` accept the markup described in `references/localisation.md`.
5. Keep the `Build/` output in version control only if you accept MD5 churn; committing sources and building in CI is cleaner.

## Troubleshooting Table

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Mod enabled, nothing changes | XML never wired to `UpdateDatabase`, or no actions at all | Add the file to `OnModActivated/UpdateDatabase` |
| UI addin never runs | Lua not declared as `EntryPoint`, or a syntax error in the file | Check `Lua.log` first line for the file name |
| Civilization missing from selection | Fewer than two unique overrides | Add a unique unit or building |
| Second leader ignored | Only one leader per civ is displayed | Use a single leader, or split into two civs |
| Building panel empty | Prerequisite tech not in the tech tree, or building class mismatch | Fix `PrereqTech`; ensure `BuildingClass` exists and names match exactly |
| Crash on game start | `BuildingClass` name mismatch, or a class with no building | Align `BuildingClass`/`DefaultBuilding` |
| Policy UI button gone | A policy row was deleted, leaving an id gap | Never `DELETE` from `Policies`; disable instead |
| Map never appears, instant victory | No valid start region; `Civilization_Start_Region_*` unsatisfiable | Use `REGION_GRASS`/`REGION_PLAINS`, or relax the preference |
| Whole file ignored | A foreign key or duplicate-key error aborted it | `Database.log` names the file and the constraint |
| Mod works alone, breaks with another | Both replace the same vanilla UI file or delete the same rows | Refactor to registration libraries; declare `Blocks` |
| Saved game will not load | `AffectsSavedGames` changed mid-game | Start a new game |