---
description: "Use when writing or editing MethodScript code for Minecraft Spigot's CommandHelper plugin."
applyTo: "**/*.{ms,msa}"
---
## MethodScript

### Style Rules and Conventions

#### Syntax and Formatting

- **Procedure declaration** - Declare procedures with `proc` and an explicit return type (`auto`, `boolean`, `string`, `array`).
- **Control flow style** - Use explicit `if` and `foreach` blocks; avoid ternary operators.
- **Concatenation style** - Prefer explicit `.` concatenation and avoid relying on autoconcatenation.
- **Quote safety** - Quote command fragments that include special symbols (for instance `-`) to prevent parse ambiguity.
- **Multiline layout** - For non-trivial aliases, use `>>>` and `<<<` and keep one clear action per line.
- **Macro style** - Avoid long backslash-separated macros; prefer multiline MethodScript blocks for readability.

#### Naming and Variables

- **Local variable prefix** - Prefix local and procedure variables with `@`.
- **Alias variable prefix** - Use `$var` placeholders in alias signatures and keep names descriptive.
- **Internal helper naming** - Prefix internal helper procedures with `_`.
- **Optional defaults** - Use `[$var=default]` for optional parameters, with static literal defaults only.
- **Final variable usage** - Use `$` as the final variable when trailing free-form input must be captured.

#### Comments and Documentation

- **Line comments** - Prefer `//` for single-line comments; reserve `#` primarily for hashbang usage.
- **Block comments** - Use `/* ... */` for multi-line explanatory notes.
- **Smart comments** - Use `/** ... */` for alias and procedure documentation.
- **Command annotations** - For command-style aliases, document `@command`, `@usage`, `@permission`, `@param`, and optional tab completer metadata in smart comments.

#### Project and File Organisation

- **Execution unit awareness** - Design with separate execution units in mind (`main.ms`, aliases, event handlers, scheduled callbacks).
- **File role separation** - Keep startup registration in `main.ms`, shared procedures in `auto_include.ms`, and command aliases in `aliases.msa`.
- **Alias implementation style** - Prefer explicit `run('...');` on alias right-hand sides, including simple forwarding aliases.
- **Signature clarity** - Avoid ambiguous alias signatures that could match the same input path.

#### Maintenance Conventions

- **Encoding** - Save `.ms` and `.msa` sources as UTF-8 (BOM optional).