---
description: "Use when writing or editing C# interfaces."
applyTo: "**/I*.{cs}"
---
## C#

### Naming Conventions
- Interfaces: `I`-prefixed PascalCase (`IAccountService`).
- For each eligible non-static concrete class with at least one `public` method (excluding models/entities), define and maintain an equivalent interface (`ClassName` <-> `IClassName`) and keep the class implementation aligned with the interface contract.

### Documentation
- All interface members in NuGet packages must have XML documentation comments (`/// <summary>...</summary>`). These must NEVER be removed or omitted, including during refactoring. When a member is renamed, moved, or restructured, its XML documentation must be preserved and updated to reflect the change.
