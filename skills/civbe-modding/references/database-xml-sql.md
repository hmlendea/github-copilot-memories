# Database, XML, and SQL

CivBE's gameplay data is a SQLite database. XML is a thin front end over it, and the two are interchangeable; both are executed at load time by `UpdateDatabase`. The mechanics are identical to Civ5's, and the Civ5 skill's `database-xml-sql.md` is the fuller treatment — this file records the Beyond-Earth-specific facts and the ones that cause the most failures.

## XML Is SQL

| XML | SQL | Effect |
|-----|-----|--------|
| `<Row>` | `INSERT INTO t (...) VALUES (...)` | Fails on a primary-key conflict; does not override |
| `<Update>` | `UPDATE t SET ... WHERE ...` | Modifies an existing row |
| `<Delete>` | `DELETE FROM t WHERE ...` | Removes a row; dangerous, see below |
| `<Replace>` | Insert-or-replace | Owns the key outright |
| `<Table>` / `<Column>` | `CREATE TABLE` / `ALTER TABLE` | DDL |
| `<Where>` inside `<Update>`/`<Delete>` | the `WHERE` clause | Predicate |

```xml
<GameData>
  <!-- insert -->
  <Units>
    <Row>
      <Type>UNIT_MYMOD_SCOUT</Type>
      <Class>UNITCLASS_MYMOD_SCOUT</Class>
      <Cost>40</Cost>
      <Description>TXT_KEY_UNIT_MYMOD_SCOUT_DESC</Description>
      <PrereqTech>TECH_HABITATION</PrereqTech>
    </Row>
  </Units>

  <!-- modify a vanilla row rather than inserting over it -->
  <Units>
    <Update>
      <Where Type="UNIT_SOLDIER"/>
      <Set Combat="9"/>
    </Update>
  </Units>

  <!-- insert-or-replace when you intend to own the key -->
  <Units>
    <Replace>
      <Type>UNIT_MYMOD_SCOUT</Type>
      <Combat>8</Combat>
    </Replace>
  </Units>
</GameData>
```

The SQL forms are accepted in a `.sql` file listed in the same action:

```sql
INSERT INTO Units (Type, Class, Cost, Description, PrereqTech)
VALUES ('UNIT_MYMOD_SCOUT', 'UNITCLASS_MYMOD_SCOUT', 40, 'TXT_KEY_UNIT_MYMOD_SCOUT_DESC', 'TECH_HABITATION');
```

## Rules That Prevent Most Failures

1. **`INSERT` never overrides.** Re-inserting an existing `Type` fails on the primary key, is reported only in `Database.log`, and leaves the original row untouched. Use `<Update>` to change vanilla and `<Replace>` to own a key.
2. **A failed statement does not halt the file.** Statements after it still run, so a partially applied file is the normal symptom of a syntax or constraint error. Invariably read `Database.log` before concluding a design is incorrect.
3. **Order matters within a file and across files.** Class tables before object tables; `<Row>` before the `<Update>` that references it; a mod that depends on another mod's rows must load later (enable order in the Mods screen).
4. **Never gap a primary key in a UI-iterated table.** Deleting a row leaves an `ID` hole and every later row becomes invisible to the UI. Disable with `<Update>`/`<Replace>` guards instead. This applies to the technology web, the virtue/policy tables, and any table the UI enumerates by id.
5. **Respect foreign keys.** Every `Type` referenced by a column (`Class` on `Units`, `PrereqTech` on anything, `CivilizationType` on the sponsor association tables, `BuildingClassType` on free building classes) must already exist in the merged database. A missing reference fails the statement or produces a row that never appears.
6. **Do not edit schema files, and do not add columns to vanilla tables.** The engine's schema defines what the engine reads; an added column is invisible unless your own code reads it. The supported route for extra data is a mod-owned table created with `<Table>`/`<Column>` and read back with `DB.Query`.
7. **Custom tables must be created before they are written**, and their name should be prefixed to avoid colliding with another mod's table.

## Working With Vanilla Files

The shipped XML under `assets/Gameplay/XML/` is the only complete documentation of the schema. Its directory layout mirrors the content types:

```
assets/Gameplay/XML/
  Units/CivBEUnits.xml, CivBEUnitClasses.xml, ...
  Civilizations/CivBECivilizations.xml, ...
  Technologies/...        Virtues/...        Affinities/...        Quests/...
  Buildings/...           Resources/...      Improvements/...      Terrain/...
  Interface/...           Text/...           GameInfo/...
  (Rising Tide additions alongside the base files)
```

Copy the nearest analogue for the object you are creating, rename it, trim what does not apply, and retain every column the vanilla row carries unless you know its default. A missing mandatory column fails the entire file.

## Inspecting the Merged Result

Every game start merges the base data, the expansions, and all enabled mods, and writes a debug snapshot of the result under `<user data>\cache\`. Open it with any SQLite browser and query it, because:

- It is the only method of observing the final value of a row after several mods have touched it.
- It displays whether your row exists at all, which distinguishes a schema error from a UI problem.
- It displays the `ID` gaps left by a `<Delete>` and the duplicate keys that were rejected.

The exact file name has varied between Civ5 builds and has not been documented for CivBE; locate it by listing `cache/` after launching the game once with `LoggingEnabled = 1`. The cache is written at startup, so the sequence for a data change is invariably *edit → delete the cache → relaunch*; a stale snapshot is indistinguishable from a broken mod.

## Conflict Queries

Load order decides who wins a plain `INSERT`, and the last writer wins. Useful checks against the snapshot:

```sql
-- did my object survive the merge?
SELECT * FROM Units WHERE Type = 'UNIT_MYMOD_SCOUT';
SELECT * FROM Civilizations WHERE Type = 'CIVILIZATION_MYMOD';

-- is a referenced key present?
SELECT Type FROM Technologies WHERE Type = 'TECH_MYMOD_PREREQ';

-- is there an unexpected id gap (a deleted row)?
SELECT ID FROM Policies ORDER BY ID;
```

When two mods must coexist and both touch identical rows, design around `<Update>` with narrow `<Where>` predicates rather than full-row `<Replace>`, and declare `Blocks` when they genuinely cannot.
