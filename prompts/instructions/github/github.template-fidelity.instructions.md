---
description: "Enforces fixed prose fidelity for GitHub markdown templates. Prose must be copied exactly; only placeholders and comments may change."
applyTo: "**/*.md"
---

# GitHub Markdown Template Prose Fidelity

Fixed template prose is immutable: copy it byte-for-byte and change only placeholders and conditional comments. Never reword, reorder, retitle, or renormalise template prose, and never "correct" its spelling or grammar.

This rule applies **only to personal repositories owned by the current git user** — repositories whose GitHub owner is a personal account (`owner.type == "User"`) and whose owner matches the current git user. Organization-owned repositories and repositories owned by another user are out of strict-fidelity scope; template prose fidelity is not enforced for them.

When the user explicitly requests the templates, this rule applies regardless of who owns the repository or whether it is personal. Pass `--force` to the validator in that case.

Invoke the `github-md-template-fidelity` skill for the complete fidelity rules, templates, rules files, validation pipeline, and validator script.
