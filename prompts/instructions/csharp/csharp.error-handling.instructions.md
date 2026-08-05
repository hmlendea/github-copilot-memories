---
description: "Use when writing or editing C# code. Covers null handling, error handling."
applyTo: "**/*.{cs}"
---

## C#

### Null Handling

- Use `is null` / `is not null` pattern. Do NOT use `== null` or `!= null`.
- No null-coalescing `??` operator.

### Exception Handling

- Use `throw;` (NOT `throw exception;`) to preserve the stack trace when rethrowing.
- Use only BCL exceptions (`ArgumentNullException`, `KeyNotFoundException`, `AuthenticationException`). Do NOT create custom exception types unless no BCL exception fits properly.

### Type Casting

- Prefer `expression as TargetType` over `(TargetType)expression` wherever the cast may fail (i.e. when the object is not guaranteed to be of that type at compile time). Use a direct cast only when you are certain of the type and want an exception on failure.
