# Database Modding with XML and SQL

Civ5 gameplay data is a SQLite database. XML files under `Assets/Gameplay/XML/` and `Assets/DLC/Expansion*/Gameplay/XML/` are translated into SQL statements at startup; `GameData` is the root element and each child names a table.

## XML Element Semantics

| Element | SQL | Notes |
|---------|-----|-------|
| `<Row>` | `INSERT` | Fails on primary-key or unique collision; the whole file is then abandoned from that statement on |
| `<Update><Where …/><Set …/></Update>` | `UPDATE … WHERE …` | Attributes or nested elements; both forms accepted |
| `<Delete …/>` | `DELETE … WHERE …` | **Dangerous**: id gaps break UI iteration |
| `<Replace>` | `INSERT OR REPLACE` | Replaces a whole row by key; missing columns take defaults |
| `<Table Name="…"><Column …/></Table>` | `CREATE TABLE` | Creates a new table, visible to SQL and `DB.Query` only |
| `<Column>` inside a table | `ALTER TABLE … ADD COLUMN` | SQL form is more readable and is what most mods use |
| `<Truncate/>` | (extension) | Empties a table; almost never what you want |

```xml
<GameData>
  <Buildings>
    <Row>
      <Type>BUILDING_MY_LIBRARY</Type>
      <BuildingClass>BUILDINGCLASS_MY_LIBRARY</BuildingClass>
      <Cost>75</Cost>
      <PrereqTech>TECH_WRITING</PrereqTech>
      <Description>TXT_KEY_BUILDING_MY_LIBRARY</Description>
    </Row>
    <Update>
      <Where Type="BUILDING_LIBRARY"/>
      <Set Cost="70"/>
    </Update>
  </Buildings>
</GameData>
```

Rules that bite:
- **Column order is irrelevant; column names must be exact.** A misspelled column aborts the file with an `XML.log` error naming the column.
- **Booleans are integers in SQL** (`1`/`0`). In XML, `true`/`false` and `1`/`0` are both accepted by the loader, but SQL files must use numbers.
- **Foreign keys are enforced.** Every `XxxType` value must exist in the referenced table *by the time this statement runs*. Order statements parent-first; a missing reference aborts the remainder of the file.
- **Ids are auto-assigned.** Do not write `ID` values. Coding against ids in Lua is a bug waiting for another mod to insert rows; use `GameInfoTypes["BUILDING_…"]` instead.
- **One statement per element.** Do not try to update two rows with one attribute set.

## SQL Files

SQL files give what XML cannot: `ALTER TABLE`, multi-row operations, computed updates, and joins.

```sql
-- new columns for your own feature
ALTER TABLE Buildings ADD COLUMN 'MyFeatureValue' INTEGER DEFAULT 0;
UPDATE Buildings SET MyFeatureValue = 3 WHERE Type = 'BUILDING_TEMPLE';

-- redistribute vanilla values
UPDATE Units SET Cost = Cost * 1.1 WHERE Class = 'UNITCLASS_MELEE';

-- own table, written and read from Lua through DB.Query
CREATE TABLE IF NOT EXISTS MyState (id INTEGER PRIMARY KEY AUTOINCREMENT, Key TEXT UNIQUE, Value TEXT);
```

- `ALTER TABLE … ADD COLUMN` on a **vanilla** table succeeds in SQLite and the column is present in the snapshot, but the engine's C++ code does not know it. Only your own Lua/SQL can use it. This is how large overhaul mods add their own hooks, and how vanilla-plus projects keep compatibility.
- `INSERT OR REPLACE` is the idiomatic idempotent upsert; `UPDATE` is the safe way to touch vanilla rows.
- Comments are `--` and `/* */`.
- Multi-statement files are executed statement by statement; the first failure stops the rest of the file. Split risky statements into separate small files so one failure does not hide the others.

## Ordering

Actions execute in the order they are listed in `OnModActivated`, then the next mod's, in mod load order. Practical order:
1. `CREATE TABLE` / `ALTER TABLE` statements.
2. New `*Class` rows.
3. New `Type` rows.
4. Association tables (`Building_YieldChanges`, `Unit_FreePromotions`, `Policy_PrereqPolicies`, …).
5. `Language_*` text.
6. `IconTextureAtlases` / `IconFontMapping`.
7. `UPDATE` adjustments to vanilla rows.

Text does not technically need to precede anything, but keeping it last makes failed-file debugging obvious: a file that runs but shows raw `TXT_KEY_…` is a missing text row, not a broken insert.

## Deletion

`DELETE` is the most common way to break a mod, because:
- Many UI panels iterate `ID` from 1 upward and stop at the first gap. Deleting one `Policies` row makes every later policy invisible.
- Other mods may hold references to the deleted row, and their inserts then fail.
- Saves may reference the id.

Prefer:
- `<Update>` the row to a harmless state (cost 9999, `PolicyBranchType` cleared, `PrereqTech` moved) so it never appears in normal play.
- `<Replace>` with a fully specified blocked row when a row must genuinely be neutralised.
- Only delete when nothing references the row and no other mod plausibly will — typically a row your own mod added in the same load.

## Schema and Foreign Keys

Every table's columns, types, defaults, and the table each `*Type` references are documented per table on Modiki and, authoritatively, in `Assets/Gameplay/XML/Schema/Civ5*.xml`. The element order in the schema is not the column order and does not matter for `<Row>`.

Schema files are engine input. Editing them without a matching DLL change is either a crash or a silent no-op; treat them as documentation.

## Database Access from Lua

```lua
-- read-only queries return a table of tables
for row in DB.Query("SELECT Type, Cost FROM Buildings WHERE Cost > 500") do
  print(row.Type, row.Cost)
end

-- use a query string built from primitives you control, never from user text
DB.Query("CREATE TABLE IF NOT EXISTS MyMod_Flags (Key TEXT UNIQUE, Value INTEGER);")
DB.Query(string.format("INSERT OR REPLACE INTO MyMod_Flags (Key, Value) VALUES ('%s', %d);", key, value))
```

`DB.Query` runs against the live database, including in-game. Reading is cheap enough for occasional use; writing per turn is not. Batch writes into one statement with several `VALUES` rows.

Two durable-storage options exist and they differ:

| Mechanism | Scope | Cost | Use for |
|-----------|-------|------|---------|
| `Modding.OpenSaveData()` | Embedded in the save; **shared by all mods** | One query per get/set | Small per-save state, keyed with your mod prefix |
| `Modding.OpenUserData(name, version)` | `ModUserData/<name>.db`; survives across saves | One query per get/set | Mod settings, cross-game unlocks |
| `Player/Plot/Unit:SetScriptData` | In the save | Cheap | Last resort; **shared namespace**, conflicts across mods |
| Own table via `DB.Query` | Live database, saved with the game | Cheap when batched | Larger structured state |

Always prefix keys (`MYMOD_`) for the shared stores.

## Verification

After the first launch following a change, query the snapshot instead of guessing:

```bash
sqlite3 "$HOME/Documents/My Games/Sid Meier's Civilization 5/cache/Civ5DebugDatabase.db" \
  "SELECT Type, Cost FROM Buildings WHERE Type LIKE 'BUILDING_MY_%';"
```

If the row is absent, the file failed; `Logs/Database.log` names the statement and the constraint.