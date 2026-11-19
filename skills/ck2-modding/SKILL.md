---
name: ck2-modding
description: "Use when creating or editing a Crusader Kings II mod, or when working with its Clausewitz script (effects, triggers, scopes, scope chains, variables, flags, event targets, scripted triggers and effects), mod descriptors (.mod), load order and duplicate-definition behaviour, replace_path overrides, events and on_actions, decisions, character, dynasty, title and province history, traits, religions, cultures, buildings, governments, laws, casus belli, modifiers, defines, localisation (.csv), interface (.gui) and graphics (.gfx, portraits, coats of arms), music, map data, or the console, The Validator and logs. Covers mod folder layout, Workshop publishing, checksum and ironman safety, and load failures. The bundled references hold the full detail and load on demand."
---

# Crusader Kings II Modding

Apply when authoring or reviewing content for **Crusader Kings II** (Paradox Development Studio, Clausewitz engine). The wiki's newest documented build is 3.3.5.1 (checksum `SOHY`); verify the installed build before trusting a patch-sensitive detail.

Source material: the [CK2 Wiki](https://ck2.paradoxwikis.com/Crusader_Kings_II_Wiki) pages `Modding`, `Mods`, `Creating a mod`, `Mod file`, `Scripting`, `Scopes`, `Conditions`, `Commands`, `Event modding`, `Decision modding`, `Character modding`, `Dynasty modding`, `Title modding`, `Province modding`, `History modding`, `Trait modding`, `Religion modding`, `Culture modding`, `Government modding`, `Law modding`, `Building modding`, `Casus Belli modding`, `Modifiers`, `Defines`, `Localisation`, `Interface modding`, `Graphics modding`, `Portrait modding`, `Coats of arms modding`, `Map modding`, `Music modding`, `Console commands`, `Troubleshooting`, `The Validator`, and `Steam Workshop`. Wiki pages are version-tagged per section (most verified 2.7–3.3); treat any unconfirmed detail as needing verification against the installed game files and The Validator output.

## Non-Negotiable Build Rules

1. **Never edit game files.** Work only inside the mod folder; Steam updates and file verification overwrite the installation.
2. **Mods live in the user data folder, not Steam.** `~/Documents/Paradox Interactive/Crusader Kings II/mod/` on Windows and macOS, `~/.paradoxinteractive/Crusader Kings II/mod/` on Linux. The game's own `mod/` directory is legacy and ignores `replace_path`.
3. **Encoding is ANSI (Windows-1252) for every text file.** CK2 does not support UTF-8, with or without BOM. A UTF-8 file produces mojibake or dropped text, and colour codes stop rendering.
4. **The localisation folder is `localisation`, and every file must end in `.csv`.** A `.txt` file in that folder is silently ignored. The separator is a semicolon, not a comma.
5. **Minimise overwritten vanilla files.** Add new files in the same folder wherever the folder merges definitions; copy a vanilla file only when whole-file replacement is intended.
6. **Never reuse an existing definition key unless the folder documents overriding as safe.** Several `common/` folders coexist duplicates instead of overriding them (`traits`, `buildings`, `societies`, `objectives`, `casus_belli`, `retinue_subunits`, `religion_features`), producing silently doubled content.
7. **Mods that change gameplay script alter the checksum and disable achievements.** Localisation and pure graphical or music replacement do not. Achievements additionally require single-player ironman and an untouched installation.
8. **Names and paths are case-sensitive on Linux and macOS.** Use `lower_with_underscores` for folders and files, and match vanilla path case exactly.
9. **Indent with one tab and comment with `#`.** Mismatched braces are the most common hard failure and the one The Validator catches fastest.
10. **Read `logs/error.log` after every change.** A silently inert command or condition is usually a wrong scope, an unregistered key, or a folder-loading rule, not a broken install.

## Layout

```
Crusader Kings II/mod/
  mymod.mod                    # launcher descriptor, no spaces in the filename
  mymod/                       # same tree as the game root
    common/                    # definitions: traits, religions, cultures, ...
    decisions/                 # decision files
    events/                    # event files, one namespace per file
    history/
      characters/              # historical characters
      titles/                  # title holder history
      provinces/               # holding, culture, religion history
      technology/              # initial technology by province
      wars/                    # on-going historical wars
    interface/                 # *.gui layouts, *.gfx sprite libraries, sound.sfx
    localisation/              # *.csv, ANSI, optional customisable_localisation/
    gfx/                       # .tga/.dds art, flags, portraits, event pictures
    map/                       # provinces.bmp, definition.csv, adjacencies, terrain
    music/                     # .ogg plus song definition .txt
    sound/                     # sound effects
```

A file at `mymod/common/traits/mytraits.txt` adds traits; a file at `mymod/localisation/00_mymod.csv` is loaded first and wins over vanilla keys. Add new files instead of copying vanilla ones whenever the folder merges.

## Domain Map

| Need | Vanilla location | Reference |
|------|------------------|-----------|
| `.mod` fields, install paths, load order, duplicate-definition rules, `replace_path`, Workshop, checksum | `mod/*.mod` | `references/mod-packaging.md` |
| Syntax, value types, numeric and boolean operators, control flow, scopes, scope chains, flags, variables, event targets, scripted triggers and effects | `common/scripted_triggers/`, `common/scripted_effects/` | `references/scripting.md` |
| Event types and blocks, pre-triggers, mean time to happen, weight multiplier, options, portraits, event chains, on_actions, decisions | `events/`, `common/on_actions/`, `decisions/` | `references/events-and-decisions.md` |
| Characters, dynasties, titles, provinces, technology, wars, bookmarks, history commands | `history/`, `common/dynasties/`, `common/landed_titles/` | `references/history-and-setup.md` |
| Traits, religions, cultures, governments, laws, buildings, casus belli, modifiers, defines, societies, artifacts, great works | `common/` | `references/common-definitions.md` |
| CSV format, language columns, colour codes, bracket commands, customisable localisation | `localisation/` | `references/localisation.md` |
| `.gui` layouts, `.gfx` sprite libraries, portraits, coats of arms, map data, music and sound | `interface/`, `gfx/`, `map/`, `music/`, `sound/` | `references/interface-graphics-map.md` |
| Console commands, debug mode, reload commands, log files, The Validator | — | `references/console-and-debugging.md` |

Open only the reference needed for the task.

## Working Method

1. **Locate the vanilla definition and its folder's loading behaviour before writing anything.** Determine whether the folder merges, overrides, or duplicates a repeated key (`references/mod-packaging.md`); that decision alone prevents most "my mod does nothing" and "my mod doubles everything" reports.
2. **Confirm the scope chain** before writing a command or condition. `character`, `title`/`holding`, `province`, `war`, `siege`/`flank`, `unit`, `religion`, `culture`, `society`, `artifact`, plus the special `portrait` scope. Scopes shift by event kind: targeted and title decisions put the taker in `FROM` and the target in `ROOT`, while `on_combat_pulse` and `on_battle_*` put the leading character in `ROOT` and the opposing commander in `FROM`.
3. **Prefer `is_triggered_only = yes` fired from an on_action, decision, or gatekeeper event.** Polled events run their `trigger` against every eligible character; add the filtering pre-triggers (`only_playable`, `only_rulers`, `ai`, `religion_group`, `has_dlc`) before anything else.
4. **Use `weight_multiplier` on on_action events, not `mean_time_to_happen`.** MTTH must be absent from triggered-only events and is reported as an error by The Validator when an on_action event uses it.
5. **Register everything the game must find**: namespace declaration at the top of every event file, localisation keys in every column you ship, graphic `spriteType` in an `interface/*.gfx` file, title flags in `gfx/flags/<title>.tga`, and any new folder entry in the correct top-level block.
6. **Validate in game, not by inspection**: launch with `-debug -debugscripts -scriptlog -fullhistoricalsetuplog`, use `testevent`, `event`, `run <file>.txt`, `reloadevents`, and `reloadloc`, then read `logs/error.log` and `logs/system_interface.log`.
7. **Run The Validator before playtesting** when iterating on bulk script; it catches brace errors, invalid scopes, unknown conditions, duplicate IDs, and missing localisation faster than any in-game loop.
8. **Re-verify vanilla keys against the installed build.** The wiki's `Commands` and `Conditions` tables lag behind in places; the shipped `.txt` files and The Validator are authoritative.

## Honest Limits

- Map modes, diplomatic action behaviour, and most button behaviour are hardcoded; existing elements can be moved or hidden, not repurposed.
- New `holding_types` cannot be added, and hardcoded restrictions on holdings still apply.
- `replace_path` works per folder and does not recurse into subfolders; it also destroys compatibility with every other mod and is only appropriate for total conversions.
- Duplicate `traits`, `buildings`, `societies`, `objectives`, `casus_belli`, `retinue_subunits`, and `religion_features` keys coexist rather than override, so reusing a vanilla name corrupts the entity instead of replacing it.
- Negative dates are not handled by the engine, so BC-era settings need workarounds.
- Some pre-triggers are unreliable: `is_female` raises an error (use `only_men`/`only_women`), and `in_command` is documented as buggy.
- Name weighting (`Name:Weight`) in culture name lists has been ignored since patch 2.5.
- The wiki's `Commands` and `Conditions` indexes are long but not exhaustive; the shipped `.txt` files and The Validator remain authoritative.