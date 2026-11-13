# MethodScript Function Reference: Web

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Contains various methods to make HTTP requests.

5 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `email([profile], options)` -> void (throws FormatException; PluginInternalException; IOException) [restricted] - Sends an email. See the extended description for more information. See more...
- `http_clear_session_cookies(cookieJar)` -> void (throws CastException) - Clears out "session" cookies, that is cookies that weren't set with an expiration (which translates to 0 in an individual cookie).
- `http_request(url, callback / url, settings)` -> void (throws FormatException) [restricted] - Makes an HTTP request to the given url. See more...
- `url_decode(param)` -> string - Decodes a previously url encoded string.
- `url_encode(param)` -> string - URL Encodes the parameter given. This escapes all special characters per the x-www-form-urlencoded format.
