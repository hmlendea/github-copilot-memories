---
description: "Use when creating or revising GitHub Actions workflow files. Defines canonical workflow file names for specific delivery targets."
applyTo: ".github/workflows/*.{yml,yaml}"
---

## Workflow File Naming Standard

When creating or revising workflow files, use these canonical file names:

- .NET Security workflows: `security.yml`
- .NET workflows: `dotnet.yml`
- Bash workflows: `bash.yml`
- GitHub Release workflows: `github-release.yml`
- Nexus Mods workflows: `nexus-mods.yml`
- NuGet.org release workflows: `nuget-release.yml`
- Release asset upload workflows: `release-assets.yml`
- Steam Workshop workflows: `steam-workshop.yml`

Do not use alternative names for these workflow categories unless the user explicitly requests an exception.
