# Setup and Entities

## Countries

### Tag Rules

- A tag is a 3-character alphanumeric identifier, unique per country, `A–Z`/`0–9`, conventionally uppercase letters (`ROM`, `CAR`).
- **Never start a tag with a digit** (`1KR`): crashes and unexplained errors.
- `A00`–`Z99` (letter plus two digits) are reserved for dynamically created countries — rebellions and provincial revolts. Using one for a scripted country consumes a finite dynamic slot; avoid it.
- Every country must own at least one province in `own_control_core`, otherwise joining multiplayer crashes.

### Where Things Go

| Data | Location |
|------|----------|
| Country block (government, culture, religion, capital, owned provinces, laws, stance, tech, families, pantheon, treasures, integrated cultures) | `setup/main/*.txt`, vanilla in `00_default.txt` |
| Per-country file (colour, ship names) | `setup/countries/<region>/<name>.txt` |
| Tag → file mapping | `common/countries.txt`, e.g. `ATH = "countries/greece/athens.txt"` |
| Heritages | `common/heritages/` |
| Coat of arms | `common/coat_of_arms/coat_of_arms/` |
| Diplomatic relations | `setup/main/*.txt` in a `diplomacy` block |

Do not place new countries in `00_default.txt` unless doing a total conversion; add a new file instead.

```
PAR = {
    government = despotic_monarchy
    primary_culture = macedonian
    religion = roman_pantheon
    diplomatic_stance = warmongering_stance
    capital = 3435

    poptype_rights = {
        { culture = pactyan type = citizen }
    }

    technology = {
        military_tech = { level = 1 progress = 0 }
        civic_tech    = { level = 1 progress = 0 }
        oratory_tech  = { level = 1 progress = 0 }
        religious_tech = { level = 1 progress = 0 }
    }

    own_control_core = { 3435 6727 7222 3441 6728 6729 }
}
```

```
# setup/countries/greece/athens.txt
color = rgb { 234 139 40 }

ship_names = { Aglaia Anthera Charis Delphis Dynamis Nike Pronoia Thera }
```

### Diplomatic relations

```
alliance = { first = TAR second = MSP }

defensive_league = {
    member = MET
    member = HCL
    member = CRO
}

dependency = { first = CAR second = BLD subject_type = feudatory }
```

### Heritages

Every country has one heritage granting two benefits and one drawback. Heritages live in `common/heritages/`; the `trigger` must end in country scope. Countries matching no heritage fall back to the default heritage — leave the default heritage alone.

```
gaul_heritage = {
    modifier = {
        global_population_capacity_modifier = 0.1
        global_population_growth = 0.1
        monthly_corruption = 0.1
    }
    trigger = { tag = GAU }
}
```

## Characters

Pre-defined characters live in `setup/characters/`.

Hard rules:

- Each pre-defined character needs a **unique, sequential numeric id with no gaps**; if the last id is 59 the next must be 60. Vanilla reached 430 by patch 2.0.5.
- A parent's id must be lower than the child's id.
- Two married characters cannot be defined in separate countries.
- Record the next free id in a README comment in the folder and keep it current — this is the most common source of silent conflicts between mods.

```
"ARM" = {
    country = "ARM"
    49 = {
        first_name = "Orontes"
        family = c:ARM.fam:Orontid
        birth_date = 418.7.8
        culture = "armenian"
        religion = "zoroaster"
        no_stats = yes
        add_martial = 6
        add_charisma = 8
        add_finesse = 5
        add_zeal = 8
        no_traits = yes
        add_trait = "unnoticeable"
        add_gold = 500
        add_popularity = 80
        c:ARM = { set_as_ruler = char:49 }
        dna = "..."
    }
}
```

| Key | Meaning |
|-----|---------|
| `first_name` | Given name |
| `family` | `c:TAG.fam:Name` for a **living** character |
| `family_name` | Plain string for a **dead or unimportant** character |
| `nickname` | Cognomen key, e.g. `"NICKNAME_II"` |
| `birth_date`, `death_date` | **Ab Urbe Condita** `YY.MM.DD` |
| `culture`, `religion` | Culture and religion keys |
| `female` | `yes` for female |
| `no_stats` | Start with 0 in all four attributes |
| `add_martial`, `add_finesse`, `add_charisma`, `add_zeal` | Attribute additions |
| `no_traits`, `add_trait` | Trait control |
| `add_gold`, `add_popularity`, `add_prominence` | Starting personal values |
| `set_as_ruler`, `set_as_coruler` | Called inside `c:TAG = { }` |
| `dna` | Portrait DNA string |
| `father`, `mother` | `char:<id>` |

Any effect may also be executed inside the character block. Generate DNA with the in-game **Portrait Editor** (`pe` console command): **Copy DNA** to the clipboard, **Paste DNA** to refine.

### Character interactions

```
<interaction_name> = {
    message = yes            # default yes
    on_other_nation = yes
    on_own_nation = yes

    potential_trigger = {
        scope:actor  = { }   # country
        scope:target = { }   # character
    }
    allowed_trigger = {
        scope:actor  = { }
        scope:target = { }
    }
    character_actor_trigger = { }
    character_target_trigger = { }

    effect = {
        scope:actor = { pay_price = <interaction_price> }
    }
}
```

## Cultures

`common/cultures/`, one file per culture group by convention. A culture group block holds: `color`, naming pools, graphical culture and ethnicity, and the cultures themselves.

```
bactrian = {
    color = hsv { 0.03 0.7 0.7 }

    male_names = { Tarxun Axak Oxyartes Spitamenes Artaxerxes }
    female_names = { Roxana Roshanak Zunesh Oniya Wyara }
    family = {
        Tarixanian.Tarixanian.Tarixanian.Tarixanian
        Arzakanian.Arzakanian.Arzakanian.Arzakanian
    }

    culture = {
        bactrian = {}
        margian = {}
        sogdian = {}
        tocharian = {
            male_names = { ... }
            female_names = { ... }
            family = { Kausal Gank Tripuskar }
        }
    }
}
```

Family entries carry four dot-separated forms (the name's declension variants); keep the vanilla shape when adding families. A culture entry may override the group-level name pools.

## Religions and Deities

```
# common/religions/
roman_pantheon = {
    color = hsv { 0.65 0.7 0.8 }
    global_citizen_happyness = happiness_large_svalue
    religion_category = pantheon
}
```

- `religion_category` distinguishes polytheistic from monotheistic and drives deity triggers.
- Modifiers must be **country-scope** modifiers; any number is allowed.
- Optional `sacrifice_icon` and `sacrifice_sound` override the default sacrifice presentation.

```
# common/deities/
deity_sekhmet = {
    trigger = {
        polytheistic_check_religion_trigger = yes
        OR = {
            rare_deity_trigger = { RELIGION = egyptian_pantheon }
            deity:omen_sekhmet = { holy_site_deity_check_trigger = yes }
        }
    }
    icon = deity_war
    passive_modifier = { discipline = deity_discipline_svalue }
    omen = { global_defensive = omen_global_defensive_svalue }
    religion = egyptian_pantheon
    deity_category = war
    on_activate = { }
    deification_trigger = { }
}
```

`deification_trigger` excludes the political-influence cost; that cost is applied by the game.

## Ideas

`common/ideas/*.txt` (vanilla `00_ideas.txt`). Any country modifier is legal. Tiers normally gate on technology via `00_tech_tiers.txt`, but any country trigger works. Keep the four-attribute grouping.

```
idea_martial_ethos = {
    trigger = { military_tech >= idea_tier_1 }
    land_morale_modifier = 0.10
    group = military_ideas
    soundeffect = "event:/SFX/UI/Actions/sfx_ui_action_select_idea_military"
}
```

## Coat of Arms

- Script: `common/coat_of_arms/coat_of_arms/`; vanilla pre-scripted flags in `00_pre_scripted_countries.txt`.
- Art: `gfx/coat_of_arms/` (`pattern`, `colored_emblem`, `textured_emblem`).

```
ROM = {
    pattern = "pattern_solid.tga"
    color1 = "roman_red"
    color2 = "roman_gold"

    colored_emblem = {
        texture = "ce_roman_eagle.dds"
        color1 = "roman_gold"
    }
}
```

A key matching a country tag is used automatically as that country's flag. Randomly generated flags come from `template = { ... }` blocks using list-driven colours (`list "triggered_colors_list1"`, `list "checkers"`) and optional `mask`/`instance` for placement. In debug mode, saved flag edits apply immediately.

| Key | Role | Notes |
|-----|------|-------|
| `pattern` | TGA in `gfx/coat_of_arms/pattern` | Omitted → solid red |
| `color1` | Replaces red in the pattern; also colours cloth folds | Required |
| `color2` | Replaces yellow; also colours unit armour | Required |
| `color3` | Replaces white | Only for 3-colour patterns |
| `colored_emblem` | Recoloured emblem | `texture` + `color1`/`color2` |
| `textured_emblem` | Pre-coloured emblem | `texture` only |

## Province Setup

`setup/provinces/*.txt`, conventionally one file per region. Province *ownership* is defined on the country, not here; ports and adjacencies live in `map/`.

```
1 = {                       # Roma
    terrain = "farmland"
    culture = "roman"
    religion = "roman_pantheon"
    trade_goods = "cloth"
    civilization_value = 40
    barbarian_power = 0
    province_rank = "city"

    citizen = { culture = "hebrew" religion = "judaism" amount = 4 }
    nobles = { amount = 5 }
    citizen = { amount = 20 }
    freemen = { amount = 30 }
    slaves = { amount = 10 }
}
```

Pop classes: `nobles`, `citizen`, `freemen`, `slaves`, `tribesmen`. Declare `culture`/`religion` on a pop block only when it differs from the province default.

## Genes

`common/genes/00_genes.txt`. Four-level hierarchy: **Gene Type → Gene Category → Gene Set → Set Entries**. Gene categories share one global index sequence starting at `0`; gene sets use per-category indices. Set entries select objects by gender/age with weighted odds. Use `reload genes` in the console to test without restarting; the in-game Portrait Editor (`pe`) shows the categories.

## Units and Combat Tactics

Unit types: `common/units/*.txt`.

```
archers = {
    army = yes
    assault = yes
    enable = yes

    maneuver = 1
    movement_speed = 2
    build_cost = 4
    build_time = 45

    light_infantry = 1.25
    heavy_infantry = 1.10
    heavy_cavalry = 0.90
    warelephant = 1.0
    archers = 1.0
    camels = 0.9
    light_cavalry = 0.9

    attrition_weight = 0.9
    morale_damage_taken = 1.25
    ai_max_percentage = 15
}
```

- `maneuver` = how many files across it can strike (0 = front rank only).
- `movement_speed` is relative; fastest land ≈ 4, slowest naval ≈ 7, so navies always outpace armies.
- Damage multipliers: `1.0` neutral, `0.75` = 25% less, `1.25` = 25% more.
- `is_second_rank`, `is_flank` set default deployment, not eligibility.
- `attrition_weight` is the unit's army supply weight.

Combat tactics (`common/combat_tactics/`):

```
frontal_assault = {
    use_as_default = yes
    navy = yes
    enable = yes
    sound = "event:/SFX/UI/Unit/sfx_ui_unit_tactic_set_offensive"

    harassment = 0.2      # strong against: +20% damage
    close_ranks = -0.1    # weak against: -10% damage

    effective_composition = {
        liburnian = 0.5
        trireme = 1.0
        mega_galley = 2.0
    }
}
```

## Governor Policies

`common/governor_policies/00_default.txt`. Two parts: the modifiers, and a `chance` block of weighted `modifier` entries.

```
bleed_them_dry = {
    province = {
        local_monthly_food_modifier = -0.25
        local_unrest = 2
        local_tax_modifier = 0.3
        state_commerce_modifier = 0.2
    }

    chance = {
        modifier = { subtract = 10 governor_or_ruler = { loyalty >= 90 } }
        modifier = { add = 5 governor_or_ruler = { has_trait = miserly } }
        modifier = { add = 5 governor_or_ruler = { has_trait = shrewd } }
    }
}
```

## Senate Support (Government)

`common/` government files define per-action approval, one block per party, each with a `base` and a list of `always_modifier` entries whose `add` may be a constant or a computed value block (`value`, `add`, `subtract`, `multiply`, `divide`, `min`, `max`).

```
declare_war = {
    approval = {
        military_party = {
            base = 0
            always_modifier = { add = 0.5  has_civil_war = no }
            always_modifier = {
                add = { value = 0.01 multiply = root.current_ruler.martial max = 0.2 }
            }
        }
        civic_party = { base = 0 always_modifier = { add = -0.5 has_civil_war = yes } }
    }
}
```

## Defines

`common/defines/`. Do **not** replace the whole file; ship a small file with only the changed keys (e.g. `end_date_defines.txt`). New defines cannot be created; only existing ones overridden. Many are undocumented and must be tested. With `-debug_mode`, define changes reload without restart.

```
NGame = {
    START_DATE = "450.10.1"
    END_DATE = "727.2.17"
    GAME_SPEED_TICKS = { 1 0.75 0.5 0.25 0.0 }
}
```