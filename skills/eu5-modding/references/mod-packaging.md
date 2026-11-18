# Mod Packaging, Metadata, Load Order, and Override Semantics

## Paths

| Purpose | Path |
|---------|------|
| Mod folder (Windows/macOS) | `%USERPROFILE%/Documents/Paradox Interactive/Europa Universalis V/mod/` (`~/Documents/Paradox Interactive/Europa Universalis V/mod/` on macOS) |
| Mod folder (Proton/Steam on Linux) | `steamapps/compatdata/3450310/pfx/drive_c/users/steamuser/Documents/Paradox Interactive/Europa Universalis V/mod/` |
| Logs | `<user data>/Europa Universalis V/logs/error.log` |
| Generated documentation | `<user data>/Europa Universalis V/docs/` |
| Settings | `<user data>/Europa Universalis V/pdx_settings.json` |
| Game installation | `<steam>/steamapps/common/Europa Universalis V/game/` |
| Steam Workshop content | `<steam>/steamapps/workshop/content/3450310/<workshop id>` |

Never install into the game directory; EU5 will not load the mod from there.

**Non-ASCII paths break loading.** If the Windows account name contains accented or non-Latin characters, the whole `Documents/Paradox Interactive/Europa Universalis V` path inherits them and affected files silently fail with `[virtualfilesystem.cpp:562]: Could not create lexer from file due to 'fopen() failed: 2'`. Fix by editing `<install>/launcher/launcher-settings.json` and changing `"gameDataPath"` to an ASCII path such as `"C:/Paradox Interactive/Europa Universalis V"`; the mod folder then becomes `<that path>/mod`.

Folder and file names are case-sensitive on Linux and macOS. Match vanilla path case exactly.

## Mod Skeleton

```
mod/
  my_mod/                          # counterpart of the game/ folder
    .metadata/
      metadata.json                # required — without it nothing loads
      thumbnail.png                # optional launcher thumbnail, < 1 MB, 512x512
    loading_screen/                # first batch: pre-menu loading screen
    main_menu/                     # second batch: main menu, mod view, multiplayer
    in_game/                       # third batch: gameplay files
```

There is no outer `.mod` descriptor file. EU5 identifies a mod solely by the `.metadata` folder, unlike CK3, Stellaris, and Imperator.

Create the skeleton from the launcher (**Add more mods**), or clone the EU5 Modding Co-op template, so encoding and registration are correct from the start.

## `metadata.json`

Located at `<mod>/.metadata/metadata.json`. JSON; comments in examples are illustrative only — real files must be valid JSON.

```json
{
  "name": "My Mod",                         // display name in the launcher
  "id": "com.example.mymod",                // unique, stable identifier; reverse-domain recommended
  "version": "1.0.0",                       // semantic versioning understood
  "game_id": "eu5",
  "supported_game_version": "1.4.*",        // use "*" wildcard freely
  "short_description": "Brief description",
  "tags": ["Balance", "Trade"],             // up to 5 local categories
  "relationships": [
    {
      "rel_type": "dependency",              // or "incompatible_with", "load_before", "load_after"
      "id": "community_mod_framework",
      "display_name": "Community Mod Framework",
      "resource_type": "mod",                // "dlc" considered but not yet available
      "version": "2.*"
    }
  ],
  "game_custom_data": {
    "multiplayer_synchronized": true        // only boolean currently used
  }
}
```

`rel_type` values: `dependency`, `incompatible_with`, `load_before`, `load_after`. `resource_type` is currently `mod` only. `version` uses the same globbing as `supported_game_version`; use `"*"` if indifferent.

## Top-Folder Load Batches

EU5 loads files in three sequential batches through top folders inside the mod. A file in the wrong top folder is never read.

| Batch | Top Folder | Loaded When |
|-------|------------|-------------|
| 1 | `loading_screen/` | Showing the Paradox/Tinto splash screen; pre-menu |
| 2 | `main_menu/` | Main menu, mod view, multiplayer lobby |
| 3 | `in_game/` | In the lobby and during the entire game session |

The folder structure inside each top folder mirrors `game/<top_folder>/`.

### `loading_screen/`
- `common/defines/` — define overrides (`NCategory` blocks); only single-key patches here
- `common/scripted_modifiers/`
- `data_binding/` — GUI macro definitions

### `main_menu/`
- `localization/<language>/` — `.yml` files (UTF-8 BOM)
- `localization/<language>/replace/` — keys here win regardless of filename
- `common/flag_definitions/`
- `common/game_concepts/`
- `common/static_modifiers/`
- `common/modifier_type_definitions/`
- `common/modifier_icons/`
- `common/script_values/`
- `setup/start/` — start managers (UTF-8, **without BOM**)
- `setup/templates/` — reusable country setup templates (UTF-8 **with BOM**)

### `in_game/`
- `common/` — scripted type definitions (largest surface)
- `events/` — event files; subfolders allowed; subfolders always load after top-level files
- `gui/` — `.gui` layouts; `scripted_widgets/` for scripted UI
- `gfx/` — `.dds` art, icons, flag parts
- `map_data/` — locations.png, definitions.txt, location_templates.txt, ports.csv, adjacencies.csv, default.map, rivers.png, decals
- `setup/countries/` — country definitions (UTF-8 **with BOM**)

## Encoding Rules

| Folder / File | Encoding |
|---------------|----------|
| `main_menu/setup/start/` files | UTF-8 **without** BOM |
| `in_game/setup/countries/` and `main_menu/setup/templates/` | UTF-8 **with** BOM |
| Localisation `.yml` files | UTF-8 **with** BOM; filename must end in `_l_<language>` (lowercase L) |
| Everything else (.txt, .gui, etc.) | UTF-8 (BOM optional; without BOM is fine) |

A file with the wrong encoding is silently ignored or fails to parse.

## File and Object Load Order

1. **Files**: ASCII order by filename within each folder. Parent-folder files load before files in subfolders.
2. **Mods**: Launcher playlist order (lower in the list = later).
3. **Database entry modes**: When multiple files edit the same top-level object via `INJECT:` / `REPLACE:` variants, operation type is processed **before** filename. Priority order (earliest → latest):
   ```
   INJECT_OR_CREATE → REPLACE_OR_CREATE → TRY_INJECT → TRY_REPLACE → INJECT → REPLACE
   ```
   Filename order breaks ties only within the same operation type.
3. **Exact-path overwrite**: A mod file at the same relative path and filename as vanilla wins; if multiple mods provide the same path, the mod lower in the playlist wins. The winning file is used **exclusively** — no merge.

## Override Semantics by Folder Category

| Category | Examples | Override Rules |
|----------|----------|----------------|
| INJECT/REPLACE folders (top-level object) | `common/building_types/`, `common/cultures/`, `common/laws/`, `common/on_action/`, `common/scripted_effects/`, `common/scripted_triggers/`, `common/script_values/`, `common/static_modifiers/`, `common/auto_modifiers/` | Same filename wins; entry modes (`INJECT:`, `REPLACE:`, variants) work on top-level blocks; `INJECT:` appends rather than deep-merges; `INJECT:` on scripted effects/triggers behaves like `REPLACE:` |
| First-loaded-wins | `events/` (subfolders after top-level) | Duplicate event IDs: the file that loads first alphabetically wins; modifying a vanilla event requires a new file alphabetically before the vanilla one |
| Last-mod-wins (playlist) | `gui/` type and template definitions (`type X = ...`, `template Y = ...`) | File order irrelevant; mod lower in the playlist wins |
| Whole-file only | `common/defines/` (in `loading_screen/`), `setup/start/`, `setup/countries/`, `setup/templates/`, `common/flag_definitions/`, `common/game_concepts/`, `map_data/` | Only exact-path overwrite works; repick entire file to modify |
| Localisation `replace/` | `localization/<language>/replace/` | Keys here win over any filename-order key; use this for single-key overrides |
| Defines | `loading_screen/common/defines/` | Single-key patching (`NCategory = { DEFINE = value }`) without replacing the whole file; multiple mods patching the same define: last loaded filename wins |

## `INJECT:` / `REPLACE:` Pitfalls

- **Top-level only**: You cannot write `building_example = { INJECT:possible_production_methods = { foo } }`. The engine errors unless the keyword is on the top-level block.
- **No deep merge**: `INJECT:` appends the whole block. If the target already has an `allow = { ... }`, adding another `allow = { ... }` produces `Trigger section already read earlier`. Use `REPLACE:` on the verified complete object instead.
- **Scripted effects/triggers**: `INJECT:` behaves exactly like `REPLACE:` for these; do not expect appends.
- **Static modifiers**: Numeric modifier entries are **additive** across mods. When changing an existing modifier, prefer `TRY_INJECT:` containing only `desired final value - verified vanilla value`; omit unchanged fields.
- **Price objects**: Scalar resource fields (`gold`, etc.) **replace** rather than add on repeated injection. If two mods inject `gold = -10` the final value is `-10`, not the sum.

## Publishing

- **Steam Workshop**: Run `window.workshopUpload.uploadMod(...)` from the in-game console, or use the `PDX Workshop Manager` tool.
- **Paradox Mods**: Manual upload through the website; the launcher downloads into the user mod folder as `PDX_<mod id>`.
- **Metadata changes**: Bump the version, keep the `id` stable, and re-upload. If `id` changes, the mod is treated as a brand-new item.

## Troubleshooting Load Failures

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Mod listed in launcher but no content | Missing `.metadata/metadata.json` | Add metadata file |
| `Could not create lexer... fopen() failed: 2` in `error.log` | Non-ASCII user folder path on Windows | Move user data path via `launcher-settings.json` |
| File silently ignored | Wrong encoding (localisation without BOM, `setup/start/` with BOM) | Re-save with correct encoding |
| Modded event never fires | Duplicate event ID; later-loaded file won | Name the mod file alphabetically before vanilla (`0000_modded_...`) |
| GUI type not applied | Mod is not lowest in playlist for GUI `type`/`template` | Move mod down in playlist; `types` containers have no overwrite logic |
| Localisation key shows raw ID | Missing key in this language or wrong filename suffix | Add `_l_english.yml` key; ensure BOM |
| `INJECT:` produces no change / error | Folder doesn't support entry modes, or sub-block injection | Use whole-file replacement for that type |
| Save games won't load / checksum fail | Mod changes `common/`, `events/`, `gui/`, `localization/`, `interface/` after save created | Disable the mod to verify; content changes alter checksum |

## Compatibility Notes from Community Practice

- Prefix all new filenames with a unique mod identifier (e.g., `SOL_economy_`).
- Use `00_` prefixes only when filename order is the tiebreaker; operation type outranks it.
- The EU5 Modding Co-op template and community mods load `setup/` definitions from `main_menu/setup/`, not `in_game/setup/`.
- `script_docs` and `dump_data_types` are the authoritative references; wiki tables lag patches and often miss new fields.
- Test multi-mod load order with the Community Mod Framework if available; it surfaces merge conflicts before runtime.