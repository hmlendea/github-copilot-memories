# MethodScript Function Reference: Persistence

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Allows scripts to store data from execution to execution. See the guide on persistence for more information. In all the functions, you may send multiple arguments for the key, which will automatically be concatenated with a period (the namespace separator). No magic happens here, you can put periods yourself, or combine manually namespaced values or automatically namespaced values with no side effects. All the functions in the Persistence API are threadsafe (though not necessarily process safe).

5 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `clear_value([namespace, ...,] key)` -> void (throws IOException; FormatException) [restricted] - Completely removes a value from storage. Calling has_value(key) after this call will return false.
- `get_value([namespace, ...,] key)` -> mixed (throws IOException; FormatException) [restricted] - Returns a stored value stored with store_value. If the key doesn't exist in storage, null is returned. On a more detailed note: If the value stored in the persistence database is not actually a constr...
- `get_values(name[, space, ...])` -> array (throws IOException; FormatException) [restricted] - Returns all the values in a particular namespace as an associative array(key: value, key: value). Only full namespace matches are considered, so if the key 'users.data.username.hi' existed in the data...
- `has_value([namespace, ...,] key)` -> boolean (throws IOException; FormatException) [restricted] - Returns whether or not there is data stored at the specified key in the Persistence database.
- `store_value([namespace, ...,] key, value)` -> void (throws FormatException; IOException; FormatException) [restricted] - Allows you to store a value, which can then be retrieved later. key must be a string containing only letters, numbers, underscores.
