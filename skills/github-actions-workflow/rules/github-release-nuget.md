Generate or revise `.github/workflows/github-release.yml` using `templates/github-release-nuget.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `github-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use this template only for repositories that host a NuGet package. For a compilable .NET project that builds release assets, use `rules/github-release-dotnet.md` instead. For an Android project that builds an APK release artefact through Gradle, use `rules/github-release-android.md` instead.
2. Use an exact copy of `templates/github-release-nuget.yml`; preserve the workflow `name`, triggers, job, permissions, steps, action versions, indentation, and whitespace layout.
3. The template must remain exactly as written, with only this exception:
   - `[[NUGET_PACKAGE_NAME]]` is replaced with the NuGet package ID.
4. The `contents: write` permission is required to upload the package to the GitHub Release and must remain.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[NUGET_PACKAGE_NAME]]` | The NuGet package ID. |

### Failure Behaviour

- If the NuGet package ID cannot be determined from evidence, cease generation and ask one concise clarification question. Never invent a package identifier.

### Mandatory Validation Before Final Output

- The output file is named `github-release.yml`.
- The workflow `name` is `GitHub Release` and triggers on published releases.
- The `pack` job grants `contents: write` and runs on `ubuntu-latest`.
- The job restores, packs, computes the SHA256 checksum, uploads the package with `gh release upload`, and appends the checksum to the release notes through `actions/github-script@v7`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `github-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `github-release.yml` exists, create one from scratch.
