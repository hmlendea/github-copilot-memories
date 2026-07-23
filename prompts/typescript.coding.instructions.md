---
description: "Use when writing or editing TypeScript or JavaScript code. Covers file structure, module organisation, naming, blank line rules, and code style."
applyTo: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
---
## TypeScript

- All general instructions from `general.instructions.md` apply here as well, unless explicitly overridden in this file.
- All general coding instructions from `general.coding.instructions.md` apply here as well, unless explicitly overridden in this file.
- All language instructions from `language.english.instructions.md` and `language.romanian.instructions.md` apply here as well, unless explicitly overridden in this file.

### File & Module Structure

- Each exported class, interface, type alias, or enum must be declared in its own file. The file name must exactly match the exported name (e.g. `AccountService.ts` for `AccountService`).
- Each class must have a single, well-defined responsibility. Do not add logic to a class unless it unambiguously belongs there. If a class grows beyond its responsibility or serves multiple concerns, split it immediately into smaller, focused classes, each placed in the module that matches its responsibility.
- Module choice is driven by responsibility, not by incidental proximity. A class that handles account validation belongs in `services/account/`, not in a generic `services/` or `utils/` folder.
- Never create catch-all or helper modules (e.g. `helpers`, `utils`, `common`, `misc`, `shared`). If you feel the need for one, it is a signal that the code has not been assigned its correct single responsibility yet.
- Organise source files by architectural layer (e.g. `controllers/`, `services/`, `repositories/`, `domain/`, `data-objects/`); each layer lives in its own folder. Within a layer, sub-folders group files by the domain concept they serve (e.g. `services/account/`, `services/check-in/`).
- File location must reflect the module structure. A file in `services/account/` must only export types logically belonging to that domain, with no exceptions.

### Blank Lines

- `if`, `for`, `for...of`, `while`, `switch`, `continue`, and `break` statements must always be separated from adjacent assignments or other statements by a blank line above and below.
- `return` statements must always be separated from other lines of code by a blank line above (unless they are the only statement in the function/method body or the first line after an opening brace).
- Never use two or more consecutive blank lines anywhere in the code.
- Never place an empty line immediately after an opening brace `{` or immediately before a closing brace `}`.
- All methods must have exactly one empty line between them: no more, no less.

### Naming Conventions

- Classes, enums, and type aliases: PascalCase.
- Interfaces: `I`-prefixed PascalCase (`IAccountService`).
- Functions, methods, variables, and parameters: camelCase.
- Private class members: camelCase, no underscore prefix (`accountRepository`, not `_accountRepository`).
- Module-level constants: `SCREAMING_SNAKE_CASE`.
- Boolean variables, properties, and functions must use a meaningful boolean-semantic prefix: `is`, `has`, `does`, `are`, or contextual tense-embedded forms (`...Was...`, `...Were...`), e.g. `isEnabled`, `hasPermission`, `requestWasHandled`. Never use vague names like `flag`, `check`, or `result` for booleans.

### Imports

- Organise `import` statements into the following groups, in this order, with exactly one blank line between groups:
  1. Built-in Node modules (`path`, `fs`, `os`, etc.).
  2. Third-party packages (`react`, `express`, etc.).
  3. Local imports (relative paths: `./`, `../`).
- Sort all imports alphabetically within each group.
- Prefer named exports and named imports over default exports.

### Code Style

- Use `const` for all declarations that are never reassigned. Use `let` only when reassignment is necessary. Never use `var`.
- Always use `===` and `!==`; never `==` or `!=`.
- Never use `any`. Use `unknown` when the type is genuinely unknown and narrow it explicitly with a type guard.
- Use `interface` over `type` for object shapes. Use `type` only for unions, intersections, or primitive aliases.
- Always declare explicit return types on exported and public functions and methods.
- Use `readonly` on class properties that are never reassigned after construction.
- Always use explicit braces for ALL control flow (`if`, `else`, `for`, `for...of`, `while`, `switch`), even for single-line bodies. Braceless bodies are never acceptable.
- The opening brace must appear on the same line as the statement (K&R style): `if (condition) {`.
