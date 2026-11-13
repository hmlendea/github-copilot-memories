# MethodScript Function Reference: Crypto

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Provides common cryptographic functions. Many functions in this class are aware of and compatible with secure_string (where specified in the function documentation). In these cases, if the argument passed in is a secure_string, it is first decrypted and the underlying string is used rather than the default string value "**secure string**".

12 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `base64_decode(base64data)` -> byte_array (throws CastException) - Decodes the base 64 encoded byte_array data back into the original byte_array data.
- `base64_encode(byteData)` -> byte_array (throws CastException) - Encodes the given byte_array data into a base 64 byte_array.
- `bcrypt(val, [workload])` -> string (throws CastException; RangeException) - Encrypts a value using bcrypt, using the specified workload, or 5 if none provided. BCrypt is supposedly more secure than SHA1, and certainly more secure than md5.
- `check_bcrypt(plaintext, hash)` -> boolean - Checks to see if this plaintext password does in fact hash to the hash specified. Unlike md5 or sha1, simply comparing hashes won't work. This function is aware of and compatible with secure_string.
- `hmac_md5(key, val)` -> string (throws PluginInternalException) - Returns the md5 HMAC of the specified value using the provided key. If the key or value is not a byte array, it will be converted to a byte array through its UTF-8 string representation.
- `hmac_sha1(key, val)` -> string (throws PluginInternalException) - Returns the sha1 HMAC of the specified value using the provided key. If the key or value is not a byte array, it will be converted to a byte array through its UTF-8 string representation.
- `hmac_sha256(key, val)` -> string (throws PluginInternalException) - Returns the sha256 HMAC of the specified value using the provided key. If the key or value is not a byte array, it will be converted to a byte array through its UTF-8 string representation.
- `md5(val)` -> string (throws PluginInternalException) - Returns the md5 hash of the specified string or byte array. The md5 hash is no longer considered secure, so you should not use it for storage of sensitive data, however for general hashing, it is a qu...
- `rot13(val)` -> string - Returns the rot13 version of val. Note that rot13(rot13(val)) returns val
- `sha1(val)` -> string (throws PluginInternalException) - Returns the sha1 hash of the specified string or byte array. Note that sha1 is considered no more secure than md5, and should not be used in a security context.
- `sha256(val)` -> string (throws PluginInternalException) - Returns the sha256 hash of the specified string or byte array. Note that sha256 is considered more secure than sha1 and md5, and is typically used when storing sensitive data.
- `sha512(val)` -> string (throws PluginInternalException) - Returns the sha512 hash of the specified string or byte array. Note that sha512 is considered more secure than sha1 and md5 (and sha256, because it takes longer to calculate), and is typically used wh...
