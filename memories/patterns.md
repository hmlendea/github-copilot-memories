## General - all languages and technologies

- Respect the existing coding style in each repository, including file naming, splitting, and structure conventions.
- Always treat file and directory paths as case-sensitive, even on Windows, to ensure cross-platform compatibility.
- Always write code that handles both LF (`\n`) and CRLF (`\r\n`) line endings. Never assume a single newline style.
- Place methods and functions in files, classes, and types based on clear responsibility; avoid multi-responsibility buckets.
- When changing existing logic, remove all leftovers: dead code, unused imports, obsolete fields, and any other artefacts that are no longer necessary after the change. Update the README if the change affects documented behaviour or setup.
- Ensure all added code is covered by tests.
- Follow clean code principles, avoid design anti-patterns, and use suitable design patterns for scalable, reviewable, understandable, and well-organised code.
- Use clear, explicit variable, type, and method names with no unclear abbreviations or shortenings. This applies **everywhere**: local variables, fields, method parameters, lambda parameters, loop variables, and out-variables. Prefixes like `tex`, `msg`, `btn`, `img`, `val`, `obj`, `mgr`, `cfg`, `pos`, `dir`, `ray`, single-letter names (`t`, `x`, `n`, `m`, `e`) or single-letter/abbreviated prefixes (`tX`, `tY`, `dirX`, `dirY`, `rayX`, `rayY`, `checkX`, `len`, `min`, `max`, `dmg`, `str`, `acc`, `def`) are forbidden — always write the full descriptive name (e.g. `textureYOffset`, `directionX`, `rayPositionX`, `samplePositionX`, `magnitude`, `minimumDamage`, `maximumDamage`, `damageRoll`, `attackerStrength`). Lambda parameters follow the same rule without exception: `items.Select(item => item.Name)`, never `items.Select(i => i.Name)` or `items.Select(x => x.Name)`.
- Use British English spelling in code and related text. Prefer latinate English words where possible (e.g. "necessary" instead of "needed").
- Keep code self-explanatory and avoid comments unless they are exceptional and genuinely useful.
- Always place at least one space after `//` at the start of a comment: `// text`, never `//text`.
- Inline and block comments must always begin with an uppercase letter and end with a period: `// Calculates the wall distance.`
- TODO comments must always use the exact format `// TODO: Description.` (uppercase TODO, colon, space, sentence ending with period).
- Never use tabs for indentation — always use 4 spaces per indent level.
- Licence new projects under GPL v3 unless the repository already uses a different licence.
- Use proper grammar in all text, including log messages, test names, comments, and user-facing strings (for example: "Appends the `sdkInitialisationKey` with ...", "when the endpoint already ...", "Already has a query string", "Added Dispose() in the factory.", "The session token retrieval has failed"), instead of variants that omit "the", "has", "a", "an", etc.

## Source Control

- Default branch name: `master`.
- Merge strategy: default (no fast-forward flags or special strategies unless the repository already specifies otherwise).
- Pull strategy: rebase (`git pull --rebase`).

## Bash & Other UNIX Shells

- Variables inside functions must be declared with `local` whenever possible.
- Never embed Python in shell scripts unless explicitly asked.
- Always write distro-agnostic code: use only POSIX-standard or universally available commands, and avoid paths or tools specific to any particular Linux distribution.
- Always use environment variables for paths instead of hardcoded values — e.g. `${HOME}`, `${XDG_CONFIG_HOME}`, `${XDG_DATA_HOME}`, `${XDG_CACHE_HOME}`. Never hardcode paths like `/home/user/` or `/etc/`.
- Constant strings (no variable references or command substitutions) must use single quotes: `'constant string'`. Strings that reference variables or call commands must use double quotes: `"Value is: ${VAR}"` / `"Today is: $(date)"`.
- Variable naming: all uppercase, always referenced with surrounding curly braces — `${VAR_NAME}`, never `$var_name`.
- Function naming: all lowercase, words separated by underscores — `my_function`, never `myFunction` or `MY_FUNCTION`.

## C# Code Style

- Always use explicit braces for ALL control flow (`if`, `else`, `for`, `foreach`, `while`, `switch`) — even when the body is a single line or a single `continue`/`break`/`return`. Braceless single-line bodies are NEVER acceptable.
- Do not use redundant parentheses. Only add parentheses when they are required to override operator precedence or to clarify a genuinely ambiguous expression.
- `if`, `for`, `foreach`, `while`, and `switch` statements must always be separated from adjacent assignments or other statements by a blank line above and below.
- `return` statements must always be separated from other lines of code by a blank line above (unless they are the only statement in the method body or the first line after an opening brace).
- Never use two or more consecutive blank lines anywhere in the code.
- Never pad spaces before `=` (or any operator) to align consecutive assignments. Each assignment uses exactly one space before and after `=`.
- Never use `++` or `--` as standalone statements or in expressions. Always use `+= 1` and `-= 1` instead. Exception: `i++` / `i--` in the iterator clause of a `for` statement is preferred.
- Always use explicit types instead of `var`.
- When a variable has a sensible default and is only conditionally overridden, initialise it with the default first and use a single `if` (no `else`) to override. Avoid `if`/`else` when the `else` branch only assigns a fallback/default value.
- Prefer `.Equals()` over `==` for comparisons.
- NEVER use ternary expressions (`condition ? a : b`). Always use an `if`/`else` statement instead. This does NOT apply to `??`, `??=`, or switch expressions.
- NEVER use `ref` parameters. Avoid `out` parameters; if returning multiple values is necessary, create a dedicated type and return an instance of it. NEVER return tuples — avoid tuples entirely.
- Use `static [Type] [Name] =>` (a static read-only property) instead of `const [Type] [Name] =`. `const` is NEVER acceptable.

## C# Project Structure

- Always target the latest stable .NET version available.
- Always prefer `.slnx` over `.sln` solution files.
- When creating a new C# solution, place the `.slnx` file and all project directories at the repository root level (no `src/` subfolder or similar). The unit test project, where applicable, must be named `[ProjectName].UnitTests`.
- NEVER use `ImplicitUsings` or implicit namespaces. Always use explicit `using` directives. Never add `<ImplicitUsings>enable</ImplicitUsings>` to any csproj.
- Never use top-level statements or free-floating code in any file. Every file must have an explicit `namespace { }` block, a `class` (or other type) block, and all code placed inside methods, constructors, or other members. This applies to `Program.cs` too — use an explicit `Program` class with a `static void Main` entry point.
- Use block-braces namespaces (`namespace Foo { ... }`), NOT file-scoped namespaces (`namespace Foo;`).
- Each new type must be declared in its own file. File name must exactly match the class name.
- Each class must have a single, well-defined responsibility. Do not add logic to a class unless it clearly belongs there. If a class grows beyond its responsibility or serves multiple concerns, split it into smaller, focused classes.
- Organise source files by architectural layer (e.g. Controllers, Services, Repositories, Domain, DataObjects); each layer lives in its own folder.
- Namespace must mirror folder structure exactly, and file location must match the namespace. A file in `Services/Account/` must declare namespace `[Root].Services.Account` — no exceptions.
- Never create a `[xyz].Interfaces` namespace. Place interfaces in the same namespace and folder as their implementations.
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
- Boolean variables, properties, and methods must use a meaningful boolean-semantic prefix: `Is`, `Has`, `Does`, `Are`, or contextual tense-embedded forms (`...Was...`, `...Were...`, `...Is...`, `...Does...`, `...Are...`) — e.g. `IsEnabled`, `HasPermission`, `DoesExist`, `AreValid`, `requestWasHandled`, `itemsAreLoaded`. Never use vague names like `flag`, `check`, or `result` for booleans.
- Test classes: Subject + `Tests` (`AccountServiceTests`).

## C# Type Declarations

- Domain models: `public sealed class`.
- Data/entity objects: `public sealed class`.
- Configuration classes: `public sealed class`.
- Mapping extension classes: no access modifier (implicitly `internal`), `static`.
- Mapping extension methods: explicitly `internal static`.
- Implement `IEquatable<T>` on domain models and entity classes where equality comparison is meaningful (e.g. value objects, entities compared by identifier). Override `Equals(object)` and `GetHashCode()` consistently.

## C# Member Organisation

- Always declare the accessibility modifier explicitly on every method, property, field, and constructor — including `private`. Never rely on implicit/default accessibility.
- Order members by accessibility: `public` first, then `protected`, then `private`.
- Within each accessibility group, order members by kind: fields (readonly first, then mutable) → properties → events → constructors and destructors → methods.
- All `public` members in NuGet packages (classes, interfaces, methods, properties, constructors, fields, enums, and their members) must have XML documentation comments (`/// <summary>...</summary>`).

## C# Constructors & Object Creation

- Use **primary constructors** (C# 12) on all service classes, controllers, and startup classes. Parameters are used directly inside method bodies — do NOT assign them to fields.
- Use **target-typed `new()`** with object initializer syntax when instantiating models or entities: `Account account = new() { Id = x, ... };`

## C# Properties & Methods

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
- When throwing exceptions, always pass as much detail as possible — include the relevant value(s), parameter name(s), and a descriptive message that clearly identifies what was invalid or missing and why.

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
- Use **NUnit 4.x** + **Moq** for all unit tests, unless other test or mocking frameworks are already installed in the project — in that case use the ones already present.
- Use `Assert.That(...)` with the NUnit constraint model exclusively. NEVER use `Assert.AreEqual`, `Assert.IsTrue`, `Assert.IsNotNull`, etc.
- Do not use `Assert.That(..., Is.True)`, just use `Assert.That(...)` directly.
- Annotate test classes with `[TestFixture]`, test methods with `[Test]` or `[TestCase(...)]`.
- Use a `[SetUp]` method named `SetUp()` to construct mocks and the SUT.
- Declare mock fields and the SUT at class level without access modifiers (implicitly private).
- Group tests within a class by the production method under test, separated by comment banners (e.g., `// ── MethodName ──────`).
- Put private static `BuildXxx()` helper methods at the bottom of the test class for constructing test data.