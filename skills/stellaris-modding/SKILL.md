---
name: stellaris-modding
description: "Use when creating or editing a Stellaris mod, or when working with its Clausewitz script (effects, triggers, scopes, conditions, variables, script values, scripted effects and triggers), mod descriptors (.mod, descriptor.mod), load order and file-override semantics (LIOS, FIOS, DUPL, MERGE), events and on_actions, decisions, buildings and districts, economies and resources, empires and governments, pops, planets, leaders, ships, starbases, armies, war and espionage, map and galaxy setup, localisation (.yml), interface (.gui, .gfx), defines, or the console and debugging tools. Covers mod folder layout, Workshop and Paradox Mods packaging, compatibility and checksum safety, and load failures. The bundled references hold the full detail and load on demand."
---

# Stellaris Modding

Apply when authoring or reviewing content for **Stellaris** (Paradox Development Studio, Clausewitz engine).

Source material: the [Stellaris Wiki](https://stellaris.paradoxwikis.com/Stellaris_Wiki) pages `Modding`, `Mods`, `Modding tutorial`, `Event modding`, `On actions`, `Effects`, `Triggers`, `Conditions`, `Scopes`, `Variables`, `Modifiers`, `Dynamic modding`, `Localisation modding`, `Interface modding`, `Map modding`, `Defines`, `Economy modding`, `AI modding`, `Building modding`, `Army modding`, `War modding`, `Anomalies modding`, `Ancestral Relics modding`, `Agenda modding`, `Bombardment Stance modding`, `Bypass modding`, `Flag modding`, `Font modding`, `Music modding`, `Portrait modding`, and `Console commands`. The wiki is version-tagged per section (most pages verified 3.0–4.2, achievements through 4.5); treat any unconfirmed detail as needing verification against the installed game files and the generated `logs/script_documentation/` dump.

## Non-Negotiable Build Rules

1. **Never edit game files.** Work only inside the mod folder; game updates and Steam file verification overwrite the installation.
2. **Mod files live in the user data directory, not Steam.** Installing into `SteamApps/common/Stellaris/mod` silently fails to load.
3. **Encoding:** script and `.mod` files UTF-8; **localisation and name-list files must be UTF-8 with BOM**, otherwise the game refuses to parse them.
4. **One default entry per key.** Stellaris resolves duplicate definitions by merge type (LIOS/FIOS/DUPL/MERGE) per `common/` subfolder; guessing causes silent overrides (`references/mod-packaging.md`).
5. **Use a unique filename prefix** equal to the mod name for every added file; never reuse a vanilla filename unless an entire-file override is intended.
6. **Achievements:** achievements cannot be earned once a console command has been used or an installed mod has altered the checksum. Any `common/`, `events/`, `localisation/`, or `interface/` change alters the checksum; pure asset replacement is the least risky category, but state it as a limitation rather than a guarantee.
7. **Keep both descriptors.** `modname.mod` links the launcher to the folder; `descriptor.mod` inside the folder is what the 2.4+ launcher and the Workshop item use.
8. **Indent with tabs and comment with `#`.** Clausewitz script is brace-structured; mismatched braces are the most frequent hard failure.
9. **Read `error.log` after every change.** A silently inert effect or trigger usually means a wrong scope or an invalid key, not a broken install.
10. **Never test a local copy alongside a published copy.** A subscribed Steam Workshop or Paradox Mods item of the mod loads as a second definition set, so local edits are merged away or shadowed and appear inert. Unsubscribe from the published item, delete its `.mod` descriptor, and start a **new game** (`references/mod-packaging.md`).

## Layout

```
Stellaris/mod/
  my_mod.mod                 # launcher descriptor for the local mod
  my_mod/
    descriptor.mod           # in-folder descriptor (required by launcher v2)
    thumbnail.png            # fixed name, >= 512x512, < 1 MB
    common/                  # scripted definitions (largest surface)
    events/                  # event files (per-namespace)
    localisation/            # <file>_l_<language>.yml (UTF-8-BOM)
    localisation/replace/    # keys here load last and win
    interface/               # *.gui layouts, *.gfx sprite libraries
    gfx/                     # .dds art, icons, models, particles
    map/                     # galaxy generation and setup scenarios
    prescripted_countries/   # pre-scripted empire setups
    flags/                   # emblem and colour definitions
    fonts/                   # fonts.asset
    music/                   # .ogg plus songs.asset / songs.txt
    sound/                   # .wav plus .asset definitions
```

A file placed at the mod-relative path of a vanilla file replaces it entirely. Prefer adding new files over copying vanilla files.

## Domain Map

| Need | Vanilla location | Reference |
|------|------------------|-----------|
| Descriptors, launcher, Workshop/Paradox Mods publishing, load order, merge semantics, compatibility | `mod/*.mod` | `references/mod-packaging.md` |
| Effects, triggers, conditions, scopes, scope chains, event targets | `common/`, `events/` | `references/scripting.md` |
| Scripted effects/triggers/localisation, variables, script values, scripted modifiers, flags | `common/scripted_*`, `common/script_values`, `common/scripted_modifiers` | `references/dynamic-scripting.md` |
| Events, namespaces, options, on_actions, anomalies, event chains | `events/`, `common/on_actions/`, `common/anomalies/` | `references/events-and-actions.md` |
| Buildings, districts, jobs, decisions, edicts, policies, resources, economies | `common/buildings`, `common/districts`, `common/pop_jobs`, `common/decisions`, `common/economic_*` | `references/economy-and-planets.md` |
| Empires, governments, civics, origins, authorities, ethics, traits, species, leaders, ascension perks, traditions, technologies, ships, starbases, armies, war, espionage, federations | `common/` | `references/empires-and-content.md` |
| Localisation, colour codes, `$`/`£`/`§`/bracket commands, scripted loc | `localisation/` | `references/localisation.md` |
| Interface `.gui`/`.gfx`, custom event windows, element types and attributes | `interface/` | `references/interface.md` |
| Galaxies, systems, planets, map setup scenarios, static maps, defines | `map/`, `common/solar_system_initializers/`, `common/defines/` | `references/map-and-defines.md` |
| Console commands, debug mode, reloads, logs, data dumps | — | `references/console-and-debugging.md` |

Open only the reference needed for the task.

## Working Method

1. **Locate the vanilla source file** and decide the merge strategy before copying anything: add a new key in a new file when the folder is LIOS, reuse the exact vanilla filename only when the entry is FIOS or needs whole-file replacement.
2. **Confirm the scope** before writing effects or triggers: `country`, `planet`, `pop`, `pop_faction`, `leader`, `fleet`, `ship`, `starbase`, `galactic_object`, `megastructure`, `army`, `species`, `federation`, `war`, `first_contact`, `spy_network`, `espionage_operation`, `archaeological_site`, `deposit`, `ambient_object`, `sector`. A scope-illegal trigger or effect writes to `error.log` and aborts the surrounding block (`references/scripting.md`).
3. **Prefer `is_triggered_only = yes` plus an on_action or a gatekeeper event.** Unconditional event polling costs CPU every tick per object; `mean_time_to_happen` is legacy and materially more expensive (`references/events-and-actions.md`).
4. **Register everything the game must find**: localisation keys in every shipped language, icon `.dds` at `gfx/interface/icons/<category>/<key>.dds`, sprite definitions in a `.gfx` file, on_actions in `common/on_actions/`, and any DLC-gated content behind a `has_dlc` check.
5. **Validate in-game, not by inspection**: launch with `-debug_mode`, use `reload <file>.gui` / `reload texture all` / `reload text`, use `run <file>.txt` for iterative script tests, then read `error.log`.
6. **Check adjacent schema** — modifiers must exist in the modifier list, on_action keys must be real, trigger names must match the installed patch, and modifier keys are often suffixes or category-bound (`country_`, `pop_`, `planet_`).

## Honest Limits

- Most GUI element types are hardcoded; only attributes of existing vanilla elements are safely modifiable. Adding or reordering elements in a vanilla window commonly crashes to desktop.
- There is no supported way to create a new top-level window: custom windows are built by reusing `custom_gui` event windows and hiding unwanted children (never deleting them).
- Map galaxies are procedurally generated from `map/setup_scenarios/` and `common/solar_system_initializers/`; radius is capped at 500 and very large galaxies degrade performance.
- Anything in `common/` may change between major patches (4.0 reworked districts, zones, and pop groups). Re-verify vanilla keys after each patch instead of trusting memory.
- The wiki's effect/trigger tables lag the installed build; `logs/script_documentation/` is authoritative.