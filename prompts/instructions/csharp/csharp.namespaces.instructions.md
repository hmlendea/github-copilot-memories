---
description: "Use when writing or editing C# code. Covers namespaces, using directives."
applyTo: "**/*.{cs}"
---
## C#

### Namespaces & Using Directives

- Use block-braces namespaces (`namespace Foo { ... }`), NOT file-scoped namespaces (`namespace Foo;`).
- Each class must have a single, well-defined responsibility. Do not add logic to a class unless it unambiguously belongs there. If a class grows beyond its responsibility or serves multiple concerns, split it immediately into smaller, focused classes, each declared in the namespace that matches its responsibility. NEVER split a class into `partial` classes; always split into separate, concrete classes placed in the appropriate namespace and folder, and reference them explicitly.
- Namespace choice is driven by responsibility, not by incidental proximity. A class that handles account validation belongs in `[Root].Services.Account`, not in a generic `[Root].Services` or `[Root].Utilities` namespace. Always ask: "What is the one thing this class does?"; the answer determines its namespace and folder.
- Never create catch-all or helper namespaces (e.g. `Helpers`, `Utils`, `Common`, `Misc`, `Shared`). If you feel the need for one, it is a signal that the class has not been assigned its correct single responsibility yet.
- Organise source files by architectural layer (e.g. Controllers, Services, Repositories, Domain, DataObjects); each layer lives in its own folder. Within a layer, sub-folders (and sub-namespaces) group classes by the domain concept they serve (e.g. `Services/Account/`, `Services/CheckIn/`).
- Namespace must mirror folder structure exactly, and file location must match the namespace. A file in `Services/Account/` must declare namespace `[Root].Services.Account`, with no exceptions. Whenever a namespace changes, the file must be moved to the matching folder immediately. Examples of well-structured namespaces:
  - `[RootNamespace].Configuration`
  - `[RootNamespace].DataAccess`
  - `[RootNamespace].DataAccess.DataObjects`
  - `[RootNamespace].Logging`
  - `[RootNamespace].Services`
  - `[RootNamespace].Services.Mapping`
  - `[RootNamespace].Services.Models`
- Never create a `[xyz].Interfaces` namespace. Place interfaces in the same namespace and folder as their implementations.
- All `using` directives go at the top of the file, **outside** and **above** the `namespace` block; NEVER inside it.
- **NEVER use fully qualified type names inline.** This applies to ALL types without exception, including BCL types such as `System.Enum`, `System.Collections.Generic.List`, etc. Always add the appropriate `using` directive and reference the type by its short name. Examples:
  - WRONG: `System.Enum.GetValues<RuneElement>()` — CORRECT: `using System;` at the top, then `Enum.GetValues<RuneElement>()`
  - WRONG: `OpenRS.Net.Client.Events.ContentLoadedEventArgs eventArgs` — CORRECT: `using OpenRS.Net.Client.Events;` at the top, then `ContentLoadedEventArgs eventArgs`
- `using` directives must be organised into the following groups, in this order, each group separated from the next by exactly one blank line. All directives within each group must be sorted alphabetically.
  1. **`System.*` usings**: all namespaces rooted at `System`.
  2. **`Microsoft.*` usings**: all namespaces rooted at `Microsoft`.
  3. **NuGet / third-party package usings**: one group per package root namespace (e.g. all `Newtonsoft.*` together, all `Serilog.*` together), ordered alphabetically by package root namespace.
  4. **Current solution usings**: namespaces belonging to the solution being worked on, all in one group.
- The last `using` directive must always be separated from the `namespace` statement by exactly one blank line.
