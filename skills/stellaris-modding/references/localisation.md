# Localisation and Text Formatting

## File Rules

- Folder name is `localisation` (British spelling), not `localization`.
- Filename must end in `_l_<language>.yml`, e.g. `my_mod_l_english.yml`.
- Encoding must be **UTF-8 with BOM**. Plain UTF-8 fails to parse.
- First line must be `l_<language>:`.
- Every entry after the header line must be indented with whitespace.
- Missing keys display as the raw key in-game; there is no fallback language, so duplicate the English file for every other language you ship.

Languages: `english`, `french`, `german`, `spanish`, `polish`, `russian`, `braz_por`, `simp_chinese`, `japanese`, `korean`.

```
l_english:
 my_mod.1.name: "A Signal"
 my_mod.1.desc: "Something answers."
 my_mod.1.a: "Investigate"
```

## Key Syntax

- `key: "string"` — the number vanilla sometimes shows after the colon is translation-tracking metadata and can be omitted.
- Escape embedded quotes as `\"`.
- These characters are invalid and render as `?`: `„ “ ‚ ‘ – ” ’ … —`. Use ASCII apostrophes and hyphens, or the game's own dash glyph.
- Newlines inside a string use `\n`.

## Overriding Vanilla Text

Create `localisation/replace/`. Files there load after every other localisation file (LIOS), so individual keys override without redefining the whole file.

Duplicating a vanilla filename also overrides it, but is fragile and should be reserved for near-total replacement.

## Bracket Commands

`[Scope.Command]` — scope chain, dot-separated, ending in a retrieval.

```
[Root.GetName] joined [From.GetName].
Total: [This.Owner.GetName] — [Root.Capital.GetName]
```

Primary scopes: `Root`, `This`, `From`, `Prev`, `event target tags` (bare, without `event_target:`), and diplomatic promotions `Actor`, `Recipient`, `Third_party`.

Secondary scopes: `Capital`, `Leader`, `Ruler`, `Heir`, `Species`, `Federation`, `Owner`, `System`, `Planet`, `MoonOf`, `Sector`, `MainAttacker`, `MainDefender`.

Retrievals most used: `GetName`, `GetNamePlural`, `GetRealName`, `GetAdj`, `GetAdjective`, `GetSpeciesName`, `GetSpeciesAdj`, `GetSpeciesClass`, `GetClassName`, `GetPlanetClass`, `GetOwnerName`, `GetControllerName`, `GetRulerName`, `GetRulerTitle`, `GetHeirName`, `GetLeaderName`, `GetHomeWorldName`, `GetStarName`, `GetAllianceName`, `GetFleetName`, `GetAge`, `GetAAnPlanetClass`, `GetHasHave`, `GetIsAre`, `GetSheHe`, `GetHerHis`, `GetWasWere`, plus gendered and empire-type-aware occupational forms (`GetScientist`, `GetEngineer`, `GetResearchers`, `GetTerraformer`, `GetLinguists` and their `Plural` variants).

Escape a literal bracket by doubling it: `[[example]` renders `[example]`.

In scripted effects and triggers, prefixed brackets must be escaped as `\\[This.GetName]`, otherwise the failure appears on the second use.

Variables and saved dates are also retrievable: `[Scope.my_variable]`, `[Scope.my_date_flag]`.

`script_documentation/localizations.log` holds the complete list for the installed build.

## `$` Codes

```
@my_value = 5
"Upkeep by +$@my_value$"
```

`$...$` interpolates a localisation key or a `@` variable. Number formatting uses a pipe: `$VALUE|*2$` renders two decimals; `$VALUE|0$` rounds to integer.

Colour inside an interpolation: `$AGE|Y$`.

## Colour Codes

`§<char>` changes colour until the next `§` code or `§!` (reset).

| Code | Colour | Typical use |
|------|--------|-------------|
| `W` | White | Neutral emphasis |
| `T` | Light grey | Default body text |
| `g` | Dark grey | Disabled |
| `L` | Brown | Lore |
| `P` | Dirty pink | Aggressive text |
| `R` | Red | Negative |
| `S` | Dark orange | Subtle highlight |
| `H`, `K` | Orange | Highlight |
| `Y`, `I` | Yellow | Neutral or suboptimal |
| `G` | Green | Positive |
| `V` | Dark green | Event body text |
| `E` | Teal | Long text blocks |
| `C` | Cyan | Concept links |
| `B` | Cyan-blue | Pop effects |
| `M` | Purple | Rare technology |
| `_` | Magenta | Placeholders |
| `c` | Blue-green | Leader trait |
| `v` | Faded green | Veteran trait |
| `d` | Tan | Destiny trait |
| `r` | Light purple | Renowned |
| `l` | Light green | Legendary |
| `!` | — | Reset to previous colour |

Definitions live in `interface/fonts.gfx`. On Windows the `§` character is `Alt+0167`.

## `£` Icon Codes

`£energy£`, `£minerals£`, `£food£`, `£influence£`, `£unity£`, `£alloys£`, `£consumer_goods£`, `£trade_value£`, `£physics£`, `£society£`, `£engineering£`, `£pops£`, `£stability£`, `£happiness£`, `£opinion£`, `£empire£`, `£military_ship£`, `£military_power£`, `£blocker£`, plus component stats such as `£ship_stats_hitpoints£`, `£fleet_template_size£`, `£trigger_yes£`.

Frames are selectable: `£leader_skill|3£`. On Windows the character is `Alt+0163`.

Find an unknown code by searching the vanilla `localisation/` folder for `£`.

## Custom Icons and Slash Codes

- A resource or concept icon registered in a `.gfx` file is referenced in localisation by its GFX name in the same way as vanilla `£` codes when the corresponding sprite is defined in the expected library.
- Slash-separated constructs (e.g. `£ship_stats_hitpoints\armor\shield£`) render several stat icons in sequence.

## Style Practices

- One key namespace per mod; mirror the event/building key so `my_mod.1.desc` pairs with `my_mod.1`.
- Keep colour codes closed: unclosed `§` bleeds into every following string in the same widget.
- Prefer `[$VARIABLE|0$]` style formatting over pre-formatted strings so numbers stay locale-correct.
- Never ship a key with unbalanced brackets; bracket parsing failures silently print the raw command.
- Validate by loading the game and running `reload text`, then check `error.log` for missing keys.

## Console Aids

| Command | Purpose |
|---------|---------|
| `reload text` | Re-reads the whole localisation table without restarting |
| `toggle_string_id` | Shows string IDs instead of text, to identify an unknown key |
| `switchlanguage l_english` | Switches language and reloads |
| `reload loc` | Legacy name; prefer `reload text` |