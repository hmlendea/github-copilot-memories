# Localisation

## File Rules

- Location: `localization/` in the mod root (Imperator spells it with `z`, unlike some other Paradox titles).
- Naming: `<file>_l_<language>.yml`. Any file not matching this pattern is ignored entirely.
- Languages: `english`, `french`, `german`, `russian`, `spanish`, `simp_chinese`.
- Encoding: **UTF-8 with BOM**. A plain UTF-8 file may load but the game warns; BOM is the supported form. Copying an existing vanilla `.yml` then editing is the reliable way to get it right.
- First line must declare the language: `l_english:`.
- Optional language subfolders are allowed for organisation.
- Overrides: put the file in `localization/replace/` so it loads after all other localisation files and wins on duplicate keys.

```
l_english:
 wonder_lighthouse_of_pharos:0 "Lighthouse of Alexandria"
 wonder_giza:0 "Giza Pyramid Complex"
```

The number after the key is Paradox's internal translation tracker and may be omitted.

Never replace whole vanilla localisation files to add entries — add a new file containing only your keys.

## Quoting and Characters

- Every value is wrapped in double quotes.
- A literal quote inside a value is escaped: `text \"name\"`.
- These characters are **invalid** inside localisation and render as `?`: curly quotes `„ “ ‚ ‘ – ” ’ … —`. Use ASCII equivalents.

## Colour Codes

`#<code> ` (letter plus a space) starts a colour; `#!` restores the default. Definitions live in `jomini/gui/jomini/basetextformatting.txt`.

| Code | Effect | Alias |
|------|--------|-------|
| `#Y` | Blue | `zero_value`, `Z` |
| `#G` | Green | `positive_value`, `P` |
| `#R` | Red | `negative_value`, `N` |
| `#I` | Italics | `instruction` |
| `#T` | Bold (also gold in some contexts) | `bold` |
| `#X` | Bold red italic (warning) | `warning` |
| `#D` | Pink (debug) | `debug` |
| `#TF` | Light grey | — |
| `#!` | Default | — |

## Hoverable Links (Get Commands)

Wrap GoTo/Get commands in square brackets to render a clickable, tooltip-bearing reference. Commands either take a definition as an argument or chain as `.Get*` from the current scope.

| Command | Meaning | Example |
|---------|---------|---------|
| `GetName` | Name of the current scope | `[ROOT.GetCountry.GetName]` |
| `GetProvince` | Province from an id | `GetProvince('(int32)362')` |
| `GetCountry` | Country from a tag | `GetCountry('MAC')` |
| `GetCharacter` | Character from an id | `GetCharacter('(int32)32')` |
| `GetRuler` | Ruler of the current country | `ROOT.GetCountry.GetRuler` |

Most chains must end in `.GetName` to render. Tooltips inside localisation are preferred over tooltips in `.gui` files because localisation supports `\n`.

## Text Icons

`@<icon_name>!` inserts an inline icon. Icon definitions live in `gui/shared/font_icons.gui` and can be added in `gui/shared/`:

```
texticon = {
    icon = icon_name
    iconsize = {
        texture = "gfx/interface/icons/font_icons/icon_name.dds"
        size = { 16 16 }
        offset = { 0 4 }
        fontsize = 16
    }
}
```

Common existing icons:

- Stats: `@military_icon!` (Martial), `@civic_icon!` (Finesse), `@oratory_icon!` (Charisma), `@religious_icon!` (Zeal).
- Parties: `@traditionalist_party!`, `@democratic_party!`, `@oligarchic_party!`, `@optimates_party!`, `@boni_party!`, `@populares_party!`.
- Land units: `@archers!`, `@camels!`, `@chariots!`, `@heavy_cavalry!`, `@heavy_infantry!`, `@horse_archers!`, `@light_cavalry!`, `@light_infantry!`, `@warelephant!`, `@supply_train!`, `@engineer_cohort!`.
- Ships: `@liburnian!`, `@trireme!`, `@tetrere!`, `@hexere!`, `@octere!`, `@mega_galley!`.

## Naming Conventions for Keys

Vanilla uses dotted suffixes: `.t` (title), `.desc` (description), `.a`/`.b`/`.c` (option names), plus `_tooltip` and `_title` where an event or decision reuses a shared string. Keeping the convention makes cross-referencing event IDs and keys mechanical.

## Checklist

- [ ] File name ends `_l_<language>.yml`.
- [ ] First line `l_<language>:`.
- [ ] UTF-8-BOM encoding.
- [ ] Every key used by script exists in every shipped language.
- [ ] No invalid Unicode punctuation.
- [ ] No vanilla file replaced to add keys; `localization/replace/` only for overrides.