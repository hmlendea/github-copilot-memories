---
description: "Use when writing or editing TypeScript or JavaScript code. Covers file structure, module organisation, naming, blank line rules, and code style."
applyTo: ["**/*.ts", "**/*.tsx"]
---
## TypeScript

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
- Never place an empty line immediately after an opening brace `{`.
- All methods must have exactly one empty line between them: no more, no less.
