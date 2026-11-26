# Kotlin Rules: Control Structures

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Merge collapsible nested `if` statements (neither with an `else` branch) into one with a combined condition; extract complex conditions into a named function or variable.
- Delete vacant nested blocks; blocks containing a comment and `while` loops with vacant bodies are exempt. **Local precedence:** The coding instructions require eliminating vacant conditionals; delete comment-only conditional blocks as well.
- Delete redundant boolean literals (`|| false`, `!false`, `if (condition) true else false`).
- Never implement two branches of an `if` chain or `when` identically; merge them, combining `when` conditions with commas.
- Never invert boolean comparisons (`!(count == limit)`); use the opposite operator (`count != limit`).
- Limit the Cognitive Complexity of each function to at most 15.
- Never place `return` in every branch of an `if`-`else` or exhaustive `when` statement; return the `if` or `when` expression instead.
- Replace `if`-`else if` chains of 3 or more branches with `when`.
- Limit `when` statements to at most 30 clauses.
- Delete `if (true)` and `if (false)` blocks; retain only the code that executes.
- Never assign a variable to itself.
- Delete unreachable code following `return`, `break`, `continue`, or `throw`.
- Never use identical expressions as both operands of a binary operator; `*`, `+`, and `=` are exempt.
- Never repeat a condition within one `if`-`else if` chain; the repeated branch never executes.
- Never apply a postfix increment or decrement whose effect is lost (`return count++`, `count = count++`).
- Never implement every branch of an `if` chain with a final `else`, or of a `when` with an `else` branch, identically.
- Never use non-existent operators (`=+`, `=-`, `=!`); use `+=`, `-=`, or `!=`, or separate the characters (`= -value`).
