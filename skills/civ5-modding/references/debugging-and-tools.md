# Debugging, Logging, and Tools

## Enable Logging First

`<user data>/config.ini`:

```ini
EnableTuner = 1
ValidateGameDatabase = 1
EnableLuaDebugLibrary = 1
LoggingEnabled = 1
```

`<user data>/usersettings.ini`:

```ini
DebugMode = 1
```

`ValidateGameDatabase` and `LoggingEnabled` are the two that matter for XML/SQL work; `EnableLuaDebugLibrary` gives stack traces in `Lua.log` and enables the `debug` table. `EnableTuner` mirrors all Lua output to FireTuner when it is attached. `DebugPanel = 1` in `config.ini` reveals an in-game debug panel (opened with the `2` key on most layouts).

Keep a copy of the edited INI files: patches and "verify files" reset them.

## Logs

| File | Contents | Read it when |
|------|----------|--------------|
| `Logs/Database.log` | XML/SQL statement errors, foreign-key violations, duplicate keys, `TXT_KEY` warnings | Anything "does nothing", anything unlocalised |
| `Logs/XML.log` | XML well-formedness and column-name errors | A file is rejected outright |
| `Logs/Lua.log` | `print` output, runtime errors with stack traces | UI does not appear, effect partially applied |
| `Logs/FireTuner.log` | Tuner session output when attached | Interactive probing |
| `cache/Civ5DebugDatabase.db` | Snapshot of the merged database after all mods applied | Verifying what your rows actually became |

Paths are in `<user data>`; on Windows 7 that is `Documents\My Games\Sid Meier's Civilization V`, and the platform ports relocate it.

Representative messages and their meaning:

```
[6904.323] Tag (TXT_KEYMODDING_SHOWDLCMODS) does not start with 'TXT_KEY_'
```
A text value used as a key is malformed; the entry is skipped.

```
[6903.917] Invalid Reference on Leader_Flavors.LeaderType - "LEADER_HARALD" does not exist in Leaders
```
Foreign key violation; the whole remaining file is abandoned.

```
Runtime Error: [string "…"]:41: attempt to concatenate local 'name' (a nil value)
stack traceback: …
```
Lua runtime error at that line; everything after it in that chunk is skipped. Paths are truncated when the file was registered by a `content` action rather than as a normal entry point — provide a custom stack trace or a minimal root context to keep paths visible.

## The Database Snapshot

Every game start writes `cache/Civ5DebugDatabase.db`, a SQLite file containing vanilla plus every loaded mod's changes. Use it for evidence rather than inspection of the XML:

```bash
sqlite3 "$HOME/Documents/My Games/Sid Meier's Civilization V/cache/Civ5DebugDatabase.db" \
  "SELECT Type, Cost, PrereqTech FROM Units WHERE Type LIKE 'UNIT_MYMOD%';"
sqlite3 … "SELECT * FROM sqlite_master WHERE type='table' AND name LIKE '%MyMod%';"
sqlite3 … "PRAGMA foreign_key_list(Building_YieldChanges);"
```

Tools: `sqlite3` (or DB Browser / SQLiteSpy / SQLite Manager on Windows). Delete the snapshot when diagnosing stale state.

## FireTuner

FireTuner is a separate executable in the SDK. It attaches to a running game, shows the mirrored Lua output, provides an interactive console, and accepts custom panels. Typical use:

```lua
for i = 0, GameDefines.MAX_MAJOR_CIVS - 1 do
  local p = Players[i]
  if p and p:IsAlive() then print(i, p:GetCivilizationType(), p:GetCapitalCity() and 1 or 0) end
end
```

Print `nil` explicitly — `print` drops `nil` arguments, so print `(x or 'nil')` to see absent values.

For an end-user-facing error path, wrap risky calls in `xpcall` and popup the result:

```lua
local ok, err = xpcall(MyMod.Dangerous, function(e) return debug.traceback(e, 2) end)
if not ok then
  Events.SerialEventGameMessagePopup({ Type = ButtonPopupTypes.BUTTONPOPUP_TEXT,
    Data1 = 800, Option1 = true, Text = "MyMod: " .. tostring(err) })
end
```

## In-Game Editor (IGE)

The community In-Game Editor spawns units and buildings, grants technologies and policies, edits terrain, and triggers wars. It is the fastest way to reach the game state a bug needs. Combine it with the FireTuner tech/policy panels to confirm a row exists at all.

## Tooling

| Tool | Purpose |
|------|---------|
| ModBuddy (SDK) | IDE, build, package, upload |
| World Builder (SDK) | map/scenario creation |
| FireTuner (SDK) | console, Lua output, custom panels |
| Nexus / Nexus Buddy 2 | 3D model import/export (`fxsxml`, `gr2`) |
| Dragon UnPACKer | extract `.fpk` packages |
| DDS Unpacker | repair over-compressed DDS |
| GIMP / Paint.NET / NVIDIA DDS tools | author `.dds` |
| `sqlite3`, DB Browser, SQLiteSpy | inspect the snapshot and `ModUserData` |
| Notepad++ / VS Code | search across all `Assets` XML to find the table you need |
| Visual C++ 2008/2010 toolchain | compile `CvGameCoreDLL` |
| Diff/merge tool | compare your mod's copy against a freshly patched vanilla file |

### DLL Work

The SDK ships `CvGameCoreDLL` sources with solutions for VS2008/2010/2012. A 2012 solution also builds in 2013; the VC++ 2008 toolchain is still required. Before compiling, change the `afxres.h` include in each `CvGameCoreDLL.rc` to `windows.h`. Build the expansion variant you target, add the DLL to the mod with import-to-VFS enabled, and select it with `SetDllPath`. Adding a column to a vanilla table is only visible to C++ if the corresponding schema and `CvGameCoreDLL` changes ship together; a schema-only change crashes, and a column-only change is silently ignored by the engine.

## Failure Catalogue

| Symptom | Cause | Fix |
|---------|-------|-----|
| Mod row absent from snapshot | File aborted on a foreign key or duplicate key | Read `Database.log`, fix ordering or duplicate `Type` |
| `TXT_KEY_…` on screen | Missing `Language_*` row, or its file aborted | Add the row; re-check the log |
| Unit/building unbuildable, panel empty | `PrereqTech` not wired into the tech tree | Add `Technology_PrereqTechs` path, or use a real tech |
| Crash immediately on game start | `BuildingClass` name mismatch or class without a default building | Align names; ensure `DefaultBuilding` exists |
| Selection screen missing the civ | Fewer than two unique overrides | Add a unique unit or building |
| Only the first leader listed | One leader per civ is a UI limit | Ship one leader per civ |
| Map ends instantly | Start-region preference unsatisfiable on that map | Adjust `Civilization_Start_Region_*` |
| Social-policy screen empty after another mod | A mod `DELETE`d `Policies` rows, leaving id gaps | Never delete; disable instead |
| Second load loses effects | File-scope event handlers not restored after load | Re-register from `Events.LoadScreenClose` |
| `include()` reports success, no globals | Called from a UI event handler | Include at file scope, or reload the context |
| Wrong file loaded by `include` | VFS compares only the first eight characters on some paths | Rename so names differ early; pass the full relative path |
| Mod broken only with another mod | Both replace the same UI file or delete the same rows | Use registration libraries; declare `Blocks` |
| Existing save refuses to load after enabling | `AffectsSavedGames = 1` | Start a new game |
| `MSB4018`/SevenZip on build | Steam/ModBuddy handshake | Quit Steam, launch `Sid Meier's Civilization V SDK.exe`, build; log in before uploading |