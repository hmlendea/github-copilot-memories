---
description: "Use when writing or editing MethodScript code for Minecraft Spigot's CommandHelper plugin."
applyTo: "**/*.{ms,msa}"
---
## MethodScript
### Coding Style & Conventions

- **Procedure declaration** – Procedures use the keyword `proc` followed by a return type (`auto`, `boolean`, `string`, `array`). Example: `auto proc _get_cache_key(string @key)`.
- **Parameters & local variables** – Both are prefixed with `@`.  Internal helpers start with `_` (e.g. `_get_cache_value`).
- **Naming style** – Camel‑case for function and variable names; underscore prefixes denote internal helpers.
- **Control flow** – Explicit `if/foreach` blocks, no ternary operators. Loops written as `foreach (…) { … }`.
- **String handling** – Concatenation via `+` or the `@` syntax (e.g. `'&a🛠&7 Recompilation finished in&f' (@timestamp_end - @timestamp_begin).'ms&7.'`).
- **Error handling** – Errors thrown with `_throw_error()`; messages sent to players with `_send_error_to_player`.  Helper `_deny_command_alternative` shows localisation support.
- **Event registration** – Uses `_register_event('event_name', associative_array( … ))` with keys like `id`, `executor`, `condition`.
- **Global state** – Accessed via `import(@key)` and set with `_set_global_value`.  Keys normalised by `_normalise_id` and prefixed with the server namespace.
- **Threading** – New threads started with `x_new_thread('name', closure() { … })`; closures used for asynchronous work.
- **Array helpers** – Dedicated procedures (`_array_copy`, `_array_keys`, etc.) are defined and reused throughout.
