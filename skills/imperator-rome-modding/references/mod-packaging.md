# Mod Packaging, Installation, and Publication

## Creating the Mod Skeleton

Use the game's own tooling; it writes both the descriptor and the folder so the launcher recognises the mod immediately.

1. Launch the loader, open **Mods → Mod Tools → Create a mod**.
2. Fill every field, including tags. *Version* means the game version the mod targets.
3. Confirm: a folder plus a `.mod` file appear in the user mod directory.

Folder names may contain spaces, but `lower_with_underscores` is conventional and safer in shell tooling.

## Paths

| Purpose | Path |
|---------|------|
| Mod install (Windows / macOS) | `~/Documents/Paradox Interactive/Imperator/mod/` |
| Mod install (GNU/Linux) | `~/.local/share/Paradox Interactive/Imperator/mod/` |
| Logs | `<user data>/Imperator/logs/error.log` |
| Steam Workshop content | `<steam>/steamapps/workshop/content/859580/` |

Never install a mod under the game's own `ImperatorRome/mod/` directory; the game will not load it correctly.

A Workshop subscription places only a stub `.mod` in the mod directory pointing at the Workshop content folder; the real files stay in `steamapps/workshop/content/`.

## Descriptor Files

- `my_mod.mod` — created by the Mod Tools dialog; this is what the launcher lists for a local mod.
- `my_mod/descriptor.mod` — created by the launcher on the **first upload**; it links the folder to the published Workshop item and is used for subsequent updates. Do not ship a mod without it if you intend to update an existing Workshop entry.

New launchers rewrite the `path` field in the `.mod` to an absolute path (`C:/Users/.../mod/my_mod`). This breaks loading for some users. Recovery:

1. Restore a relative path such as `path="mod/my_mod"`.
2. Mark the file read-only (file properties) so the launcher cannot rewrite it.
3. Unset read-only before uploading, since the launcher needs write access.

## Thumbnail

Place `thumbnail.png` inside the mod folder. Minimum 200×200 pixels, otherwise Steam pads it with black borders.

## Installing a Third-Party Mod Manually

1. Delete any previous installation, including the old folder and `.mod` file. The game loads every file present in the mod folder, so leftovers from a renamed or removed file conflict with the new version.
2. Delete the cached `<user data>/Imperator/<mod_name>/gfx` folder if present.
3. Extract the archive so the mod folder contains both the `.mod` file and the mod directory.
4. Select the mod in the launcher Mod tab. The launcher display name can differ from the `.mod` filename.
5. Launch.

## Publishing and Updating

1. **Mods → Upload Mod**, pick the mod from the dropdown, choose the platform, upload. A description is optional.
2. The item appears under the Steam profile's Workshop Items and is uploaded **private**; set visibility to Public to publish.
3. Update by uploading again from the loader; the existing `descriptor.mod` is reused.
4. While testing the Workshop build, move the local folder *and* its `.mod` file elsewhere, otherwise the two copies conflict.

Paradox Mods (`mods.paradoxplaza.com/games/imperator_rome`) is not integrated into the loader; mods are downloaded manually and require game registration.

## Checksum and Ironman Safety

- The checksum is a 4-character identifier in the bottom-right of the main menu, computed from base game (excluding DLC) plus the enabled mod set.
- Multiplayer requires identical checksums: identical mod set, identical load order, no debug console enabled, identical mod versions, and identical game version. A macOS bug makes locally installed mods checksum differently from Workshop-installed ones.
- Only texture, font, and music replacements are checksum-safe. Everything else disables achievements.
- Loading an ironman save with a checksum-changing mod can make the save permanently unplayable. Warn users explicitly when a mod is not ironman-safe.
- `checksum_manifest.txt` in the game folder lists the checksummed folders and files.

## Load Order

Load order matters and is defined by the launcher playset order. Later entries override earlier ones at file level. Use `localization/replace/` when a localisation entry must win regardless of file order.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Mods appear in the launcher but have no in-game effect; no Resume button | Documents folder relocated (secondary drive, OneDrive, Google Drive) | Edit `<game>/launcher/launcher-settings.json`, set `gameDataPath` to `"%USER_DOCUMENTS%/Paradox Interactive/Imperator"`, or a full forward-slash quoted path such as `"F:/Documents/Paradox Interactive/Imperator"` |
| Crashes, wrong rulers, general strangeness | A badly written mod left generated files in the user data folder | Quit the game, keep only `mod`, `logs`, `save games`, `screenshots` under `<user data>/Imperator/`, delete everything else, relaunch |
| Mods disabled yet the old UI or checksum persists | Stale files in `<user data>/Imperator/mod` | Clean the mod folder |
| Mod silently ignored | Wrong install path, or a local copy colliding with the Workshop copy | Reinstall to the correct user data path; remove the duplicate |
| New country crashes on multiplayer join | Country has no province under `own_control_core` | Assign at least one owned province |