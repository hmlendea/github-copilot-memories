# C# Rules: Tests

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never mark a test `[Ignore]` without a reason (a trailing comment or a `[WorkItem]` attribute); repair, reactivate, or delete it.
- Ensure every test class (`[TestFixture]`, `[TestClass]`) contains at least one test method.
- Ensure every test contains at least one assertion, mock verification, or expected-exception check.
- Never assert boolean literals (for example `Assert.That(true, Is.True)`); assert the condition under test.
- Never call `Thread.Sleep` in tests; await the condition, use a synchronisation primitive, or use a fake clock.
- Complete every fluent assertion chain (FluentAssertions `Should()`, NFluent `Check.That()`, NSubstitute `Received()`) with an assertion or member call.
- Pass expected and observed values to assertions in the order the assertion library defines (for example, the observed value first in `Assert.That(actual, Is.EqualTo(expected))`).
- Never use `[ExpectedException]`; assert with `Assert.Throws`, `Assert.ThrowsAsync`, or an equivalent wrapping the specific call.
- Declare test methods `public`, non-generic (unless the test library supports it), and returning `void` or `Task`; never `async void`.
