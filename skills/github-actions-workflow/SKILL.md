---
name: github-actions-workflow
description: Use when creating or revising any GitHub Actions workflow, including bash, .NET, security, release, NuGet, Nexus Mods, Steam Workshop, release-assets, or repository-specific workflows. Synchronises all affected documentation and validates the result.
---

# GitHub Actions Workflow

Use this skill for every creation or revision of a workflow under `.github/workflows/`, and for requests to generate any workflow covered by the repository's GitHub Actions instructions.

## Supported workflow templates

The path-scoped workflow instruction files remain the single source of truth for each workflow file. This skill does not duplicate their YAML; it reads them, applies them, and drives the cross-file documentation work.

Read the applicable instruction files before editing. The canonical templates are:

| Workflow | File | Instruction |
|---|---|---|
| Bash | `bash.yml` | `prompts/instructions/github/actions/github.actions.workflows.bash.instructions.md` |
| .NET | `dotnet.yml` | `prompts/instructions/github/actions/github.actions.workflows.dotnet.instructions.md` |
| .NET Security | `security.yml` | `prompts/instructions/github/actions/github.actions.workflows.dotnet.security.instructions.md` |
| Nexus Mods | `nexus-mods.yml` | `prompts/instructions/github/actions/github.actions.workflows.nexus-mods.instructions.md` |
| NuGet.org release | `nuget-release.yml` | `prompts/instructions/github/actions/github.actions.workflows.nuget-release.instructions.md` |
| GitHub Release | `github-release.yml` | `prompts/instructions/github/actions/github.actions.workflows.nuget.github-release.instructions.md` |
| Steam Workshop | `steam-workshop.yml` | `prompts/instructions/github/actions/github.actions.workflows.steam-workshop.instructions.md` |
| Release assets | `release-assets.yml` | Use the general Actions instruction and repository evidence when no dedicated template exists. |

For any other workflow, use the general Actions instruction, preserve existing behaviour, and document the workflow from its actual YAML rather than inventing a template.

## Procedure

1. Read the general Actions instruction and the selected workflow instruction completely. Read all referenced templates and applicable repository instructions.
2. Inspect the repository, existing workflows, default branch, remote metadata, manifests, scripts, and documentation. Preserve unrelated working-tree changes.
3. Create or revise the canonical workflow file. Replace only documented placeholders and repository-specific values. Keep required permissions, triggers, actions, secrets, and exact template structure.
4. Enumerate every file under `.github/workflows/`. Treat the complete set, not only the changed file, as the source of truth for documentation.
5. Read the README template and rules before changing `README.md`. Update the complete conditional workflow documentation:
   - Add or update the primary build badge when a primary validation workflow exists.
   - Add or update the security badge when `security.yml` exists.
   - Update `## ⚙️ GitHub Actions` with one row for every workflow.
   - Link each workflow to its verified repository path and default branch.
   - Describe each workflow's evidenced purpose and principal actions.
   - Regenerate the table of contents after headings are final.
6. Read the applicable policy-document template and rules before changing it. Update existing documentation when the workflow changes its content:
   - Synchronise the complete automated-scanning section in `SECURITY.md` for security workflows.
   - Synchronise relevant CI, release, deployment, package, or contributor guidance in `CONTRIBUTING.md`, `ARCHITECTURE.md`, `ROADMAP.md`, and `docs/` when present.
   - Update links, commands, workflow names, filenames, branches, and purposes; do not leave stale references.
7. If a referenced documentation file does not exist, create it only when the applicable rules require it or the workflow makes the documentation materially necessary. Do not create speculative documentation.
8. Run the repository's Markdown fidelity validator for every generated or revised GitHub Markdown file. Check workflow paths, badge URLs, links, placeholders, heading order, table-of-contents entries, and stale workflow references.
9. Review the final diff and confirm that the workflow and all affected documentation are consistent. Report any unverifiable GitHub metadata or blocked validation instead of guessing.

## Completion criteria

The task is incomplete until the workflow and every affected documentation file are synchronised, or a concrete documentation blocker is reported. A workflow-only change is not sufficient when README or existing documentation describes workflows, security scanning, CI, releases, packages, deployment, or contributor procedures.

Never expose secrets. Never invent package identifiers, release assets, workflow capabilities, branch names, hosted URLs, or security guarantees.
