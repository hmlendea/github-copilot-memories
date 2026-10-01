---
description: "Use for C# tests and test projects. Covers structure, naming, framework, mocks, and assertions."
applyTo: "**/*Tests.{cs,csproj},**/*.{Tests,IntegrationTests,UnitTests}/*.cs,**/*.{Tests,IntegrationTests,UnitTests}/**/*.cs"
---
## C#

### Naming Conventions
- Test classes: Subject + `Tests` (`AccountServiceTests`).
- Unit tests: `Given[x]_When[y]_Then[z]`, fluent/grammatical with gerund `When` (e.g. `GivenANonExistentUser_WhenLoggingIn_ThenAnAuthenticationExceptionIsThrown`).

### Projects
- Never add `InternalsVisibleTo` or other production-project changes solely for tests.

### Unit Tests
- Use project framework; absent framework defaults to NUnit 4.x + Moq.
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

### Branch Coverage
- Use common testing guidance and the `test-design` skill for branches, erroneous/inconsistent, edge, and unexpected scenarios.

### Structure
- Class `[TestFixture]`; methods `[Test]`/`[TestCase(...)]`. Group by production method, no comment banners.
- Private static `BuildXxx()` test-data helpers at class bottom. Helpers without instance state: `static`.
- Cache `JsonSerializerOptions` in static readonly fields, never per call.

### Compatibility
- Tests are platform-safe: no hard-coded paths, locale-dependent formats, or OS-specific APIs; support Linux/Windows/macOS and x86/ARM.

### Integration Testing

- API integration tests cover all input/output success and failure scenarios, including applicable HTTP statuses (e.g. 400, 401, 404, 500).
- Use project integration framework; absent framework defaults to NUnit + FluentAssertions + Microsoft.AspNetCore.Mvc.Testing.
- Assert response body and status. Parameterise with `[InlineData]`/`[Theory]`; mock external dependencies for deterministic speed.
