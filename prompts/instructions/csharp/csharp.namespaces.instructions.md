---
description: "Use when writing or editing C# code. Covers namespaces, using directives."
applyTo: "**/*.{cs}"
---
## C#

### Namespaces

- Use block namespaces (`namespace Foo { ... }`), never file-scoped (`namespace Foo;`).
- Namespace follows responsibility: account validation belongs in `[Root].Services.Account`, not generic `Services`/`Utilities`.
- Organise first by layer (`Controllers`, `Services`, `Repositories`, `Domain`, `DataObjects`), then domain (for example, `Services/Account/`). Namespace and folder mirror exactly; relocate files immediately after namespace changes.
- Standard namespaces: `[RootNamespace].Configuration`, `.DataAccess`, `.DataAccess.DataObjects`, `.Logging`, `.Services`, `.Services.Mapping`, `.Services.Models`.
- No `[xyz].Interfaces`; colocate interfaces with implementations.

### Using Directives
- Place all `using` directives above and outside the namespace.
- No inline fully qualified types, including BCL types. Add a `using` and use the short name (e.g. `using System;` plus `Enum`, not `System.Enum`).
- Group `using` directives in this order: `System.*`; `Microsoft.*`; third-party, one group per alphabetically ordered package root; current solution. Alphabetise within groups and place one blank line between groups.
- Exactly one blank line between final `using` and namespace.
