Generate or revise `.github/workflows/steam-workshop-release.yml` using `templates/steam-workshop-release.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `steam-workshop-release.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use an exact copy of `templates/steam-workshop-release.yml`; preserve the workflow `name`, triggers, job, steps, action versions, indentation, and whitespace layout.
2. The template must remain exactly as written, with only the placeholders replaced.
3. The `STEAM_USERNAME`, `STEAM_PASSWORD`, and `STEAM_2FA_SEED` secrets must be referenced as `${{secrets.STEAM_USERNAME}}`, `${{secrets.STEAM_PASSWORD}}`, and `${{secrets.STEAM_2FA_SEED}}` respectively; their values must never be exposed.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[GITHUB_REPO_USERNAME]]` | The GitHub repository owner. |
| `[[GITHUB_REPO_NAME]]` | The GitHub repository name. |
| `[[RELEASE_ASSET_LABEL]]` | The release asset label used by the corresponding `github-release.yml` assets. |
| `[[STEAM_APP_ID]]` | The Steam application identifier. |
| `[[STEAM_WORKSHOP_ITEM_ID]]` | The Steam Workshop item identifier. |

### Failure Behaviour

- If any Steam identifier remains indeterminate after evidence collection, cease generation and ask one concise clarification question. Never invent an identifier.

### Mandatory Validation Before Final Output

- The output file is named `steam-workshop-release.yml`.
- The workflow `name` is `Steam Workshop` and triggers on a `v*.*.*` tag push.
- The `release` job downloads and unzips the release asset and uploads through `hmlendea/steam-workshop-update@v1.0.0`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret value, credential, or personal datum is exposed.

If a `steam-workshop-release.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `steam-workshop-release.yml` exists, create one from scratch.
