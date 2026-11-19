---
name: eu5-modding
description: "Use when creating or editing a Europa Universalis V mod, or when working with its Jomini script (effects, triggers, scopes, iterators, variables, script values, macros, MTTH, defines), mod metadata (.metadata/metadata.json), the top folders, file and object load order, database entry modes (INJECT, REPLACE, TRY_*), events and on_actions, actions and interactions, missions, situations, disasters, resolutions, peace treaties, casus belli and wargoals, countries and country setup, cultures, religions, estates, laws, international organizations, subject types, advances, buildings and production methods, goods, pops, institutions, units, diseases, setup managers, map data and the map editor, localisation (.yml), GUI and scripted GUIs, flags and coats of arms, art, music, sound, fonts, or the console, debug mode, script_docs and error logs. Covers folder layout, Workshop and Paradox Mods packaging, and load failures. The bundled references hold the full detail and load on demand."
---

# Europa Universalis V Modding

Apply when authoring or reviewing content for **Europa Universalis V** (Paradox Development Studio / Paradox Tinto, Clausewitz engine with the Jomini scripting layer).

Source material: the [EU5 Wiki](https://eu5.paradoxwikis.com/Modding) pages `Modding`, `Mod`, `Mod structure`, `Mod compatibility`, `Setup modding`, `Effect`, `Trigger`, `Scope`, `Scope link`, `Event modding`, `On action`, `Mean time to happen`, `Modifier types`, `Modifier modding`, `Variable`, `Script value`, `Macro`, `Defines`, `Localization`, `GUI script`, `Scripted gui`, `Interface modding guide`, `Action modding`, `Disaster modding`, `Mission modding`, `Situation modding`, `Advance modding`, `Art modding`, `Building modding`, `Character modding`, `Concept modding`, `Country modding`, `Culture modding`, `Disease modding`, `Estate modding`, `Goods modding`, `Institution modding`, `International organization modding`, `Law modding`, `Pop modding`, `Religion modding`, `Subject type modding`, `Trait modding`, `Unit modding`, `War modding`, `Map modding`, `Terrain modding`, `Flag modding`, `Input action`, `Console commands`, and `Save-game editing`, plus the community project `HLJSXK/eu5-modding-project` (target layout, metadata, and observed compatibility practice). Wiki page states range from pre-release through 1.4; treat any unconfirmed detail as needing verification against the installed `game/` files, the `script_docs` dump, the `dump_data_types` dump, and `error.log`.

## Non-Negotiable Build Rules

1. **Never edit game files.** Work only inside the mod folder; patches and Steam file verification overwrite the installation.
2. **Mods live in the user data directory, not Steam.** `Documents/Paradox Interactive/Europa Universalis V/mod/` on Windows and macOS; under Proton the Linux path is `steamapps/compatdata/3450310/pfx/drive_c/users/steamuser/Documents/Paradox Interactive/Europa Universalis V/mod/`. Installing into the game directory silently fails.
3. **Three top folders, in load batches.** A mod mirrors the `game/` folder through `loading_screen/`, then `main_menu/`, then `in_game/`. `mod/TestMod/in_game/events/x.txt` is correct; `mod/TestMod/events/x.txt`, `mod/TestMod/game/in_game/...`, and `mod/TestMod/in_game/on_action/x.txt` are not.
4. **`.metadata/metadata.json` is mandatory.** No metadata folder means the game will not load the mod, however complete the content is.
5. **Encoding differs per folder.** `setup/start` files must be **UTF-8 without BOM** or their top-level functions fail to read; `setup/countries` and `setup/templates` are **UTF-8 BOM**; localisation `.yml` files must be **UTF-8 BOM** or the file is ignored entirely.
6. **Same path and filename overwrites a file whole.** Content is otherwise merged by load order, never deep-merged; prefer new, uniquely prefixed files over copies of vanilla files.
7. **`INJECT:`/`REPLACE:` work only on top-level objects** and only in folders that support them. `INJECT:` appends script rather than deep-merging, cannot reach into a sub-block, and behaves like `REPLACE:` for scripted effects and scripted triggers.
8. **Operation type outranks filename.** Conflicts resolve in the order `INJECT_OR_CREATE -> REPLACE_OR_CREATE -> TRY_INJECT -> TRY_REPLACE -> INJECT -> REPLACE`, and filename only breaks ties inside one operation type.
9. **Events never fire by themselves.** There is no event-side `mean_time_to_happen`; an event needs an on_action, a `dynamic_historical_event` block, a `trigger_event` from script, or an action. MTTH syntax survives only as weight and frequency notation.
10. **Indent with tabs and comment with `#`.** Clausewitz script is brace-structured; mismatched braces are the most frequent hard failure.
11. **Read `error.log` after every change.** An inert effect or trigger almost always means a wrong scope or an invalid key, not a broken install.

## Layout

```
Europa Universalis V/mod/
  my_mod/                          # counterpart of the game/ folder
    .metadata/
      metadata.json                # required by the launcher
      thumbnail.png                # launcher and Workshop thumbnail, < 1 MB, 512x512 recommended
    loading_screen/                # first batch: pre-menu loading screen
      common/defines/              # NCategory define overrides
      common/scripted_modifiers/
      data_binding/                # GUI macros
    main_menu/                     # second batch: main menu, mod view, multiplayer view
      localization/<language>/     # <file>_l_<language>.yml (UTF-8 BOM)
      localization/<language>/replace/   # keys here win regardless of filename
      common/flag_definitions/
      common/game_concepts/
      common/static_modifiers/
      common/modifier_type_definitions/
      common/modifier_icons/
      common/script_values/
      setup/start/                 # start managers (UTF-8, no BOM)
      setup/templates/             # reusable country setup templates (UTF-8 BOM)
    in_game/                       # third batch: everything needed to play
      common/                      # scripted type definitions (largest surface)
      events/                      # event files, subfolders allowed
      gui/                         # *.gui layouts, scripted_widgets/
      gfx/                         # .dds art, icons
      map_data/                    # locations.png, definitions.txt, location_templates.txt, ...
      setup/countries/             # country definitions (UTF-8 BOM)
```

Workshop subscriptions live in `<steam>/steamapps/workshop/content/3450310/<workshop id>`.

Canonical `common/` subfolders observed in vanilla and community mods: `actions`, `advances`, `artist_types`, `artist_work`, `auto_modifiers`, `avatars`, `building_categories`, `building_types`, `cabinet_actions`, `casus_belli`, `character_interactions`, `country_interactions`, `cultures`, `culture_groups`, `customizable_localization`, `diplomatic_costs`, `disasters`, `diseases`, `employment_systems`, `estates`, `estate_privileges`, `generic_actions`, `generic_action_ai_lists`, `gods`, `goods`, `goods_demand`, `goods_demand_category`, `government_reforms`, `government_types`, `heir_selections`, `holy_sites`, `holy_site_types`, `institutions`, `international_organizations`, `languages`, `laws`, `levies`, `missions`, `modifier_type_definitions`, `on_action`, `peace_treaties`, `pop_types`, `prices`, `production_methods`, `recruitment_method`, `religions`, `religion_groups`, `religious_aspects`, `religious_factions`, `religious_figures`, `religious_focuses`, `religious_schools`, `resolutions`, `road_types`, `scripted_effects`, `scripted_guis`, `scripted_triggers`, `script_values`, `situations`, `static_modifiers`, `subject_types`, `topography`, `town_setups`, `traits`, `trigger_localization`, `unit_abilities`, `unit_categories`, `unit_types`, `vegetation`, `wargoals`.

## Domain Map

| Need | Vanilla location | Reference |
|------|------------------|-----------|
| Metadata, install paths, top folders, load order, override and entry-mode semantics, publishing, troubleshooting | `.metadata/`, `game/` | `references/mod-packaging.md` |
| Syntax, scopes, scope links, effects, triggers, iterators, variables, script values, macros, MTTH, defines | `common/`, `loading_screen/common/defines/` | `references/scripting.md` |
| Events, namespaces, options, on_actions, situations, disasters, missions, resolutions | `events/`, `common/on_action/`, `common/situations/`, `common/disasters/`, `common/missions/`, `common/resolutions/` | `references/events-and-actions.md` |
| Generic actions, character and country interactions, cabinet actions, prices, cooldowns, action AI | `common/generic_actions/`, `common/character_interactions/`, `common/country_interactions/`, `common/cabinet_actions/`, `common/prices/` | `references/actions-and-interactions.md` |
| Setup managers, country definitions, templates, timed modifiers, development, starting wars, diplomacy, disease, colonies, exploration | `main_menu/setup/start/`, `main_menu/setup/templates/`, `in_game/setup/countries/` | `references/setup-and-history.md` |
| Map data, the map editor, locations, definitions, location templates, ports, adjacencies, heightmap, rivers, decals | `map_data/`, `gfx/map/` | `references/map-and-terrain.md` |
| Countries, governments, laws, estates, privileges, international organizations, subject types, casus belli, wargoals, peace treaties | `in_game/setup/countries/`, `common/government_types/`, `common/laws/`, `common/estates/`, `common/international_organizations/` | `references/countries-and-politics.md` |
| Goods, demand, buildings, production methods, employment, prices, pops, institutions, advances | `common/goods/`, `common/building_types/`, `common/production_methods/`, `common/pop_types/`, `common/institutions/`, `common/advances/` | `references/economy-and-pops.md` |
| Characters, cultures, languages, religions and religious content, traits, units and levies, diseases, works of art | `common/cultures/`, `common/religions/`, `common/traits/`, `common/unit_types/`, `common/diseases/` | `references/content-definitions.md` |
| `.gui` layouts, templates and types, scripted widgets, GUI script data types, localisation, flags and coats of arms, fonts, models, music, sound | `gui/`, `localization/`, `common/flag_definitions/`, `common/scripted_guis/` | `references/interface-localisation-graphics.md` |
| Debug mode, console commands, hotloading, `script_docs`, `dump_data_types`, logs, save-game editing | — | `references/console-and-debugging.md` |

Open only the reference needed for the task.

## Working Method

1. **Pick the top folder first.** Defines, scripted modifiers, static modifiers, flag definitions, concepts, and country definitions load from `loading_screen/` or `main_menu/`; gameplay script, events, GUI, and map data load from `in_game/`. A file in the wrong top folder is never read.
2. **Decide the override mechanism before writing anything.** Same path overwrites wholesale; supported folders take `INJECT:`/`REPLACE:` variants; events are first-loaded-wins; GUI types and templates are last-mod-wins; localisation needs the `replace/` folder; defines patch single keys.
3. **Confirm the scope** before writing effects or triggers: `country`, `location`, `province`, `area`, `region`, `character`, `pop`, `building`, `market`, `goods`, `war`, `culture`, `religion`, `institution`, `international_organization`, `situation`, `disaster`, `unit`, `value`, `none`. A scope-illegal effect or trigger writes to `error.log` and aborts the surrounding block.
4. **Register everything the game must find**: localisation keys in every shipped language, icons at the conventional `gfx/interface/icons/<category>/` path, GUI windows in `in_game/gui/scripted_widgets/*.txt`, on_action hooks, and setup entries for anything that must exist at game start.
5. **Verify in-game, not by inspection**: launch with `-debug_mode`, let the file watcher hotload, run `script_docs` and `dump_data_types` after a patch, then read `Documents/Paradox Interactive/Europa Universalis V/logs/error.log`.
6. **Check adjacent schema** — modifier keys must exist in `common/modifier_type_definitions`, every `culture:`, `religion:`, `government_type:`, `law_type:` reference must resolve, and setup managers are additive, so removing a vanilla entry requires a full file replacement.

## Honest Limits

- Migration logic, battle casualty logic, and map modes are hardcoded and cannot be modded.
- Setup managers are additive: entries can be added freely, but a removal needs whole-file replacement.
- `INJECT:` cannot reach into a sub-block, so types whose only useful field is nested are not injectable; duplicating a singleton block such as `allow` or `trigger` produces a "section already read earlier" error.
- Events cannot be `REPLACE:`-ed or `INJECT:`-ed. Modifying a base-game event requires a pre-alphabetically named file that redefines the event, which logs a duplicated-ID error by design, and subfolders always load after top-level event files.
- On actions accept only an additional `on_actions` block; restating `trigger` or `effect` errors and overwrites the vanilla block.
- GUI `type` and `template` definitions are last-mod-wins, not filename-wins; `types` containers have no overwrite logic at all.
- Localisation keys do not overwrite later-loaded keys by default and files are read in reverse alphabetical order, so only `localization/<language>/replace/` reliably overrides vanilla text.
- Start-setup values are approximations: pop counts, development, resistance, and currency are re-derived by the game after load.
- Float literals are truncated to 5 decimal places, `min` is the lower clamp and `max` the upper clamp, and an `ordered_*` iterator without an explicit `max` returns one scope, not all of them.
- Wiki coverage is uneven: `Interface modding`, `Music modding`, `Sound modding`, `AI modding`, `Model modding`, `Graphical asset modding`, `Font modding`, `Map mode modding`, `Checksum`, and `Mod troubleshooting` are absent or stubs. When the wiki is silent, read the shipped files and the `script_docs` / `dump_data_types` output instead of guessing.