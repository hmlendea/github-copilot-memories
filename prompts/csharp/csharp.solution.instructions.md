---
description: "Use when writing or editing C# .csproj, or .slnx files. Covers project structure, project configuration, solution structure, and solution configuration."
applyTo: "**/*.{csproj,slnx}"
---
## C#

### Project Structure

- Always target the latest stable .NET version available.
- NEVER use `ImplicitUsings` or implicit namespaces. Always use explicit `using` directives. Never add `<ImplicitUsings>enable</ImplicitUsings>` to any csproj.
- Never use top-level statements or free-floating code in any file. Every file must have an explicit `namespace { }` block, a `class` (or other type) block, and all code placed inside methods, constructors, or other members. This applies to `Program.cs` too; use an explicit `Program` class with a `static void Main` entry point.
- Every type must be declared in its own file — one type per file, without exception. File name must exactly match the type name. If a file contains multiple type definitions, extract each additional type into its own file immediately.

### Solution

- Always prefer `.slnx` over `.sln` solution files.
- When creating a new C# solution, place the `.slnx` file and all project directories at the repository root level (no `src/` subfolder or similar). The unit test project, where applicable, must be named `[ProjectName].UnitTests`.