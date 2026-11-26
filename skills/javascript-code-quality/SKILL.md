---
name: javascript-code-quality
description: "Use when editing or reviewing JavaScript naming, modules and imports, control flow, classes and prototypes, functions and parameters, errors, regular expressions, numbers, dates, arrays, sets and maps, promises and async code, DOM and Node.js APIs, React and JSX, accessibility and ARIA, Mocha, Chai, and Jest tests, or analyser diagnostics, and to apply the complete JavaScript rule catalogue: naming and layout, control structures, types and inheritance, members and parameters, exceptions and errors, strings, numbers, and dates, collections and arrays, promises and async, platform APIs, React and JSX, accessibility, and tests. Preserves equality, promise-rejection, accessibility, and error-reporting requirements even without analyser diagnostics."
---

# JavaScript Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [coding instructions](../../instructions/common/common.coding.instructions.md), [naming instructions](../../instructions/common/common.naming.instructions.md), and [error-handling instructions](../../instructions/common/common.error-handling.instructions.md) for universal conventions and compatibility precedence, and the JavaScript [security instructions](../../instructions/javascript/javascript.security.instructions.md) for JavaScript security conventions. Load them if absent from context. Required external contracts and supported stable syntax take precedence; report exceptions rather than silently weakening a rule.

## Rule Catalogue

The `references/rules-*.md` files contain one directive per JavaScript quality and reliability rule (319 rules); the [security instructions](../../instructions/javascript/javascript.security.instructions.md) contain the 86 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations:
  - The class naming rule permits any name conforming to `^[A-Z][a-zA-Z0-9]*$`; the naming instructions additionally prohibit abbreviations and single-letter names, so apply both.
  - The suppression comment rule requires ESLint directive comments (`eslint-disable`, `eslint-disable-line`, `eslint-disable-next-line`) that name specific rules; the coding instructions require comments to start with a capital letter and conclude with a period. Suppression directives are a required external contract and prevail, so retain the tool syntax exactly and report each occurrence.

| Concern | Threshold |
| --- | --- |
| Class names | Names conform to `^[A-Z][a-zA-Z0-9]*$`, without abbreviations or single-letter names locally |
| Function parameters | At most 7 per function |
| `switch` size | At most 30 `case` clauses per `switch` statement |
| Function nesting | At most 4 levels |
| Cognitive Complexity | At most 15 per function |
| Regular expression complexity | At most 20 per regular expression |
| Constructor invocation | `new` only with functions and classes; JSDoc annotations disregarded |
| Getter returns | An explicit value in every getter path; implicit returns prohibited |
| JSX properties | Only recognised DOM properties and attributes; no additional permitted properties |
| Intrusive permissions | `geolocation` |
| Request size | At most 2,000,000 bytes for standard requests and 8,000,000 bytes for file uploads |
| Hardcoded credentials | Credential words `password`, `pwd`, `passwd`, and `passphrase` |
| Hardcoded secrets | Secret words `api[_.-]?key`, `auth`, `credential`, `secret`, and `token`; randomness sensitivity 5.0 |

| Topic | Reference |
| --- | --- |
| Class and constructor names, reserved words, commented-out code, `TODO`/`FIXME` tags, braces, variable declarations, imports and exports, `node:` imports, ESLint suppression comments, architecture dependencies | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| Blocks, `switch` clauses, loops and counters, jumps, labels, assignments, boolean, equality, and conditional expressions, optional chaining, unreachable code, Cognitive Complexity | [rules-control-structures.md](references/rules-control-structures.md) |
| Classes and private members, primitive wrappers, `new` and constructors, `this`, `super()`, `typeof` and `instanceof`, getters and setters, prototypes, `undefined` comparisons | [rules-types-and-inheritance.md](references/rules-types-and-inheritance.md) |
| Parameter counts and defaults, arguments, vacant and duplicated functions, unused variables, function nesting, return values and types, generators, `bind()`, `call()`, and `apply()` | [rules-members-and-parameters.md](references/rules-members-and-parameters.md) |
| `finally` jumps, caught exceptions, rethrowing, `Error` objects and messages, error parameter names, `TypeError` | [rules-exceptions-and-errors.md](references/rules-exceptions-and-errors.md) |
| Numeric literals, template literals, regular expressions, `NaN`, escape sequences, string methods, `Date`, `Math`, and `Number` APIs | [rules-strings-numbers-dates.md](references/rules-strings-numbers-dates.md) |
| Array indexes and lengths, `sort()` and `reverse()`, array callbacks, sparse arrays, spread syntax, `reduce()`, `find()`, `flat()`, `includes()`, `at()`, `Set` and `Map` | [rules-collections-and-arrays.md](references/rules-collections-and-arrays.md) |
| `await`, promise construction and rejection, unawaited promises, asynchronous constructors, `Promise.all()`, thenables, top-level `await` | [rules-promises-and-async.md](references/rules-promises-and-async.md) |
| Deprecated APIs, native function arguments, package exports, HTTP request bodies, polyfills, `Blob`, DOM methods, `dataset`, `globalThis`, `structuredClone()` | [rules-platform-apis.md](references/rules-platform-apis.md) |
| React `render()`, Hooks, state setters, JSX keys, conditions, comments, and fragments, Context values, `setState()`, prop types and defaults, refs, legacy lifecycle methods and APIs | [rules-react-and-jsx.md](references/rules-react-and-jsx.md) |
| Alternative text, keyboard equivalents, captions, `lang`, tables, ARIA roles and properties, `tabIndex`, focus, anchors, headings, labels, `autocomplete` | [rules-accessibility.md](references/rules-accessibility.md) |
| Skipped and exclusive tests, test cases and assertions, Chai chains, argument order, expected errors, retries, `done()`, Mocha timeouts | [rules-tests.md](references/rules-tests.md) |

## Verification

- Review every applicable section and rule reference, not just the reported diagnostic.
- Execute existing focused test, lint, analyser, and regression checks for the changed code; retain Cognitive Complexity <= 15, parameter counts <= 7, and function nesting <= 4.
- Verify equality semantics, promise rejection and error propagation, accessible markup, and exception semantics where affected. Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
