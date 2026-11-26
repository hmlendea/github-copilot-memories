# Python Rules: Naming And Layout

One directive per Python rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Name methods per `^[a-z_][a-z0-9_]*$` (snake case). **Local precedence:** The naming instructions additionally prohibit abbreviations and single-letter names; apply both.
- Name classes per `^_?([A-Z_][a-zA-Z0-9]*|[a-z_][a-z0-9_]*)$`. **Local precedence:** The coding instructions require PascalCase for every class, and the naming instructions prohibit abbreviations and single-letter names; apply the PascalCase form only.
- Name class and instance fields per `^[_a-z][_a-z0-9]*$` (snake case). **Local precedence:** The naming instructions additionally prohibit abbreviations and single-letter names; apply both.
- Name local variables and function parameters per `^[_a-z][a-z0-9_]*$` (snake case). **Local precedence:** The naming instructions additionally prohibit abbreviations and single-letter names, including loop, comprehension, and lambda variables; apply both.
- Name functions per `^[a-z_][a-z0-9_]*$` (snake case). **Local precedence:** The naming instructions additionally prohibit abbreviations and single-letter names; apply both.
- Name the first parameter of class methods `cls`, `mcs`, or `metacls`. **Local precedence:** The naming instructions prohibit abbreviations; use a descriptive name and report each deviation.
- Declare `self` as the first parameter of every instance method; methods decorated with `abstractmethod` are exempt.
- Never name a field identically to its containing class.
- Never declare methods or fields whose names differ only by capitalisation.
- Never name local variables after builtins (for example `list`, `id`, or `type`), which shadows them.
- Never use wildcard imports (`from module import *`), except in `__init__.py`.
- List only strings in `__all__`.
- List only names defined in the module in `__all__`.
- Delete redundant pairs of parentheses.
- Delete commented-out code; only comments corresponding entirely to `(fmt|py\w+):.*` (formatter and type-checker directives) are exempt.
- Resolve every `FIXME` comment and delete it once resolved.
- Resolve every `TODO` comment and delete it once complete; format any interim one as `# TODO: Description.`
- Format issue suppression comments correctly: `# noqa` alone or `# noqa: rule1,rule2`, without redundant commas, and with balanced parentheses in equivalent analyser suppression markers. **Local precedence:** The coding instructions require comments to start with an uppercase letter and conclude with a period; suppression markers are a required external contract, so retain the tool syntax exactly and report each occurrence.
- Never use backticks for string conversion; call `repr()`.
- Never use the Python 2 `exec` statement; call the `exec()` function.
- Never use `<>` to test inequality; use `!=`.
- Never use the Python 2 `print` statement; call the `print()` function.
