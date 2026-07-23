---
description: "Use when writing or editing C# tests, .csproj, or .slnx files. Covers project structure, testing preferences, naming conventions, member organisation, and unit tests."
applyTo: "**/*.{cs,csproj,slnx}"
---
## C#

- All C# coding instructions from `csharp.coding.instructions.md` apply to test code as well, unless explicitly overridden in this file.
- All test value instructions from `general.test-values.instructions.md` apply here as well, unless explicitly overridden in this file.

### Project Structure

- The unit test project, where applicable, must be named `[MainProjectName].UnitTests`.

### Naming Conventions

- Test classes: Subject + `Tests` (`AccountServiceTests`).

### Unit Tests

- NEVER add `<AssemblyAttribute Include="System.Runtime.CompilerServices.InternalsVisibleTo">` (or any other production code change) to a project just to enable unit test access. Do not modify the production project or its csproj solely for the sake of tests.
- Always write unit tests in the `Given[x]_When[y]_Then[z]` naming format.
- Use the existing unit‑testing framework of the project. If no testing framework is present, default to **NUnit 4.x** with **Moq**.
- Use `Assert.That(...)` with the NUnit constraint model exclusively. NEVER use `Assert.AreEqual`, `Assert.IsTrue`, `Assert.IsNotNull`, etc.
- Do not use `Assert.That(..., Is.True)`, just use `Assert.That(...)` directly.
- Never call `.Equals()` inside `Assert.That`. Use `Assert.That(actual, Is.EqualTo(expected))` and `Assert.That(actual, Is.Not.EqualTo(unexpected))` instead.
- Use `Is.Empty` instead of `Is.EqualTo(string.Empty)` in asserts.
- Use `Has.Length.EqualTo(n)` instead of asserting on `.Length` directly: `Assert.That(collection, Has.Length.EqualTo(n))`, never `Assert.That(collection.Length, Is.EqualTo(n))`.
- Annotate test classes with `[TestFixture]`, test methods with `[Test]` or `[TestCase(...)]`.
- When a test method contains only a single `Assert.That(...)` call (i.e. no Arrange or Act steps), use `=>` instead of a block body `{ ... }`. For multi‑argument `Assert.That` calls, place the expression on the next line with one extra level of indentation, and each argument on its own line. Example:
  ```csharp
  // Wrong:
  [Test]
  public void GivenX_WhenY_ThenZ()
  {
      string actual = subject.GetValue("input");
      Assert.That(actual, Is.EqualTo("expected"));
  }

  // Correct:
  [Test]
  public void GivenX_WhenY_ThenZ()
      => Assert.That(
          subject.GetValue("input"),
          Is.EqualTo("expected"));
  ```
- Use a `[SetUp]` method named `SetUp()` to construct mocks and the SUT.
- Declare mock fields and the SUT at class level as `private`.
- Group tests within a class by the production method under test. Do NOT use comment banners or any other separator between groups.
- Put private static `BuildXxx()` helper methods at the bottom of the test class for constructing test data.
