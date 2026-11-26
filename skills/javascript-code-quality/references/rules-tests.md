# JavaScript Rules: Tests

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never skip tests (`it.skip()`, `describe.skip()`, `xit()`) without stating the reason in an adjacent comment.
- Include at least one test case in every test file.
- Include at least one assertion in every test.
- Complete every assertion; never leave a Chai `expect()` or `should` chain without a concluding assertion.
- Pass the actual value first and the expected value second to assertion functions (`assert.equal(actual, expected)`).
- Never compare a value with itself in an assertion (`assert.equal(value, value)`).
- Specify the expected error type or message in assertions that expect an exception (`assert.throws(fn, TypeError)`, `expect(fn).to.throw(TypeError)`).
- Ensure tests are stable; never use `jest.retryTimes()` or Mocha retries (`this.retries()`).
- Execute no code in a test after calling `done()`.
- Deactivate Mocha timeouts explicitly with `this.timeout(0)`, never with values beyond 2,147,483,647 milliseconds.
- Ensure each Chai assertion succeeds for a single reason; never combine `.not` with `.throw()` arguments, `.include()` objects, multi-argument `.property()` or `.ownPropertyDescriptor()`, or `.members()`.
- Never commit exclusive tests (`describe.only()`, `it.only()`, `test.only()`).
