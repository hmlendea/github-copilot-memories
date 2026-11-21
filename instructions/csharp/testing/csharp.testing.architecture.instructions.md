---
description: "Use for C# architecture and fitness tests. Obligates the `csharp-architecture-testing` skill, which holds the ArchUnit.NET dependency rules, the Roslyn source and semantic convention checks, the project and solution policies, and the C# instruction enforcement catalogue."
applyTo: "**/*.ArchitectureTests.csproj,**/*.ArchitectureTests/**/*.cs"
---

## Mandatory Skill

Every C# architecture or fitness test is governed by the `csharp-architecture-testing` skill. Invoking that skill is mandatory, not optional: read `skills/csharp-architecture-testing/SKILL.md` before creating, revising, or reviewing any architecture or fitness test, and apply it in full.

The skill holds the project placement and framework rules, the layer dependency matrix, the boundary and placement rules, the source-file convention rules, the enforcement scope and mechanisms, the per-instruction enforcement catalogue, and the project and solution conventions. Never modify an architecture test unless the user explicitly requests it.
