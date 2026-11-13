# MethodScript Function Reference: ExtensionMeta

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides the ability for finding out information about installed extensions, including events and functions.

4 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `event_exists(name)` -> boolean - Returns true if the event is known to MethodScript. Like function_exists(), this function is resolved at compile time, and allows for conditional uses of events that may or may not exist.
- `extension_exists(name)` -> boolean - Returns true if the extension is known to MethodScript and loaded. Like function_exists(), this function is resolved at compile time.
- `extension_info([extensionName])` -> array - Returns extension info for the extensions the system has loaded, or the given extension if extensionName is specified.
- `function_exists(name)` -> boolean - Returns true if the function is known to MethodScript. This is a special function; it is resolved at compile time, and allows for conditional uses of functions that may or may not exist, such as funct...
