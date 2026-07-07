## General - all languages and technologies

- Respect the existing coding style in each repository, including file naming, splitting, and structure conventions.
- Place methods and functions in files, classes, and types based on clear responsibility; avoid multi-responsibility buckets.
- Ensure all added code is covered by tests.
- Follow clean code principles, avoid design anti-patterns, and use suitable design patterns for scalable, reviewable, understandable, and well-organised code.
- Use clear, explicit variable, type, and method names with no unclear abbreviations or shortenings.
- Use British English spelling in code and related text. Prefer latinate English words where possible (e.g. "necessary" instead of "needed").
- Keep code self-explanatory and avoid comments unless they are exceptional and genuinely useful.
- Use proper grammar in all text, including log messages, test names, comments, and user-facing strings (for example: "Appends the `sdkInitialisationKey` with ...", "when the endpoint already ...", "Already has a query string", "Added Dispose() in the factory.", "The session token retrieval has failed"), instead of variants that omit "the", "has", "a", "an", etc.

## C# General

- Always use explicit braces for control flow. `=>` expression-bodied members are encouraged for single-expression methods/properties/constructors.
- Never declare multiple variables on one line.
- Each new type must be declared in its own file. File name must exactly match the class name.
- Prefer `.Equals()` over `==` for comparisons.
- NEVER use conditional (ternary) expressions (`? :`). Always use `if` statements instead, in every session, in every project.
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
- Private fields: camelCase, NO underscore prefix (`accountRepository`, not `_accountRepository`).
- Boolean properties/methods: `Is`-prefixed (`IsEnabled`, `IsToday()`).
- Test classes: Subject + `Tests` (`AccountServiceTests`).

## C# Access Modifiers

- Domain models: `public sealed class`.
- Data/entity objects: `public sealed class`.
- Configuration classes: `public sealed class`.
- Mapping extension classes: no access modifier (implicitly `internal`), `static`.
- Mapping extension methods: explicitly `internal static`.
- Private methods in service classes: omit the `private` keyword (let it default to implicitly private).

## C# Constructors & Object Creation

- Use **primary constructors** (C# 12) on all service classes, controllers, and startup classes. Parameters are used directly inside method bodies — do NOT assign them to fields.
- Use **target-typed `new()`** with object initializer syntax when instantiating models or entities: `Account account = new() { Id = x, ... };`

## C# Properties

- Use auto-properties `{ get; set; }` for all models, entities, requests, responses, and settings.
- Use expression-bodied (`=>`) for derived/computed read-only properties.
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
- Use C# 12 collection expressions `[...]` for inline collection initialization.
- Use LINQ (`.Where()`, `.Any()`, `.First()`, `.Select()`, `.Append()`) for in-memory querying.

## C# Controller Style

- Controller actions return `ActionResult` (not `ActionResult<T>`).
- Use expression-bodied actions for single-expression delegates to a `ProcessRequest(...)` call.

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