---
description: "Use for C# collection APIs, XML-serialised collections, collection expressions, or LINQ."
---
## C#

### Collections

- Use `IEnumerable<T>` as the return type and parameter type for all collections. Never `List<T>`, `IList<T>`, `IReadOnlyList<T>`, `HashSet<T>`.
- **Exception:** entity/data objects that are XML-serialised (e.g. via `XmlSerializer`) must use `List<T>` for collection properties, as the XML serialiser cannot reflect interface types.
- Use C# 12 collection expressions `[...]` for inline collection initialization of **any** collection type (`List<T>`, `Dictionary<K,V>`, arrays, etc.), including empty ones. `new List<T>()`, `new Dictionary<K,V>()`, `new T[]{}` are all wrong; use `[]` instead.
- Use LINQ (`.Where()`, `.Any()`, `.First()`, `.Select()`, `.Append()`) for in-memory querying.
