---
description: "Use when writing or editing C# code. Covers line splitting and indentation rules."
applyTo: "**/*.{cs}"
---
## C#

### Line Splitting & Indentation

#### Control Flow Conditions

- When an `if` condition contains multiple sub-conditions joined by `&&` or `||` **and** the full condition text exceeds 72 characters, split each sub-condition onto its own line with the logical operator placed at the **end** of the line (not the start). Continuation lines are indented by one extra level (4 spaces) relative to the `if` keyword. Do NOT split conditions that fit within 72 characters. Example:
  ```csharp
  if (GameData.TileWalkability is not null &&
      tileId < GameData.TileWalkability.Length &&
      GameData.TileWalkability[tileId] != 0)
  {
      return new Colour(20, 60, 120);
  }
  ```

#### Return Expressions

- When a `return` expression spans multiple lines, place `return` alone on the first line and indent the expression. Place operators (`||`, `&&`, `+`, etc.) at the **end** of each line, not at the start of the continuation. Example:
  ```csharp
  return
      markerEven == MarkerRefPack ||
      markerEven == MarkerQfsLow ||
      markerEven == MarkerBigChunk;
  ```

#### Properties

- Each property must be on its own line, separated by a blank line from adjacent members.
- When a property has both `get` and `set` accessors (or any combination of accessors with bodies), each accessor must be on its own line inside the property block. Placing multiple accessors on the same line is NEVER acceptable. Example:
  ```csharp
  // Wrong:
  public bool IsInterlaced { get => renderer.IsInterlaced; set => renderer.IsInterlaced = value; }

  // Correct:
  public bool IsInterlaced
  {
      get => renderer.IsInterlaced;
      set => renderer.IsInterlaced = value;
  }
  ```

#### Method Parameters & Arguments

- A parameter list (declaration) or argument list (call site) must either fit entirely on one line, or be split so that **each** parameter or argument appears on its own line with none remaining on the opening line. Mixing — placing some parameters on the same line as the method name and others on continuation lines — is never acceptable. When splitting, each parameter or argument is indented by one extra level (4 spaces) relative to the method name, and the closing `)` goes on its own line at the original indentation level. Split when the single-line form would exceed 96 characters. The method name itself must NEVER be split from its return type or access modifiers; only the parameter list may wrap. Example:
  ```csharp
  // Declaration - all on one line (fits within 96 characters):
  public void Move(int directionX, int directionY)
  {
      ...
  }

  // Declaration - split, each parameter on its own line:
  public void RecordCheckIn(
      string accountId,
      string locationId,
      DateTime timestamp)
  {
      ...
  }

  // Constructor - split, each parameter on its own line:
  public Camera(
      GameImage gameImageSource,
      int maxObjects,
      int maxVisibleObjects,
      int maxSceneObjects)
  {
      ...
  }

  // Call site - split, each argument on its own line:
  RecordCheckIn(
      account.Id,
      location.Id,
      DateTime.UtcNow);
  ```

#### Expression-Bodied Methods

- When a method signature is too long to fit on one line and the method is expression-bodied, place `=>` on the next line indented by 4 spaces relative to the method name, with the expression on the same line as `=>`. Example: `public void DrawNpc(int x, int y, int width, int height)\n    => inner.DrawNpc(x, y, width, height);`

- When the expression of an expression-bodied method spans multiple lines (because it is a complex expression, not because the signature is too long), place `=>` at the **end** of the signature line and spread the expression across subsequent lines, each indented by 4 spaces, with operators at the **end** of each line. A block body with `return` is **never** acceptable in this case. Example:
  ```csharp
  // Wrong:
  private static int ReadBigEndian24(byte[] data, int offset)
  {
      return
          (data[offset] << 16) | (data[offset + 1] << 8) | data[offset + 2];
  }

  // Correct:
  private static int ReadBigEndian24(byte[] data, int offset) =>
      (data[offset] << 16) |
      (data[offset + 1] << 8) |
      data[offset + 2];
  ```

- When an expression-bodied method uses a multi-line `new() { ... }` object initialiser, always place `=> new()` on the **same line** as the method signature; never on the next line. The opening `{` of the initialiser goes on the line after the signature, and the closing `}` with `;` closes the method. Example:
  ```csharp
  internal static UnitDataObject ToDataObject(this Unit model) => new()
  {
      Id = model.TypeIndex.ToString(),
      Name = model.Name,
  };
  ```

- When a method signature and the expression would together exceed 96 characters if the `=>` were placed at the end of the signature line, move `=>` to the **next line** indented by 4 spaces, with the expression on the same line as `=>`. This applies even if the expression itself is simple and fits on one line. Example:
  ```csharp
  // Wrong (exceeds 96 characters):
  private static string FormatBalance(decimal balance) =>
      $"{balance:0.00} {DashboardConstants.CurrencyCode}";

  // Correct:
  private static string FormatBalance(decimal balance)
      => $"{balance:0.00} {DashboardConstants.CurrencyCode}";
  ```
