# Database, SQL and GameData XML

Civ6 stores all configuration in two SQLite databases, merged at startup from the base game, the enabled expansions, and every enabled mod.

| Database | File in `Cache/` | Contents |
|----------|------------------|----------|
| Gameplay | `DebugGameplay.sqlite` | `Types` and every content, modifier, requirement, and association table |
| Localisation | `DebugLocalization.sqlite` | `LocalizedText(Tag, Language, Text)` |

Never edit either file directly; they are regenerated. Delete both to force a rebuild when diagnosing stale data.

## The `Types` Registry

`Types(Type, Kind, Hash)` is the root of everything. `Type` is the string key used across all tables, `Kind` is a `KIND_*` discriminator (`KIND_BUILDING`, `KIND_UNIT`, `KIND_TRAIT`, …), and `Hash` is derived from the key by the engine. `Kinds` is the companion table listing the valid kinds; the engine hardcodes what each one means, so a new `Kind` cannot be invented in data.

```sql
INSERT INTO Types (Type, Kind) VALUES ('BUILDING_MYMOD_LIBRARY', 'KIND_BUILDING');
```

Rules that save hours:
- Let the engine compute `Hash`; insert `Type` and `Kind` only.
- `Kind` must match the table the row lives in, and some tables are additionally gated by `Tags`/`TypeTags`.
- A game-visible object with no `Types` row is invisible; a `Types` row whose content row is missing usually appears in the UI with placeholder text.
- Do not reuse a vanilla key to override it. `UPDATE` the vanilla row instead.

## SQL versus GameData XML

Both are accepted by `UpdateDatabase` and are equivalent: XML elements are a mapping onto the same statements. XML is easier to diff against vanilla; SQL is easier for bulk changes and joins.

```xml
<GameData>
  <Types><Row Type="BUILDING_MYMOD_LIBRARY" Kind="KIND_BUILDING"/></Types>
  <Buildings>
    <Row BuildingType="BUILDING_MYMOD_LIBRARY" Name="LOC_BUILDING_MYMOD_LIBRARY_NAME"
         Cost="120" PrereqTech="TECH_WRITING" MaxPlayerInstances="1" InternalOnly="false"/>
  </Buildings>
</GameData>
```

```sql
INSERT INTO Buildings (BuildingType, Name, Cost, PrereqTech, MaxPlayerInstances, InternalOnly)
VALUES ('BUILDING_MYMOD_LIBRARY', 'LOC_BUILDING_MYMOD_LIBRARY_NAME', 120, 'TECH_WRITING', 1, 0);
```

| Intent | GameData XML | SQL |
|--------|--------------|-----|
| Add a row | `<Row Column="..."/>` | `INSERT INTO` |
| Change specific columns | `<Update><Where .../><Set .../></Update>` | `UPDATE ... WHERE` |
| Replace the whole row | `<Replace .../>` | `INSERT OR REPLACE INTO` |
| Remove a row | `<Delete .../>` | `DELETE FROM` |

```xml
<GameData>
  <Buildings>
    <Update>
      <Where BuildingType="BUILDING_MONUMENT"/>
      <Set Cost="40"/>
    </Update>
    <Delete BuildingType="BUILDING_MYMOD_LIBRARY"/>
  </Buildings>
</GameData>
```

Semantics to hold onto:
- A failed statement aborts that statement, not the file and not the game. Everything after it still applies, so a mod can load "mostly".
- `INSERT` of an existing key fails; use `UPDATE` or `INSERT OR REPLACE`.
- `UPDATE` matching no row succeeds silently. Verify with a `SELECT` afterwards.
- Load order decides which mod's `INSERT OR REPLACE` survives; see `mod-packaging.md`.
- SQL is executed in file order, so `CREATE TABLE` and `ALTER TABLE` before the statements that need them.

## Schema and Column Discovery

Do not guess a column list. Either read the vanilla table definition under `Base/Assets/Gameplay/Data/` / `DLC/Expansion2/Assets/Gameplay/Data/`, or query the snapshot:

```bash
sqlite3 "Cache/DebugGameplay.sqlite" "PRAGMA table_info(Units);"
sqlite3 "Cache/DebugGameplay.sqlite" "SELECT sql FROM sqlite_master WHERE name='Buildings';"
sqlite3 "Cache/DebugGameplay.sqlite" "SELECT * FROM Types WHERE Type LIKE 'UNIT_MYMOD%';"
```

```sql
-- Is my object registered and fully defined?
SELECT t.Type, t.Kind, b.Cost, b.PrereqTech
FROM Types t LEFT JOIN Buildings b ON b.BuildingType = t.Type
WHERE t.Type LIKE '%MYMOD%';

-- Which table references a missing key?
SELECT * FROM Building_ValidTerrains
WHERE BuildingType NOT IN (SELECT Type FROM Types);

-- What did another mod do to a row I also touch?
SELECT * FROM Buildings WHERE BuildingType = 'BUILDING_MONUMENT';
```

Useful inspection tooling: the `sqlite3` shell, DB Browser for SQLite, or the Steam guide's SQLite Browser workflow (open the cache file, browse structure, browse data, execute ad-hoc SQL). Reopen the file after each reload; the old handle points at the previous snapshot.

## Expansion Columns and Tables

Gathering Storm and Rise and Fall add suffix tables and extra columns:
- `_XP1` and `_XP2` suffixed tables exist only in that ruleset.
- The base-game column set is a subset; a base-game launch ignores expansion-only rows but rejects statements naming an expansion-only column.

Therefore: gate `UpdateDatabase` actions on a criteria (see `mod-packaging.md`) or maintain one data file per ruleset.

## Custom Tables

`CREATE TABLE` is available and is the supported way to keep a mod's own bookkeeping in SQLite. Keep them prefixed, keep them out of vanilla table names, and never `ALTER TABLE` a vanilla table to add a column — the engine and the UI read a fixed column set, so an added column is inert for the game and lost on patch changes.

## Ordering and Idempotence

- Write files so each statement is valid if run twice (`INSERT OR REPLACE`, or `UPDATE` after a guarded `INSERT`).
- Re-running `UpdateDatabase` happens whenever the mod list changes, so an unguarded `INSERT` in a front-end action fails on the second start.
- Prefer `DELETE` before `INSERT` for a key you fully own, so a removed vanilla row does not collide.
- Keep text in `UpdateText`. `LocalizedText` is not in the gameplay database.