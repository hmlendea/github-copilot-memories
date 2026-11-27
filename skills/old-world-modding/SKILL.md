---
name: old-world-modding
description: "Use when creating or editing an Old World mod, including ModInfo.xml mod directories, Infos XML add/change/append files, event stories and bonuses, text localisation, custom units and formations, Unity asset bundles, DLL entry-point mods, mod.io publishing, console commands, and debug logs. Covers Old World mod structure, XML merge semantics, event subjects and triggers, custom assets, .NET Framework compatibility, and troubleshooting."
---

# Old World Modding

Apply when authoring or reviewing content for **Old World** (Mohawk Games, Unity).

Source material: the [Old World Wiki Modding page](https://oldworldwiki.org/index.php/Modding), Dale's [Creating Old World Mods](https://dales.world/files/Creating%20Old%20World%20Mods.pdf), the [Mohawk Games modding page](https://mohawkgames.com/modding/), the linked Event Browser documentation, Event Modding Guide, Event Style Guide, Text Editing Cheat Sheet, Console Commands, Hotkey List, and Unit Modding Guide. Version-sensitive details require confirmation against the installed game, its Reference/XML files, current modding tools, and logs.

## Non-Negotiable Build Rules

1. **Never edit Reference/XML or installed game files.** Those files are references; runtime content is loaded from the mod directory.
2. **Use a mod directory and `ModInfo.xml`.** Create or manage the mod from the in-game Mods screen when possible, then place files under the generated mod folder. The folder name is the displayed mod name; the description comes from `ModInfo.xml`.
3. **Put XML content in `Infos/`.** Use the filename suffix deliberately: `-add.xml` creates new entries, `-change.xml` modifies existing elements and fields, and `-append.xml` adds lines to existing elements. Match the original XML structure and `zType` identifiers.
4. **Use a test build with debug mode enabled.** Activate the mod, return to the start screen, inspect `Logs/output.txt`, and fix errors one at a time before testing a new game.
5. **Use new games for validation.** Saves do not refresh every XML or asset change; use the Game Editor for rapid setup where appropriate.
6. **Do not assume stale guides are authoritative.** The guide targets older Unity and game versions. Verify Unity version, supported .NET target, XML schemas, and entry-point APIs against the installed build.
7. **Keep identifiers unique and preserve references.** New `zType` values, text keys, assets, events, options, bonuses, and unit definitions must be consistently connected.

## Mod Layout

```
Mods/
  My Mod/
    ModInfo.xml
    Infos/
      nation-add.xml
      nation-change.xml
      text-english-add.xml
      spriteGroup-append.xml
      eventStory-add.xml
      option-add.xml
      bonus-add.xml
      asset-add.xml
      modUnit-add.xml
      formation-add.xml
      unit-add.xml
    # Optional: DLL and asset-bundle files
```

The documented Windows path is `Documents/My Games/OldWorld/Mods/<Mod Name>/`; use the current game's user-data location on other platforms. The in-game Mods screen can create the profile, open the folder, enable or disable the mod, and upload a build through the mod.io integration.

## Domain Map

| Need | Location or artefact | Reference |
|------|----------------------|-----------|
| Mod profile, activation, upload, and folder layout | `Mods/<name>/ModInfo.xml` | `references/mod-packaging.md` |
| XML creation, modification, append semantics, identifiers, and text | `Infos/*-add.xml`, `*-change.xml`, `*-append.xml` | `references/xml-and-content.md` |
| Event stories, subjects, triggers, options, bonuses, flavour text, and event testing | Event XML and text XML | `references/events-and-text.md` |
| Custom units, formations, prefabs, animation clips, sprites, and asset bundles | `asset-add.xml`, `modUnit-add.xml`, `formation-add.xml`, Unity project | `references/assets-and-units.md` |
| DLL entry points, references, Unity, and .NET compatibility | Mod DLL and game `*_Data/Managed/` assemblies | `references/dll-modding.md` |
| Console, hotkeys, debug mode, logs, and reload workflow | Console and `Logs/output.txt` | `references/debugging-and-tools.md` |

Open only the reference needed for the task.

## Working Method

1. Create or open the mod through the Mods screen; confirm the mod folder and `ModInfo.xml`.
2. Copy the relevant file from the installed `Reference/XML/` directory into `Infos/`, rename it with `-add`, `-change`, or `-append`, and make the smallest edit.
3. For events, define metadata, a unique story `zType`, valid subjects, trigger and probability fields, at least one option, and bonuses aligned with subject order; connect all generated text and option identifiers.
4. For text, preserve the game's markup and variable conventions. Validate subject indexes, gender conditionals, links, and plural or grammatical forms in the target language.
5. For custom assets, use the game-compatible Unity version and asset template; create PNG assets at suitable dimensions, add asset-bundle references, and test one asset before scaling up.
6. For custom units, provide the required asset, model, animation, formation, and gameplay XML; ensure `modUnit` animation fields reference asset entries and the formation references the mod unit.
7. For DLL work, target the supported .NET Framework, reference the installed Unity and game assemblies, derive from `ModEntryPointAdaptor`, implement `Initialize()`, and copy the compiled DLL into the mod folder. Never guess assembly APIs.
8. Enable the mod, inspect `Logs/output.txt`, test from a new game, and use the console or Game Editor to exercise the changed content.
9. Upload only after local validation; confirm the mod.io profile and build contain the expected files.

## Honest Limits

- XML files in the installed `Reference/XML/` directory are not runtime overrides; they are templates and documentation.
- `-change` changes existing elements and fields; `-append` adds lines to an existing element. Choosing the wrong suffix can produce ignored content or an unintended merge.
- Asset and UI work requires Unity and compatible asset bundles; a normal text editor is sufficient only for basic XML modding.
- DLL mods are coupled to the installed game's Unity, managed assemblies, and .NET Framework API surface; updates can break binary compatibility.
- Event behaviour depends on the trigger's subject and extra indexes. A syntactically valid event can remain inert if its subjects, trigger, weight, probability, or repeat settings are wrong.
- The public guide's Unity version and loader details are historical. Verify the current version and API before creating an asset or DLL project.
