# MethodScript Function Reference: SQL

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

3 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `query(profile, query, [parameters...])` -> mixed (throws SQLException) [restricted] - Executes an SQL query, and returns various data depending on the query type. See the extended information for more details. See more...
- `query_async(profile, query, [params...], callback)` -> void (throws CastException) [restricted] - Asynchronously makes a query to an SQL server. The profile, query, and params arguments work the same as query, so see the documentation of that function for details about those parameters.
- `unsafe_query(profile, query, [parameters...])` -> mixed (throws SQLException) [restricted] - Executes a query, just like the query function, however, no validation is done to ensure that SQL injections might occur (essentially allowing for concatenation directly in the query).
