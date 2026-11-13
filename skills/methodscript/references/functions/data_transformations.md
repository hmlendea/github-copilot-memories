# MethodScript Function Reference: DataTransformations

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

8 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `ini_decode(string)` -> array (throws FormatException) - Returns an array, given an INI format input. INI files are loosely defined as a set of key->value pairs, which lends itself to an associative array format.
- `ini_encode(array, [comment])` -> string (throws FormatException; CastException) - Encodes an array into an INI format output. An associative array is expected, and a format exception is thrown if it is a normal array.
- `json_decode(string)` -> array (throws FormatException) - Takes a JSON encoded string, and returns an array, either normal or associative, depending on the contents of the JSON string. If the JSON string is improperly formatted, a FormatException is thrown.
- `json_encode(array)` -> string (throws CastException) - Converts an array into a JSON encoded string. Both normal and associative arrays are supported. Within the array, only primitives and arrays can be encoded.
- `parse_text_table(string table, [array options])` -> array (throws FormatException; CastException) - Parses tabular data into an array See more...
- `xml_read(xml, xpath)` -> mixed (throws FormatException) - Reads a field from some xml using an XPath address. The XPath address is assumed to be absolute, even if it doesn't start with a '/'.
- `yml_decode(string)` -> array (throws FormatException; PluginInternalException) - Takes a YML encoded string, and returns an associative array, depending on the contents of the YML string. If the YML string is improperly formatted, a FormatException is thrown.
- `yml_encode(array, [prettyPrint])` -> string (throws CastException) - Converts an array into a YML encoded string. Only associative arrays are supported. prettyPrint defaults to false. Within the array, only primitives and arrays can be encoded.
