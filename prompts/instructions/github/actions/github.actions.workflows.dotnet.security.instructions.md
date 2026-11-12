---
description: "Use when creating or revising the .NET Security GitHub Actions workflow file. Provides the canonical template for security.yml."
applyTo: ".github/workflows/security.yml"
---

Use the canonical template `skills/github-actions-workflow/templates/security.yml` for `security.yml`, and its rules `skills/github-actions-workflow/rules/security.md`.

The template must remain exactly as written, with only these exceptions:

- `dotnet-version` must be set to the actual .NET version used in the repository.

The `security-events` permission must be `write`. The CodeQL `analyze` action uploads SARIF results to GitHub Code Scanning, and that upload requires the `security-events: write` scope. With `security-events: read`, the upload fails on `push` and `schedule` runs with `Resource not accessible by integration`, while `pull_request` runs still complete. GitHub's own CodeQL workflow therefore grants `security-events: write`.

Apply the complete `github-actions-workflow` skill in `skills/github-actions-workflow/SKILL.md` for the cross-file procedure, documentation synchronisation, fidelity contract, and validation.
