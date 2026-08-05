---
description: "Use when writing or editing C# code. Covers code style, naming conventions, type declarations, member organisation, constructors, methods, properties, collections, async, dependency injection."
applyTo: "**/*.{cs}"
---
## C#

### Code Style

- Always use explicit braces for ALL control flow (`if`, `else`, `for`, `foreach`, `while`, `switch`), even when the body is a single line or a single `continue`/`break`/`return`. Braceless single-line bodies are NEVER acceptable.
- The opening brace of a control flow block must always appear on its own line (Allman style). NEVER place the opening brace or the body on the same line as the statement: `if (condition) { ... }` is NEVER acceptable.
- `else if` must always appear on a single line. NEVER split it so that `else` is on one line and `if` is on another.
- Do not use redundant parentheses. Only add parentheses when they are required to override operator precedence or to clarify a genuinely ambiguous expression.
- `if`, `for`, `foreach`, `while`, `switch`, `continue`, and `break` statements must always be separated from adjacent assignments or other statements by a blank line above and below.
- `return` statements must always be separated from other lines of code by a blank line above (unless they are the only statement in the method body or the first line after an opening brace).
- Never use two or more consecutive blank lines anywhere in the code.
- Never place an empty line immediately after an opening brace `{` or immediately before a closing brace `}`. This applies to all braces without exception: type bodies, method bodies, property accessors, control flow blocks, and every other brace-delimited scope.
- Never use `#region` or `#endregion`. They are forbidden everywhere without exception.
- All C# methods must have exactly one empty line between them: no more, no less. This applies equally when a method ends with `};` (e.g. a multi-line expression-bodied method with an object initialiser): there must still be exactly one empty line before the next method.
- Never pad spaces before `=` (or any operator) to align consecutive assignments. Each assignment uses exactly one space before and after `=`.
- Prefer `+= 1` and `-= 1` over explicit self-assignments such as `a = a + 1` and `a = a - 1`.
- Always use explicit types instead of `var`, no exceptions.
- When a variable has a sensible default and is only conditionally overridden, initialise it with the default first and use a single `if` (no `else`) to override. Avoid `if`/`else` when the `else` branch only assigns a fallback/default value.
- Prefer the static `Equals(a, b)` form (e.g. `object.Equals(a, b)` or `string.Equals(a, b)`) over instance `.Equals()` calls or `==` for comparisons. Never call `.Equals()` directly on a potentially null reference, as doing so throws a `NullReferenceException`. Use the static form or guard with a null check first.
- If a method does not access instance state, mark it `static`.
- NEVER use ternary expressions (`condition ? a : b`). Always use an `if`/`else` statement instead. This does NOT apply to `??=` or switch expressions.
- NEVER use `ref` parameters. Avoid `out` parameters; if returning multiple values is necessary, create a dedicated type and return an instance of it. NEVER return tuples; avoid tuples entirely.
- Use `static [Type] [Name] =>` (a static read-only property) instead of `const [Type] [Name] =`. `const` is NEVER acceptable.

### Type Declarations

- Do not use `partial` classes unless explicitly required by framework-generated contract or explicitly requested by the user.
- Every non-static class that declares at least one `public` method and is not a domain model or data/entity object must have an equivalent interface and must implement that interface. Prefer colocated naming pairs such as `AccountService` + `IAccountService` and keep the interface surface aligned with the class's public contract.
- All classes that are not explicitly designed for inheritance must be declared `sealed`. When in doubt, default to `sealed`.
- Domain models: `public sealed class`.
- Data/entity objects: `public sealed class`.
- Configuration classes: `public sealed class`.
- Implement `IEquatable<T>` on domain models and data objects where equality comparison is meaningful (e.g. value objects, data objects compared by identifier). Override `Equals(object)` and `GetHashCode()` consistently.
- Every type must be declared in its own file — one type per file, without exception. File name must exactly match the type name. If a file contains multiple type definitions, extract each additional type into its own file immediately.

### Member Organisation

- ALWAYS declare the accessibility modifier explicitly on EVERY member: every field, property, event, constructor, and method must begin with `public`, `protected`, `internal`, `private`, or a valid combination. NEVER omit the modifier and rely on the implicit default. This applies even to `private` members — write `private int counter;`, NEVER just `int counter;`. Writing a field or method with no accessibility modifier is a bug.
- Order members by kind first, then by accessibility within each kind group. The top-level kind order is: fields -> properties -> events -> constructors and destructors -> methods.
- Within the fields group, order by: static readonly -> static mutable -> instance readonly -> instance mutable. Within each of those sub-groups, order by accessibility: `public` first, then `protected`, then `private`.
- Within every other kind group (properties, events, constructors, methods), order by accessibility: `public` first, then `protected`, then `private`.
- All `public` members in NuGet packages (classes, methods, properties, constructors, fields, enums, and their members) must have XML documentation comments (`/// <summary>...</summary>`). These must NEVER be removed or omitted, including during refactoring. When a member is renamed, moved, or restructured, its XML documentation must be preserved and updated to reflect the change.
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

### Methods

- Do NOT use optional parameters. Use method overloads instead.
- Keep methods small and focused on a single responsibility. If a method grows beyond ~20-30 lines or handles more than one logical concern, extract the extra logic into well-named private helper methods.
- Use expression-bodied (`=>`) for **any** method whose entire body is a single statement; this includes `return` expressions (`public Foo GetFoo() => foo;`), void delegation calls (`public void Reset() => inner.Reset();`), and `throw` expressions (`public void ResetCombat()\n    => throw new NotImplementedException();`). A block body `{ return x; }` or `{ Foo(); }` with a single statement is **always wrong**; use `=> x;` or `=> Foo();` instead.
- Use expression-bodied (`=>`) for methods whose entire body is a single `new() { ... }` initialiser; do NOT assign to a local variable and return it: `internal static Foo ToDataObject(this Bar bar) => new() { Id = bar.Id };`.
- Never leave unreachable statements after an unconditional `return`, `throw`, `continue`, `break`, or exhaustive switch expression return.

### Parsing & Serialisation
- When parsing or formatting date/time values with explicit formats (`ParseExact`, `TryParseExact`, etc.), always use `CultureInfo.InvariantCulture` unless a different culture is explicitly required.
- Do not allocate `JsonSerializerOptions` repeatedly in hot paths or loops. Cache and reuse static readonly options instances.

### Networking
- For Kestrel listeners that are expected to accept IPv6, bind using `IPAddress.IPv6Any` rather than `IPAddress.Any` unless there is an explicit requirement to reject IPv6.

### Collections

- Use `IEnumerable<T>` as the return type and parameter type for all collections. Never `List<T>`, `IList<T>`, `IReadOnlyList<T>`, `HashSet<T>`.
- **Exception:** entity/data objects that are XML-serialised (e.g. via `XmlSerializer`) must use `List<T>` for collection properties, as the XML serialiser cannot reflect interface types.
- Use C# 12 collection expressions `[...]` for inline collection initialization of **any** collection type (`List<T>`, `Dictionary<K,V>`, arrays, etc.), including empty ones. `new List<T>()`, `new Dictionary<K,V>()`, `new T[]{}` are all wrong; use `[]` instead.
- Use LINQ (`.Where()`, `.Any()`, `.First()`, `.Select()`, `.Append()`) for in-memory querying.

### Async

- Prefer synchronous service methods. Do not add `Task<T>` return types or `async/await` unless required.
- No `CancellationToken` usage unless explicitly needed.

### Compiler Instructions

- Never use `#nullable enable` in any class. All code must be written as if nullable reference types are enabled, without using the compiler directive.
