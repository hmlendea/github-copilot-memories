---
name: imperator-rome-modding
description: Use when creating or editing an Imperator Rome mod, or when working with its Clausewitz/Jomini script (effects, triggers, scopes, variables, script values), mod descriptors (.mod, descriptor.mod), setup files (countries, characters, provinces, cultures, religions, deities, heritages), events, decisions, ideas, units, combat tactics, governor policies, localisation (.yml), GUI (.gui), coat of arms, map data, defines, or the in-game console and debugging tools. Covers mod folder layout, packaging and publishing through the Paradox launcher, checksum and ironman safety, and troubleshooting load failures.
---

# Imperator: Rome Modding

Apply when authoring or reviewing content for **Imperator: Rome** (Paradox Development Studio, Clausewitz engine with the Jomini scripting layer).

Source material: the [Imperator Wiki](https://imperator.paradoxwikis.com/Imperator_Wiki) pages `Modding`, `Mods`, `Mod_file`, `Effects`, `Triggers`, `Scopes`, `Variables`, `Script Values`, `Event modding`, `Decision modding`, `Country creation`, `Character modding`, `Culture modding`, `Religion modding`, `Government modding`, `Governor policy modding`, `Idea modding`, `Unit modding`, `Combat tactics modding`, `Province setup`, `Map modding`, `Localisation`, `GUI modding`, `Coat of arms modding`, `Genes modding`, `Defines`, and `Console commands`. Individual wiki pages are marked as last verified for game versions 1.0–1.5; treat any unconfirmed detail as needing verification against the installed game files.

## Non-Negotiable Build Rules

1. **Never edit game files.** Work only inside the mod folder; game updates overwrite `game/` and the user's install may be verified/repaired.
2. **Mod files live in the user data directory, not Steam.** Wrong location is a common "mod does not load" cause.
3. **Encoding:** script and text files UTF-8 or UTF-8-BOM; **localisation files must be UTF-8-BOM** (other encodings produce a game warning or broken glyphs).
4. **Achievements and ironman:** any script/GUI change alters the checksum and disables achievements; loading an ironman save with a checksum-changing mod can corrupt it irreversibly. Only texture, font, and music replacements are checksum-safe. The authoritative list is `checksum_manifest.txt` in the game folder.
5. **Do not ship a local copy of a Steam Workshop mod** with the same content; delete or move the local folder when testing the Workshop version.
6. **Keep `descriptor.mod`.** The launcher writes it on first upload and uses it to update the Workshop item; deleting it orphans the published mod.
7. **Indent consistently and comment with `#`.** Clausewitz script is brace-structured; mismatched braces are the most frequent hard failure.
8. **Always read `error.log`** after every script change; a silent script error usually means a wrong trigger, effect, or scope, not a broken install.

## Layout

```
Imperator/mod/
  my_mod.mod                 # descriptor for a local mod
  my_mod/
    descriptor.mod           # written by launcher on first upload
    thumbnail.png            # >= 200x200, optional but recommended
    common/                  # scripted definitions
    events/                  # event files
    decisions/               # decision files
    localization/            # <file>_l_<language>.yml (UTF-8-BOM)
    gui/                     # .gui layout files
    gfx/                     # .dds textures, icons, interface art
    setup/                   # countries, provinces, characters
    map/                     # map data, roads, ports, adjacencies
    localization/replace/    # files that must load last and override vanilla
```

A file at `my_mod/gui/ingame_topbar.gui` replaces the vanilla `game/gui/ingame_topbar.gui` of the same path. Both `localization` (Imperator's spelling) and the vanilla file layout must be matched exactly.

## Domain Map

| Need | Vanilla location | Reference |
|------|------------------|-----------|
| Mod descriptor, launcher, publishing, load order, install paths | `mod/*.mod` | `references/mod-packaging.md` |
| Effects, triggers, scopes, variables, script values, scripted effects | `common/`, `events/` | `references/scripting.md` |
| Events and decisions | `events/`, `decisions/` | `references/events-and-decisions.md` |
| Countries, characters, cultures, religions, deities, heritages, ideas, coat of arms | `setup/`, `common/` | `references/setup-and-entities.md` |
| Localisation, colour codes, text icons, hover links | `localization/` | `references/localisation.md` |
| UI layout, GUI editor, textures, scripted GUIs | `gui/`, `gfx/` | `references/gui.md` |
| Map, provinces, roads, clouds, buildings, heightmaps | `map/`, `map_data/`, `setup/provinces/` | `references/map-and-world.md` |
| Console, debug mode, reload commands, logging, data dumps | — | `references/console-and-debugging.md` |

Open only the reference needed for the task.

## Working Method

1. **Locate the vanilla source file** and copy it into the mod at the identical relative path; extend rather than recreate whenever the format allows merging (localisation, defines, script values).
2. **Confirm the scope** before writing effects or triggers: country, character, province, state, governorship, region, area, unit, subunit, pop, party, family. An effect or trigger used in the wrong scope silently does nothing (`references/scripting.md`).
3. **Register everything that needs registration**: new country tags in `countries.txt`, new provinces in the map/province setup, new localisation keys in every shipped language, new files referenced from the correct top-level block.
4. **Validate in-game, not by inspection**: launch with `-debug_mode -develop`, use `reload gui` / `reload texture` for UI, restart for map or setup changes, then read `error.log`.
5. **Check adjacent schema** — modifiers must exist in the modifier list, triggers and effects must exist and be scope-legal, and modifier keys are usually suffixes (`_modifier`, `local_`, `global_`).

## Honest Limits

- Mapmodes, diplomatic actions, and new hotkeys are hardcoded and cannot be modded.
- GUI cannot make two windows visible simultaneously, cannot display data that was not pre-configured for that window, and cannot add hotkeys.
- A custom saved scope persists only within an uninterrupted effect chain; it is lost outside it.
- New defines cannot be added; only existing ones can be overridden.
- Wiki coverage is uneven (several pages are stubs or marked expand/outdated). When the wiki is silent, read the decompiled or shipped `.txt` files and the `script_docs` output instead of guessing.