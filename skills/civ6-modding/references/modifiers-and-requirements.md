# Modifiers and Requirements

This is the heart of Civ6 modding. Almost every gameplay effect is a **modifier**: a named instance of a modifier type, with arguments, attached to an owner (trait, building, district, policy, belief, government, unit ability, great person), optionally filtered by requirement sets on the owner and on the subject.

```
attachment table ─── Modifiers ─── ModifierArguments
                        │  ModifierType ──> DynamicModifiers(CollectionType, EffectType)
                        │  OwnerRequirementSetId ─┐
                        └─ SubjectRequirementSetId ┴─> RequirementSets ─> RequirementSetRequirements
                                                          ─> Requirements ─> RequirementArguments
```

Per the community reference: a **modifier type** is the combination of an **effect type** (what it does) and a **collection type** (which objects it ranges over), and modifier types live in `DynamicModifiers`. The **owner** is the object the modifier is attached to; the **subject** is whatever the collection type selects from that owner. Owner and subject requirement sets are tested separately.

## The Instance

```sql
-- Verified vanilla pattern: flat science in the capital, no requirement
INSERT INTO Modifiers (ModifierId, ModifierType)
VALUES ('MYMOD_CAPITAL_SCIENCE', 'MODIFIER_PLAYER_CAPITAL_CITY_ADJUST_CITY_YIELD_CHANGE');

INSERT INTO ModifierArguments (ModifierId, Name, Value) VALUES
  ('MYMOD_CAPITAL_SCIENCE', 'YieldType', 'YIELD_SCIENCE'),
  ('MYMOD_CAPITAL_SCIENCE', 'Amount',    '2');

INSERT INTO TraitModifiers (TraitType, ModifierId)
VALUES ('TRAIT_CIVILIZATION_MYMOD', 'MYMOD_CAPITAL_SCIENCE');
```

`Modifiers` columns that matter: `ModifierId`, `ModifierType`, `RunOnce`, `Permanent`, `OwnerRequirementSetId`, `SubjectRequirementSetId`. Copy the column set from a vanilla row of the same shape rather than inventing one.

`ModifierId` is your own string. Vanilla names read as `<OWNER>_<WHAT_IT_DOES>`, which is worth imitating because the merged database and `GameEffects.log` are read by name.

## Modifier Types, Effect Types, Collections

`DynamicModifiers` maps each `ModifierType` to a `CollectionType` and an `EffectType`.

| Kind | Naming | Verified examples |
|------|--------|-------------------|
| Modifier type | `MODIFIER_<COLLECTION>_<EFFECT>` | `MODIFIER_PLAYER_CAPITAL_CITY_ADJUST_CITY_YIELD_CHANGE`, `MODIFIER_PLAYER_GRANT_UNIT_IN_CAPITAL`, `MODIFIER_SINGLE_CITY_GRANT_UNIT_IN_CITY`, `MODIFIER_ALL_PLAYERS_ATTACH_MODIFIER` |
| Effect type | `EFFECT_<VERB>_<THING>` | `EFFECT_ADJUST_CITY_YIELD_CHANGE`, `EFFECT_ADJUST_PLAYER_YIELD_CHANGE`, `EFFECT_GRANT_UNIT_IN_CITY`, `EFFECT_ATTACH_MODIFIER` |
| Collection type | `COLLECTION_<OWNER>_<SUBJECT>` | `COLLECTION_PLAYER_PLOT_YIELDS` (documented); the rest follow the same shape |

Every effect type has a **class** (`PLAYERS`, `CITIES`, `UNITS`, `PLOTS`, `ANY`, …). The class is the cheapest sanity check before attaching: an effect whose class is `CITIES` does nothing when attached to a player-scoped collection, and reports nothing.

Effect families and the arguments they take:

| Family | Examples | Arguments |
|--------|----------|-----------|
| Flat yield on a scope | `EFFECT_ADJUST_CITY_YIELD_CHANGE`, `EFFECT_ADJUST_PLAYER_YIELD_CHANGE` | `YieldType`, `Amount` |
| Percentage yield modifier | `EFFECT_ADJUST_CITY_YIELD_MODIFIER`, `EFFECT_ADJUST_BUILDING_YIELD_MODIFIER`, `EFFECT_ADJUST_DISTRICT_YIELD_MODIFIER` | `YieldType`, `Amount` |
| Combat adjustment | `EFFECT_ADJUST_ATTACKER_STRENGTH_MODIFIER`, `EFFECT_ADJUST_DEFENDER_STRENGTH_MODIFIER` | `Amount` |
| Grant a unit or building | `EFFECT_GRANT_UNIT_IN_CITY`, `EFFECT_GRANT_BUILDING_IN_CITY` | `UnitType`/`BuildingType`, `Amount`, plus extras such as `AllowUniqueOverride` |
| Conditional payload | `EFFECT_ATTACH_MODIFIER` | `ModifierId` of the payload |
| Per-count scaling | `EFFECT_ADJUST_PLAYER_YIELD_MODIFIER_PER_TRIBUTARY` and siblings | effect-specific |

The full inventory — hundreds of effect types, each with its parameter list and vanilla samples — is indexed by the community wiki as `civ-6/database/EffectType.<NAME>`, and every requirement type as `RequirementType.<NAME>`. Use those pages or grep the base-game data instead of guessing: an unknown effect or argument is dropped and appears only in `GameEffects.log`.

## Requirement Sets and Requirements

```sql
INSERT INTO RequirementSets (RequirementSetId, RequirementSetType)
VALUES ('MYMOD_CITY_HAS_LIBRARY_REQSET', 'REQUIREMENTSET_TEST_ALL');

INSERT INTO RequirementSetRequirements (RequirementSetId, RequirementId)
VALUES ('MYMOD_CITY_HAS_LIBRARY_REQSET', 'MYMOD_CITY_HAS_LIBRARY');

INSERT INTO Requirements (RequirementId, RequirementType)
VALUES ('MYMOD_CITY_HAS_LIBRARY', 'REQUIREMENT_CITY_HAS_BUILDING');

INSERT INTO RequirementArguments (RequirementId, Name, Value) VALUES
  ('MYMOD_CITY_HAS_LIBRARY', 'BuildingType', 'BUILDING_LIBRARY'),
  ('MYMOD_CITY_HAS_LIBRARY', 'MustBeFunctioning', '1');
```

- `RequirementSetType` is `REQUIREMENTSET_TEST_ALL` (every requirement) or `REQUIREMENTSET_TEST_ANY` (at least one).
- `Requirements` also carries an `Inverse` column; `Inverse = 1` negates the test, which is how vanilla expresses "has no market".
- `OwnerRequirementSetId` tests the modifier's owner; `SubjectRequirementSetId` tests each object the collection yields. Putting a city requirement on the owner of a player-scoped modifier never passes — the classic no-effect bug.
- Requirement types are classed like effect types (`PLAYERS`, `CITIES`, `PLOTS`, `UNITS`); the class must match the object being tested.
- Requirements can be shared between sets; reuse vanilla `REQSET_*` and `REQUIREMENT_*` ids instead of cloning them.

Verified requirement types: `REQUIREMENT_CITY_HAS_BUILDING` (arguments `BuildingType`, `MustBeFunctioning`), `REQUIREMENT_CITY_HAS_DISTRICT`, `REQUIREMENT_PLAYER_IS_AT_WAR` (no arguments), `REQUIREMENT_PLAYER_HAS_TECHNOLOGY`, `REQUIREMENT_GAME_ERA_IS`/`_ATLEAST`/`_ATMOST` (plus `_XP1`/`_XP2` variants), `REQUIREMENT_PLOT_PROPERTY_MATCHES`, `REQUIREMENT_PLOT_UNIT_CITY_HAS_DISTRICT_SAME_OWNER`, `REQUIREMENT_TRADE_ROUTE_BETWEEN_ALLIANCE_PARTNERS`, `REQUIREMENT_PLAYER_TURN_STARTED`.

`REQUIREMENT_PLOT_PROPERTY_MATCHES` reads a **property** stored on a plot, and `EFFECT_ASSIGN_<OBJECT>_PROPERTY` / `EFFECT_ADJUST_<OBJECT>_PROPERTY` write them. That pair is how a mod records custom state which requirements can then read without any Lua.

## Attachment Tables

| Owner kind | Attachment table |
|------------|------------------|
| Civilization trait | `TraitModifiers` |
| Leader trait | `TraitModifiers` (the trait row is what differs) |
| Building | `BuildingModifiers` |
| District | `DistrictModifiers` |
| Improvement | `ImprovementModifiers` |
| Unit ability | `UnitAbilityModifiers` |
| Policy | `PolicyModifiers` |
| Belief | `BeliefModifiers` |
| Government | `GovernmentModifiers` |
| Great person | `GreatPersonIndividualActionModifiers` |
| Wonder | `BuildingModifiers` — wonders are buildings |
| Project | the project modifier tables (`ProjectCompletionModifiers` and relatives) |
| Religion, pantheon, corporation, governor, emergency | one table each, named after the owner |

Attaching to the wrong table produces no error and no effect. Confirm the table name against vanilla rows for the same kind of owner.

## Patterns Worth Reusing

**Grant a unit once, permanently, from a trait:**

```sql
INSERT INTO Modifiers (ModifierId, ModifierType, RunOnce, Permanent)
VALUES ('MYMOD_GRANT_TRADER', 'MODIFIER_PLAYER_GRANT_UNIT_IN_CAPITAL', 1, 1);
INSERT INTO ModifierArguments (ModifierId, Name, Value) VALUES
  ('MYMOD_GRANT_TRADER', 'UnitType', 'UNIT_TRADER'),
  ('MYMOD_GRANT_TRADER', 'Amount',   '1');
INSERT INTO TraitModifiers (TraitType, ModifierId)
VALUES ('TRAIT_CIVILIZATION_MYMOD', 'MYMOD_GRANT_TRADER');
```

`RunOnce` + `Permanent` is how vanilla grants one-off founder and leader bonuses that must not repeat every turn.

**Conditional payload** — a wrapper using `EFFECT_ATTACH_MODIFIER` carries the requirement set and points at a payload modifier that has none. The payload stays reusable across owners:

```sql
INSERT INTO Modifiers (ModifierId, ModifierType, OwnerRequirementSetId)
VALUES ('MYMOD_ATTACH_WAR_SCIENCE', 'MODIFIER_ALL_PLAYERS_ATTACH_MODIFIER', 'MYMOD_PLAYER_AT_WAR_REQSET');
INSERT INTO ModifierArguments (ModifierId, Name, Value)
VALUES ('MYMOD_ATTACH_WAR_SCIENCE', 'ModifierId', 'MYMOD_WAR_SCIENCE_PAYLOAD');
```

**Percentage instead of flat** — the `_MODIFIER` yield family treats `Amount` as a percentage; the `_CHANGE` family treats it as a flat value. Mixing them produces effects that are wrong rather than broken.

**Per-district / per-population yield gated on the subject** — verified in a published civ mod, which is the clearest illustration of owner versus subject:

```sql
INSERT INTO TraitModifiers (TraitType, ModifierId)
VALUES ('TRAIT_LEADER_MYMOD', 'MYMOD_CAMPUS_CULTURE');

INSERT INTO Modifiers (ModifierId, ModifierType, SubjectRequirementSetId)
VALUES ('MYMOD_CAMPUS_CULTURE',
        'MODIFIER_PLAYER_CITIES_ADJUST_CITY_YIELD_PER_DISTRICT',
        'CITY_HAS_CAMPUS_SST');

INSERT INTO ModifierArguments (ModifierId, Name, Value) VALUES
  ('MYMOD_CAMPUS_CULTURE', 'YieldType', 'YIELD_CULTURE'),
  ('MYMOD_CAMPUS_CULTURE', 'Amount',    '2');
```

Owner = the player (via the leader trait); subject = each city the collection yields. The requirement set belongs on the **subject**, because it is the city that must have the Campus. The sibling modifier type `MODIFIER_PLAYER_CITIES_ADJUST_CITY_YIELD_PER_POPULATION` takes the same shape with the same two arguments.

Overriding a vanilla modifier's value is just an `UPDATE`:

```sql
UPDATE ModifierArguments SET Value = '5'
WHERE ModifierId = 'TRAIT_X_CAMPUS_SCIENCE' AND Name = 'Amount';
```

Because `ModifierId` values are global, two mods editing the same vanilla modifier will fight; the later one in load order wins.

## Diagnosing a Modifier That Does Nothing

1. `GameEffects.log` — unknown `ModifierType`, unknown `EffectType`, missing argument, unresolved requirement.
2. Cache snapshot — is the `Modifiers` row present, and does the attachment row exist?
3. Argument names are case-sensitive. `amount` instead of `Amount` is silently ignored.
4. Class mismatch — effect class against collection and requirement class.
5. Scope — does the collection type actually range over the object the requirement tests?
6. Attachment — is the owner present in play (trait granted, building built, policy slotted)?
7. Repetition — a `RunOnce` modifier fires once per game, not once per turn.
8. Vanilla requirement reuse — a `REQSET_*` you picked may already include conditions you did not expect.

## Things the System Cannot Do

- Compare two arbitrary values (two yields against each other, unit count versus era) unless a requirement type exists for it.
- React to an event. That is `GameEvents` in Lua (`lua-scripting.md`).
- Change a rule inside combat resolution or AI decision making; only the exposed adjustment effects exist.
- Persist data, except through object properties that both requirements and effects can read.