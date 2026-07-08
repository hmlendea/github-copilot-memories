## General - all languages and technologies

- Respect the existing coding style in each repository, including file naming, splitting, and structure conventions.
- Place methods and functions in files, classes, and types based on clear responsibility; avoid multi-responsibility buckets.
- Ensure all added code is covered by tests.
- Follow clean code principles, avoid design anti-patterns, and use suitable design patterns for scalable, reviewable, understandable, and well-organised code.
- Use clear, explicit variable, type, and method names with no unclear abbreviations or shortenings. Prefixes like `tex`, `msg`, `btn`, `img`, `val`, `obj`, `mgr`, `cfg`, `pos` etc. are forbidden — always write the full word (`texture`, `message`, `button`, `image`, `value`, `object`, `manager`, `configuration`, `position`).
- Use British English spelling in code and related text. Prefer latinate English words where possible (e.g. "necessary" instead of "needed").
- Keep code self-explanatory and avoid comments unless they are exceptional and genuinely useful.
- Always place at least one space after `//` at the start of a comment: `// text`, never `//text`.
- Inline and block comments must always begin with an uppercase letter and end with a period: `// Calculates the wall distance.`
- TODO comments must always use the exact format `// TODO: Description.` (uppercase TODO, colon, space, sentence ending with period).
- Never use tabs for indentation — always use spaces.
- Use proper grammar in all text, including log messages, test names, comments, and user-facing strings (for example: "Appends the `sdkInitialisationKey` with ...", "when the endpoint already ...", "Already has a query string", "Added Dispose() in the factory.", "The session token retrieval has failed"), instead of variants that omit "the", "has", "a", "an", etc.

## C# General

- Always use explicit braces for ALL control flow (`if`, `else`, `for`, `foreach`, `while`, `switch`) — even when the body is a single line or a single `continue`/`break`/`return`. Braceless single-line bodies are NEVER acceptable.
- Do not use redundant parentheses. Only add parentheses when they are required to override operator precedence or to clarify a genuinely ambiguous expression.
- `if`, `for`, `foreach`, `while`, and `switch` statements must always be separated from adjacent assignments or other statements by a blank line above and below.
- Never pad spaces before `=` (or any operator) to align consecutive assignments. Each assignment uses exactly one space before and after `=`.
- Never use `++` or `--` as standalone statements or in expressions. Always use `+= 1` and `-= 1` instead. Exception: `i++` / `i--` in the iterator clause of a `for` statement is preferred.
- Each new type must be declared in its own file. File name must exactly match the class name.
- Prefer `.Equals()` over `==` for comparisons.
- NEVER use ternary expressions (`condition ? a : b`). Always use an `if`/`else` statement instead. This does NOT apply to `??`, `??=`, or switch expressions.
- Always use explicit types instead of `var`.
- NEVER use `ImplicitUsings` or implicit namespaces. Always use explicit `using` directives. Never add `<ImplicitUsings>enable</ImplicitUsings>` to any csproj.
- Always prefer `.slnx` over `.sln` solution files.
- Use block-braces namespaces (`namespace Foo { ... }`), NOT file-scoped namespaces (`namespace Foo;`).
- Namespace must mirror folder structure exactly.
- All `using` directives go at the top of the file, **outside** the namespace block. Order: System → third-party → project.

## C# Naming Conventions

- Classes: PascalCase.
- Interfaces: `I`-prefixed PascalCase (`IAccountService`).
- Controllers: pluralized noun + `Controller` (`AccountsController`).
- Data/entity objects: `Entity` suffix (`AccountEntity`).
- Domain models: plain noun, no suffix (`Account`, `CheckIn`).
- Request DTOs: Verb + Noun + `Request` (`AddAccountRequest`, `RecordCheckInRequest`).
- Response DTOs: `Get` + Noun + `Response` (`GetAccountResponse`).
- Configuration classes: Noun + `Settings` (`DataStoreSettings`).
- Mapping classes: Noun + `MappingExtensions` (`AccountMappingExtensions`).
- Mapping methods: `ToDomainModel` / `ToDomainModels` for entity→model direction; `ToDataObject` / `ToDataObjects` for model→entity direction. Never `ToEntity` or `ToEntities`.
- Private fields: camelCase, NO underscore prefix (`accountRepository`, not `_accountRepository`).
- Boolean properties/methods: `Is`-prefixed (`IsEnabled`, `IsToday()`).
- Test classes: Subject + `Tests` (`AccountServiceTests`).

## C# Access Modifiers

- Domain models: `public sealed class`.
- Data/entity objects: `public sealed class`.
- Configuration classes: `public sealed class`.
- Mapping extension classes: no access modifier (implicitly `internal`), `static`.
- Mapping extension methods: explicitly `internal static`.
- Always declare the accessibility modifier explicitly on every method, property, field, and constructor — including `private`. Never rely on implicit/default accessibility.

## C# Constructors & Object Creation

- Use **primary constructors** (C# 12) on all service classes, controllers, and startup classes. Parameters are used directly inside method bodies — do NOT assign them to fields.
- Use **target-typed `new()`** with object initializer syntax when instantiating models or entities: `Account account = new() { Id = x, ... };`

## C# Properties

- Use auto-properties `{ get; set; }` for all models, entities, requests, responses, and settings.
- Use expression-bodied (`=>`) for derived/computed read-only properties.
- Use expression-bodied (`=>`) for **any** method whose entire body is a single statement — this includes `return` expressions (`public Foo GetFoo() => foo;`), void delegation calls (`public void Reset() => inner.Reset();`), and `throw` expressions. A block body `{ return x; }` or `{ Foo(); }` with a single statement is **always wrong**; use `=> x;` or `=> Foo();` instead.
- Use expression-bodied (`=>`) for methods whose entire body is a single `new() { ... }` initialiser — do NOT assign to a local variable and return it: `internal static Foo ToDataObject(this Bar bar) => new() { Id = bar.Id };`. This applies unconditionally to all mapping extension methods (`ToDomainModel`, `ToDataObject`, and their plurals).
- Each property on its own line, separated by a blank line from other members.
- No `init`-only properties.

## C# Null Handling

- Use `is null` / `is not null` pattern. Do NOT use `== null` or `!= null`.
- No null-coalescing `??` operator.

## C# Exception Handling

- Use log-and-rethrow pattern: `catch (Exception exception) { logger.Error(...); throw; }`.
- Use `throw;` (NOT `throw exception;`) to preserve the stack trace.
- Use only BCL exceptions (`ArgumentNullException`, `KeyNotFoundException`, `AuthenticationException`). Do NOT create custom exception types.

## C# Collections

- Use `IEnumerable<T>` as the return type and parameter type for all collections. Never `List<T>`, `IList<T>`, `IReadOnlyList<T>`, `HashSet<T>`.
- Use C# 12 collection expressions `[...]` for inline collection initialization of **any** collection type (`List<T>`, `Dictionary<K,V>`, arrays, etc.), including empty ones. `new List<T>()`, `new Dictionary<K,V>()`, `new T[]{}` are all wrong — use `[]` instead.
- Use LINQ (`.Where()`, `.Any()`, `.First()`, `.Select()`, `.Append()`) for in-memory querying.

## C# Controller Style

- Controller actions return `ActionResult` (not `ActionResult<T>`).
- Use expression-bodied actions for single-expression delegates to a `ProcessRequest(...)` call.

## XNA / MonoGame with NuciXNA

- When NuciXNA packages are present, ALWAYS use `GuiImage` instead of raw `Texture2D` fields/dictionaries for loading and holding textures. NEVER use `NuciContentManager.Instance.LoadTexture2D(...)` directly when `GuiImage` can be used instead.
- When NuciXNA packages are present, ALWAYS use `GuiText` instead of raw `SpriteFont` / `SpriteBatch.DrawString(...)` for text rendering.
- The lifecycle (LoadContent, UnloadContent, Update, Draw) of ANY `GuiControl` is managed entirely by the NuciXNA GUI Manager — NEVER call those methods directly on any control.
- Inside a `GuiControl` subclass: register child controls via `RegisterChildren(...)` or `RegisterChild(...)`.
- Inside a `Screen` subclass: register controls via `GuiManager.Instance.RegisterControls(...)` or `GuiManager.Instance.RegisterControl(...)`.
- There are NO exceptions to the registration rule — do not manually call LoadContent/UnloadContent/Update/Draw on any GuiControl.

## C# Async

- Prefer synchronous service methods. Do not add `Task<T>` return types or `async/await` unless required.
- No `CancellationToken` usage unless explicitly needed.

## C# Dependency Injection

- Register all services as `AddSingleton`. Do NOT use `AddScoped` or `AddTransient`.
- Centralize all DI registration in a `ServiceCollectionExtensions.cs` file with extension methods on `IServiceCollection`.

## C# Unit Tests

- Always write unit tests in the `Given[x]_When[y]_Then[z]` naming format.
- Use **NUnit 4.x** + **Moq** for all unit tests.
- Use `Assert.That(...)` with the NUnit constraint model exclusively. NEVER use `Assert.AreEqual`, `Assert.IsTrue`, `Assert.IsNotNull`, etc.
- Do not use `Assert.That(..., Is.True)`, just use `Assert.That(...)` directly.
- Annotate test classes with `[TestFixture]`, test methods with `[Test]` or `[TestCase(...)]`.
- Use a `[SetUp]` method named `SetUp()` to construct mocks and the SUT.
- Declare mock fields and the SUT at class level without access modifiers (implicitly private).
- Group tests within a class by the production method under test, separated by comment banners (e.g., `// ── MethodName ──────`).
- Put private static `BuildXxx()` helper methods at the bottom of the test class for constructing test data.