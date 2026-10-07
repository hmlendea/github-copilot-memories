---
description: "Use for .sln or .slnx edits. Covers solution structure and configuration."
applyTo: "**/*.{sln,slnx}"
---
## C#

### Solution Files

- Always prefer `.slnx` over `.sln` solution files.
- The `.slnx` file must be **SDK-style**.

### Projects - Code
- All projects must be placed in a subfolder named after the project, at the same level as the `.slnx` file.
- Do not create a `src/` subfolder or similar for the projects.
- Project order in the `.slnx`:
  1. Main project first
  2. Other source projects alphabetically
  3. Test projects alphabetically

### Projects - Tests
- The unit test project, where applicable, must be named `[MainProjectName].UnitTests`.
- The `csproj` file of any test project must contain `<IsTestProject>true</IsTestProject>` and `<ExcludeFromCodeCoverage>true</ExcludeFromCodeCoverage>`.
