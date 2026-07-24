---
description: "Use when working with XNA, MonoGame, or NuciXNA. Covers GuiImage, GuiText, control lifecycle, child registration, and screen registration rules."
---

## C#

- All general instructions from `general.instructions.md` apply to C# code as well, unless explicitly overridden in this file.
- All general coding instructions from `general.coding.instructions.md` apply to C# code as well, unless explicitly overridden in this file.
- All C# coding instructions from `csharp.coding.instructions.md` apply to MonoGame/XNA code as well, unless explicitly overridden in this file.
- All C# logging instructions from `csharp.logging.instrutions.md` apply when writing logging code.

### XNA / MonoGame with NuciXNA

- When NuciXNA packages are present, ALWAYS use `GuiImage` instead of raw `Texture2D` fields/dictionaries for loading and holding textures. NEVER use `NuciContentManager.Instance.LoadTexture2D(...)` directly when `GuiImage` can be used instead.
- When NuciXNA packages are present, ALWAYS use `GuiText` instead of raw `SpriteFont` / `SpriteBatch.DrawString(...)` for text rendering.
- The lifecycle (LoadContent, UnloadContent, Update, Draw) of ANY `GuiControl` is managed entirely by the NuciXNA GUI Manager; NEVER call those methods directly on any control.
- Inside a `GuiControl` subclass: register child controls via `RegisterChildren(...)` or `RegisterChild(...)`.
- Inside a `Screen` subclass: register controls via `GuiManager.Instance.RegisterControls(...)` or `GuiManager.Instance.RegisterControl(...)`.
- There are NO exceptions to the registration rule; do not manually call LoadContent/UnloadContent/Update/Draw on any GuiControl.
- Always use `Point2D.Empty` instead of `new Point2D(0, 0)`, and `Size2D.Zero` instead of `new Size2D(0, 0)`.
- The only acceptable numeric constants in layout code are measurements within the artwork itself (e.g. where an inner border starts in a texture), expressed as named constants that describe what they measure in the asset, used as numerators in proportional scaling against the texture's runtime dimensions. Always read texture dimensions at runtime via `GuiImage`; never hardcode them.
