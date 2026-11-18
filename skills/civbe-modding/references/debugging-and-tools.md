# Debugging and Tools

## Enable Logging First

`config.ini` and `usersettings.ini` under `<user data>`:

```ini
; config.ini
LoggingEnabled = 1
ValidateGameDatabase = 1
EnableTuner = 1
EnableLuaDebugLibrary = 1

; usersettings.ini
DebugMode = 1
```

`EnableTuner = 1` makes FireTuner able to attach; `ValidateGameDatabase = 1` makes the loader report schema and constraint problems; `EnableLuaDebugLibrary = 1` exposes Lua's debug facilities where the build honours it. Recent CivBE reports note that mod scripts do not reach `debug.getinfo` and the like by default, so treat `print` plus `Lua.log` as the primary channel and this flag as a bonus when it functions. A patch or a Steam "verify files" pass can reset these, so retain a copy.

## Log Files

All under `<user data>\Logs\`, and all overwritten on each launch.

| File | Contents | Read it when |
|------|----------|--------------|
| `Database.log` | XML/SQL syntax errors, foreign-key violations, duplicate keys | Anything "does nothing"; anything unlocalised |
| `XML.log` | XML parse results and the files the loader consumed | A file appears not to load at all |
| `Lua.log` | `print` output and script errors | UI missing, a script partially applied |
| FireTuner output | Tuner session console | Interactive probing |

The sequence for a data change is invariably *edit → delete the cache → relaunch*, because the cache is only rewritten at startup.

Representative failure signatures (the Civ5 skill's `debugging-and-tools.md` carries the full catalogue; these are the ones the Beyond-Earth tutorials report):

```
[Xml] ERROR: ... <FileName> ... line N: ...
```
An XML syntax error — an unclosed tag, an unquoted attribute, or a stray `&` and `<` in text. The message names the file and line; the fix is almost invariably escaping.

```
[Database] ERROR: UNIQUE constraint failed: <table>.<column>
```
The key already exists — a second `INSERT`, or a collision with another mod. Switch to `<Update>` or `<Replace>`.

```
[Database] ERROR: FOREIGN KEY constraint failed
```
A referenced `Type` does not exist in the merged database — a missing class row, a typo, or a row from an expansion you did not declare.

```
Runtime Error: MyMod.lua:41: attempt to index a nil value (field 'X')
```
A `GameInfo`/`Players` lookup returned `nil`. Everything after that point in the handler is skipped.

```
TXT_KEY_... shown in the interface
```
The text row is absent, misspelled, in a language table that does not match the active language, or in a file whose earlier statement failed.

## Which File the Error Is In

The loader reports the file, the line, and the constraint. Read the *first* error in `Database.log`, because one failed statement can cascade into several. If the game shows content on one launch and not the next with no source change, an earlier mod in load order changed a row you depend on.

## FireTuner

FireTuner is the interactive console. It is the fastest method of answering "what is the engine's state right now": read a player's affinity level, enumerate the cities, print a table's contents, call a function you exposed, and confirm that an event handler is firing. It is a development aid only — never design a mod whose behaviour depends on a tuner connection, and never ship work that only functions with it attached.

Practical uses: verify that a handler registered after a load, confirm the id `GameInfoTypes` returned for a new `Type`, and check whether a sponsor, unit, or technology actually reached the database.

## Inspecting the Merged Database

The debug snapshot under `<user data>\cache\` is rebuilt at startup from the base data, the expansions, and all enabled mods. Query it with any SQLite browser to observe the row your `<Row>` actually produced, and to locate the id gap a `<Delete>` left. This is the only reliable method of diagnosing a silent failure; `database-xml-sql.md` lists query patterns.

## Extracting Vanilla Data and Art

- **Data**: the shipped XML under `assets/Gameplay/XML/` is the schema reference. Grep it for the table you require and copy a row as the template.
- **Art**: vanilla textures live in `.fpk` archives under `Resource\dx11\` and `Resource\common\`. Extract with Dragon UnPACKer; `.dds` entries are run-length encoded and need the paired `-index` file or a decompressor, and some are DXT4 and open in Photoshop only. The forum thread `Extracting art assets` is the reference.
- **Icons and UI images**: the `Info about UI image files in CBE` thread is the reference for formats, sizes, and the art conventions.

## Tools

| Tool | Purpose | Availability |
|------|---------|--------------|
| SDK / ModBuddy | Project, build, deploy, publish | Windows only, Steam tool |
| FireTuner | Live console and state inspection | Windows (declared by the game's own mods page) |
| Dragon UnPACKer | Unpack `.fpk` archives | Third-party |
| Community DDS unpacker | Decompress the run-length-encoded DDS entries | Third-party |
| SQLite browser | Query the debug snapshot | Third-party |
| Nexus / Blender | `.gr2`/`.fxsxml` model and animation work | Third-party |
| Windows Texture Viewer | Preview DDS, including channels and alpha | NVIDIA, Windows |

The Fandom mods page records that Beyond Earth "currently supports FireTuner, Mod Buddy (available in Steam Tools), and Nexus Mods", and mods are subscribed and enabled through the game's Steam Workshop page.

## What to Check When "Nothing Happens"

1. Is the mod enabled, and does it appear in the Mods screen at all? If not, the folder or `.modinfo` is misplaced or malformed.
2. Does the file appear in `Database.log` as consumed? If not, it is not wired to an action.
3. Does the first line of `Database.log` mention a failure? Fix that before reading the rest.
4. Does the object exist in the merged snapshot? If not, the statement failed or the row was overwritten by a later mod.
5. Does the object exist but with no name, no icon, or no ability? Then the missing piece is text, an atlas row, or the leader link.
6. Does it exist and behave wrongly? Then it is a design problem in the copied columns, not a wiring problem.
