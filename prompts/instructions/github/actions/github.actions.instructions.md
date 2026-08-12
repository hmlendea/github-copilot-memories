---
description: "Use when creating or revising GitHub Actions workflow files. Defines canonical workflow file names for specific delivery targets."
applyTo: ".github/workflows/*.{yml,yaml}"
---

## Workflow File Naming Standard

When creating or revising workflow files, use these canonical file names:

- .NET workflows: `dotnet.yml`
- Nexus Mods workflows: `nexus-mods.yml`
- Steam Workshop workflows: `steam-workshop.yml`
- Release asset upload workflows: `release-assets.yml`

Do not use alternative names for these workflow categories unless the user explicitly requests an exception.
