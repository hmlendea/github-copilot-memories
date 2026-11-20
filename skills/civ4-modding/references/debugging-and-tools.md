# Debugging and Tools

## Enable Logging First

Nothing in Civ4 modding is diagnosable without logging, and the ini that controls it is in the user directory, not the mod folder.

| File | Purpose |
|------|---------|
| `<user dir>\CivilizationIV.ini` | The game's own ini: logging switches, Python console, custom-asset toggles |

Set, at minimum:

```ini
LoggingEnabled = 1
EnablePythonConsole = 1
```

and, when the symptom is intermittent or multiplayer-related:

```ini
SynchLog = 1
RandLog = 1
MessageLog = 1
OverwriteLogs = 1
```

`OverwriteLogs = 1` keeps the logs from growing without bound across sessions; leave it at `0` while reproducing a bug so the previous session's log survives.

## The Logs

All of them land in `<user dir>\Logs\`.

| Log | Contents |
|-----|----------|
| `PythonErr.log` | Python exceptions with traceback — the first place to look for anything that "does nothing" |
| `PythonDbg.log` | `CvUtil.pyPrint` output; the modder's own channel |
| `init.log` | Start-up: which mod loaded, which XML files were read, which were rejected |
| `Res.log` | Resource and art loading |
| `Rand.log` | Random-number draws, with `RandLog = 1` |
| `Synch.log` | Multiplayer synchronisation data, with `SynchLog = 1` |
| `MPLog.txt` | Multiplayer connection log |
| `MessageLog.txt` | Message traffic, with `MessageLog = 1` |
| `xml.log` / per-table logs | The XML loader's own output where the build emits it |

The diagnostic order is: `init.log` (did the mod and its files load at all) → the XML loader's complaint (was a table rejected) → `PythonErr.log` (did Python fail) → `PythonDbg.log` (what did the mod's own tracing say).

## The Python Console

With `EnablePythonConsole = 1` the game exposes an interactive Python console; the community binds it to a key (`Shift+~` or `` ` `` in most builds). It evaluates against the same interpreter and the same `CvPythonExtensions` module the game uses, so it is the live way to:

- Inspect state: `gc.getActivePlayer().getGold()`, `gc.getGame().getGameTurn()`.
- Resolve a type: `gc.getInfoTypeForString("UNIT_MYMOD_LONGBOW")` — a `-1` here is a `Type` that no loaded file declares.
- Trigger a handler by hand to confirm it is reachable.
- Read `CyTranslator().getText("TXT_KEY_...", ())` to confirm whether a text key resolves.

The console reaches the same objects as a mod's Python, so a value it can read is a value a handler can use — and a value it cannot read is not exposed by the SDK.

## In-Game Diagnostics

| Tool | Use |
|------|-----|
| WorldBuilder | Inspect the live map, place any unit/building/improvement, and save a WBS to reproduce a state |
| FireTuner equivalent | The Python console plus the debug screens (`CvDebugInfoScreen`, `CvDebugTools`) |
| `CvDebugTools.py` / `CvPerfTest.py` | Shipped debug and performance modules |
| The Civilopedia | The fastest check that a new content entry loaded and that its text and art resolved; a missing entry is a missing row, and a `TXT_KEY_` here is a missing text row |
| Chipotle / reveal-map cheat | Reach the late-game state a rule needs without playing to it |

## Third-Party Tools

Modiki's *Civ4 Useful Programs* page is the canonical list, grouped by purpose:

| Group | Tools |
|-------|-------|
| XML | XML schema-aware editors; **Civ4 File Checker** (validates XML before launching and is explicitly recommended for everyone); XML Marker |
| Python | Any text editor; the community's **Civilization4 Python API Reference Guide**, which documents the `Cy*` surface; Python IDLE is listed but discounted, with the recommendation that work needing a real IDE belongs in the SDK |
| Graphics | Blender, Gmax, 3ds Max, NifTools, NifSkope, DXTBmp, GIMP with its DDS plugin, the **GameFont.tga Editor Utility**, the BMP↔WorldBuilderSave converter |
| Map/Scenario | The WorldBuilder-like editors and generators, and the community's expanded in-game WorldBuilder component |
| SDK | The compiler and library set above, plus the community's clean SDK sources and error databases |
| Packaging | NSIS for installers, 7-Zip, PakBuild for the game's package files |
| General | Civchecker, a search tool for the asset tree |

The community's consistent advice is that a plain text editor is preferable to a specialised XML editor for the XML itself, and that the one mandatory tool is an XML validation pass. **Validate before launching**: a schema error caught by a checker costs seconds, and the same error in game costs a launch, a log read, and a restart.

## Failure Catalogue

| Symptom | Most likely cause | Where to look |
|---------|-------------------|---------------|
| Mod loads, nothing changes | The mod replaces no file the game reads, or the replacement file was rejected | `init.log`; confirm the path and the schema |
| A modular file has no effect | `ModularLoading` is not `1`; file outside `Assets\Modules\`; entry element mismatch | The mod's ini; the target table's root element |
| One object missing, others fine | A referenced `Type` is absent (class, art define, text key) | `init.log`, `Res.log`; walk the dependency chain |
| Text shows as `TXT_KEY_...` | The text row is missing or overridden | The mod's `Assets\XML\Text\` file |
| Wrong icon | A bad font index or atlas coordinate | The `Button` field against the font sheet's index comment |
| Callback seems ignored | Its switch in `PythonCallbackDefines.xml` is `0` | The mod's copy of that file |
| Python handler runs but nothing happens | An exception after the first effect, aborting the rest of the handler | `PythonErr.log` |
| Map loads part-empty | `num plots written` disagrees with the plot count | Hand-edit the WBS header |
| Scenario loads with missing content | `ModPath` wrong or absent | The WBS `BeginGame` block |
| Crash on loading a save | Table indices shifted by inserted rows, or a new serialised member | Revert the content addition; the save is not recoverable |
| Multiplayer desync or refusal | Divergent mod or DLL between clients | `Synch.log`, `MPLog.txt` |
| Works for the author, not for others | The mod edited the base tree, or depends on `CustomAssets` | Move the change into the mod folder; set `NoCustomAssets` |
| Everything breaks after a patch | The mod's copied tables pin the pre-patch content | Diff the tables against the new base tree |

## Isolation Procedure

When the cause is unclear, bisect the mod rather than reasoning about it:

1. Launch with logging on and confirm whether the mod loaded at all.
2. Disable the mod's Python by renaming `Assets\Python\` temporarily: if the symptom disappears, it is Python; if it persists, it is XML or art.
3. Disable the mod's XML likewise: a missing feature that survives both is an art or path problem.
4. With Python involved, add `CvUtil.pyPrint` tracing at the top of the suspected handler; an untraced handler was never entered, and a traced one that stops mid-way threw after the last trace.
5. With XML involved, replace the suspect file with the unmodified vanilla file: if the symptom disappears, the edit is at fault; if not, the file is not the one being loaded.
6. Reproduce from a clean install if a third-party mod is also present. Civ4 loads only one mod, but `CustomAssets` is always present unless `NoCustomAssets = 1`, and it is the usual hidden variable.

## Reproducing and Reporting

- Record the exact expansion and patch level, the mod list (one mod, plus whether `CustomAssets` is populated), the map size and game speed, and whether the game was loaded from a save or started fresh.
- Attach `init.log` and `PythonErr.log` rather than a description of them.
- A minimum reproduction is a scenario (WBS) plus the smallest mod that shows the problem; anything else leaves the reporter guessing.
