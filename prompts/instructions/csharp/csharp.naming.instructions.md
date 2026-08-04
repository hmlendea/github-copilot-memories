---
description: "Use when writing or editing C# code. Covers naming rules and conventions."
applyTo: "**/*.{cs}"
---
## C#

### Naming Conventions

- Always use the lowercase alias for built-in types: `string`, `int`, `bool`, `object`, `long`, `double`, `float`, `decimal`, `byte`, `char`, etc. NEVER use the BCL class names `String`, `Int32`, `Boolean`, `Object`, etc.
- All `public` and `protected` members — without exception — must begin with an uppercase letter. This applies to fields, properties, methods, events, delegates, constructors, and nested types, regardless of context.
- Methods: PascalCase, clear and explicit names with no abbreviations or shortenings, following the same naming rules as for variables and parameters.
- Classes: PascalCase.
- For eligible non-static classes (those with at least one `public` method and not models/entities), the equivalent interface name must be `I` + class name (`AccountService` -> `IAccountService`), and the class must implement that interface.
- Data/entity objects: `DataObject` suffix (`AccountDataObject`).
- Domain models: plain noun, no suffix (`Account`, `CheckIn`).
- Request DTOs: Verb + Noun + `Request` (`AddAccountRequest`, `RecordCheckInRequest`).
- Response DTOs: `Get` + Noun + `Response` (`GetAccountResponse`).
- Configuration classes: Noun + `Settings` (`DataStoreSettings`).
- Private fields: camelCase, NO underscore prefix (`accountRepository`, not `_accountRepository`).
- Boolean variables, properties, and methods must use a meaningful boolean-semantic prefix: `Is`, `Has`, `Does`, `Are`, or contextual tense-embedded forms (`...Was...`, `...Were...`, `...Is...`, `...Does...`, `...Are...`), e.g. `IsEnabled`, `HasPermission`, `DoesExist`, `AreValid`, `requestWasHandled`, `itemsAreLoaded`. Never use vague names like `flag`, `check`, or `result` for booleans.
- Private fields: camelCase, NO underscore prefix (`accountRepository`, not `_accountRepository`).