# Debugging, Logging, and Tools

## Enable the Tuner and Logging First

`<user data>\AppOptions.txt`:

```ini
;0 windowed, 1 fullscreen, 2 windowed without title bar
FullScreen 0

[Debug]
;Enable FireTuner
EnableTuner 1
```

Keep a copy: a patch or a "verify files" pass can reset these. `FullScreen 0` is required because the FireTuner needs to sit alongside the game.

## Log Files

All in `<user data>\Logs\`, and all overwritten on each launch:

| File | Contents | Read it when |
|------|----------|--------------|
| `modding.log` | Mod scan, load order, which actions each mod contributed, criteria evaluation | The mod is absent from Additional Content, or an action appears not to run |
| `Database.log` | SQL/XML syntax errors, foreign-key violations, duplicate keys | Anything "does nothing"; anything unlocalised |
| `GameEffects.log` | Modifier and requirement resolution: unknown effect/requirement types, bad arguments, unresolved sets | A modifier or requirement has no effect |
| `Lua.log` | `print` output and script errors | UI missing, script partially applied |
| `FireTuner.log` | Tuner session output when attached | Interactive probing |
| `AI.log`, `Diplomacy.log`, `RandomEvents.log` | Domain-specific traces | AI or event behaviour questions |

Two Windows conveniences: keep the logs open in an editor that reloads changed files, and remember the cache is only rewritten at startup, so the sequence for a data change is always *edit → delete cache → relaunch*.

Representative failure signatures:

```
[Database] ERROR: no such column: MyColumn
```
A column name is wrong, or it exists only in an expansion. Statements after it in the same file still run.

```
[Database] ERROR: UNIQUE constraint failed: Types.Type
```
The key already exists — a second `INSERT`, or a collision with another mod. Switch to `UPDATE` or `INSERT OR REPLACE`.

```
[GameEffects] WARNING: Modifier MODIFIER_X: unknown effect type EFFECT_Y
```
The modifier is dropped. Verify the `DynamicModifiers` row and the exact effect name.

```
[GameEffects] WARNING: … requirement set REQSET_X has no requirements
```
The set resolves, but to nothing, so it always passes. Often the sign that the wrong set id was used.

```
Runtime Error: MyMod.lua:41: attempt to index a nil value (field 'X')
```
A `GameInfo`/`Players` lookup returned `nil`. Everything after that point in the handler is skipped.

## Cache Snapshots

The game writes two SQLite files under `<user data>\Cache\` (per some guides, `%LOCALAPPDATA%\Firaxis Games\Sid Meier's Civilization VI\Cache`):

| File | Contents |
|------|----------|
| `DebugGameplay.sqlite` | The merged gameplay database: `Types`, content tables, modifiers, requirements |
| `DebugLocalization.sqlite` | `LocalizedText` |
| `DebugConfiguration.sqlite` | Configuration-layer data |

Query them instead of inspecting source files — this is the only way to see what all enabled mods actually produced:

```bash
sqlite3 "DebugGameplay.sqlite" "SELECT Type, Kind FROM Types WHERE Type LIKE '%MYMOD%';"

sqlite3 "DebugGameplay.sqlite" \
  "SELECT m.ModifierId, d.EffectType, d.CollectionType
   FROM Modifiers m JOIN DynamicModifiers d ON d.ModifierType = m.ModifierType
   WHERE m.ModifierId LIKE '%MYMOD%';"

# Every attachment of a modifier, so you can tell whether it is attached twice
sqlite3 "DebugGameplay.sqlite" \
  "SELECT BuildingType, ModifierId FROM BuildingModifiers WHERE ModifierId LIKE '%MYMOD%';"

# Which table actually references an effect you are trying to copy
sqlite3 "DebugGameplay.sqlite" "PRAGMA table_info(DynamicModifiers);"
```

Delete the `Cache` folder when diagnosing stale state, and reopen the file in the browser after each relaunch.

## Tools

| Tool | Purpose |
|------|---------|
| ModBuddy | Project, properties, actions, build and deploy |
| FireTuner / LiveTuner | Attached Lua console, autocomplete, pre-built debug panels |
| Development Tools' documentation | Local HTML reference for Content Creation, FireFX, Forge UI, Forge UI Controls, Modding |
| Asset Editor | Art defines, Pantry cook, model preview |
| WorldBuilder | Maps and scenarios |
| Steam Workshop Uploader | Publication |
| SQLite Browser / `sqlite3` | Cache inspection — the single most useful third-party tool |
| Notepad++ or another reloading editor | Watching `Database.log` live |

## FireTuner

1. Launch the SDK, start FireTuner, then start the game; the panel shows *Connected* once a game is in progress.
2. The console runs Lua in the game process and mirrors `print` output.
3. `TAB` in the console completes from the live API.
4. `File → Open Panel` loads the `.ltp` panels under `<steam>\steamapps\common\Sid Meier's Civilization VI\Debug\`; reading their Lua is the fastest way to learn correct API usage.
5. Typical probe:

```lua
for i = 0, GameDefines.MAX_MAJOR_CIVS - 1 do
    local p = Players[i]
    if p ~= nil and p:IsAlive() then
        print(i, p:GetCivilizationType(), p:GetCapitalCity() and 1 or 0)
    end
end
```

Print `nil` explicitly — `print` drops `nil` arguments, so print `(x or 'nil')` to see absent values.

6. FireTuner is a development aid. Never rely on a tuner connection for a shipped mod's behaviour.

## Symptom-to-Cause Catalogue

| Symptom | Most likely cause |
|---------|-------------------|
| Mod absent from Additional Content, or present but greyed | `.modinfo` not in the mod root, invalid XML, or an unmet `<Dependencies>` entry |
| Mod listed, but nothing changes | Action missing a `<File>`, or the file is not in the action's list, or a criteria gated it out |
| Data applies in the base game but not with an expansion (or vice versa) | Action not gated, or it references a ruleset-specific table or column |
| Content row appears but with `LOC_...` text | Text shipped through `UpdateDatabase` instead of `UpdateText`, or a tag typo |
| Object visible but unusable/unreachable | Missing `Types` row, missing `Prereq*` row, or missing boost row for a tech/civic |
| Modifier has no effect | Wrong collection class, wrong attachment table, missing requirement set, or a mis-cased `ModifierArguments` name |
| Icon blank at one size only | That `IconSize` row is missing from `IconTextureAtlases`, or the wrong `Index` |
| UI control nil | Element id typo, or the context's Lua file not in `ImportFiles`/`<Files>` |
| Crash on load | A `DELETE`/`UPDATE` that breaks a foreign key another vanilla row relies on |
| Save cannot load | Mod set changed, or `AffectsSavedGames` mismatch between the mod and the save |
| Game desyncs in multiplayer | Differing mod sets, criteria, or load order; or a UI script mutating gameplay state |

## Order of Investigation

1. `modding.log` — did the mod load, and did each action run?
2. `Database.log` — the first error, in file order, is the one that matters; later errors are often consequences.
3. `GameEffects.log` — modifiers and requirements.
4. Cache snapshot — what the rows actually became.
5. `Lua.log` — only after the data is confirmed.
6. FireTuner — to inspect live state and to test a hypothesis without a restart.