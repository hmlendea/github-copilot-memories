# Lua Scripting

CivBE's Lua is the same embedded Lua 5.1 engine as Civ5's, with the same stripped standard library and the same event buses. The Civ5 skill's `lua-scripting.md` documents the sandbox, the `include` traps, the event list sources, object lookups, and persistence in full; this file records the Beyond-Earth specifics and the patterns that matter for its content systems.

## The Sandbox

- Lua 5.1, with `io`, `file`, `package`, `os` (except `clock`/`date`/`time`/`difftime`), `load`/`loadfile`/`loadstring`/`module`/`require`, and `getfenv`/`setfenv` removed.
- `include(file[, useRegex])` is the loader; it only sees the VFS, so an included file must be imported.
- The `debug` library is **not** available to mod scripts by default in CivBE; a 2026 forum thread asks specifically how to enable `debug.getinfo` and friends and the answer is a configuration change, not something a normal mod relies on. Debug with `print` and `Lua.log`, or by extracting logic into plain functions you can call from FireTuner.
- A syntax error kills the entire file; a runtime error kills the rest of that fragment. The game continues, so the symptom is a partial effect, not a crash.

## Event Buses

| Bus | Purpose | Typical use in CivBE |
|-----|---------|----------------------|
| `Events` | UI and shell events routed through the engine | `LoadScreenClose`, `SequenceGameInitComplete` for re-registration |
| `GameEvents` | Game-rule events | `PlayerDoTurn`, `CityCanTrain`, `UnitKilledInCombat`, `PlayerAdoptPolicy` (used for virtues), tech and quest events |
| `LuaEvents` | Same-mod and cross-mod dynamic events | The only supported inter-context channel; how a UI panel talks to a gameplay script |

The event names are the Civ5 set plus the Beyond-Earth additions; enumerate them from the shipped `assets/` Lua rather than from a tutorial, because the community event listings for CivBE are incomplete.

## Patterns

Declare a namespace table per file to avoid colliding with vanilla globals:

```lua
MyMod = MyMod or {}
```

### Events That Do Not Survive Loading

Handlers registered at file scope frequently cease firing after a save/load cycle, the identical behaviour documented for Civ5. Re-register from a load event and print so you can confirm in the log:

```lua
function MyMod.OnLoadScreenClose()
    GameEvents.PlayerDoTurn.Add(MyMod.OnPlayerDoTurn)
end
Events.LoadScreenClose.Add(MyMod.OnLoadScreenClose)
print("MyMod: bootstrap loaded")
```

### Guard Every Lookup

`GameInfoTypes`, `GameInfo`, `Players`, and `Teams` all return `nil` for an id that is absent (expansion missing, typo, or a row deleted by another mod). A `nil` dereference truncates the rest of the handler.

```lua
local techType = GameInfoTypes["TECH_MYMOD_PREREQ"]
if techType and Teams[Game.GetActiveTeam()]:IsHasTech(techType) then
    -- ...
end
```

### Granting Content

Granting a technology, unit, building, or yield to a player is a `GameEvents` handler plus the matching engine method, in the pattern the forum thread `How to grant a tech to a player` arrives at. Invariably resolve the `Type` to its id with `GameInfoTypes` first and guard the result.

### Conditional Effects Belong in Data Where Possible

Passive yields and unconditional bonuses belong in a hidden ("dummy") building or a trait column applied by XML, because they survive save/load and cost nothing per turn. Reserve Lua for what tables cannot express: an effect conditioned on an affinity level reached, on a quest outcome, on a covert operation resolving, or on a unit dying.

```lua
-- example shape: a per-turn effect conditioned on affinity, which data alone cannot express
function MyMod.OnPlayerDoTurn(playerID)
    local player = Players[playerID]
    if not player or player:IsBarbarian() then return end
    -- read the affinity level, then apply the effect
end
GameEvents.PlayerDoTurn.Add(MyMod.OnPlayerDoTurn)
```

### Persistence

CivBE inherits Civ5's string-based persistence (`ModData` / `SetScriptData`-style storage backed by SQLite). It is slow; cache in a local table, write only on change, and never treat the store as private — it is shared with every other enabled mod. Per-turn writes are measurable, so never persist in a turn handler without a reason.

## Where Lua Is Required

- **Quest logic.** Quest definition rows declare the objective; the trigger and the completion check are Lua.
- **Affinity-driven effects** that depend on a threshold being crossed at a moment other than the turn boundary.
- **Covert operations** whose outcome depends on the target's state.
- **UI behaviour.** Every context behaviour is registered from Lua with `RegisterCallback` (`ui-and-art.md`).
- **Anything the tables have no column for.** Walk the shipped XML first; a column that already exists is invariably cheaper than a handler.

## Performance and Compatibility

- A `PlayerDoTurn` handler runs for every player every turn; restrict it to a few comparisons and return early.
- Never scan all plots or all cities in a turn handler for something a table column could express.
- Determinism matters: a handler that reads unordered data and changes game state desynchronises multiplayer.
- Prefer `LuaEvents` for cross-context communication over reaching into another context's globals, which are isolated.
