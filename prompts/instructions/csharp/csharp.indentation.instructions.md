---
description: "Use when writing or editing C# code. Covers line splitting and indentation rules."
applyTo: "**/*.{cs}"
---
## C#

### Line Splitting & Indentation

#### Control Flow Conditions

- Multi-clause `if` conditions exceeding 72 characters: one clause per line, operator (`&&`/`||`) at line end, continuation indented 4 spaces. Do not split conditions within 72 characters. Example:
  ```csharp
  if (GameData.TileWalkability is not null &&
      tileId < GameData.TileWalkability.Length &&
      GameData.TileWalkability[tileId] != 0)
  {
      return new Colour(20, 60, 120);
  }
  ```

#### Return Expressions

- Multi-line return: `return` alone, expression indented, operators (`||`, `&&`, `+`, etc.) at line ends. Example:
  ```csharp
  return
      markerEven == MarkerRefPack ||
      markerEven == MarkerQfsLow ||
      markerEven == MarkerBigChunk;
  ```

#### Properties

- One property per line, separated from adjacent members by a blank line.
- Accessors with bodies: one accessor per line; never combine them. Example:
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

- Parameter/argument lists exceeding 96 characters: none on the opening line; one per line, indented 4 spaces; closing `)` at original indentation. Never mix inline and continued items. Keep method name with modifiers and return type; wrap only the list. Example:
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

- Long expression-bodied signature: next-line `=>` indented 4 spaces, followed by its expression. Example: `public void DrawNpc(int x, int y, int width, int height)\n    => inner.DrawNpc(x, y, width, height);`

- Multi-line expression: `=>` ends the signature; expression lines indent 4 spaces; operators end lines. Never replace it with a block-body `return`. Example:
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

- Multi-line `new()` initialiser: signature ends with `=> new()`; `{` starts next line; `};` closes method. Example:
  ```csharp
  internal static UnitDataObject ToDataObject(this Unit model) => new()
  {
      Id = model.TypeIndex.ToString(),
      Name = model.Name,
  };
  ```

- Signature plus expression exceeding 96 characters: next-line `=>` indented 4 spaces with expression, even when expression alone fits one line. Example:
  ```csharp
  // Wrong (exceeds 96 characters):
  private static string FormatBalance(decimal balance) =>
      $"{balance:0.00} {DashboardConstants.CurrencyCode}";

  // Correct:
  private static string FormatBalance(decimal balance)
      => $"{balance:0.00} {DashboardConstants.CurrencyCode}";
  ```
