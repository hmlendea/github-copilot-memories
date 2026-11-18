# Localisation and Text Markup

CivBE stores all strings as `Language_*` tables keyed by `Tag`, exactly as Civ5 does. The Civ5 skill's `localisation.md` covers the table shape, the language list, the markup vocabulary, and the key conventions in full; this file records the Beyond-Earth variant the sponsor tutorial uses and the behaviours specific to it.

## The Table

Two equivalent forms are accepted, and both travel through the `UpdateDatabase` action.

```xml
<GameData>
  <Language_en_US>
    <Row Tag="TXT_KEY_CIV_MYMOD_DESC"><Text>Shang Mu</Text></Row>
    <Row Tag="TXT_KEY_CIV_MYMOD_SHORT_DESC"><Text>Shang Mu</Text></Row>
    <Row Tag="TXT_KEY_CIV_MYMOD_ADJECTIVE"><Text>Shang Mu</Text></Row>
  </Language_en_US>
</GameData>
```

```xml
<GameData>
  <LocalizedText>
    <Row Language="en_US" Tag="TXT_KEY_CIV_MYMOD_DESC"><Text>Shang Mu</Text></Row>
  </LocalizedText>
</GameData>
```

Both styles appear in published Beyond Earth mods. The `Language_*` table derives the language from the table name; the `LocalizedText` form states it in a `Language` attribute. Use whichever matches the rest of the mod, and be consistent.

## Language Attribute Behaviour

The tutorial `Custom Sponsor Tutorial` spells out what the attribute means in practice: the game looks up the tag for the active language and falls back to another language's row for the identical tag when the active language's row is absent. Authoring two rows with the identical tag and different languages is therefore a legitimate method of overriding the display per region:

```xml
<Row Language="en_US" Tag="TXT_KEY_SOMETHING"><Text>English text</Text></Row>
<Row Language="es_ES" Tag="TXT_KEY_SOMETHING"><Text>Texto en español</Text></Row>
```

English (`en_US`) is the only language you must ship, since it is the fallback. A key with no row in any language renders as the raw tag.

## The `%` Substitution

A `%` inside a tag value is substituted with an index. The game appends `0`, `1`, and so on and looks up the resulting tag, so `TXT_KEY_CIV_INTRO_MYMOD_TEXT_%` resolves to `..._0`, then `..._1`. This is how vanilla sponsors carry several greetings or load-screen texts for the same event, and it is the mechanism the sponsor tutorial uses for the introduction quote.

```xml
<Row Language="en_US" Tag="TXT_KEY_CIV_INTRO_MYMOD_TEXT_0"><Text>...text...[NEWLINE][NEWLINE]</Text></Row>
<Row Language="en_US" Tag="TXT_KEY_CIV_INTRO_MYMOD_TEXT_1"><Text>...alternate text...</Text></Row>
```

## Key Conventions

- `TXT_KEY_` prefix is required by the loader for a value used as a key; the loader warns when a `Description`/`Help` value does not start with `TXT_KEY_`.
- Per-object suffixes observed in Beyond Earth: `_DESC`, `_SHORT_DESC`, `_ADJECTIVE`, `_HELP`, `_STRATEGY`, `_TEXT` (Civilopedia), `_QUOTE`, `_PEDIA`.
- Sponsor keys follow the vanilla shape (`TXT_KEY_CIV_<NAME>_DESC`, `TXT_KEY_CIV_<NAME>_SHORT_DESC`, `TXT_KEY_CIV_<NAME>_ADJECTIVE`, `TXT_KEY_CIV_INTRO_<NAME>_TEXT_%`), and city and spy names follow `TXT_KEY_CITY_NAME_<NAME>_<N>` and `TXT_KEY_SPY_NAME_<NAME>_<N>`.
- Unit keys follow `TXT_KEY_UNIT_<NAME>_DESC`, `_PEDIA`, `_HELP`, as the unit tutorial demonstrates.

## Markup

The markup vocabulary is the Civ5 one: `[NEWLINE]`, `[COLOR_*]...[ENDCOLOR]`, `[ICON_*]` for yield and resource icons, and the font-icon shorthands the `Reference - Font Icons` thread lists. A misspelled `[ICON_*]` or `[COLOR_*]` name renders literally rather than failing, so check the result in game rather than in the file.

## Why Text Goes Missing

Text shows as a raw `TXT_KEY_...` string, or an object shows no name, when:

- the row is absent, misspelled, or in a file whose earlier statement failed;
- the key in the data row and the key in the text row differ by one character;
- the language table name is wrong (`Language_en_US` and not, say, `Language_en_gb`);
- the file was never wired to an action.

All of these are diagnosed in the identical manner: search `Database.log` for the tag and check the snapshot for the merged row.
