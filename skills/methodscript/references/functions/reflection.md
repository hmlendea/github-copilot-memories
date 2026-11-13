# MethodScript Function Reference: Reflection

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

10 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `class_type(string name)` -> ClassType (throws CastException; NotFoundException) [restricted] - Returns a ClassType object for the given fully qualified class name. If the given class doesn't exist, a NotFoundException is thrown.
- `get_aliases()` -> array [restricted] - Returns an array of the defined alias signatures (The part left of the = sign).
- `get_classes()` -> array [restricted] - Returns a list of all known classes. This may not be completely exhaustive, but will at least contain all system defined classes. The returned value is an array of ClassType objects.
- `get_events()` -> array [restricted] - Returns an array of all registered event names.
- `get_functions()` -> array [restricted] - Returns an associative array of all loaded functions. The keys of this array are the names of the classes containing the functions (which you know as the sections of the API page), and the values are...
- `get_procedures()` -> array [restricted] - Returns an array of procedures callable in the current scope.
- `reflect_docs(/ element, docField)` -> string (throws FormatException) [restricted] - Returns the documentation for an element. There are 4 things that an element might have, and one of these should be passed as the docField argument: type, return, args, description.
- `reflect_pull(param, [args, ...])` -> mixed (throws FormatException; IOException) [restricted] - Returns information about the runtime in a usable format. Depending on the information returned, it may be usable directly, or it may be more of a referential format. See more...
- `reflect_type(type)` -> array (throws CastException) [restricted] - Returns information about the given ClassType. See more...
- `reflect_value_source(persistenceKey)` -> string [restricted] - Returns the source file that this key will store a value to in the Persistence Network. For instance, in your persistence.ini file, if you have the entry "storage.test.**=json:///path/to/file.json", t...
