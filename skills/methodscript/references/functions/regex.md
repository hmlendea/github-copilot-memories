# MethodScript Function Reference: Regex

Extracted from the official MethodScript 3.3.5 API documentation (`https://methodscript.com/docs/3.3.5/API.html`), retrieved 13 November 2026. Confirm behaviour against the upstream page before relying on any single entry.

6 functions.

Each entry shows the signature, the return type, the exceptions thrown, and `[restricted]` when the function requires CommandHelper permission to run, followed by a behaviour summary. Optional arguments appear in square brackets; ` / ` separates alternative overloads.

- `reg_count(pattern, subject)` -> int (throws FormatException) - Counts the number of occurrences in the subject.
- `reg_escape(arg)` -> string - Escapes arg so that it may be used directly in a regular expression, without fear that it will have special meaning; that is, it escapes all special characters.
- `reg_match(pattern, subject)` -> array (throws FormatException) - Searches for the given pattern, and returns an array with the results. Captures are supported. If the pattern is not found anywhere in the subject, an empty array is returned.
- `reg_match_all(pattern, subject)` -> array (throws FormatException) - Searches subject for all matches to the regular expression given in pattern, unlike reg_match, which just returns the first match.
- `reg_replace(pattern, replacement, subject)` -> string (throws FormatException; CastException) - Replaces any occurrences of pattern with the replacement in subject. Back references are allowed. 'replacement' can be a string, or a closure that accepts a found occurrence of 'pattern' and returns t...
- `reg_split(pattern, subject, [limit])` -> array (throws FormatException; CastException) - Splits a string on the given regex, and returns an array of the parts. If nothing matched, an array with one element, namely the original subject, is returned.
