---
description: "Use when writing or editing MethodScript code for Minecraft Spigot's CommandHelper plugin."
applyTo: "**/*.{ms,msa}"
---
## MethodScript

### Architecture and Paradigms

#### Project Structure Paradigm

- **Local package triad** - Organise each feature package with `main.ms` (runtime orchestration), `auto_include.ms` (shared procedures), and `aliases.msa` (alias signatures).
- **Single-responsibility files** - Keep alias declaration logic out of `main.ms`, and keep heavy implementation logic out of `aliases.msa`.
- **Root-level shared utilities** - Use root `auto_include.ms` for cross-package primitives that are reused broadly.

#### Execution Model Paradigm

- **Independent execution units** - Treat alias executions, event handlers, timeout callbacks, and thread closures as isolated execution flows.
- **Reload-safe design** - Assume scripts may be recompiled frequently (`/reloadaliases` or `/recompile`), and write code that can be reinitialised without stale state.
- **Deterministic registration** - Use stable IDs for commands, events, tasks, and threads so replacement and unregistration are predictable.

#### Command Definition Paradigm

- **Declarative command registration** - Prefer associative option objects and closures for command behaviour (`executor`, `condition`, `tab_completer`, metadata fields).
- **Permission-first flow** - Gate command execution and tab completion through explicit permission checks before business logic.
- **Argument normalisation pipeline** - Parse arguments early and pass validated values to dedicated helpers.

#### Event-Driven Paradigm

- **Declarative event wiring** - Register events with explicit IDs, optional prefilter criteria, optional conditions, and focused executors.
- **Condition-first handlers** - Use fast guard clauses and conditions to reject non-applicable events early.
- **Controlled mutation** - Use event cancellation and mutation only when the event contract supports it.

#### Data and State Paradigm

- **Layered state strategy** - Distinguish between transient cache state, global in-memory state (`import`/`export`), and durable file-backed state.
- **Associative arrays as records** - Represent structured objects (options, locale bundles, player data) with associative arrays.
- **Localisation as data** - Model localised messages as structured values (for example `{ro: ..., en: ...}`) and resolve language late.

#### Procedure-Centred Paradigm

- **Strongly typed boundaries** - Declare explicit return and parameter types for procedures wherever practical.
- **Utility procedure abstraction** - Centralise reusable logic in helper procedures, then compose features through these helpers.
- **Composable closures** - Use closures for callbacks in scheduling, tab completion, asynchronous flows, and event dispatch.

#### Asynchronous and Scheduling Paradigm

- **Non-blocking by design** - Move expensive or remote work (I/O, network, heavy transforms) to threads or deferred callbacks.
- **Main-thread safety** - Keep thread-sensitive game operations on the main runtime context.
- **Timeout and queue orchestration** - Use `set_timeout`, queue, and thread utilities for staged operations instead of synchronous waiting.

#### Error and Reliability Paradigm

- **Fail-fast guards** - Validate preconditions early and return or throw before side effects.
- **Explicit exception channels** - Prefer controlled throw helpers and `try/catch` around external boundaries (shell, file, network, API calls).
- **Recoverable defaults** - Use `import(..., default)` or custom safe getters for optional data paths.

#### Alias Language Paradigm

- **Best-practice alias RHS** - Prefer `run('/command ...')` on alias right-hand sides instead of legacy macro chaining for maintainability.
- **Final-variable capture** - Use `$` as the final capture variable only when truly necessary for variadic/free-form command tails.
- **Non-ambiguous signatures** - Avoid alias definitions that can match the same command input in multiple ways.

#### Safety and Compatibility Paradigm

- **Shell boundary hardening** - Treat shell execution as privileged; validate and sanitise any user-derived inputs.
- **Dynamic code caution** - Avoid `eval`-style patterns for untrusted content.
- **Feature compatibility checks** - Use compile-time capability checks (`function_exists`, `extension_exists`) when supporting mixed environments.