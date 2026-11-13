# MethodScript Function Reference: ResourceManager

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

2 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `res_create_resource(type, [data])` -> Resource (throws CastException; FormatException) [restricted] - Creates a new resource, which is stored in memory. Various functions require resources of certain types, which are created with this function.
- `res_free_resource(Resource)` -> void (throws CastException; NotFoundException) [restricted] - Frees the given resource. This should ALWAYS be called at some point after creating a resource with res_create_resource, once you are done with the resource.
