---
description: "Use when writing or editing C# code. Covers naming rules and conventions."
applyTo: "**/*.{cs}"
---
## C#

### Naming Conventions

- Always use the lowercase alias for built-in types: `string`, `int`, `bool`, `object`, `long`, `double`, `float`, `decimal`, `byte`, `char`, etc. NEVER use the BCL class names `String`, `Int32`, `Boolean`, `Object`, etc.
- All `public` and `protected` fields, properties, methods, events, delegates, constructors, and nested types begin uppercase.
- Methods and classes: PascalCase; common explicit-name rules apply.
- Data/entity objects: `DataObject` suffix (`AccountDataObject`).
- Domain models: plain noun, no suffix (`Account`, `CheckIn`).
- Request DTOs: Verb + Noun + `Request` (`AddAccountRequest`, `RecordCheckInRequest`).
- Response DTOs: `Get` + Noun + `Response` (`GetAccountResponse`).
- Configuration classes: Noun + `Settings` (`DataStoreSettings`).
- Private fields: camelCase, NO underscore prefix (`accountRepository`, not `_accountRepository`).
- Booleans use `Is`, `Has`, `Does`, `Are`, or contextual `Was`/`Were`/`Is`/`Does`/`Are` forms (for example, `requestWasHandled`). Never use `flag`, `check`, or `result`.