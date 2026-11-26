# JavaScript Rules: Platform APIs

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never use deprecated APIs; use their documented substitutes.
- Pass arguments of the documented types to native functions (`Math`, `String`, `Array`, and `Number` methods).
- Import only a package's public exports, never its internal modules (`./node_modules/foo/helpers`).
- Never include a request body in HTTP `GET` or `HEAD` requests (the `body` option of `fetch()`).
- Never import polyfills for functionality that all supported environments provide natively.
- Use `Blob` methods (`text()`, `arrayBuffer()`) rather than `FileReader`.
- Access `data-*` attributes via `dataset`, not `getAttribute()` or `setAttribute()`.
- Delete DOM nodes with `remove()`, not `parentNode.removeChild()`.
- Use `globalThis` rather than `window`, `self`, or `global`.
- Use modern DOM methods (`replaceWith()`, `before()`, `after()`, `append()`, `prepend()`) rather than `replaceChild()`, `insertBefore()`, `insertAdjacentText()`, and `insertAdjacentElement()`.
- Use `structuredClone()` for recursive cloning rather than `JSON.parse(JSON.stringify())` or library functions (`_.cloneDeep()`).
