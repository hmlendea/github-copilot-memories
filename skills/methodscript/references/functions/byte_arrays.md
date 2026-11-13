# MethodScript Function Reference: ByteArrays

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

23 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `ba_as_array(byte_array)` -> array (throws CastException) - Returns a new read only copy of the underlying byte array. This array is much more efficient than if the array were made manually, however, it is read only.
- `ba_get_byte(byte_array, [pos])` -> int (throws CastException; RangeException) - Returns an int, read in as an 8 bit signed byte, from the given position, or wherever the marker is currently at by default.
- `ba_get_bytes(byte_array, length, [pos])` -> byte_array (throws CastException; RangeException) - Returns a new byte_array primitive containing 'length' bytes starting from pos (or wherever the marker is by default) in the given byte array.
- `ba_get_char(byte_array, [pos])` -> string (throws CastException; RangeException) - Returns a one character string, read in as an 32 bit char, from the given position, or wherever the marker is currently at by default.
- `ba_get_double(byte_array, [pos])` -> double (throws CastException; RangeException) - Returns a double, read in as a 64 bit double, from the given position, or wherever the marker is currently at by default.
- `ba_get_float(byte_array, [pos])` -> double (throws CastException; RangeException) - Returns a double, read in as a 32 bit float, from the given position, or wherever the marker is currently at by default.
- `ba_get_int(byte_array, [pos])` -> int (throws CastException; RangeException) - Returns an int, read in as a 32 bit signed int, from the given position, or wherever the marker is currently at by default.
- `ba_get_long(byte_array, [pos])` -> int (throws CastException; RangeException) - Returns an int, read in as a 64 bit signed long, from the given position, or wherever the marker is currently at by default.
- `ba_get_short(byte_array, [pos])` -> int (throws CastException; RangeException) - Returns an int, read in as a 16 bit signed short, from the given position, or wherever the marker is currently at by default.
- `ba_get_string(byte_array, [pos], [encoding])` -> string (throws CastException; RangeException) - Returns a UTF-8 encoded string, from the given position, or wherever the marker is currently at by default. The string is assumed to have encoded the length of the string with a 32 bit integer, then t...
- `ba_is_little_endian(byte_array)` -> boolean (throws CastException) - Returns true if this byte array is little endian. By default, byte arrays are big endian, but this may be changed with ba_set_little_endian.
- `ba_put_byte(byte_array, int, [pos])` -> void (throws CastException; RangeException) - Writes an int, interpreted as an 8 bit signed byte, starting from the given position, or wherever the marker is currently at by default.
- `ba_put_bytes(destination_byte_array, source_byte_array, [pos])` -> void (throws CastException) - Writes the contents of the source_byte_array into this byte array, starting at pos, or wherever the marker is currently at by default.
- `ba_put_char(byte_array, string, [pos])` -> void (throws CastException) - Writes the first character of the string, interpreted as an 32 bit char, starting from the given position, or wherever the marker is currently at by default.
- `ba_put_double(byte_array, double, [pos])` -> void (throws CastException) - Writes a double, interpreted as a 64 bit double, starting from the given position, or wherever the marker is currently at by default.
- `ba_put_float(byte_array, double, [pos])` -> void (throws CastException; RangeException) - Writes a double, interpreted as a 32 bit float, starting from the given position, or wherever the marker is currently at by default.
- `ba_put_int(byte_array, int, [pos])` -> void (throws CastException; RangeException) - Writes an int, interpreted as a 32 bit signed int, starting from the given position, or wherever the marker is currently at by default.
- `ba_put_long(byte_array, int, [pos])` -> void (throws CastException) - Writes an int, interpreted as a 64 bit signed long, starting from the given position, or wherever the marker is currently at by default.
- `ba_put_short(byte_array, int, [pos])` -> void (throws CastException; RangeException) - Writes an int, interpreted as an 16 bit signed short, starting from the given position, or wherever the marker is currently at by default.
- `ba_put_string(byte_array, string, [pos], [encoding])` -> void (throws CastException) - Writes the length of the string to the byte array, as a short, (interpreted as UTF-8), then writes the UTF-8 string itself.
- `ba_rewind(byte_array)` -> void (throws CastException) - Rewinds the byte array marker to 0.
- `ba_set_little_endian(byte_array, setLittleEndian)` -> void (throws CastException) - Sets the byte order that the specified byte array will use for all future gets/sets. By default, a byte array is Big Endian.
- `byte_array()` -> byte_array - Returns a new byte array primitive, which can be operated on with the ba_ series of functions.
