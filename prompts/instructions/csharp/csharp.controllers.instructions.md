---
description: "Use when writing or editing C# controller classes."
applyTo: "**/*Controller.{cs}"
---
## C#

### Naming Conventions

- Controllers: pluralized noun + `Controller` (`AccountsController`).

### Controller Style

- Controller actions return `ActionResult` (not `ActionResult<T>`).
- Use expression-bodied actions for single-expression delegates to a `ProcessRequest(...)` call.
