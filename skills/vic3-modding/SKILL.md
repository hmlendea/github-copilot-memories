---
name: vic3-modding
description: Use when creating or editing a Victoria 3 mod, or when working with its Jomini script (effects, triggers, scopes, event targets, script values, variables, scripted effects and triggers), mod metadata (.metadata/metadata.json), load order and override semantics (INJECT, REPLACE, TRY_*, *_OR_CREATE, implicit replace), events, on_actions, decisions, journal entries, scripted buttons and progress bars, countries, laws, interest groups, parties, institutions, decrees, power blocs, diplomacy, political movements, buildings and production methods, goods, pops and professions, technologies, cultures, religions and discrimination traits, history and state setup, map and state regions, localisation (.yml), GUI script, scripted GUIs, coat of arms and flags, 3D models, FMOD sound banks, or the console and debugging tools. Covers mod folder layout, launcher and Workshop/Paradox Mods publishing, compatibility, and troubleshooting load failures.
---

# Victoria 3 Modding

Apply when authoring or reviewing content for **Victoria 3** (Paradox Development Studio, Clausewitz engine with the Jomini scripting layer).

Source material: the [Victoria 3 Wiki](https://vic3.paradoxwikis.com/Victoria_3_Wiki) pages `Modding`, `Mod`, `Mod structure`, `Mod compatibility` (redirected from `Mod files load order`), `Defines`, `Effect`, `Trigger`, `Scope`, `Event target`, `Data types` (GUI script), `Script value`, `Macro`, `On actions`, `Event modding`, `Decision modding`, `Journal entry modding`, `Scripted gui`, `Localization`, `Script localization`, `Interface modding`, `History modding`, `Map modding`, `State modding guide`, `New country modding`, `Country modding`, `Law modding`, `Interest group modding`, `Character modding`, `Institution modding`, `Decree modding`, `Diplomacy modding`, `Power bloc modding`, `Political movement modding`, `Goods modding`, `Pop modding`, `Building modding`, `Technology modding`, `Culture modding`, `Religion modding`, `Discrimination trait modding`, `Flag modding`, `Graphical asset modding`, `Model modding`, `Sound modding`, `AI modding`, `Console commands`, and `Scripted test`. Wiki pages are last-verified for versions 1.8–1.13; treat any unconfirmed detail as needing verification against the installed game files and the `script_docs` dump.

## Non-Negotiable Build Rules

1. **Never edit game files.** Work only inside the mod folder; game updates and Steam file verification overwrite `Victoria 3/game`.
2. **Mods live in the user data directory, not Steam.** `Documents/Paradox Interactive/Victoria 3/mod` (Windows and macOS) or `~/.local/share/Paradox Interactive/Victoria 3/mod` (Linux). Installing under the game directory silently fails to load.
3. **The mod folder mirrors `Victoria 3/game` exactly.** `common/decisions/`, not `game/common/decisions/`, `common/decisions/`'s parent, or `decisions/`. A wrong level or a misspelled folder is not read at all.
4. **`.metadata/metadata.json` is mandatory.** Without it the launcher will not load the mod, however complete the content is.
5. **Encoding:** all `.txt` and `.yml` files must be **UTF-8 with BOM**. Localisation filenames must end in `_l_<language>` with a lowercase ell: `mymod_decisions_l_english.yml`.
6. **Never rely on implicit replacement inside `INJECT`/`REPLACE` folders.** Those types error out instead of overriding; outside them, a redefinition silently replaces the whole object.
7. **Do not copy a vanilla filename unless a whole-file replacement is intended.** New, uniquely prefixed files load after base game files and do not collide with other mods.
8. **Events never fire by themselves.** Victoria 3 has no mean-time-to-happen polling: every event must be raised by an effect, an on_action, a journal entry, a decision, or another event.
9. **Achievements are not disabled by mods in Victoria 3**, but a debug-mode session and console use are a separate matter; state this rather than promising achievement compatibility.
10. **Indent with tabs and comment with `#`.** Clausewitz script is brace-structured; mismatched braces are the most frequent hard failure.
11. **Read `error.log` after every change.** A silently inert effect or trigger almost always means a wrong scope or an invalid key, not a broken install.

## Layout

```
Victoria 3/mod/
  my_mod/                          # the mod folder itself (counterpart of game/)
    .metadata/
      metadata.json                # required by the launcher
      thumbnail.png                # optional launcher thumbnail
    common/                        # scripted type definitions (largest surface)
    events/                        # event files, subfolders allowed
    common/history/                # starting game state, subfolders allowed
    map_data/
      state_regions/               # state regions and their provinces
      provinces.png                # province map (only for new provinces)
    localization/
      english/                     # <file>_l_english.yml
      english/replace/             # keys here win regardless of filename
      <language>/                  # braz_por, french, german, polish, russian,
                                   # spanish, japanese, simp_chinese, korean, turkish
    gui/                           # *.gui layout and type files
    gfx/                           # .dds art, icons, coat of arms parts, models
    sound/banks/                   # FMOD .bank files
    tools/scripted_tests/          # optional automated state checks
```

Workshop subscriptions live in `<steam>/steamapps/workshop/content/529340/<workshop id>`; Paradox Mods downloads land inside the user `mod/` folder named `PDX_<mod id>`.

## Domain Map

| Need | Vanilla location | Reference |
|------|------------------|-----------|
| Metadata, launcher, install paths, load order, INJECT/REPLACE semantics, publishing, troubleshooting | `.metadata/`, `mod/` | `references/mod-packaging.md` |
| Syntax, effects, triggers, scopes, event targets, variables, script values, macros, scripted lists | `common/`, `events/` | `references/scripting.md` |
| Events, on_actions, decisions, journal entries, scripted buttons, progress bars, objectives | `events/`, `common/on_actions`, `common/decisions`, `common/journal_entries` | `references/events-and-actions.md` |
| Countries, laws, interest groups, parties, institutions, decrees, power blocs, diplomacy, political movements, AI | `common/country_definitions`, `common/laws`, `common/interest_groups`, `common/ai_strategies` | `references/politics-and-economy.md` |
| Buildings, building groups, production methods, goods, pops, professions, technologies, cultures, religions, discrimination traits, modifiers | `common/buildings`, `common/production_methods`, `common/goods`, `common/pops` | `references/pops-and-buildings.md` |
| History files, state regions, strategic regions, map editor, new countries and states | `common/history/`, `map_data/state_regions/` | `references/history-and-map.md` |
| Localisation syntax, formatting, text icons, data functions, concepts, customizable and script localisation | `localization/`, `common/customizable_localization`, `common/effect_localization` | `references/localisation.md` |
| GUI script, templates and types, scripted widgets, scripted GUIs, data functions | `gui/`, `common/scripted_guis` | `references/interface.md` |
| Coat of arms and flags, textures, 3D models, FMOD sound banks | `common/coat_of_arms`, `common/flag_definitions`, `gfx/`, `sound/` | `references/graphics-and-audio.md` |
| Debug mode, console commands, hotloading, `script_docs`, logs, scripted tests | — | `references/console-and-debugging.md` |

Open only the reference needed for the task.

## Working Method

1. **Decide the override mechanism before writing anything.** Injectable types take `INJECT:` (append) or `REPLACE:` (replace); implicitly replaced types (`country_definitions`, `cultures`, `coat_of_arms`, …) need the whole object restated; events and GUI types are first-loaded-wins (`references/mod-packaging.md`).
2. **Confirm the scope** before writing effects or triggers: `country`, `state`, `state_region`, `character`, `interest_group`, `pop`, `building`, `market`, `market_goods`, `journal_entry`, `law`, `power_bloc`, `war`, `diplomatic_play`, `front`, `treaty`, `none`. A scope-illegal effect writes to `error.log` and aborts the surrounding block (`references/scripting.md`).
3. **Gate events behind an explicit trigger.** Because nothing polls events, an event without a trigger fires wherever the raising effect runs, including for every country the raising on_action visits (`references/events-and-actions.md`).
4. **Register everything the game must find**: localisation keys in every shipped language, icons at the expected `gfx/interface/icons/<category>/` path, journal entry groups, on_action chains, scripted buttons and progress bars in their own `common/` folders.
5. **Verify in-game, not by inspection**: launch with `-debug_mode`, rely on hotloading for `.gui` and most script files, run `script_docs` and `DumpDataTypes` after a patch, then read `error.log`.
6. **Check adjacent schema** — modifier keys must exist in `common/modifier_type_definitions`, every `law_type:`, `cu:`, `rel:`, `ig:`, `je:`, `s:` reference must resolve, and `add_modifier` must name a defined static modifier.

## Honest Limits

- Migration logic, battle casualty logic, and map modes are hardcoded and cannot be modded.
- Events cannot be `INJECT`-ed or `REPLACE`-d; the first definition loaded wins, and `events/` subfolders always load after top-level event files.
- `INJECT:` cannot reach into a sub-block, and it silently behaves like `REPLACE:` for scripted effects and scripted triggers.
- On actions only accept additional `on_actions` and `events` entries; changing an existing `trigger` or `effect` requires replacing the whole file.
- GUI `type` and `template` definitions are first-loaded-wins and cannot be overwritten; only `types` containers can be redefined.
- Localisation files without a BOM are ignored entirely, and locale folders use `localization` with a z.
- Wiki coverage is uneven — `Interface modding` and `GUI script` are stubs, and several definition pages are marked expand or outdated. When the wiki is silent, read the shipped `.txt` files and the `script_docs` output instead of guessing.