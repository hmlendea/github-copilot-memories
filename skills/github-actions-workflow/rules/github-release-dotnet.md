Generate or revise `.github/workflows/github-release.yml` using `templates/github-release-dotnet.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `github-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use this template only for compilable .NET projects, that is, projects that build to release assets. Do not use it for NuGet packages. For a repository that hosts a NuGet package, use `rules/github-release-nuget.md` instead.
2. Use an exact copy of `templates/github-release-dotnet.yml`; preserve the workflow `name`, triggers, permissions, job, steps, action versions, indentation, and whitespace layout.
3. The template must remain exactly as written, with only the placeholders replaced.
4. The `contents: write` permission is required to publish release assets and must remain.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[DOTNET_PROJECT_PATH]]` | The repository-relative path of the primary project file whose `TargetFramework` determines the .NET version (for example `NuciCraft.API/NuciCraft.API.csproj`). |
| `[[RELEASE_ASSET_GLOB]]` | The repository-relative glob of the release assets produced by the release script (for example `NuciCraft.API/bin/Release/nucicraft-api_*`). |

### Failure Behaviour

- If the primary project path or release asset glob cannot be determined from evidence, cease generation and ask one concise clarification question. Never invent a path or glob.

### Mandatory Validation Before Final Output

- The output file is named `github-release.yml`.
- The workflow `name` is `GitHub Release` and triggers on published releases.
- Top-level `permissions` sets `contents: write`.
- The `release` job determines the .NET version from `[[DOTNET_PROJECT_PATH]]`, builds the release artefacts through the shared release script, and publishes `[[RELEASE_ASSET_GLOB]]` with `softprops/action-gh-release@v2`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `github-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `github-release.yml` exists, create one from scratch.
