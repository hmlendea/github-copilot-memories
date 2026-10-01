---
description: "Use when writing or editing C# code. Covers code style, naming conventions, type declarations, member organisation, constructors, methods, properties, collections, async, dependency injection."
applyTo: "**/*.{cs}"
---
## C#

### Code Style

- Prefer `+= 1` and `-= 1` over explicit self-assignments such as `a = a + 1` and `a = a - 1`.
- Types: explicit; never `var`.
- Conditional default: initialise first; one `if` overrides it, without fallback-only `else`.
- Comparisons: prefer static `Equals(a, b)` or `string.Equals(a, b)` over `==` and instance `.Equals()`. Guard any nullable instance call.
- No instance state access: mark method `static`.
- No ternary (`condition ? a : b`); use `if`/`else`. `??=` and switch expressions remain permitted.
- Parameters: no `ref`; avoid `out`; return a dedicated type for multiple values. No tuples.
- No `#region` or `#endregion`.
- Exactly one empty line between methods, including after methods ending with `};`.
- Constants: `static [Type] [Name] =>`; never `const`.
- Every control-flow body uses braces, including single `continue`, `break`, or `return`; opening brace occupies its own line.
- Keep `else if` on one line.
- Derive variant indices via `(int)value`; never store them directly.
- No optional/default parameters; use overloads.
- Interface and implementation parameter names must match exactly (e.g. `accountId`, not `id`).
- Group overloads together, ordered from fewest/simplest to most parameters/complexity.
- No blank line immediately before `}`, `]`, or `)`.
- Always place a blank line above AND below a block control flow statement (`if`, `for`, `foreach`, `while`, `do`, `switch`, `continue`, `break`) when it is adjacent to non-blank, non-control-flow statements in the same block. Always place a blank line above only for `return` and `throw` statements when preceded by one or more non-blank, non-control-flow statements. Do not add the blank line when the statement is the very first statement in the block, or when the adjacent line is itself an opening brace or another control flow statement.

### File Structure

- No top-level/free-floating code. Every file, including `Program.cs`, requires explicit namespace and type blocks; `Program` uses `static void Main`.
- One type per identically named file; extract additional types immediately.

### Type Declarations

- Do not use `partial` classes unless explicitly required by framework-generated contract or explicitly requested by the user.
- Every non-static class that declares at least one `public` method and is not a domain model or data/entity object must have an equivalent interface and must implement that interface. Prefer colocated naming pairs such as `AccountService` + `IAccountService` and keep the interface surface aligned with the class's public contract.
- All classes that are not explicitly designed for inheritance must be declared `sealed`. When in doubt, default to `sealed`.
- Domain models: `public sealed class`.
- Data/entity objects: `public sealed class`.
- Configuration classes: `public sealed class`.
- Implement `IEquatable<T>` on domain models and data objects where equality comparison is meaningful (e.g. value objects, data objects compared by identifier). Override `Equals(object)` and `GetHashCode()` consistently.

### Member Organisation

- ALWAYS declare the accessibility modifier explicitly on EVERY member: every field, property, event, constructor, and method must begin with `public`, `protected`, `internal`, `private`, or a valid combination. NEVER omit the modifier and rely on the implicit default. This applies even to `private` members — write `private int counter;`, NEVER just `int counter;`. Writing a field or method with no accessibility modifier is a bug.
- Order members by kind first, then by accessibility within each kind group. The top-level kind order is: fields -> properties -> events -> constructors and destructors -> methods.
- Within the fields group, order by: static readonly -> static mutable -> instance readonly -> instance mutable. Within each of those sub-groups, order by accessibility: `public` first, then `protected`, then `private`.
- Within every other kind group (properties, events, constructors, methods), order by accessibility: `public` first, then `protected`, then `private`.
- All `public` members in NuGet packages (classes, methods, properties, constructors, fields, enums, and their members) must have XML documentation comments (`/// <summary>...</summary>`). These must NEVER be removed or omitted, including during refactoring. When a member is renamed, moved, or restructured, its XML documentation must be preserved and updated to reflect the change.
- NEVER remove a `public` member from a NuGet package during refactoring, even if it appears unused within the solution. External clients of the package may depend on it. A `public` member may only be removed when explicitly instructed to do so by the user.

### Constructors & Object Creation

- Use **primary constructors** (C# 12) on all service classes, controllers, and startup classes. Parameters are used directly inside method bodies; do NOT assign them to fields.
- Use **target-typed `new()`** with object initializer syntax when instantiating models or entities: `Account account = new() { Id = x, ... };`
- Whenever a `new` expression appears on the same line as the variable/property/field declaration (so the type is already stated on the left-hand side), always use `new(...)` instead of `new [Type](...)`. Example: `private static Colour HoverTintColour => new(255, 220, 80);`; NEVER `new Colour(255, 220, 80)` in that position.

### Properties

- Use auto-properties `{ get; set; }` for all models, entities, requests, responses, and settings.
- Use expression-bodied (`=>`) for derived/computed read-only properties.
- No `init`-only properties.

### Methods

- Implementation classes must NOT contain mapping methods. All mapping logic must be implemented as extension methods in a dedicated `*MappingExtensions.cs` file under a `*.Mappings` namespace.
- Use expression-bodied (`=>`) for **any** method whose entire body is a single statement; this includes `return` expressions (`public Foo GetFoo() => foo;`), void delegation calls (`public void Reset() => inner.Reset();`), and `throw` expressions (`public void ResetCombat()\n    => throw new NotImplementedException();`). A block body `{ return x; }` or `{ Foo(); }` with a single statement is **always wrong**; use `=> x;` or `=> Foo();` instead.
- Use expression-bodied (`=>`) for methods whose entire body is a single `new() { ... }` initialiser; do NOT assign to a local variable and return it: `internal static Foo ToDataObject(this Bar bar) => new() { Id = bar.Id };`.

### Parsing & Serialisation

- Always use a format provider when parsing or formatting date-time objects. Use `CultureInfo.InvariantCulture` for culture-independent operations (the most common case), or an explicitly specified culture when required. Methods like `DateTime.Parse()`, `DateTime.TryParse()`, `ParseExact()`, `TryParseExact()`, `ToString()`, and similar should always receive a format provider or format string. Never call `DateTime.Parse("2026-08-05")` without a format provider; use `DateTime.ParseExact("2026-08-05", "yyyy-MM-dd", CultureInfo.InvariantCulture)` instead.
- For API request and response DTOs, every property name segment `Identifier` must serialise with `id` in JSON names via `JsonPropertyName`. Examples: `Identifier` -> `id`, `AccountIdentifier` -> `accountId`, `UserIdentifier` -> `userId`.
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
