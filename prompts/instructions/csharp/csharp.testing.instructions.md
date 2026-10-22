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
- Integration tests MUST only be written in a dedicated integration-test project, never in a production or unit-test project.
- The default integration-test project name is `[RootNamespace].IntegrationTests`.

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

### Architecture/Fitness Tests
- Fitness and architecture tests MUST live in a project named `<RootNamespace>.ArchitectureTests`.
- Fitness and architecture tests MUST use ArchUnit.NET and NUnit.
- Architecture/Fitness tests MUST NEVER be modified by the agent, even if they are failing, unless the user EXPLICITLY asks for it.
- Architecture tests MUST explicitly load all relevant production assemblies, exclude test assemblies, and reuse the loaded architecture for the test run.
- Every rule MUST select expected types; tests MUST fail when a selector matches none rather than pass vacuously.
- Tests MUST enforce the documented layer dependency matrix. Domain MUST NOT depend on Application, Infrastructure, or API; Application MUST NOT depend on Infrastructure or API; Infrastructure MUST NOT depend on API; and API MUST NOT reference Domain directly.
- Dependency rules MUST be checked independently at both levels: type dependencies in the loaded production assemblies and project/assembly references declared by the production projects. A passing type-dependency check MUST NOT substitute for the project/assembly-reference check.
- API boundary rules MUST verify that API code does not directly depend on Entity Framework, DynamoDB, or their persistence namespaces. API MUST NOT contain public repositories or command/query handlers; controllers, request/response contracts, and validation contracts MUST use the prescribed API namespaces; and controllers MUST NOT depend on repositories.
- Application boundary and placement rules MUST verify that Application does not depend on persistence implementations, DynamoDB, or Entity Framework, and does not expose controllers or middleware. Repository and service interfaces, commands, queries, and their handlers MUST be placed in their designated namespaces. Validators MUST be placed in the matching command or query use-case namespace.
- Domain boundary rules MUST verify that Domain does not depend on ASP.NET Core, Entity Framework, DynamoDB, Dapper, or MediatR. Domain types MUST NOT use persistence attributes. Public controllers, handlers, DTOs, validation contracts, commands, queries, and repositories MUST be prohibited in Domain.
- Tests MUST check cycles where components are defined as independent or acyclic. Do not assume layer names or impose a layered design beyond the documented matrix. Any permitted cycle MUST be documented and narrowly scoped.
- Enforce namespace placement, naming, and interface implementation conventions only when required by the documented architecture; do not duplicate generic style or analyser rules.
- Failure messages MUST identify the violated boundary and reason. Rule exceptions MUST be explicit and narrowly scoped.

### General/Test Constraints
- Constructors and methods MUST have no more than seven parameters.
- Business unit tests MUST contain an assertion, a Moq verification, or an `ExpectedResult`; architecture tests are exempt from this assertion requirement.

### Branch Coverage
- Use common testing guidance and the `test-design` skill for branches, erroneous/inconsistent, edge, and unexpected scenarios.
- Tests MUST comprehensively cover every stated requirement with a wide range of representative values, boundaries, exceptional inputs, and unexpected inputs.

### Structure
- Class `[TestFixture]`; methods `[Test]`/`[TestCase(...)]`. Group by production method, no comment banners.
- Private static `BuildXxx()` test-data helpers at class bottom. Helpers without instance state: `static`.
- Dummy custom implementations MUST be top-level `internal` classes in separate files, never private classes nested within public test classes. Apply all regular class rules to them.
- Cache `JsonSerializerOptions` in static readonly fields, never per call.

### Compatibility
- Tests are platform-safe: no hard-coded paths, locale-dependent formats, or OS-specific APIs; support Linux/Windows/macOS and x86/ARM.

### Integration Testing

- API integration tests cover all input/output success and failure scenarios, including applicable HTTP statuses (e.g. 400, 401, 404, 500).
- Use project integration framework; absent framework defaults to NUnit + FluentAssertions + Microsoft.AspNetCore.Mvc.Testing.
- Do not use xunit unless it was explicitly chosen as the project testing framework or already in use.
- Assert response body and status. Parameterise with `[InlineData]`/`[Theory]`; mock external dependencies for deterministic speed.
