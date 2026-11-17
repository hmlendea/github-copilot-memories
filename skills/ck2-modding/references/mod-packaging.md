# Mod Packaging, Installation, Load Order, and Override Semantics

## Paths

| Purpose | Path |
|---------|------|
| Mod install (Windows / macOS) | `~/Documents/Paradox Interactive/Crusader Kings II/mod/` |
| Mod install (GNU/Linux) | `~/.paradoxinteractive/Crusader Kings II/mod/` |
| Logs | `<user data>/Crusader Kings II/logs/` |
| Steam install | `<steam>/steamapps/common/Crusader Kings II/` |
| Steam Workshop content | `<steam>/steamapps/workshop/content/203770/` |

Never install into the game's own `mod/` folder. That folder is legacy: `replace_path` and `archive` are ignored there, so mods load partially or not at all.

Folder and file names are case-sensitive on Linux and macOS. Match vanilla path case exactly (`events/`, not `Events/`).

## Mod Skeleton

```
mod/
  mymod.mod          # launcher metadata
  mymod/             # content, mirroring the game root
```

The `.mod` file must not contain spaces in its filename, or the launcher will not auto-select it on restart. Filenames are otherwise free-form, but `lower_with_underscores` avoids the Linux and macOS case traps.

Build the skeleton by hand or copy an existing unpacked mod. Steam Workshop mods cannot be used as a template: they ship as `.zip` plus a stub descriptor.

## Descriptor Fields

| Field | Required | Effect |
|-------|----------|--------|
| `name` | yes | Display name in the launcher and the load-order key |
| `path` | yes for a local mod | Mod folder, relative to the CK2 user directory, e.g. `mod/MyMod` |
| `archive` | replaces `path` | Zip instead of folder, relative to the user directory; Workshop format only |
| `user_dir` | no | Stores saves and temporary files in `<user data>/Crusader Kings II/<value>/`. Set it for overhauls whose saves are not vanilla-compatible. Never set it on a sub-mod: all active `user_dir` values are concatenated |
| `replace_path` | no | Discards every vanilla file in that folder and loads only the mod's. Folder-only, non-recursive |
| `dependencies` | no | `{ "Main Mod" "Another Mod" }`; those mods load first, so this one can override them. Not a hard requirement |
| `picture` | no | Workshop banner image inside the mod folder, displayed as 268×268 JPEG |
| `tags` | no | Workshop tags, quoted when they contain spaces |
| `supported_checksums` | no | Checksums for which the `supported_checksums` condition evaluates true; used to warn players |

Small mod:
```
name = "Small Mod"
path = "mod/SmallMod"
picture = "SmallMod.jpg"
tags = { "Mods" "Small" }
```

Overhaul:
```
name = "Big Mod"
path = "mod/BigMod"
user_dir = "BigMod"
replace_path = "history/provinces"
picture = "BigMod.jpg"
tags = { "Mods" "Big" }
```

Sub-mod:
```
name = "Sub Mod"
path = "mod/SubMod"
dependencies = { "\"Main Mod\"" }
```

Dependency names match the `name` field of the other descriptor, not its filename. Quoting rules:
- A dependency whose name has no spaces must be quoted before Workshop upload, because the uploader strips quotes.
- A dependency whose name has spaces must use escaped quotes: `"\"Main Mod\""`.

## Load Order

- Load order is launcher playset order. Later mods override earlier ones at file level, and `dependencies` is the declared way to force that.
- Within a playset, priority is decided by the `name` field, not the filename or folder: names starting with digits outrank uppercase, which outranks lowercase, in ASCII order.
- Vanilla always loads before mods.

## Duplicate Definition Behaviour

CK2 has no single override rule. Each folder does one of four things with a repeated key:

| Behaviour | Meaning |
|-----------|---------|
| First wins | The first loaded definition is kept; later ones are ignored |
| Last wins | The later definition fully replaces the earlier one |
| Merge / append | Blocks with the same key are merged, or lists are appended |
| Coexist | Both definitions are retained, so the entity is duplicated |

Selected rules:

| Folder | Behaviour |
|--------|-----------|
| `common/traits` | Coexist; random characters can receive both copies |
| `common/buildings` | Coexist; reusing a name duplicates the building |
| `common/cb_types` | Coexist; reusing a name duplicates the casus belli |
| `common/societies`, `common/objectives` | Coexist; reusing a name duplicates the entry |
| `common/retinue_subunits`, `common/religion_features` | Coexist; same key duplicates |
| `common/minor_titles` | Cannot be overridden; duplicates share tags |
| `common/holding_types` | Triggers append; a holding must satisfy every file's triggers |
| `common/laws` | `allow` conditions append; `potential` does not |
| `common/scripted_triggers` | Conditions append rather than replace |
| `common/on_actions` | Events append to the existing list (since 2.4) |
| `common/religions` | Merge; a religion may be overridden without copying the group. Reformed religion must be defined before the unreformed one |
| `common/cultures` | Merge since 2.4, like religions |
| `common/landed_titles` | Merge, with complicated and unreliable results |
| `events/` | A redefined event in an alphabetically later file fully overrides; discouraged by the developers |
| `decisions/` | Reusing a name breaks the decision instead of replacing it |
| `localisation/` | Full override; across files the first loaded wins, within one file the last duplicate wins |
| `interface/*.gfx` | Files load alphabetically; the last `spriteType` with a given name wins |
| `interface/sound.sfx` | Only this file is read; other `.sfx` files are ignored |
| `common/dynasties` | Duplicates loaded early (`000_` prefix) override shields; duplicates loaded late (`z_` prefix) override names |
| `history/characters` | Merge; duplicate character IDs corrupt character history |
| `map/`, `common/defines.lua` | Whole-file or per-entry override only |

Practical consequences:
- Prefix a replacement localisation file with `00_` so it loads first.
- Prefix a replacement `.gfx` file with `zz_` so it loads last and wins.
- Add a new file instead of copying a vanilla one in every folder that merges.
- Never reuse a vanilla key in a coexist folder.

## Overwriting and `replace_path`

- To replace a file, place a file with the same relative path and name in the mod. The vanilla file is then ignored.
- `replace_path` removes everything in a vanilla folder, including content other mods add. Use it only for total conversions, and only for folders the mod fully supplies.
- `replace_path` is folder-granular and does not cascade: replacing `history` does not replace `history/characters`.
- Delete the `user_dir` gfx cache (`<user data>/Crusader Kings II/<mod_name>/gfx`) after changing assets, or stale textures persist.

## User Directory Cautions

- Saves and temporary files move to the named directory, isolating them from vanilla.
- Sub-mods must not set it; the launcher concatenates the value of every active mod.
- Steam Cloud appears to break for mods whose `user_dir` contains capital letters on Linux.

## Steam Workshop

Upload:
1. Optionally set `picture` and `tags` in the `.mod`.
2. Launch the game with the mod active, `path =` format, and no `archive =`.
3. **Content → Manage → Publish/Update.**
4. The item is created private; set visibility to public from the Workshop page.

Update:
1. Unsubscribe, then remove the old `.zip` and `.mod` from the mod folder.
2. Restore the unpacked folder and a `path =` descriptor.
3. Delete any `descriptor.mod` inside the folder.
4. **Content → Manage → Update.** Visibility resets to hidden after each update.

Constraints:
- The 50 MB limit was lifted in 2.8, but uploads above roughly 350 MB fail.
- Downloaded mods are rewritten to `archive = "mod/MyMod.zip"` with quotes stripped; that is why space-containing dependency names need escaping.
- Maximum 50 subscriptions.
- The Workshop auto-updates, so previous saves can become unplayable.

## Manual Installation

1. Remove the previous install, both folder and `.mod`.
2. Delete `<user data>/Crusader Kings II/<mod_name>/gfx` if present.
3. Extract so the mod folder holds both the `.mod` and the mod directory.
4. Enable it in the launcher Mod tab; the launcher display name may differ from the filename.

## Checksum, Ironman, and Achievements

- The launcher shows the expected checksum; the lobby shows the actual checksum, recomputed from loaded files.
- Achievements require single-player ironman, no Ruler Designer start, and an unaltered checksum.
- Gameplay script changes alter the checksum and disable achievements. Localisation and graphical or music replacement do not.
- State the limitation rather than promising achievement safety.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Mod absent from the launcher | Wrong folder, or `.mod.txt` extension | Move into the user `mod/` folder; disable hidden extensions |
| Mod not auto-selected after restart | Space in the `.mod` filename | Rename without spaces |
| Mod enabled but inert | `replace_path` or `archive` used from the game's legacy `mod/` folder | Move to the user `mod/` folder |
| Only some files load | Wrong case in folder or file name on Linux/macOS | Match vanilla casing |
| Content doubled | Reused a key in a coexist folder | Rename the key |
| Custom map or history ignored | `replace_path` missing, or pointing at a subfolder | Replace the parent folder as well |
| Stale textures or portraits | Cached gfx from a previous install | Delete the mod's `gfx` cache under `<user data>` |
| Sub-mod cannot override the main mod | Wrong `dependencies` name, or stripped quotes after Workshop upload | Use the `name` field value; escape quotes |
| Workshop mod fails after manual install | Both copies present | Remove the manual `.mod` and `.zip` |