# Lua Scripting

Civ6 scripting runs on **HavokScript**, a superset of Lua 5.1. Plain Lua 5.1 syntax works; HavokScript adds optional statically typed variables and structs (`hstructure`, `hmake`), which Firaxis uses internally and which appear in published mods as `function f(x:number)` and `local n:number = 0`. Typed syntax is optional and your editor will flag it; use it only if the surrounding code does. Lua is confined to what the modifier system cannot express — events, queries, custom UI, and engine side effects.

## The Two Contexts

| Context | Loaded by | Sees | Use it for |
|---------|-----------|------|-----------|
| Gameplay | `AddGameplayScripts` | `GameEvents`, `GameInfo`, `GlobalParameters`, `Players`, `Cities`, `Game` | State changes and event reactions that must run identically for every player |
| UI | `AddUserInterfaces` + `ImportFiles` | `Controls`, `ContextPtr`, `Events`, `LuaEvents`, `InstanceManager`, and the managers read-only | Presentation, panels, tooltips, input |

Rules that follow from the split:
- The two contexts do not share Lua globals. The usual bridge is `ExposedMembers`, a table a gameplay script populates and UI contexts read; confirm the pattern against the vanilla gameplay scripts under `<install>/Base/Assets/Gameplay/Lua/` in your build, since its behaviour is not documented in the community references. `Events`/`LuaEvents` are the alternative.
- Gameplay scripts run for every player and must therefore be deterministic and multiplayer-safe; a UI-only script must not mutate game state, because it runs on one client.
- A UI script must not assume the gameplay script ran first. Guard every lookup.
- `include("InstanceManager")`-style imports load **vanilla** support files (`InstanceManager`, `SupportFunctions`, `Civ6Common`, `TabSupport`, `PopupDialog`, `Colors`, `InputSupport`). Your own shared files are plain imported `.lua` files; give them names that cannot collide.
- `Modding.IsModActive("GUID")` tests whether another mod (including an expansion pseudo-mod) is enabled — the runtime counterpart of `.modinfo` criteria.

```lua
-- Scripts/MyMod.lua (gameplay)
ExposedMembers.MyMod = ExposedMembers.MyMod or {}
ExposedMembers.MyMod.turnsAtWar = 0

function OnPlayerTurnActivated(playerID:number, isFirstTime:boolean)
    local pPlayer = Players[playerID]
    if pPlayer == nil or not pPlayer:IsAlive() then return end
    print("MyMod: turn activated for", playerID)
end
Events.PlayerTurnActivated.Add(OnPlayerTurnActivated)
```

```lua
-- UI/MyModPanel.lua (UI)
local turns = 0
if ExposedMembers.MyMod then turns = ExposedMembers.MyMod.turnsAtWar or 0 end
```

## Events

Every event exists on `GameEvents`; a subset also exists on `Events`. The reference wiki records, per event, which namespace Firaxis actually uses, and warns that an event registered on the wrong one can fire incorrectly or not at all. Practical rule: register on the namespace the vanilla code uses for that event, and if unsure use `Events` for gameplay state and `GameEvents` for engine callbacks.

```lua
-- verified signature: (playerID, cityID, iConstructionType, unitID, bCancelled)
Events.CityProductionCompleted.Add(function(playerID:number, cityID:number, iConstructionType:number, unitID:number, bCancelled:boolean)
    local pCity = Players[playerID]:GetCities():FindID(cityID)
    if pCity == nil then return end
    print("MyMod: production completed in", pCity:GetName())
end)

-- verified signatures
Events.CityProjectCompleted.Add(function(playerID, cityID, projectID) end)
Events.UnitKilledInCombat.Add(function(killedPlayerID, killedUnitID, playerID, unitID) end)
Events.PlayerTurnActivated.Add(function(playerID, isFirstTime) end)
Events.LocalPlayerTurnBegin.Add(function() end)
```

- Signatures are positional and untyped at call time; read them from the reference page for the event, not from memory.
- Events can carry a **table** instead of positional arguments; comments in vanilla code show both forms (`-- CityProjectCompleted = { "player", "iCityID", ... }`), so match the form the handler receives.
- Removing a handler requires the exact function reference: `Events.X.Remove(fn)`.
- Handlers registered at file scope survive a save/load in Civ6, but state in local variables does not; persist anything that must outlive the session.
- Events that are documented but never fire usually mean the wrong namespace or the wrong ruleset.
- FireTuner panels under `Debug/*.ltp` are working samples of correct event usage.

## GameInfo and the Database

`GameInfo`, `GameInfo.Units`, `GameInfo.Buildings`, and the like are generated views over the gameplay database, available in both contexts.

```lua
local kUnit = GameInfo.Units["UNIT_WARRIOR"]
if kUnit then print(kUnit.Combat, kUnit.Cost, kUnit.Index) end

for row in GameInfo.Buildings() do
    if row.PrereqDistrict == "DISTRICT_CITY_CENTER" then print(row.BuildingType) end
end

-- the numeric row index is the id the engine APIs take (verified idiom)
local BUILDING_PALACE_UPGRADE:number = GameInfo.Buildings.BUILDING_X and GameInfo.Buildings.BUILDING_X.Index or -1;

-- object lookup by id (verified idioms)
local pCity  = Players[playerID]:GetCities():FindID(cityID);
local pCity2 = Cities.GetCityInPlot(cityX, cityY);
local pUnit  = Players[playerID]:GetUnits():FindID(unitID);
```

- A missing key returns `nil`; a `nil` field access raises a runtime error that aborts the rest of that handler. Guard every lookup, including `GlobalParameters.KEY` when the row may not exist in the active ruleset.
- `GameInfo.<Table>` is a keyed view; `GameInfo.<Table>()` iterates it. `.Index` on a row is the numeric id the engine takes; the string key is what the database columns store.
- Iterating a `GameInfo.*()` view every turn is expensive; cache results in a local table and invalidate on the event that changes them (era change, tech completion, building completion).
- `DB.Query` runs read-only SQL against the merged gameplay database and is the escape hatch for joins the views cannot express:

```lua
for row in DB.Query("SELECT BuildingType, Cost FROM Buildings WHERE Cost > 500") do
    print(row.BuildingType, row.Cost)
end
```

- `GlobalParameters` exposes the key/value table that data files write to; it is the standard way to pass a version or a mod option from SQL into Lua (and for one mod to read another's exposed parameters).

## Game Objects

| Object | Access | Notes |
|--------|--------|-------|
| Player | `Players[i]`, `Game.GetLocalPlayer()` | `i` from `0` to `GameDefines.MAX_MAJOR_CIVS + MAX_MINOR_CIVS`; always nil-check |
| City | `pPlayer:GetCities():FindID(cityID)`, `Cities.GetCityInPlot(x, y)` | Iterate with `for _, pCity in pCities:Members() do` |
| Unit | `pPlayer:GetUnits():FindID(unitID)` | Same `Members()` iteration |
| Plot | `Map.GetPlot(x, y)` | Coordinates are 0-based; `Map.GetPlotByIndex` for the flat index |
| District | `pCity:GetDistricts()` | `GetDistrict()` by type id |
| Buildings in a city | `pCity:GetBuildings()` | `HasBuilding`, `RemoveBuilding`; queue changes go through `pCity:GetBuildQueue():CreateBuilding(...)` |
| Game | `Game.GetEra()`, `Game.GetCurrentGameTurn()`, `Game.GetProperty` | Global state and persistence |

Always guard ids obtained from an event; a unit can die inside the same combat that fired the event.

## Persistence

`SetProperty`/`GetProperty` store data **in the save file**, are shared by every script and every mod, and accept Lua tables:

```lua
Game.SetProperty("MYMOD_STATE", { foundingTurn = Game.GetCurrentGameTurn() })
local state = Game.GetProperty("MYMOD_STATE")
```

- Always prefix keys with the mod name; the namespace is global across mods.
- The methods require `:` (implicit self), including on `Game`.
- Values set on a game object (player, city, unit, plot, district) behave the same way: saved with the game, readable by any script.
- `Modding.SaveJSON`/`LoadJSON`-style helpers and `GameConfiguration.IsSavedGame()` exist for file-backed data; prefer properties for game state and files only for caches that can be rebuilt.
- Do not store object references; store ids and re-resolve after load.

## Performance and Safety

- Per-turn loops over every city or plot add up; scope by player and cache by turn.
- `print` writes to `Lua.log` and is mirrored to FireTuner; leave useful `print`s in during development and remove or gate them before publishing.
- Wrap risky work in `pcall`/`xpcall`; an uncaught error aborts the rest of that handler, not the game.
- Never call UI functions from gameplay scripts or gameplay mutations from UI scripts.
- Test in multiplayer: scripts that mutate state per client, or that assume the human is the active player, desynchronise.
- A script loaded by two mods runs twice; prefix globals and function names.

## What Lua Cannot Do Here

- Replace combat, AI, or core rule resolution; only the exposed API surface.
- Invent new modifier effect types or requirement types.
- Change a modifier's behaviour at runtime; the database is fixed once loaded.
- Run on the main menu unless the action's context allows it.