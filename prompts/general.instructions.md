---
description: "Use when writing or editing any code. General coding rules: clean code, naming, comments, blank lines, indentation, British English, magic numbers, dead code, single responsibility, tests, source control."
applyTo: "**"
---
See also: [test-values.instructions.md](test-values.instructions.md) for standard test values to use in tests.

## General

- When editing code, actively refactor the affected areas to comply with all rules defined here — do not leave surrounding code in violation of these rules when you have touched that area.
- Respect the existing coding style in each repository, including file naming, splitting, and structure conventions.
- Always treat file and directory paths as case-sensitive, even on Windows, to ensure cross-platform compatibility.
- Always write code that handles both LF (`\n`) and CRLF (`\r\n`) line endings. Never assume a single newline style.
- All files must end with an empty line.
- Every class, file, and module must have a single, well-defined responsibility. Place methods and functions only in the class that owns that responsibility. Never create multi-responsibility buckets or utility dumping-grounds. When a class begins to serve more than one concern, split it immediately into separate, focused classes — each placed in the namespace or module that corresponds to its responsibility.
- Always remove dead code, unused imports, unused variables, redundant assignments, unused methods, obsolete fields, empty `if` blocks (conditionals with no logic inside their braces), and any other artefacts that serve no purpose. When changing existing logic, also update the README if the change affects documented behaviour or setup.
- Never use magic numbers or magic strings. Use enums for categorical values and named constants for all other fixed values. In C#, named constants must use `static [Type] [Name] =>` (a static read-only property) — never `const`.
- When an object has a "type" or "variant" (e.g. which button, which icon, etc.), always model it with an enum property — never an `int` index. The enum name should describe the category (e.g. `ButtonType`), and its values should be the specific variants (e.g. `Undo`, `Restart`, `Info`, `Settings`). The index is derived from the enum value via `(int)value` — never stored directly.
- Screen coordinates, sizes, and all layout measurements must be dynamic and relative — derived from screen size, control size, texture/spritesheet dimensions read at runtime, or other already-computed layout values. Never hardcode pixel positions or dimensions. The only acceptable numeric constants are measurements *within the artwork itself* (e.g. where an inner border starts in a texture), expressed as named constants that describe what they measure in the asset, used as numerators in proportional scaling against the texture's runtime dimensions.
- Whenever writing or editing code, if a test project or test files already exist in the repository, also write or update the tests for all affected or newly added code as part of the same change.
- Avoid code duplication. Always extract and reuse existing logic whenever it is reasonable to do so — never copy-paste code blocks, repeat the same expression in multiple places, or re-implement logic that already exists elsewhere. When making changes in an area of code, actively look for and eliminate any existing duplication in that area as part of the same change.
- Follow clean code principles, avoid design anti-patterns, and use suitable design patterns for scalable, reviewable, understandable, and well-organised code.
- Use clear, explicit variable, type, and method names with no unclear abbreviations or shortenings. This applies **everywhere**: local variables, fields, method parameters, lambda parameters, loop variables, and out-variables. Prefixes like `tex`, `msg`, `btn`, `img`, `val`, `obj`, `mgr`, `cfg`, `pos`, `dir`, `ray`, single-letter names (`t`, `x`, `n`, `m`, `e`) or single-letter/abbreviated prefixes (`tX`, `tY`, `dirX`, `dirY`, `rayX`, `rayY`, `checkX`, `len`, `min`, `max`, `dmg`, `str`, `acc`, `def`) are forbidden — always write the full descriptive name (e.g. `textureYOffset`, `directionX`, `rayPositionX`, `samplePositionX`, `magnitude`, `minimumDamage`, `maximumDamage`, `damageRoll`, `attackerStrength`). Lambda parameters follow the same rule without exception: `items.Select(item => item.Name)`, never `items.Select(i => i.Name)` or `items.Select(x => x.Name)`.
- Use British English spelling in code and related text. Prefer latinate English words where possible (e.g. "necessary" instead of "needed"). Key spelling differences: `normalise` (not `normalize`), `serialise` (not `serialize`), `initialise` (not `initialize`), `colour` (not `color`), `behaviour` (not `behavior`), `centre` (not `center`), `licence` (not `license` for the noun), `recognise` (not `recognize`), `synchronise` (not `synchronize`). Apply this to all identifiers, method names, comments, and strings.
- Keep code self-explanatory and avoid comments unless they are exceptional and genuinely useful.
- Always place at least one space after `//` at the start of a comment: `// text`, never `//text`.
- Inline and block comments must always begin with an uppercase letter and end with a period: `// Calculates the wall distance.`
- TODO comments must always use the exact format `// TODO: Description.` (uppercase TODO, colon, space, sentence ending with period).
- Never use tabs for indentation — always use 4 spaces per indent level.
- Lines must not exceed 96 characters (including indentation and whitespace). When a line is too long, split it across multiple lines. Place the line break before a method call, argument, or operator so that the continuation is indented by one extra level relative to the opening statement. For example, in C#:
  ```csharp
  // Method call chain — break before the chained call:
  DataStoreSettings dataStoreSettings = app.ApplicationServices
      .GetRequiredService<DataStoreSettings>();

  // Long argument — break after the opening parenthesis:
  string directory = Path.GetDirectoryName(
      dataStoreSettings.ProductKeysStorePath);
  ```
- Licence new projects under GPL v3 unless the repository already uses a different licence.
- Use proper grammar in all text, including log messages, test names, comments, and user-facing strings (for example: "Appends the `sdkInitialisationKey` with ...", "when the endpoint already ...", "Already has a query string", "Added Dispose() in the factory.", "The session token retrieval has failed"), instead of variants that omit "the", "has", "a", "an", etc.

## Source Control

- Default branch name: `master`.
- Merge strategy: default (no fast-forward flags or special strategies unless the repository already specifies otherwise).
- Pull strategy: rebase (`git pull --rebase`).
