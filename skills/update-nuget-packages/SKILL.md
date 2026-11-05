---
name: update-nuget-packages
description: Use when updating NuGet package dependencies in a .NET solution or project. Runs test baselines when tests exist, updates every referenced package to the latest version project by project, and validates and repairs the final result.
---

# Update NuGet Packages

## 1. Discover The Target

- Inspect the repository root for `.sln`, `.slnx`, and `.csproj` files.
- If exactly one solution exists, use it as the target and enumerate its projects with `dotnet sln <solution> list`.
- If no solution exists and exactly one project exists, use that project as the target.
- If multiple solutions or standalone projects make the target ambiguous, ask which target to update; do not guess.
- Exclude generated, `bin`, and `obj` paths.
- Preserve the current working tree. Do not discard unrelated changes.

## 2. Establish The Test Baseline

- Determine whether tests exist before running tests. Treat a project as a test project when its project file references a test SDK or test framework, or when it contains test source files.
- If tests exist, run `dotnet test <solution-or-project>` for the complete target before changing package references.
- If the baseline fails, record the command and distinct diagnostics, report that the baseline is failing, and stop. Do not attribute those failures to package updates.
- If no tests exist, explicitly record that the test steps were skipped.

## 3. Update Every Project

- Process solution projects sequentially, one project at a time. For a single-project target, process only that project.
- Read each project's `.csproj` and collect every explicit `PackageReference` `Include` value. Ignore project references, framework references, and package references excluded by a false condition.
- For each collected package ID, run `dotnet add <project> package <package-id>` without `--version`; the default is the latest version available from the configured NuGet sources.
- Run each package command from the repository root, preserve the project's existing package source configuration, and wait for success before continuing.
- If a package update fails, capture the diagnostic, repair only the relevant project/configuration issue, and rerun that command. Stop and report if the failure cannot be resolved safely.
- Account for central package management (`Directory.Packages.props`) and verify that each command actually changed or confirmed the effective package version; do not duplicate version declarations.
- Review the diff after each project and retain intentional project-file and lock-file changes only.

## 4. Validate And Repair

- After all package updates complete, if tests exist, run `dotnet test <solution-or-project>` for the complete target again.
- If final tests fail, classify each failure and fix the affected production code or tests as appropriate; do not weaken or delete tests merely to make them pass.
- Re-run the complete target test after every repair until it passes or a safe repair is not possible.
- Check the final diff for unintended changes, package downgrades, duplicate references, leaked credentials, and generated artifacts.
- Report the target, projects processed, packages updated, test commands and outcomes, repairs made, and any unresolved blockers.
