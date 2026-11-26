---
name: python-code-quality
description: "Use when editing or reviewing Python naming, control flow, classes, type hints, special methods, exceptions, string formatting, regular expressions, floating-point arithmetic, dates and time zones, collections, comprehensions, async code, Django, AWS Lambda and boto3, NumPy, pandas, scikit-learn, TensorFlow, PyTorch, PySpark, unittest, pytest, or analyser diagnostics, and to apply the complete Python rule catalogue: naming and layout, control structures, types and inheritance, members and parameters, exceptions and resources, strings, numbers, and dates, collections and comprehensions, concurrency and async, platform APIs, data science and machine learning, and tests. Preserves type, numeric, cancellation, resource-release, and error-reporting requirements even without analyser diagnostics."
---

# Python Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [coding instructions](../../instructions/common/common.coding.instructions.md), [naming instructions](../../instructions/common/common.naming.instructions.md), and [error-handling instructions](../../instructions/common/common.error-handling.instructions.md) for universal conventions and compatibility precedence, and the Python [coding instructions](../../instructions/python/python.coding.instructions.md) and [error-handling instructions](../../instructions/python/python.error-handling.instructions.md) for Python conventions. Load them if absent from context. Required external contracts and supported stable syntax take precedence; report exceptions rather than silently weakening a rule.

## Rule Catalogue

The `references/rules-*.md` files contain one directive per Python quality and reliability rule (278 rules); the [security instructions](../../instructions/python/python.security.instructions.md) contain the 86 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations:
  - The class naming rule permits snake_case class names; the coding instructions require PascalCase for every class.
  - The naming rules for methods, functions, fields, local variables, and parameters permit abbreviations and single-letter names; the naming instructions prohibit them, so apply both.
  - The class method first-parameter rule requires `cls`, `mcs`, or `metacls`, which are abbreviations; the naming instructions prohibit abbreviations, so use a descriptive name and report each deviation.
  - The string formatting rules cover `%` formatting and `str.format`; the coding instructions require f-strings for all interpolation, so apply those rules only to any remaining format strings.
  - The suppression comment syntax rule conflicts with the comment format in the coding instructions (an uppercase initial letter and a final period); suppression markers are a required external contract and prevail, so retain the tool syntax exactly and report each occurrence.

| Concern | Threshold |
| --- | --- |
| Method names | Names conform to `^[a-z_][a-z0-9_]*$` |
| Class names | Names conform to `^_?([A-Z_][a-zA-Z0-9]*\|[a-z_][a-z0-9_]*)$`, with PascalCase only locally |
| Field names | Names conform to `^[_a-z][_a-z0-9]*$` |
| Local variable and parameter names | Names conform to `^[_a-z][a-z0-9_]*$` |
| Function names | Names conform to `^[a-z_][a-z0-9_]*$` |
| Class method first parameter | `cls`, `mcs`, or `metacls`, with descriptive names locally |
| Instance method first parameter | `self`; methods decorated with `abstractmethod` exempt |
| Function parameters | At most 13 per function, method, and lambda |
| Duplicated literals | A literal of 5 or more characters repeated 3 or more times; literals within decorators and literals containing only letters, digits, and underscores exempt |
| Cognitive Complexity | At most 15 per function |
| Regular expression complexity | At most 20 per regular expression |
| Commented-out code | Comments corresponding to `(fmt\|py\w+):.*` exempt |
| Unused local variables | Names corresponding to `(_[a-zA-Z0-9_]*\|dummy\|unused\|ignored)` exempt |
| Unread private attributes | Double-underscore attributes only; single-underscore attributes exempt |
| Statements without effect | String statements unreported; operators `<<`, `>>`, and `\|` ignored |
| PySpark expressions | At most 5 nested calls and 5 comparisons per expression |
| f-string nesting | Fewer than 3 levels |
| pandas operation chains | `DataFrame.pipe` from 7 operations |
| Async sleep durations | `sleep_forever()` beyond 24 hours |
| Password salts | At least 16 bytes |
| Password hashing | PBKDF2 of at least 1,300,000 iterations for SHA-1, 600,000 for SHA-256, and 210,000 for SHA-512 |
| Cryptographic keys | RSA and DSA of at least 2048 bits; elliptic curves of at least 224 bits |
| Hardcoded credentials | Credential words `password`, `passwd`, `pwd`, and `passphrase` |
| Hardcoded secrets | Secret words `api[_.-]?key`, `auth`, `credential`, `secret`, and `token`; randomness sensitivity 3.0 |

| Topic | Reference |
| --- | --- |
| Naming patterns, first parameters, `__all__`, wildcard imports, parentheses, commented-out code, `TODO`/`FIXME` tags, suppression comments, Python 2 syntax | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| Conditions, branches, loops, jumps, assignments, boolean and conditional expressions, the walrus operator, recursion, Cognitive Complexity, unused variables | [rules-control-structures.md](references/rules-control-structures.md) |
| Type compatibility, identity comparisons, special methods, `NotImplemented`, overriding contracts, type hints, generics, type aliases, `None` access | [rules-types-and-inheritance.md](references/rules-types-and-inheritance.md) |
| Parameters and arguments, default values, unused members, vacant and duplicated functions, return values, closures in loops, method signatures | [rules-members-and-parameters.md](references/rules-members-and-parameters.md) |
| Raising and catching, `except` clauses, exception classes, `SystemExit`, `__exit__`, exception groups, `open()` modes | [rules-exceptions-and-resources.md](references/rules-exceptions-and-resources.md) |
| String literals and formatting, f-strings, template strings, regular expressions, floating-point comparison, division, `datetime`, time zones | [rules-strings-numbers-dates.md](references/rules-strings-numbers-dates.md) |
| Collection sizes and literals, dictionaries, sets, unpacking, indexing, comprehensions, generator expressions, collection constructors | [rules-collections-and-comprehensions.md](references/rules-collections-and-comprehensions.md) |
| asyncio, trio, and anyio timeouts, sleeps, blocking calls, cancellation, tasks, TaskGroups and Nurseries, asynchronous context managers | [rules-concurrency-and-async.md](references/rules-concurrency-and-async.md) |
| Django, AWS Lambda, CloudWatch, boto3 | [rules-platform-apis.md](references/rules-platform-apis.md) |
| NumPy, pandas, scikit-learn, TensorFlow, PyTorch, PySpark | [rules-data-science-and-machine-learning.md](references/rules-data-science-and-machine-learning.md) |
| unittest and pytest skipping, test discovery, assertions | [rules-tests.md](references/rules-tests.md) |

## Verification

- Review every applicable section and rule reference, not just the reported diagnostic.
- Execute existing focused test, type-check, analyser, and regression checks for the changed code; retain Cognitive Complexity <= 15 and parameter counts <= 13.
- Verify type contracts, numeric contracts, cancellation semantics, resource release, and exception semantics where affected. Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
