---
name: shell-code-quality
description: "Use when editing or reviewing Shell scripts for function and variable naming, TODO comments, conditional tests, case default clauses, self-assignments, identical operands, positional parameters, explicit returns, duplicated string literals, error messages on stderr, glob expansion, package manager consent flags, command substitution, or analyser diagnostics, and to apply the complete Shell rule catalogue: naming, layout, and comments, control structures, functions and variables, strings, numbers, and dates, logging and diagnostics, and commands and packages. Preserves predictable exit statuses and non-interactive execution even without analyser diagnostics."
---

# Shell Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [Shell coding instructions](../../instructions/shell/shell.coding.instructions.md), [Shell naming instructions](../../instructions/shell/shell.naming.instructions.md), and [Shell error-handling instructions](../../instructions/shell/shell.error-handling.instructions.md) for local Shell conventions, and the [common coding instructions](../../instructions/common/common.coding.instructions.md) for universal conventions and compatibility precedence. Load them if absent from context. Required external contracts take precedence; report exceptions rather than silently weakening a rule.

## Rule Catalogue

The `references/rules-*.md` files contain one directive per Shell quality and reliability rule (16 rules); the [security instructions](../../instructions/shell/shell.security.instructions.md) contain the 7 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations:
  - The variable naming rule requires lower_case names for local variables; the naming instructions require uppercase names for every variable, so retain uppercase local variables and report each occurrence.
  - The rule requiring `[[ ]]` for conditional tests exempts scripts that explicitly require POSIX compatibility; the coding instructions require `[[ ]]` for all conditional tests, so the exemption does not apply; report each such script.

| Concern | Threshold |
| --- | --- |
| Duplicated literals | A string literal repeated 3 or more times |

| Topic | Reference |
| --- | --- |
| Function and variable naming, `TODO` comments | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| Nested `if` merging, `case` default clauses, `[[ ]]` conditional tests, self-assignment, identical operands | [rules-control-structures.md](references/rules-control-structures.md) |
| Positional parameters, explicit `return` statuses, unused local variables | [rules-functions-and-variables.md](references/rules-functions-and-variables.md) |
| Duplicated string literals and `readonly` constants | [rules-strings-numbers-dates.md](references/rules-strings-numbers-dates.md) |
| Error messages on stderr | [rules-logging-and-diagnostics.md](references/rules-logging-and-diagnostics.md) |
| Glob expansion, package manager consent flags, command substitution | [rules-commands-and-packages.md](references/rules-commands-and-packages.md) |

## Verification

- Review every applicable section and rule reference, not just the reported diagnostic.
- Execute existing focused checks for the changed scripts, for example `bash -n` and any ShellCheck configuration the repository already uses.
- Verify exit statuses, error messages on stderr, non-interactive execution, and glob expansion where affected. Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
