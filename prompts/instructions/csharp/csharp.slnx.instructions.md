---
description: "Use when writing or editing C# .sln, or .slnx files. Covers solution structure, and solution configuration."
applyTo: "**/*.{sln,slnx}"
---
## C#

### Solution Files

- Always prefer `.slnx` over `.sln` solution files.
- When creating a new C# solution, place the `.slnx` file and all project directories at the repository root level (no `src/` subfolder or similar).
- The unit test project, where applicable, must be named `[MainProjectName].UnitTests`.
