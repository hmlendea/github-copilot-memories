# JavaScript Rules: Exceptions And Errors

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never use jump statements (`return`, `break`, `continue`, `throw`) in `finally` blocks.
- Never ignore caught exceptions; address, log, or rethrow each one.
- Delete `catch` clauses that only rethrow the caught error.
- Throw only `Error` objects, never literals.
- Never construct an `Error` without throwing it.
- Name the error parameter `error`, or a descriptive name concluding with `Error` (`fsError`), in `catch` clauses, `.catch()` callbacks, and the second argument of `.then()`.
- Construct every native error with a descriptive message (`new Error('…')`, `new TypeError('…')`).
- Throw `TypeError`, not a generic `Error`, when a type check (`typeof`, `instanceof`, `Array.isArray()`) excludes a value.
