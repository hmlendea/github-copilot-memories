---
name: csharp-code-quality
description: "Use when editing or reviewing C# strings, StringBuilder, JSON options, regexes, reusable arrays, URI composition, enum values, controller input binding, parsing, exceptions, guards, option validation, dictionary lookups, or analyser diagnostics, and to apply the complete C# rule catalogue: naming, layout, control structures, types, inheritance, members, parameters, disposal, numbers, dates, collections, LINQ, concurrency, async, logging, platform APIs, interop, reflection, and tests. Preserves allocation, numeric-contract, binding, and error-reporting requirements even without analyser warnings."
---

# C# Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [coding instructions](../../instructions/csharp/csharp.coding.instructions.md) for universal conventions, thresholds, and compatibility precedence. Load them if absent from context. Required external contracts and supported stable syntax take precedence; report exceptions rather than silently weakening a rule.

## Strings And Reusable Objects

- Prefer `string.StartsWith(char)` / `string.EndsWith(char)` for single-character checks when semantics and API support agree.
- Use `StringBuilder` for iterative or large incremental string operations when it offers a significant performance advantage. Prefer a simpler, clearer string operation for minor one-off compositions.
- Reuse `JsonSerializerOptions`: one `static readonly` instance per configuration for repeated serialisation, including tests; no allocation per operation or test execution. Complete configuration prior to first use; do not mutate shared options between tests.
- Use `GeneratedRegex` for constant patterns when supported by the generator and configured stable SDK. Its required `partial` declarations are permitted. For unsupported generation or other repeated patterns, reuse a `Regex` instance; preserve pattern, options, and timeout semantics.
- Repeated non-mutated array arguments use `static readonly` fields. Verify consumers do not mutate or retain them for mutation; `readonly` protects the field reference, not array elements.
- Prefer `TryGetValue` over `ContainsKey` plus an indexer; its required `out` argument is permitted.

## URI, Enum And Controller Contracts

- No URI path separators embedded at call sites: use URI APIs or a named URI-specific separator, never a platform filesystem separator. Preserve escaping, relative/absolute resolution, and trailing-separator semantics.
- Enum numeric values are unique unless an alias preserves a persisted/serialised contract. Intentional aliases require a narrowly scoped `CA1069` suppression, compatibility rationale, and regression tests pinning the numeric contract; never renumber persisted values merely to silence diagnostics. Also apply [csharp-enumerations](../csharp-enumerations/SKILL.md) for enumeration changes.
- Bind ASP.NET controller inputs with explicit binding attributes rather than extracting values directly from `Request` / `HttpContext.Request`. This governs input binding, not legitimate access to request metadata or cancellation.

## Control Flow And Performance

- Prefer sequential guard clauses for independent preconditions and cohesive named predicates when a long compound condition obscures intent. Preserve short-circuit order and semantics.
- In loops, use `continue` guards for per-item exclusions rather than nesting the remaining body. Do not assume `foreach` plus `if` is inefficient or replace it with LINQ/materialisation solely to remove the conditional; hoist loop-invariant checks only when semantics are unchanged.

## Parsing, Exceptions And Option Validation

- No empty `catch` blocks. Expected parse failure uses an explicit, checked result or a sanitised exception; never substitute success-like defaults. Prefer `TryParse`-style APIs over exception-driven parsing.
- Preserve the [exception policy](../../instructions/csharp/csharp.error-handling.instructions.md): prefer BCL exceptions; create a custom type only when no BCL exception fits. If required, custom exceptions must be accessible to their mappers and consumers. When catching to log and rethrow, log securely and use `throw;` without altering the exception.
- For null arguments, prefer `ArgumentNullException.ThrowIfNull` when supported by the target framework, or the existing project guard helper. Otherwise use `ArgumentNullException` with the genuine parameter name; do not define a custom exception or subclass a guard utility for null validation.
- Apply the [argument-guard policy](../../instructions/csharp/csharp.error-handling.instructions.md#argument-guards): prefer supported BCL or existing project guards whenever their predicate, validation order, exception type, parameter name and diagnostics fit. Reuse domain-specific guards for cohesive policy checks; retain explicit validation when compatible guards are unavailable.
- Inspect automatic guard messages for sensitive-value exposure. Preserve bounded, non-sensitive diagnostics and central string or invariant-culture interpolated messages; do not catch and replace a guard exception for message formatting or introduce a package or exception subclass solely for brevity.
- Never invent an unused parameter merely to supply exception `ParamName`. Name a real argument only when that argument is invalid; identify the invalid option and value in the message, masking sensitive values per the [security instructions](../../instructions/csharp/csharp.security.instructions.md).

## Rule Catalogue

The `references/rules-*.md` files contain one directive per C# quality and reliability rule (297 rules); the [security instructions](../../instructions/csharp/csharp.security.instructions.md) contain the 70 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations:
  - The rule to log or rethrow a caught exception, never both, conflicts with the log-and-rethrow policy; retain the local policy and report each occurrence.
  - The rule against nested `?:` operators is less strict than the coding instructions, which prohibit `?:` entirely.
  - The rule preferring indexer access over LINQ element methods applies only where the static type is a list or array; collection contracts remain `IEnumerable<T>`.
  - The logger naming rule permits an underscore prefix; the naming instructions prohibit it.
  - The rule prescribing `IHttpClientFactory` does not apply to hmlendea repositories, which use NuciWeb.HTTP.
  - The rule permitting `ActionResult<T>` yields to the controller instructions, which require non-generic `ActionResult`; document response types with `[ProducesResponseType]`.

| Concern | Threshold |
| --- | --- |
| Method parameters | At most 7 parameters |
| Inheritance | Inheritance depth at most 5 |
| Duplicated literals | A literal of 5 or more characters repeated 3 or more times |
| Large `switch` statements | One statement per section in a `switch` with more than 30 sections |
| Generic type parameters | At most 2 type parameters per type and 3 per method |
| Cognitive Complexity | At most 15 per method and 3 per property accessor |
| Logging volume | Per code block at most 4 debug, 2 information, 1 warning, and 1 error logging calls |
| Request body size | Request bodies at most 8,000,000 bytes |
| Enumeration names | Names conform to `^([A-Z]{1,3}[a-z0-9]+)*([A-Z]{2})?$`; `[Flags]` names append `s` |
| Logger names | Names conform to `^_?[Ll]og(ger)?$`, without the underscore locally |

| Topic | Reference |
| --- | --- |
| Naming, braces, layout, comments, `TODO`/`FIXME` tags, namespaces | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| Conditions, branches, loops, `switch`, jumps, assignments, null dereferences, Cognitive Complexity | [rules-control-structures.md](references/rules-control-structures.md) |
| Classes, inheritance, equality, operators, casts, type checks, generics, attributes | [rules-types-and-inheritance.md](references/rules-types-and-inheritance.md) |
| Fields, properties, methods, parameters, overloads, caller-information attributes, events, delegates, unused members | [rules-members-and-parameters.md](references/rules-members-and-parameters.md) |
| Throwing, catching, exception types, argument validation, `IDisposable`, finalisers, streams | [rules-exceptions-and-disposal.md](references/rules-exceptions-and-disposal.md) |
| String literals, formatting, URIs, regular expressions, numeric arithmetic, `Guid`, `DateTime`, time zones | [rules-strings-numbers-dates.md](references/rules-strings-numbers-dates.md) |
| Collection returns, counts, indexers, LINQ, ordering | [rules-collections-and-linq.md](references/rules-collections-and-linq.md) |
| Locks, threads, `async`/`await`, `Task`, `ValueTask`, `ConcurrentDictionary` | [rules-concurrency-and-async.md](references/rules-concurrency-and-async.md) |
| Logger calls, message templates, logger naming and injection, `Trace`, `Debug.Assert` | [rules-logging-and-diagnostics.md](references/rules-logging-and-diagnostics.md) |
| ASP.NET Core controllers and routing, `HttpClient`, Blazor, Azure Functions, WCF, MEF, Windows Forms, serialisation, Entity Framework | [rules-platform-apis.md](references/rules-platform-apis.md) |
| P/Invoke, `SafeHandle`, assembly loading and versioning, reflection | [rules-interop-and-reflection.md](references/rules-interop-and-reflection.md) |
| Test classes and methods, assertions, ignored tests | [rules-tests.md](references/rules-tests.md) |

## Verification

- Review every applicable section and rule reference, not just the reported diagnostic.
- Execute existing focused build, analyser, and regression checks for the changed code; retain Cognitive Complexity <= 15 and parameter counts <= 7 under the coding instructions.
- Verify allocation reuse, mutation isolation, equality/numeric contracts, binding, cancellation, and exception semantics where affected. Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
