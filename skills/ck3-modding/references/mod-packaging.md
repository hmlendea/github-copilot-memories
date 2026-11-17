# Mod Packaging, Installation, Load Order, and Override Semantics

## Paths

| Purpose | Path |
|---------|------|
| Mod install (Windows / macOS) | `~/Documents/Paradox Interactive/Crusader Kings III/mod/` |
| Mod install (GNU/Linux) | `~/.local/share/Paradox Interactive/Crusader Kings III/mod/` |
| Logs | `<user data>/Crusader Kings III/logs/` |
| Save games | `<user data>/Crusader Kings III/save games/` |
| Run scripts | `<user data>/Crusader Kings III/run/` |
| Game installation | `<steam>/steamapps/common/Crusader Kings III/game/` |
| Steam Workshop content | `<steam>/steamapps/workshop/content/1158310/` |

Folder and file names are case-sensitive on Linux and macOS. Match vanilla path case exactly.

The two user-data paths can be relocated: `launcher-settings.json` (`gameDataPath`) in the Launcher folder moves the launcher's data, and a `game/userdir.txt` file containing an absolute path ending in `/` moves game data. Useful when the default location is inside a synced folder.

## Mod Skeleton

```
mod/
  my_mod.mod          # launcher metadata, alongside the folder
  my_mod/
    descriptor.mod    # in-folder copy, no path key
    thumbnail.png
    ...
```

The folder name and the `.mod` filename should match; the launcher recognises a mod by the `.mod` file, not the folder. The mod folder itself does **not** have to be inside `mod/` — only the `.mod` file must be there, and `path` may point anywhere (absolute paths are accepted).

**Preferred creation method:** the game launcher (Mod library → Upload Mod → Create a Mod). It writes the folder, `descriptor.mod`, and the outer `.mod` with correct syntax. Name must be at least three characters; the directory may contain spaces but must not end with one, and must not contain non-English characters (a non-ASCII Windows account name forces a directory outside `Documents`).

## Descriptor Keys

| Key | Required | Effect |
|-----|----------|--------|
| `name` | yes | Display name in the launcher |
| `version` | yes | Version of the *mod*, a quoted string |
| `path` | required in the outer `.mod`, omitted in `descriptor.mod` | Mod folder: absolute, or relative to the CK3 user directory as `mod/my_mod` |
| `supported_version` | required in the outer `.mod`, optional in `descriptor.mod` | Latest supported game version (semantic `MAJOR.MINOR.PATCH`); a wildcard `*` may define a range. A mismatch only produces a launcher warning |
| `tags` | no | Workshop-aligned categories, quoted, e.g. `tags={ "Culture" "Decisions" "Fixes" }` |
| `remote_file_id` | required for Steam upload/update | Must equal the Steam Workshop ID; set automatically on first upload |
| `picture` | no | Image for the launcher; Steam ignores it and always looks for `thumbnail.png` |
| `replace_path` | no | Suppresses loading of all vanilla files under that path |

Syntax is the same key/value language as script: `key="value"`, `list={ "a" "b" }`, `#` comments. Quotation marks around paths and names are required; a missing quote is a common reason a mod does not appear at all.

```
version="0.0.1"
tags={
	"Culture"
	"Fixes"
}
name="My Mod"
supported_version="1.20.*"
path="mod/my_mod"
```

The documented key set for CK3 does not include a `dependencies` key; do not carry CK2 syntax over.

## Install Paths Recognised by the Launcher

| Situation | What is needed |
|-----------|----------------|
| Local mod | `.mod` alongside the mod folder, `path` pointing at the folder |
| Stepped folder | `.mod` in `mod/`, `path` pointing anywhere (for example outside `Documents`) |
| Forum mod archive | Unpack the whole archive (`.mod` plus folder) into `mod/` |
| Paradox Mods download | The archive contains **only** the folder contents: unzip into a new folder in `mod/`, copy `descriptor.mod` out to `mod/`, rename it, add a `path="mod/<folder>"` line |
| Steam Workshop subscription | Managed by Steam; do not keep a local copy as well |

## Load Order

Mods load top to bottom within a playset. **The mod lower in the playset wins** for identical files. Put a mod you never want overridden at the very bottom.

Load order only matters where footprints overlap, so keep the footprint (the set of vanilla files and objects the mod overrides) minimal. Conflicts are written to `logs/database_conflicts.log`; grep it after adding a mod to a playset.

In multiplayer every player must run the same mods in the same order.

## Override Semantics

Four mechanisms exist, and the correct one depends on what is being changed.

### 1. Whole-file override

A file at the same relative path with the same filename replaces the vanilla file entirely. Use it only when the whole file is intended to be replaced; the correct approach is usually to add a new, uniquely named file instead.

### 2. Single-object override (LIOS — Last In, Only Served)

A **top-level declaration** (a key defined at the start of a line, not nested in a block) can be redefined from a different file. The file whose name sorts later in ASCIIbetical order wins, so a mod file named `01_...` overrides `00_defines.txt`, and a file named `zzz_...` overrides almost everything.

- The override must supply the whole object; it changes an object but **cannot delete one**.
- Prefix added filenames with the mod name so they are identifiable in `database_conflicts.log`.
- Example: a new `common/scripted_triggers/all_can_raid_trigger.txt` containing `can_raid_trigger = { always = yes }` replaces the vanilla `can_raid_trigger` and lets anyone raid.

### 3. UI types and templates (FIOS — First In, Only Served)

Types and templates take the **first** loaded definition, so the file name must sort *earlier*: `00_my_buttons.gui` overrides a vanilla `types` block. A type replacement needs a `types <GroupName> { type ... }` wrapper (any group name); a template needs nothing extra.

### 4. Priority-scoped overrides (events and characters, 1.20+)

Single events use `id_override_priority`; single characters use `history_override_priority`. Baseline vanilla priority is 0; a higher number wins.

```
namespace = custom_events
custom_events.0001 = {
	type = character_event
	id_override_priority = 10
	...
}
```

```
42 = {                          # char ID
	history_override_priority = 10
	name = "Clemens"
	culture = "french"
	867.1.1 = { birth = "840.1.1" }
}
```

## Merging Versus Overwriting, Folder by Folder

| Area | Behaviour |
|------|-----------|
| `common/scripted_effects`, `common/scripted_triggers`, `common/script_values` | Object-level LIOS override; define the same key in a later-sorting file |
| `common/defines` | Object-level override of a category block, e.g. `NCharacter = { BASE_FERTILITY = 0.5 }` |
| `common/on_action` | `events`, `random_events` and `on_actions` are **appended**. A restated `trigger` or `effect` overwrites (and errors). Chain a custom on_action instead |
| `localization` | Keys merge; a single key may be replaced, but only from a `replace/` folder without producing errors |
| `gui` | Windows are replaced whole; types and templates are FIOS |
| `common/holdings`, `common/buildings` | Adding buildings or holding types requires overwriting the whole `common/holdings/holdings.txt` |
| `gfx/portraits` genes | New clothing requires overwriting the `genes` definitions |
| animations | New animations require overwriting the idle animation |

## Compatibility Techniques

- **Zero footprint** is the safest compatibility posture: never mention vanilla database keys (faiths, cultures, titles, characters) if the mod must survive a total conversion.
- **Shared variable**: one mod sets `set_variable = { name = erre_seduced_each_other value = ... }`; the other tests `has_variable = erre_seduced_each_other`, which is false when the first mod is absent. No hard dependency either way.
- **Shared scripted effect**: the caller invokes `mod_a_fire_thing_effect = yes`; mod A defines it in an early-sorting file, mod B redefines it in a late-sorting file. Whichever mod is absent, the remaining definition still works.
- **Shared scripted trigger for detection**: the detected mod defines `shrek_is_loaded = { always = yes }` in a late-sorting file; the detecting mod defines the same key as `always = no` in an early-sorting file, so the definition survives only when the other mod is loaded.
- **Global variable for detection**: a mod sets `set_global_variable = { name = shrek_is_loaded value = yes }` from `on_game_start`. Only reliable after `on_game_start` has run, and only if the game was started with that mod active.

## Publishing

1. Launcher → Mod library → Upload Mod.
2. Choose the mod from the dropdown and the target platform.
3. Enter the description (the launcher overwrites it from the site when updating).
4. Add the thumbnail:
   - Steam Workshop: `thumbnail.png` inside the mod folder, 1:1 ratio, max 1 MB (displayed at roughly 600×600).
   - Paradox Mods: drag the image into the field below the description; suggested minimum 900×500, PNG or JPG, max 1 MB.
5. Upload.
   - Steam uploads **privately**; set the Workshop item to Public afterwards.
   - Paradox Mods publishes after verification and strips line breaks and BBCode from the description.

Never subscribe to a mod while keeping a local copy: the launcher cannot reconcile the two and the mod may fail to load. Publishing to both platforms is preferable, since not every player owns the game on Steam.

## Troubleshooting

| Symptom | Cause and fix |
|---------|---------------|
| Paradox Mods mod seems to add nothing | The game ignores **new files** from Paradox Mods downloads; remove from the playset, download, and install manually |
| Mod uploaded to Steam does not work | Both a local copy and a subscription exist; remove one |
| Mods stop working for no apparent reason | Launcher → Mod library → Reload Mods; remove the mod from the playset, close the launcher, resubscribe, re-add. If that fails, delete `mods_registry.json` and `launcher-v2.sqlite` from the user directory and restart the launcher |
| Two mods fight over the same file or object | Expected conflict — read `logs/database_conflicts.log`; build a compatch mod loaded after both |
| Mod does not appear in the launcher | Missing or malformed outer `.mod`, quotation marks omitted, or name/folder mismatch |
| Script errors for a vanilla key | The patch changed it; regenerate documentation with `script_docs` and re-check |

Inspecting a downloaded mod's footprint: drop the mod folder into a text editor and use search-in-folder (Ctrl+Shift+F in VS Code) to list the vanilla paths it carries.
