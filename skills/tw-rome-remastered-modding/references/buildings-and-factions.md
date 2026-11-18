# Buildings, Factions, Religions, Resources, and Senate

## EDB Entry

`data/export_descr_buildings.txt`. Trees are unlimited in count and level from 2.0.4, but the building browser still displays five settlement levels; a sixth level works and breaks the UX.

```
building missiles
{
	classification military
	icon ranged
	levels practice_field archery_range catapult_range siege_engineer
	{
		practice_field requires factions { barbarian, carthaginian, eastern, greek, roman, } and not hidden_resource sparta
		{
			capability
			{
				recruit "carthaginian peltast" 0
				recruit "roman velite" 0 requires not major_event "marian_reforms"
				recruit "roman light infantry auxillia" 0 requires major_event "marian_reforms"
				recruits_morale_bonus bonus 1 requires factions { dacia, }
			}
			construction 3
			cost 1200
			settlement_min large_town
			upgrades
			{
				archery_range
			}
		}
	}
}
```

- Building names carry no spaces.
- `icon` picks the browser category image; `classification` picks the browser section.
- The trailing number in `recruit "<unit type>" <n>` is starting experience (0–9).
- Level blocks, not the tree, hold `capability`, `construction`, `cost`, `settlement_min`, and `upgrades`.

### Classification

`core | defence | military | trade | water | culture | religious`. `fortification`, `infrastructure`, and `other` are still recognised but deprecated and no longer render. Omitting `classification` makes the engine guess from the name: `core_building` → core; `defenses` → defence; `barracks|equestrian|missiles|smith|despotic_law` → military; `market|port_buildings|hinterland_*|caravans` → trade; `health` → water; `academic|amphitheatres|theatres|taverns` → culture; `temple_*|christian_acedemic` → religious. An explicit value overrides the guess.

### Exclusivity tags

```
tags
{
	temple
}
```

Declared once near the top of the file, then applied per building with `tag temple` and enforced with the `no_building_tagged temple [queued] [factionwide]` condition. This replaces the hard-coded "only one temple type" rule and supports arbitrary groups.

### Custom condition strings

```
alias no_other_temple
{
	requires no_building_tagged temple queued
	display_string SMT_TECH_TREE_THREAD_REQUIRES_TEMPLE_DESTRUCTION
}
```

`display_string` resolves through the localisation files (`data/text/expanded_bi.txt` and its language variants), so the reason appears in tooltips and stays localisable. Use an alias whenever a condition is not self-explanatory in the browser.

### Conditions

All of these may gate a level, a capability, or a recruitment line:

| Condition | Meaning |
|-----------|---------|
| `factions { <all\|culture\|faction>, }` | Settlement owner |
| `building_factions { <all\|culture\|faction>, }` | Which faction **built** the building — how conquest-only recruitment is done |
| `building_present <name> [queued] [factionwide]` | Building exists at any level |
| `building_present_min_level <name> <level> [queued] [factionwide]` | At least that level |
| `no_building_tagged <tag> [queued] [factionwide]` | No building with the tag |
| `resource <name> [factionwide]` / `hidden_resource <name>` | Resource presence |
| `port` | Coastal region with a port |
| `is_player` / `is_toggled "<toggle>"` | Player-only, or keyed to a Classic/Remastered toggle |
| `capability <name> <n>` | Settlement has at least that much of a capability |
| `major_event "<name>"` | Major event fired for this faction (replaces `marian_reforms`) |
| `diplomacy <allied\|protector\|protectorate\|same_superfaction\|at_war> <faction>` | Owner's relationship |
| `religion <name> <op> <n>` | Religion influence in the settlement |
| `majority_religion <name>` / `official_religion <name>` | Religious status |
| `is_land`, `climate`, `temple_of_*` (legacy) | Terrain and legacy checks |

Connectors are `and`, `or`, `not`. `queued` includes the build queue; `factionwide` checks every settlement the faction owns, which is how one-per-faction buildings are made.

### Capabilities

| Capability | Effect |
|-----------|--------|
| `population_growth_bonus`, `population_health_bonus` | Growth and public health |
| `trade_base_income_bonus`, `trade_level_bonus`, `trade_fleet` | Trade value, land trade, sea routes |
| `taxable_income_bonus`, `mine_resource`, `farming_level` | Income |
| `road_level`, `wall_level`, `tower_level`, `gate_strength`, `gate_defences` | Infrastructure |
| `armour`, `weapon_simple`, `weapon_missile`, `weapon_bladed`, `weapon_siege`, `weapon_other` | Upgrade availability |
| `recruits_morale_bonus`, `recruits_exp_bonus` | Recruitment quality |
| `happiness_bonus`, `law_bonus` | Public order |
| `construction_cost_bonus_{military,religious,defensive,other}`, `construction_time_bonus_*` | Cost and time |
| `extra_recruitment_points`, `extra_construction_points` | Parallel build capacity |
| `recruit`, `agent`, `agent_limit_settlement <type>` | Availability |
| `religious_belief`, `religious_order` | Conversion and unrest suppression |
| `stage_games`, `stage_races` | Entertainment |
| `dummy` | No effect; a hook for a custom string |

Unused in practice: `population_loyalty_bonus`, `fire_risk`/`population_fire_risk_bonus`, `upgrade_bodyguard`.

2.0.4 lifted the 32-effect-per-level limit and allows negative values to display. `trade_level_bonus`, `recruits_morale_bonus`, and `extra_*_points` were previously inert.

## Resources

`data/descr_sm_resources.txt` is a JSON-style file; hidden resources moved here from EDB.

```json
"gold":
{
	"subtype": "mineable",
	"name": "SMT_RESOURCE_GOLD",
	"tooltip": "TMT_GOLD_TOOLTIP",
	"icon": "data/ui/resources/resource_gold.tga",
	"mining tooltip": "TMT_GOLD_MINE_TOOLTIP",
	"tier": 5,
	"trade value": 15,
	"tags": [ "precious_minerals", "all_minerals", ],
	"mine model": "data/models_strat/resource_mine.CAS",
	"quantity models":
	{
		"data/models_strat/resource_gold.CAS": 1,
		"data/models_strat/resource_gold_02.CAS": 2,
	},
	"default model": "data/models_strat/resource_gold_03.CAS",
}
```

`subtype` is `hidden` (invisible), `slaves` (created by enslavement), `mineable`, or `none`.

Optional attributes: `growth modifier`, `base turns` and `pop impact` (slave lifetime), `single tooltip` (last turn), `mining tooltip` and `mine model` (when `mine_resource` > 1).

Keep the `rome` hidden resource: victory conditions still read it. Hidden resources are placed in `descr_regions.txt` or added at runtime with `add_hidden_resource`.

Decorative resources are subtype `none` with no trade value and no tooltip wiring; useful for dressing the campaign map.

## Factions

`data/descr_sm_factions.txt` is a JSON-style `"factions": [ ... ]` document.

```json
"huns":
{
	"string": "HUNS",
	"description": "HUNS_DESCR",
	"culture": "hun",
	"ethnicity": "eastasian",
	"tags": [ "fgroup_battleforge_temple", ],
	"namelists": { "men": "huns_men", "women": "huns_women", "surnames": "blank_surnames" },
	"horde": { "horde units": [ ... ], "min horde units": 60, "max horde units": 100, ... },
	"logos":
	{
		"loading screen icon": "data/ui/faction_icons/huns.tga",
		"standard index": 4,
		"rebel standard index": 25,
		"logo index": 0,
		"rebel logo index": 25,
		"strat symbol model": "data/models_strat/symbol_huns.CAS",
		"strat rebel symbol model": "data/models_strat/symbol_hun_rebel.CAS",
	},
	"colours":
	{
		"primary": [ 70, 70, 70 ],
		"secondary": [ 0, 0, 0 ],
		"family tree":
		{
			"background": [ 44, 43, 42 ],
			"font": [ 255, 255, 255 ],
			"selected line": [ 255, 255, 255 ],
			"unselected line": [ 200, 187, 187 ],
		},
	},
	"movies": { "victory": "...", "defeat": "..." },
	"available in custom battles": true,
	"prefer naval invasions": false,
	"default religion": "pagan",
	"allow reproduction": true,
}
```

- `standard index` and `logo index` address sprite sheets in `descr_standards.txt` (four per page) and `descr_sm_faction_logos.txt` (one per page); the `rebel_*` variants supply rebel versions.
- A new faction needs its icons, symbol `.CAS` models, standard and logo entries, colour set, namelists, and an entry in `descr_strat.txt`.
- Faction groups (`descr_faction_groups.txt`) and resource groups (`descr_sm_resource_groups.txt`) exist so traits and scripts can test a whole group.
- 2.0.4 makes factions, cultures, religions effectively unlimited, supports multiple super factions, and makes all previously hard-coded emergent factions moddable.

`descr_sm_factions_difficulty.json` tunes per-difficulty faction behaviour. `feral_descr_reputations_and_relations.txt` tunes reputation gain and loss.

## Cultures

`data/descr_cultures.txt` carries per-culture UI, agent settings, and merchant recruit cost/turns. `descr_sm_factions.txt`'s `culture` must exist here. 2.0.4 lets a culture be flagged barbarian-like and makes a number of settlement mechanics per-culture.

## Religions

`data/descr_beliefs.txt` is the religion database, rewritten for Remastered.

```json
"religions":
[
	"hellenism":
	{
		"trait": "Hellene",
		"unrest icon": "data/pips/hellenism_unrest.tga",
		"religion icon": "data/pips/hellenism.tga",
		"info button": "data/ui/buttons/settlementdetailschristianity.tga",
		"name": "HELLENISM_LABEL",
		"unrest tooltip": "HELLENE_UNREST",
		"group": "greek",
		"unrest multipliers": { "heretics": 1, "heathens": 0.1, },
		"hide at zero": true,
	},
]
```

- `trait` is auto-generated when omitted.
- Pips are external `.tga` files, not sprite-sheet offsets, so any number of religions works.
- `group` plus `unrest multipliers` drive heresy-versus-heathen unrest; 2.0.4 also allows unrest scaled by settlement population.
- Enable religion per campaign in `descr_campaigns.txt`; disable the feature and the whole UI disappears for that campaign.
- A settlement's `descr_strat.txt` block may override the religion profile that `descr_regions.txt` sets.

## Senate

`data/descr_senate.txt` is read top to bottom: attitude coefficients and six attitude boundaries; `Begin_Offices <superfaction> … End_Offices`; `Begin_Unit_Rewards <superfaction> … End_Unit_Rewards`; then global fines, rewards, and the mission penalty/reward matrix.

```
Begin_Offices romans_senate

Quaestor
Title           SMT_SENATE_OFFICE_QUAESTOR_TITLE
Description     SMT_SENATE_OFFICE_QUAESTOR_DESCRIPTION
Rank            10
Quantity        1
Duration        8
Sittings        1
Restrictions
End_restrictions
Senate_benefits
	quaestor_immunity
End_senate_benefits
End

End_Offices
```

- `Rank` and `Sittings` are not consumed by the shipped logic.
- `Quantity` is seats, `Duration` is turns served.
- Restrictions accept `not_consecutively`, `<office>_tenure`, and `trait_<name> <level>`.
- Benefits are `quaestor_immunity`, `censor_immunity`, `no_censor_suicide`.
- Unit reward pools list unit types with optional `, requires_event <event>`.
- Office titles and descriptions live in `data/text/expanded_bi.txt`.
- 2.0.4: unlimited super factions, more than three child members, offices fully data-driven, `HasOffice` condition, `TakeOffice`/`LeaveOffice` events, and the `set_faction_senate_standing` / `set_faction_people_standing` / `override_superfaction_popularity` commands.

Log messages to recognise: `Issue when attempting to read descr_senate.txt`, `Unable to find offices for faction <name>`, `Couldn't find senate office title '<key>' in expanded string table`, `'<name>' does not contain a valid office name`, `'<name>' does not contain a valid trait name`, `Expected either 'not_consecutively', 'trait_<trait_name>' or '<office name>_tenure' for restriction, not '<name>'`, `Unrecognised senate benefit`.

## Major Events and Hording

`descr_sm_major_events.txt` defines events that previously were hard-coded (Marian reforms and successors). Each can carry a `major_event_scripts/<event>_trigger.txt`. Gate content with the `major_event "<name>"` condition in EDB and script; force state from `descr_strat.txt` with `set_major_event_enabled` and `trigger_status`.

Hording and emergent factions work as in Barbarian Invasion: define the `horde` block on the faction, mark the faction `emergent` or `re_emergent`, and drive spawning from `descr_strat.txt` or a faction-spawn script. 2.0.4 makes all previously hard-coded emergent factions moddable and adds per-region brigand and pirate faction assignment.

## AI Tuning Files

- `feral_descr_ai_personality.txt` — campaign AI priority profiles; each `personality <name>` block sets `building_priority`, `military_priority`, `diplomatic_priority`. The file accepts at most 32 entries, and a `descr_strat.txt` personality must be written with underscores (`comfortable_caesar`, not `comfortable caesar`) or the AI will not expand.
- `descr_battle_ai_personalities.txt` — 3D battle AI constants and order selection.
- `descr_diplomacy_comments.txt` — optional per-faction or per-culture diplomacy lines.
- `descr_mission_modifiers.txt` — agent mission success rates.
- `descr_sm_factions_difficulty.json` — difficulty scaling.
- `data/toggles/` — Classic versus Remastered rule switches, including campaign and battle AI improvements.