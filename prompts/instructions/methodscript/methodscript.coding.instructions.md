---
description: "Use when writing or editing MethodScript code for Minecraft Spigot's CommandHelper plugin."
applyTo: "**/*.{ms,msa}"
---
## MethodScript

### Language and Runtime Reference

#### Core Data Model

- **Primary value types** - MethodScript core runtime values include `string`, `int`, `double`, `boolean`, `null`, and `array`.
- **Arrays** - Indexed arrays are created with `array(...)`; key-value structures are represented with `associative_array(...)`.
- **Variable model** - Alias parameters use `$...`, while script-level variables use `@...`; globals are commonly accessed with `import(...)` and persisted with `export(...)` style flows.
- **Callable blocks** - `closure(...) { ... }` supports callback-style execution in scheduling, queues, and threading.
- **Null and equality checks** - Runtime behaviour can differ by coercion context, so explicit null and equality checks reduce ambiguity.

#### Execution and File Model

- **Execution units** - `main.ms`, each alias body, bound event handlers, queue elements, and timed callbacks execute as separate units.
- **Role of files** - `main.ms` is startup/reload execution, `auto_include.ms` provides shared declarations, and `aliases.msa` contains alias definitions.
- **Alias signatures** - Signatures should remain non-ambiguous because overlapping match paths create compile-time conflicts.
- **Alias variables** - Optional arguments use `[$var=default]`, and the final variable `$` captures trailing free-form arguments.

#### Event and Callback Model

- **Register handlers** - Event bindings (for example via helper wrappers around `bind`) should include deterministic IDs and explicit conditions.
- **Deregister handlers** - Unbind handlers during teardown to prevent stale listeners across reload cycles.
- **Event mutation and cancellation** - Event APIs support cancellation, consumption, and event mutation where the event type permits it.
- **Filtering** - Narrow binding conditions reduce unnecessary handler execution and side effects.

#### Command and Metadata Integration

- **Smart comment command metadata** - `@command`, `@usage`, `@permission`, `@param`, and tab-completion annotations provide command-system integration.
- **Runtime registration caveat** - Some command metadata changes may require stronger reload boundaries than alias body changes.

#### Runtime Operations

- **Reload commands** - `/reloadaliases` maps to `/recompile` and is the normal refresh path after script edits.
- **Module reload behaviour** - Partial recompile modes can leave inconsistent runtime state versus full-module reload.

#### Capability Areas

- **Control and logic** - Branching, loop, and logical function groups drive script flow.
- **Arrays and data handling** - Array traversal, mapping, merge, serialisation, and coercion helpers are core data tools.
- **Strings and regex** - Pattern matching, replacement, splitting, formatting, and validation functions cover text processing.
- **Math and numeric** - Arithmetic, rounding, bounds checks, randomisation, and conversions support numeric workflows.
- **Exceptions** - Exception constructs support catch, propagation, and controlled failure handling.
- **Persistence and IO** - File and persistence primitives support durable state and data exchange.
- **Scheduling and queues** - Timers and queue functions support deferred and staged execution.
- **Threading** - Thread APIs (including `x_new_thread`) support asynchronous execution.
- **Integration surfaces** - SQL, web/network, and server/world/player APIs provide external and platform integration.

#### Safety and Reliability Notes

- **Shared state** - Imported/exported global data can be accessed from multiple execution paths, so race conditions are possible.
- **Dynamic evaluation** - Runtime evaluation of untrusted input can introduce security and correctness risks.
- **Teardown discipline** - Reload-safe scripts release scheduled work, event bindings, and transient state deterministically.