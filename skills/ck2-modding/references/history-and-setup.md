# History, Setup, and World Data

## History Layout

```
history/
  characters/    # >18000 vanilla characters
  titles/        # holder history per landed title
  provinces/     # holdings, culture, religion, dates
  technology/    # initial province technology by start date
  wars/          # wars already in progress at a start date
  offmap_powers/ # offmap holder and status history
```

History is read when a campaign starts. Loading from a save skips vanilla history entirely (since 2.5), so history edits never affect an ongoing game.

Titles that must not exist at game start (a reformed religion's head, for example) need a history file that disables the title; without it a ruler is generated randomly.

## Characters

Defined in `history/characters/`. The key is the numeric character ID, and duplicate IDs break character history.

```
122 = {
    name = "Harold"
    dynasty = 756
    dna = "medjejoencc"
    properties = "ae00e0"
    martial = 8
    diplomacy = 6
    intrigue = 5
    stewardship = 6
    learning = 4
    religion = "catholic"
    culture = "saxon"
    add_trait = "arbitrary"
    add_trait = "proud"
    father = 120
    mother = 101534

    1025.1.2 = { birth = yes }
    1048.1.1 = { add_spouse = 131 }
    1065.6.6 = { add_spouse = 123 }
    1066.9.14 = { raise_levies = { location = 62 force_mult = 2.5 } }
    1066.10.14 = {
        raise_levies = { dismiss = yes location = 62 force_mult = 2.5 }
        death = { death_reason = death_battle killer = 140 }
    }
}
```

Attributes:

| Attribute | Type | Notes |
|-----------|------|-------|
| `name` | string | Rendered literally; **not** a localisation key |
| `female` | bool | Sex |
| `dynasty` | dynasty ID | Numeric ID from `common/dynasties`; `random` picks one. `dynasty = none` no longer works — use `effect = { dynasty = none }` inside the birth date |
| `father`, `mother` | char ID | Parents |
| `real_father` | char ID | Biological father; unused in vanilla |
| `dna` | 11-char string | Portrait genetics |
| `properties` | 6- or 11-char string | Clothing and headgear |
| `martial`, `diplomacy`, `intrigue`, `stewardship`, `learning` | int | Base attributes |
| `health`, `fertility` | int, float | Base values |
| `religion`, `secret_religion`, `culture`, `race` | ID | `race` uses a culture's graphical culture |
| `trait` / `add_trait` | trait ID | Repeatable; characters with no traits get random ones unless `disallow_random_traits = yes` |
| `occluded` | bool | Portrait occlusion |
| `historical` | bool | Never pruned from the database |
| `easter_egg` | bool | Never auto-assigned to a society |

Date blocks take `YYYY.MM.DD` keys and history commands:

| Command | Effect |
|---------|--------|
| `birth = yes` | Birth date |
| `death = yes` / `death = { death_reason = <reason> killer = <char id> }` | Death; reasons include `death_natural`, `death_murder`, `death_murder_unknown`, `death_hashshashin`, `death_battle`, `death_duel`, `death_execution`, `death_dungeon`, `death_sacrificed`, `death_accident`, `death_suicide`, `death_rabble`, `death_childbirth`, `death_trait` |
| `add_claim` / `remove_claim` | Strong claim on a title; `add_weak_claim` is only available through `effect` |
| `add_spouse`, `add_matrilineal_spouse`, `add_consort`, `add_lover`, `remove_spouse` | Relations by character ID |
| `employer`, `give_job_title` | Move to another court and grant a council job |
| `give_nickname` | Nickname ID |
| `prestige`, `piety`, `decadence`, `wealth` | Adjust values at that date; negatives allowed |
| `remove_trait`, `capital`, `dynasty` | Change state at that date |
| `immortal_age` | Physical age at which the character became immortal; also pairs with an `immortal` trait |
| `raise_levies = { location = <province> force_mult = <float> dismiss = yes }` | Raise or dismiss historical armies |
| `effect = { ... }` | Arbitrary character-scope commands; applied at game start only, and only while alive |
| `effect_even_if_dead = { ... }` | Same, but also after death |

Notes:
- `effect` blocks execute at the first game tick, not during lobby rendering, so anything that must be visible in the lobby has to be expressed as attributes.
- Historical armies use `raise_levies` together with `death` to model real battles.

## Dynasties

Located in `common/dynasties/`. A dynasty is a numeric key with a name and a coat of arms.

```
756 = {
    name = "Godwin"
    culture = "saxon"
    coat_of_arms = {
        template = 0
        layer = {
            texture = 2
            texture_internal = 9
            emblem = 0
            color = 3
            color = 1
            color = 2
        }
    }
}
```

- Duplicates loaded **before** vanilla (prefix `000_`) override the shield; duplicates loaded **after** (prefix `z_`) override the name. Override both by duplicating twice with both prefixes.
- Coats of arms are described by `template`, `texture`, `emblem`, `texture_internal`, and three colours, using the tables in `interface/coats_of_arms.txt`.
- `coat_of_arms = { data = { 0 2 0 9 3 1 2 } }` is the shorthand in the order template, texture, emblem, texture_internal, color1, color2, color3.
- Dynasty shields use the layered system; landed titles use flat `gfx/flags/<title>.tga` images instead.

## Titles

Titles live in `common/landed_titles/` (since 3.3; older layouts put them in one `landed_titles.txt`). Tier is encoded in the prefix: `b_` barony, `c_` county, `d_` duchy, `k_` kingdom, `e_` empire.

Minimal titular title:

```
k_mytitle = {
    color = { 255 255 0 }
    color2 = { 255 255 255 }   # border colour, optional
    capital = 57               # province ID
}
```

Hierarchy is expressed by nesting: kingdoms inside empires, duchies inside kingdoms, counties inside duchies. Title `de_jure_liege = d_york` overrides the de jure parent of an individual title without moving it in the tree.

Other fields:

| Field | Effect |
|-------|--------|
| `norwegian = "Søreyar"` and similar culture keys | Localised name per culture, inline |
| `title = <loc key>` | Override the ruler's title name |
| `coat_of_arms = { ... }` | Barony arms; higher tiers read `gfx/flags/<title>.tga` |
| `pagan_coa = { ... }` | Alternative arms while held by a pagan |
| `holy_site = <religion>` | Holy site marker (also configurable from religion files) |
| `de_jure_liege` | Override the de jure parent |

Rules:
- A missing `gfx/flags/<title>.tga` shifts flag assignment for other titles, so always ship one. Flags must be 24-bit uncompressed 128×128 `.tga`, or the game crashes.
- Baronies cannot use `gfx/flags/` images; give them `coat_of_arms` or `pagan_coa` blocks instead.
- Localise `<title>` and `<title>_adj`; the console command `log_missing_adjectives` lists titles missing the adjective.
- History for titles goes in `history/titles/<title>.txt`; an active title with no history receives a randomly generated ruler.
- `de jure` drift during play changes the hierarchy that the start date defines.

## Provinces

`history/provinces/` describes each province's county title, holdings, culture, religion, terrain, and dated changes. Filenames follow `<ProvinceId> - <ProvinceName>.txt`, where the province name must match `definition.csv` exactly.

```
# 1 - Vestisland
# County Title
title = c_vestisland

# Settlements
max_settlements = 2
b_reykjavik = tribal
#b_alftanes = city
#b_skalholt = temple

# Misc
culture = norse
religion = norse_pagan
terrain = arctic

# History
867.1.1 = {
    b_reykjavik = tb_shipyard_1
}
900.1.1 = {
    b_reykjavik = castle
    b_reykjavik = ca_shipyard_1
    b_alftanes = city
}
1000.1.1 = {
    culture = norwegian
    religion = catholic
}
```

Notes:
- Top-level keys apply at every start date; dated blocks change holdings, buildings, culture, or religion from that date onwards.
- A barony is created by naming it with a holding type (`castle`, `city`, `temple`, `tribal`); later dates replace it with the actual building chain IDs.
- `max_settlements` caps how many baronies the county can hold.
- There is no `effect = { }` history command for provinces; put the logic in the county title's history and scope through `location`.
- Province IDs must match `map/definition.csv`; adding a province requires map edits.

## Technology History

`history/technology/` sets starting technology per province and start date. Values are defined per technology group. A common pattern is a base file plus dated overrides for later bookmarks.

## Wars

`history/wars/` seeds wars already running at a start date: attacker, defender, casus belli, war score, and participants. Used only for bookmarks with a war in progress.

## Bookmarks

`common/bookmarks/` defines the selectable start dates, ordered chronologically in-game regardless of file order.

```
bookmark = {
    name = "BM_THE_MONGOLS"
    desc = "BM_THE_MONGOLS_DESC"
    date = 1220.1.1
    character = 140
    character = 1316
}
```

- The first six `character` entries appear in the era screen, each needing an `ERA_CHAR_INFO_<character_id>` localisation key.
- The starting-era screen is hardcoded to five bookmarks; free eras rely on the hardcoded names `BM_FATE_OF_ENGLAND`, `BM_THE_MONGOLS`, and `BM_100_YEARS_WAR`, plus their `EARLY_MED`, `HIGH_MED`, and `LATE_MED` text keys.
- Hiding DLC-locked eras requires overriding `interface/frontend.gui` and moving the unwanted windows off-screen.

## Alternate Starts

`common/alternate_start/` configures shattered-world and random-world options: which titles are kept, how realms splinter, and what randomness is allowed. It is merged, and the mod file should not set `replace_path` on it unless the mod replaces the concept wholesale.

## Definitions and Defines

`common/defines.lua` holds the hardcoded tuning values. `common/defines/*.txt` entries override individual keys from the `.lua`.

```
NDefines.NDiplomacy.MARRIAGE_AI_PRESTIGE_VALUE = 2
```

- Only existing keys can be changed; new defines cannot be added.
- The wiki `Defines` page lists the current keys grouped by life, realm, warfare, dynasty, interactions, interface, and miscellaneous.
- Overriding a define changes the checksum.

## Static and Triggered Modifiers

- `common/static_modifiers.txt` defines the difficulty, rank, and standard modifier blocks used engine-wide. It is not folder-loadable, so overriding requires a whole-file copy.
- `common/triggered_modifiers/` defines modifiers that attach and detach automatically from conditions, evaluated daily for every landed character. Keep the list short and the conditions cheap.
- `common/event_modifiers/` defines attachable modifiers used by `add_character_modifier`, `add_province_modifier`, and `add_holding_modifier`.

## Culture and Religion Links

Character history, titles, and provinces reference culture and religion IDs defined under `common/cultures/` and `common/religions/`. A typo there is silent at load and only surfaces as a wrong map mode or a missing conversion option; validate IDs with The Validator after adding new ones.