---
name: csharp-monogame
description: Use when working with XNA, MonoGame, or NuciXNA C# code, especially GUI controls, screens, textures, text rendering, layout, or control lifecycle.
---

# C# MonoGame / NuciXNA

Apply these rules whenever the task involves XNA, MonoGame, or NuciXNA:

- When NuciXNA packages are present, use `GuiImage` instead of raw `Texture2D` fields or dictionaries for loading and holding textures. Do not call `NuciContentManager.Instance.LoadTexture2D(...)` directly when `GuiImage` can be used.
- When NuciXNA packages are present, use `GuiText` instead of raw `SpriteFont` or `SpriteBatch.DrawString(...)` for text rendering.
- Let the NuciXNA GUI Manager fully manage `GuiControl` lifecycle methods (`LoadContent`, `UnloadContent`, `Update`, and `Draw`). Never call those methods directly on a control.
- Inside a `GuiControl` subclass, register child controls through `RegisterChildren(...)` or `RegisterChild(...)`.
- Inside a `Screen` subclass, register controls through `GuiManager.Instance.RegisterControls(...)` or `GuiManager.Instance.RegisterControl(...)`.
- There are no exceptions to the registration rule; never manually call `LoadContent`, `UnloadContent`, `Update`, or `Draw` on a `GuiControl`.
- Use `Point2D.Empty` instead of `new Point2D(0, 0)` and `Size2D.Zero` instead of `new Size2D(0, 0)`.
- In layout code, numeric constants are limited to measurements within the artwork itself, expressed as named constants describing what they measure in the asset and used as numerators in proportional scaling against runtime texture dimensions. Read texture dimensions at runtime through `GuiImage`; never hardcode them.
