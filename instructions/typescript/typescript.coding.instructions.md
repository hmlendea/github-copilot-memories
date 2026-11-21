---
description: "Use for TypeScript edits. Covers files, modules, imports, and spacing."
applyTo: "**/*.{ts,tsx}"
---
## TypeScript

### File & Module Structure

- Each exported class, interface, type alias, or enum must be declared in its own file. The file name must exactly match the exported name (e.g. `AccountService.ts` for `AccountService`).
- Module choice is driven by responsibility, not by incidental proximity. A class that handles account validation belongs in `services/account/`, not in a generic `services/` or `utils/` folder.
- Organise source files by architectural layer (e.g. `controllers/`, `services/`, `repositories/`, `domain/`, `data-objects/`); each layer lives in its own folder. Within a layer, sub-folders group files by the domain concept they serve (e.g. `services/account/`, `services/check-in/`).
- File location must reflect the module structure. A file in `services/account/` must only export types logically belonging to that domain, with no exceptions.

### Blank Lines

- `if`, `for`, `for...of`, `while`, `switch`, `continue`, and `break` statements must always be separated from adjacent assignments or other statements by a blank line above and below.
- `return` statements must always be separated from other lines of code by a blank line above (unless they are the only statement in the function/method body or the first line after an opening brace).
- Never place an empty line immediately after an opening brace `{` or immediately before a closing brace `}`.
- All methods must have exactly one empty line between them: no more, no less.

### Imports

- Organise `import` statements into the following groups, in this order, with exactly one blank line between groups:
  1. Built-in Node modules (`path`, `fs`, `os`, etc.).
  2. Third-party packages (`react`, `express`, etc.).
  3. Local imports (relative paths: `./`, `../`).
- Sort all imports alphabetically within each group.
- Prefer named exports and named imports over default exports.
