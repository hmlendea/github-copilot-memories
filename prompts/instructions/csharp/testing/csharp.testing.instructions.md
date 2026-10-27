---
description: "Use for C# tests and test projects. Covers shared structure, naming, coverage, and compatibility."
applyTo: "**/*Tests.{cs,csproj},**/*.{Tests,ArchitectureTests,IntegrationTests,UnitTests}/*.cs,**/*.{Tests,ArchitectureTests,IntegrationTests,UnitTests}/**/*.cs"
---
## C#

### Naming Conventions
- Test classes: Subject + `Tests` (`AccountServiceTests`).

### Projects
- Never add `InternalsVisibleTo` or other production-project changes solely for tests.

### General/Test Constraints
- Constructors and methods MUST have no more than seven parameters.

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
