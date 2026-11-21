---
description: "Use when creating or revising the GitHub Release workflow for an Electron project. Provides the canonical template for github-release.yml."
applyTo: ".github/workflows/github-release.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/github-release-electron.yml` for `.github/workflows/github-release.yml`, and its rules `skills/github-actions-workflow/rules/github-release-electron.md`.

Use this template only for Electron projects that build release artefacts through `electron-builder`. Do not use it for NuGet packages. For a repository that hosts a NuGet package, use `instructions/github/actions/github.actions.workflows.nuget.github-release.instructions.md` instead. For a compilable .NET project that builds release assets, use `instructions/github/actions/github.actions.workflows.dotnet.github-release.instructions.md` instead. For an Android project that builds an APK release artefact through Gradle, use `instructions/github/actions/github.actions.workflows.android.github-release.instructions.md` instead.

The template must remain exactly as written, with only the placeholders replaced:

- `[[NODE_VERSION]]` must be replaced with the Node.js major version used in the repository (for example `20`), consistent with `.nvmrc`, the `engines` field, and the continuous-integration workflow.
- `[[RELEASE_ASSET_GLOB]]` must be replaced with the repository-relative glob of the release assets produced by `npm run build` (for example `dist/geforcenow-electron_*`). When several patterns are required, expand the placeholder into a YAML block scalar containing one pattern per line.

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.
