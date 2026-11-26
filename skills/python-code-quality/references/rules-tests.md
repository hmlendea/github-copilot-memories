# Python Rules: Tests

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Provide a reason when skipping a test (`@unittest.skip('reason')` or `pytest.mark.skip(reason=...)`).
- Name test methods in test case classes with the `test_` prefix so they are discoverable, unless the class uses them internally.
- Use the most specific `unittest` assertion (`assertIsNone(value)` rather than `assertTrue(value is None)`).
- Never use assertions whose result is constant regardless of the code under test.
- Never place assertions after the statement expected to raise within `pytest.raises` or `assertRaises` blocks; they never execute.
- Skip tests explicitly with `self.skipTest()` or `pytest.skip()`, never with a conditional `return` at the start of the test.
- Never assert equality between values of incompatible types.
- Never call `assert` on a tuple literal (`assert (condition, message)`); use `assert condition, message`.
