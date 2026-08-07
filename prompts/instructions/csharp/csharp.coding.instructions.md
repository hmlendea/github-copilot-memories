---
description: "Use when writing or editing C# code. Covers code style, naming conventions, type declarations, member organisation, constructors, methods, properties, collections, async, dependency injection."
applyTo: "**/*.{cs}"
---
## C#

### Code Style

- Prefer `+= 1` and `-= 1` over explicit self-assignments such as `a = a + 1` and `a = a - 1`.
- Always use explicit types instead of `var`, no exceptions.
- When a variable has a sensible default and is only conditionally overridden, initialise it with the default first and use a single `if` (no `else`) to override. Avoid `if`/`else` when the `else` branch only assigns a fallback/default value.
- Prefer the static `Equals(a, b)` form (e.g. `object.Equals(a, b)` or `string.Equals(a, b)`) over instance `.Equals()` calls or `==` for comparisons. Never call `.Equals()` directly on a potentially null reference, as doing so throws a `NullReferenceException`. Use the static form or guard with a null check first.
- If a method does not access instance state, mark it `static`.
- NEVER use ternary expressions (`condition ? a : b`). Always use an `if`/`else` statement instead. This does NOT apply to `??=` or switch expressions.
- NEVER use `ref` parameters. Avoid `out` parameters; if returning multiple values is necessary, create a dedicated type and return an instance of it. NEVER return tuples; avoid tuples entirely.
- Never use `#region` or `#endregion`. They are forbidden everywhere without exception.
- All C# methods must have exactly one empty line between them: no more, no less. This applies equally when a method ends with `};` (e.g. a multi-line expression-bodied method with an object initialiser): there must still be exactly one empty line before the next method.
- Use `static [Type] [Name] =>` (a static read-only property) instead of `const [Type] [Name] =`. `const` is NEVER acceptable.
- Always use explicit braces for ALL control flow (`if`, `else`, `for`, `foreach`, `while`, `switch`, etc.), even when the body is a single line or a single statement like `continue`, `break`, or `return`. Braceless single-line bodies are NEVER acceptable.
- The opening brace of a control flow block must always appear on its own line. NEVER place the opening brace or the body on the same line as the statement.
- `else if` must always appear on a single line. NEVER split it so that `else` is on one line and the condition is on another.
- Never use magic numbers or magic strings. Use enums for categorical values and named constants for all other fixed values. Named constants must use `static [Type] [Name] =>` (a static read-only property), not `const`.
- When an object has a "type" or "variant" (e.g. which button, which icon, etc.), always model it with an enum property, not an `int` index. The enum name should describe the category (e.g. `ButtonType`), and its values should be the specific variants (e.g. `Undo`, `Restart`, `Info`, `Settings`). The index is derived from the enum value via `(int)value` and is never stored directly.
- Do NOT use optional parameters or default arguments. Use method/function overloads instead.
- Parameter names in interfaces and their implementing classes must match exactly. If an interface defines a method with a parameter named `accountId`, all implementing classes must use the same parameter name `accountId`, not an alias like `id` or `account`. This ensures consistency and proper IDE support for overrides and implementations.
- Overloaded methods must be grouped together (no unrelated members between them) and ordered from simplest/fewest parameters to most-complex/most-numerous parameters.
- Never place a blank line immediately before a closing brace or bracket (`}`, `]`, `)`). The last statement inside a block must be followed directly by the closing delimiter with no empty line between them.
- Always place a blank line above AND below a block control flow statement (`if`, `for`, `foreach`, `while`, `do`, `switch`, `continue`, `break`) when it is adjacent to non-blank, non-control-flow statements in the same block. Always place a blank line above only for `return` and `throw` statements when preceded by one or more non-blank, non-control-flow statements. Do not add the blank line when the statement is the very first statement in the block, or when the adjacent line is itself an opening brace or another control flow statement.

### File Structure

- Never use top-level statements or free-floating code in any file. Every file must have an explicit `namespace { }` block, a `class` (or other type) block, and all code placed inside methods, constructors, or other members. This applies to `Program.cs` too; use an explicit `Program` class with a `static void Main` entry point.
- Every type must be declared in its own file — one type per file, without exception. File name must exactly match the type name. If a file contains multiple type definitions, extract each additional type into its own file immediately.

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

- Keep methods small and focused on a single responsibility. If a method grows beyond ~20-30 lines or handles more than one logical concern, extract the extra logic into well-named private helper methods.
- Avoid duplicated code; respect the DRY (Don't Repeat Yourself) principle. Extract common logic into well-named private helper methods or utility functions. Never copy-paste code across multiple methods or classes.
- Implementation classes must NOT contain mapping methods. All mapping logic must be implemented as extension methods in a dedicated `*MappingExtensions.cs` file under a `*.Mappings` namespace.
- Use expression-bodied (`=>`) for **any** method whose entire body is a single statement; this includes `return` expressions (`public Foo GetFoo() => foo;`), void delegation calls (`public void Reset() => inner.Reset();`), and `throw` expressions (`public void ResetCombat()\n    => throw new NotImplementedException();`). A block body `{ return x; }` or `{ Foo(); }` with a single statement is **always wrong**; use `=> x;` or `=> Foo();` instead.
- Use expression-bodied (`=>`) for methods whose entire body is a single `new() { ... }` initialiser; do NOT assign to a local variable and return it: `internal static Foo ToDataObject(this Bar bar) => new() { Id = bar.Id };`.
- Never leave unreachable statements after an unconditional `return`, `throw`, `continue`, `break`, or exhaustive switch expression return.

### Parsing & Serialisation

- Always use a format provider when parsing or formatting date-time objects. Use `CultureInfo.InvariantCulture` for culture-independent operations (the most common case), or an explicitly specified culture when required. Methods like `DateTime.Parse()`, `DateTime.TryParse()`, `ParseExact()`, `TryParseExact()`, `ToString()`, and similar should always receive a format provider or format string. Never call `DateTime.Parse("2026-08-05")` without a format provider; use `DateTime.ParseExact("2026-08-05", "yyyy-MM-dd", CultureInfo.InvariantCulture)` instead.
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
