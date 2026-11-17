# Common Definitions: Traits, Cultures, Religions, Governments, Holdings, Buildings, Men-at-Arms, Modifiers, Defines, Lifestyles, Terrains

Nearly everything in this file lives in a `common/` subfolder and follows the same pattern: a key, a set of flags, and modifier blocks. A file added in the same subfolder merges at the object level, subject to the override rules in `references/mod-packaging.md`.

## Traits

`common/traits/*.txt`.

```
my_new_trait = {
	education = yes            # marks it as an education trait
	category = personality     # see the category table
	valid_sex = all
	minimum_age = 16
	maximum_age = 15
	potential = {
		exists = dynasty.dynast
		faith = dynasty.dynast.faith
	}

	health = 1.0
	fertility = 0.5
	inherit_chance = 50
	birth = 5
	random_creation = 1
	genetic = yes
	good = yes
	immortal = yes
	physical = yes
	shown_in_ruler_designer = no
}
```

### Categories

`personality`, `education`, `childhood`, `commander`, `winter_commander`, `lifestyle`, `court_type`, `fame`, `health`. Category determines gameplay grouping and sorting, not just display: `education` traits are exclusive, `personality` traits are auto-generated, and so on.

### Notable flags

| Flag | Effect |
|------|--------|
| `valid_sex`, `minimum_age`, `maximum_age`, `potential` | Character eligibility |
| `health`, `fertility` | Numeric effects |
| `inherit_chance`, `birth`, `random_creation` | Inheritance and generation rates |
| `triggered_opinion = { opinion_modifier = <key> ... }` | Opinion modifier conditional on `parameter`, `check_missing`, `same_faith`, `same_dynasty`, `ignore_opinion_value_if_same_trait`, `male_only`, `female_only` |
| `compatibility = { <trait> = <value> }` | Trait compatibility score, read by `compatibility_modifier` and the `trait_compatibility` trigger |
| `parent_inheritance_sex`, `child_inheritance_sex`, `inherit_from_real_father` | Inheritance gating |
| `genetic` | Inactive/active inheritance with a 100%/50% rule |
| `enables_inbred` | Enables the `inbred` outcome when the parents share ancestors |
| `group_equivalence` | Lets several traits answer one `has_trait` group check |
| `genetic_constraint_all`, `forced_portrait_age_index`, `portrait_extremity_shift` | Portrait/DNA consequences; the constraint names must also exist in `gfx\portraits\trait_portrait_modifiers` |
| `immortal` | Stops visual ageing and natural death; pair with `set_immortal_age` |
| `physical` | Marks the trait physical |
| `trait_exclusive_if_realm_contains` | Restricts random commander assignment to listed terrain types |
| `shown_in_ruler_designer` | Ruler Designer visibility (default yes) |

Traits no longer use numeric indexes; Ruler Designer order follows definition order.

Localisation: `trait_<key>` for the name and `trait_<key>_desc` for the description; both may be replaced with `name` / `desc` / `icon` blocks (`first_valid`, `triggered_desc`). Icon default: `gfx/interface/icons/traits/<key>.dds`. In dynamic blocks the root is the character, and it may not exist — always include a `NOT = { exists = this }` fallback first.

## Cultures

`common/culture/`, whose documented subfolders include `cultures/` (culture and culture-group membership), `innovations/`, `traditions/` and `name_lists/`. The culture modding page frames the article as covering every subfolder of `common/culture`, so confirm the complete set against the installed game before assuming one exists.

Culture-group membership is defined in `common/culture/cultures/`, which is also where a culture's group is fixed.

- `graphical_cultures`, `mercenary_names`, `color`, `heritage`
- `character_modifier`
- Name lists: `male_names`, `female_names` (optionally weighted via `10 = { ... }`), `dynasty_names`, `cadet_dynasty_names`, `dynasty_of_location_prefix`, `bastard_dynasty_prefix`
- Naming rules: `pat_grf_name_chance`, `mat_grf_name_chance`, `father_name_chance`, `pat_grm_name_chance`, `mat_grm_name_chance`, `mother_name_chance`, `patronym_prefix_*`, `patronym_suffix_*`, `always_use_patronym`
- `ethnicities` (weighted list), `dynasty_title_names`, `founder_named_dynasties`, `dynasty_name_first`

Note the `nameX_baseY` convention: a name suffixed with `_baseY` marks it as a variant of base name `Y`.

Culture group IDs are lowercase, spaces and hyphens to underscores, plus `_group`. Culture IDs are lowercase with diacritics stripped. Both have documented exceptions (for example Scots → `scottish`, Oghuz → `turkish`), so confirm in the vanilla files rather than deriving blindly.

## Religions, Faiths, Rites, Holy Sites

Four levels: religion family → religion → faith → rite.

### Reinforcement of precedence

`graphical_faith`, `piety_icon_group` and the tenet background icons resolve lowest-level-first: faith beats religion beats family.

### Religion family

`common/religion/religion_family_types/*.txt`.

```
rf_sinitic = {
	piety_icon_group = "taoism"
	graphical_faith = "dharmic_gfx"
	hostility_doctrine = sinitic_hostility_doctrine
	tenet_background_icon = tenet_banner_known_core
	tenet_heretical_background_icon = tenet_banner_unknown_heretical
	tenet_neutral_background_icon = tenet_banner_known_neutral
	tenet_unknown_background_icon = tenet_banner_unknown_neutral
}
```

### Religion

`common/religion/religion_types/*.txt`. A religion sets `family`, `piety_icon_group`, `graphical_faith`, `theocracy_government_type`, `theocracy_lease_contract_type`, `pagan_roots`, plus `doctrine = <key>` lines that apply to every faith inside it. It also defines `traits = { virtues = { ... } sins = { ... } }` with per-trait `weight` and `scale`, `reserved_male_names`, `reserved_female_names`, `holy_order_names`, `holy_order_maa`, `custom_faith_icons` and a `localization = { ... }` block.

Doctrines that allow more than one pick cannot be defined at religion level. Doctrines must be written before the faiths section. Doctrines placed on the religion are a convenience equivalent to repeating them in each faith, and a faith may override them.

### Faith

`common/religion/faith_types/*.txt`.

```
lobbist = {
	main_rite = lobbist
	faith_details = {
		religion = sea_cults
		color = { 0.2 0.2 0.9 }
		icon = lobbist
		reformed_icon = lobbist_reformed
		graphical_faith = "pagan_gfx"
	}
	eminent_holy_sites = { uppsala lejre paderborn }
	holy_sites = { zeeland ranaheim }
	tenets = { tenet_warmonger tenet_human_sacrifice }
	doctrines = { unreformed_faith_doctrine }
}
```

- `holy_sites` and `eminent_holy_sites` are mutually exclusive; never list the same site in both. Eminent sites grant global bonuses as well as local ones.
- `religious_head` (title) and `head_of_rite` (title) appoint the faith's head when a specific title should hold the role.
- A faith without a scripted main Rite has one generated dynamically, seeded by its `tenets` and `doctrines`.
- A faith's doctrines are additive to its main Rite; a doctrine on the Rite in the same group takes precedence.

### Rites

`common/religion/rite_types/*.txt`. Rites add `name`, `desc`, `color`, `icon`, `graphical_faith`, `founder`, `faith`, `cultures`, `convert`, `create`, `tenets`, `doctrines`, `tenet_selection_pair = { requires_dlc_flag = ... tenet = ... fallback_tenet = ... }`. Rite tenets override parent faith tenets for the instantiated main Rite.

### Holy sites

`common/religion/holy_site_types/*.txt`. Only `county` is mandatory.

```
jerusalem = {
	county = c_jerusalem
	barony = b_vaticano
	parameters = { jerusalem_conversion_bonus }
	county_holder_character_modifier = { monthly_piety_gain_mult = 0.05 different_faith_opinion = 5 }
	county_modifier_scaled = { scale = holy_site_total_artifact_rarity development_growth_factor = 0.01 travel_danger = -1 }
	faith_character_modifier = { character_travel_safety_mult = 0.1 }
}
```

`faith_*_modifier_scaled` and `county_modifier_scaled` multiply by a script value. `faith_character_modifier_scaled` applies only when the site is Eminent for the faith; `county_modifier_scaled` applies for Regular and Eminent sites.

Localisation: `holy_site_<name>_name`, `holy_site_<name>_effect_name`, `holy_site_<name>_effects`.

Faith icons: `gfx/interface/icons/faith/<icon>.dds`, 100×100.

Faith/religion localisation requires the family of keys `<name>`, `<name>_adj`, `<name>_adherent`, `<name>_adherent_plural`, `<name>_desc`, plus the large priest/deity/afterlife key set (`HighGodName`, `DevoteeMale`, `PriestFemalePlural`, `PositiveAfterLife`, `GHWName`, and the rest). Many of these may point at other keys rather than new text.

## Governments

`common/governments/00_government_types.txt`; `_governments.info` documents the format.

```
feudal_government = {
	create_cadet_branches = yes
	rulers_should_have_dynasty = yes
	dynasty_named_realms = yes
	council = yes
	regiments_prestige_as_gold = no
	primary_holding = castle_holding
	valid_holdings = { city_holding }
	required_county_holdings = { castle_holding city_holding church_holding }
	vassal_contract = { feudal_government_taxes feudal_government_levies ... }
	ai = {
		use_lifestyle = yes
		imprison = yes
		start_murders = yes
		arrange_marriage = yes
		use_goals = yes
		use_decisions = yes
		use_scripted_guis = yes
		perform_religious_reformation = yes
	}
	color = hsv{ 0.67 1.00 0.78 }
}
```

- `primary_holding` sets the holding type the government treats as primary; `valid_holdings` adds further permitted holdings; `required_county_holdings` enforces the holding mix in a county.
- `vassal_contract` lists the available contract obligations.
- The `ai = { }` block switches individual AI behaviours off — some are additionally disabled by context (independence, tier).

## Holdings

`common/holdings/*.txt`. Adding a holding type requires replacing the whole holdings file (see `references/mod-packaging.md`).

```
my_holding = {
	primary_building = my_01
	buildings = { mychurch_01 mycastle_01 myarmoury_01 }
	flag = myflag
	can_be_inherited = yes
}
```

Loading a holding type auto-generates the modifiers `<holding>_build_speed`, `<holding>_build_gold_cost`, `<holding>_build_piety_cost`, `<holding>_build_prestige_cost`, `<holding>_holding_build_speed`, `<holding>_holding_build_gold_cost`, `<holding>_holding_build_piety_cost`, `<holding>_holding_build_prestige_cost`. They are not declared but may be given values in `common/modifiers`.

Game concept for the icon: `common/game_concepts`, with `alias`, `parent = holding_type` and `texture = "gfx/interface/icons/<name>.dds"`.

## Buildings

`common/buildings/*.txt`.

```
name_of_the_building = {
	levy = 200
	max_garrison = 100
	garrison_reinforcement_factor = 0.01
	construction_time = 720
	type = regular            # regular / special / duchy_capital
	asset = {
		type = pdxmesh
		name = "western_castle_01_level_03_mesh"
		names = { "..." "..." }
		illustration = "path/to/image.dds"
		soundeffect = { soundeffect = "event:/..." soundparameter = { "Tier" = 2.0 } }
		graphical_cultures = { arabicgfx muslimgfx }
		graphical_faiths = { catholic_gfx }
		graphical_regions = { western mena }
		provinces = { 496 1000 }
		governments = { tribal_government }
	}
	is_enabled = { }
	can_construct_potential = { }
	can_construct_showing_failures_only = { }
	can_construct = { }
	show_disabled = no
	cost = { gold = 500 }
	next_building = castle_02
	effect_desc = <loc key>

	character_modifier = { }
	character_culture_modifier = { parameter = <culture param> }
	character_faith_modifier = { parameter = <faith param> }
	characer_dynasty_modifier = { county_holder_dynasty_perk = fp2_urbanism_legacy_1 monthly_prestige_gain_mult = 0.2 }
	province_modifier = { }
	province_culture_modifier = { }
	province_faith_modifier = { }
	province_terrain_modifier = { terrain = <terrain> is_coastal = <bool> is_riverside = <bool> }
	province_dynasty_modifier = { county_holder_dynasty_perk = ... monthly_income = 0.2 }
	county_modifier = { }
	county_culture_modifier = { }
	county_faith_modifier = { }
	duchy_capital_county_modifier = { }
	duchy_capital_county_culture_modifier = { }
}
```

- Asset selection priority, in order: government, province, graphical region, graphical faith/religion/family, graphical culture.
- `is_enabled` gates the building's effects; `can_construct*_potential` gates its availability in the build menu and implicitly includes `is_enabled`.
- The building must also be listed under a holding that can construct it.

## Men-at-Arms

`common/men_at_arms_types/*.txt`; unique filenames are recommended for compatibility.

```
example_maa = {
	type = skirmishers
	damage = 10
	toughness = 10
	pursuit = 10
	screen = 10
	terrain_bonus = { forest = { damage = 10 } }
	counters = { archers }
	buy_cost = { }
	low_maintenance_cost = { }
	high_maintenance_cost = { }
	stack = <men per unit>
	ai_quality = { }
	icon = <icon name without .dds>
	can_recruit = { always = no }    # optional character-scope trigger
}
```

Unit types are scoped to characters; regiment composition rules live under `common/` alongside.

## Modifiers

Modifiers are declared in `common/modifiers/*.txt` when they need a name and icon, and referenced elsewhere as keys.

```
my_modifier = {
	icon = my_icon
	monthly_income = 0.2
}
```

Modifier keys are context-bound — a `country_`-style key is legal only on the corresponding object type. `modifiers.log` lists every modifier and the object types that accept it; consult it before writing a modifier into a trait, building or event. Generated modifiers (holding and terrain families) are not declared but may be assigned values.

Static modifiers applied through script use `add_character_modifier`, `add_county_modifier`, `add_province_modifier` and the corresponding `remove_` effects.

## Defines

`common/defines/*.txt`, organised by category block:

```
NCharacter = {
	BASE_FERTILITY = 0.5
	BASE_HEALTH = 5.0
}
```

- Overrides are object-level: restating a category block replaces the entries supplied, so include only the intended keys or a specific value, and give the file a late-sorting name.
- AI tuning values live in `common/defines/ai` and are also settable in `00_defines.txt`.
- Map dimensions and related constants live in `common/defines/00_defines.txt` and `common/defines/graphic/00_graphics.txt` (for example `PANNING_WIDTH`).
- New defines cannot be created; only existing ones may be overridden.

## Lifestyles, Focuses and Perks

- Lifestyles: `common/lifestyles/`. `is_highlighted`, `is_valid`, `is_valid_showing_failures_only`, `xp_per_level`, `base_xp_gain`, `icon`.
- Focuses: `common/focuses/`. Include `lifestyle = <lifestyle>` to attach a focus to a lifestyle and `type = lifestyle`.
- Perks: `common/lifestyle_perks/`. `lifestyle`, `tree` (GUI layout), `position = { x y }`, `icon`, `parent` (one or more; required to unlock), `can_be_picked`, `can_be_auto_selected`, `auto_selection_weight` (script value, default 1000), `trait`, `effect`, plus `character_modifier`, `doctrine_character_modifier`, `culture_character_modifier` and `government_character_modifier` (the last supports `flag` and `invert_check`).

Perk `name` may be a `first_valid` block in character scope; the perf-tree position multiplies `PERK_X_OFFSET` and `PERK_Y_OFFSET`.

## Terrain Types

`common/terrain_types/*.txt`.

- `attacker_combat_effects` and `defender_combat_effects` are combat effects (see `common/combat_effects/_combat_effects.info`), e.g. `{ name = combat_wetlands image = defender_wetlands advantage = 5 }`.
- Province-to-terrain mapping lives in `common/province_terrain/00_province_terrain.txt`; every province needs a terrain.

## Council Positions and Tasks

- Positions: `common/council_positions/`. Key attributes include `skill`, `special_council_position`, `auto_fill`, `inherit`, `can_fire`, `can_reassign`, `can_change_once`, `name` (with triggered loc support), `modifier` and `council_owner_modifier` (each accepting a `scale` script value, up to five each), `valid_position`, `valid_character`, `on_get_position`, `on_lose_position`, `on_fired_from_position`, `max_amount`, `use_for_scheme_power`.
- Define a `_possessive` localisation key for a position unless `special_council_position = yes`; when composing triggered name strings, only the final key needs it.
- Tasks: `common/council_tasks/`.

## AI Tuning

- Numeric AI constants: `common/defines/ai` and a few in `00_defines.txt`.
- AI weights in script: `ai_chance = { base = <n> modifier = { add = <n> <trigger> } modifier = { factor = 0 <trigger> } ai_value_modifier = { ai_zeal = 1 } }`. `add` and `factor` adjust the base when their trigger passes; `ai_value_modifier` scales with a personality value.
- `is_ai = no` as a trigger in an event or option removes it from AI consideration entirely; `limit = { is_ai = yes }` inside an effect splits behaviour between AI and player.
- Related clauses elsewhere: `ai_will_do`, `ai_potential`, `ai_score`, `ai_check_interval`, `ai_goal`, `ai_quality`.
- Personality values (set by traits and modifiers, read by script): `ai_amenity_spending`, `ai_amenity_target_baseline`, `ai_boldness`, `ai_compassion`, `ai_energy`, `ai_greed`, `ai_honor`, `ai_zeal`, and the rest of the documented set.
- Army composition and combat behaviour is hardcoded; influence it through terrain combat effects, men-at-arms statistics and government AI switches rather than by rewriting it.
