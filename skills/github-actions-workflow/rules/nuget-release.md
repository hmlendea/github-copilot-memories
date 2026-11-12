Generate or revise `.github/workflows/nuget-release.yml` using `templates/nuget-release.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `nuget-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use an exact copy of `templates/nuget-release.yml`; preserve the workflow `name`, triggers, job, permissions, steps, action versions, indentation, and whitespace layout.
2. The template must remain exactly as written, with only this exception:
   - `[[NUGET_PACKAGE_NAME]]` is replaced with the NuGet package ID.
3. The repository must define the `NUGET_USER` secret with the NuGet.org account name associated with the package. NuGet trusted publishing must be configured for the repository so `NuGet/login` can exchange the GitHub Actions OIDC token for a temporary API key.
4. The `id-token: write` permission is required for the OIDC exchange and must remain.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[NUGET_PACKAGE_NAME]]` | The NuGet package ID. |

### Failure Behaviour

- If the NuGet package ID cannot be determined from evidence, cease generation and ask one concise clarification question. Never invent a package identifier.

### Mandatory Validation Before Final Output

- The output file is named `nuget-release.yml`.
- The workflow `name` is `NuGet.org Release` and triggers on published releases.
- The `publish` job grants `contents: read` and `id-token: write`, and runs on `ubuntu-latest`.
- The job restores, packs, logs in through `NuGet/login@v1` using `${{ secrets.NUGET_USER }}`, and pushes the package to `https://api.nuget.org/v3/index.json`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `nuget-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `nuget-release.yml` exists, create one from scratch.
