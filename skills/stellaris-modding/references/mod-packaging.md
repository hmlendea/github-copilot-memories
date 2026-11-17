# Mod Packaging, Installation, Load Order, and Override Semantics

## Paths

| Purpose | Path |
|---------|------|
| Mod install (Windows) | `%USERPROFILE%\Documents\Paradox Interactive\Stellaris\mod\` |
| Mod install (macOS) | `~/Documents/Paradox Interactive/Stellaris/mod/` |
| Mod install (GNU/Linux) | `~/.local/share/Paradox Interactive/Stellaris/mod/` |
| Logs, saves, screenshots | One level above `mod/` |
| Steam Workshop content | `<steam>/steamapps/workshop/content/281990/<workshop id>` |
| Paradox Mods content | Inside the user `mod/` folder, named `PDX_<mod id>` |

Never install a mod under the game installation directory; Stellaris will not load it. Folder and file names are case-sensitive on Linux and macOS.

## Mod Skeleton

A local mod needs exactly two entries in `mod/`:

```
mod/
  my_mod.mod            # launcher metadata + path
  my_mod/               # the content folder
    descriptor.mod      # same metadata, no path
    thumbnail.png
    common/ events/ localisation/ interface/ gfx/ ...
```

`my_mod.mod` is what the launcher lists. `descriptor.mod` is what launcher v2 (2.4+) reads and uploads; if missing, the launcher falls back to `my_mod.mod`. The launcher rewrites `my_mod.mod` to match `descriptor.mod`, so edit `descriptor.mod` when both exist.

Create the skeleton through the launcher (**Mods → Mod Tools → Create a Mod**) so both descriptors get the right encoding and the launcher registers the mod immediately.

## Descriptor Fields

| Field | Required | Notes |
|-------|----------|-------|
| `name` | yes | Display name; must match between both descriptors |
| `path` | `my_mod.mod` only | Relative (`mod/MyMod`) or absolute; always use forward slashes; ignored in `descriptor.mod` |
| `dependencies` | no | `{ "Other Mod" }` — this mod loads after those, if present. Use for submods and patches |
| `picture` | no | Must be `"thumbnail.png"` for launcher v2 |
| `tags` | no | `{ "Gameplay" "Graphics" }` — non-standard tags can block Paradox Mods upload; max 10 |
| `version` | no | Arbitrary modder-facing string, not the game version |
| `supported_version` | recommended | `"v3.14.*"` — last component may be `*`; purely a launcher indicator, never gates loading |
| `remote_file_id` | no | Written by the launcher on upload; never edit |

```
name="SomeMod"
path="mod/SomeMod"
dependencies={ "OtherMod" "Another Mod" }
tags={ "Gameplay" "Overhaul" }
picture="thumbnail.png"
version="0.3"
supported_version="v3.14.*"
```

## Thumbnail

`thumbnail.png` in the mod root — the filename is fixed for launcher v2. Minimum 512×512, under 1 MB, otherwise the Workshop upload silently omits or pads it. Close the launcher before changing descriptor or thumbnail files; it reverts them on exit.

## Override Semantics

Stellaris does not have a single duplicate-definition rule. Each `common/` subfolder has one of five behaviours:

| Code | Meaning |
|------|---------|
| **LIOS** | Last In, Only Served — the definition loaded last wins; define the same key in a new file |
| **FIOS** | First In, Only Served — the definition loaded first wins; must sort before the vanilla file (prefix `!!` to the filename) |
| **DUPL** | Both definitions are retained and coexist (lists accumulate, weighted samples pool) |
| **MERGE** | Blocks with the same key are merged field by field; omitted fields keep their original values |
| **NO** | Not moddable, or whole-file replacement only |

Processing order is ASCIIbetical by filename, then launcher/playset order for equal filenames. Vanilla loads before mods.

`events/` is **FIOS**, unlike nearly every other folder: to override a single vanilla event without replacing the whole file, give your event file a name that sorts earlier, e.g. `!!vanilla_override_events.txt`. Since `!` (0x21) sorts below letters, the prefix is the standard trick.

### `common/` merge types (selected)

| Folder | Type | Notes |
|--------|------|-------|
| `agreement_presets`, `agreement_terms`, `agreement_resources` | LIOS | Subject-type terms |
| `ai_budget`, `ai_espionage` | LIOS | AI spending and spy agency |
| `ambient_objects` | DUPL/FIOS | |
| `anomalies` | LIOS | Anomaly categories |
| `archaeological_site_types` | LIOS | |
| `armies` | LIOS | |
| `artifact_actions`, `relics` | LIOS | |
| `ascension_perks`, `ascension_perk_categories` | LIOS | |
| `attitudes` | LIOS | AI attitudes |
| `bombardment_stances` | LIOS | |
| `buildings`, `districts` | LIOS since 3.3 | Pre-3.3 breaks generated modifiers |
| `bypass` | LIOS | Gateways, wormholes, L-gates |
| `casus_belli` | LIOS | |
| `colony_automation*` | LIOS | |
| `colony_types` | LIOS | Colony designations |
| `colors` | NO | Append only |
| `component_sets`, `component_templates` | FIOS | |
| `component_slot_templates` | LIOS | |
| `country_types` | LIOS | |
| `crisis_levels`, `crisis_objectives`, `crisis_paths` | LIOS | Become the Crisis |
| `decisions` | LIOS | |
| `defines` | LIOS | Copy, rename, then keep only the keys you change |
| `deposits`, `deposit_categories` | LIOS | |
| `diplo_phrases` | DUPL | Whole-file override only |
| `diplomatic_actions`, `diplomatic_economy` | LIOS | |
| `economic_categories`, `economic_plans` | LIOS / LIOS* | `economic_plans` merges fields of same-named keys |
| `edicts`, `policies` | LIOS | |
| `espionage_asset*`, `espionage_operation*` | LIOS | Some whole-file only |
| `ethics` | LIOS | Whole-file replacement recommended (multi-file ethics) |
| `event_chains` | FIOS | |
| `fallen_empires` | LIOS | |
| `federation_laws`, `federation_perks`, `federation_types`, `federation_law_categories` | LIOS | |
| `first_contact` | LIOS | |
| `game_concepts`, `game_rules` | LIOS | |
| `global_ship_designs` | FIOS | |
| `governments` | LIOS | Nested `authorities` are FIOS, `civics` LIOS |
| `intel_categories`, `intel_levels` | LIOS | |
| `leader_classes` | LIOS | |
| `map_modes` | LIOS | |
| `megastructures` | LIOS | |
| `message_types` | LIOS | |
| `name_lists` | DUPL | |
| `on_actions` | NO/MERGE | Existing entries cannot be edited; new `name={}` entries merge; files load top-first |
| `personalities` | LIOS | AI personalities |
| `planet_classes`, `planet_modifiers` | DUPL/LIOS | Individual override breaks habitability modifiers |
| `pop_categories`, `pop_jobs`, `pop_faction_types` | LIOS | |
| `portrait_categories`, `portrait_sets` | MERGE/LIOS | |
| `precursor_civilizations` | LIOS | |
| `script_values`, `scripted_effects`, `scripted_triggers`, `scripted_modifiers` | LIOS | |
| `scripted_loc`, `scripted_variables` | FIOS | |
| `section_templates`, `ship_behaviors` | DUPL/FIOS, FIOS | Ship sections |
| `ship_sizes`, `starbase_*` | LIOS | |
| `situations` | LIOS | |
| `solar_system_initializers`, `special_projects` | FIOS | Static maps and unique systems |
| `species_archetypes`, `species_classes`, `species_rights` | LIOS | |
| `species_names`, `random_names` | MERGE/DUPL | |
| `star_classes`, `system_types`, `system_tooltips` | LIOS | |
| `static_modifiers` | LIOS | |
| `strategic_resources` | DUPL | Resources |
| `technology` | LIOS* | LIOS overrides work; a replacement without `potential` inherits the original's |
| `terraform` | DUPL | |
| `traits` | DUPL/FIOS | Whole-file override only |
| `traditions`, `tradition_categories` | LIOS | |
| `war_goals` | LIOS | |

Anything marked with `?` on the wiki is undocumented; assume LIOS and verify by test.

## Load Order

Mods load in playlist order, top first, and later mods win where the merge type allows. Vanilla is always first.

Conventional ordering:
1. Unofficial patches
2. Gameplay mods
3. Submods and compatibility patches
4. UI mods
5. UI patches
6. Universal patches

Names beginning with `~` sort to the top intent, `!` towards the bottom. Submods and patches must sit below the mods they touch. Multiplayer requires an identical mod set **and** identical load order.

## Compatibility Practice

- Prefer new files over copied vanilla files; every copied file must be re-diffed after each game patch.
- Prefix all added filenames and all new keys with a unique mod token.
- Never ship a local copy of a Workshop mod with identical content: the game refuses to load a mod present in both places.
- DLC-gated content must be locked behind its DLC check even when the base mechanic exists without it.
- Ship a symbolically linked working directory during development (a junction on Windows, a symlink on Linux/macOS) and keep only the `.mod` file copied by hand.

## Installing Third-Party Mods Manually

1. Delete any previous installation — both the folder and the `.mod` file. Every file present in the mod folder is loaded, so stale files conflict.
2. Delete the gfx cache at `<user data>/Stellaris/<mod_name>/gfx`.
3. Extract so that `mod/MyMod.mod` and `mod/MyMod/` both exist. A frequent error is extracting into an extra nesting level.
4. If the launcher cannot find the mod, open its `.mod` file and check `path` — Workshop-ripped archives often carry `path="steam/workshop/<name>/"`, which must become `path="mod/<name>/"`.

## Publishing

Upload through **Mods → Upload a Mod**, choose Steam Workshop or Paradox Mods, and confirm the item page afterwards. Updates reuse `descriptor.mod`. The uploaded copy must never coexist with the local folder while testing.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Mod absent from launcher | Wrong install path, or non-ASCII characters in the path | Move under the user data `mod/` folder; use an ASCII path |
| Mod listed but no effect | Local and Workshop copies both present | Remove one, including its `.mod` |
| Mod vanished after launcher update | Stale `launcher-v2.sqlite` entry | Fix `dirPath`/`status` in `launcher-v2.sqlite`, or purge mod state and reload |
| Checksum mismatch in multiplayer | Different mod set, load order, or game version | Equalise playlists and versions exactly |
| Nothing works after many installs | Corrupt launcher database | Quit launcher, unsubscribe all, clear `workshop/content/281990`, delete `dlc_load.json`, `launcher-v2.sqlite`, and the `last_mods={}` block in `settings.txt`, then resubscribe and let all downloads finish |

## Achievements

Achievements cannot be earned once any console command has been used or any installed mod has altered the game's checksum. Script and interface edits alter the checksum; source-only presentation work is the least risky category, but never promise achievement compatibility for a gameplay mod.