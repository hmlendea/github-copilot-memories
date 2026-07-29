---
description: "Use when writing or editing C# logging code. Covers logging rules, standards and conventions."
applyTo: "**/*.{cs}"
---
## C#

### Logging
- When using `NuciLog`, always include an `Operation` in all log calls.
- When using `NuciLog`, always prefer `LogInfoKey` entries over embedding information directly in the `Message` string. Use `Message` only for content that cannot be expressed as a key-value pair.
- When using `NuciLog`, always pass exceptions via the dedicated `exception` parameter. Never embed exception messages or stack traces as text inside `Message`.
- When using `NuciLog`, place all custom `Operation` and `LogInfoKey` classes in the `[Project].Logging` namespace.
