---
description: "Use when writing or editing any code. General coding rules: clean code, naming, comments, blank lines, indentation, British English, magic numbers, dead code, single responsibility, test design, regression coverage, edge cases, source control."
applyTo: "**/*.{c,cpp,cs,h,java,js,jsx,py,sh,ts,tsx}"
---

## General

- When editing code, actively refactor the affected areas to comply with all rules defined here; do not leave surrounding code in violation of these rules when you have touched that area.
- When refactoring, all public-facing contracts must remain 100% backwards compatible. This includes UI visuals, CLI interfaces, API contracts, library public APIs, serialised output formats, and any other surface that an end-user or external client directly interacts with or depends on. Internal restructuring must never alter observable behaviour. For NuGet packages and other APIs, use all existing unit tests to validate that no contract has been broken; if the tests pass, the change is safe to proceed.
- Respect the existing coding style in each repository, including file naming, splitting, and structure conventions.
- Default timestamp format should be: "yyyy'-'MM'-'dd'T'HH':'mm':'ss.fffffffK".
- Always treat file and directory paths as case-sensitive, even on Windows, to ensure cross-platform compatibility.
- Always write code that handles both LF (`\n`) and CRLF (`\r\n`) line endings. Never assume a single newline style.
- All files must end with an empty line.
- Every class, file, and module must have a single, well-defined responsibility. Place methods and functions only in the class that owns that responsibility. Never create multi-responsibility buckets or utility dumping-grounds. When a class begins to serve more than one concern, split it immediately into separate, focused classes, each placed in the namespace or module that corresponds to its responsibility.
- Do not create catch-all `Helpers`, `Utils`, `Common`, `Misc`, or `Shared` modules or namespaces. Assign each type to the domain or responsibility it serves.
- Do not leave empty placeholder classes or types. Every type must have a concrete purpose and at least one meaningful member, behaviour, or contract.
- Always remove dead code, unused imports, unused variables, redundant assignments, unused methods, obsolete fields, empty `if` blocks (conditionals with no logic inside their braces), and any other artefacts that serve no purpose.
- After every edit, explicitly check for and remove any imports or `using` directives that are no longer referenced. This is MANDATORY and must never be skipped, even when the change seems unrelated to imports.
- Never use magic numbers or magic strings. Use enums for categorical values and named constants for all other fixed values.
- When an object has a "type" or "variant" (e.g. which button, which icon, etc.), always model it with an enum property, not an `int` index. The enum name should describe the category (e.g. `ButtonType`), and its values should be the specific variants (e.g. `Undo`, `Restart`, `Info`, `Settings`).
- In every model, data object, entity, DTO, and analogous structured object, declare the primary identifier property first, before every other property. Use the object's established identifier name, such as `Identifier` or `Id`; when multiple identifiers exist, declare the primary identifier first and the remaining identifiers immediately afterwards.
- Screen coordinates, sizes, and all layout measurements must be dynamic and relative, derived from screen size, container dimensions, or other already-computed layout values. Never hardcode pixel positions or dimensions.
- Avoid code duplication. Always extract and reuse existing logic whenever it is reasonable to do so; never copy-paste code blocks, repeat the same expression in multiple places, or re-implement logic that already exists elsewhere. When making changes in an area of code, actively look for and eliminate any existing duplication in that area as part of the same change.
- Keep methods and functions small and focused on a single responsibility. If a method grows beyond ~20-30 lines or handles more than one logical concern, extract the extra logic into well-named private helper methods or utility functions.
- Never leave unreachable statements after an unconditional `return`, `throw`, `continue`, `break`, or exhaustive pattern match/switch expression. These are always logic errors.
- Follow clean code principles, avoid design anti-patterns, and use suitable design patterns for scalable, reviewable, understandable, and well-organised code.
- Write code that is as descriptive as reasonably possible. Prefer intention-revealing names for types, methods, functions, variables, constants, parameters, files, and directories so the code explains what it does, why it exists, and how it is meant to be used without requiring extra explanation. Favour clarity over brevity, except where a short name is already an established and unambiguous convention.
- Use British English spelling in code and related text. Prefer latinate English words where possible (e.g. "necessary" instead of "needed"). Key spelling differences: `normalise` (not `normalize`), `serialise` (not `serialize`), `initialise` (not `initialize`), `colour` (not `color`), `behaviour` (not `behavior`), `centre` (not `center`), `licence` (not `license` for the noun), `recognise` (not `recognize`), `synchronise` (not `synchronize`). Apply this to all identifiers, method names, comments, and strings.
- Keep code self-explanatory and avoid comments unless they are exceptional and genuinely useful. This rule does NOT apply to XML documentation comments (`/// <summary>`) in NuGet packages, which are mandatory and must never be removed.
- Always place at least one space after `//` at the start of a comment: `// text`, never `//text`.
- Inline and block comments must always begin with an uppercase letter and end with a period: `// Calculates the wall distance.`
- TODO comments must always use the exact format `// TODO: Description.` (uppercase TODO, colon, space, sentence ending with period).
- Never use tabs for indentation; always use 4 spaces per indent level.
- Never use two or more consecutive blank lines anywhere in the code.
- Do not use redundant parentheses. Only add parentheses when they are required to override operator precedence or to clarify a genuinely ambiguous expression.
- Licence new projects under GPL v3 unless the repository already uses a different licence.
- Use proper grammar in all text, including log messages, test names, comments, and user-facing strings (for example: "Appends the `sdkInitialisationKey` with ...", "when the endpoint already ...", "Already has a query string", "Added Dispose() in the factory.", "The session token retrieval has failed"), instead of variants that omit "the", "has", "a", "an", etc.
- Never use characters or phrasing that indicate AI-generated content. This includes em dashes (`—`), en dashes (`–`), ellipsis characters (`…`), arrow characters (`→`), box-drawing characters, and overly verbose transitional phrases such as "it is worth noting", "it is important to", "in order to", "this ensures that", "as mentioned above". Use plain ASCII punctuation (`,`, `;`, `:`, `-`, `->`) and direct phrasing instead. Emojis are allowed in user-facing strings and the readme.

## Testing

- Whenever writing or editing code, if a test project or test files exist, add or revise tests for every affected behaviour as part of the same change. Do not limit coverage to the primary success case.
- Derive test cases from the observable contract, domain invariants, control-flow branches, and changed lines. Cover every reachable conditional result, guard clause, state transition, exception, fallback, and externally visible side effect.
- For each numeric, temporal, length, or range boundary, test the value immediately below the boundary, the boundary itself, and the value immediately above it whenever those values are representable and relevant.
- Cover applicable input classes, including absent and null values, empty values, single and multiple elements, zero and negative values, minimum and maximum values, overflow, duplicates, ordering variations, whitespace, casing, Unicode, malformed data, and unusually large inputs. Only test invalid values that can reach the tested boundary or that the contract explicitly rejects.
- Test significant interactions between conditions, not only each condition in isolation. Prioritise combinations involving multiple boundaries, partial failures, repeated invocation, stale state, retries, cancellation, timeouts, and dependency failures when the production behaviour supports them.
- Every defect correction must include a regression test that fails without the correction and passes with it. Exercise the public or observable boundary nearest to the defect.
- Assert the complete observable result: returned values, errors, state changes, persisted data, emitted events, dependency calls, and the absence of prohibited side effects. Each assertion must be capable of detecting a plausible regression; do not test implementation details, framework internals, or trivial accessors.
- Use parameterised tests when several inputs exercise identical behaviour. Use separate tests when setup, expected behaviour, failure diagnostics, or control flow differs. Every case must add distinct defect-detection value; never add duplicate cases solely to increase the test count.
- Aim for complete branch coverage of affected code, then inspect uncovered lines and branches. Coverage metrics identify omissions but do not replace behavioural assertions or edge-case analysis. Any intentionally untested reachable branch must have a concrete justification.
- Keep tests deterministic and isolated. Control time, randomness, locale, environment variables, scheduling, and external dependencies when relevant; do not depend on real network services, real delays, execution order, or state left by another test.

## README

- When the user asks to update or create a `README.md` (e.g. "update the readme", "create a readme", "generate the readme"), always follow the template and rules defined in `github-readme.prompt.md`.
- After every code change, check whether the `README.md` requires updating to reflect the change. If it does, update it as part of the same change.

## Source Control

- Default branch name: `master`.
- Merge strategy: default (no fast-forward flags or special strategies unless the repository already specifies otherwise).
- Pull strategy: rebase (`git pull --rebase`).
