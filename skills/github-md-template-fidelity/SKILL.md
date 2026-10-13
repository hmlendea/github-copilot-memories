---
description: "Enforces 100% template fidelity for GitHub markdown files (README.md, ARCHITECTURE.md, CONTRIBUTING.md, SECURITY.md, PRIVACY.md, ROADMAP.md). Validates output against templates and rules before allowing completion."
---

# GitHub MD Template Fidelity Skill

This skill enforces **100% template fidelity** for all GitHub markdown document generation. It must be invoked for any task that creates or revises these files.

## Invocation Protocol

When generating or revising any of these files, the agent MUST:
1. Read this skill file first
2. Read the corresponding template AND rules files
3. Execute the full validation pipeline before output

## Target Files & Required Pairs

| Target | Template | Rules | Fidelity |
|--------|----------|-------|----------|
| README.md | `prompts/instructions/github/github.readme.template.instructions.md` | `prompts/instructions/github/github.readme.rules.instructions.md` | `prompts/instructions/github/github.template-fidelity.instructions.md` |
| ARCHITECTURE.md | `prompts/instructions/github/github.architecture.template.instructions.md` | `prompts/instructions/github/github.architecture.rules.instructions.md` | `prompts/instructions/github/github.template-fidelity.instructions.md` |
| CONTRIBUTING.md | `prompts/instructions/github/github.contributing.template.instructions.md` | `prompts/instructions/github/github.contributing.rules.instructions.md` | `prompts/instructions/github/github.template-fidelity.instructions.md` |
| SECURITY.md | `prompts/instructions/github/github.security.template.instructions.md` | `prompts/instructions/github/github.security.rules.instructions.md` | `prompts/instructions/github/github.template-fidelity.instructions.md` |
| PRIVACY.md | `prompts/instructions/github/github.privacy.template.instructions.md` | `prompts/instructions/github/github.privacy.rules.instructions.md` | `prompts/instructions/github/github.template-fidelity.instructions.md` |
| ROADMAP.md | `prompts/instructions/github/github.roadmap.template.instructions.md` | `prompts/instructions/github/github.roadmap.rules.instructions.md` | `prompts/instructions/github/github.template-fidelity.instructions.md` |

## Validation Pipeline (MANDATORY - NO SHORTCUTS)

### Step 1: Template Acquisition
```bash
# Read ALL THREE files completely - no partial reads
read_file(template_path, 1, -1)
read_file(rules_path, 1, -1)
read_file(fidelity_path, 1, -1)  # prompts/instructions/github/github.template-fidelity.instructions.md
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
| **Fixed prose fidelity** | **Byte-for-byte match of all template prose outside placeholders/comments (per `github.template-fidelity.instructions.md`)** |
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
- User requests creation/revision of any target GitHub MD file
- Agent detects GitHub MD file operation in progress
- Validation is requested explicitly

The skill provides the `validate_github_md` function for programmatic validation.

## Validation Script Usage
```bash
# Validate a generated file
python3 skills/github-md-template-fidelity/validate_github_md.py /path/to/repo README.md generated_readme.md

# Validate from stdin
cat generated_readme.md | python3 skills/github-md-template-fidelity/validate_github_md.py /path/to/repo README.md
```

Exit codes:
- 0: Validation passed (100% fidelity)
- 1: Validation failed (errors found)
- 2: Script usage error

## Agent Instructions for 100% Fidelity

When generating ANY GitHub MD file, the agent MUST:

1. **READ BOTH FILES FIRST** - Template AND Rules for the target file type
2. **COLLECT EVIDENCE** - For every conditional in template, verify with repository
3. **PROCESS LINE BY LINE** - Copy fixed prose verbatim, resolve placeholders, evaluate conditionals
4. **GENERATE ToC LAST** - After all content finalized, with NO emojis, 2-space indent
5. **VALIDATE BEFORE OUTPUT** - Run all checks, regenerate on ANY failure

### Critical Rules That Must NEVER Be Violated

| Rule | Enforcement |
|------|-------------|
| No emojis in ToC | Auto-reject |
| No unresolved placeholders | Auto-reject |
| No template comments in output | Auto-reject |
| **No rephrased fixed prose (byte-for-byte fidelity per `github.template-fidelity.instructions.md`)** | **Auto-reject** |
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
| README.md | `prompts/instructions/github/github.readme.template.instructions.md` | `prompts/instructions/github/github.readme.rules.instructions.md` |
| ARCHITECTURE.md | `prompts/instructions/github/github.architecture.template.instructions.md` | `prompts/instructions/github/github.architecture.rules.instructions.md` |
| CONTRIBUTING.md | `prompts/instructions/github/github.contributing.template.instructions.md` | `prompts/instructions/github/github.contributing.rules.instructions.md` |
| SECURITY.md | `prompts/instructions/github/github.security.template.instructions.md` | `prompts/instructions/github/github.security.rules.instructions.md` |
| PRIVACY.md | `prompts/instructions/github/github.privacy.template.instructions.md` | `prompts/instructions/github/github.privacy.rules.instructions.md` |
| ROADMAP.md | `prompts/instructions/github/github.roadmap.template.instructions.md` | `prompts/instructions/github/github.roadmap.rules.instructions.md` |