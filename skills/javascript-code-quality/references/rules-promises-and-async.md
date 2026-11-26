# JavaScript Rules: Promises And Async

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Use `await` only with promises and thenables.
- Use `Promise.resolve()` and `Promise.reject()` rather than constructing a promise that immediately resolves or rejects.
- Never enclose unawaited promises in `try` blocks to catch their rejections; await the promise or use `.catch()`.
- Never misapply promises: never pass them where a boolean condition or a `void`-returning callback is expected, and never supply `async` functions as `Promise` executors.
- Reject promises only with `Error` objects, never literals.
- Never start asynchronous operations in constructors; use an asynchronous factory method.
- Never pass single-element arrays to `Promise.all()`, `Promise.any()`, or `Promise.race()`; await the promise directly.
- Never define a `then` property on objects, classes, or modules.
- Never use `Promise.resolve()` or `Promise.reject()` within `async` functions or promise callbacks; return the value or throw the error.
- Use top-level `await` rather than wrapping asynchronous operations in immediately invoked async functions or promise chains at module level.
