---
description: "Use when writing or editing MethodScript code for Minecraft Spigot's CommandHelper plugin."
applyTo: "**/*.{ms,msa}"
---
## MethodScript

### Style Rules and Conventions

#### Syntax and Formatting

- Procedures use explicit types (`auto`, `boolean`, `string`, `int`, `array`) where practical.
- Prefer keyword/brace syntax for `proc`, `if`, loops, and `try/catch` over function-form flow.
- Non-trivial aliases: `>>>`/`<<<`, one operation per line. Avoid backslash macro chains; use explicit `run(...)` blocks.
- Prefer explicit `.` concatenation, especially for command strings. Terminate operational script statements with semicolons.

#### Alias Conventions

- Quote alias literals/command fragments with parse-sensitive characters (e.g. `-`).
- Optional alias parameters: `[$var=default]` with static defaults.

#### Naming and Typing

- Procedures: lowercase snake_case; private/internal helpers `_`-prefixed.
- Variables: `@var` scripts, `$var` alias parameters. Prefer descriptive names such as `@player_uuid`, `@cache_expiry_sec`.
- Associative keys/IDs remain stable and predictable: lowercase snake_case or kebab-case per subsystem.

#### Command and Event Option Objects

- Closures use explicit context-specific parameters (e.g. executor/player/args/locale).
- Context-dependent command/event options provide `condition` closures.

#### Error Handling and Guards

- Before deep access use `is_null`, `array_index_exists`, or project wrappers.

#### Comments and Documentation

- Comments: concise intent/non-obvious invariants only. Preserve local `#` style, including disabled lines.
- Keep `@command`, `@usage`, `@permission`, and `@param` metadata synchronised with behaviour.

#### Project and File Organisation

- Package-specific procedures remain in their LocalPackage unless intentionally cross-cutting.

#### Concurrency and Runtime Safety

- `x_new_thread` IDs are deterministic/namespaced. Keep game-world mutation in safe runtime context; not every API is thread-safe.
- Delayed actions use `set_timeout` with explicit delays and short focused closures.

#### Persistence and IO Conventions

- Resolve/validate paths before writes. Use JSON/YML intentionally; keep schemas stable across writes.

#### Maintenance Conventions

- `.ms`/`.msa`: UTF-8. Keep utility procedures pure where possible; isolate side effects in orchestrators.