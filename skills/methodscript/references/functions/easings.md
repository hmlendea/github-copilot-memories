# MethodScript Function Reference: Easings

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

Easing related functions. Easings are based on the easings listed at http://easings.net, with the addition of the LINEAR easing, which just returns x.

2 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `ease_between_loc(array start, array finish, EasingType type, double x)` -> array (throws CastException) - Given an easing type, and a duration percentage x, returns the given resulting interpolated distance. See more...
- `easing(EasingType type, double x)` -> double (throws CastException) - Given an easing type, and a duration percentage x, returns the given resulting interpolation value. See more...
