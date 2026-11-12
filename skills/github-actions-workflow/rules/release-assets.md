Generate or revise `.github/workflows/release-assets.yml` from repository evidence.

## Scope

This workflow has **no canonical template**. There is no `templates/release-assets.yml`. Generate the file from the repository's actual release-asset requirements, using the general GitHub Actions instruction and verified repository evidence, while preserving any existing working behaviour.

Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. When a canonical template exists for a related workflow, follow that template; otherwise the general Actions rules apply.

### Generation Contract

1. Use the canonical file name `release-assets.yml`.
2. Preserve existing behaviour when revising an existing workflow; change only what the task requires.
3. Do not invent release assets, globs, tags, permissions, or capabilities. Derive them from manifests, scripts, existing workflows, and documentation.
4. Keep required permissions, triggers, actions, secrets, and structure intact.

### Failure Behaviour

- If a mandatory release-asset value remains indeterminate after evidence collection, cease generation and ask one concise clarification question. Never invent assets or identifiers.

### Mandatory Validation Before Final Output

- The output file is named `release-assets.yml`.
- The YAML is valid and defines `name`, `on`, and `jobs`.
- Every action, path, glob, and identifier agrees with repository evidence.
- No secret value, credential, or personal datum is exposed.

If a `release-assets.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `release-assets.yml` exists, create one only when the task requires it.
