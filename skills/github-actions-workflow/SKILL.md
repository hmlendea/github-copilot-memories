---
name: github-actions-workflow
description: Use when creating or revising any GitHub Actions workflow, including bash, .NET, Android, security, release, NuGet, Nexus Mods, Steam Workshop, release-assets, or repository-specific workflows. Holds each canonical workflow template, its rules, the fidelity contract, and the validation script; synchronises all affected documentation and validates the result.
---

# GitHub Actions Workflow

Use this skill for every creation or revision of a workflow under `.github/workflows/`, and for requests to generate any workflow covered by the repository's GitHub Actions instructions. The canonical YAML templates, their generation rules, the fidelity contract, and the validator all live in this skill.

## Fidelity scope (precondition)

Strict template fidelity applies **only to personal repositories owned by the current git user** — repositories whose GitHub owner is a personal account (`owner.type == "User"`) and whose owner matches the current git user. Organization-owned repositories and repositories owned by another user are out of strict-fidelity scope; the validator skips all fidelity checks for them.

The only exception is an **explicit user request** for the templates. When the user explicitly asks for template-based generation, full fidelity applies regardless of who owns the repository or whether it is personal. Pass `--force` to the validator, or set `GITHUB_ACTIONS_FORCE_FIDELITY=1`.

Confirm scope before generating or revising any workflow:

```bash
git -C <repo_root> remote get-url origin          # e.g. git@github.com:<owner>/<repo>.git
gh api repos/<owner>/<repo> --jq .owner.type      # must return "User"
gh api user --jq .login                           # current git user
# fallbacks for the current git user: git config github.user,
# then the login in a users.noreply.github.com commit e-mail
```

- Owner type `User` **and** owner equal to the current git user → enforce full template fidelity.
- Owner type `Organization`, owner is a different user, or either value cannot be confirmed → **skip** fidelity enforcement unless the templates are explicitly requested.

## Invocation Protocol

When creating or revising any workflow, the agent MUST:
1. Read this skill file first
2. Read the corresponding template AND rules file
3. Read the general Actions instruction and every applicable repository instruction
4. Execute the full validation pipeline and the cross-file documentation procedure before output

**Failure to read the template and rules = immediate termination.**

## Resources

| Resource | Path |
|----------|------|
| Templates | `skills/github-actions-workflow/templates/` |
| Rules | `skills/github-actions-workflow/rules/` |
| Fidelity contract | `skills/github-actions-workflow/fidelity.md` |
| Validator | `skills/github-actions-workflow/validate_github_actions.py` |

All resource paths above are relative to the skill directory `skills/github-actions-workflow/`.

## Target Files & Required Pairs

| Workflow | Output file | Template | Rules |
|----------|-------------|----------|-------|
| Bash | `bash.yml` | `templates/bash.yml` | `rules/bash.md` |
| .NET | `dotnet.yml` | `templates/dotnet.yml` | `rules/dotnet.md` |
| Android | `android.yml` | `templates/android.yml` | `rules/android.md` |
| .NET Security | `security.yml` | `templates/security.yml` | `rules/security.md` |
| Nexus Mods | `nexus-mods-release.yml` | `templates/nexus-mods-release.yml` | `rules/nexus-mods-release.md` |
| NuGet.org release | `nuget-release.yml` | `templates/nuget-release.yml` | `rules/nuget-release.md` |
| GitHub Release (compilable .NET project) | `github-release.yml` | `templates/github-release-dotnet.yml` | `rules/github-release-dotnet.md` |
| GitHub Release (NuGet package) | `github-release.yml` | `templates/github-release-nuget.yml` | `rules/github-release-nuget.md` |
| GitHub Release (Android project) | `github-release.yml` | `templates/github-release-android.yml` | `rules/github-release-android.md` |
| Steam Workshop | `steam-workshop-release.yml` | `templates/steam-workshop-release.yml` | `rules/steam-workshop-release.md` |
| Release assets | `release-assets.yml` | — (no canonical template) | `rules/release-assets.md` |

`github-release.yml` has three mutually exclusive templates; select exactly one from evidence. For `release-assets.yml` and any other workflow, use the general Actions instruction and repository evidence, preserve existing behaviour, and document the workflow from its actual YAML rather than inventing a template.

## Validation Pipeline (MANDATORY — NO SHORTCUTS)

### Step 1: Template & Rules Acquisition
Read all applicable files completely — no partial reads:
- `skills/github-actions-workflow/templates/<template>.yml`
- `skills/github-actions-workflow/rules/<rules>.md`
- `skills/github-actions-workflow/fidelity.md`
- `skills/github-actions-workflow/SKILL.md`

### Step 2: Evidence Collection
Resolve every placeholder and conditional step from repository evidence: default branch, repository .NET version, MonoGame usage, primary project path and release asset glob, NuGet package ID, Nexus Mods file ID, Steam identifiers, and existing workflows. Preserve unrelated working-tree changes.

### Step 3: Template Processing (strict)
Process the template top to bottom:
- Copy fixed workflow content byte-for-byte (per `fidelity.md`).
- Replace only `[[PLACEHOLDER]]` tokens with single evidence-based values.
- Include a step gated by a `# Only include ... Otherwise, remove it.` comment only when its condition is evidenced; otherwise remove the step **and** its directive comment in their entirety.
- Strip every template guidance comment from the delivered workflow.
- Never reformat YAML, rename or reorder jobs/steps/triggers/permissions, or change pinned action versions.

### Step 4: Cross-File Documentation Synchronisation
Enumerate every file under `.github/workflows/` and treat the complete set as the source of truth for documentation:
- Read the README template and rules before changing `README.md`: add or update the primary build badge and the security badge when their workflows exist, and update the complete `## ⚙️ GitHub Actions` section with one row for every workflow, linking each to its verified path on the default branch and describing its evidenced purpose and principal actions. Regenerate the table of contents after headings are final.
- Read the applicable policy-document template and rules before changing it: synchronise the automated-scanning section in `SECURITY.md`, and relevant CI, release, deployment, package, or contributor guidance in `CONTRIBUTING.md`, `ARCHITECTURE.md`, `ROADMAP.md`, and `docs/`.
- Update links, commands, workflow names, filenames, branches, and purposes; leave no stale references.

### Step 5: Mandatory Validation (BLOCKING)
Run the workflow fidelity validator and the Markdown fidelity validator for every affected document. ANY failure requires regeneration from Step 3.

| Check | Pass criteria |
|-------|---------------|
| File name | Matches the canonical name for the workflow category |
| Fixed content fidelity | Every fixed template line present verbatim (per `fidelity.md`) |
| Placeholder clearance | Zero `[[...]]` tokens remain |
| Guidance comments | Zero `# Only include ...` / `# Only if ...` directives remain |
| Conditional steps | Only included with evidence; removed blocks removed entirely |
| YAML validity | Workflow parses as valid YAML |
| Documentation sync | README, SECURITY.md, and other documents updated and consistent |
| Security | No secrets, credentials, personal data, or unsafe scripts |

## Forbidden Patterns (Auto-Reject)
- ❌ Reformatting, renaming, or rephrasing fixed workflow content
- ❌ Reordering triggers, permissions, jobs, or steps
- ❌ Changing pinned action versions or action identifiers
- ❌ Residual `[[PLACEHOLDER]]` tokens
- ❌ Residual template guidance comments
- ❌ Half-applied conditional steps (one MonoGame step present, the other absent)
- ❌ Invalid YAML
- ❌ Stale or unsynchronised documentation
- ❌ Invented assets, identifiers, branches, or capabilities
- ❌ Exposed secrets or credentials

## Evidence Priority (Non-Negotiable)
1. Repository source, manifests, scripts, existing workflows, documentation, policy files
2. Git metadata, release tags, package metadata, configured remotes
3. Public registry, store, and hosted metadata when accessible
4. **ONE** concise user clarification if a mandatory value remains indeterminate

## Failure Behaviour
- Unknown mandatory value after evidence collection → **STOP** and ask ONE clarification question.
- ANY validation failure → **REGENERATE from Step 3**.
- **NEVER** output a partial workflow or unsynchronised documentation.

## Integration with Agent Workflow
This skill is invoked when a workflow under `.github/workflows/` is created or revised in a scoped personal repository, when the user explicitly requests the templates, or when validation is requested. It provides the validation pipeline and the `validate_github_actions.py` validator.

Organization-owned repositories, repositories owned by another user, and repositories whose ownership cannot be confirmed are out of strict-fidelity scope; the validator skips enforcement for them unless the templates are explicitly requested.

## Validation Script Usage

```bash
# Validate a generated workflow file
python3 skills/github-actions-workflow/validate_github_actions.py /path/to/repo dotnet.yml generated_dotnet.yml

# Validate from stdin
cat generated_dotnet.yml | python3 skills/github-actions-workflow/validate_github_actions.py /path/to/repo dotnet.yml

# Disambiguate the shared github-release.yml output
python3 skills/github-actions-workflow/validate_github_actions.py --variant nuget /path/to/repo github-release.yml generated_github_release.yml
python3 skills/github-actions-workflow/validate_github_actions.py --variant android /path/to/repo github-release.yml generated_github_release.yml

# Enforce fidelity regardless of ownership (explicit template request)
python3 skills/github-actions-workflow/validate_github_actions.py --force /path/to/repo security.yml generated_security.yml
```

Exit codes:
- 0: Validation passed (100% fidelity)
- 1: Validation failed (errors found)
- 2: Script usage error
- 3: Enforcement skipped (repository is not a personal repository owned by the current git user, and templates were not explicitly requested)

## Evidence Collection Checklist

- [ ] Default branch name
- [ ] Repository .NET version (`TargetFramework`, `global.json`)
- [ ] Repository Java (JDK) version (`sourceCompatibility`, `jvmTarget`)
- [ ] MonoGame usage
- [ ] Primary project path and release asset glob
- [ ] NuGet package ID and `NUGET_USER` secret
- [ ] Nexus Mods file ID and `NEXUSMODS_API_KEY` secret
- [ ] Steam app ID, Workshop item ID, and Steam secrets
- [ ] Existing workflows under `.github/workflows/`
- [ ] README, `SECURITY.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `ROADMAP.md`, and `docs/`
