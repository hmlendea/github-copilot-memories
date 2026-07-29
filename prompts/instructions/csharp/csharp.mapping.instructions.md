---
description: "Use when writing or editing C# mappings."
applyTo: "**/*{Mappings,MappingExtensions}.{cs}"
---
## C#

### Naming Conventions

- Mapping classes: Noun + `MappingExtensions` (`AccountMappingExtensions`).
- Mapping methods: `ToServiceModel` / `ToServiceModels` for entity->model direction; `ToDataObject` / `ToDataObjects` for model->entity direction.

### Type Declarations

- Mapping extension classes: explicitly `internal static class`.
- Mapping extension methods: explicitly `internal static`.

### Methods

- Use expression-bodies (`=>`) for methods whose entire body is a single `new() { ... }` initialiser; do NOT assign to a local variable and return it: `internal static Foo ToDataObject(this Bar bar) => new() { Id = bar.Id };`. This applies unconditionally to all mapping extension methods (`ToServiceModel`, `ToDataObject`, and their plurals).
