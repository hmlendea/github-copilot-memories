---
description: "Use when writing or editing any code. General coding rules: clean code, naming, comments, blank lines, indentation, British English, magic numbers, dead code, single responsibility, test design, regression coverage, edge cases, source control."
applyTo: "**/*.{c,cpp,cs,h,java,js,jsx,py,sh,ts,tsx}"
---

## General

- Touched code and its affected area must comply with these rules.
- Refactors must preserve every observable contract, including UI, CLI, API, public library API, and serialised formats. Existing NuGet/API tests must pass.
- Preserve repository file naming, splitting, structure, and coding style.
- Default timestamp: `yyyy'-'MM'-'dd'T'HH':'mm':'ss.fffffffK`.
- Treat paths as case-sensitive on every operating system.
- Handle both LF (`\n`) and CRLF (`\r\n`).
- All files must end with an empty line.
- Each class, file, and module has one responsibility. Place logic with its owner; split mixed concerns into focused types in the corresponding namespace or module.
- No catch-all `Helpers`, `Utils`, `Common`, `Misc`, or `Shared` modules/namespaces; assign each type to its domain or responsibility.
- No empty placeholder types; every type requires a concrete purpose and meaningful member, behaviour, or contract.
- Remove dead or unreachable code, unused imports/variables/methods/fields, redundant assignments, and empty conditionals. Check imports after every edit.
- Never use magic numbers or magic strings. Use enums for categorical values and named constants for all other fixed values.
- When an object has a "type" or "variant" (e.g. which button, which icon, etc.), always model it with an enum property, not an `int` index. The enum name should describe the category (e.g. `ButtonType`), and its values should be the specific variants (e.g. `Undo`, `Restart`, `Info`, `Settings`).
- In every model, data object, entity, DTO, and analogous structured object, declare the primary identifier property first, before every other property. Use the object's established identifier name, such as `Identifier` or `Id`; when multiple identifiers exist, declare the primary identifier first and the remaining identifiers immediately afterwards.
- Screen coordinates, sizes, and all layout measurements must be dynamic and relative, derived from screen size, container dimensions, or other already-computed layout values. Never hardcode pixel positions or dimensions.
- Reuse existing logic; no copied blocks, repeated expressions, or duplicate implementations. Eliminate duplication in the affected area.
- Methods/functions: one concern and approximately 20-30 lines maximum; extract additional logic into named private functions.
- No statements after unconditional `return`, `throw`, `continue`, `break`, or exhaustive pattern/switch.
- Follow clean code principles, avoid design anti-patterns, and use suitable design patterns for scalable, reviewable, understandable, and well-organised code.
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

- Changed code: when tests exist, add or revise tests for every affected behaviour. Every defect correction requires a regression test.
- Cover observable contracts and relevant success/failure paths, branches, boundaries, input classes, interactions, and side effects. Assert complete results and prohibited-side-effect absence.
- Tests must be distinct, deterministic, and isolated. Parameterise only identical behaviour. Aim for complete affected branch coverage; justify omissions.
- Use the `test-design` skill for detailed case derivation.

## Source Control

- Default branch name: `master`.
- Merge strategy: default (no fast-forward flags or special strategies unless the repository already specifies otherwise).
- Pull strategy: rebase (`git pull --rebase`).
