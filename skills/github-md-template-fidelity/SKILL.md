---
description: "Enforces 100% template fidelity for GitHub markdown files in personal repositories owned by the current git user (README.md, ARCHITECTURE.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, PRIVACY.md, ROADMAP.md). Validates output against templates and rules before allowing completion. Skipped for organization-owned repositories, repositories owned by another user, and repositories whose ownership cannot be confirmed — unless the user explicitly requests the templates."
---

# GitHub MD Template Fidelity Skill

This skill enforces **100% template fidelity** for GitHub markdown document generation **only in personal repositories owned by the current git user** — repositories whose GitHub owner is a personal account (`owner.type == "User"`) and whose owner matches the current git user. Organization-owned repositories and repositories owned by another user are out of strict-fidelity scope; the validator skips all fidelity checks for them.

The only exception is an **explicit user request** for the templates. When the user explicitly asks for template-based generation, full fidelity applies regardless of who owns the repository or whether it is personal.

## Repository Scope (precondition)

Enforce fidelity only when the target repository is personal **and** owned by the current git user:

```bash
git -C <repo_root> remote get-url origin          # e.g. git@github.com:<owner>/<repo>.git
gh api repos/<owner>/<repo> --jq .owner.type      # must return "User"
gh api user --jq .login                           # current git user
# fallbacks for the current git user: git config github.user,
# then the login in a users.noreply.github.com commit e-mail
```

- Owner type `User` **and** owner equal to the current git user → enforce full template fidelity (read templates/rules/fidelity, run the pipeline, validate before output).
- Owner type `Organization`, owner is a different user, or either value cannot be confirmed → **skip** template fidelity enforcement entirely; treat GitHub markdown generation as optional guidance without enforcement.
- **Explicit request override:** when the user explicitly requests the templates (for example "use the templates", "apply template fidelity", or running the `github-md-generator` prompt), enforce full fidelity regardless of owner type or ownership. Pass `--force` to the validator, or set `GITHUB_MD_FORCE_FIDELITY=1`.

---

## Invocation Protocol

When generating or revising any of these files **in a scoped personal repository, or whenever the user explicitly requests the templates**, the agent MUST:
1. Read this skill file first
2. Read the corresponding template AND rules files
3. Execute the full validation pipeline before output

## Resources

| Resource | Path |
|----------|------|
| Templates | `skills/github-md-template-fidelity/templates/` |
| Rules | `skills/github-md-template-fidelity/rules/` |
| Fidelity contract | `skills/github-md-template-fidelity/fidelity.md` |
| Validator | `skills/github-md-template-fidelity/validate_github_md.py` |

## Target Files & Required Pairs

| Target | Template | Rules | Fidelity |
|--------|----------|-------|----------|
| README.md | `templates/readme.md` | `rules/readme.md` | `fidelity.md` |
| ARCHITECTURE.md | `templates/architecture.md` | `rules/architecture.md` | `fidelity.md` |
| CONTRIBUTING.md | `templates/contributing.md` | `rules/contributing.md` | `fidelity.md` |
| CODE_OF_CONDUCT.md | `templates/code-of-conduct.md` | `rules/code-of-conduct.md` | `fidelity.md` |
| SECURITY.md | `templates/security.md` | `rules/security.md` | `fidelity.md` |
| PRIVACY.md | `templates/privacy.md` | `rules/privacy.md` | `fidelity.md` |
| ROADMAP.md | `templates/roadmap.md` | `rules/roadmap.md` | `fidelity.md` |

All resource paths above are relative to the skill directory `skills/github-md-template-fidelity/`.

## Validation Pipeline (MANDATORY - NO SHORTCUTS)

### Step 1: Template Acquisition
```bash
# Read ALL THREE files completely - no partial reads
read_file(template_path, 1, -1)   # skills/github-md-template-fidelity/templates/<target>.md
read_file(rules_path, 1, -1)      # skills/github-md-template-fidelity/rules/<target>.md
read_file(fidelity_path, 1, -1)   # skills/github-md-template-fidelity/fidelity.md
```

### Step 2: Evidence Collection
For each conditional block in template, verify evidence exists:
- File existence: `ls`, `test -f`, `glob`
- GitHub metadata: `gh api`, `gh release`, `gh workflow`
- Config parsing: `jq`, `dotnet`, `cargo`, `npm`, `pip`
- Directory structure: `find`, `tree`

### Step 3: Line-by-Line Template Processing
Process template from line 1 to EOF:
- **Fixed prose**: Copy EXACTLY (byte-for-byte including whitespace)
- **Placeholders**: Replace with evidence-based values
- **Conditionals**: Evaluate `<!-- Only if ... -->` and `<!-- Always include -->`
- **Repeatable**: Duplicate only when template comment says "Repeat"
- **Comments**: Strip ALL template comments from output

### Step 4: ToC Generation (Post-Content)
After ALL content finalized:
```markdown
## 📑 Table of Contents

- [Exact Heading Text](#exact-heading-anchor)
  - [Nested Heading](#nested-heading-anchor)
```
Rules:
- Include EVERY `##`, `###`, `####` in final output order
- Indent: 2 spaces per nesting level
- **ZERO emojis** in ToC text or anchors
- Valid markdown links to heading anchors

### Step 5: Final Validation (BLOCKING)
Run ALL checks - ANY failure requires full regeneration:

| Check | Pass Criteria |
|-------|---------------|
| Heading fidelity | Every heading matches template EXACTLY (emoji, case, punctuation, order) |
| Badge validity | Every badge has evidenced service/package/workflow/distribution/license |
| Mandatory sections | All "Always include" sections present |
| Conditional sections | Only included with evidence + substantive content |
| Additional sections | Only if genuinely material + no template section fits |
| **Fixed prose fidelity** | **Byte-for-byte match of all template prose outside placeholders/comments (per `fidelity.md`)** |
| Placeholder clearance | Zero `[[...]]`, `[[[...]]]`, template comments, unused examples |
| Empty content | No empty headings, tables, lists, code blocks |
| ToC completeness | Every final heading in ToC, correct order, 2-space indent, no emojis |
| Evidence alignment | Commands, paths, versions, links, defaults match repository |
| Release subsection | Exactly one `### Release` (or fixed .NET `release.sh` subsection) |
| Security | No secrets, credentials, personal data, private endpoints, unsafe scripts |

## Forbidden Patterns (Auto-Reject)
- ❌ Emojis in Table of Contents
- ❌ Missing template-defined headings
- ❌ Unresolved `<!-- [...] -->` conditional content
- ❌ Rephrased fixed template prose
- ❌ Placeholder text in output
- ❌ Empty sections/tables/code blocks
- ❌ Incorrect heading hierarchy
- ❌ Wrong emoji in headings
- ❌ Invented capabilities/packages/features

## Evidence Priority (Non-Negotiable)
1. Repository source, docs, manifests, configs, scripts, workflows, policy files
2. Git metadata, release tags, package metadata, configured remotes
3. Public registry metadata, hosted docs, deployment metadata
4. **ONE** concise user clarification if mandatory value indeterminate

## Failure Behavior
- If mandatory core value indeterminate after evidence collection → **STOP** and ask ONE clarification question
- If ANY validation check fails → **REGENERATE from Step 3**
- **NEVER** output partial or non-compliant document

## Integration with Agent Workflow
This skill is automatically invoked when:
- User requests creation/revision of any target GitHub MD file **in a personal repository owned by the current git user**
- Agent detects GitHub MD file operation in progress in such a repository
- Validation is requested explicitly
- User explicitly requests the templates, regardless of repository ownership or owner type

Organization-owned repositories, repositories owned by another user, and repositories whose ownership cannot be confirmed are out of strict-fidelity scope; the validator skips enforcement for them unless the templates are explicitly requested.

The skill provides the `validate_github_md` function for programmatic validation.

## Validation Script Usage
```bash
# Validate a generated file
python3 skills/github-md-template-fidelity/validate_github_md.py /path/to/repo README.md generated_readme.md

# Validate from stdin
cat generated_readme.md | python3 skills/github-md-template-fidelity/validate_github_md.py /path/to/repo README.md

# Enforce fidelity regardless of ownership (explicit template request)
python3 skills/github-md-template-fidelity/validate_github_md.py --force /path/to/repo README.md generated_readme.md
```

Exit codes:
- 0: Validation passed (100% fidelity)
- 1: Validation failed (errors found)
- 2: Script usage error
- 3: Enforcement skipped (repository is not a personal repository owned by the current git user, and templates were not explicitly requested)

## Agent Instructions for 100% Fidelity

When generating ANY GitHub MD file, the agent MUST:

1. **READ BOTH FILES FIRST** - Template AND Rules for the target file type
2. **COLLECT EVIDENCE** - For every conditional in template, verify with repository
3. **PROCESS LINE BY LINE** - Copy fixed prose verbatim, resolve placeholders, evaluate conditionals
4. **GENERATE ToC LAST** - When the template defines a ToC, generate it after all content is finalized, with NO emojis and 2-space indent
5. **VALIDATE BEFORE OUTPUT** - Run all checks, regenerate on ANY failure

### Critical Rules That Must NEVER Be Violated

| Rule | Enforcement |
|------|-------------|
| No emojis in ToC | Auto-reject |
| No unresolved placeholders | Auto-reject |
| No template comments in output | Auto-reject |
| **No rephrased fixed prose (byte-for-byte fidelity per `fidelity.md`)** | **Auto-reject** |
| No missing mandatory sections | Auto-reject |
| No empty sections/tables/code blocks | Auto-reject |
| Heading hierarchy matches template exactly | Auto-reject |
| Badges only for evidenced services | Auto-reject |
| Evidence-based values only | Auto-reject |

### Evidence Collection Checklist

For each target file type, verify:

**README.md:**
- [ ] LICENSE file exists
- [ ] preview.png exists
- [ ] screenshots/ directory with images
- [ ] examples/ or samples/ directory
- [ ] .github/workflows/ files
- [ ] Package manifests (package.json, .csproj, Cargo.toml, pyproject.toml, etc.)
- [ ] GitHub releases (published, not just tags)
- [ ] Repository website/Pages URL
- [ ] .github/FUNDING.yml
- [ ] Coverage provider configured
- [ ] Code quality service configured
- [ ] Container image published
- [ ] Default branch name

**ARCHITECTURE.md:**
- [ ] Entry points, composition roots
- [ ] Project manifests, configuration
- [ ] Public contracts, persistence adapters
- [ ] Integration boundaries, tests
- [ ] Deployment artefacts
- [ ] Directory structure

**CONTRIBUTING.md:**
- [ ] CODE_OF_CONDUCT.md exists
- [ ] SECURITY.md exists
- [ ] ROADMAP.md exists
- [ ] Development setup commands
- [ ] Test commands
- [ ] Lint/format commands
- [ ] Default branch

**CODE_OF_CONDUCT.md:**
- [ ] Verified reporting contact or channel
- [ ] Contributor Covenant v1.4 wording and attribution
- [ ] `CONTRIBUTING.md` and `README.md` links when those files exist

**SECURITY.md:**
- [ ] Supported versions/distribution channels
- [ ] Vulnerability reporting process
- [ ] Disclosure policy
- [ ] Safe harbour statement
- [ ] Recognition practice

**PRIVACY.md:**
- [ ] Self-hosted deployment support
- [ ] Data categories handled
- [ ] Processing activities
- [ ] Storage/retention/deletion practices
- [ ] External integrations
- [ ] User controls
- [ ] International transfers
- [ ] Children/age restrictions
- [ ] Security safeguards

**ROADMAP.md:**
- [ ] Current initiatives
- [ ] Planned labour
- [ ] Milestones
- [ ] Dependencies/risks
- [ ] CHANGELOG.md exists
- [ ] Related planning docs

## Quick Reference: Template + Rules File Pairs

| Target | Template | Rules |
|--------|----------|-------|
| README.md | `templates/readme.md` | `rules/readme.md` |
| ARCHITECTURE.md | `templates/architecture.md` | `rules/architecture.md` |
| CONTRIBUTING.md | `templates/contributing.md` | `rules/contributing.md` |
| CODE_OF_CONDUCT.md | `templates/code-of-conduct.md` | `rules/code-of-conduct.md` |
| SECURITY.md | `templates/security.md` | `rules/security.md` |
| PRIVACY.md | `templates/privacy.md` | `rules/privacy.md` |
| ROADMAP.md | `templates/roadmap.md` | `rules/roadmap.md` |