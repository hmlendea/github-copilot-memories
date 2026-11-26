# Java Rules: Logging And Diagnostics

One directive per Java rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never emit log messages to `System.out` or `System.err`; use a dedicated logger.
- Never evaluate logging or `Preconditions` arguments eagerly (concatenation, `String.format`, or method calls); use parameterised messages (`{}`) or a level guard.
- Create each logger with its enclosing class (for example `LoggerFactory.getLogger(Enclosing.class)`).
- Never place expressions with side effects within `assert` statements; assertions may be deactivated at runtime.
