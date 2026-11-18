# Content Definitions: Characters, Cultures and Languages, Religions, Traits, Units, Diseases, and Works of Art

## Characters

Characters are primarily created in setup (`character_db` in `main_menu/setup/start/`) and modified at runtime through effects. Character interactions live in `common/character_interactions/` (see `references/actions-and-interactions.md`).

### Character scope

`scope:actor`, `scope:recipient`, `ruler`, `heir`, `consort`, `regent`, and `character:<script key>` all resolve to character scope. Attributes readable and writable include `adm`, `dip`, `mil`, `age_in_years`, `fertility`, `has_trait`, `in_cabinet`, and estate/bank membership.

### Character skill and trait categories

Trait categories bind a trait to a character role:

| Category | Applies To |
|----------|------------|
| `ruler` | Rulers and heirs |
| `general` | Army commanders |
| `admiral` | Naval commanders |
| `artist` | Artists |
| `child` | Childhood traits |
| `religious_figure` | Religious figures |
| `cabinet` | Cabinet members |
| `health` | Health traits |

### Character definition fields (setup)

`first_name`, `nickname`, `last_name`, `culture`, `religion`, `adm`, `dip`, `mil`, `birth_date`, `death_date`, `female`, `birth`, role traits, `tag`, `estate`, `dynasty`, `father`, `mother`, `spouse`, `has_patronym`, `timed_modifier`, `fertility`, and artist fields. Full example: `references/setup-and-history.md`.

## Traits

**Folder:** `common/traits/`

```
trait_name = {
    allow = {
        adm > 33
        NOT = { has_trait = conflicting_trait }
    }

    category = ruler
    flavor = personality          # personality / education / interests / government_approach

    modifier = {
        global_estate_target_satisfaction = tiny_permanent_target_satisfaction
        monthly_towards_free_subjects = societal_value_minor_monthly_move
        peace_offer_fairness = 0.2
        stability_importance_modifier = 0.1
    }
}
```

Every modifier key must exist in `common/modifier_type_definitions`.

## Cultures

**Folder:** `common/cultures/`

```
welsh = {
    language = welsh_dialect
    color = map_WLS
    tags = { welsh_gfx celtic_gfx british_gfx western_european_gfx european_gfx }

    opinions = {
        cornish = kindred
        english = negative
        breton = positive
    }

    culture_groups = {
        celtic_group
        british_group
    }
}
```

Culture groups: `common/culture_groups/` — a group needs only its script key:
```
celtic_group = { }
```
A culture may belong to multiple groups. Opinion values: `enemy`, `negative`, `neutral`, `positive`, `kindred`.

## Languages and Dialects

**Folder:** `common/languages/`

```
brythonic_language = {
    color = map_WLS
    family = celtic_language_family

    male_names = { ... }
    female_names = { ... }
    dynasty_names = { ... }
    ship_names = { ... }
    lowborn = { ... }

    patronym_prefix_son = "patronym_prefix_welsh_son"
    patronym_prefix_son_vowel = "patronym_prefix_welsh_son_vowel"
    patronym_prefix_daughter = "patronym_prefix_welsh_daughter"
    patronym_prefix_daughter_vowel = "patronym_prefix_welsh_daughter_vowel"
    patronym_suffix_son = "patronym_suffix_..."
    patronym_suffix_daughter = "patronym_suffix_..."

    location_prefix = "de"
    location_prefix_vowel = "d'"
    location_suffix = "..."
    location_prefix_elision = { ... }

    dialects = {
        welsh_dialect = { }
        breton_dialect = { }
    }
}
```

Dialects inherit every language property except nested `dialects`; a dialect's own value overrides the parent's.

Name lists are localisation keys in vanilla; a localisation entry is required for each name key used.

## Religions

**Folder:** `common/religions/`

```
anglican = {
    color = color_anglican
    group = christian
    enable = 9999.1.1

    religious_aspects = 3
    has_religious_influence = yes
    ai_wants_convert = yes

    definition_modifier = {
        global_max_literacy = 5
        global_build_buildings_cost = -0.05
        monthly_religious_influence = 0.1
        maximum_religious_influence = 400
    }

    opinions = {
        bogomilism = enemy
        catharism = neutral
        hussite = positive
        orthodox = kindred
    }

    unique_names = { name_aaron name_abraham ... }
    custom_tags = { lategame_manufactory guild }

    language = latin                # optional fixed liturgical language

    religious_focuses = { ... }
    num_religious_focuses_needed_for_reform = 5
    reform_to_religion = protestant

    tags = { protestant_gfx western_christian_gfx christian_gfx abrahamic_gfx }
}
```

- `definition_modifier` uses religion-category modifiers and propagates to every country following the religion.
- Religious currencies are opt-in booleans: `has_religious_influence`, `has_karma`, `has_yanantin`, `has_doom`, `has_honor`, `has_purity`, `has_rite_power`.
- Religion opinions are symmetric in practice; the default is `neutral` and can be omitted.
- A fixed `language` forces the liturgical language of all follower nations and cannot change at runtime.
- Setting `religious_focuses` and `reform_to_religion` enables a religion-reform path once enough focuses are adopted.

### Related folders

- `common/religion_groups/`
- `common/religious_schools/` (school opinions set at start via `religion_manager`)
- `common/religious_aspects/`
- `common/religious_factions/`
- `common/religious_figures/`
- `common/religious_focuses/`
- `common/holy_sites/`, `common/holy_site_types/`
- `common/gods/`
- `common/avatars/`

## Units

**Folder:** `common/unit_types/`

```
a_caterans = {
    category = army_infantry
    copy_from = a_age_1_traditions_infantry
    light = yes

    buildable = no
    levy = yes

    combat_speed = 0.05
    flanking_ability = 1.5
    initiative = 5

    mercenaries_per_location = {
        pop_type = peasants
        multiply = 0.01
    }

    gfx_tags = { sword_tag light_tag }
}
```

`copy_from` copies unit category, build time, demands, age association, terrain impacts, and light-unit status. The copied template **must be loaded before** the copying unit; when injecting into a template, the mod file must load before any `copy_from` usage.

Related folders: `common/unit_categories/`, `common/unit_abilities/`, `common/levies/`, `common/recruitment_method/`.

## Diseases

**Folder:** `common/diseases/`

Disease definitions control spawning, R0, mortality, spread, environmental infection, stagnation, resistance decay, map mode visibility, and localisation. Starting outbreaks and resistance are set in `main_menu/setup/start` `disease_outbreak_manager`.

Key behaviours:
- Both `add_disease_resistance` and `add_disease_outbreak` **set** values rather than adding.
- The engine adds +5% resistance on top of the declared value.
- Character death chance is driven by per-disease mortality values.

## Works of Art and Artists

**Folders:** `common/artist_work/`, `common/artist_types/`

```
statue = {
    captured = yes
    allow = {
        artist_type = sculptor
    }
}
```

- Passive art creation requires the owner country to have `has_cultural_maintenance`.
- Creation chance sums `global_monthly_art_start_chance` (country) and `artist_monthly_start_chance` (character).
- Production pace uses the `ARTIST_MONTHLY_PROGRESS` define, plus `art_creation_speed`, scaled by the Culture Investment slider share.
- Quality accrues monthly from artist skill × (1 + `work_of_art_quality_modifier`).
- On siege, each work of art has `ART_DESTROY_CHANCE_ON_CONQUEST` to be destroyed and `ART_CAPTURE_CHANCE_ON_CONQUEST` to be captured; the capture chance is net of the destroy chance.
- Starting works of art are placed with `main_menu/setup/start` `work_of_art_manager`.
- Icons use the `WORK_OF_ART_ICON_PATH` define.

## Concepts

**Folder:** `main_menu/common/game_concepts/`

Concepts are the in-game encyclopaedia tooltips. Concept text is blue by default and can be overridden with formatting. Each defined concept needs its own localisation key and may specify a custom icon (default icon otherwise).

## Practical Rules

- Any key referenced from another definition (`culture:`, `religion:`, `language:`, `artist_type:`) must resolve; unresolved keys are logged and the enclosing block aborts.
- Modifier keys must exist in `common/modifier_type_definitions`.
- Every new named entity needs localisation: `<key>`, `<key>_desc`, `<key>_adj`, and category-specific suffixes.
- Static modifier values must be constant; dynamic calculations are rejected at load time.