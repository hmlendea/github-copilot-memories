# MethodScript Function Reference: FileHandling

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

7 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `async_read(file, [encoding], callback)` -> void (throws SecurityException) [restricted] - Asynchronously reads in a file. See more...
- `comp_read(path, [encoding])` -> string [restricted] - Returns the value of a file at compile time only. Unlike read, this runs and is fully resolved at compile time. This is useful for optimization reasons, if you have a file that is unchanging, this can...
- `file_resolve(file)` -> string (throws IOException) [restricted] - Returns the canonical, absolute path of the given path. This provides a context independent and unique path which always points to the specified path, and removes any duplicate . or .. parts.
- `file_size(path)` -> int (throws IOException; SecurityException) [restricted] - Returns the size of a file on the file system.
- `read(file, [encoding])` -> string (throws IOException; SecurityException) [restricted] - Reads in a file from the file system at location var1 and returns it as a string. The path is relative to the file that is being run, not CommandHelper.
- `read_binary(file)` -> byte_array (throws IOException) [restricted] - Reads in a file, and returns a byte_array for it. The file is returned exactly as is on disk, no conversions are done. base-dir restrictions are enforced for the path, the same as read().
- `read_gzip_binary(file)` -> byte_array (throws IOException) [restricted] - Reads in a gzipped file, and returns a byte_array for it. The file is returned exactly as is on disk, no conversions are done other than unzipping it.
