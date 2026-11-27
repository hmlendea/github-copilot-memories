# Mod Packaging and Installation

## Mod directory

Old World loads mod content from the user mod directory, not from the installed `Reference/XML/` directory. The documented Windows location is:

```
Documents/My Games/OldWorld/Mods/<Mod Name>/
```

Use the current user-data path for the installed platform and version. The in-game Mods screen is the safest way to create a profile: use `UPLOAD` -> `CREATE NEW MOD`, then `OPEN MOD FOLDER`.

## Required profile

Create or retain `ModInfo.xml`. The mod folder name is shown as the mod name in the selection menu, while the description is read from the profile. Enable the mod in `MODS` -> `MANAGE`, save the selection, return to the start screen, and start a new game.

## Publishing

The documented workflow uses the in-game mod.io integration. Create the profile, validate locally, then use `UPLOAD BUILD`. Confirm the registered mod and uploaded build before distributing it. Keep development and published builds distinguishable.

## Common failures

- Editing installed reference files has no runtime effect.
- A missing or malformed `ModInfo.xml` prevents normal profile management.
- Testing from an old save can hide changes that require a new game.
- A mod.io registration or upload failure can be a platform-account issue; inspect the mod.io site and game logs.
