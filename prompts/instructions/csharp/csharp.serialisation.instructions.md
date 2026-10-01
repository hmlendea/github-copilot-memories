---
description: "Use for C# date parsing/formatting, API DTO JSON names, or JsonSerializerOptions allocation."
---
## C#

### Parsing And Serialisation

- Always use a format provider when parsing or formatting date-time objects. Use `CultureInfo.InvariantCulture` for culture-independent operations (the most common case), or an explicitly specified culture when required. Methods like `DateTime.Parse()`, `DateTime.TryParse()`, `ParseExact()`, `TryParseExact()`, `ToString()`, and similar should always receive a format provider or format string. Never call `DateTime.Parse("2026-08-05")` without a format provider; use `DateTime.ParseExact("2026-08-05", "yyyy-MM-dd", CultureInfo.InvariantCulture)` instead.
- For API request and response DTOs, every property name segment `Identifier` must serialise with `id` in JSON names via `JsonPropertyName`. Examples: `Identifier` -> `id`, `AccountIdentifier` -> `accountId`, `UserIdentifier` -> `userId`.
- Do not allocate `JsonSerializerOptions` repeatedly in hot paths or loops. Cache and reuse static readonly options instances.
