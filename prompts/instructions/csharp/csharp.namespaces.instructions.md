---
description: "Use when writing or editing C# code. Covers namespaces, using directives."
applyTo: "**/*.{cs}"
---
## C#

### Namespaces

- Use block namespaces (`namespace Foo { ... }`), never file-scoped (`namespace Foo;`).
- Namespace follows responsibility: account validation belongs in `[Root].Services.Account`, not generic `Services`/`Utilities`.
- Organise by architectural layer (Controllers, Services, Repositories, Domain, DataObjects), then domain subfolder/namespace (e.g. `Services/Account/`).
- Namespace and folder mirror exactly. Namespace changes require immediate file relocation. Examples:
  - `[RootNamespace].Configuration`
  - `[RootNamespace].DataAccess`
  - `[RootNamespace].DataAccess.DataObjects`
  - `[RootNamespace].Logging`
  - `[RootNamespace].Services`
  - `[RootNamespace].Services.Mapping`
  - `[RootNamespace].Services.Models`
- No `[xyz].Interfaces`; colocate interfaces with implementations.

### Using Directives
- Place all `using` directives above and outside the namespace.
- No inline fully qualified types, including BCL types. Add a `using` and use the short name (e.g. `using System;` plus `Enum`, not `System.Enum`).
- Group `using` directives in this order, one blank line between groups; alphabetise within each group.
  1. **`System.*` usings**: all namespaces rooted at `System`.
  2. **`Microsoft.*` usings**: all namespaces rooted at `Microsoft`.
  3. **NuGet / third-party package usings**: one group per package root namespace (e.g. all `Newtonsoft.*` together, all `Serilog.*` together), ordered alphabetically by package root namespace.
  4. **Current solution usings**: namespaces belonging to the solution being worked on, all in one group.
- Exactly one blank line between final `using` and namespace.
