---
description: "Use for code edits. Covers shared structure, style, comments, testing, compatibility, and cleanup."
applyTo: "**/*.{c,cpp,cs,h,java,js,jsx,ms,msa,py,sh,ts,tsx}"
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
- No magic values: enums for categories; named constants otherwise.
- Type/variant properties use descriptive enums, never integer indices (e.g. `ButtonType`: `Undo`, `Restart`, `Info`, `Settings`).
- Structured objects: primary identifier (`Identifier`, `Id`, etc.) first, followed by remaining identifiers.
- Layout measurements are dynamic and relative to screen, container, or computed values; no hardcoded pixels.
- Reuse existing logic; no copied blocks, repeated expressions, or duplicate implementations. Eliminate duplication in the affected area.
- Methods/functions: one concern and approximately 20-30 lines maximum; extract additional logic into named private functions.
- No statements after unconditional `return`, `throw`, `continue`, `break`, or exhaustive pattern/switch.
- Follow clean code principles, avoid design anti-patterns, and use suitable design patterns for scalable, reviewable, understandable, and well-organised code.
- Prefer self-explanatory code; comments only when exceptionally useful. NuGet XML documentation (`/// <summary>`) remains mandatory.
- Always place at least one space after `//` at the start of a comment: `// text`, never `//text`.
- Inline and block comments must always begin with an uppercase letter and end with a period: `// Calculates the wall distance.`
- TODO comments must always use the exact format `// TODO: Description.` (uppercase TODO, colon, space, sentence ending with period).
- Never use tabs for indentation; always use 4 spaces per indent level.
- Never use two or more consecutive blank lines anywhere in the code.
- Do not use redundant parentheses. Only add parentheses when they are required to override operator precedence or to clarify a genuinely ambiguous expression.
- All text uses complete grammar, including articles and auxiliaries in logs, tests, comments, and user strings.
- No AI-styled em/en dashes, ellipsis/arrow/box-drawing characters, or verbose transitions. Use direct phrasing and ASCII punctuation (`,`, `;`, `:`, `-`, `->`). User strings and README may contain emojis.
- Use the `repository-defaults` skill for repository creation, licensing, branching, merging, and pulling.

## Testing

- Changed code: when tests exist, add or revise tests for every affected behaviour. Every defect correction requires a regression test.
- Cover observable contracts and relevant success/failure paths, branches, boundaries, input classes, interactions, and side effects. Assert complete results and prohibited-side-effect absence.
- Tests must be distinct, deterministic, and isolated. Parameterise only identical behaviour. Aim for complete affected branch coverage; justify omissions.
- Use the `test-design` skill for detailed case derivation.
