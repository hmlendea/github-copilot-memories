# Python Rules: Control Structures

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never use `++` or `--`; Python provides no increment or decrement operators, so use `+= 1` or `-= 1`.
- Never use non-existent operators (for example `=+`, `=-`, or `=not`); use the compound assignment operator (`+=`, `-=`) or separate a unary operator from `=` with a space.
- Never double the prefix operators `not` or `~`.
- Ensure every statement changes control flow or produces at least one side effect; string statements are not reported, and the operators `<<`, `>>`, and `|` are ignored.
- Never use `break`, `continue`, or `return` in `finally` blocks.
- Use `break` and `continue` only within loops.
- Use `yield` and `return` only within functions.
- Refactor loops that execute at most once.
- Delete code that can never execute (after `return`, `raise`, `break`, or `continue`).
- Correct conditions that are invariably true or invariably false, so that conditionally executed code can execute.
- Never use boolean expressions that invariably evaluate to an identical value; simplify or correct them.
- Never use identical expressions on both sides of a binary operator.
- Never repeat a condition in an `if`/`elif` chain.
- Never implement every branch of an `if` chain or conditional expression identically.
- Never implement two branches of an `if` chain identically; merge them. Single-line branches are exempt, except in chains without `else` where every branch is identical.
- Ensure every recursive function attains a base case; never recurse infinitely.
- Merge nested `if` statements without `else` into a single condition combined with `and`.
- Never invert boolean comparisons (`not first == second`); use the opposite operator (`first != second`).
- Delete unnecessary `pass` statements (in blocks containing other statements).
- Never use an `else` clause on a loop without `break`.
- Never nest conditional expressions (`value if condition else other`).
- Delete redundant jump statements (a final `return` without a value, or a final `continue` in a loop).
- Retain Cognitive Complexity of 15 or below per function.
- Never use constants as conditions in `if`, `elif`, conditional expressions, or boolean expressions.
- Never compare to `None` where the result is constant (the operand can never be, or is invariably, `None`).
- Never assign a variable to itself.
- Delete unused assignments; the values `-1`, `0`, `1`, `None`, `True`, `False`, and `""`, and unpacking, are exempt.
- Delete unused local variables; names corresponding to `(_[a-zA-Z0-9_]*|dummy|unused|ignored)` are exempt.
- Never use nested blocks containing only `pass`; implement them or include a comment explaining the reason.
- Define variables, classes, and functions prior to using them.
- Never use the walrus operator (`:=`) confusingly, for example unparenthesised at statement level or within f-strings.
