---
description: "Use when writing or editing any code. General coding rules: clean code, naming, comments, blank lines, indentation, British English, magic numbers, dead code, single responsibility, tests, source control."
applyTo: "**"
---
See also: [test-values.instructions.md](test-values.instructions.md) for standard test values to use in tests.

## General

- When editing code, actively refactor the affected areas to comply with all rules defined here; do not leave surrounding code in violation of these rules when you have touched that area.
- When refactoring, all public-facing contracts must remain 100% backwards compatible. This includes UI visuals, CLI interfaces, API contracts, library public APIs, serialised output formats, and any other surface that an end-user or external client directly interacts with or depends on. Internal restructuring must never alter observable behaviour.
- Respect the existing coding style in each repository, including file naming, splitting, and structure conventions.
- Always treat file and directory paths as case-sensitive, even on Windows, to ensure cross-platform compatibility.
- Always write code that handles both LF (`\n`) and CRLF (`\r\n`) line endings. Never assume a single newline style.
- All files must end with an empty line.
- Every class, file, and module must have a single, well-defined responsibility. Place methods and functions only in the class that owns that responsibility. Never create multi-responsibility buckets or utility dumping-grounds. When a class begins to serve more than one concern, split it immediately into separate, focused classes, each placed in the namespace or module that corresponds to its responsibility.
- Always remove dead code, unused imports, unused variables, redundant assignments, unused methods, obsolete fields, empty `if` blocks (conditionals with no logic inside their braces), and any other artefacts that serve no purpose.
- After every edit, explicitly check for and remove any imports or `using` directives that are no longer referenced. This is MANDATORY and must never be skipped, even when the change seems unrelated to imports.
- Never use magic numbers or magic strings. Use enums for categorical values and named constants for all other fixed values. In C#, named constants must use `static [Type] [Name] =>` (a static read-only property), not `const`.
- When an object has a "type" or "variant" (e.g. which button, which icon, etc.), always model it with an enum property, not an `int` index. The enum name should describe the category (e.g. `ButtonType`), and its values should be the specific variants (e.g. `Undo`, `Restart`, `Info`, `Settings`). In C#, the index is derived from the enum value via `(int)value` and is never stored directly.
- Screen coordinates, sizes, and all layout measurements must be dynamic and relative, derived from screen size, container dimensions, or other already-computed layout values. Never hardcode pixel positions or dimensions.
- Whenever writing or editing code, if a test project or test files already exist in the repository, also write or update the tests for all affected or newly added code as part of the same change.
- When writing tests, write a large number of test cases covering a wide range of input values and edge cases. Aim for 100% branch coverage. Every distinct code branch must have at least one dedicated test that targets it directly; do not rely solely on other tests that happen to pass through that branch indirectly. Write multiple test cases per branch where different input values could reveal different behaviour.
- Avoid code duplication. Always extract and reuse existing logic whenever it is reasonable to do so; never copy-paste code blocks, repeat the same expression in multiple places, or re-implement logic that already exists elsewhere. When making changes in an area of code, actively look for and eliminate any existing duplication in that area as part of the same change.
- Follow clean code principles, avoid design anti-patterns, and use suitable design patterns for scalable, reviewable, understandable, and well-organised code.
- Use clear, explicit variable, type, and method names with no unclear abbreviations or shortenings. This applies **everywhere**: local variables, fields, method parameters, lambda parameters, loop variables, and out-variables. Prefixes like `tex`, `msg`, `btn`, `img`, `val`, `obj`, `mgr`, `cfg`, `pos`, `dir`, `ray`, single-letter names (`t`, `x`, `n`, `m`, `e`) or single-letter/abbreviated prefixes (`tX`, `tY`, `dirX`, `dirY`, `rayX`, `rayY`, `checkX`, `len`, `min`, `max`, `dmg`, `str`, `acc`, `def`) are forbidden; always write the full descriptive name (e.g. `textureYOffset`, `directionX`, `rayPositionX`, `samplePositionX`, `magnitude`, `minimumDamage`, `maximumDamage`, `damageRoll`, `attackerStrength`). Lambda parameters follow the same rule without exception: `items.Select(item => item.Name)`, never `items.Select(i => i.Name)` or `items.Select(x => x.Name)`.
- Use British English spelling in code and related text. Prefer latinate English words where possible (e.g. "necessary" instead of "needed"). Key spelling differences: `normalise` (not `normalize`), `serialise` (not `serialize`), `initialise` (not `initialize`), `colour` (not `color`), `behaviour` (not `behavior`), `centre` (not `center`), `licence` (not `license` for the noun), `recognise` (not `recognize`), `synchronise` (not `synchronize`). Apply this to all identifiers, method names, comments, and strings.
- Keep code self-explanatory and avoid comments unless they are exceptional and genuinely useful.
- Always place at least one space after `//` at the start of a comment: `// text`, never `//text`.
- Inline and block comments must always begin with an uppercase letter and end with a period: `// Calculates the wall distance.`
- TODO comments must always use the exact format `// TODO: Description.` (uppercase TODO, colon, space, sentence ending with period).
- Never use tabs for indentation; always use 4 spaces per indent level.
- Never place a blank line immediately before a closing brace or bracket (`}`, `]`, `)`). The last statement inside a block must be followed directly by the closing delimiter with no empty line between them.
- Always place a blank line before a control flow statement (`if`, `for`, `foreach`, `while`, `do`, `switch`, `return`, `break`, `continue`, `throw`) when it is preceded by one or more non-blank, non-control-flow statements in the same block. Do not add the blank line when the control flow statement is the very first statement in the block, or when the preceding line is itself an opening brace or a control flow statement.
- Lines must not exceed 96 characters (including indentation and whitespace). When a line is too long, split it across multiple lines. Place operators (`+`, `-`, `&&`, `||`, etc.) at the end of the line, not the start of the continuation. Method chain calls (`.Method()`) break before the dot. When splitting a call with multiple arguments or parameters across multiple lines, each argument or parameter must be on its own separate line. When a `return` statement's expression spans multiple lines, place `return` alone on the first line and indent the expression. When an expression-bodied member (`=>`) is too long, break after `=>` and indent the body on the next line. For example, in C#:
  ```csharp
  // Method call chain - break before the dot:
  DataStoreSettings dataStoreSettings = app.ApplicationServices
      .GetRequiredService<DataStoreSettings>();

  // Single long argument - break after the opening parenthesis:
  string directory = Path.GetDirectoryName(
      dataStoreSettings.ProductKeysStorePath);

  // Multiple arguments - each on its own line:
  SomeMethod(
      firstArgument,
      secondArgument,
      thirdArgument);

  // Long assignment with operators - operator at end of each line:
  Point2D screenLocation =
      new Point2D(dotSprite.SpriteSize / 2) +
      ScreenLocation +
      minimapLocation;

  // Multi-line return - `return` on its own line, operator at end of each line:
  return
      IsDestinationTwoInBounds(directionX, directionY) &&
      board.Tiles[destinationX, destinationY].Id == TileId.CrateOnFloor &&
      board.Tiles[destination2X, destination2Y].Id == TileId.Floor;

  // Expression-bodied member too long - break after `=>` and indent the body:
  private static int ClampToTexture128Range(int value) =>
      Math.Clamp(value, 0, Texture128RowMask);
  ```
- Licence new projects under GPL v3 unless the repository already uses a different licence.
- Use proper grammar in all text, including log messages, test names, comments, and user-facing strings (for example: "Appends the `sdkInitialisationKey` with ...", "when the endpoint already ...", "Already has a query string", "Added Dispose() in the factory.", "The session token retrieval has failed"), instead of variants that omit "the", "has", "a", "an", etc.
- Never use characters or phrasing that indicate AI-generated content. This includes em dashes (`—`), en dashes (`–`), ellipsis characters (`…`), arrow characters (`→`), box-drawing characters, and overly verbose transitional phrases such as "it is worth noting", "it is important to", "in order to", "this ensures that", "as mentioned above". Use plain ASCII punctuation (`,`, `;`, `:`, `-`, `->`) and direct phrasing instead. Emojis are allowed in user-facing strings and the readme.

## README

- When the user asks to update or create a `README.md` (e.g. "update the readme", "create a readme", "generate the readme"), always follow the template and rules defined in `github-readme.prompt.md`.
- After every code change, check whether the `README.md` requires updating to reflect the change. If it does, update it as part of the same change.

## Source Control

- Default branch name: `master`.
- Merge strategy: default (no fast-forward flags or special strategies unless the repository already specifies otherwise).
- Pull strategy: rebase (`git pull --rebase`).
