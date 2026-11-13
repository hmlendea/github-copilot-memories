# GitHub Actions Workflow Template Fidelity

This rule applies **only to personal repositories owned by the current git user** — repositories whose GitHub owner is a personal account (`owner.type == "User"`) and whose owner matches the current git user. Organization-owned repositories and repositories owned by another user are out of strict-fidelity scope; fixed workflow-template fidelity is not enforced for them. Confirm repository ownership before generating or revising any workflow file:

```bash
git -C <repo_root> remote get-url origin
gh api repos/<owner>/<repo> --jq .owner.type   # must return "User"
gh api user --jq .login                        # current git user; fallback: git config github.user
```

When the user explicitly requests the templates, this rule applies regardless of who owns the repository or whether it is personal.

When generating or revising any GitHub Actions workflow from a template (`bash.yml`, `dotnet.yml`, `android.yml`, `security.yml`, `nexus-mods-release.yml`, `nuget-release.yml`, `github-release.yml`, `steam-workshop-release.yml`), the following rule is absolute.

`github-release.yml` has three mutually exclusive variants — `github-release-dotnet.yml`, `github-release-nuget.yml`, and `github-release-android.yml` — selected from evidence; all other rules in this contract apply equally to each variant.

`security.yml` has two mutually exclusive variants — `security-dotnet.yml` and `security-android.yml` — selected from evidence; all other rules in this contract apply equally to each variant.

## Repository Visibility Gate (`security.yml`)

Before creating or revising `security.yml` in either variant, confirm the repository is public:

```bash
gh api repos/<owner>/<repo> --jq .visibility   # must return "public"
```

GitHub Code Scanning requires a public repository, or GitHub Enterprise Cloud with GitHub Advanced Security. A `private` or `internal` repository, or one whose visibility cannot be confirmed, must be **refused**: add nothing, explain that CodeQL requires the repository to be public, and do not weaken the workflow to work around the restriction.

## Fixed Workflow Content Is Immutable

**Every template line outside of `[[PLACEHOLDER]]` tokens and template guidance comments must be copied byte-for-byte into the output workflow.** In this context a workflow template is YAML, so "fixed content" means:

- The workflow `name`
- `on` triggers, branches, tags, schedules, and event types
- `permissions` scopes
- Job and step names, ordering, and nesting
- `uses` action identifiers and pinned versions
- `run` commands, `with` inputs, `env` values, and expressions
- YAML key names, indentation, quoting style, and inline-array formatting
- Blank lines, comments that are not guidance directives, and line breaks exactly as written in the template

## What May Change

Only these elements may be modified during generation:

1. **Scalar placeholders** — `[[UPPER_SNAKE_CASE]]` tokens replaced with single evidence-based values
2. **Conditional steps** — entire steps gated by an adjacent `# Only include this step if ... Otherwise, remove it.` guidance comment, included or removed in their entirety
3. **Template guidance comments** — all `# Only include ...`, `# Only if ...`, `# Otherwise, remove it.`, and equivalent directive comments stripped from final output
4. **Comment lines that carry guidance** removed together with their block

## What Must Never Change

- ❌ Rewording, renaming, or "improving" any workflow `name`, job, or step
- ❌ Adding, removing, or reordering triggers, permissions, jobs, or steps beyond an evidenced conditional block
- ❌ Changing pinned action versions, action identifiers, or marketplace references
- ❌ Altering `run` commands, shell scripts, `with` inputs, or expressions
- ❌ Reformatting YAML (indentation, quoting, inline vs. block arrays, or blank lines)
- ❌ "Correcting" spelling, grammar, or formatting in fixed workflow content
- ❌ Keeping a template guidance comment in the delivered workflow

## Cross-Document Synchronisation

When creating or revising a workflow, the corresponding documentation is part of the same change. The complete `## ⚙️ GitHub Actions` section in `README.md`, the automated-scanning section in `SECURITY.md`, and any CI, release, package, deployment, or contributor guidance in `CONTRIBUTING.md`, `ARCHITECTURE.md`, `ROADMAP.md`, or `docs/` must reflect the workflow's evidenced purpose, filename, branch, and actions. A link to the workflow alone is not a substitute for synchronising the corresponding documented section.

## Enforcement

This rule is validated by the `github-actions-workflow` skill. Any output that rephrases fixed workflow content, keeps a guidance comment, or leaves an unresolved placeholder will be rejected and must be regenerated from the exact template source.
