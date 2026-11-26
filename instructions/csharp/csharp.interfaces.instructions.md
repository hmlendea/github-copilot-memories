---
description: "Use when writing or editing C# interfaces."
applyTo: "**/I*.{cs}"
---
## C#

### Naming Conventions
- Interfaces: `I`-prefixed PascalCase (`IAccountService`).
- Every non-static concrete class with a public instance method requires a colocated equivalent interface (`ClassName` <-> `IClassName`), except domain models and data/entities. Mirror its public instance contract; controllers and test fixtures are not implicitly exempt. Required instance signatures take precedence over the state-free `static` preference.

### Documentation
- All interface members in NuGet packages must have XML documentation comments (`/// <summary>...</summary>`). These must NEVER be removed or omitted, including during refactoring. When a member is renamed, moved, or restructured, its XML documentation must be preserved and updated to reflect the change.
