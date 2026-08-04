---
description: "Use when writing or editing C# code. Covers custom exception types."
applyTo: "**/*Exception.{cs}"
---
## C#

### Exceptions
- Exception type names must always end with `Exception`.
- Each constructor overload must also have an additional overload that accepts an `Exception innerException` parameter.
- All constructor overloads must ultimately call the base `Exception` constructor with the appropriate parameters.