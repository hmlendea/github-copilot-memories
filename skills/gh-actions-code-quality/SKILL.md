---
name: gh-actions-code-quality
description: "Use when editing or reviewing GitHub Actions workflows or action metadata for TODO comments, package manager consent flags, shell glob expansion, container image tags, or analyser diagnostics, and to apply the complete GitHub Actions rule catalogue: naming, layout, and comments, and commands and containers. Preserves non-interactive execution and reproducible container images even without analyser diagnostics."
---

# GitHub Actions Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [GitHub Actions instructions](../../instructions/github/actions/github.actions.instructions.md) for workflow file names and the [github-actions-workflow](../github-actions-workflow/SKILL.md) skill for the canonical workflow templates and their fidelity contract. Load them if absent from context. Required external contracts and canonical template content take precedence; report exceptions rather than silently weakening a rule.

## Rule Catalogue

The `references/rules-*.md` files contain one directive per GitHub Actions quality and reliability rule (4 rules); the [security instructions](../../instructions/gh-actions/gh-actions.security.instructions.md) contain the 20 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations:
  - The rule requiring an explicit consent flag on package manager commands conflicts with the canonical .NET workflow template, which installs fonts with `sudo apt install` and no consent flag.
  - The rule pinning external actions to a full commit SHA conflicts with the canonical workflow templates, which reference non-exempt actions by version tag, and one by `latest`.
  - The rules declaring `read` and `write` permission scopes at job level conflict with the canonical Bash workflow template and the Android, .NET, Electron, and mod GitHub Release templates, which declare them at workflow level.
  - The rule prohibiting the expansion of externally controlled values in `run:` scripts conflicts with the canonical Android, .NET, and NuGet GitHub Release templates, which expand `github.event.release.tag_name` directly.
  - The rule prohibiting redirects from HTTPS to HTTP conflicts with the canonical .NET GitHub Release template, which pipes `wget` into `bash` without `--max-redirect=0`.
  - The template fidelity contract requires byte-for-byte template content, so retain each canonical occurrence and report it; outside template-fidelity scope, apply the rules in full.

| Concern | Threshold |
| --- | --- |
| Commit-SHA pinning exemptions | Action and reusable workflow references starting with `./`, `actions/`, or `github/`; Docker image references starting with `./` |

| Topic | Reference |
| --- | --- |
| `TODO` comments in workflows and action metadata | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| Package manager consent flags, glob expansion in shell commands, container image tags | [rules-commands-and-containers.md](references/rules-commands-and-containers.md) |

## Verification

- Review every applicable section and rule reference, not just the reported diagnostic.
- Execute existing workflow validation for the changed files, for example YAML parsing or the canonical template validator; verify permissions, action pinning, secret handling, and externally controlled input against the security instructions.
- Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
