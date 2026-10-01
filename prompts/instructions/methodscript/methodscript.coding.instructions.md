---
description: "Use when writing or editing MethodScript code for Minecraft Spigot's CommandHelper plugin."
applyTo: "**/*.{ms,msa}"
---
## MethodScript

### Architecture and Paradigms

#### Project Structure Paradigm

- Feature package: `main.ms` orchestration, `auto_include.ms` shared procedures, `aliases.msa` alias signatures.
- Keep aliases out of `main.ms`, implementation out of `aliases.msa`; use root `auto_include.ms` for shared cross-package primitives.

#### Execution Model Paradigm

- Alias executions, event handlers, timeout callbacks, and thread closures are isolated flows.
- Reload-safe for `/reloadaliases`/`/recompile`: reinitialise without stale state.
- Commands, events, tasks, and threads use stable IDs for predictable replacement/unregistration.

#### Command Definition Paradigm

- Commands: associative options plus closures (`executor`, `condition`, `tab_completer`, metadata).
- Permission checks precede command/tab business logic. Parse early; pass validated arguments to focused helpers.

#### Event-Driven Paradigm

- Events: explicit ID, optional prefilter/condition, focused executor.
- Reject non-applicable events early. Cancel/mutate only where event contract permits.

#### Data and State Paradigm

- State layers: transient cache; global in-memory `import`/`export`; durable files.
- Structured options, locale bundles, and player data use associative arrays. Locales use values such as `{ro: ..., en: ...}` and resolve late.

#### Procedure-Centred Paradigm

- Procedures use explicit return/parameter types where practical. Centralise reusable logic in helpers.
- Closures serve scheduling, tab completion, asynchronous flows, and event dispatch callbacks.

#### Asynchronous and Scheduling Paradigm

- Move expensive/remote I/O, network, and transforms to threads or deferred callbacks.
- Keep thread-sensitive game operations on the main context. Use `set_timeout`, queues, and threads for staged work, never synchronous waiting.

#### Error and Reliability Paradigm

- Validate preconditions before side effects. Use controlled throws and `try/catch` at shell/file/network/API boundaries.
- Optional data paths use `import(..., default)` or safe getters.

#### Alias Language Paradigm

- Alias RHS: `run('/command ...')`, not legacy macro chains. Use `$` only as final variadic/free-form capture; signatures remain unambiguous.

#### Safety and Compatibility Paradigm

- Shell execution is privileged: validate/sanitise user input. No `eval`-style untrusted content.
- Mixed environments: compile-time capability checks (`function_exists`, `extension_exists`).