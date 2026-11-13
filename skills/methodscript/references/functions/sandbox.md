# MethodScript Function Reference: Sandbox

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

5 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `srand(Resource)` -> double (throws CastException) - Returns a new rand value using the provided a RANDOM Resource. If the seed used to create the resource is the same, each resulting series of numbers will be the same.
- `super_cancel()` -> void (throws BindException) [restricted] - "Super Cancels" an event. This only will work if play-dirty is set to true. If an event is super cancelled, not only is the cancelled flag set to true, the event stops propagating down, so no other pl...
- `test_composite_function(a, b)` -> boolean (throws CastException) - This is a test function, which demonstrates to extension authors how to make a composite function. It returns true if a and b added together are greater than 0, false otherwise.
- `x_recompile_includes(path)` -> int (throws IOException; IncludeException) [restricted] - Recompiles specified files already compiled with include(). If there's no compile errors, scripts that then include() these files will use the updated code.
- `x_write(path, content, [mode])` -> void (throws SecurityException; IOException) [restricted] - Writes a file to the file system. This method only works from the cmdline, if not in cmdline, a SecurityException is thrown. Because of this, there is no check against the base-dir path. See more...
