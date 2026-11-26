# JavaScript Rules: Members And Parameters

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Limit functions to 7 parameters.
- Never pass more arguments than a function declares; use rest parameters (`...args`) for variadic functions.
- Never leave functions vacant; include a comment explaining the reason or throw an error. Exempt: arrow functions, functions named `on…` or containing `noop`, and constructors.
- Read the initial value of every parameter, caught exception, and loop variable prior to reassigning it.
- Delete unused local variables and functions.
- Never define functions within loops; define them beyond the loop.
- Never duplicate parameter names within a function signature.
- Place parameters with default values after all parameters without defaults.
- Limit function nesting to 4 levels.
- Use the return value of every function without side effects (`concat()`, `trim()`, `toUpperCase()`, `map()`).
- Pass arguments in the order the parameters are declared when argument names correspond to parameter names.
- Never use boolean selector parameters to select between two code branches; divide the function into two functions.
- Never use `arguments.caller` or `arguments.callee`.
- Ensure functions with several `return` statements do not return an invariant value.
- Include at least one `yield` in every generator function.
- Never use the return value of a function that returns nothing.
- Return a single, consistent type from every function.
- Never implement two functions identically; have one invoke the other. Exempt: functions of fewer than 3 lines, and function and arrow expressions.
- Never call `.bind()` unnecessarily: on arrow functions or on functions that do not use `this`.
- Use spread syntax (`fn(...args)`) rather than `apply()`.
- Call functions directly rather than via redundant `.call()` or `.apply()` that pass the default `this`.
- Never call literals as functions.
- Move functions that capture no variables from their enclosing scope to the outermost possible scope.
- Never use object literals with properties as default parameter values; use destructured parameters with individual defaults (`{ size = 1 } = {}`).
- Never use immediately invoked arrow functions whose body is a parenthesised expression; assign the intermediate value to a variable.
- Use default parameters rather than reassigning parameters with literal fallback values (`value = value || 'default'`).
- Pass native conversion functions directly (`array.map(String)`, `array.filter(Boolean)`) rather than wrapping them (`value => String(value)`).
