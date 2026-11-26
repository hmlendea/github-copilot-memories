---
name: java-code-quality
description: "Use when editing or reviewing Java naming, control flow, classes, equality, generics, records, exceptions, try-with-resources, strings, regular expressions, numeric arithmetic, dates, collections, streams, concurrency, logging, serialisation, Spring, AWS SDK, JUnit, AssertJ, Mockito, reflection, or analyser diagnostics, and to apply the complete Java rule catalogue: naming and layout, control structures, types and inheritance, members and parameters, exceptions and resources, strings, numbers, and dates, collections and streams, concurrency and threads, logging and diagnostics, platform APIs, interop and reflection, and tests. Preserves equality, numeric, resource-release, thread-safety, and error-reporting requirements even without analyser diagnostics."
---

# Java Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [coding instructions](../../instructions/common/common.coding.instructions.md), [naming instructions](../../instructions/common/common.naming.instructions.md), and [error-handling instructions](../../instructions/common/common.error-handling.instructions.md) for universal conventions and compatibility precedence. Load them if absent from context. Required external contracts and supported stable syntax take precedence; report exceptions rather than silently weakening a rule.

## Rule Catalogue

The `references/rules-*.md` files contain one directive per Java quality and reliability rule (481 rules); the [security instructions](../../instructions/java/java.security.instructions.md) contain the 94 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations:
  - The rule to log or rethrow a caught exception, never both, conflicts with the log-and-rethrow policy; retain the local policy and report each occurrence.
  - The naming rules for methods, classes, interfaces, constants, fields, `static` non-`final` fields, local variables, parameters, and packages permit abbreviations and single-letter names; the naming instructions prohibit them, so apply both.
  - The type parameter naming rule requires a single capital letter, optionally followed by a digit; the naming instructions prohibit single-letter names, so use descriptive type parameter names and report each deviation.
  - The package naming rule permits catch-all packages; the coding instructions prohibit `Helpers`, `Utils`, `Common`, `Misc`, and `Shared` packages.
  - The brain method rule tolerates methods of up to 65 lines of code; the coding instructions limit methods to approximately 20-30 lines.
  - The rule grouping similar tests into parameterised tests is subordinate to the coding instructions, which permit parameterisation only for identical behaviour.
  - The rule permitting either spaces or tabs for text block indentation is subordinate to the coding instructions, which prohibit tabs for indentation.

| Concern | Threshold |
| --- | --- |
| Method names | Names conform to `^[a-z][a-zA-Z0-9]*$` |
| Class names | Names conform to `^[A-Z][a-zA-Z0-9]*$` |
| Interface names | Names conform to `^[A-Z][a-zA-Z0-9]*$` |
| Constant names | Names conform to `^[A-Z][A-Z0-9]*(_[A-Z0-9]+)*$` |
| Field names | Names conform to `^[a-z][a-zA-Z0-9]*$` |
| `static` non-`final` field names | Names conform to `^[a-z][a-zA-Z0-9]*$` |
| Local variable and parameter names | Names conform to `^[a-z][a-zA-Z0-9]*$` |
| Type parameter names | Names conform to `^[A-Z][0-9]?$`, with descriptive names locally |
| Package names | Names conform to `^[a-z_]+(\.[a-z_][a-z0-9_]*)*$` |
| Test class names | Names conform to `^((Test\|IT)[a-zA-Z0-9_]+\|[A-Z][a-zA-Z0-9_]*(Test\|Tests\|TestCase\|IT\|ITCase))$` |
| Test class detection | Classes whose names correspond to `.*(Test\|Tests\|TestCase)` contain at least one test |
| Method parameters | At most 7 parameters per method and per constructor |
| Inheritance | Inheritance depth at most 5 |
| Class coupling | Dependencies on at most 20 other classes |
| Duplicated literals | A literal of 5 or more characters repeated 3 or more times |
| Large `switch` statements | At most 30 `case` clauses |
| Cognitive Complexity | At most 15 per method |
| Brain methods | Never simultaneously above 65 lines of code, cyclomatic complexity 15, nesting depth 3, and 7 accessed variables; approximately 20-30 lines per method locally |
| Regular expression complexity | At most 20 per regular expression |
| Regular expression stack consumption | Stack consumption factor at most 5.0 |
| Text blocks in lambdas | At most 5 lines |
| Tabs in literals | Literal tabs prohibited, including in text blocks |
| Assertions per test | At most 25 per test method |
| Request size | File uploads at most 8,388,608 bytes; other requests at most 2 MB |
| Hardcoded credentials | Credential words `password`, `passwd`, `pwd`, `passphrase`, and `java.naming.security.credentials` |
| Hardcoded secrets | Secret words `api[_.-]?key`, `auth`, `credential`, `secret`, and `token`; randomness sensitivity 5.0 |

| Topic | Reference |
| --- | --- |
| Naming patterns, braces, modifiers, imports, comments, `TODO`/`FIXME` tags, packages, array designators | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| Conditions, branches, loops, `switch`, labels, jumps, assignments, boolean expressions, Cognitive Complexity, brain methods | [rules-control-structures.md](references/rules-control-structures.md) |
| Classes, inheritance, `equals`/`hashCode`/`compareTo`, `clone`, deprecation, generics, casts, `instanceof` patterns, records, sealed types, enums | [rules-types-and-inheritance.md](references/rules-types-and-inheritance.md) |
| Fields, methods, parameters, lambdas, method references, `static` members, nullability annotations, unused members, return values | [rules-members-and-parameters.md](references/rules-members-and-parameters.md) |
| Throwing, catching, exception types, `throws` clauses, `finally`, try-with-resources, I/O streams, finalisers, file deletion | [rules-exceptions-and-resources.md](references/rules-exceptions-and-resources.md) |
| String literals and operations, `StringBuilder`, format strings, regular expressions, numeric arithmetic and conversions, `BigDecimal`, `Random`, date-time patterns | [rules-strings-numbers-dates.md](references/rules-strings-numbers-dates.md) |
| Collection types and contracts, maps, arrays, iteration, `Stream` pipelines, gatherers, sequenced collections | [rules-collections-and-streams.md](references/rules-collections-and-streams.md) |
| `synchronized`, locks, `wait`/`notify`, threads, executors, `ThreadLocal`, atomics, lazy initialisation | [rules-concurrency-and-threads.md](references/rules-concurrency-and-threads.md) |
| Logger creation, standard output, eager argument evaluation, `assert` | [rules-logging-and-diagnostics.md](references/rules-logging-and-diagnostics.md) |
| Serialisation, JDBC, Spring beans, injection, controllers, transactions, caching, AWS SDK and Lambda, Guava | [rules-platform-apis.md](references/rules-platform-apis.md) |
| `sun.*` packages, garbage collection calls, reflection, JDBC driver loading, the Class-File API | [rules-interop-and-reflection.md](references/rules-interop-and-reflection.md) |
| JUnit, TestNG, AssertJ, Mockito, Spring test contexts, assertions, deactivated tests, test naming | [rules-tests.md](references/rules-tests.md) |

## Verification

- Review every applicable section and rule reference, not just the reported diagnostic.
- Execute existing focused build, analyser, and regression checks for the changed code; retain Cognitive Complexity <= 15 and parameter counts <= 7, and methods of approximately 20-30 lines under the coding instructions.
- Verify equality and hashing contracts, resource release, thread safety, numeric contracts, serialisation, and exception semantics where affected. Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
