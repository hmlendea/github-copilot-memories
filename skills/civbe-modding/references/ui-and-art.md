# UI and Art

CivBE's UI is Civ5's: declarative `Context` XML that builds a control tree, plus Lua that reaches the controls through the global `Controls` table and registers behaviour with `RegisterCallback`. The Civ5 skill's `ui-and-art.md` documents the context rules, the `Instance`/`InstanceManager` pattern, the `Replace` hazard, icon atlases, and `.fxsxml`/`.gr2` art in full. This file records the Beyond-Earth specifics and the critique the forum reference `Reference - UI Controls - comparison with CivV` raised.

## Context XML

```xml
<Context Name="MyModPanel">
    <Container ID="RootContainer" Anchor="L,T" Size="400,300" Offset="100,100" Hidden="0">
        <Label ID="Title" String="[COLOR_POSITIVE_TEXT]MyMod[ENDCOLOR]" Font="TwCenMT20" />
        <Button ID="ActionButton" Anchor="L,T" Offset="10,10" Size="120,40"
                Texture="Art/MyButton.dds" />
    </Container>
</Context>
```

```lua
local function OnActionClicked()
    print("MyMod: button clicked")
end

Controls.ActionButton:RegisterCallback(Mouse.eLClick, OnActionClicked)
```

A renamed or un-ID'd control fails at the registration line, not at click time, so read the first `Lua.log` error rather than the visible absence.

## Beyond-Earth UI Differences

- The engine is Civ5's, so the control vocabulary is close, but the reference thread `Reference - UI Controls - comparison with CivV` exists precisely because several controls behave differently and some Civ5 controls are absent. Check a control against the shipped `assets/` UI before copying a Civ5 example.
- **The sponsor-select and load screens are Beyond-Earth-specific.** A sponsor's `IntroductionImage`, `IntroductionQuote`, and `IntroductionAudio` feed the load screen directly (`content-definitions.md`), and the sponsor-select screen reads the icon atlases and the personality.
- **Modularity is weak, as in Civ5.** Most UI work replaces an entire vanilla Lua/XML file, so only one such mod can win the file. Use registration libraries rather than shipping your own replacement of the identical file.
- **An `InGameUIAddin` pointed at a `.lua`** receives the shared base context, not its own; `ContextPtr:SetHide` and control creation are not available there. Point entry points at the `Context` XML for real panels.

## Icon Atlases

Icons are DDS files registered by size. The sponsor-icon work is the best-documented Beyond-Earth case, from the `Custom Sponsor Tutorial` icon step and the `Info about UI image files in CBE` reference.

```xml
<GameData>
  <IconTextureAtlases>
    <Row>
      <Atlas>CIV_COLOR_ATLAS_MYMOD</Atlas>
      <IconSize>128</IconSize>
      <Filename>IconAtlas_MyMod_128x128.dds</Filename>
      <IconsPerRow>1</IconsPerRow>
      <IconsPerColumn>1</IconsPerColumn>
    </Row>
    <!-- Repeat the row for every size the UI requests: -->
    <!-- Icon Atlases (colour): 128, 64, 45, 32 -->
    <!-- Alpha Atlases:         48, 32, 24       -->
  </IconTextureAtlases>
</GameData>
```

The `<Atlas>` tag names the set — all sizes of one icon share it — and the sponsor's `<IconAtlas>`/`<AlphaIconAtlas>` columns must carry exactly that name. Sizes 80 and 57 also exist in the vanilla atlases and are widely reported unused.

| DDS format | Alpha | Relative size | Use for |
|------------|-------|---------------|---------|
| ARGB 8.8.8.8 | full | largest | maximum quality; the format most vanilla files use |
| DXT5 | interpolated (gradients) | approximately a quarter of ARGB | icons and art with soft transparency |
| DXT1 | none | approximately an eighth of ARGB | splash images and opaque art |

Save UI art without mip maps — they only add size here. Crop the atlas to the icons you actually ship; leaving one icon on an untouched 8x8 template multiplies the file and VRAM cost by sixty-four.

Icon composition, per the identical reference: the colour map is the visible artwork and carries the alpha channel that indicates what shows through (black conceals, white reveals, grey is partial). The alpha atlas is the logo alone in solid white with the shape in the alpha channel, because the game recolours those instances.

Two warnings from the reference that save wasted effort:

- **Gradient and glow maps are present in the code and in vanilla archives but have no visible effect**, so do not spend time on them.
- **Some shipped DDS files are DXT4**, which most viewers, GIMP, and the Windows photo viewer render blank; the file is not corrupt and the usual DXT1/DXT3/DXT5 repack works once you can open it at all.

## Extracting Vanilla Art

Vanilla art is packed in `.fpk` archives under `Resource\dx11\` and `Resource\common\`. The extraction procedure, from the forum thread `Extracting art assets`:

1. `Dragon UnPACKer` (or the dormant Firaxis unpacker) opens an `.fpk` and lists its contents; extract the files you require, optionally converting to PNG/BMP/TGA on the way out.
2. `.dds` entries are run-length encoded; a viewer displays them scrambled until the paired `-index` file is used, or a decompressor such as the community DDS unpacker is applied.
3. Some entries are DXT4 and open in Photoshop only; the practical workaround is to open, then resave as DXT3 with alpha.

Locate the file you require by grepping the shipped XML for the atlas or art-define name, then locate that file in the archive.

## Where Extracted Art Must Be Applied

An extracted or edited texture used at runtime must be imported into the VFS under the vanilla relative path (identical file name, path and capitalisation must match on Linux, so prefer lower case throughout) and the matching `Reload*System` flag set in ModBuddy. If the VFS route does not take effect, the documented alternatives are a fake DLC, or `LooseFilesOverridePAK = 1` in `config.ini` plus a copy into the game's assets folder.

## Units and Leaders in 3D

- `UnitArtInfos` and `UnitMemberArtInfos` are replaced wholesale, which is why unit-art mods conflict with each other; a mod that touches one member art wins or loses the entire set.
- 3D work uses the identical toolchain as Civ5 (Nexus for export/import, Blender for models and animations). The forum thread `Fun with fxsxml and unit animations for CivBE` is the practical reference for the animation side.
- Recolouring and rescaling an existing unit is considerably cheaper than authoring one: the textures can be edited directly, the `.fxsxml` scale and member count adjusted, and the result referenced by a novel `UnitArtInfo`. Case reports caution that the engine dislikes repeated in-place edits of an identical model or texture — export each iteration under a novel name and revise the code reference.
- 3D leader scenes are the expensive frontier and most modded sponsors ship a 2D portrait plus the vanilla leaderhead.

## Font Icons

Font icons use the identical `ggxml` map plus a same-named `.dds` pairing as Civ5, imported into the VFS. The forum thread `Reference - Font Icons` lists the shorthand codes the vanilla interface uses in text markup.
