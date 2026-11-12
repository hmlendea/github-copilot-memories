Generate or revise `.github/workflows/dotnet.yml` using `templates/dotnet.yml`.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every `dotnet.yml` creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organization-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

1. Use an exact copy of `templates/dotnet.yml`; preserve the workflow `name`, triggers, job, steps, action versions, indentation, and whitespace layout.
2. The template must remain exactly as written, with only these exceptions:
   - `[[REPOSITORY_DOTNET_VERSION]]` is replaced with the actual .NET version used in the repository.
   - The two MonoGame steps are included only when the project uses MonoGame.
3. The MonoGame `Setup MGCB` and `Setup fonts` steps are gated by adjacent `# Only include this step if the project uses MonoGame. Otherwise, remove it.` comments. Include both steps together, or remove both steps **and** their directive comments, in their entirety. Never keep one step without the other.
4. When MonoGame steps are included, place them immediately before `Restore dependencies`.
5. Remove all guidance comments from the final output; the delivered `dotnet.yml` contains no `# Only include ...` comments.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[REPOSITORY_DOTNET_VERSION]]` | The actual .NET version used in the repository (for example `8.0` or `10.0`). |

### Failure Behaviour

- If the repository .NET version cannot be determined from evidence, cease generation and ask one concise clarification question. Never produce a partial workflow.

### Mandatory Validation Before Final Output

- The output file is named `dotnet.yml`.
- The workflow `name` is `.NET`.
- Triggers are `push` and `pull_request` on `master`.
- The `build` job runs on `ubuntu-latest` and performs restore, build, and test.
- `actions/setup-dotnet@v5` is used with the evidenced `dotnet-version`.
- The MonoGame steps are either both present (immediately before `Restore dependencies`) with their directive comments removed, or both absent.
- Every fixed template line is present verbatim; no placeholder, guidance comment, or reformatted line remains.
- No secret, credential, or personal datum is exposed.

If a `dotnet.yml` previously exists, preserve any content that is correct and up to date, and revise only what has changed or is missing. If no `dotnet.yml` exists, create one from scratch.
