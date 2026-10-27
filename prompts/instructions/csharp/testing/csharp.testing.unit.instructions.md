---
description: "Use for C# unit tests and unit-test projects. Covers naming, NUnit, Moq, assertions, setup, and configuration exclusions."
applyTo: "**/*.{Tests,UnitTests}.csproj,**/*.{Tests,UnitTests}/**/*.cs"
---
## C#

### Naming Conventions
- Unit tests: `Given[x]_When[y]_Then[z]`, fluent/grammatical with gerund `When` (e.g. `GivenANonExistentUser_WhenLoggingIn_ThenAnAuthenticationExceptionIsThrown`).

### Unit Tests
- Use project framework; absent framework defaults to NUnit 4.x + Moq.
- Do not use xunit unless it was explicitly chosen as the project testing framework or already in use.
- Prefer parameterised unit tests with `[TestCase(...)]`; when parameterised, include at least two test cases. This is not mandatory when parameterisation is not practical.
- Unit tests MUST neither require `InternalsVisibleTo` in the source project nor use reflection to directly test non-public code.
- NUnit: `Assert.That(...)` constraint model only; never `Assert.AreEqual`, `Assert.IsTrue`, or `Assert.IsNotNull`.
- Use `Assert.That(...)`, not `Assert.That(..., Is.True)`; compare with `Is.EqualTo`/`Is.Not.EqualTo`, never `.Equals()`.
- Use `Is.Empty`, not `Is.EqualTo(string.Empty)`; use `Has.Length.EqualTo(n)`, not direct `.Length` assertion.
- Single-assert test without Arrange/Act: expression-bodied. Multi-argument assert: next line plus one indent, one argument per line. Example:
  ```csharp
  [Test]
  public void GivenX_WhenY_ThenZ()
      => Assert.That(
          subject.GetValue("input"),
          Is.EqualTo("expected"));
  ```
- `[SetUp] SetUp()` constructs mocks/SUT; mock/SUT fields are class-level `private`.
- Configuration values: integration tests or runtime checks, never unit tests.
- Business unit tests MUST contain an assertion, a Moq verification, or an `ExpectedResult`.