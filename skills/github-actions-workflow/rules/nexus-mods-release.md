Generate or revise `.github/workflows/nexus-mods-release.yml` using `templates/nexus-mods-release.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `nexus-mods-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use an exact copy of `templates/nexus-mods-release.yml`; preserve the workflow `name`, triggers, job, steps, action versions, indentation, and whitespace layout.
2. The template must remain exactly as written, with only the placeholders replaced.
3. The `NEXUSMODS_API_KEY` secret must be referenced as `${{ secrets.NEXUSMODS_API_KEY }}` and its value must never be exposed.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[RELEASE_ASSET_LABEL]]` | The release asset label used by the corresponding `github-release.yml` assets. |
| `[[GITHUB_REPO_USERNAME]]` | The GitHub repository owner. |
| `[[GITHUB_REPO_NAME]]` | The GitHub repository name. |
| `[[NEXUSMODS_FILE_ID]]` | The Nexus Mods file identifier for the mod. |

### Failure Behaviour

- If a mandatory Nexus Mods identifier remains indeterminate after evidence collection, cease generation and ask one concise clarification question. Never invent an identifier.

### Mandatory Validation Before Final Output

- The output file is named `nexus-mods-release.yml`.
- The workflow `name` is `Nexus Mods`.
- Triggers are a `v*.*.*` tag push and a manual `workflow_dispatch` with a required `tag` input.
- The `release` job downloads the release asset and uploads through `Nexus-Mods/upload-action@v1.0.0-beta.10`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `nexus-mods-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `nexus-mods-release.yml` exists, create one from scratch.
