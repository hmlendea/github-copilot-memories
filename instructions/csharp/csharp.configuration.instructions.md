---
description: "Use for C# configuration settings classes, JSON configuration files, configuration keys, or configuration binding. Covers camelCase keys, case-insensitive lookup, and key-name mapping."
applyTo: "**/*.{cs,json}"
---
## C#

### Configuration

- Read every setting from the configuration providers; never hardcode a configurable value in code.
- JSON configuration files (`appsettings.json`, `appsettings.{Environment}.json`) use camelCase for every section root and key, for example `cacheDurationInMinutes`, `patreonUsername`, and `saltBank`.
- Configuration key lookup is case-insensitive, so any casing resolves to the same setting and casing is never used to disambiguate keys. Treat the camelCase form as canonical.
- The binder matches a key to a property name ignoring case, and a camelCase key differs from a PascalCase property only by case, so camelCase keys bind without a mapping attribute. Never add `[ConfigurationKeyName]` when its value differs from the property name only by case.
- Add `[ConfigurationKeyName("key")]` only when the key must differ from the property name by more than case, such as when a property shortened to `Identifier` must bind `id`.
- Settings classes use `public sealed class`, are named `[Noun]Settings`, and live in the `[Root].Configuration` namespace. Declare one public auto-property per key with an empty default (`string.Empty`).
- Expose the section name as `public static string SectionName => "camelCase";` and bind with `configuration.GetSection(XSettings.SectionName).Bind(settings)`.
- Absent or blank optional settings keep their empty default, and the consuming code decides whether to omit the affected feature.
- Validate required settings while starting, and reject invalid values with `ArgumentOutOfRangeException` or `ArgumentException` before the application serves traffic.
- When the same settings class is also serialised as JSON for an API or a file, add `[JsonPropertyName("camelCase")]` alongside the mapping attribute when one is required, so both binding paths agree.
