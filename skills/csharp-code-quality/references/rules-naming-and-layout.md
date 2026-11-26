# C# Rules: Naming, Layout And Comments

One directive per C# rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Name types in PascalCase; treat acronyms of more than two letters as words (for example `HtmlParser`, `IOStream`).
- Never commit commented-out code; delete it, as version control retains its history.
- Delete redundant parentheses, for example doubled pairs or a pair enclosing an entire expression that changes no grouping.
- Delete stray semicolons that form no-op statements.
- Supply an explanation in every `[Obsolete]` attribute, naming the substitute API.
- Delete `[Obsolete]` code once its deprecation period has elapsed; deprecated members are pending deletion.
- Never commit `FIXME` comments; correct the defect or record it in the issue tracker.
- Resolve `TODO` comments prior to completion; record outstanding activity in the issue tracker rather than in source.
- Never nest a bare `{ }` code block within a method; extract a method instead.
- Never use `async` or `await` as identifiers.
- Name enumerations per `^([A-Z]{1,3}[a-z0-9]+)*([A-Z]{2})?$`; use a plural name for `[Flags]` enumerations, per the identical expression with a trailing `s`.
- Never suffix an enumeration name with `Enum` or `Flags`.
- Enclose multiline `if`, `else`, and loop bodies in braces; indentation never defines a block.
- Delete namespaces that contain no types.
- Suffix the name of every type deriving from `Attribute`, `EventArgs`, or `Exception` with that base name.
- Declare every type within a named namespace.
- Start an `if` that succeeds a closing brace on a separate line, or combine it into `else if`.
- Indent the single statement of a braceless `if` or loop body, and never indent the subsequent statement at that level.
- Declare all overloads of a method adjacent to each other.
- Never commit comments without text (`//`, `/* */`).
