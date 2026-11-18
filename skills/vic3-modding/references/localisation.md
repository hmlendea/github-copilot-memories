# Localisation, Text Formatting, and Script Localisation

Apply to files inside `localization/` (spelled with a `z`, matching vanilla) and `common/{customizable_localization,effect_localization,trigger_localization}/`.

## File Rules

- Directory: `<mod>/localization/<language>/`. The language folder name matches the internal name: `english`, `braz_por`, `french`, `german`, `polish`, `russian`, `spanish`, `japanese`, `simp_chinese`, `korean`, `turkish`.
- Filename: `<unique_prefix>_<category>_l_<language>.yml`. The suffix uses a lowercase ell (`l_`), never uppercase `I` or digit `1`.
- Encoding: **UTF-8 with BOM**. Files without a BOM are silently ignored by the engine.
- Header line: `l_<language>:` as the very first line, flush left.
- Indentation: every entry after the header must be indented with a single space.
- Format: ` key: "Text"` or ` key:0 "Text"` (the number is translation tracking metadata and can be omitted).

```yaml
l_english:
 mymod_decision_title: "Construct New Port"
 mymod_decision_desc: "Modern trade requires deeper anchorages."
```

Missing keys display as raw key strings in-game. Victoria 3 has no fallback language: provide at least the English file duplicated into each supported language directory if full localisation is unavailable.

## Overriding Vanilla Text

Vanilla localisation files are loaded in reverse alphabetical order (Z to A), so a file named `00_...` or `a_...` loads after `z_...`.

The safe, non-colliding override method is the `replace/` subfolder:

```
localization/
  english/
    replace/
      mymod_replace_l_english.yml
```

Keys declared inside `replace/` win over any previous definition regardless of filename. Do not replace the whole vanilla file.

## String Formatting and Escape Rules

- Quote escaping: embedded quotes must be `\"`.
- Invalid glyphs: typographer quotes (`“ ” ‘ ’`), ellipsis (`…`), and dashes (`— –`) render as `?`. Use ASCII `'`, `"`, and `-`.
- Line breaks: `\n`.
- Comments: `#` outside quotation marks.
- Key reuse: `$other_key$` inserts the text of `other_key`.

### Colour codes

Formatting uses `#<code` followed by a space and terminated with `#!` (no space before `#!`):

```
my_loc: "This #R text#! is red!"
```

| Code | Colour / effect |
|------|-----------------|
| `#!` | Terminate current formatting rule |
| `#r` / `#R` | Red |
| `#green` | Green |
| `#light_green` | Light green |
| `#blue` / `#U` | Blue |
| `#white` | White |
| `#darker_white` / `#default_text` | Default body text |
| `#yellow` | Yellow |
| `#gold` / `#O` | Gold (same colour as game concepts) |
| `#black` | Black |
| `#gray` / `#lore` | Grey / lore text |
| `#b` | Bold |
| `#italic` | Italic |
| `#shadow` | Drop shadow |
| `#l` / `#L` | Underline |

Codes can be nested (each requires its own `#!`) or separated by semi-colons: `#b;#gold important text#!#!`.

### Text icons

Icons are referenced with `@<key>!`. Base icons live in `gui/texticons.gui`; mods can add custom icons to any `.gui` file inside `gui/`.

Examples: `@information!`, `@warning!`, `@money!`, `@green_checkmark!`, `@red_cross!`, `@construction!`, `@bur!`, `@aut!`, `@inf!`, `@innovation!`, `@officers!`, `@capitalists!`, `@clergymen!`, `@engineers!`, `@devout!`.

```
my_loc: "Requires @bur! 100 Bureaucracy and @money! 500 £."
```

## Data Functions and Scope Chaining

Dynamic data uses `[Function]` or `[Scope.Function]` inside square brackets. Function names use PascalCase and frequently start with `Get`.

```
my_je_reason: "The [SCOPE.sCountry('usa_nation_scope').GetName] is a country in the Americas."
ruler_event_desc: "Our ruler, [SCOPE.sCharacter('pru_leader').GetFullName], has declared a jubilee."
```

Arguments are enclosed in parentheses: single quotes for script objects (`GetGoods('iron')`, `ScriptValue('my_val')`), no quotes for nested data functions.

### Common data functions

| Function | Purpose |
|----------|---------|
| `GetName` | Tooltipped name (includes flag for countries) |
| `GetNameNoFlag` | Country name without flag icon |
| `GetAdjective` / `GetAdjectiveNoFormatting` | Country adjective |
| `GetFullName` / `GetFirstName` / `GetLastName` | Character names |
| `GetSheHe` / `GetHerHis` / `GetHerselfHimself` | Gendered pronouns |
| `GetPrimaryRoleTitle` | Character role title |
| `GetGoods('key')` | Scope to goods for further chaining |
| `ScriptValue('named_value')` | Calculate and format a named script value |
| `GetCurrentBarValue` | Progress bar value |

### Function formatting pipes

Format modifiers follow a vertical pipe `|` before the closing bracket: `[Function|modifiers]`.

| Modifier | Effect |
|----------|--------|
| `*` | Convert to K / M / B (thresholds 1 000, 1 000 000, 1 000 000 000) |
| `K` | Convert to K with two fixed decimal places |
| `=` | Add explicit `+` for positive and `-` for negative |
| `+` | Green for positive, red for negative |
| `-` | Red for positive, green for negative |
| `:` | Gold for positive, blue for negative |
| `;` | Blue for positive, gold for negative |
| `U` / `l` | Uppercase / lowercase first letter |
| `L` | Underline |
| `%` | Convert to percentage (multiply by 100, add `%`) |
| `1`-`5` | Decimal places shown (max 3 when used with `*`) |

Example: `[Country.GetGDP|*2=+]` formats GDP with K/M/B, two decimals, and sign-dependent colouring.

## Game Concepts

Concepts are defined in `common/game_concepts/` and linked via `[concept_key]`:

```
my_loc: "We lack sufficient [concept_legitimacy] to enact this law."
```

Rendered in gold (`#gold`) by default and carries an automatic tooltip explaining the mechanic.

Custom text for a concept uses the `Concept` function:

```
my_loc: "Low [Concept('concept_construction', 'State Construction Efficiency')] delays work."
```

## Custom Tooltips

Add an inline hover tooltip to arbitrary text:

```
#tooltippable;tooltip:<tooltip_loc_key> <tooltip_text>#!
#tooltippable #tooltip:<tooltip_loc_key> <tooltip_text>#!#!
```

Displays `<tooltip_text>` in yellow; hovering displays the text defined at `<tooltip_loc_key>`.

## Saved Scopes in Localisation

Save the scope in an `immediate` block or from an unbroken event chain before the text is evaluated:

```
immediate = {
    c:USA = { save_scope_as = usa_scope }
    ruler = { save_scope_as = current_ruler }
}
```

Then reference with `[SCOPE.s<Type>('name')]`:

- Countries: `[SCOPE.sCountry('usa_scope').GetName]`
- Characters: `[SCOPE.sCharacter('current_ruler').GetFullName]`
- States: `[SCOPE.sState('target_state').GetName]`
- Interest groups: `[SCOPE.sInterestGroup('army_ig').GetName]`

## Customizable Localisation

Defined in `common/customizable_localization/`:

```
ruler_residence = {
    type = country
    random_valid = no              # default no: first valid text block wins

    text = {
        trigger = { has_law = law_type:law_monarchy }
        localization_key = custom_royal_palace
    }
    text = {
        trigger = { has_law = law_type:law_presidential_republic }
        localization_key = custom_presidential_palace
    }
    text = {
        trigger = { always = no }
        fallback = yes
        localization_key = custom_palace
    }
}
```

Invoke with `[Country.GetCustom('ruler_residence')]` (local scope) or `[Localize('ruler_residence')]` (global scope).

Supported types: `Country`, `Character`, `State`, `StateRegion`, `Province`, `Building`, `BuildingType`, `Culture`, `Religion`, `Goods`, `Market`, `MarketGoods`, `InterestGroup`, `InterestGroupTrait`, `Ideology`, `Law`, `LawType`, `Institution`, `InstitutionType`, `JournalEntry`, `Party`, `PoliticalMovement`, `PowerBloc`, `Decree`, `Technology`, `War`, `DiplomaticPlay`, `DiplomaticPact`, `CombatUnit`, `Front`, `Hq`, `ShippingLane`, `Theater`.

## Script Localisation

Localises scripted effects and triggers dynamically depending on whether the actor is the root country, another country, or a third party.

Wrap the effect or trigger in `custom_description`:

```
steal_treasury_effect = {
    custom_description = {
        text = "steal_treasury_effect_loc"
        subject = this
        object = $TARGET$
        value = $AMOUNT$

        change_variable = { name = gold add = $AMOUNT$ }
        $TARGET$ = { change_variable = { name = gold subtract = $AMOUNT$ } }
    }
}
```

Link the `text` key to a definition in `common/effect_localization/` (or `common/trigger_localization/`):

```
steal_treasury_effect_loc = {
    first = STEAL_TREASURY_FIRST_POS
    first_neg = STEAL_TREASURY_FIRST_NEG
    third = STEAL_TREASURY_THIRD_POS
    third_neg = STEAL_TREASURY_THIRD_NEG
    global = STEAL_TREASURY_GLOBAL_POS
    global_neg = STEAL_TREASURY_GLOBAL_NEG
}
```

- `first`: evaluated for the player's country (`root`).
- `third`: single effect evaluated on another country.
- `global`: multiple effects evaluated on another country.
- `_neg`: used when the `value` is negative.

The referenced keys (`STEAL_TREASURY_FIRST_POS: "[ROOT.GetCountry.GetName] takes [VALUE] from [TARGET.GetName]"`) are then defined in the `.yml` localisation file.
