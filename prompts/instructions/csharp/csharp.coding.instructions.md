---
description: "Use for C# edits. Covers style, types, members, construction, methods, properties, async, and compiler rules."
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

- No `partial` classes except framework contracts or explicit user requests.
- Non-static classes with public methods implement a colocated equivalent interface (e.g. `AccountService`/`IAccountService`), except domain models and data/entities. Interface mirrors public contract.
- Classes are `sealed` unless designed for inheritance. Domain models, data/entities, and configuration classes: `public sealed class`.
- Domain/data objects with meaningful equality implement `IEquatable<T>`, `Equals(object)`, and consistent `GetHashCode()`.

### Member Organisation

- Every field, property, event, constructor, and method explicitly declares valid accessibility, including `private`; omission is a defect.
- Kind order: fields -> properties -> events -> constructors/destructors -> methods.
- Field order: static readonly -> static mutable -> instance readonly -> instance mutable; within each: `public` -> `protected` -> `private`.
- Other member groups: `public` -> `protected` -> `private`.
- Every public NuGet class/member, including enum members, requires preserved and current XML documentation (`/// <summary>...</summary>`).
- Never remove a public NuGet member unless explicitly requested; external clients may use it.

### Constructors & Object Creation

- Services, controllers, and startup classes use C# 12 primary constructors; use parameters directly, without fields.
- Models/entities use target-typed `new()` initialisers: `Account account = new() { Id = x, ... };`.
- When declaration already states the type, use `new(...)`, never `new Type(...)` (e.g. `Colour colour = new(1, 2, 3);`).

### Properties

- Use auto-properties `{ get; set; }` for all models, entities, requests, responses, and settings.
- Use expression-bodied (`=>`) for derived/computed read-only properties.
- No `init`-only properties.

### Methods

- Mapping exists only as extension methods in dedicated `*MappingExtensions.cs` files under `*.Mappings`; never in implementation classes.
- Every single-statement method is expression-bodied (`=>`), including return, delegation, throw, and `new()` initialisers; never use a block or temporary local (e.g. `public Foo GetFoo() => foo;`).

### Async

- Prefer synchronous service methods. Do not add `Task<T>` return types or `async/await` unless required.
- No `CancellationToken` usage unless explicitly needed.

### Compiler Instructions

- Never use `#nullable enable` in any class. All code must be written as if nullable reference types are enabled, without using the compiler directive.
