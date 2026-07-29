---
description: "Use when writing or editing C# .sln, or .slnx files. Covers solution structure, and solution configuration."
applyTo: "**/*.{sln,slnx}"
---
## C#

### Solution Files

- Always prefer `.slnx` over `.sln` solution files.

### Projects - Code
- All projects must be placed in a subfolder named after the project, at the same level as the `.slnx` file.
- Do not create a `src/` subfolder or similar for the projects.

### Projects - Tests
- The unit test project, where applicable, must be named `[MainProjectName].UnitTests`.
- The `csproj` file of any test project must contain `<IsTestProject>true</IsTestProject>` and `<ExcludeFromCodeCoverage>true</ExcludeFromCodeCoverage>`.
