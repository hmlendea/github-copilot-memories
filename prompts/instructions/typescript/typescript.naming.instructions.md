---
description: "Use when writing or editing TypeScript code. Covers naming conventions."
applyTo: "**/*.{ts,tsx}"
---
## TypeScript

### Naming Conventions

- Classes, enums, and type aliases: PascalCase.
- Interfaces: `I`-prefixed PascalCase (`IAccountService`).
- Functions, methods, variables, and parameters: camelCase.
- Private class members: camelCase, no underscore prefix (`accountRepository`, not `_accountRepository`).
- Module-level constants: `SCREAMING_SNAKE_CASE`.
- Boolean variables, properties, and functions must use a meaningful boolean-semantic prefix: `is`, `has`, `does`, `are`, or contextual tense-embedded forms (`...Was...`, `...Were...`), e.g. `isEnabled`, `hasPermission`, `requestWasHandled`. Never use vague names like `flag`, `check`, or `result` for booleans.
