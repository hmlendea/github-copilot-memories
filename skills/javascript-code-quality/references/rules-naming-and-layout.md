# JavaScript Rules: Naming And Layout

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Name classes per `^[A-Z][a-zA-Z0-9]*$` (Pascal case). **Local precedence:** The naming instructions additionally prohibit abbreviations and single-letter names; apply both.
- Delete commented-out code; retain only explanatory comments.
- Delete unused imports and unused imported bindings.
- Resolve every `FIXME` comment and delete it once resolved.
- Resolve every `TODO` comment and delete it once complete; format any interim one as `// TODO: Description.`
- Place the opening parenthesis of a call's argument list on the callee's line, never at the start of a subsequent line.
- Never use future reserved words (`implements`, `interface`, `package`, `private`, `protected`, `public`, `static`, `enum`, `await`, `yield`) as identifiers.
- Never bind or assign the special identifiers `eval`, `arguments`, `undefined`, `NaN`, and `Infinity`.
- Start the name of every function invoked with `new` with a capital letter.
- Enclose multi-line blocks in curly braces; never indent several statements under a brace-less `if`, `for`, or `while`.
- Declare every variable explicitly; never create implicit globals by assigning undeclared names.
- Never redeclare a variable or function within one scope.
- Declare variables with `let` or `const`, never `var`.
- Merge multiple imports from a single module into one `import` declaration.
- Place each `if` statement on its own line; never place it directly after the closing brace of a preceding `if` block without `else`.
- Never reassign imported bindings.
- Never rename import, export, or destructuring bindings to the identical name (`{ foo as foo }`, `{ foo: foo }`).
- Never use absolute file-system paths in imports; use relative paths or package names.
- Never export mutable bindings; export only `const` declarations, functions, and classes.
- Never import a module into itself.
- Name the specific rules in every ESLint suppression comment (`eslint-disable`, `eslint-disable-line`, `eslint-disable-next-line`); never suppress all rules at once. **Local precedence:** The coding instructions require comments to start with a capital letter and conclude with a period; suppression directives are a required external contract, so retain the tool syntax exactly and report each occurrence.
- Name default exports; never export an anonymous function, class, or arrow function as the default.
- Use the dedicated default syntax (`import foo from`, `export default`) rather than `import { default as foo }` or `export { foo as default }`.
- Re-export with `export … from` syntax rather than importing and then exporting.
- Import Node.js standard-library modules with the `node:` protocol (`import fs from 'node:fs'`).
- Never use vacant specifier lists in `import` or `export` declarations (`import {} from 'module'`, `export {}`); use a side-effect import (`import 'module'`) where intended.
- Align module dependencies with the intended architecture; never introduce a dependency the architecture prohibits.
- Locate each file in the directory the intended architecture prescribes.
- Eliminate each dependency that an architecture directive marks for elimination, to resolve dependency cycles.
