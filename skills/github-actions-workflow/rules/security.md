Generate or revise `.github/workflows/security.yml` using `templates/security.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `security.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use an exact copy of `templates/security.yml`; preserve the workflow `name`, triggers, job, permissions, steps, action versions, indentation, and whitespace layout.
2. The template must remain exactly as written, with only this exception:
   - `[[DOTNET_VERSION]]` is replaced with the actual .NET version used in the repository.
3. The `security-events` permission must be `write`. The CodeQL `analyze` action uploads SARIF results to GitHub Code Scanning, and that upload requires the `security-events: write` scope. With `security-events: read`, the upload fails on `push` and `schedule` runs with `Resource not accessible by integration`, while `pull_request` runs still complete. GitHub's own CodeQL workflow therefore grants `security-events: write`.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[DOTNET_VERSION]]` | The actual .NET version used in the repository. |

### Failure Behaviour

- If the repository .NET version cannot be determined from evidence, cease generation and ask one concise clarification question. Never downgrade the `security-events` permission below `write`.

### Mandatory Validation Before Final Output

- The output file is named `security.yml`.
- The workflow `name` is `Security`.
- Triggers are `push`, `pull_request` on `master`, and a weekly `schedule`.
- The `security-scan` job grants `security-events: write` and `contents: read`, and runs on `ubuntu-latest`.
- Steps restore dependencies, check for vulnerable packages, run CodeQL `init@v4` for `csharp`, build, and run CodeQL `analyze@v4`.
- Every fixed template line is present verbatim; no placeholder or reformatted line remains.
- No secret, credential, or personal datum is exposed.

If a `security.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `security.yml` exists, create one from scratch.
