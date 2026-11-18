# Localisation

Civ6 keeps text in a separate database from gameplay data. `LocalizedText` rows live in `Cache/DebugLocalization.sqlite` and are shipped through `UpdateText`, never through `UpdateDatabase`.

## The Table

```sql
INSERT INTO LocalizedText (Language, Tag, Text) VALUES
  ('en_US', 'LOC_BUILDING_MYMOD_LIBRARY_NAME', 'Grand Library'),
  ('en_US', 'LOC_BUILDING_MYMOD_LIBRARY_DESCRIPTION', '+2 [ICON_Science] Science in this city.');
```

| Column | Meaning |
|--------|---------|
| `Language` | `en_US`, `de_DE`, `es_ES`, `fr_FR`, `it_IT`, `ja_JP`, `ko_KR`, `pl_PL`, `pt_BR`, `ru_RU`, `zh_Hans_CN`; the full list is the `Languages` table |
| `Tag` | The lookup key the gameplay row stores in its `Name`/`Description`/`...` column |
| `Text` | Displayed text; may carry markup |
| `Gender` | Article/gender handling for inflected languages (`Masculine`, `Feminine`, `Neuter`, or `no_article`) |
| `Plurality` | Numeral-alternate forms separated by `|`, e.g. `1|2` for a singular/plural pair |

Equivalently as `GameData` XML:

```xml
<GameData>
  <LocalizedText>
    <Row Tag="LOC_BUILDING_MYMOD_LIBRARY_NAME" Language="en_US">
      <Text>Grand Library</Text>
    </Row>
  </LocalizedText>
</GameData>
```

Both forms are accepted; use whichever matches the rest of the mod. `UpdateText` files accept `<File Priority="N">` to control intra-action order.

## Key Conventions

- Firaxis uses `LOC_<OBJECT>_<FIELD>`: `LOC_BUILDING_..._NAME`, `_DESCRIPTION`, `_EXPANSION2_DESCRIPTION`, `LOC_UNIT_..._NAME`, `LOC_TRAIT_..._NAME`.
- Suffixed variants (`_DESCRIPTION`, `_EXPANSION1_DESCRIPTION`, `_EXPANSION2_DESCRIPTION`) are looked up by the UI depending on ruleset; supply the expansion variants when your object behaves differently there.
- Prefix your own tags with the mod name if you want a guaranteed absence of collisions — any prefix other than `LOC_` also guarantees no conflict with vanilla — but then keep it consistent, because every consumer must use the exact string.
- Reusing a vanilla tag means you are overriding that vanilla text for every player with your mod enabled. That is a legitimate technique for a rename mod and a bug in a content-adding mod.

## Escaping and Markup

- A literal apostrophe inside a single-quoted SQL string is doubled: `'Catherine''s Scouts'`. Forgetting this is the most common `UpdateText` syntax error.
- In XML, escape `&` as `&amp;` and `<` as `&lt;`; apostrophes need no escaping.
- `[NEWLINE]` inserts a line break, `[ICON_Science]`/`[ICON_Faith]`/`[ICON_Gold]` insert font icons, `[COLOR_Green]...[/COLOR]` colours inline text, and `[ICON_Bullet]` makes a list bullet. Unknown tags render literally.
- `%` and brace-style placeholders only work where the UI performs formatting; do not assume substitution happens.
- Keep descriptions free of engine-only markup. The Civilopedia, the tooltip, and the loading screen each render a different subset.

## Coverage and Fallbacks

- A tag defined only for `en_US` shows as the raw tag for a player in another language.
- Vanilla text is not copied into your mod: for a translated release, ship one `UpdateText` file per language (a common layout is `Text/MyMod_en_US.sql`, `Text/MyMod_ru_RU.sql`, …) and list them all in the same action.
- Community translations are safest as separate `UpdateText` files that can be updated without touching the data files.
- Some languages need `Gender`/`Plurality` filled for correct articles and numeral agreement; wrong values read as broken grammar rather than an error.

## Diagnosing Text Problems

1. `LOC_...` shown literally → the tag has no row in the active language, or the row is in the gameplay database instead of `UpdateText`.
2. Nothing shown at all → the content row's `Name`/`Description` column is empty, or points at a tag with a typo.
3. Stale text after an edit → the localisation cache was not rebuilt; delete `Cache/` and relaunch.
4. `Database.log` error `near "s": syntax error` in a text file → unescaped apostrophe.
5. Wrong text only in one place → the UI looks up a different tag than the one the row provides (for example a `_DESCRIPTION` versus `_EXPANSION2_DESCRIPTION` variant).

```sql
-- What did the merged localisation database end up with?
SELECT Language, Tag, Text FROM LocalizedText WHERE Tag LIKE 'LOC_%MYMOD%';
```