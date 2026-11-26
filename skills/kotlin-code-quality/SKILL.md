---
name: kotlin-code-quality
description: "Use when editing or reviewing Kotlin naming, conditionals, `when` expressions, classes, objects, data classes, equality, nullability, preconditions, strings, regular expressions, collections, sequences, coroutines, `Flow`, dispatchers, JDBC, Guava, Gradle Kotlin DSL build scripts, or analyser diagnostics, and to apply the complete Kotlin rule catalogue: naming and layout, control structures, types and inheritance, members and parameters, exceptions and resources, strings and regular expressions, collections and sequences, concurrency and coroutines, platform APIs, and build scripts. Preserves equality, nullability, structured-concurrency, and error-reporting requirements even without analyser diagnostics."
---

# Kotlin Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [coding instructions](../../instructions/common/common.coding.instructions.md), [naming instructions](../../instructions/common/common.naming.instructions.md), and [error-handling instructions](../../instructions/common/common.error-handling.instructions.md) for universal conventions and compatibility precedence. Load them if absent from context. Required external contracts and supported stable syntax take precedence; report exceptions rather than silently weakening a rule.

## Rule Catalogue

The `references/rules-*.md` files contain one directive per Kotlin quality and reliability rule (98 rules); the [security instructions](../../instructions/kotlin/kotlin.security.instructions.md) contain the 60 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations:
  - The naming rules for functions, classes, local variables, and parameters permit abbreviations and single-letter names; the naming instructions prohibit them, so apply both.
  - The vacant nested block rule exempts blocks that contain only a comment; the coding instructions require eliminating vacant conditionals, so delete comment-only conditional blocks as well.
  - The identical function implementation rule exempts functions with fewer than 2 statements; the coding instructions prohibit every duplicate implementation.
  - The rule against declaring a lambda parameter explicitly as `it` recommends the implicit `it`; the naming instructions require clear, explicit lambda parameter names, so declare a descriptive name instead.

| Concern | Threshold |
| --- | --- |
| Function names | Names conform to `^[a-zA-Z][a-zA-Z0-9]*$` |
| Class names | Names conform to `^[A-Z][a-zA-Z0-9]*$` |
| Local variable and parameter names | Names conform to ``^`?[_a-z][a-zA-Z0-9]*`?$`` |
| Function parameters | At most 7 parameters per function |
| Duplicated literals | A literal of 6 or more characters, not composed only of letters, digits, and `_`, repeated 3 or more times |
| Large `when` statements | At most 30 clauses |
| Cognitive Complexity | At most 15 per function |
| Chained `if` statements | Chains of 3 or more branches become `when` |
| Regular expression complexity | At most 20 per regular expression |
| Hardcoded credentials | Credential words `password`, `passwd`, `pwd`, and `passphrase` |
| Hardcoded secrets | Secret words `api[_.-]?key`, `auth`, `credential`, `secret`, and `token`; randomness sensitivity 3.0 |

| Topic | Reference |
| --- | --- |
| Naming patterns, imports, comments, `TODO`/`FIXME` tags, parentheses, lambda parameter names | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| Conditions, branches, `when`, jumps, assignments, boolean expressions, operators, Cognitive Complexity | [rules-control-structures.md](references/rules-control-structures.md) |
| Classes, interfaces, `fun interface`, objects, delegation, data classes, `equals`/`hashCode`, casts and type checks, deprecation | [rules-types-and-inheritance.md](references/rules-types-and-inheritance.md) |
| Functions, parameters, property accessors, indexed access, equality operators, null checks, unused members, dead stores | [rules-members-and-parameters.md](references/rules-members-and-parameters.md) |
| `finally`, preconditions, status values, finalisers | [rules-exceptions-and-resources.md](references/rules-exceptions-and-resources.md) |
| String literals, constants, regular expressions | [rules-strings-and-regular-expressions.md](references/rules-strings-and-regular-expressions.md) |
| Read-only and mutable collections, collection operations, arrays, maps, `Sequence` and `Stream` pipelines | [rules-collections-and-sequences.md](references/rules-collections-and-sequences.md) |
| Coroutines, scopes, dispatchers, `Flow`, `Deferred`, suspending functions, timeouts, executors | [rules-concurrency-and-coroutines.md](references/rules-concurrency-and-coroutines.md) |
| JDBC, Guava | [rules-platform-apis.md](references/rules-platform-apis.md) |
| Gradle tasks, settings, plugins, dependency declarations and versions | [rules-build-scripts.md](references/rules-build-scripts.md) |

## Verification

- Review every applicable section and rule reference, not just the reported diagnostic.
- Execute existing focused build, analyser, and regression checks for the changed code; retain Cognitive Complexity <= 15 and parameter counts <= 7, and functions of approximately 20-30 lines under the coding instructions.
- Verify equality and hashing contracts, nullability, structured concurrency and coroutine cancellation, resource release, and exception semantics where affected. Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
