---
description: "Use when writing or editing C# interfaces."
applyTo: "**/I*.{cs}"
---
## C#

### Naming Conventions

- Interfaces: `I`-prefixed PascalCase (`IAccountService`).

### Documentation

- All interface members in NuGet packages must have XML documentation comments (`/// <summary>...</summary>`). These must NEVER be removed or omitted, including during refactoring. When a member is renamed, moved, or restructured, its XML documentation must be preserved and updated to reflect the change.
