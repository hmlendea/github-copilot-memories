---
description: "Use when writing or editing TypeScript code. Covers coding style."
applyTo: "**/*.{ts,tsx}"
---
## TypeScript

### Code Style

- Use `const` for all declarations that are never reassigned. Use `let` only when reassignment is necessary. Never use `var`.
- Always use `===` and `!==`; never `==` or `!=`.
- Never use `any`. Use `unknown` when the type is genuinely unknown and narrow it explicitly with a type guard.
- Use `interface` over `type` for object shapes. Use `type` only for unions, intersections, or primitive aliases.
- Always declare explicit return types on exported and public functions and methods.
- Use `readonly` on class properties that are never reassigned after construction.
- Always use explicit braces for ALL control flow (`if`, `else`, `for`, `for...of`, `while`, `switch`), even for single-line bodies. Braceless bodies are never acceptable.
- The opening brace must appear on the same line as the statement (K&R style): `if (condition) {`.
