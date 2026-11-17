# Localisation, Data Types, Customizable Localization, Flavorization

## File Rules

| Rule | Detail |
|------|--------|
| Folder | `localization/<language>/`, e.g. `localization/english/`. The US spelling `localization` is mandatory |
| Extension | `.yml` |
| Encoding | **UTF-8 with BOM.** Without the BOM the game does not read the file correctly |
| Filename | Must contain `l_<language>`, e.g. `my_locs_l_english.yml`. The character is a lowercase L, not the digit 1 or a capital I |
| First line | Must be `l_<language>:` |
| Entry | `key: "Text"` — the text must be quoted |
| Line break | `\n`; two of them give a paragraph break. Only works in localisation, never in `.gui` |
| Whitespace | A leading space before an entry is harmless and marginally speeds loading of large files |

A mod that ships only English leaves every other language showing raw keys such as `unlocalized_strings_like_this`. Copy the files to the other language folders, changing `l_english` in both the filename and the first line, even without translating.

Individual keys may be replaced without replacing the whole file **only** if the file lives in a `replace` folder. Both `localization/replace/english` and `localization/english/replace` work, but the first takes precedence, which matters when several mods target the same key.

```
l_english:
 my_key:0 "My text"
```

The number after the colon is optional and inert — a legacy translation-team marker. Modern files omit it, though both forms parse.

## Formatting Codes

`#<code> <text>#!` — the space after the code matters. Combine with `;`, e.g. `#high;bold`. All styles are defined in `gui/preload/textformatting.gui` (and `jomini/gui/jomini/basetextformatting.gui`), which is also where a mod may add its own.

| Code | Meaning |
|------|---------|
| `#P` | Positive (green) |
| `#N` | Negative (red) |
| `#V` | White |
| `#T` | Title — bold and large |
| `#E` | Game concept — light blue |
| `#S` | Bold and italic |
| `#bold`, `#italic`, `#EMP` | Bold, italic, emphasised |
| `#weak` | Darker italic, for asides |
| `#help` | Help style — blue-grey italic |
| `#I` | Informational — green italic |
| `#warning`, `#X` | Warning — red italic |
| `#indent_newline:N` | Spaces to insert after a line break |

## Re-Using Entries

`$<other key>$` inlines another localisation entry, keeping them synchronised:

```
unlock_march_contract:0 "Unlocks the #high $special_contract_march_short$#! [feudal_contract|E]"
```

The same `$...$` notation also exposes engine-supplied values in specific contexts, optionally with formatting: `$VALUE|=+0$` displays a sign and rounds to zero decimals.

## Bracketed Expressions and Data Types

`[ ... ]` invokes a data type. Data types must be scoped, usually to a character:

```
[ROOT.Char.GetLadyLord] [ROOT.Char.GetNamePossessiveRegnal] [ROOT.Char.GetFirstNameNicknamed]
```

Generate the complete list with `dump_data_types` into `logs/data_types/`, or browse it in-game with `data_types_explorer`. Promotes return a scope (like an event target); functions return a value or perform an action. Merge the dumped files for searching with `type *.txt > ALL_DATA_TYPES.txt` on Windows.

Frequently used groups:

| Group | Examples |
|-------|----------|
| Gender-aware pronouns and roles | `GetHerHim`, `GetHerHis`, `GetHerselfHimself`, `GetLadyLord`, `GetSheHe`, `GetDaughterSon` |
| Character names | `GetFirstName`, `GetFullName`, `GetTitledFirstName`, with suffixes for `Nicknamed`, `NoTooltip`, `Possessive`, `OrMe`, `Regnal` and combinations |
| Link helpers | `[faith\|E]`, `[Concept('faith','religion')\|E]`, `[GetTrait('brave').GetName( GetNullCharacter )]`, `[GetTitleByKey('k_france').GetName]` |

Arguments follow a pipe: `|U` uppercases the first letter, `|L` lowercases it, and formatting codes may be combined (`|LV` = lowercase white, the vanilla idiom for traits).

## Number Formatting

| Code | Effect |
|------|--------|
| `0`–`9` | Rounds **down** to that many decimals, keeping trailing zeros |
| `=` | Always shows the sign and rounds to two decimals; combine, e.g. `=0` |
| `k` / `K` | Displays as thousands |
| `+` | Colours as a positive modifier (green positive, red negative, white zero) |
| `-` | Colours as a negative modifier (the inverse) |
| `%` | Multiplies by 100, appends `%`, rounds to two decimals; combine, e.g. `%0` |

## Customizable Localization

`common/customizable_localization/*.txt`. Each entry declares a `type` (one of `artifact`, `character`, `landed_title`, `province`, `activity`, `secret`, `scheme`, `combat`, `combat_side`, `title_and_vassal_change`, `faith`, `dynasty`) and one or more `text` blocks:

```
MyCustomLocalization = {
	type = character
	random_valid = yes

	text = { localization_key = my_loc_1 }

	text = {
		trigger = { my_trigger1 = no }
		localization_key = my_loc_2
	}

	text = {
		trigger = { my_trigger2 = yes }
		localization_key = my_loc_3
		fallback = yes
	}
}
```

- `random_valid = no` (default) picks the first valid text; `yes` picks randomly among valid texts each invocation.
- `fallback = yes` marks the entry used when nothing else is valid.
- The folder's `_readme.info` describes the format; the referenced `localization_key` entries must exist in a localisation file, and the referenced triggers must exist as scripted triggers.

## Flavorization

Flavorization composes grammatical strings (names, titles, orderings, articles, prefixes) from parts rather than storing each combination. Definitions are grammatical building blocks such as prefix, suffix, article and name forms, and the resulting text is assembled by script at display time. Consult the vanilla flavorization files and the grammar section for the available slots before adding a new one.

## Game Concepts

A game concept gives a term a tooltip and an encyclopedia entry:

```
### common/game_concepts/MY_game_concepts.txt
my_custom_concept = { }
```

```
### localization/english/MY_l_english.yml
l_english:
 game_concept_my_custom_concept:0 "My Name"
 game_concept_my_custom_concept_desc:0 "My Description"
```

Override a vanilla concept description by redefining `game_concept_<key>_desc` in a `replace` localisation file.

## Common Localisation Keys for Modded Objects

| Object | Required keys |
|--------|---------------|
| Trait | `trait_<key>`, `trait_<key>_desc` (overridable with `name`, `desc`, `icon` dynamic blocks) |
| Decision | `<name>`, `<name>_desc`, `<name>_tooltip`, `<name>_confirm` |
| Landed title | `<title key>`, `<title key>_adj`, optionally `<title key>_article` |
| Religion / faith | `<name>`, `<name>_adj`, `<name>_adherent`, `<name>_adherent_plural`, `<name>_desc`, plus the prayer/priest/afterlife key set |
| Holy site | `holy_site_<name>_name`, `holy_site_<name>_effect_name`, `holy_site_<name>_effects` |
| Dynasty | `dynn_<key>`; prefixes `dynnp_<key>` |
| Holding | `<holding>` and `<holding>_concept_key` |
| Music track | A localisation key named in `music.txt` |
| Men-at-arms | Unit name and description keys matching the type |
| Lifestyle, focus, perk | Name and description keys; undefinable names may fall back to the key itself |
