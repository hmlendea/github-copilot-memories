---
name: ck3-modding
description: "Use when creating or editing a Crusader Kings III mod, or when working with its Jomini script (effects, triggers, scopes, event targets, saved scopes, variables, script values, scripted effects and triggers, scripted GUIs), mod descriptors (.mod, descriptor.mod), load order and override semantics (LIOS, FIOS, id_override_priority), events and on_actions, decisions, interactions, schemes, activities, story cycles, struggles, characters and DNA, portrait modifiers, dynasties, title and province history, bookmarks, traits, cultures, religions, faiths, holy sites, governments, succession, laws, holdings, buildings, men-at-arms, modifiers, defines, localisation (.yml, UTF-8-BOM), data types, flavorization, interface (.gui), coat of arms, 3D models, map and terrain, music and FMOD sound, fonts, or the console, debug mode and error logs. Covers folder layout, Workshop and Paradox Mods publishing, and load failures. The bundled references hold the full detail and load on demand."
---

# Crusader Kings III Modding

Apply when authoring or reviewing content for **Crusader Kings III** (Paradox Development Studio, Clausewitz engine with the Jomini scripting layer).

Source material: the [CK3 Wiki](https://ck3.paradoxwikis.com/Crusader_Kings_III_Wiki) pages `Modding`, `Modding: getting started`, `Mod structure`, `Mod file`, `Mod compatibility`, `Checksum`, `Scripting`, `Scopes`, `Effects`, `Triggers`, `Variables`, `Script values`, `Scripted effects`, `Scripted triggers`, `Event modding`, `Decisions modding`, `Interactions modding`, `Schemes modding`, `Activities modding`, `Story cycles modding`, `Struggle modding`, `Characters modding`, `Dynasties modding`, `History modding`, `Title modding`, `Trait modding`, `Culture modding`, `Religions modding`, `Governments modding`, `Holdings modding`, `Regiments modding`, `Lifestyles modding`, `Bookmarks modding`, `Defines`, `Modifiers`, `Localization`, `Customizable localization`, `Flavorization`, `Interface`, `Data types`, `Coat of arms modding`, `Graphical assets`, `3D models`, `Map modding`, `Terrain modding`, `Music modding`, `Sound modding`, `Fonts`, `Exporters`, `Console commands`, `Modding tools`, and `Mod troubleshooting`. Most pages are marked timeless or verified between 1.9 and 1.21; treat any unconfirmed detail as needing verification against the installed game files, the `script_docs` dumps, and the error log.

## Non-Negotiable Build Rules

1. **Never edit game files.** Work only inside the mod folder; patches and Steam file verification overwrite the installation. Use a personal mod even for a one-line change.
2. **Mod files live in the user data directory, not Steam.** Windows and macOS: `~/Documents/Paradox Interactive/Crusader Kings III/mod/`. Linux: `~/.local/share/Paradox Interactive/Crusader Kings III/mod/`.
3. **Two descriptors are required and share the mod's name.** `<modname>.mod` sits *alongside* the mod folder and is the one the launcher needs; `descriptor.mod` sits *inside* the folder. The in-folder copy omits `path`.
4. **Localisation is `.yml`, must be UTF-8 **with BOM**, must sit in a language subfolder, must include `l_<language>` in the filename, and must start with `l_<language>:` on the first line.** The folder and the spelling are `localization` (US) — `localisation` is not read.
5. **Whole-file override is by identical path and filename.** Copying a vanilla file replaces all of it. Prefer a new file with a unique, mod-prefixed name wherever the folder merges single objects.
6. **Single-object overrides follow load order**: LIOS (last in, only served) for most script, FIOS (first in, only served) for UI types and templates. Name files accordingly (`01_` later than `00_` for LIOS, `00_my_buttons.gui` for FIOS). With overrides, an object can be changed but never removed.
7. **Achievements and ironman are safe since 1.9** — mods no longer disable achievements and no longer invalidate ironman saves. Console commands still disable achievements, so state that caveat rather than promising achievement compatibility. In multiplayer every player needs the same mods in the same order.
8. **Only one version of a mod may be installed.** A local copy plus a Workshop subscription, or a Paradox Mods copy plus a local folder, confuses the launcher and can stop the mod loading entirely.
9. **Indent with tabs and comment with `#`.** Clausewitz script is brace-structured; mismatched braces are the most frequent hard failure.
10. **Read `logs/error.log` after every change** and run `script_docs` once per patch. A silently inert effect or trigger is usually a wrong scope, a misspelled key, or a patch-level change — not a broken install.

## Layout

```
Crusader Kings III/mod/
  my_mod.mod                 # launcher descriptor (required, alongside the folder)
  my_mod/
    descriptor.mod           # in-folder descriptor (no path key)
    thumbnail.png            # 1:1, max 1 MB; Workshop banner
    common/                  # scripted definitions (largest surface)
      defines/               # NCharacter, NEngine, ...
      on_action/             # singular: on_action, not on_actions
      scripted_effects/
      scripted_triggers/
      script_values/
      scripted_guis/
      decisions/
      character_interactions/
      traits/ cultures/ religion/ landed_titles/ holdings/ buildings/
      men_at_arms_types/ modifiers/ dynasties/ lifestyles/ lifestyle_perks/
      focuses/ terrain_types/ struggle/ story_cycles/ council_positions/
      council_tasks/ bookmarks/ ...
    events/                  # *.txt, one namespace per file
    history/
      characters/ titles/ provinces/ wars/ cultures/  # initial state
      # plus: common/bookmarks/ for start dates and bookmarks
    localization/
      english/               # <name>_l_english.yml (UTF-8 BOM)
      replace/english/       # keys here load last and win
    gui/                     # *.gui layouts (whole-window replacement)
    gfx/                     # .dds icons, portraits, coat-of-arms art
      portraits/portrait_modifiers/   # DNA and outfit-tag modifiers
    map_data/                # heightmap.png, rivers.png, province maps
    music/                   # music.txt, music_categories/, .ogg
    run/                     # optional: run-script .txt files for testing
```

A file at `my_mod/common/scripted_triggers/all_can_raid_trigger.txt` overrides the vanilla `can_raid_trigger` declaration; a file at `my_mod/gui/window_character.gui` replaces the entire vanilla window.

## Domain Map

| Need | Vanilla location | Reference |
|------|------------------|-----------|
| Descriptors, install paths, load order, override rules, footprint and compatibility, publishing, troubleshooting | `mod/*.mod` | `references/mod-packaging.md` |
| Syntax, effects, triggers, logic blocks, scopes, event targets, saved scopes and values, variables, statements, loops, iterators, lists, scripted effects and triggers, script values | `common/scripted_*`, `common/script_values` | `references/scripting.md` |
| Event files, namespaces, event types, portraits and animations, themes, triggers, descriptions, options, on_actions, pulses, delays | `events/`, `common/on_action/` | `references/events-and-actions.md` |
| Decisions, character interactions, schemes, activities, story cycles, struggles | `common/decisions/`, `common/character_interactions/`, `common/activities/` | `references/decisions-and-interactions.md` |
| Characters, DNA, portrait modifiers, outfit tags, dynasties and houses, title and province history, bookmarks | `history/`, `common/dynasties/`, `common/bookmarks/` | `references/history-and-characters.md` |
| Traits, cultures, innovations, religions, faiths, rites, holy sites, landed titles (tiers `b_`–`h_`, including hegemony), governments, succession, laws, holdings, buildings, men-at-arms, modifiers, defines, lifestyles, terrains | `common/` | `references/common-definitions.md` |
| `.yml` rules, BOM, formatting codes, `$` reuse, data types, arguments, customizable localization, flavorization | `localization/` | `references/localisation.md` |
| `.gui` layouts, scripted GUIs, data types in UI, portraits and DNA, coat of arms, 3D models, map, terrain, music, sound, fonts | `gui/`, `gfx/`, `map_data/`, `music/` | `references/interface-graphics-map.md` |
| Console, launch options, `script_docs` dumps, logs, run scripts, CK3 Tiger, debugging workflow | — | `references/console-and-debugging.md` |

Open only the reference needed for the task.

## Working Method

1. **Locate the vanilla source file and decide the override strategy before copying anything.** Determine whether the folder is LIOS, FIOS, whole-file only, or append-only (`references/mod-packaging.md`); that single decision prevents most "my mod does nothing" and "my mod broke another mod" reports.
2. **Confirm the scope chain before writing an effect or trigger.** Character, landed title, province, county, faith, culture, dynasty, house, artefact, scheme, activity, story cycle, struggle, war, army, combat side. Events, decisions and interactions differ in what they make available: interactions expose `scope:actor` and `scope:recipient` and have **no** `root`, while on_actions expose whatever their file comments declare (`references/scripting.md`).
3. **Guard optional links.** Trigger blocks early-out, so an existence check placed first prevents both errors and cost; tooltipped blocks do **not** early-out and need `trigger_if` instead. Use `?=` for existence-checked comparisons.
4. **Prefer firing events from an on_action, decision, interaction or scripted GUI over inventing polling.** Events never fire on their own. When you must append behaviour to an on_action, chain a custom on_action through its `on_actions = { }` list — never restate `effect` or `trigger`.
5. **Register everything the game must find**: namespace line at the top of every event file, localisation keys for every new object (`trait_<key>`, `<decision>_desc`, `<title>_adj`, `<faith>_adherent`, and the rest), `.dds` icon at the conventional path, a `.gfx` entry where sprites are used, and unlimited `history/` entries for anything that must exist at game start.
6. **Validate in game, not by inspection**: launch with `-debug_mode -develop`, use `event`, `run <file>.txt`, `reload gui`, `script_docs`, the Explorer, and the error tracker (`release_mode`), then read `logs/error.log` and `logs/database_conflicts.log`.
7. **Run CK3 Tiger (or the Paradox Modding Toolkit / CWTools) while iterating.** Static validation catches unknown triggers and effects, wrong scopes, missing localisation keys, and duplicate definitions faster than any in-game loop.
8. **Re-verify vanilla keys after each patch.** The wiki tables lag the installed build; `script_docs` output (`effects.log`, `triggers.log`, `modifiers.log`, `event_scopes.log`, `event_targets.log`, `on_actions.log`) and the shipped `.txt` files are authoritative.

## Honest Limits

- Script has no string manipulation, no inline maths, and only one-dimensional lists and variables. Arrays are emulated with list variables over containers (provinces, story cycles).
- `while` loops are capped at 1000 iterations and cannot be broken out of. Unbounded `every_*` inside `every_*` iterators (for example `every_living_character = { every_province = { ... } }`) is a documented lag source.
- Scripted GUIs are hidden events triggered from the UI; they cannot make two windows share data that the code was not configured to share.
- UI cannot add hotkeys (`.shortcuts` in a mod is ignored), cannot create a new HUD skin (new `.skin` files are ignored), and cannot display another window's data unless the developers exposed it. Windows must be replaced whole, in the specifically named `.gui` file.
- The GUI editor exists but is limited; `gui.debug` inspection and the Explorer are the practical tools.
- AI and army behaviour is hardcoded. It can be influenced through `ai_*` clauses and weights, not rewritten.
- Adding buildings or holdings requires replacing the whole `common/holdings/holdings.txt`; new clothing requires overwriting `genes`; new animations require overwriting the idle animation.
- A single-object override cannot delete an object, only change it. On_actions append `events`, `random_events` and `on_actions`, but a restated `trigger` or `effect` overwrites (and errors).
- Mods downloaded from Paradox Mods that add **new files** can be silently ignored by the game; installing them manually is the documented workaround.
- Map modding is unforgiving: a river map with any colour outside the vanilla index (including antialiasing or alpha) crashes the game to desktop, and the heightmap must be 16-bit greyscale matching `original_heightmap_size`, repacked after every change.
- Sound cannot be added without FMOD banks (FMOD Studio 1.10.20 is the recommended version) and neither sound nor music reloads without a game restart.
- A local copy and a subscribed copy of the same mod must never coexist; the launcher cannot reconcile them.
