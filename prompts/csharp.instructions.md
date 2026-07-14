---
description: "Use when writing or editing C# code, .csproj, or .slnx files. Covers project structure, code style, naming conventions, type declarations, member organisation, constructors, methods, properties, null handling, exception handling, collections, async, dependency injection, controller style, and unit tests."
applyTo: ["**/*.cs", "**/*.csproj", "**/*.slnx"]
---
## C#

### Project Structure

- Always target the latest stable .NET version available.
- Always prefer `.slnx` over `.sln` solution files.
- When creating a new C# solution, place the `.slnx` file and all project directories at the repository root level (no `src/` subfolder or similar). The unit test project, where applicable, must be named `[ProjectName].UnitTests`.
- NEVER use `ImplicitUsings` or implicit namespaces. Always use explicit `using` directives. Never add `<ImplicitUsings>enable</ImplicitUsings>` to any csproj.
- Never use top-level statements or free-floating code in any file. Every file must have an explicit `namespace { }` block, a `class` (or other type) block, and all code placed inside methods, constructors, or other members. This applies to `Program.cs` too — use an explicit `Program` class with a `static void Main` entry point.
- Use block-braces namespaces (`namespace Foo { ... }`), NOT file-scoped namespaces (`namespace Foo;`).
- Each new type must be declared in its own file. File name must exactly match the class name.
- Each class must have a single, well-defined responsibility. Do not add logic to a class unless it unambiguously belongs there. If a class grows beyond its responsibility or serves multiple concerns, split it immediately into smaller, focused classes — each declared in the namespace that matches its responsibility.
- Namespace choice is driven by responsibility, not by incidental proximity. A class that handles account validation belongs in `[Root].Services.Account`, not in a generic `[Root].Services` or `[Root].Utilities` namespace. Always ask: "What is the one thing this class does?" — the answer determines its namespace and folder.
- Never create catch-all or helper namespaces (e.g. `Helpers`, `Utils`, `Common`, `Misc`, `Shared`). If you feel the need for one, it is a signal that the class has not been assigned its correct single responsibility yet.
- Organise source files by architectural layer (e.g. Controllers, Services, Repositories, Domain, DataObjects); each layer lives in its own folder. Within a layer, sub-folders (and sub-namespaces) group classes by the domain concept they serve (e.g. `Services/Account/`, `Services/CheckIn/`).
- Namespace must mirror folder structure exactly, and file location must match the namespace. A file in `Services/Account/` must declare namespace `[Root].Services.Account` — no exceptions. Whenever a namespace changes, the file must be moved to the matching folder immediately.
- Never create a `[xyz].Interfaces` namespace. Place interfaces in the same namespace and folder as their implementations.
- Never create a `[xyz].Enumerations` (or `Enums`) namespace. Place enums in the same namespace and folder as the domain models they belong to.
- All `using` directives go at the top of the file, **outside** and **above** the `namespace` block — NEVER inside it.
- NEVER use fully qualified type names inline (e.g. `OpenRS.Net.Client.Events.ContentLoadedEventArgs eventArgs`). Always add the appropriate `using` directive and reference the type by its short name (e.g. `using OpenRS.Net.Client.Events;` and `ContentLoadedEventArgs eventArgs`).
- `using` directives must be organised into the following groups, in this order, each group separated from the next by exactly one blank line. All `using` directives within each group must be sorted alphabetically.
  1. **`System.*` usings** — all namespaces rooted at `System`.
  2. **`Microsoft.*` usings** — all namespaces rooted at `Microsoft`.
  3. **NuGet / third-party package usings** — one group per package root namespace (e.g. all `Newtonsoft.*` together, all `Serilog.*` together), ordered alphabetically by package root namespace.
  4. **Current solution usings** — namespaces belonging to the solution being worked on, all in one group.
- The last `using` directive must always be separated from the `namespace` statement by exactly one blank line.

### Code Style

- Always use explicit braces for ALL control flow (`if`, `else`, `for`, `foreach`, `while`, `switch`) — even when the body is a single line or a single `continue`/`break`/`return`. Braceless single-line bodies are NEVER acceptable.
- The opening brace of a control flow block must always appear on its own line (Allman style). NEVER place the opening brace or the body on the same line as the statement: `if (condition) { ... }` is NEVER acceptable.
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
- Never use two or more consecutive blank lines anywhere in the code.
- Never place an empty line immediately after an opening brace `{`.
- All C# methods must have exactly one empty line between them — no more, no less. This applies equally when a method ends with `};` (e.g. a multi-line expression-bodied method with an object initialiser): there must still be exactly one empty line before the next method.
- Never pad spaces before `=` (or any operator) to align consecutive assignments. Each assignment uses exactly one space before and after `=`.
- Prefer `+= 1` and `-= 1` over explicit self-assignments such as `a = a + 1` and `a = a - 1`.
- Always use explicit types instead of `var`.
- When a variable has a sensible default and is only conditionally overridden, initialise it with the default first and use a single `if` (no `else`) to override. Avoid `if`/`else` when the `else` branch only assigns a fallback/default value.
- Prefer the static `Equals(a, b)` form (e.g. `object.Equals(a, b)` or `string.Equals(a, b)`) over instance `.Equals()` calls or `==` for comparisons. Never call `.Equals()` directly on a potentially null reference — doing so throws a `NullReferenceException`. Use the static form or guard with a null check first.
- NEVER use ternary expressions (`condition ? a : b`). Always use an `if`/`else` statement instead. This does NOT apply to `??`, `??=`, or switch expressions.
- NEVER use `ref` parameters. Avoid `out` parameters; if returning multiple values is necessary, create a dedicated type and return an instance of it. NEVER return tuples — avoid tuples entirely.
- Use `static [Type] [Name] =>` (a static read-only property) instead of `const [Type] [Name] =`. `const` is NEVER acceptable.

### Naming Conventions

- Always use the lowercase alias for built-in types: `string`, `int`, `bool`, `object`, `long`, `double`, `float`, `decimal`, `byte`, `char`, etc. NEVER use the BCL class names `String`, `Int32`, `Boolean`, `Object`, etc.
- Methods: PascalCase, clear and explicit names with no abbreviations or shortenings — same naming rules as for variables and parameters.
- Classes: PascalCase.
- Interfaces: `I`-prefixed PascalCase (`IAccountService`).
- Controllers: pluralized noun + `Controller` (`AccountsController`).
- Data/entity objects: `DataObject` suffix (`AccountDataObject`).
- Domain models: plain noun, no suffix (`Account`, `CheckIn`).
- Request DTOs: Verb + Noun + `Request` (`AddAccountRequest`, `RecordCheckInRequest`).
- Response DTOs: `Get` + Noun + `Response` (`GetAccountResponse`).
- Configuration classes: Noun + `Settings` (`DataStoreSettings`).
- Mapping classes: Noun + `MappingExtensions` (`AccountMappingExtensions`).
- Mapping methods: `ToDomainModel` / `ToDomainModels` for entity→model direction; `ToDataObject` / `ToDataObjects` for model→entity direction. Never `ToEntity` or `ToEntities`.
- Private fields: camelCase, NO underscore prefix (`accountRepository`, not `_accountRepository`).
- Boolean variables, properties, and methods must use a meaningful boolean-semantic prefix: `Is`, `Has`, `Does`, `Are`, or contextual tense-embedded forms (`...Was...`, `...Were...`, `...Is...`, `...Does...`, `...Are...`) — e.g. `IsEnabled`, `HasPermission`, `DoesExist`, `AreValid`, `requestWasHandled`, `itemsAreLoaded`. Never use vague names like `flag`, `check`, or `result` for booleans.
- Test classes: Subject + `Tests` (`AccountServiceTests`).

### Type Declarations

- Domain models: `public sealed class`.
- Data/entity objects: `public sealed class`.
- Configuration classes: `public sealed class`.
- Mapping extension classes: no access modifier (implicitly `internal`), `static`.
- Mapping extension methods: explicitly `internal static`.
- Implement `IEquatable<T>` on domain models and data objects where equality comparison is meaningful (e.g. value objects, data objects compared by identifier). Override `Equals(object)` and `GetHashCode()` consistently.

### Enumerations and Enumeration Classes

- Use a regular `enum` for simple categorical values that carry no additional data and require no string serialisation.
- Use an **enumeration class** instead of an `enum` when any of the following apply:
  - Each value must carry additional structured data (e.g. multiple properties per value).
  - The value must serialise to and deserialise from a string reliably (e.g. stored in a database, returned in an API response).
  - The type needs custom equality semantics or operator overloads.

An enumeration class follows this exact structure:

```csharp
public class CheckInEligibility : IEquatable<CheckInEligibility>
{
    private static readonly Dictionary<string, CheckInEligibility> values = new()
    {
        { nameof(Allowed), new CheckInEligibility(nameof(Allowed)) },
        { nameof(Disallowed), new CheckInEligibility(nameof(Disallowed)) },
    };

    public string Name { get; }

    private CheckInEligibility(string name)
    {
        Name = name;
    }

    public static CheckInEligibility Allowed => values[nameof(Allowed)];
    public static CheckInEligibility Disallowed => values[nameof(Disallowed)];

    public static Array GetValues() => values.Values.ToArray();

    public static CheckInEligibility FromString(string name)
    {
        if (!values.ContainsKey(name))
        {
            return Disallowed;
        }

        return values[name];
    }

    public bool Equals(CheckInEligibility other)
    {
        if (other is null)
        {
            return false;
        }

        if (ReferenceEquals(this, other))
        {
            return true;
        }

        return Name == other.Name;
    }

    public override bool Equals(object obj)
    {
        if (obj is null)
        {
            return false;
        }

        if (ReferenceEquals(this, obj))
        {
            return true;
        }

        if (obj.GetType() != GetType())
        {
            return false;
        }

        return Equals((CheckInEligibility)obj);
    }

    public override int GetHashCode() => $"{nameof(CheckInEligibility)}:{Name}".GetHashCode();

    public override string ToString() => Name;

    public static bool operator ==(CheckInEligibility current, CheckInEligibility other) => current.Equals(other);

    public static bool operator !=(CheckInEligibility current, CheckInEligibility other) => !current.Equals(other);

    public static implicit operator string(CheckInEligibility eligibility) => eligibility.Name;
}
```

Rules for enumeration classes:

- The class must be `public` (not `sealed` — enumeration classes may be extended in some patterns, but if no extension is intended, `sealed` is acceptable).
- The backing dictionary must be `private static readonly` and use `nameof(...)` for both the key and the constructor argument — never string literals.
- Each value's static property uses `=>` (expression-bodied, not `{ get; }`).
- The constructor must be `private`.
- Always implement `IEquatable<T>`, override `Equals(object)` and `GetHashCode()`, and provide `==` / `!=` operator overloads.
- Always provide a `FromString(string name)` factory method. When the name is unrecognised, return a safe default (e.g. `Disallowed`) rather than throwing.
- Always provide `GetValues()` returning all registered values.
- Always provide an `implicit operator string` conversion so the value can be used directly where a string is expected.
- Place the enumeration class in the same namespace and folder as the domain model it belongs to — the same rule as for regular enums.

### Member Organisation

- Always declare the accessibility modifier explicitly on every method, property, field, and constructor — including `private`. Never rely on implicit/default accessibility.
- Order members by accessibility: `public` first, then `protected`, then `private`.
- Within each accessibility group, order members by kind: fields (readonly first, then mutable) → properties → events → constructors and destructors → methods.
- All `public` members in NuGet packages (classes, interfaces, methods, properties, constructors, fields, enums, and their members) must have XML documentation comments (`/// <summary>...</summary>`).
- Overloaded methods must be grouped together (no unrelated members between them) and ordered from simplest/fewest parameters to most-complex/most-numerous parameters.

### Constructors & Object Creation

- Use **primary constructors** (C# 12) on all service classes, controllers, and startup classes. Parameters are used directly inside method bodies — do NOT assign them to fields.
- Use **target-typed `new()`** with object initializer syntax when instantiating models or entities: `Account account = new() { Id = x, ... };`
- Whenever a `new` expression appears on the same line as the variable/property/field declaration (so the type is already stated on the left-hand side), always use `new(...)` instead of `new [Type](...)`. Example: `private static Colour HoverTintColour => new(255, 220, 80);` — NEVER `new Colour(255, 220, 80)` in that position.

### Method Signatures

- Do NOT use optional parameters. Use method overloads instead.
- Keep methods small and focused on a single responsibility. If a method grows beyond ~20–30 lines or handles more than one logical concern, extract the extra logic into well-named private helper methods.
- When a parameter list (declaration) or argument list (call site) **exceeds 64 characters** in total length, split it so that each parameter or argument appears on its own line, indented by one extra level (4 spaces) relative to the method name. The closing `)` goes on its own line at the original indentation level. Example:
  ```csharp
  // Declaration:
  public void RecordCheckIn(
      string accountId,
      string locationId,
      DateTime timestamp)
  {
      ...
  }

  // Call site:
  RecordCheckIn(
      account.Id,
      location.Id,
      DateTime.UtcNow);
  ```

### Properties & Methods

- Use auto-properties `{ get; set; }` for all models, entities, requests, responses, and settings.
- Use expression-bodied (`=>`) for derived/computed read-only properties.
- Use expression-bodied (`=>`) for **any** method whose entire body is a single statement — this includes `return` expressions (`public Foo GetFoo() => foo;`), void delegation calls (`public void Reset() => inner.Reset();`), and `throw` expressions. A block body `{ return x; }` or `{ Foo(); }` with a single statement is **always wrong**; use `=> x;` or `=> Foo();` instead.
- Use expression-bodied (`=>`) for methods whose entire body is a single `new() { ... }` initialiser — do NOT assign to a local variable and return it: `internal static Foo ToDataObject(this Bar bar) => new() { Id = bar.Id };`. This applies unconditionally to all mapping extension methods (`ToDomainModel`, `ToDataObject`, and their plurals).
- When an expression-bodied method uses a multi-line `new() { ... }` object initialiser, always place `=> new()` on the **same line** as the method signature — never on the next line. The opening `{` of the initialiser goes on the line after the signature, and the closing `}` with `;` closes the method. Example:
  ```csharp
  internal static UnitDataObject ToDataObject(this Unit model) => new()
  {
      Id = model.TypeIndex.ToString(),
      Name = model.Name,
  };
  ```
- Each property on its own line, separated by a blank line from other members.
- No `init`-only properties.

### Null Handling

- Use `is null` / `is not null` pattern. Do NOT use `== null` or `!= null`.
- No null-coalescing `??` operator.

### Exception Handling

- Use log-and-rethrow pattern: `catch (Exception exception) { logger.Error(...); throw; }`.
- Use `throw;` (NOT `throw exception;`) to preserve the stack trace.
- Use only BCL exceptions (`ArgumentNullException`, `KeyNotFoundException`, `AuthenticationException`). Do NOT create custom exception types.
- When throwing exceptions, always pass as much detail as possible — include the relevant value(s), parameter name(s), and a descriptive message that clearly identifies what was invalid or missing and why.

### Collections

- Use `IEnumerable<T>` as the return type and parameter type for all collections. Never `List<T>`, `IList<T>`, `IReadOnlyList<T>`, `HashSet<T>`.
- **Exception:** entity/data objects that are XML-serialised (e.g. via `XmlSerializer`) must use `List<T>` for collection properties — the XML serialiser cannot reflect interface types.
- Use C# 12 collection expressions `[...]` for inline collection initialization of **any** collection type (`List<T>`, `Dictionary<K,V>`, arrays, etc.), including empty ones. `new List<T>()`, `new Dictionary<K,V>()`, `new T[]{}` are all wrong — use `[]` instead.
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

### Unit Tests

- NEVER add `<AssemblyAttribute Include="System.Runtime.CompilerServices.InternalsVisibleTo">` (or any other production code change) to a project just to enable unit test access. Do not modify the production project or its csproj solely for the sake of tests.
- Always write unit tests in the `Given[x]_When[y]_Then[z]` naming format.
- Use **NUnit 4.x** + **Moq** for all unit tests, unless other test or mocking frameworks are already installed in the project — in that case use the ones already present.
- Use `Assert.That(...)` with the NUnit constraint model exclusively. NEVER use `Assert.AreEqual`, `Assert.IsTrue`, `Assert.IsNotNull`, etc.
- Do not use `Assert.That(..., Is.True)`, just use `Assert.That(...)` directly.
- Never call `.Equals()` inside `Assert.That`. Use `Assert.That(actual, Is.EqualTo(expected))` and `Assert.That(actual, Is.Not.EqualTo(unexpected))` instead.
- Use `Is.Empty` instead of `Is.EqualTo(string.Empty)` in asserts.
- Use `Has.Length.EqualTo(n)` instead of asserting on `.Length` directly: `Assert.That(collection, Has.Length.EqualTo(n))`, never `Assert.That(collection.Length, Is.EqualTo(n))`.
- Annotate test classes with `[TestFixture]`, test methods with `[Test]` or `[TestCase(...)]`.
- Use a `[SetUp]` method named `SetUp()` to construct mocks and the SUT.
- Declare mock fields and the SUT at class level without access modifiers (implicitly private).
- Group tests within a class by the production method under test, separated by comment banners (e.g., `// ── MethodName ──────`).
- Put private static `BuildXxx()` helper methods at the bottom of the test class for constructing test data.
