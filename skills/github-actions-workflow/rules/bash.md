Generate or revise `.github/workflows/bash.yml` using `templates/bash.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `bash.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use an exact copy of `templates/bash.yml`; preserve the workflow `name`, triggers, permissions, job, steps, action versions, indentation, and whitespace layout.
2. This template contains no placeholders. Do not alter any line.
3. Do not add, remove, rename, or reorder triggers, jobs, or steps.
4. Do not change the pinned action versions (`actions/checkout@v7`).
5. Remove no lines and add no YAML comments; the template contains no guidance comments.

### Placeholders

This template defines no placeholders.

### Failure Behaviour

- If the workflow must validate a non-default branch, cease generation and request one concise clarification before diverging from `master`. Never produce a partial workflow.

### Mandatory Validation Before Final Output

- The output file is named `bash.yml`.
- The workflow `name` is `Bash`.
- Triggers are `push`, `pull_request` (both on `master`), and `workflow_dispatch`.
- Top-level `permissions` sets `contents: read`.
- The `lint` job runs on `ubuntu-latest` and lints Bash scripts with `shellcheck **/*.sh --severity error`.
- Every fixed template line is present verbatim; no placeholder, added comment, or reformatted line remains.
- No secret, credential, or personal datum is exposed.

If a `bash.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `bash.yml` exists, create one from scratch.
