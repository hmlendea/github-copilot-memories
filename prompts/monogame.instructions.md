---
description: "Use when working with XNA, MonoGame, or NuciXNA. Covers GuiImage, GuiText, control lifecycle, child registration, and screen registration rules."
---
## XNA / MonoGame with NuciXNA

- When NuciXNA packages are present, ALWAYS use `GuiImage` instead of raw `Texture2D` fields/dictionaries for loading and holding textures. NEVER use `NuciContentManager.Instance.LoadTexture2D(...)` directly when `GuiImage` can be used instead.
- When NuciXNA packages are present, ALWAYS use `GuiText` instead of raw `SpriteFont` / `SpriteBatch.DrawString(...)` for text rendering.
- The lifecycle (LoadContent, UnloadContent, Update, Draw) of ANY `GuiControl` is managed entirely by the NuciXNA GUI Manager — NEVER call those methods directly on any control.
- Inside a `GuiControl` subclass: register child controls via `RegisterChildren(...)` or `RegisterChild(...)`.
- Inside a `Screen` subclass: register controls via `GuiManager.Instance.RegisterControls(...)` or `GuiManager.Instance.RegisterControl(...)`.
- There are NO exceptions to the registration rule — do not manually call LoadContent/UnloadContent/Update/Draw on any GuiControl.
