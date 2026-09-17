---
description: "Use when writing or editing C# logging code. Covers logging rules, standards and conventions."
applyTo: "**/*.{cs}"
---
## C#

### Logging
- When using `NuciLog`, always include an `Operation` in all log calls.
- When using `NuciLog`, always prefer `LogInfoKey` entries over embedding information directly in the `Message` string. Use `Message` only for content that cannot be expressed as a key-value pair.
- When using `NuciLog`, always pass exceptions via the dedicated `exception` parameter. Never embed exception messages or stack traces as text inside `Message`.
- When using `NuciLog`, always mark keys whose values contain passwords, tokens, API keys, credentials, or other secrets as sensitive by deriving the custom key from `LogInfoKey` and calling the protected `LogInfoKey(string name, bool isSensitive)` constructor with `true`, for example `base(name, true)`. Never place secrets in `Message`, exception text, operation names, status names, or key names, because sensitive masking applies to structured values whose `LogInfoKey.IsSensitive` value is `true`.
- When using `NuciLog`, place all custom `Operation` and `LogInfoKey` classes in the `[Project].Logging` namespace.
