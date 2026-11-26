# Kotlin Rules: Naming And Layout

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Name functions per `^[a-zA-Z][a-zA-Z0-9]*$`. **Local precedence:** The naming instructions additionally prohibit abbreviations and single-letter names; apply both.
- Name classes per `^[A-Z][a-zA-Z0-9]*$` (Pascal case). **Local precedence:** The naming instructions additionally prohibit abbreviations and single-letter names; apply both.
- Name local variables and function parameters per ``^`?[_a-z][a-zA-Z0-9]*`?$`` (camel case, optionally enclosed in backticks or prefixed with `_`). **Local precedence:** The naming instructions additionally prohibit abbreviations and single-letter names, including loop and lambda variables; apply both.
- Delete redundant pairs of parentheses.
- Delete unnecessary imports (unused or duplicated); imports referenced in KDoc are exempt.
- Resolve every `FIXME` comment and delete it once resolved.
- Resolve every `TODO` comment and delete it once complete; format any interim one as `// TODO: Description.`
- Delete commented-out code.
- Delete vacant multi-line comments (`/* */`).
- Never declare a lambda parameter explicitly as `it` (`{ it -> ... }`). **Local precedence:** The naming instructions require clear, explicit lambda parameter names; declare a descriptive one (for example `{ item -> ... }`) instead of relying upon the implicit `it`.
