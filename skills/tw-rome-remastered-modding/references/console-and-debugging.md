# Console, Launch Options, Logs, Tools, and Porting

## RomeShell

The in-game console (RomeShell) is reachable from campaign and battle. Commands are listed in `VFS/Local/Rome/documentation/docudemon_romeshell.txt`, regenerated on every launch; the shipped `documentation/feature_guides/scripts/console_commands.txt` is a readable copy.

Each entry declares availability: `campaign`, `battle`, or `campaign_ed` (campaign editor). A command fired in the wrong mode does nothing.

Frequently used:

| Command | Use |
|---------|-----|
| `add_money [faction] <amount>` | Give or take denarii (negative allowed) |
| `add_population <settlement> <amount>` | Adjust settlement population |
| `process_cq <settlement>` | Complete the construction queue |
| `auto_win attacker\|defender` | Force the next auto-resolved battle |
| `toggle_fow` | Reveal or hide fog of war |
| `show_cursorstat` | Tile coordinates under the cursor |
| `character_reset <name>` | Restore a character's action points |
| `force_diplomacy <accept\|decline\|off>` | Auto-accept or auto-decline AI proposals |
| `kill_character <name>` | Remove a character |
| `bounds`, `building_debug` | Battle debug overlays |
| `check_persistent_var <name>` | Write a persistent counter to the log |
| `event volcano <x> <y>` | Trigger a volcano |
| `amdb_min`, `amdb_max`, `amdb_offset` | Aerial map depth bias |

Script reaches the same surface with `console_command <name> <args>`.

## Launch Options

Set in the pre-game options panel, Advanced tab. Combine freely.

| Option | Effect |
|--------|--------|
| `enable_logging` | Writes `message_log.txt` and `campaign_ai_log.txt` with progress, warnings, and errors |
| `verbose_script_logging` | Writes `scripting_log.txt`; line-by-line, very large |
| `enable_dialogs` | Shows the extended warnings as pop-ups |
| `-show_err` | Original single-message error dialog; weaker than `enable_dialogs` |
| `battle_model_info` | Shift+left-click a unit in battle to dump its model, texture, and variation data |
| `building_debug_info` | Hover a building in battle for its asset information |
| `log_conversion_calc` | Per-turn religion conversion maths in the log (needs `enable_logging`) |
| `report_model_mismatches` | Model/texture mismatch list; hundreds of benign lines |
| `verbose_skeletons` | Skeleton and animation pack detail |
| `enhanced_tweaks` | Opens the graphics variable overlay |
| `unpack_characters` | Extracts character `.cas` from packs |
| `movie_cam` | Cinematic camera |

## Logs

All under `%LOCALAPPDATA%\Feral Interactive\Total War ROME REMASTERED\VFS\Local\Rome\logs\`:

| File | Content |
|------|---------|
| `message_log.txt` | Data-file progress, warnings, errors |
| `campaign_ai_log.txt` | Per-faction AI decision trace |
| `scripting_log.txt` | Every script command and monitor evaluation |

`enable_dialogs` exists because some failures only surface as warnings; expect benign warnings even in the unmodded game.

## Generated Documentation

Every launch writes into `VFS/Local/Rome/documentation/`:

- `docudemon_events.txt`
- `docudemon_conditions.txt`
- `docudemon_commands.txt`
- `docudemon_romeshell.txt`

These reflect the installed build, not the wiki. When a shipped Markdown file and the docudemon disagree, the docudemon is correct.

## Error Catalogue

| Message | Meaning |
|---------|---------|
| `read_no_endian(&data, sizeof(T)) Failed` | Reader hit end-of-file early — a truncated or wrongly formatted file, or a missing trailing line |
| `num_stations < MAX_ENGINE_STATIONS` | `descr_engines.txt` has more than 4 `engine_station` entries for one engine |
| `defender->battle_combo_get().defense.m_is_valid Failed` | Second value in `stat_pri_armour` or `stat_sec_armour` is 0; minimum is 1 |
| `Condition parser doesn't recognise this token: <token>` | Trigger name casing or spelling — triggers are case-sensitive |
| `Unexpected in condition parsing` | A dangling `and`/`or`, or a condition split across lines |
| `settlement '' not found in stringtable` | A `descr_regions.txt` block is missing a line, so the religion line shifted and the parser started a new block |
| Blank launch error with a yellow `!` | Path length |
| No errors, mod does nothing | Stale manifest, wrong base game, wrong case, UTF-8 BOM, 0 KB file |
| `Issue when attempting to read descr_senate.txt` | Senate file structure error |
| `Couldn't find senate office title '<key>' in expanded string table` | Office title missing from `expanded_bi.txt` |

## Bundled Tools

| Tool | Purpose |
|------|---------|
| Skeleton Converter | Upgrade a skeleton to Remastered format |
| Audio Packer | Unpack and repack `.feral.dat` audio |
| CAS Exporter (`casPacker`) | Convert `.fbx` ↔ `.cas` |
| Campaign Map Tool | Blender mesh generation and sectioning for the campaign map |
| `unpack_characters` launch option | Extract character `.cas` from packs |
| Unit Card generator | Standalone repository that renders cards from models |
| RSD Packer | Unpack and repack `.rsd` UI textures |
| RomeTextureCompress | Build the packed albedo and PBR `.dds` files |

## Third-Party Tools

- **IWTE** — the workhorse: `.cas` ↔ `.dae`, unit meshes plus animations, campaign mesh and textures from `map_*.tga`, bulk texture decompression.
- **XIDX** — packs and repacks the `.idx`/`.pak` archives.
- **Vercingetorix's tools** — original IDX and PAK extractors.
- **LOD Generator** — Blender plug-in for model LODs.
- **Settlement and region name extractor**.
- **VS Code "Total War Script Highlighting"** — syntax highlighting for the script language and data files.

**Do not mix conversion tools within one asset.** Each has its own default scale and orientation; import and export with the same tool.

## Porting an RTW or BI Mod

1. Confirm the target base game and match its internal faction, culture, and religion names — or ship every file that names them.
2. Build a minimal mod folder first: copy in the map files, change one visible thing (for example the playable faction list), and confirm the mod loads.
3. Rewrite `descr_strat.txt`:
   - Every character name must exist for that faction in `descr_names.txt` and `data/text/names.txt`; a mismatch is a CTD.
   - Add the resource quantity: `resource marble, 56, 62` → `resource marble, 1, 56, 62`.
   - Convert AI personalities from `comfortable caesar` to `comfortable_caesar` and register the combination in `feral_descr_ai_personality.txt`; otherwise the AI will not expand.
   - Remove units and buildings you have not re-registered; the EDB structure is largely compatible but every `recruit` line needs an EDU entry and every EDU entry needs a DMB model.
4. Convert models: RTW `.cas` works but the DMB structure changed — `model <base path>` with four `.cas` LODs, ethnicity models, and `pbr_texture` entries replace `model_flexi` and `indiv_range` for units. Skill weights: LOD0 may use two bones, lower LODs must not.
5. Rebuild the campaign mesh if the map shape differs. Heightmap `.bin` files and the 3D mesh do not follow the TGAs.
6. Ship localisation for every language you renamed.
7. Regenerate the manifest and test with `enable_logging`.

## Verification Loop

1. Regenerate the manifest.
2. Launch with `enable_logging`, plus `verbose_script_logging` for script work and `enable_dialogs` when a silent failure is likely.
3. Reproduce the change in the shortest possible campaign or a custom battle.
4. Read `message_log.txt`; if script is involved, `scripting_log.txt`; if AI behaviour is involved, `campaign_ai_log.txt`.
5. If the log is clean and the change still does not appear, re-check the four non-obvious causes: base-game mismatch, filename case, file encoding, and path length.