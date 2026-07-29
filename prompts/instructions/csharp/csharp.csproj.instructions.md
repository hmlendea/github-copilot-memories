---
description: "Use when writing or editing C# .csproj, or .slnx files. Covers project structure, project configuration, solution structure, and solution configuration."
applyTo: "**/*.{csproj}"
---
## C#

### Projects
- Target .NET 10.0 or newer for all projects in a solution. Use `<TargetFramework>net10.0</TargetFramework>` in each `.csproj` file.
- All `csproj` files of any project must contain:
  - `<ImplicitUsings>disable</ImplicitUsings>`
  - `<LangVersion>latest</LangVersion>`
  - `<IsPackable>false</IsPackable>` unless the project is intended to be published as a NuGet package, in which case it should be `true`.
  - `<Nullable>enable</Nullable>`
