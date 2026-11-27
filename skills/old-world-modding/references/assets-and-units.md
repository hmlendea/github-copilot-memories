# Assets and Units

Basic XML modding needs only a text editor. Asset and UI work requires the Unity version supported by the installed game, a compatible asset template, an image editor, and an asset-bundle build workflow. The wiki recommends PNG images, preferably with dimensions divisible by four; verify current import requirements.

Asset extraction tools such as AssetStudio can inspect installed bundles. Extract for reference only; do not edit the game's bundles.

## Custom units

A documented custom unit normally requires:

- `asset-add.xml` for prefab and animation-clip asset paths;
- `modUnit-add.xml` for the model and animation assignments;
- `formation-add.xml` for model usage, display rules, and formation details;
- `unit-add.xml` for gameplay behaviour, or `unit-change.xml` to attach a custom model to an existing unit.

The `modUnit` asset should be a prefab with a `SkinnedMeshRenderer` and `Animator` using the correct rig avatar. Animation fields include attack, building idle, combat idle, death, fortify, harvest, hidden idle, hit, idle, and spread-religion clips. Use the installed XML and asset template as the schema authority.

Build and test one asset or unit first. Check the output log before adding more content.
