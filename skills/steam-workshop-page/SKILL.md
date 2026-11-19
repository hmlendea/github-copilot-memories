---
name: steam-workshop-page
description: "Use when creating or revising a Steam Workshop page description, or when a mod, UI pack, or other Workshop item page requires its BBCode body generated or refreshed. Holds the canonical BBCode template, its generation rules, the fidelity contract, and the validator; synchronises affected documentation and validates the result."
---

# Steam Workshop Page

Use this skill for every creation or revision of a Steam Workshop page description — the BBCode body published on the item's Workshop page. The canonical template, its generation rules, the fidelity contract, and the validator all live in this skill.

## Fidelity scope (precondition)

Strict template fidelity applies **only to personal repositories owned by the current git user** — repositories whose GitHub owner is a personal account (`owner.type == "User"`) and whose owner matches the current git user. Organisation-owned repositories and repositories owned by another user are out of strict-fidelity scope; the validator skips all fidelity checks for them.

The only exception is an **explicit user request** for the template. When the user explicitly requests template-based generation, full fidelity applies regardless of who owns the repository or whether it is personal. Pass `--force` to the validator, or set `STEAM_WORKSHOP_FORCE_FIDELITY=1`.

Confirm scope prior to generating or revising a description:

```bash
git -C <repo_root> remote get-url origin          # e.g. git@github.com:<owner>/<repo>.git
gh api repos/<owner>/<repo> --jq .owner.type      # must return "User"
gh api user --jq .login                           # current git user
# fallbacks for the current git user: git config github.user,
# then the login in a users.noreply.github.com commit e-mail
```

- Owner type `User` **and** owner equal to the current git user → enforce full template fidelity.
- Owner type `Organization`, owner is a different user, or either value remains unconfirmed → **skip** fidelity enforcement unless the template is explicitly requested.

## Invocation Protocol

When creating or revising a Workshop page description, the agent MUST:
1. Read this skill file first
2. Read the template AND rules file
3. Read every applicable repository instruction
4. Execute the full validation pipeline prior to output

**Failure to read the template and rules = immediate termination.**

## Resources

| Resource | Path |
|----------|------|
| Template | `skills/steam-workshop-page/templates/workshop-description.bbcode` |
| Rules | `skills/steam-workshop-page/rules/workshop-description.md` |
| Fidelity contract | `skills/steam-workshop-page/fidelity.md` |
| Validator | `skills/steam-workshop-page/validate_steam_workshop_page.py` |

All resource paths above are relative to the skill directory `skills/steam-workshop-page/`.

## Target File & Required Pair

| Target | Output path | Template | Rules | Fidelity |
|--------|-------------|----------|-------|----------|
| Steam Workshop description (BBCode) | `description/steam-workshop.bbcode` | `templates/workshop-description.bbcode` | `rules/workshop-description.md` | `fidelity.md` |

Write the generated description to `description/steam-workshop.bbcode` in the repository root, creating the `description/` directory when it does not exist. Never use another path or file name.

## Validation Pipeline (MANDATORY — NO SHORTCUTS)

### Step 1: Template & Rules Acquisition
Read all applicable files completely — no partial reads:
- `skills/steam-workshop-page/templates/workshop-description.bbcode`
- `skills/steam-workshop-page/rules/workshop-description.md`
- `skills/steam-workshop-page/fidelity.md`
- `skills/steam-workshop-page/SKILL.md`

### Step 2: Evidence Collection
Resolve every placeholder from repository evidence:
- Repository URL, owner, and name from the `origin` remote
- Funding link from `.github/FUNDING.yml` (`custom` first, then `github`)
- Asset base URL that hosts `announcement_donation.png` and `banner_donate.png`
- Game, supported versions, dependencies, load order, and compatibility constraints from descriptors and documentation
- Installation, enabling, and troubleshooting guidance from existing documentation

Do not infer unsupported capabilities, compatibility, guarantees, or requirements. Never expose credentials, secret values, personal data, or private endpoints.

### Step 3: Template Processing (strict)
Process the template top to bottom:
- Copy the header and footer blocks byte-for-byte (per `fidelity.md`).
- Copy every fixed prose line in place; the template holds the About, Capabilities, Installation, Contributing, Support, Project Engagement, and License wording.
- Replace only `[[PLACEHOLDER]]` tokens with single evidence-based values.
- Duplicate each `Repeat` line once per evidenced record, then remove the example placeholder.
- Include a block gated by an `<!-- Only if ... -->` comment only when its condition is evidenced; otherwise remove the block together with its heading, body, and directive comment.
- Strip every template comment from the delivered description.
- Never reorder, merge, or reformat the header or footer blocks.
- Never reorder the mandatory sections.
- Never normalise the `:/linkfilter/` segment or the stray space within the header's first closing `[/url]` chain.
- Never normalise the `:/linkfilter/` segment or the stray space within the header's first closing `[/url]` chain.

### Step 4: Cross-File Documentation Synchronisation
- When the Steam Workshop description lives in the repository, update the README section that documents Workshop publication, and any packaging documentation that references the page body.
- Update links, commands, filenames, and purposes; retain no stale references.

### Step 5: Mandatory Validation (BLOCKING)
Run the description fidelity validator. ANY failure requires regeneration from Step 3.

| Check | Pass criteria |
|-------|---------------|
| Output path | The description is written to `description/steam-workshop.bbcode` |
| Header fidelity | The exact initial block is present, in order, byte-for-byte after substitution |
| Footer fidelity | The exact closing donate banner is the final block |
| Mandatory sections | About, Capabilities, Installation, Support, Project Engagement, and License are present, in order, with their template prose |
| Fixed prose fidelity | Every fixed template line survives verbatim; only placeholders, `Repeat` lines, and conditional blocks change |
| Conditional blocks | Included only with evidence; otherwise removed entirely with their directive comments |
| Installation section | Badge block, then the conditional `[h2]Upgrading[/h2]` sub-section; no Manual Installation or Uninstallation sub-section |
| Requirements section | Present only when more than the base game is required |
| Capabilities list | Non-vacant `[list]` of at most twelve evidenced capabilities |
| Compatibility content | Fixed unified sentence `This mod is compatible with <GAME_NAME> <SUPPORTED_GAME_VERSION> on all operating systems.`, the language list, the incompatible-mod list when applicable, and the `[h2]Load Order[/h2]` subsection |
| Support content | Fixed issue-tracker sentence, plus the conditional FAQ sentence, troubleshooting-document sentence, and additional support |
| Merged sections | No standalone Troubleshooting, FAQ, Changelog, or Localisation section exists; Load Order is a Compatibility subsection |
| Contributing section | Conditional on `CONTRIBUTING.md`; carries only the fixed guidelines sentence |
| License section | Single fixed sentence whose licence title links to `LICENSE`; no separate licence sentence |
| Related Mods | Each mod links to its Steam Workshop page, otherwise Nexus Mods, otherwise GitHub |
| Installation badges | At least one badge in the exact store form; at most three per line, distributed as evenly as possible across the fewest lines; four-space prefix; one trailing space on every line but the last |
| Placeholder clearance | Zero `[[...]]` tokens remain |
| Link filtering | Every non-Steam outbound link is wrapped in the Steam link filter |
| BBCode only | No Markdown syntax and no literal HTML |
| Content substance | Evidenced features, requirements, installation, and compatibility only |
| Documentation sync | README and packaging documents updated and consistent |
| Security | No secrets, credentials, personal data, or private endpoints |

## Prohibited Constructs
- ❌ Removing, reordering, or partially emitting the header or footer blocks
- ❌ Omitting or reordering the mandatory About, Capabilities, Installation, Contributing, Support, Project Engagement, or License section
- ❌ Emitting a standalone Troubleshooting, FAQ, Changelog, or Localisation section, or a Manual Installation or Uninstallation sub-section
- ❌ Emitting the Requirements section when only the base game is required
- ❌ Reinstating the removed game-version line, the removed OS-agnostic paragraph, or inline emphasis inside the unified compatibility sentence
- ❌ Emitting the removed development-platform paragraph or the removed blanket multi-mod compatibility claim
- ❌ Emitting `Load Order` as a top-level section, or opening `Contributing` with the removal welcome paragraph
- ❌ Rewording, reformatting, or relocating any fixed template prose
- ❌ Leaving a `<!-- ... -->` directive comment or a `Repeat` example in the delivered description
- ❌ More than three badges on one badge line, an uneven badge distribution across lines, or a missing four-space prefix or trailing space
- ❌ Changing the store-badge path from `/badges/stores/`
- ❌ "Fixing" `https://steamcommunity.com:/linkfilter/?url=` into a normal URL
- ❌ Markdown or HTML syntax in the description body
- ❌ Invented capabilities, dependencies, compatibility, or asset hosts
- ❌ Residual `[[PLACEHOLDER]]` tokens
- ❌ Vacant headings, vacant sections, or filler content
- ❌ Keyword stuffing, hidden text, or unverified claims
- ❌ Writing the description to a path or file name other than `description/steam-workshop.bbcode`

## Evidence Priority (Non-Negotiable)
1. Repository source, descriptors, manifests, documentation, and existing page content
2. Git metadata, release tags, and configured remotes
3. Public Workshop metadata and hosted documentation when accessible
4. **ONE** concise user clarification if a mandatory value remains indeterminate

## Failure Handling
- If a mandatory value remains indeterminate after evidence collection → **STOP** and request ONE clarification question. Never invent a URL or asset host.
- If ANY validation check fails → **REGENERATE from Step 3**
- **NEVER** produce a partial or non-compliant description

## Donation Link Resolution
Resolve `[[FUNDING_URL]]` from `.github/FUNDING.yml`:
1. Use the `custom` field value verbatim.
2. When `custom` is absent or devoid of a value, use the `github` field as `https://github.com/sponsors/<github>`.
3. When the user or repository explicitly provides a donation link, use that instead.
Never invent a donation link.

## Integration with Agent Workflow
This skill is automatically invoked when:
- The user requests creation or revision of a Steam Workshop page description **in a personal repository owned by the current git user**
- The agent detects Workshop description generation in progress in such a repository
- Validation is requested explicitly
- The user explicitly requests the template, regardless of repository ownership or owner type

The skill provides the `validate_steam_workshop_page` function for programmatic validation.

## Validation Script Usage
```bash
# Validate a generated description
python3 skills/steam-workshop-page/validate_steam_workshop_page.py /path/to/repo generated_description.bbcode

# Validate from stdin
cat generated_description.bbcode | python3 skills/steam-workshop-page/validate_steam_workshop_page.py /path/to/repo

# Enforce fidelity regardless of ownership (explicit template request)
python3 skills/steam-workshop-page/validate_steam_workshop_page.py --force /path/to/repo generated_description.bbcode
```

Exit codes:
- 0: Validation passed (100% fidelity)
- 1: Validation failed (errors found)
- 2: Script usage error
- 3: Enforcement skipped (repository is not a personal repository owned by the current git user, and the template was not explicitly requested)

## Agent Instructions for 100% Fidelity

When generating a Workshop page description, the agent MUST:

1. **READ BOTH FILES FIRST** — template AND rules
2. **COLLECT EVIDENCE** — for every placeholder, verify with the repository
3. **PROCESS LINE BY LINE** — copy fixed blocks verbatim, resolve placeholders, expand content
4. **VALIDATE BEFORE OUTPUT** — run all checks, regenerate on ANY failure

### Critical Rules That Must NEVER Be Violated

| Rule | Enforcement |
|------|-------------|
| Header block present and exact | Auto-reject |
| Closing banner final and exact | Auto-reject |
| Mandatory sections present, ordered, and unmodified | Auto-reject |
| Installation badge layout exact | Auto-reject |
| No unresolved placeholders | Auto-reject |
| No Markdown or HTML | Auto-reject |
| Every non-Steam outbound link link-filtered | Auto-reject |
| Evidence-based values only | Auto-reject |
| No literal-HTML or script injection | Auto-reject |

### Evidence Collection Checklist

- [ ] Repository URL resolved from `origin`
- [ ] Funding link resolved from `.github/FUNDING.yml`
- [ ] Asset base URL resolves both banner images
- [ ] Steam Workshop item identifier resolved
- [ ] Licence title and suffix resolved from `LICENSE`
- [ ] At least one evidenced distribution channel for the Installation badges
- [ ] Manual installation steps evidence-collected
- [ ] Principal capabilities evidence-collected
- [ ] FAQ document presence confirmed or denied
- [ ] Supported languages and translation completeness evidence-collected
- [ ] Game name, supported game version, load order, and known incompatible mods evidence-collected
- [ ] Related mods identified with their Steam, Nexus, or GitHub pages
- [ ] Game and supported version identified from the descriptor
- [ ] Dependencies, load order, and compatibility confirmed from documentation
- [ ] Material limitations confirmed and recorded under Compatibility or Troubleshooting