# Mod Packaging, Metadata, Load Order, and Override Semantics

## Paths

| Purpose | Path |
|---------|------|
| Mod folder (Windows) | `%USERPROFILE%\Documents\Paradox Interactive\Victoria 3\mod\` |
| Mod folder (macOS) | `~/Documents/Paradox Interactive/Victoria 3/mod/` |
| Mod folder (GNU/Linux) | `~/.local/share/Paradox Interactive/Victoria 3/mod/` |
| Logs | `<user data>/Victoria 3/logs/error.log` |
| Generated documentation | `<user data>/Victoria 3/docs/` |
| Settings | `<user data>/Victoria 3/pdx_settings.json` |
| Game installation | `<steam>/steamapps/common/Victoria 3/game/` |
| Steam Workshop content | `<steam>/steamapps/workshop/content/529340/<workshop id>` |
| Paradox Mods download | Inside the user `mod/` folder, named `PDX_<mod id>` |

Never install into the game directory; Victoria 3 will not load it from there.

**Non-ASCII paths break loading.** If the Windows account name contains accented or non-Latin characters, the whole `Documents/Paradox Interactive/Victoria 3` path inherits them and affected files silently fail with `[virtualfilesystem.cpp:562]: Could not create lexer from file due to 'fopen() failed: 2'`. Fix by editing `Steam/steamapps/common/Victoria 3/launcher/launcher-settings.json` and changing `"gameDataPath"` to an ASCII path such as `"C:/Paradox Interactive/Victoria 3"`; the mod folder then becomes `<that path>/mod`.

Folder and file names are case-sensitive on Linux and macOS. Match vanilla path case exactly.

## Mod Skeleton

```
mod/
  my_mod/                        # counterpart of Victoria 3/game
    .metadata/
      metadata.json              # required — without it nothing loads
      thumbnail.png              # optional launcher thumbnail
    common/
    events/
    localization/
    map_data/
    gui/
    gfx/
```

There is no outer `.mod` descriptor file. Victoria 3 identifies a mod solely by the `.metadata` folder, unlike CK3, Stellaris, and Imperator.

Create the skeleton from the launcher (**Add more mods**), or clone the Victoria 3 Modding Co-op template, so encoding and registration are correct from the start.

## `metadata.json`

Located at `<mod>/.metadata/metadata.json`. JSON, and comments in the wiki sample are illustrative only — real files must be valid JSON.

| Key | Notes |
|-----|-------|
| `name` | Display name in the launcher |
| `id` | Unique, stable identifier; reverse-domain notation recommended (`com.github.mymod`). Must never change: relationships and updates reference it. Do not include a version number |
| `version` | Mod version; semantic versioning is understood, other schemes are unreliable |
| `game_id` | Always `"victoria3"` |
| `supported_game_version` | Target game version; supports `*` and a trailing `+` for "or higher" |
| `short_description` | Short launcher text |
| `tags` | Up to 5 local categories; must be re-specified at upload |
| `relationships` | Array of `{ rel_type, id, display_name, resource_type, version }` |
| `game_custom_data` | Engine data; `multiplayer_synchronized` boolean |

`rel_type` values: `dependency`, `incompatible_with`, `load_before`, `load_after`. `resource_type` is currently `mod` only; `dlc` is being considered. `version` uses the same globbing as `supported_game_version`; use `"*"` if indifferent.

`thumbnail.png` sits next to `metadata.json` inside `.metadata/`.

## Folder Structure Rules

The mod folder mirrors `Victoria 3/game` one-for-one. To add a decision, the only valid path is:

```
<mod>/common/decisions/<file>.txt
```

These all fail silently:
- `<mod>/game/common/decisions/` (extra level)
- `<mod>/common/<file>.txt` (missing level)
- `<mod>/decisions/` (missing `common`)

Most folders are plural (`buildings`, `laws`, `decisions`); the notable exception is `common/technology`. `common/history` and `events` accept arbitrarily named subfolders for organisation; subfolders load after the files in the parent folder.

## File Loading Order

All files load in ASCII order regardless of whether they come from the base game or a mod: `00_foo.txt` before `01_bar.txt`. Subfolder files load after parent-folder files, so `events/zz_example.txt` loads before `events/example/00_example.txt`.

Defined game objects load in definition order, which means filenames affect only the visual ordering of objects in screens, not their merges.

## Override Mechanisms

### Direct file overwrite

A file at the same relative path with the same filename replaces the vanilla file entirely, as if the other files did not exist. A mod lower in the playset wins over a mod higher in the playset. Prefer new, uniquely prefixed files.

### `INJECT` / `REPLACE` keywords

Only valid for top-level blocks. Both error if the target object does not exist.

| Keyword | Behaviour |
|---------|-----------|
| `INJECT:` | Appends the block to the existing definition |
| `REPLACE:` | Replaces the definition |
| `TRY_INJECT:` | As `INJECT:`, no error when the object is absent |
| `TRY_REPLACE:` | As `REPLACE:`, no error when the object is absent |
| `INJECT_OR_CREATE:` | Appends, creating the object when absent |
| `REPLACE_OR_CREATE:` | Replaces, creating the object when absent |

```
INJECT:building_example = {
    production_method_groups = {
        pmg_foo
    }
}
```

Invalid — the keyword must be at the top level:
```
building_example = {
    INJECT:production_method_groups = { pmg_foo }
}
```

Processing order is fixed and independent of filename:
`INJECT_OR_CREATE` → `REPLACE_OR_CREATE` → `TRY_INJECT` → `TRY_REPLACE` → `INJECT` → `REPLACE`.

Filenames resolve conflicts only between entries using the same keyword. A `REPLACE:` therefore always beats a `REPLACE_OR_CREATE:` of the same object, and any inject is lost to a later `REPLACE:`.

`INJECT:` cannot reach into a sub-block. Injecting a block that already exists (`is_visible`, most trigger and effect blocks) fails; injecting one that does not exist works. `INJECT:` on scripted effects and scripted triggers behaves like `REPLACE:` and overwrites them.

Injecting a repeatable block appends a second copy of the block rather than merging into the first, so a repeated `wargoal_scores = { d = { ... } }` will not be merged with the existing `wargoal_scores`.

### Implicit replace

Folders without `INJECT`/`REPLACE` support replace whole objects: the last definition of the same key wins. Do not mix approaches — implicit replacement does not work inside keyword-capable folders.

## Folder Support for `INJECT` / `REPLACE`

Supported (non-exhaustive): `common/ai_strategies`, `common/building_groups`, `common/buildings`, `common/character_interactions`, `common/character_templates`, `common/character_traits`, `common/country_creation`, `common/country_definitions`, `common/country_formation`, `common/cultures`, `common/decisions`, `common/decrees`, `common/diplomatic_actions`, `common/diplomatic_plays`, `common/discrimination_trait_groups`, `common/discrimination_traits`, `common/flag_definitions`, `common/game_concepts`, `common/goods`, `common/government_types`, `common/geographic_regions`, `common/ideologies`, `common/institutions`, `common/interest_group_traits`, `common/interest_groups`, `common/journal_entries`, `common/journal_entry_groups`, `common/law_groups`, `common/laws`, `common/modifier_type_definitions`, `common/objectives`, `common/parties`, `common/political_lobbies`, `common/political_movements`, `common/pop_needs`, `common/pop_types`, `common/power_bloc_identities`, `common/power_bloc_principles`, `common/production_method_groups`, `common/production_methods`, `common/religions`, `common/scripted_buttons`, `common/scripted_guis`, `common/scripted_lists`, `common/scripted_modifiers`, `common/scripted_progress_bars`, `common/static_modifiers`, `common/strategic_regions`, `common/subject_types`, `common/technology`, `common/terrain`, `common/treaty_articles`, `common/war_goal_types`, and several `gfx/map/` and `gfx/portraits/` folders.

`REPLACE` only: `common/script_values`, `common/scripted_effects`, `common/scripted_rules`, `common/scripted_triggers`.

Not supported — use direct overwrite or implicit replace: `common/history/*`, `events/`, `localization/`, `gui/`, `common/defines/`, `common/on_actions/`, `map_data/`.

## Exceptions and Special Cases

| Area | Behaviour |
|------|-----------|
| `gui/` types and templates | First loaded **wins**; a later definition is ignored. The `types` container name is not unique and has no overwrite logic at all |
| `events/` | First loaded wins (opposite of other definitions). Subfolders load after parent files, so modding vanilla events from a subfolder is unreliable |
| `common/defines/` | Per-define replacement: restating a category block changes only the listed defines |
| `common/on_actions/` | Only additional `on_actions` and `events` entries are appended; changing `trigger` or `effect` requires replacing the whole file |
| `localization/` | Keys merge; use `localization/<language>/replace/` to override vanilla keys safely |

## Compatibility Techniques

- **Minimal footprint.** Never restate an object you do not intend to change; prefer `INJECT:` over `REPLACE:` and a new file over a copied vanilla file.
- **Add, do not copy.** A uniquely named file in the right folder loads after vanilla files in most implicit-replace folders.
- **Chain on actions.** From a vanilla on_action, call a uniquely named on_action of your own; never restate the vanilla one.
- **DLC gating.** Content that replicates DLC features must be wrapped in `has_dlc_feature = ...`; mods cannot unlock DLC content.
- **Compatibility patches** belong in a separate mod loaded after both parents, never inside either parent.

## Publishing

- **Steam Workshop** (`steamcommunity.com/app/529340/workshop/`): upload from the Paradox launcher. Subscribers get the files in `steamapps/workshop/content/529340/<id>`.
- **Paradox Mods** (`mods.paradoxplaza.com/games/victoria3`): upload from the launcher or the web; downloaded content appears in the user `mod/` folder as `PDX_<mod id>`.
- **Manual distribution**: archive the mod folder itself (the folder holding `.metadata/`). Installing means extracting it into `mod/` and adding it to a playset with **Add more mods**.
- Re-specify tags at upload; local `tags` do not guarantee correct backend categorisation.
- Remove any previous installation before installing a new version — the game loads every file present, so stale renamed files conflict.

## Troubleshooting

| Symptom | Cause |
|---------|-------|
| Mod listed in the launcher but no effect | Wrong folder depth, misspelled folder, or a `.txt`/`.yml` file saved without a BOM |
| Whole mod absent from the launcher | Missing or malformed `.metadata/metadata.json`; non-ASCII path; wrong `game_id` |
| Some files have no effect, `error.log` reports a lexer/`fopen` failure | Permissions, or non-ASCII characters in the path |
| A specific object refuses to change | Folder needs `REPLACE:` rather than a plain redefinition, or the object is FIOS (`gui` types, `events`) |
| Two mods fight over an object | Both use `REPLACE:`; the later filename wins — build a patch mod loaded after both |
| A patch changed a key and the mod errors | Regenerate `script_docs` and compare against the installed build |
| Vanilla file works alone, fails with another mod | Both overwrite the same vanilla filename; rename one and switch to `INJECT:` |