# Shell Rules: Naming, Layout And Comments

One directive per Shell rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Name functions in snake_case, with lowercase words separated by underscores (`process_file`); never `processFile` or `ProcessFile`.
- Name exported environment variables in ALL_CAPS (`export DATA_DIRECTORY=…`) and local variables in lower_case (`local file_name=…`). **Local precedence:** the naming instructions require uppercase names for every variable, referenced as `${VAR_NAME}`; retain uppercase local variables and report each occurrence.
- Resolve every `TODO` comment and delete it once complete; format any interim one as `# TODO: Description.`
