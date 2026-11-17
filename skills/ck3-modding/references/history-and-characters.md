# History, Characters, Dynasties, Houses, Bookmarks

## Character Definitions

Characters are defined per start date in `history/characters/<bookmark>/<file>.txt`. A character block looks like:

```
999001 = {
	name = "Henri"
	dna = lyon_twin_dna_entry
	dynasty = 2100001           # dynasty without a house
	dynasty_house = <house_id>  # use this alternatively
	martial = 14
	prowess = 14
	diplomacy = 23
	intrigue = 10
	stewardship = 21
	learning = 21
	rite = roman_rite
	culture = french
	trait = diligent
	trait = education_learning_4
	female = no                 # yes makes the character female
	sexuality = heterosexual    # asexual, heterosexual, homosexual, bisexual
	health = base_health_value
	fertility = base_fertility_value
	disallow_random_traits = yes

	father = 999003
	mother = 999004

	846.7.29 = { birth = yes }               # date block: yyyy.mm.dd
	920.5.25 = { death = yes }
}
```

Modifying traits within a date block is supported; `give_nickname = <id>` adds/replaces a nickname. Councillor assignment within a date block accepts `councillor_marshal`, `councillor_spymaster`, `councillor_chancellor`, `councillor_court_chaplain`, `councillor_steward`.

Character IDs need only be unique; numbers above 900000 are safe. A string ID is permitted if globally unique.

Attributes cap at 100; unassigned ones are randomised at generation. Character scope access is via `character:<id>`; this works only for historical characters with predictable IDs. Non-historical characters possess only runtime IDs and cannot be targeted from script directly.

### DNA and Portrait Modifiers

DNA tweaks live in `gfx/portraits/portrait_modifiers/<file>.txt`:

```
dna_change_example_modifier = {
	usage = game
	priority = 50                 # higher priority overwrites earlier ones

	dna_change_example_modifier = {
		dna_modifiers = {
			accessory = {
				mode = add
				gene = headgear
				template = western_imperial
				value = 1.0
			}
			color = {
				mode = modify
				gene = hair_color
				x = 0.5
				y = -0.5
			}
		}
		weight = {
			base = 0
			modifier = {
				add = 100
				has_character_flag = dna_change_example_modifier
			}
		}
	}
}
```

Add the flag with `add_character_flag = { flag = dna_change_example_modifier }`.

Outfit tags are listed or tagged conditionally on a portrait:

```
triggered_outfit = {
	trigger = { }
	outfit_tags = { western_stealth_hood sub_saharan_high_nobility mena_war_legwear }
	remove_default_outfit = no
	hide_info = no
}
```

Outfit tags cover body parts and do not overwrite each other. Valid tags are found by searching `..\game\events` and `..\game\gfx\portraits\portrait_modifiers` for `outfit_tags`. Create new tags by editing templates in those folders under `outfit_tags`.

Scripted characters get correct hairstyles/beards by adding a weighted modifier referencing `character:<history_id>` in `gfx\portraits\portrait_modifiers\99_beards_scripted_characters.txt` and `...99_hairstyles_scripted_characters.txt`.

### Calling Characters

Use `character:<id>` from script such as on_actions:

```
character:74025 = {
	if = { limit = { is_alive = yes is_landed = yes } }
	trigger_event = bookmark.0200
}
```

## Dynasty and House Modding

A new dynasty touches four folders:

1. `common/dynasties/<name>.txt` — ID, `prefix`, `name` (a localisation path), `culture`.
2. `localization/<language>/dynasties/dynnn_nnn_l_<language>.yml` — `dynn_<name>: "Dynasty Name"`.
3. `localization/<language>/` prefixes — `dynnp_de: "de "`.
4. `common/dynasty_houses/<name>.txt` — one or more houses attached to the dynasty.

Example:

```
2100001 = {
	prefix = "dynnp_de"
	name = "dynn_Lyon"
	culture = french
}
```

Prefixes live in `localization/english/dynasty_names_l_english.yml` (like `dynnp_de`, `dynnp_d-`); new ones may be added to a custom localisation file.

## Title History

`history/titles/<title>.txt` holds per-date entries:

```
d_name = {
	867.1.1 = { holder = 91491 liege = k_lotharingia de_jure_liege = d_x }
	1066.1.1 = { change_development_level = 10 }
	...
	court_language = language_french   # rank 4/5 with Royal Court only
	set_capital_county = title:c_x     # cosmetic only
	succession_laws = { <law>_succession_law }
}
```

Dates are read in the order they appear, so set high-tier titles before low-tier ones and the low-tier entry wins. For a missing holder entry at game start, the game either takes the last valid de jure carrier or generates a holder spontaneously.

Setting an impossible combination (for example a Muslim holding the Catholic papacy) errors or crashes, and an unclean `government` or `liege` entry can propagate the wrong government or liege to unrelated later holders.

## Bookmarks

`common/bookmarks/<file>.txt` defines campaign start dates, portrait positioners and buttons. Refer to the `.info` file in that folder; bookmarks link characters to titles through the history files above.

### Portraits

Bookmark portraits permit entering an existing character's portrait editor and override its displayed look for the bookmark screen only.

## Culture and Province History

Culture history and province mapping sit under `history/cultures/` and `history/provinces/` — province history changes culture, religion, development or holder by date block.
