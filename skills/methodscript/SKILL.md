---
name: methodscript
description: Use when writing or editing MethodScript code for Minecraft Spigot's CommandHelper plugin. Supplies the architecture and paradigm rules (project structure, execution model, commands, events, data and state, procedures, asynchronous scheduling, error and reliability, alias language, safety and compatibility), the style conventions (syntax and formatting, aliases, naming and typing, command and event option objects, error handling and guards, comments and documentation, project and file organisation, concurrency and runtime safety, persistence and IO, maintenance), and references for the 897 built-in functions and 104 bindable events of MethodScript 3.3.5.
---

# MethodScript

Apply when writing or editing `.ms` and `.msa` files for Minecraft Spigot's CommandHelper plugin.

## Built-in Function and Event References

This skill bundles a reference for every built-in function and bindable event, extracted from the official MethodScript 3.3.5 documentation:
- `references/functions/` - 897 functions across 57 categories, one file per category; each entry lists the signature, return type, thrown exceptions, restriction flag, and a behaviour summary.
- `references/events.md` - 104 events across 10 categories; each entry lists its behaviour, prefilter fields, event data keys, and mutable fields.

Open only the category file needed for the task instead of loading every reference. Consult the upstream pages (`https://methodscript.com/docs/3.3.5/API.html` and `https://methodscript.com/docs/3.3.5/Event_API.html`) for complete prose, worked examples, and anything the summaries omit.

### Function Reference Index

| Category | Reference file | Functions |
|----------|----------------|-----------|
| ArrayHandling | `references/functions/array_handling.md` | 43 |
| BasicLogic | `references/functions/basic_logic.md` | 31 |
| BossBar | `references/functions/boss_bar.md` | 8 |
| BukkitMetadata | `references/functions/bukkit_metadata.md` | 4 |
| ByteArrays | `references/functions/byte_arrays.md` | 23 |
| Clipboard | `references/functions/clipboard.md` | 2 |
| Cmdline | `references/functions/cmdline.md` | 27 |
| Commands | `references/functions/commands.md` | 7 |
| Compiler | `references/functions/compiler.md` | 2 |
| ControlFlow | `references/functions/control_flow.md` | 16 |
| Crypto | `references/functions/crypto.md` | 12 |
| DataHandling | `references/functions/data_handling.md` | 41 |
| DataTransformations | `references/functions/data_transformations.md` | 8 |
| Debug | `references/functions/debug.md` | 6 |
| Easings | `references/functions/easings.md` | 2 |
| Echoes | `references/functions/echoes.md` | 12 |
| Enchantments | `references/functions/enchantments.md` | 8 |
| EntityManagement | `references/functions/entity_management.md` | 73 |
| Environment | `references/functions/environment.md` | 46 |
| EventBinding | `references/functions/event_binding.md` | 13 |
| Exceptions | `references/functions/exceptions.md` | 5 |
| ExecutionQueue | `references/functions/execution_queue.md` | 8 |
| ExtensionMeta | `references/functions/extension_meta.md` | 4 |
| FileHandling | `references/functions/file_handling.md` | 7 |
| InventoryManagement | `references/functions/inventory_management.md` | 34 |
| ItemMeta | `references/functions/item_meta.md` | 5 |
| Marquee | `references/functions/marquee.md` | 2 |
| Math | `references/functions/math.md` | 37 |
| MatrixHandling | `references/functions/matrix_handling.md` | 19 |
| Meta | `references/functions/meta.md` | 24 |
| Minecraft | `references/functions/minecraft.md` | 18 |
| MobManagement | `references/functions/mob_management.md` | 51 |
| OAuth | `references/functions/oauth.md` | 2 |
| OS | `references/functions/os.md` | 1 |
| ObjectManagement | `references/functions/object_management.md` | 2 |
| Performance | `references/functions/performance.md` | 1 |
| Permissions | `references/functions/permissions.md` | 1 |
| Persistence | `references/functions/persistence.md` | 5 |
| PlayerManagement | `references/functions/player_management.md` | 111 |
| PluginMeta | `references/functions/plugin_meta.md` | 6 |
| Recipes | `references/functions/recipes.md` | 6 |
| Reflection | `references/functions/reflection.md` | 10 |
| Regex | `references/functions/regex.md` | 6 |
| ResourceManager | `references/functions/resource_manager.md` | 2 |
| SQL | `references/functions/sql.md` | 3 |
| Sandbox | `references/functions/sandbox.md` | 5 |
| Scheduling | `references/functions/scheduling.md` | 11 |
| Scoreboards | `references/functions/scoreboards.md` | 21 |
| Statistics | `references/functions/statistics.md` | 5 |
| StringHandling | `references/functions/string_handling.md` | 32 |
| TaskHandling | `references/functions/task_handling.md` | 2 |
| Threading | `references/functions/threading.md` | 11 |
| Trades | `references/functions/trades.md` | 7 |
| Weather | `references/functions/weather.md` | 5 |
| Web | `references/functions/web.md` | 5 |
| World | `references/functions/world.md` | 38 |
| XGUI | `references/functions/xgui.md` | 1 |

Reference files are relative to this skill directory. Fall back to `function_exists(<name>)` and the upstream documentation when a function is absent, deprecated, or supplied by an extension.

## Architecture and Paradigms

### Project Structure Paradigm

- Feature package: `main.ms` orchestration, `auto_include.ms` shared procedures, `aliases.msa` alias signatures.
- Keep aliases out of `main.ms`, implementation out of `aliases.msa`; use root `auto_include.ms` for shared cross-package primitives.

### Execution Model Paradigm

- Alias executions, event handlers, timeout callbacks, and thread closures are isolated flows.
- Reload-safe for `/reloadaliases`/`/recompile`: reinitialise without stale state.
- Commands, events, tasks, and threads use stable IDs for predictable replacement/unregistration.

### Command Definition Paradigm

- Commands: associative options plus closures (`executor`, `condition`, `tab_completer`, metadata).
- Permission checks precede command/tab business logic. Parse early; pass validated arguments to focused helpers.

### Event-Driven Paradigm

- Events: explicit ID, optional prefilter/condition, focused executor.
- Reject non-applicable events early. Cancel/mutate only where event contract permits.

### Data and State Paradigm

- State layers: transient cache; global in-memory `import`/`export`; durable files.
- Structured options, locale bundles, and player data use associative arrays. Locales use values such as `{ro: ..., en: ...}` and resolve late.

### Procedure-Centred Paradigm

- Procedures use explicit return/parameter types where practical. Centralise reusable logic in helpers.
- Closures serve scheduling, tab completion, asynchronous flows, and event dispatch callbacks.

### Asynchronous and Scheduling Paradigm

- Move expensive/remote I/O, network, and transforms to threads or deferred callbacks.
- Keep thread-sensitive game operations on the main context. Use `set_timeout`, queues, and threads for staged work, never synchronous waiting.

### Error and Reliability Paradigm

- Validate preconditions before side effects. Use controlled throws and `try/catch` at shell/file/network/API boundaries.
- Optional data paths use `import(..., default)` or safe getters.

### Alias Language Paradigm

- Alias RHS: `run('/command ...')`, not legacy macro chains. Use `$` only as final variadic/free-form capture; signatures remain unambiguous.

### Safety and Compatibility Paradigm

- Shell execution is privileged: validate/sanitise user input. No `eval`-style untrusted content.
- Mixed environments: compile-time capability checks (`function_exists`, `extension_exists`).
- Restricted functions require explicit CommandHelper permission before they run; check the `[restricted]` marker in the function references and confirm permission handling before use.

## Style Rules and Conventions

### Syntax and Formatting

- Procedures use explicit types (`auto`, `boolean`, `string`, `int`, `array`) where practical.
- Prefer keyword/brace syntax for `proc`, `if`, loops, and `try/catch` over function-form flow.
- Non-trivial aliases: `>>>`/`<<<`, one operation per line. Avoid backslash macro chains; use explicit `run(...)` blocks.
- Prefer explicit `.` concatenation, especially for command strings. Terminate operational script statements with semicolons.

### Alias Conventions

- Quote alias literals/command fragments with parse-sensitive characters (e.g. `-`).
- Optional alias parameters: `[$var=default]` with static defaults.

### Naming and Typing

- Procedures: lowercase snake_case; private/internal helpers `_`-prefixed.
- Variables: `@var` scripts, `$var` alias parameters. Prefer descriptive names such as `@player_uuid`, `@cache_expiry_sec`.
- Associative keys/IDs remain stable and predictable: lowercase snake_case or kebab-case per subsystem.

### Command and Event Option Objects

- Closures use explicit context-specific parameters (e.g. executor/player/args/locale).
- Context-dependent command/event options provide `condition` closures.

### Error Handling and Guards

- Before deep access use `is_null`, `array_index_exists`, or project wrappers.

### Comments and Documentation

- Comments: concise intent/non-obvious invariants only. Preserve local `#` style, including disabled lines.
- Keep `@command`, `@usage`, `@permission`, and `@param` metadata synchronised with behaviour.

### Project and File Organisation

- Package-specific procedures remain in their LocalPackage unless intentionally cross-cutting.

### Concurrency and Runtime Safety

- `x_new_thread` IDs are deterministic/namespaced. Keep game-world mutation in safe runtime context; not every API is thread-safe.
- Delayed actions use `set_timeout` with explicit delays and short focused closures.

### Persistence and IO Conventions

- Resolve/validate paths before writes. Use JSON/YML intentionally; keep schemas stable across writes.

### Maintenance Conventions

- `.ms`/`.msa`: UTF-8. Keep utility procedures pure where possible; isolate side effects in orchestrators.
