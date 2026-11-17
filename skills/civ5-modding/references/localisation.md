# Localisation and Text Markup

Civ5 stores all strings as `Language_*` tables keyed by `Tag`:

```xml
<GameData>
  <Language_en_US>
    <Row Tag="TXT_KEY_BUILDING_MYMOD_LIBRARY">
      <Text>Library</Text>
    </Row>
    <Row Tag="TXT_KEY_BUILDING_MYMOD_LIBRARY_HELP">
      <Text>+1 [ICON_RESEARCH] Science per [ICON_CITIZEN] Citizen.</Text>
    </Row>
  </Language_en_US>
</GameData>
```

| Language table | Locale |
|----------------|--------|
| `Language_en_US` | English (the only one you must ship) |
| `Language_fr_FR`, `Language_de_DE`, `Language_es_ES`, `Language_it_IT`, `Language_ja_JP`, `Language_ko_KR`, `Language_pl_PL`, `Language_ru_RU`, `Language_zh_Hans_CN`, `Language_pt_BR` | shipped localisations |

Everything unresolved shown to a player is a missing tag: `TXT_KEY_…` text on screen means the row is absent, misspelled, or in a file that aborted.

## Key Conventions

- `TXT_KEY_` prefix is required by the loader for text used as a key; the loader warns when a `Description`/`Help` value does not start with `TXT_KEY_`.
- Per-object suffixes used by vanilla: `_DESC`, `_SHORT_DESC`, `_ADJECTIVE`, `_HELP`, `_STRATEGY`, `_TEXT` (Civilopedia), `_QUOTE`, `_PEDIA`.
- Name pattern: `TXT_KEY_<TABLE>_<TYPE>` for the display name and `TXT_KEY_<TABLE>_<TYPE>_TEXT` for Civilopedia prose, mirrors how `<Description>` vs `<Civilopedia>` rows are consumed.
- Civilization keys conventionally follow vanilla (`TXT_KEY_CIV_<NAME>_DESC`, `TXT_KEY_CIV_<NAME>_SHORT_DESC`, `TXT_KEY_CIV_<NAME>_ADJECTIVE`, `TXT_KEY_CIV5_<NAME>_TEXT`, `TXT_KEY_CIV5_DAWN_<NAME>_TEXT`).
- Never reuse a vanilla tag for different text unless a `Language_*` `<Update>` or `<Replace>` is intended; a duplicate `Tag` insert fails the file.

## Text Markup

| Markup | Effect |
|--------|--------|
| `[NEWLINE]`, `[TAB]`, `[SPACE]` | whitespace |
| `[COLOR_X]…[ENDCOLOR]` | colour span; `COLOR_POSITIVE_TEXT`, `COLOR_NEGATIVE_TEXT`, `COLOR_YIELD_GOLD`, `COLOR_PLAYER_ORANGE`, `COLOR_CYAN`, plain colour names |
| `[ICON_…]` | 22×22 icon from `IconFontMapping`; e.g. `[ICON_GOLD]`, `[ICON_FOOD]`, `[ICON_RESEARCH]`, `[ICON_CULTURE]`, `[ICON_HAPPINESS_4]`, `[ICON_CITIZEN]`, `[ICON_BULLET]`, `[ICON_PIRATE]` |
| `[LINK=TYPE]text[/LINK]` | Civilopedia hyperlink, e.g. `[LINK=IMPROVEMENT_TRADING_POST]` |
| `{1_…}`, `{2_…}` | argument substitution |
| `{1_Key[2]}` | pick form 2 from a multi-form row |
| `{1 ^ 'feminine:trait'}` | pick the form whose gender trait matches |
| `{1:plural 1?one; other?many;}` | plural selection |
| `{1:upper}`, `:lower`, `:title`, `:percent`, `:number`, `:roman`, `:spellout`, `:textkey` | transforms (several were never finished in the shipped build; verify before relying on them) |

Markup works in XML text and in Lua strings alike, including `Teaser` and `Description` in `.modinfo`.

## Gendered and Plural Strings

A row can hold several forms:

```xml
<Row Tag="TXT_KEY_SAMPLE">
  <Text>Form 1|Form 2|Form 3|Form 4</Text>
  <Gender>neuter:trait_one|masculine:trait_two|feminine:trait_three|mixed:trait_four</Gender>
  <Plurality>1|1|1|2</Plurality>
</Row>
```

`neuter`, `masculine`, `feminine`, and `mixed` are the only hard-coded genders; the part after `:` is a free-form trait you match against. Selecting a form, gender, or plural requires the argument (`{1}`) to carry meta-information. `{1_Num}` does not, so `{1_Num} {1:plural 1?turn; other?turns;}` always yields "turn" and silently ignores the plural branch. When the string needs pluralisation, pass the number through a keyed row that declares `<Plurality>`, not through a raw number argument.

Practical limitation: a transform cannot be combined with a form/gender/plural selector — transforms apply to the first form, always.

## Missing-Language Behaviour

A mod that ships only English shows `TXT_KEY_…` in every other language for any new key the vanilla files do not provide. Two acceptable strategies:
1. Copy the `Language_*` block into other language tables with the English text as a fallback.
2. Ship English only and accept raw keys in non-English locales; state it in the mod description.

## Debugging Text

- A raw `TXT_KEY_…` on screen: the tag is missing, or its file aborted. Check `Logs/Database.log` for `does not start with 'TXT_KEY_'` and foreign-key errors.
- Wrong icon: the `[ICON_…]` name is not in `CIV5IconFontMapping`; the failure is silent, leaving literal text.
- Wrapped or clipped labels: `[NEWLINE]` inside a single-line control, or markup inside an attribute that is not a text control.
- A Civilopedia link goes nowhere: `[LINK=…]` must name a `Type` that exists in the `Concepts`/Civilopedia table.