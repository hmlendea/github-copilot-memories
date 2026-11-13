# MethodScript Function Reference: Debug

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides methods for viewing data about both CommandHelper and the other plugins in your server. Though not meant to be called by normal scripts, these methods are available everywhere other methods are available. Note that for some of these functions to even work, play-dirty mode must set to on. These are most useful in conjunction with interpreter mode.

6 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `always_trace(ivar)` -> void (throws CastException) [restricted] - Outputs debug information about a variable to standard out. Unlike debug, this only accepts an ivar; it is a meta function.
- `debug(message)` -> void (throws IOException) [restricted] - Manually logs a timestamped message to the debug log and the console, if debug-mode is set to true in the preferences
- `dump_threads()` -> array [restricted] - Returns an array of all thread names that are currently running in the JVM. This is a debugging tool for your server, and less of a CommandHelper specific thing.
- `heap_dump()` -> void (throws PluginInternalException) [restricted] - Creates a heap dump file, and places it in the working directory, as "dump.hprof". This might throw a PluginInternalException if the heap dump tools aren't available in your JVM.
- `set_debug_output(booleanValue)` -> void [restricted] - Turns verbose debug output on or off. This should generally never be on in a production server, but can be useful to quickly trace what a script is doing when it runs in a test environment.
- `trace(ivar)` -> void (throws CastException) [restricted] - Works like always_trace, but only if debug-mode is enabled in the preferences. See always_trace for details of the output.
