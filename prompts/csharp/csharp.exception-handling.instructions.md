---
description: "Use when writing or editing C# code. Covers null handling, exception handling."
applyTo: "**/*.{cs}"
---
## C#

### Null Handling

- Use `is null` / `is not null` pattern. Do NOT use `== null` or `!= null`.
- No null-coalescing `??` operator.

### Exception Handling

- Use log-and-rethrow pattern: `catch (Exception exception) { logger.Error(...); throw; }`.
- Use `throw;` (NOT `throw exception;`) to preserve the stack trace.
- Use only BCL exceptions (`ArgumentNullException`, `KeyNotFoundException`, `AuthenticationException`). Do NOT create custom exception types.
- When throwing exceptions, always pass as much detail as possible; include the relevant value(s), parameter name(s), and a descriptive message that clearly identifies what was invalid or missing and why.
- Prefer `expression as TargetType` over `(TargetType)expression` wherever the cast may fail (i.e. when the object is not guaranteed to be of that type at compile time). Use a direct cast only when you are certain of the type and want an exception on failure.
