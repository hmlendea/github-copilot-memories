---
description: "Use for C# null handling, exceptions, error handling, or type casting."
---

## C#

### Null Handling

- Use `is null` / `is not null` pattern. Do NOT use `== null` or `!= null`.
- No null-coalescing `??` operator.

### Exception Handling

- Use `throw;` (NOT `throw exception;`) to preserve the stack trace when rethrowing.
- Use only BCL exceptions (`ArgumentNullException`, `KeyNotFoundException`, `AuthenticationException`). Do NOT create custom exception types unless no BCL exception fits properly.
- Centralise reusable error messages in a dedicated message/constants type. Use named formatting helpers for parameterised messages and avoid duplicating message strings at throw sites.
- For a null argument, use `ArgumentNullException.ThrowIfNull` when supported by the target framework; otherwise throw `ArgumentNullException` with the real parameter name. Reuse an existing project guard helper when available; do not create a custom exception or derive one from a guard utility for this case.

### Type Casting

- Prefer `expression as TargetType` over `(TargetType)expression` wherever the cast may fail (i.e. when the object is not guaranteed to be of that type at compile time). Use a direct cast only when you are certain of the type and want an exception on failure.
