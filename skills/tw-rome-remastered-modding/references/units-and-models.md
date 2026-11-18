# Units, Models, Mounts, Variation, and Ancillaries

## Relationships

One unit spans five files. Nothing is complete until all five agree:

| File | Owns |
|------|------|
| `data/export_descr_unit.txt` (EDU) | Statistics, attributes, ownership, cost, officer and mount references |
| `data/descr_model_battle.txt` (DMB) | Skeleton, LOD models, albedo and PBR textures, ethnicity models, officer models |
| `data/text/export_units.txt` | Display name and description keys |
| `data/characters/` and the vanilla `data/ui/` card folders | `.cas` model and texture sets, unit cards |
| `data/export_descr_buildings.txt` (EDB) | The `recruit` line that makes it reachable |

`descr_strat.txt` starting armies and `descr_battle.txt` historical battles can also name the unit type.

## EDU Entry

```
type             barb peltast gaul
dictionary       barb_peltast_gaul      ; Skirmisher Warband
category         infantry
class            missile
voice_type       Light_1
voice_indexes    0 1 2
soldier          barb_peltast_gaul, 40, 0, 0.9
mount_effect     elephant +6, chariot +6
attributes       sea_faring, hide_improved_forest, hide_long_grass
formation        1.6, 2, 3.2, 4, 3, square
stat_health      1, 0
stat_pri         9, 4, javelin, 50, 6, thrown, archery, piercing, spear, 25, 1
stat_pri_attr    thrown
stat_sec         6, 4, no, 0, 0, melee, simple, piercing, knife, 25, 1
stat_sec_attr    no
stat_pri_armour  0, 1, 2, flesh
stat_sec_armour  0, 0, flesh
stat_heat        2
stat_ground      2, -2, 3, 2
stat_mental      4, low, untrained
stat_charge_dist 30
stat_fire_delay  0
stat_food        60, 300
stat_cost        1, 220, 130, 30, 40, 220
ownership        gauls
ethnicity        gauls, Central_Gaul, don't_allow_mixed, don't_allow_regional, don't_allow_custom
tattoo_color     blue
recruit_priority_offset 100
```

`rebalance_statblock` and a repeated stat block occur in the shipped file to carry the alternate "remastered" balance; the first block is the classic set.

### Field notes that change behaviour

- `type` is free-form with spaces and is the identifier every other file uses.
- `dictionary` supplies the localisation key used by `export_units.txt`.
- `category` (`infantry`, `cavalry`, `missile`, `siege`, `ship`) drives counters and movement.
- `class` (`light`, `heavy`, `missile`, `spearmen`, `berserker`, …) drives combat behaviour and, in 2.0.4, per-class campaign movement.
- `soldier <model>, <soldiers>, <extras>, <mass>[, <radius>, <height>]` — `soldiers` is the medium unit-size count (6–60; general units cap at 31); `extras` is attached animals; `mass` is collision mass and is irrelevant for mounted units, where the mount's mass applies. Hidden `radius` (default 0.4) and `height` (default 1.7) alter fighting density; higher height is weaker.
- **Attack statistics are affected by choice of skeleton**: larger model scale and faster attack animations both increase combat effectiveness. Compensate with `min_delay_between_attacks` (in `stat_pri`) and lethality.
- `mount_effect` accepts at most three entries; extra are ignored. Bonuses apply to melee attack only, never to missiles, and the class bonus stacks with the specific-type bonus.
- `officer` lines accept up to nine models (three before 2.0.4). Officers cannot be assigned to elephants or chariots.
- Exactly one of `animal`, `ship`, or `engine` may be used.
- `stat_health` caps at 15 for both fields; the animal field still counts in auto-resolve.
- `stat_pri atk, chrg, msl_type, msl_rng, msl_ammo, wpn_type, wpn_tech, dmg_type, snd_type, min_delay, lethality`:
  - attack caps at 63 (`63` is used for anything higher); difficulty shifts AI attack by −4 / 0 / +4 / +7.
  - charge caps at 63; the engine uses the **melee** weapon's charge value while the card displays the missile weapon's.
  - missile range floor is 20 and the ceiling comes from the projectile's velocity and angles in `descr_projectile_new.txt`.
  - ammunition floor is 2, or 0 when there is no missile weapon; `infinite_ammo` overrides depletion.
  - `wpn_type`: `melee`, `thrown`, `missile`, `siege_missile`.
  - `wpn_tech`: `simple`, `other`, `blade`, `archery`, `siege`.
  - `snd_type`: `none`, `knife`, `mace`, `club`, `axe`, `sword`, `spear`.
  - `min_delay` is tenths of a second and applies only to foot melee skeletons.
  - lethality is a percentile kill chance per landed blow; it decides whether melee ends in kills or knock-downs and is unused for ranged fire.
- `stat_pri_armour armour, def_skill, shield, sound`: armour and defence skill cap at 63, shield at 31. Defence skill does not help against missiles; shield helps only front and left, and doubles against frontal missiles. `sound` is `flesh`, `leather`, or `metal`.
- `stat_sec_armour` has no shield field. A vehicle or animal with defence skill 0 is treated as 1 HP.
- `stat_heat` runs −2 to 5; it only matters in hot climates.
- `stat_ground scrub, sand, forest, snow` runs 8 to −8 and maps 1:1 to attack.
- `stat_mental morale, discipline, training`: morale 1–2 shows "Poor", 8–11 "Good", 12+ "Excellent". Discipline is `low`, `normal`, `disciplined`, `impetuous`, `berserker`. Training is `untrained`, `trained`, `highly_trained`.
- `stat_fire_delay` is intended as extra volley delay, but the community consensus is that any non-zero value breaks cavalry charges; keep it 0 unless testing deliberately.
- `stat_food` appears unused; vanilla carries `60, 300`.
- `stat_cost turns, recruit, upkeep, weapon_upgrade, armour_upgrade, custom_battle` — turns cap at 244.
- `recruit_priority_offset` (2.0.4) biases AI recruitment: `100` means twice as likely.
- `ownership` controls custom-battle availability and bribery, not campaign recruitment.
- `ethnicity` selects a variation group defined in `descr_unit_variation.txt`; `tattoo_color` seeds colour variation.

### Attributes

`can_sap`, `can_withdraw`, `can_formed_charge`, `can_feign_rout`, `can_run_amok`, `can_swim`, `can_horde`, `hide_forest`, `hide_improved_forest`, `hide_long_grass`, `hide_anywhere`, `sea_faring`, `command`, `heavy`, `hardy` (−2 fatigue), `very_hardy` (−4), `extremely_hardy` (−8), `inexhaustible`, `infinite_ammo`, `non_scaling`, `power_charge`, `slave`, `frighten_foot`, `frighten_mounted`, `mercenary_unit`, `no_custom`, `is_peasant`, `cantabrian_circle`, `druid`, `screeching_women`, `warcry`, `general_unit`, `general_unit_upgrade`, `legionary_name`.

The Remastered-only trio is `extremely_hardy`, `inexhaustible`, and `infinite_ammo`; all three work without arcade mode. Fatigue attributes stack.

### Weapon attributes

`ap` (halve armour), `bp` (body piercing), `prec` (pre-charge throw), `thrown` (elephant and chariot bonus, 20% shorter volley delay), `launching`, `area`, `long_pike` (removed in BI), `short_pike` (required for schiltrom, overrides `spear`/`light_spear`), `spear_bonus_x` (even, 4–12; needs `spear`/`light_spear`), `light_spear` (+8 defence vs cavalry, −4 vs infantry), `spear` (+8 attack vs cavalry, −4 vs infantry, strong push).

Secondary weapon upgrades are bugged: the primary weapon's tech decides upgrades and the secondary inherits the change.

## DMB Entry

```
type carthaginian_general
skeleton            fs_dagger
skeleton_horse      fs_hc_swordsman
skeleton_elephant   fs_forest_elephant_rider
skeleton_chariot    fs_chariot_sword
skeleton_camel      fs_hc_swordsman
male
body Default
angry_face no
medieval_features no
tired VeryTired
aged 0.00
pbr_texture data/characters/textures/carthaginian_general_pbr.tga
pbr_texture spain, data/characters/textures/carthaginian_general_spain_pbr.tga
texture data/characters/textures/carthaginian_general.tga
texture spain, data/characters/textures/carthaginian_general_spain.tga
model African data/characters/carthaginian_general_African
model spain, African data/characters/carthaginian_general_spain_African
no_variation model African data/characters/carthaginian_general_African_no_variation
```

### Skeleton lines

- `skeleton <primary> [secondary]` is mandatory; the rest are optional and used when the unit is mounted on that class.
- Valid skeleton names live in `descr_skeleton.txt` (original) and `descr_skeleton_feral_overrides.txt` (Remastered additions and overrides). Pick the closest existing unit's skeleton rather than inventing one.
- Common originals: `fs_swordsman`, `fs_fast_swordsman`, `fs_semi_fast_swordsman`, `fs_standard_bearer`, `fs_dagger`, `fs_javelinman`, `fs_spearman`, `fs_2handed`, `fs_2handed_berserker`, `fs_crossbow`, `fs_archer`, `fs_slinger_new`, `fs_hc_swordsman`, `fs_hc_archer`, `fs_hc_spearman`, `fs_forest_elephant_rider`, `fs_big_elephant_rider`, `fs_chariot_sword`, `fs_chariot_archer`, `fs_carriage_ballistae_crew`, `fs_horse`, `fs_medium_horse`, `fs_fast_horse`, `fs_cataphract_horse`, `fs_forest_elephant`, `fs_indian_elephant`.

### Appearance fields

| Field | Values |
|-------|--------|
| `male` / `female` | Gender, selects skin texture and voice set |
| `body` | `Default`, `Athletic`, `Bulky`, `Skinny`, `SkinnyAthletic`, `Overweight` — limits the body atlas slots used |
| `angry_face` | `no` uses `<race>_<gender>_faces_serious`, `yes` uses `_faces_angry` |
| `medieval_features` | `no`/`yes`; enables head atlas slots 12–15; per faction as `medieval_features dacia, 0.00` |
| `tired` | `No`, `Tired`, `VeryTired` |
| `aged` | `0.00`–`1.00` share of aged faces (atlas slots 0–4); per faction as `aged dacia, 0.00` |

Skin atlas layout: 5 body sections and 16 face sections. Section use by body type — `Skinny` 1–2, `SkinnyAthletic` 1–3, `Default` 2–4, `Athletic` 3–5, `Bulky` 4–5. `Culann` and `Berserker` ethnicities are hard-coded to all five sections regardless of body type.

### Textures

- `texture [faction,] <path>.tga` points at a `.dds` file whose name merely ends in `.tga`. Contains albedo and alpha. Built with RomeTextureCompress.
- `pbr_texture [faction,] <path>.tga` points at an RGBA map: `R+G` normal, `B` metallic, `A` roughness. Built with RomeTextureCompress.
- The blue channel's metallic effect is **not** read for skin sections.
- Hair is a single `hair.tga.dds`: normal in red/green, diffuse brightness in blue, alpha in alpha. Colour comes from `descr_unit_variation.txt`; hairstyle choice follows UV position.

### Models

- `model <ethnicity> <path>` (and `model <faction>, <ethnicity> <path>`) names a **base path** only. The engine appends `_lod0.cas` … `_lod3.cas`, and all four must exist — copy the nearest LOD and rename it when you have fewer than four.
- `no_variation model …` supplies the set used when the "Unit Variation" graphics option is off.
- `model_flexi <path>.cas, <distance>` and `model_flexi_m` are the older form, still used for animals and mounts, and required when vertices are weighted across two bones. `max` is valid as a distance.
- Same conventions for `descr_model_strat.txt` on the campaign map.

### Model authoring constraints

- `.cas` type 3 chunks: LOD0 may weight vertices across two bones; LOD1 and below must be single-bone.
- Primary and secondary weapons are separate meshes using a single bone.
- 20,000-face limit per model.

## Mounts

`data/descr_mount.txt`. Entry fields: `type`, `class`, `model`, `radius`/`x_radius`, `height`, `mass` (mounted collision mass), `banner_height`, `bouyancy_offset`, `water_trail_effect`, `water_trail_effect_running`, `root_node_height`, `rider_offset`, `attack_delay`, `dead_radius`, `tusk_z`, `tusk_radius`, `riders`, `axle_width`, `wheel_radius`, `pivot_offset`, `pole_length`, `pole_pivot`, `pole_connect`, `harness_connect`. Mount counts are effectively unlimited from 2.0.2.

Mounts follow the `model_flexi` pattern (explicit `.cas` names with distance), not the base-path `model` pattern.

## Animals

`data/descr_animals.txt`. Three classes now: `wardog`, `hound`, `pig`. Each type takes `width` and `offset`. The EDU model/type name must match the `descr_animals.txt` type name — that pairing is no longer hard-coded.

## Unit Variation

`data/descr_unit_variation.txt` defines ethnicity blocks:

```
Central_Gaul
{
	variant
	{
		ethnicity african
		distribution 35
	}
	variant
	{
		ethnicity arabic
		distribution 65
	}
}
```

Referenced from the EDU `ethnicity` line. Distribution values weight the random pick. Hair colour per ethnicity is set here too.

## Traits and Ancillaries

`export_descr_character_traits.txt` and `export_descr_ancillaries.txt` supply effects as keys; valid effect names include `Command`, `Influence`, `Management`, `Subterfuge`, `Loyalty`, `TroopMorale`, `MovementPoints`, `Attack`, `Defence`, `SiegeAttack`, `SiegeDefence`, `Ambush`, `NavalCommand`, `SiegeEngineering`, `NightBattle`, `PersonalSecurity`, `PublicSecurity`, `Bribery`, `BribeResistance`, `Electability`, `LineOfSight`, `TrainingUnits`, `TrainingAgents`, `Construction`, `Trading`, `LocalPopularity`, `Negotiation`, `Farming`, `Mining`, `TaxCollection`, `Fertility`, `CavalryCommand`, `InfantryCommand`, `ElephantCommand`, `GrainTrading`, `SlaveTrading`, `Health`, `Squalor`, `Unrest`, `Law`, `Looting`, `SenateStanding`, `PopularStanding`, `BodyguardValour`, `HitPoints`, `TrainingAnimalUnits`, `BattleSurgery`, `Finance`, `Combat_V_<religion|faction|culture>`, `Religious_Belief <religion>`, `Religious_Order <religion>`.

Constraints that bite: 9 levels per trait, 100 points per trigger, 600 points per threshold. Trigger names are case-sensitive — `BattleOdds` and `Battleodds` are different tokens and the parser reports `Condition parser doesn't recognise this token`.

2.0.4 additions: `MaxAllowed` on traits, `inherit_chance` for inheritance by children, multiple religious effects per trait or ancillary.

`feral_descr_portraits_variation.txt` matches portrait art to character variation.

## Unit Cards and Art

Ship unit cards as `.tga` at 164×224 (4:3, 32-bit with alpha) and the large image at 328×448 where the UI needs it, in the same `data/ui/` subfolder the vanilla cards use — mirror an existing faction's card folder rather than inventing a path. The official unit-card generator is a standalone repository (`FeralInteractive/romeremastered-unitcards`) that renders cards from models; blank grass-circle portrait templates ship in the tech-art guides.