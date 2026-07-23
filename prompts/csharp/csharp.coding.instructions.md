---
description: "Use when writing or editing C# code, .csproj, or .slnx files. Covers code style, naming conventions, type declarations, member organisation, constructors, methods, properties, collections, async, dependency injection, controller style."
applyTo: "**/*.{cs}"
---
## C#

### Code Style

- Always use explicit braces for ALL control flow (`if`, `else`, `for`, `foreach`, `while`, `switch`), even when the body is a single line or a single `continue`/`break`/`return`. Braceless single-line bodies are NEVER acceptable.
- The opening brace of a control flow block must always appear on its own line (Allman style). NEVER place the opening brace or the body on the same line as the statement: `if (condition) { ... }` is NEVER acceptable.
- `else if` must always appear on a single line. NEVER split it so that `else` is on one line and `if` is on another.
- When an `if` condition contains multiple sub-conditions joined by `&&` or `||` **and** the full condition text exceeds 72 characters, split each sub-condition onto its own line with the logical operator placed at the **end** of the line (not the start). Continuation lines are indented by one extra level (4 spaces) relative to the `if` keyword. Do NOT split conditions that fit within 72 characters. Example:
  ```csharp
  if (GameData.TileWalkability is not null &&
      tileId < GameData.TileWalkability.Length &&
      GameData.TileWalkability[tileId] != 0)
  {
      return new Colour(20, 60, 120);
  }
  ```
- Do not use redundant parentheses. Only add parentheses when they are required to override operator precedence or to clarify a genuinely ambiguous expression.
- `if`, `for`, `foreach`, `while`, `switch`, `continue`, and `break` statements must always be separated from adjacent assignments or other statements by a blank line above and below.
- `return` statements must always be separated from other lines of code by a blank line above (unless they are the only statement in the method body or the first line after an opening brace).
- When a `return` expression spans multiple lines, place `return` alone on the first line and indent the expression. Place operators (`||`, `&&`, `+`, etc.) at the **end** of each line, not at the start of the continuation. Example:
  ```csharp
  return
      markerEven == MarkerRefPack ||
      markerEven == MarkerQfsLow ||
      markerEven == MarkerBigChunk;
  ```
- Never use two or more consecutive blank lines anywhere in the code.
- Never place an empty line immediately after an opening brace `{` or immediately before a closing brace `}`. This applies to all braces without exception: type bodies, method bodies, property accessors, control flow blocks, and every other brace-delimited scope.
- Never use `#region` or `#endregion`. They are forbidden everywhere without exception.
- All C# methods must have exactly one empty line between them: no more, no less. This applies equally when a method ends with `};` (e.g. a multi-line expression-bodied method with an object initialiser): there must still be exactly one empty line before the next method.
- Never pad spaces before `=` (or any operator) to align consecutive assignments. Each assignment uses exactly one space before and after `=`.
- Prefer `+= 1` and `-= 1` over explicit self-assignments such as `a = a + 1` and `a = a - 1`.
- Always use explicit types instead of `var`.
- When a variable has a sensible default and is only conditionally overridden, initialise it with the default first and use a single `if` (no `else`) to override. Avoid `if`/`else` when the `else` branch only assigns a fallback/default value.
- Prefer the static `Equals(a, b)` form (e.g. `object.Equals(a, b)` or `string.Equals(a, b)`) over instance `.Equals()` calls or `==` for comparisons. Never call `.Equals()` directly on a potentially null reference, as doing so throws a `NullReferenceException`. Use the static form or guard with a null check first.
- NEVER use ternary expressions (`condition ? a : b`). Always use an `if`/`else` statement instead. This does NOT apply to `??=` or switch expressions.
- NEVER use `ref` parameters. Avoid `out` parameters; if returning multiple values is necessary, create a dedicated type and return an instance of it. NEVER return tuples; avoid tuples entirely.
- Use `static [Type] [Name] =>` (a static read-only property) instead of `const [Type] [Name] =`. `const` is NEVER acceptable.

### Naming Conventions

- Always use the lowercase alias for built-in types: `string`, `int`, `bool`, `object`, `long`, `double`, `float`, `decimal`, `byte`, `char`, etc. NEVER use the BCL class names `String`, `Int32`, `Boolean`, `Object`, etc.
- All `public` and `protected` members — without exception — must begin with an uppercase letter. This applies to fields, properties, methods, events, delegates, constructors, and nested types, regardless of context.
- Methods: PascalCase, clear and explicit names with no abbreviations or shortenings, following the same naming rules as for variables and parameters.
- Classes: PascalCase.
- Interfaces: `I`-prefixed PascalCase (`IAccountService`).
- Controllers: pluralized noun + `Controller` (`AccountsController`).
- Data/entity objects: `DataObject` suffix (`AccountDataObject`).
- Domain models: plain noun, no suffix (`Account`, `CheckIn`).
- Request DTOs: Verb + Noun + `Request` (`AddAccountRequest`, `RecordCheckInRequest`).
- Response DTOs: `Get` + Noun + `Response` (`GetAccountResponse`).
- Configuration classes: Noun + `Settings` (`DataStoreSettings`).
- Mapping classes: Noun + `MappingExtensions` (`AccountMappingExtensions`).
- Mapping methods: `ToServiceModel` / `ToServiceModels` for entity->model direction; `ToDataObject` / `ToDataObjects` for model->entity direction.
- Private fields: camelCase, NO underscore prefix (`accountRepository`, not `_accountRepository`).
- Boolean variables, properties, and methods must use a meaningful boolean-semantic prefix: `Is`, `Has`, `Does`, `Are`, or contextual tense-embedded forms (`...Was...`, `...Were...`, `...Is...`, `...Does...`, `...Are...`), e.g. `IsEnabled`, `HasPermission`, `DoesExist`, `AreValid`, `requestWasHandled`, `itemsAreLoaded`. Never use vague names like `flag`, `check`, or `result` for booleans.

### Type Declarations

- All classes that are not explicitly designed for inheritance must be declared `sealed`. When in doubt, default to `sealed`.
- Domain models: `public sealed class`.
- Data/entity objects: `public sealed class`.
- Configuration classes: `public sealed class`.
- Mapping extension classes: explicitly `internal static class`.
- Mapping extension methods: explicitly `internal static`.
- Implement `IEquatable<T>` on domain models and data objects where equality comparison is meaningful (e.g. value objects, data objects compared by identifier). Override `Equals(object)` and `GetHashCode()` consistently.

### Member Organisation

- ALWAYS declare the accessibility modifier explicitly on EVERY member: every field, property, event, constructor, and method must begin with `public`, `protected`, `internal`, `private`, or a valid combination. NEVER omit the modifier and rely on the implicit default. This applies even to `private` members — write `private int counter;`, NEVER just `int counter;`. Writing a field or method with no accessibility modifier is a bug.
- Order members by kind first, then by accessibility within each kind group. The top-level kind order is: fields -> properties -> events -> constructors and destructors -> methods.
- Within the fields group, order by: static readonly -> static mutable -> instance readonly -> instance mutable. Within each of those sub-groups, order by accessibility: `public` first, then `protected`, then `private`.
- Within every other kind group (properties, events, constructors, methods), order by accessibility: `public` first, then `protected`, then `private`.
- All `public` members in NuGet packages (classes, interfaces, methods, properties, constructors, fields, enums, and their members) must have XML documentation comments (`/// <summary>...</summary>`). These must NEVER be removed or omitted, including during refactoring. When a member is renamed, moved, or restructured, its XML documentation must be preserved and updated to reflect the change.
- NEVER remove a `public` member from a NuGet package during refactoring, even if it appears unused within the solution. External clients of the package may depend on it. A `public` member may only be removed when explicitly instructed to do so by the user.
- Overloaded methods must be grouped together (no unrelated members between them) and ordered from simplest/fewest parameters to most-complex/most-numerous parameters.

### Constructors & Object Creation

- Use **primary constructors** (C# 12) on all service classes, controllers, and startup classes. Parameters are used directly inside method bodies; do NOT assign them to fields.
- Use **target-typed `new()`** with object initializer syntax when instantiating models or entities: `Account account = new() { Id = x, ... };`
- Whenever a `new` expression appears on the same line as the variable/property/field declaration (so the type is already stated on the left-hand side), always use `new(...)` instead of `new [Type](...)`. Example: `private static Colour HoverTintColour => new(255, 220, 80);`; NEVER `new Colour(255, 220, 80)` in that position.

### Properties

- Use auto-properties `{ get; set; }` for all models, entities, requests, responses, and settings.
- Use expression-bodied (`=>`) for derived/computed read-only properties.
- No `init`-only properties.
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

### Methods

- Do NOT use optional parameters. Use method overloads instead.
- Keep methods small and focused on a single responsibility. If a method grows beyond ~20-30 lines or handles more than one logical concern, extract the extra logic into well-named private helper methods.
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
- Use expression-bodied (`=>`) for **any** method whose entire body is a single statement; this includes `return` expressions (`public Foo GetFoo() => foo;`), void delegation calls (`public void Reset() => inner.Reset();`), and `throw` expressions (`public void ResetCombat()\n    => throw new NotImplementedException();`). A block body `{ return x; }` or `{ Foo(); }` with a single statement is **always wrong**; use `=> x;` or `=> Foo();` instead.
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
- Use expression-bodied (`=>`) for methods whose entire body is a single `new() { ... }` initialiser; do NOT assign to a local variable and return it: `internal static Foo ToDataObject(this Bar bar) => new() { Id = bar.Id };`. This applies unconditionally to all mapping extension methods (`ToServiceModel`, `ToDataObject`, and their plurals).
- When an expression-bodied method uses a multi-line `new() { ... }` object initialiser, always place `=> new()` on the **same line** as the method signature; never on the next line. The opening `{` of the initialiser goes on the line after the signature, and the closing `}` with `;` closes the method. Example:
  ```csharp
  internal static UnitDataObject ToDataObject(this Unit model) => new()
  {
      Id = model.TypeIndex.ToString(),
      Name = model.Name,
  };
  ```

### Collections

- Use `IEnumerable<T>` as the return type and parameter type for all collections. Never `List<T>`, `IList<T>`, `IReadOnlyList<T>`, `HashSet<T>`.
- **Exception:** entity/data objects that are XML-serialised (e.g. via `XmlSerializer`) must use `List<T>` for collection properties, as the XML serialiser cannot reflect interface types.
- Use C# 12 collection expressions `[...]` for inline collection initialization of **any** collection type (`List<T>`, `Dictionary<K,V>`, arrays, etc.), including empty ones. `new List<T>()`, `new Dictionary<K,V>()`, `new T[]{}` are all wrong; use `[]` instead.
- Use LINQ (`.Where()`, `.Any()`, `.First()`, `.Select()`, `.Append()`) for in-memory querying.

### Async

- Prefer synchronous service methods. Do not add `Task<T>` return types or `async/await` unless required.
- No `CancellationToken` usage unless explicitly needed.

### Dependency Injection

- Register all services as `AddSingleton`. Do NOT use `AddScoped` or `AddTransient`.
- Centralize all DI registration in a `ServiceCollectionExtensions.cs` file with extension methods on `IServiceCollection`.

### Controller Style

- Controller actions return `ActionResult` (not `ActionResult<T>`).
- Use expression-bodied actions for single-expression delegates to a `ProcessRequest(...)` call.
