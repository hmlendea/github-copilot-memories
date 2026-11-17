# Lua Scripting

Civ5's Lua is based on **Lua 5.1.4**, stripped of `io`, `file`, `package`, `os` (only `clock`/`date`/`time`/`difftime` remain), `debug` (added in May 2012 via `EnableLuaDebugLibrary`), `load`/`loadfile`/`loadstring`/`module`/`require`, `__G`, and `getfenv`/`setfenv`. Code loading instead uses `include(file[, useRegex])`.

Everything practical runs through four event buses:
- **`Events`** — UI and shell events routed through the engine (`LoadScreenClose`, `SerialEventCityCaptured`, UI field-change dirty events).
- **`GameEvents`** — game-rule events (`PlayerDoTurn`, `CityCanTrain`, `PlayerAdoptPolicy`, `CanDeclareWar`…). The full list is on `Lua Game Events`; newer patches add flag-only events (`Events.InstalledModsUpdated`).
- **`LuaEvents`** — same-mod or cross-mod dynamic events; the only supported inter-context communication path. Any context may fire/listen.
- Debug-logged events: `DoFunc`/`CanFunc` bodies are **not** instrumented by logging, so debug them by extracting to testable functions (documented caveat in `Debugging (Civ5)`).

## Standard Patterns

Declare one namespace table per file to avoid colliding with vanilla globals:

```lua
MyMod = MyMod or {}
```

### Events That Do Not Survive Loading

Handlers registered at file scope frequently stop firing after a save/load cycle. Register in `Events.LoadScreenClose` or `Events.SequenceGameInitComplete`, and emit a `print` so you can verify registration in the FireTuner output:

```lua
function MyMod.OnLoadScreenClose()
    GameEvents.PlayerDoTurn.Add(MyMod.OnPlayerDoTurn)
end
Events.LoadScreenClose.Add(MyMod.OnLoadScreenClose)
print("MyMod: bootstrap loaded")
```

### The Guard Pattern

`Players`, `Map.GetPlot(x, y)`, `GameInfo`, `GameInfoTypes` all yield `nil` for missing ids, and a `nil` dereference aborts the rest of the chunk:

```lua
local player = Players[iPlayer]
if not player or not player:IsAlive() then return end

local civType = GameInfo.Civilizations[player:GetCivilizationType()]
if not civType or civType.Type ~= "CIVILIZATION_MYMOD" then return end
```

Never index `GameInfoTypes["UNIT_…"]` without a `Type` guard bundled inside the same test, because a BNW-only type missing from G&K is `nil`.

### Dummy Building Pattern (Preferred Over Per-Turn Lua)

Persistent effects that XML columns cannot express:

```lua
-- once, at init
local DUMMY_BUILDING = GameInfoTypes["BUILDINGCLASS_DUMMY_EFFECT"]

function MyMod.ApplyDummyBuildings()
    for iPlayer = 0, GameDefines.MAX_MAJOR_CIVS - 1 do
        local pPlayer = Players[iPlayer]
        if pPlayer and pPlayer:IsAlive() then
            local pCity = pPlayer:GetCapitalCity()
            if pCity then
                pCity:SetNumRealBuilding(DUMMY_BUILDING, 1)
            end
        end
    end
end
Events.SequenceGameInitComplete.Add(MyMod.ApplyDummyBuildings)
```

`SetNumRealBuilding` persists with the city through saves; set-and-forget effects cost nothing per turn. Grant it again on any event that can remove it (captured city, razed city).

### Persistence

```lua
local gSave = Modding.OpenSaveData()
local gProps = {}

function MyMod.GetProperty(name, default)
    if gProps[name] == nil then gProps[name] = gSave.GetValue(name) end
    local v = gProps[name]
    return v == nil and default or v
end

function MyMod.SetProperty(name, value)
    if gProps[name] == value then return end
    gSave.SetValue(name, value); gProps[name] = value
end
```

Use your own mod-specific key prefix (`MYMOD_`). `OpenSaveData` is shared by all mods in one save; `Modding.OpenUserData("MyMod", 1)` writes `<user data>/ModUserData/MyMod.db`.

### Database Access from Lua

```lua
local RESULTS = {}
for row in DB.Query("SELECT Type FROM Buildings WHERE MyModColumn = 1") do
    table.insert(RESULTS, row.Type)
end
```

Reads are cheap; per-turn writes are not. Batch multiple `INSERT OR REPLACE`/`UPDATE` rows into one statement.

### UI Addin Registration

In `<EntryPoints>`:

```xml
<EntryPoint type="InGameUIAddin" file="UI/MyModPanel.xml">
    <Name>MyModPanel</Name>
    <Description>My mod panel</Description>
</EntryPoint>
```

In Lua:

```lua
include("InstanceManager")
local g_InstanceManager = InstanceManager:new("Row", "Container", Controls.List)
```

Do not `include()` inside a UI callback — it reports success without importing globals in that path — and do not register two file names whose first eight characters collide; VFS matching is loose on both counts.

### Event-Type Traps

- `PlayerDoTurn` does **not** fire on turn 1 for any player, fires for humans at start of turn 2, then all players every turn after. Do not anchor one-shot setup to it; anchor to `SequenceGameInitComplete` instead.
- `CanDeclareWar`, `CityCanTrain`, etc. are `TestAll` events: every listener must return true.
- Contexts are isolation scopes: globals in one context are invisible to sibling contexts, and `Player` objects compare unequal across contexts even when identical. Use primitive ids or `LuaEvents` to cross contexts.
- A runtime error in one handler aborts the rest of **that chunk**; it does not crash the game. Silent partial behaviour is the normal Lua symptom.

### Frequently Consulted Objects

| Object | Typical members | Notes |
|--------|----------------|-------|
| `Players[i]` | `GetCivilizationType`, `IsAlive`, `GetCapitalCity`, `SetHasPolicy`, `InitUnit`, `DestroyAllUnits` | User-visible player at index `i` |
| `Game.GetGameTurn()`, `Game.GetActivePlayer()` | — | Turn 0 on first activation; active player is human |
| `Map.GetPlot(x, y)`, `Map.GetNumPlots()` | — | Grid index `x + y * width` |
| `Unit:GetX()/GetY()`, `Unit:SetXY()` | — | Plot-level navigation |
| `City:SetNumRealBuilding(id, count)` | — | Grant/remove dummy buildings |
| `GameInfoTypes["BUILDING_…"]` | — | Id lookup; nil for missing types |
| `Locale.ConvertTextKey("TXT_KEY_…")` | — | Turns a key into translated text |

Tables naming rows return `GameInfoTables` entries indexed by numeric id; `GameInfo.Civilizations()[id].Type` is the row-reading idiom, where `GameInfo["Civilizations"](id)` is the MachineTranslation-compatible older idiom.

### What Cannot Be Done in Lua

Unit and combat logic is driven by the DLL; the API exposes no general hook to replace standard AI. AI behaviour is tuned through `Trait_*` flavours (`FLAVOR_NAVAL`, `FLAVOR_PRODUCTION`, …) and `Leader_Flavors`/`Leader_MajorCivApproachBiases`, not rewritten. Terrain/plot changes that touch the 3D mesh do not redraw until reload. Audio cannot be added: only asset names already declared by the engine's sound system can be referenced.

See `references/content-definitions.md` for the tables and `references/ui-and-art.md` for the UI context lifecycle. Per-event semantics live in Modiki's `Lua Game Events` and `Lua Game Objects/*` pages, which list each object's methods and each event's argument list; read the page for the object you are calling rather than guessing a method name, because an unknown method is a runtime error and not a warning.