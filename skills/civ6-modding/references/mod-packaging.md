# Mod Packaging, Actions, Criteria, Load Order, and Publishing

## Paths

| Purpose | Windows |
|---------|---------|
| User data | `%USERPROFILE%\Documents\My Games\Sid Meier's Civilization VI` |
| Installed / deployed mods | `<user data>\Mods\<ModName>\` (contains `ModName.modinfo` and the payload) |
| Settings | `<user data>\AppOptions.txt` (`[Debug] EnableTuner`, `FullScreen`) |
| Logs | `<user data>\Logs\` |
| Cache databases | `<user data>\Cache\DebugGameplay.sqlite`, `DebugLocalization.sqlite`, `DebugConfiguration.sqlite` (per some guides under `%LOCALAPPDATA%\Firaxis Games\Sid Meier's Civilization VI\Cache`) |
| Game assets (reference only) | `<steam>\steamapps\common\Sid Meier's Civilization VI\Base\`, `DLC\Expansion1\`, `DLC\Expansion2\` |
| Steam Workshop content | `<steam>\steamapps\workshop\content\289070\<id>` |
| Debug panels | `<steam>\steamapps\common\Sid Meier's Civilization VI\Debug\*.ltp` |

The macOS and Linux builds relocate user data (Aspyr prefix); locate it by running the game once and finding `Logs/modding.log` rather than assuming a path. The SDK only exists on Windows.

## ModBuddy

Installed as the Steam tool *Sid Meier's Civilization VI Development Tools*. The *Development Assets* package is optional and only needed for art authoring; its absence produces the build error `The "GeneratePantryPaths" task was not given a value for the required parameter "AssetsPath"`.

1. `File → New → Project` and pick a starter template (the templates already contain the correct action skeleton).
2. Project name becomes the mod name; keep it ASCII.
3. **Properties** edits the `.modinfo`: `Name`, `Description`, `Teaser`, `Authors`, `CompatibleVersions`, `AffectsSavedGames`, `SupportsSinglePlayer`/`SupportsMultiplayer`.
4. **FrontEndActions** run during setup (ruleset and map-option work). **InGameActions** run when a game starts.
5. **ActionCriteria** defines the criteria an action can be gated on.
6. `Ctrl+Shift+B` builds and deploys straight into `<user data>\Mods\`.

Everything the properties pages produce is plain XML in the `.modinfo`; hand-editing is supported and is often faster for many files, but re-check after editing properties in the UI.

## Action Types

| Action | Purpose | Typical payload |
|--------|---------|-----------------|
| `UpdateDatabase` | Run SQL/`GameData` XML against the gameplay database | `Data/*.sql`, `Data/*.xml` |
| `UpdateText` | Run SQL against the localisation database | `Text/*.sql` |
| `ImportFiles` | Copy files into the game's file context so they can be opened by path | UI `.lua`, art, `.dds`, models |
| `UpdateArt` | Load a cooked art package | a `.dep` (game dependency data) file |
| `UpdateColors` | Register player/civilization colours | a `GameInfo` XML with the colour tables |
| `UpdateAudio` | Load a Wwise sound bank | `Platforms/Windows/Audio/*.ini` plus `.bnk`/`.wem` files |
| `UpdateLogitechARX` | Register LCD images | `.png` files |
| `AddGameplayScripts` | Load a Lua file into the gameplay context | `Scripts/*.lua` |
| `AddUserInterfaces` | Load a UI context at startup | `UI/*.xml` |
| `UpdateIcons` | Register icon atlases and definitions | `Icons/*.xml` (`IconTextureAtlases`, `IconDefinitions`) |
| `ReplaceUIScript` | Replace one vanilla UI Lua context wholesale | `LuaContext`, `LuaReplace` properties |

Every action accepts `<Properties>` with `<LoadOrder>` (higher runs later) and `UpdateText` files accept `<File Priority="N">`. Use `LoadOrder` when your statements must run after another mod's; do not rely on alphabetical file names.

An action's criteria can be given either as an attribute (`criteria="Expansion2"`) or as a child element:

```xml
<UpdateDatabase id="Gameplay">
  <Criteria>Expansion2</Criteria>
  <File>Data/MyMod_XP2.xml</File>
</UpdateDatabase>
```

Both forms appear in published mods and are equivalent.

Two wiring rules cause most "my mod does nothing" reports:
- A Lua file given to `AddGameplayScripts` must **also** appear in `<Files>`, or it never reaches the game.
- A UI file in `AddUserInterfaces` needs its paired `.lua` in `ImportFiles` (and usually in `<Files>`), because the context loads the script by path.

```xml
<InGameActions>
  <UpdateDatabase id="Data">
    <Properties><LoadOrder>100</LoadOrder></Properties>
    <File>Data/MyMod.sql</File>
  </UpdateDatabase>
  <UpdateText id="Text">
    <File>Text/MyMod_Text.xml</File>
  </UpdateText>
  <UpdateIcons id="Icons">
    <File>Icons/MyMod_Icons.xml</File>
  </UpdateIcons>
  <ImportFiles id="Runtime">
    <File>Icons/MyMod_Icons32.dds</File>
    <File>UI/MyModPanel.lua</File>
  </ImportFiles>
  <AddUserInterfaces id="UI">
    <Properties><Context>InGame</Context></Properties>
    <File>UI/MyModPanel.xml</File>
  </AddUserInterfaces>
</InGameActions>
<Files>
  <File>Data/MyMod.sql</File>
  <File>Text/MyMod_Text.xml</File>
  <File>Icons/MyMod_Icons.xml</File>
  <File>UI/MyModPanel.lua</File>
  <File>UI/MyModPanel.xml</File>
</Files>
```

`AddUserInterfaces` context values in use: `InGame`, `FrontEnd`. A `FrontEnd` context that touches gameplay managers fails at the main menu; keep main-menu UI separate from in-game UI, and duplicate an `ImportFiles` action into both `FrontEndActions` and `InGameActions` when a file is needed in both.

`ImportFiles` accepts either direct `<File>` children or an `<Items>` wrapper; both appear in published mods and are equivalent.

## Action Criteria and Rulesets

```xml
<ActionCriteria>
  <Criteria id="Expansion1"><GameCoreInUse>Expansion1</GameCoreInUse></Criteria>
  <Criteria id="Expansion2"><GameCoreInUse>Expansion2</GameCoreInUse></Criteria>
  <Criteria id="Expansion2RuleSet"><RuleSetInUse>RULESET_EXPANSION_2</RuleSetInUse></Criteria>
</ActionCriteria>
```

Reference a criteria with `criteria="Expansion2"` on the action. Semantics that matter:
- No `criteria` attribute → the action runs under **every** game core and ruleset.
- A criteria that does not match the running game → the action never runs, silently.
- `GameCoreInUse` matches the installed core (`Expansion1`, `Expansion2`); `RuleSetInUse` matches the active ruleset and accepts a comma-separated list; `ModInUse` matches an enabled mod's GUID.
- Other criteria children seen in published mods include `<LeaderPlayable>` — a comma-separated `Table:Collection::KEY` list used for DLC presence checks. Additional children exist, so read a vanilla `.modinfo` under `Base/` instead of guessing.
- To target base plus one expansion, duplicate the action with different ids and criteria.
- Content referencing `_XP1`/`_XP2` tables must be gated; those tables do not exist in the base core.

## Dependencies, References, Blocks

| Element | Meaning |
|---------|---------|
| `<Dependencies>` | Hard requirement; the mod is rejected without them, and load order is resolved to load this mod after them |
| `<References>` | Soft requirement; loads earlier if present, no error if absent |
| `<Blocks>` | Declared incompatibility; the game refuses to enable both |

Dependencies name a `<Mod id="GUID" title="..."/>`; published content mods depend on the expansion pseudo-mods (`1B28771A-C749-434B-9053-D1380C553DE9` = Rise and Fall, `4873eb62-8ccc-4574-b784-dda455e74e68` = Gathering Storm) instead of, or in addition to, criteria gating. Use `Dependencies` when another mod's content is queried at load, `References` when a modifier or UI hook is merely improved by it, and `Blocks` only for genuine conflicts — normally whole-file UI replacements or overlapping `Types` keys.

`<Properties>` also carries `<SubscriptionID>` on uploaded mods (the Workshop item id) and `<SupportsMultiplayer>`, `<Homepage>`, `<Teaser>`, `<CompatibleVersions>`.

## Load Order

The engine resolves dependencies first and then applies the remaining mods in the order recorded in `Logs/modding.log`; users cannot reorder mods from the UI. Consequences:
- When two mods define the same key, the later one wins unless it uses `INSERT OR REPLACE` against a row it does not own. Never rely on winning silently; delete or scope the conflicting key.
- UI files are whole-file replacements, so only one mod can own a given vanilla context file.
- Declare a dependency on anything whose rows you `UPDATE`; otherwise a user without it gets a statement error.

## Compatibility and Saved Games

- Set `AffectsSavedGames` to `1` when the mod changes existing saves' database shape; the game then warns that saves cannot be loaded without it.
- Adding or removing mods mid-game is safest when the mod only adds types; removing a type that a save references breaks it.
- Multiplayer requires an identical enabled set on every client; a differing ruleset criteria or load order desynchronises immediately.
- Record the tested patch level and expansions in the description; `CompatibleVersions` is advisory.

## Publishing

1. Build, deploy, and playtest with the cache deleted.
2. Upload with the SDK's *Steam Workshop Uploader*: it uses the mod's id, `Name`, `Description`, and a preview image.
3. Workshop descriptions can reference the mod's own `LOC_*` keys only within the mod; the page text itself is plain text.
4. Re-upload after a patch only after verifying the cache snapshot again.

If Steam is holding file handles, builds fail with a SevenZip/`MSB` error; exit Steam, run the SDK executable directly, build, then sign back in before uploading.