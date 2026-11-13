# MethodScript Function Reference: Compiler

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Compiler internal functions should be declared here. If you're reading this from anywhere but the source code, there's a bug, because these functions shouldn't be public or used in a script.

2 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `__smart_string__(string)` -> none - This is a compiler construct, and is not normally used directly. It is created via double quoted strings.
- `__unsafe_assign__([type], ivar, mixed)` -> ivariable (throws CastException) - Accepts an ivariable ivar as a parameter, and puts the specified value mixed in it. Returns the variable that was assigned. Operator syntax is also supported: <code>@a = 5;</code>.
