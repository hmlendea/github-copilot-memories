# Common Definitions: Traits, Religions, Cultures, Governments, Laws, Buildings, War, Modifiers

## Loader Behaviour First

Before adding content to any `common/` folder, check `references/mod-packaging.md`. Several folders duplicate rather than override. Reusing a vanilla key in `traits`, `buildings`, `cb_types`, `societies`, `objectives`, `retinue_subunits`, `religion_features`, or `minor_titles` corrupts or doubles the entity.

## Traits

`common/traits/`. Keys are the trait IDs used in script, history, and localisation.

```
selfish = {
    personality = yes
    stewardship = 2
    diplomacy = -1
    opposites = { charitable }
    opposite_opinion = -30
    general_opinion = -10
}
```

Flags select icon grouping and engine behaviour:

| Flag | Effect |
|------|--------|
| `personality` | Personality trait slot |
| `education` | Education trait; `attribute = <attribute>` names the skill it trains |
| `childhood` | Childhood trait |
| `lifestyle` | Lifestyle choice trait |
| `leader` | Command trait; `leadership_traits = N` grants N automatically |
| `is_health` | Health trait, excluded from healthy-only events |
| `is_illness` | Disease; targeted by `is_ill` and `cure_illness` |
| `is_symptom`, `is_epidemic` | Symptom and epidemic markers |
| `cached` | Enables the `<trait> = { }` character scope; keep the count small |
| `hidden`, `hidden_from_others`, `same_trait_visibility` | Visibility control |
| `cannot_marry`, `cannot_inherit`, `can_hold_titles` | Behavioural blocks |
| `incapacitating` | Requires a regent |
| `immortal`, `pilgrimage`, `in_hiding` | Special states |
| `agnatic`, `enatic`, `inherit_chance`, `both_parent_has_trait_inherit_chance` | Inheritance |
| `birth` | Out of 10,000 newborns, how many receive the trait |
| `random = no` | Never assigned to randomly generated characters |
| `religious`, `religious_branch` | Discarded on conversion; branch traits are inherited |
| `opposites` | Mutually exclusive traits |
| `caste_tier` | Ordering within caste traits |
| `customizer` | Whether the Ruler Designer shows it; `ruler_designer_cost` sets its price |
| `vice`, `virtue` | Moral classification |
| `tolerates_<group>` | Sympathy traits |

Rules:
- Positive modifiers are written bare (`stewardship = 2`); a leading `+` is not parsed.
- AI weights (`ai_zeal`, `ai_rationality`, and similar) belong on the trait as modifier-style fields and shape decision making.
- Trait icons are grouped in-game by type (`education`, `caste_tier`, undefined, `lifestyle`, `personality`, `is_health`), in order of application within a group.
- A trait icon is a 24×24 `.dds` or `.tga` in `gfx/traits/` plus a `spriteType` named `GFX_trait_<trait>` in an `interface/*.gfx` file, carrying `noOfFrames = 1`, `norefcount = yes`, and `effectFile = "gfx/FX/buttonstate.lua"`.
- Localise `<trait>`, `<trait>_desc`, and any custom modifier keys.

## Religions

`common/religions/`. Groups contain religions; both are alphanumeric IDs.

```
catholic_group = {
    graphical_culture = westerngfx
    crusade_cb = crusade
    playable = yes

    catholic = {
        icon = 1
        color = { 0.9 0.9 0.9 }
        high_god_name = GOD_GOD
        god_names = { GOD_GOD GOD_THE_LORD }
        evil_god_names = { SATAN LUCIFER THE_DEVIL }
        scripture_name = THE_BIBLE
        priest_title = PRIEST
        crusade_name = CRUSADE
        investiture = yes
        can_excommunicate = yes
        can_grant_divorce = yes
        can_grant_invasion_cb = invasion
        can_call_crusade = yes
        can_have_antipopes = yes
        can_retire_to_monastery = yes
        priests_can_marry = no
    }
}
```

Group fields: `color`, `graphical_culture`, `has_coa_on_barony_only`, `hostile_within_group`, `crusade_cb`, `playable`, `ai_peaceful`, `ai_fabricate_claims`, `merge_republic_interface`.

Religion fields cover conversion AI (`ai_convert_same_group`, `ai_convert_other_group`), presentation (`icon`, `color`, `crusade_name`, `scripture_name`, `god_names`, `high_god_name`, `evil_god_names`, `piety_name`, `priest_title`), religious-head rights (`can_excommunicate`, `can_grant_divorce`, `can_grant_invasion_cb`, `can_grant_claim`, `can_call_crusade`, `can_have_antipopes`), and behaviour (`investiture`, `can_demand_religious_conversion`, `priests_can_marry`, `priests_can_inherit`, `feminist`, `pacifist`, `uses_decadence`, `uses_jizya_tax`, `attacking_same_religion_piety_loss`, `hard_to_convert`, `men_can_take_consorts`, `women_can_take_consorts`, `max_consorts`, `interface_skin`, `parent`).

Rules:
- Religions merge, so a single religion may be overridden without copying the group.
- Reformed pagans must be defined before unreformed ones, and heresies of reformed pagans after both.
- `parent = <religion>` marks a heresy; the parent must be defined earlier in the load order.
- Religion icons are frame indices into `gfx/interface/religion_icon_strip.dds` (plus `religion_icon_strip_small.dds` and the `shattered_random` copies). Adding an icon means widening the strip by 32 pixels (20 for the small strip) per icon, incrementing `noOfFrames` on `GFX_religion_icon_strip` and `GFX_religion_icon_strip_small` in `interface/generalstuff.gfx`, and appending the new index.
- `heresy_icon` is declared on the **parent** religion, not on the heresy.
- Holy sites can be declared in religion files or in landed titles; prefer religion files for compatibility.

## Cultures

`common/cultures/`. Groups contain cultures; both merge since 2.4.

```
north_germanic = {
    graphical_cultures = { westerngfx }

    english = {
        graphical_cultures = { englishgfx westerngfx }
        unit_graphical_cultures = { saxongfx }
        color = { 0.8 0.2 0.2 }
        male_names = { Alfred_Alfred_Alfred_Alfred_Alfred Athelred Harold_Hereweald }
        female_names = { Aethelflaed Godgifu }
        male_patronym = "son"
        female_patronym = "dottir"
        from_dynasty_prefix = "of "
        bastard_dynasty_prefix = "Fitz"
        pat_grf_name_chance = 55
        mat_grf_name_chance = 5
        father_name_chance = 30
        pat_grm_name_chance = 60
        mat_grm_name_chance = 15
        mother_name_chance = 15
    }
}
```

Fields: `graphical_cultures`, `unit_graphical_cultures`, `secondary_event_pictures`, `color` (0.0–1.0 RGB), `horde`, `used_for_random`, `allow_in_ruler_designer`, `dukes_called_kings`, `baron_titles_hidden`, `count_titles_hidden`, `parent`, `modifier`, `character_modifier`, `founder_named_dynasties`, `dynasty_title_names`, `disinherit_from_blinding`, `allow_looting`, `seafarer`, `dynasty_name_first`, `feminist`.

Names:
- `male_names`/`female_names` are space-separated lists. Underscores join equivalent variants (`Johan_John`) so regnal numbering stays consistent across a culture change. Quoted double names (`"Sarah Ann"`) are one name.
- `parent` suppresses the foreigner opinion penalty in one direction only; it is not transitive, and the parent must be defined first.
- Patronyms use `male_patronym`, `female_patronym`, `prefix`, and `grammar_transform = french | spanish`.
- Name weighting (`Name:Weight`) is ignored since 2.5; do not rely on it.

## Governments

`common/governments/`. A government defines who can rule and what they may hold.

Key fields: `potential`, `trigger`, `aggression`, `max_consorts`, `max_liege_levy`, `max_liege_tax`, `free_levies_in_offensive_war`, `unit_modifier`, `unit_home_modifier`, `character_modifier`, `preferred_holdings`, `allowed_holdings` and its `_culture`, `_religion`, `_culture_and_religion` variants, `builds_with_prestige`, `builds_with_piety`, `accepts_liege_governments*`, `free_revoke_on_governments*`, `free_revoke_on_tiers*`, `ignore_in_vassal_limit_calculation`.

Notes:
- Government groups can be split across several files.
- `aggression` shifts the AI's war-declaration opinion threshold by 20 per point; 1 is neutral, below 1 is passive, 0 disables AI war entirely.
- Holding permissions determine the "wrong government type" penalty, so mirror the `allowed_holdings_*` variants for culture- and religion-tolerant cases.

## Laws

`common/laws/`. Laws are grouped by title tier and category (demesne, realm, crown, succession).

```
succ_papal_succession = {
    potential = {
        OR = {
            title = k_papal_state
            title = d_my_religion
        }
    }
    effect = { succession = papal_succession }
    revoke_allowed = { always = no }
}
```

Rules:
- A law reusing an existing name **appends** `allow` conditions but does not replace `potential`, so the law becomes stricter than intended.
- `potential` decides who sees the law, `allow` decides who can pass it, `effect` applies the change.
- Adding an entirely new succession law also needs `common/succession_voting/` rules and matching Crown or realm law hooks, plus localisation for the law and its description.

## Buildings

`common/buildings/`. Buildings belong to a holding type block (`castle`, `city`, `temple`, `tribal`) and are organised in upgrade chains.

```
ca_keep_6 = {
    desc = ca_keep_1_desc
    trigger = { TECH_FORTIFICATIONS_CONSTRUCTION = 8 }
    upgrades_from = ca_keep_5
    gold_cost = 500
    build_time = 2190
    levy_size = 0.3
    garrison_size = 0.2
    ai_creation_factor = 97
    extra_tech_building_start = 0.2
}
```

Fields: `potential` (province scope, with `FROM` as the holder and `FROMFROM` as the holding), `desc`, `add_number_to_name`, `replaces`, `trigger`, `is_active_trigger`, `port`, `prerequisites`, `not_if_x_exists`, `upgrades_from`, `gold_cost` / `prestige_cost` / `piety_cost` (mutually exclusive), `build_time`, `ai_creation_factor`, `ai_feudal_modifier`, `ai_republic_modifier`, `extra_tech_building_start`, `scouting`, `convert_to_city` / `convert_to_castle` / `convert_to_temple` / `convert_to_tribal`, plus any building modifier.

Notes:
- `upgrades_from` accumulates modifiers; `replaces` makes the replaced building unbuildable.
- The global `BUILDING_COST_MULT` define scales all gold costs.
- A negative `tax_income` models upkeep.
- A holding applies only one special-unit modifier set; later special-unit entries on other buildings are ignored.
- Reusing a vanilla building name duplicates it rather than overriding.
- Localise `<building>`, `<building>_desc`, and optionally `<building>_<religion_group>`.

## Holdings

`common/holding_types/`. Triggers **append** across files, so redefining a holding type makes it stricter rather than different. New holding types cannot be added, and some restrictions are hardcoded.

## Casus Belli

`common/cb_types/`. A casus belli is a lifecycle, not a single block.

```
can_use            # on the target character
can_use_title      # on candidate titles
on_add, on_add_title, on_add_posttitle
is_valid, is_valid_title   # polled during the war
on_success, on_fail, on_reverse_demand
```

Important flags: `name`, `war_name`, `sprite`, `truce_days`, `is_permanent`, `is_independence`, `hostile_against_others`, `full_hostility`, `can_ask_to_join_war`, `is_claim_all`, `is_revolt_cb`, `major_revolt`, `press_claim`, `allow_whitepeace`, `allowed_to_target_tributaries`, `can_call_allies`, `attacker_can_call_allies`, `defender_can_call_allies`, `can_call_vassals`, `can_attack_vassals`, `check_de_jure_tier`, `check_dejure_duchies`, `check_all_titles`, `check_all_trade_posts`, `check_actor_direct_vassals`, `other_de_jure_claim`, `is_holy_war`, `battle_warscore_mult`, `attacker_rel_head_is_ally`, `display_on_map`, `infamy_modifier`, `ticking_war_score_multiplier` and its attacker and defender variants.

Rules:
- `is_permanent = no` hides the CB from the interface; use it for war declarations fired by events.
- `check_de_jure_tier` requires `is_permanent = yes`.
- `war_name` localisation can use `$OTHER_TITLE$`.
- Reusing a vanilla key duplicates the CB.

## Modifiers

Four kinds live in different folders:

| Kind | Folder | Attach mechanism |
|------|--------|------------------|
| Event modifier | `common/event_modifiers/` | `add_character_modifier`, `add_province_modifier`, `add_holding_modifier` |
| Triggered modifier | `common/triggered_modifiers/` | Automatic, evaluated daily for landed characters |
| Static modifier | `common/static_modifiers.txt` | Referenced by name from script |
| Custom modifier | `common/modifier_definitions/` | Presentation-only naming convention |

```
sweet_temptation = {
    fertility = 0.2
    church_opinion = -20
    icon = 26
}
```

```
add_character_modifier = {
    modifier = sweet_temptation
    duration = -1          # -1 is permanent
}
```

```
my_triggered = {
    potential = { is_ruler = yes }
    trigger = { trait = ambitious }
    icon = 24
    land_morale = -0.25
}
```

Rules:
- Event modifiers require an `icon` index from `gfx/interface/modifier_icons.dds` and accept optional `is_visible` and `major = yes`.
- Triggered modifiers cost CPU every day; each added one is a permanent tax on late-game speed. `active = no` disables one without deleting it.
- Custom modifiers follow naming conventions that make them work automatically for new content: `<special_unit>`, `<special_unit>_offensive`, `_defensive`, `_morale`, `<culture>_opinion`, `<culture_group>_opinion`, `<religion>_opinion`, `<religion_group>_opinion`, `<trait>_opinion`, `opinion_of_<trait>`, and the offmap currency token.
- Custom modifier display flags: `show_as_percent`, `is_good`, `is_monthly`, `is_hidden`, `max_decimals`, `show_value`. `show_value = no` with no naming match turns the modifier into a pure tooltip carrier.
- Localise `<modifier>` and `<modifier>_EXPLANATION`; the second renders in opinion and modifier breakdowns.

## Minor Titles, Societies, Objectives, Artifacts, Great Works

- `common/minor_titles/` — honorary titles. Cannot be overridden; duplicates share tags.
- `common/societies/` — societies and their ranks, powers, and missions. Duplicates coexist.
- `common/objectives/` — ambitions, plots, factions, foci. Duplicates coexist.
- `common/artifacts/` plus `artifact_spawns/` — artifacts and their spawn rules.
- `common/wonders/`, `wonder_upgrades/` — Great Works and their upgrade tiers.
- `common/offmap_powers/` plus `policies/` and `statuses/` — offmap powers, available without the Jade Dragon DLC.

All merge, but any key that duplicates an existing definition creates a second entity instead of replacing it.

## Death, Disease, Combat, Retinues, Nicknames

- `common/death/`, `execution_methods/`, `death_text/`, `heir_text/` — death reasons and succession flavour text.
- `common/disease/` — disease definitions with outbreak and immunity parameters.
- `common/combat_tactics/`, `special_troops/`, `retinue_subunits/`, `mercenaries/` — battle behaviour and troop composition. Duplicate tactic and retinue keys duplicate.
- `common/nicknames/` — nicknames referenced by `give_nickname`.
- `common/succession_voting/` — elective and tanistry voting rules plus AI voting.

## Game Rules, Bloodlines, Technology

- `common/game_rules/` — lobby-selectable rule toggles. Displayed in file-then-key order; a rule's `potential` gates when it appears.
- `common/bloodlines/` — bloodlines with inheritance rules, `flags = { }`, and modifiers.
- `common/technology.txt` plus `history/technology/` — technology groups, levels, and starting values. A new technology entry also needs localisation and, usually, a building or modifier that consumes it.

## Defines

`common/defines.lua` sets engine tuning. `common/defines/*.txt` entries override individual keys:

```
NDefines.NDiplomacy.MARRIAGE_AI_PRESTIGE_VALUE = 2
```

- New defines cannot be created; only existing keys can be changed.
- Any define change alters the checksum.
- The wiki `Defines` page groups the current keys by life, realm, warfare, dynasty, interactions, interface, and misc; treat it as a research aid, not a contract.