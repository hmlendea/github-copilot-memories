# Mod Packaging, Modular Loading, Load Order, and Installation

## Paths

| Purpose | Path |
|---------|------|
| Base game (off-limits) | `<steam>/steamapps/common/Sid Meier's Civilization IV/` |
| BtS base assets | `<install>/Beyond the Sword/Assets/` |
| Mods | `<install>/Beyond the Sword/Mods/<ModName>/` |
| User directory (BtS) | `%USERPROFILE%\Documents\My Games\Beyond the Sword\` |
| Logs | `<user dir>\Logs\` (`PythonErr.log`, `init.log`, `Res.log`, …) |
| `Civ4.ini` | `<user dir>\CivilizationIV.ini` |
| Custom assets (always loaded) | `<user dir>\CustomAssets\` |
| Saves | `<user dir>\Saves\` |
| Public maps per install | `<install>/Beyond the Sword/PublicMaps/` |

The macOS and Linux ports relocate the user directory; find it by searching the filesystem for the `Logs` folder after running the game once. **Case matters on those platforms and not on Windows.** The community is inconsistent about the spelling: the widely distributed mods inspected use lowercase `Assets/xml/...`, while other trees use `Assets/XML/...`, and on Windows both load. Mirror the case of the base tree in the target install exactly, and do not assume a widely used third-party spelling is the platform-native one; a mismatch that is invisible under Windows produces a mod that silently loads nothing under macOS and Linux.

## Mod Skeleton

```
Mods/MyMod/
  MyMod.ini
  Assets/
    XML/            whole-file table replacements
    Modules/        modular additions merged into the target tables
    Python/         script replacements and the mod's own modules
    Art/            .dds, .nif, .kfm
    Res/Fonts/      GameFont.tga, GameFont_75.tga
    Config/         per-mod configuration XML
  PublicMaps/       map scripts and scenarios
  CvGameCoreDLL.dll only if the mod rebuilds the engine
```

A mod's asset at the same relative path as a base asset replaces it. Only the *loaded* mod's tree is on the search path, so a mod that does not replace a file inherits the base one.

## `<Mod>.ini`

The ini is the mod's own configuration. The BtS keys that matter to modders:

| Key | Effect |
|-----|--------|
| `ModularLoading` | `1` enables merging from `Assets\Modules\`. Off by default; the single most common reason a modular file does nothing |
| `AllowPublicMaps` | `1` exposes the install's `PublicMaps` inside this mod |
| `Name` | The name shown in the in-game mod list |
| `Description` | Shown in the mod list |
| `ModImageFile` | Splash image for the mod list |
| `NoCustomArt` / `NoCustomAssets` | `1` ignores the user directory's `CustomAssets`, isolating the mod from whatever the user has installed |
| `NoCustomScenario` | Hides the Custom Scenario entry |
| `NoTeams` | Disables team play |
| `ForceGameOptions` | Reads game options from the mod's XML rather than the ini/profile |
| `ForceStandardEra`, `ForceScenario` | Pins the era or a scenario |
| `SinglePlayerOnly` | Hides the mod in multiplayer |
| `SkipMainMenu` | Boots straight into the mod |

Set `NoCustomAssets = 1` for a mod that must behave identically on every machine; leave it at `0` when the mod is expected to cooperate with a user's `CustomAssets`.

## Loading a Mod

1. The user picks it in *Advanced → Load a Mod*, or the shortcut passes `mod="\Mods\MyMod"`.
2. The engine mounts `Mods\MyMod\Assets\` over the base `Assets\`, then loads XML, then Python entry points, then optionally the mod's DLL.
3. `ModularLoading = 1` additionally walks `Assets\Modules\` and merges each eligible file.
4. A failure in any stage is recorded in the logs and the engine continues with whatever loaded, so the symptom is a missing feature, not a refusal to start.

## What a Mod Can Replace

| Asset class | Replace by path | Add via modular loading |
|-------------|-----------------|-------------------------|
| XML table (`CIV4UnitInfos.xml`, …) | Yes, whole file | Yes |
| Text (`Assets\XML\Text\*.xml`) | Yes, whole file | Yes, and text files merge readily because each row is independent |
| Art defines (`CIV4ArtDefines_*.xml`) | Yes, whole file | Yes |
| Python (any `.py` under `Assets\Python\`) | Yes, whole file | Yes — a new module is simply imported by name |
| `Assets\XML\GlobalDefines.xml`, `GlobalDefinesAlt.xml` | Yes, whole file | `GlobalDefinesAlt.xml` exists to be merged; per-mod `*_GlobalDefines.xml` files are the conventional addition point |
| `GameFont.tga` | Yes | No — it is an image, not a table |
| DDS/NIF/KFM/WAV art | Yes or add under any path the XML names | No concept of merging; the art define names the path |
| `CvGameCoreDLL.dll` | Yes | n/a — one DLL per mod, matching expansion and patch |
| `Screens\CvMainInterface.py` and peers | Yes, whole file | n/a — two mods replacing the same screen conflict |

## Modular Loading

Modular loading lets a mod add rows to a table without shipping the table. Rules, all of which are fail-silent:

- `ModularLoading = 1` in the mod's ini.
- The file lives anywhere under `Assets\Modules\` — the usual convention is one folder per contributor (`Assets\Modules\MyMod\`) and one folder per added civilization (`.../Aborigines/Nulla Nulla/`), with the files named `<Owner>_CIV4<Table>.xml`.
- **A modular file ships its own schema copy and names it in the `xmlns`.** A real modular unit file declares `xmlns="x-schema:Nulla_Nulla_CIV4UnitSchema.xml"` and sits beside a renamed copy of `CIV4UnitSchema.xml`. The engine resolves that schema relative to the modular file, which is how a module can extend the vocabulary (the community's `ReplacementCondition`/expression extensions are declared exactly this way). A module with a correct root element but a missing or wrong scoped schema does not load.
- The root element and the entry element must match the target exactly (`<Civ4UnitInfos><UnitInfos><UnitInfo>…`), and the tags inside each entry follow the schema order.
- A `Type` already present in the base table is a collision; the engine does not repair it.
- Module load order is engine-decided; two modules declaring the same `Type` have no defined winner. Prefix every `Type` with the owning mod or civilization and the collision cannot arise by accident.
- Modular loading is a BtS feature. Vanilla and Warlords ignore `Assets\Modules\` entirely.

The practical consequence: additions are modular, modifications are whole-file replacements. A mod that both adds units and retunes a vanilla unit therefore ships both a module file and a full `CIV4UnitInfos.xml`; the module is merged into the replacement, not into the base file, so the replacement must itself contain the vanilla definitions the module expects.

## Load Order, Merging, and Conflict

- **Only one mod is active at a time.** Civ4 has no mod-stacking; the base tree plus one mod plus that mod's modules is the whole world.
- **Therefore "mod merging" means building one mod out of several**, not enabling several. Merging is done by hand, by diffing the two mods' XML, resolving each table, and concatenating the Python side with explicit imports.
- A BtS patch bumps the base tree; a mod's copied XML silently pins the pre-patch numbers. After each patch, diff the mod's tables against the new base tables and port forward.
- `Assets\Modules\` files load after the base tree and after the mod's own replacements. Order between two module files is not user-controllable.

## Installation and Distribution

- Distribution is a folder copy: put `Mods\MyMod\` into the target install. An installer (NSIS is the community standard) simply unpacks that folder and optionally places a desktop shortcut carrying `mod="\Mods\MyMod"`.
- A mod that ships a DLL must state the exact expansion and patch level it was built against.
- A scenario is installed into `PublicMaps\` or `Saves\WorldBuilder\` and is loaded from the scenarios list, not the mod list.
- A mod that only replaces art and text is save-compatible; a mod that changes table rows that a save references by index is not.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Mod appears in the list, game looks vanilla | XML file never loaded, or the file's root element or tag order was rejected | Check the loader log; validate against the shipped `*Schema.xml` |
| A modular file has no effect | `ModularLoading` is not `1`, or the file is outside `Assets\Modules\`, or its entry element does not match | Set the ini key, move the file, match the shape |
| One added unit is missing, the rest load | Its `Class`, `ArtDefineTag`, or a referenced `TXT_KEY` is absent | Walk the dependency chain and check every referenced `Type` |
| New text shows as `TXT_KEY_…` | The text row is absent, or `Assets\XML\Text\*.xml` was replaced without the new row | Add the row to the mod's own text file rather than replacing a vanilla one |
| Mod crashes on load after an edit | An unclosed tag, a wrong tag order, or a duplicate `Type` | Revert the last edit; re-apply against a copied vanilla entry |
| Mod works, then breaks after Steam verifies files | The mod edited the base tree | Move the change into the mod folder |
| Icon shows the wrong picture | The `Button`'s font-index or atlas coordinates are wrong | Correct the index against the font sheet's index comment |
