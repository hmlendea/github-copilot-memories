---
description: "Use when writing or editing MethodScript code for Minecraft Spigot's CommandHelper plugin."
applyTo: "**/*.{ms,msa}"
---
## MethodScript

### Style Rules and Conventions

#### Syntax and Formatting

- **Procedure declaration** - Declare procedures with explicit return and argument types (`auto`, `boolean`, `string`, `int`, `array`) where practical.
- **Brace syntax preference** - Prefer keyword and brace syntax for `proc`, `if`, loops, and `try/catch` over function-form flow control.
- **Multiline alias construct** - For non-trivial alias logic, use `>>>` and `<<<` with one operation per line.
- **Macro minimisation** - Avoid long backslash macro chains; convert to multiline blocks with explicit `run(...)` calls.
- **Concatenation explicitness** - Prefer explicit `.` concatenation, especially when composing command strings.
- **Statement clarity** - Terminate operational statements with semicolons in script blocks for consistency.

#### Alias Conventions

- **Best-practice alias RHS** - Prefer `run('/command ...')` on alias right-hand sides, including forwarding aliases.
- **Special-character quoting** - Quote alias literals or command fragments containing parse-sensitive characters (for example `-`).
- **Optional arguments** - Use `[$var=default]` for optional alias parameters; keep defaults static.
- **Final variable discipline** - Use `$` only as the final variadic capture when free-form argument tails are required.
- **Signature uniqueness** - Avoid ambiguous alias signatures that may match the same invocation path.

#### Naming and Typing

- **Procedure naming** - Use lowercase snake_case for procedures; prefix private/internal helpers with `_`.
- **Variable prefixes** - Use `@var` for script variables and `$var` for alias-signature parameters.
- **Descriptive identifiers** - Prefer semantically descriptive names (`@player_uuid`, `@cache_expiry_sec`) over short opaque names.
- **Key naming consistency** - Keep associative-array keys and IDs stable and predictable, typically lowercase snake_case or lowercase kebab-case based on the subsystem.

#### Command and Event Option Objects

- **Associative option payloads** - Use associative arrays for command and event options instead of long positional parameter lists.
- **Closure signatures** - Keep closure parameters explicit and context-specific (for example executor/player/args/locale).
- **Condition-first option sets** - Provide `condition` closures when command or event execution is context dependent.

#### Error Handling and Guards

- **Guard clauses first** - Validate permissions, existence checks, and argument shape before mutation or external calls.
- **Null safety** - Use explicit null/empty helpers (`is_null`, `array_index_exists`, project wrappers) before deep access.
- **External boundary protection** - Wrap shell, network, and file operations in `try/catch` where failure is plausible.

#### Comments and Documentation

- **Comment style** - Use concise single-line comments for intent and non-obvious invariants; avoid narrating obvious code.
- **Repository convention** - In this codebase, `#` comments are common (including temporarily disabled lines); preserve existing local style when editing.
- **Smart metadata comments** - Where command metadata is used, keep annotations (`@command`, `@usage`, `@permission`, `@param`) synchronised with actual command behaviour.

#### Project and File Organisation

- **Role separation** - Keep runtime registration and orchestration in `main.ms`, shared helpers in `auto_include.ms`, and aliases in `aliases.msa`.
- **Feature modularity** - Keep package-specific procedures in their LocalPackage unless they are intentionally cross-cutting.
- **Localisation structure** - Represent translatable output as structured locale maps and resolve at emission time.

#### Concurrency and Runtime Safety

- **Thread naming** - Use deterministic, namespaced thread IDs when calling `x_new_thread`.
- **Main-thread operations** - Keep game-world mutation in safe runtime context; do not assume all API calls are thread-safe.
- **Delayed execution clarity** - Use `set_timeout` for delayed actions with explicit delay values and short, focused closures.

#### Persistence and IO Conventions

- **State layering** - Use `import`/`export` for process-local shared state and dedicated file helpers for durable state.
- **Path safety** - Resolve and validate file paths before write operations.
- **Serialisation format choice** - Use JSON/YML intentionally, and keep data schema stable across writes.

#### Maintenance Conventions

- **Encoding** - Save `.ms` and `.msa` as UTF-8.
- **Backward compatibility** - Prefer patterns that remain compatible with `reloadaliases`/`recompile` workflows.
- **Minimal side effects** - Keep utility procedures pure where possible; isolate side effects in orchestrator procedures.