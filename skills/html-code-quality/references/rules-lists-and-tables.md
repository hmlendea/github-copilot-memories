# HTML Rules: Lists And Tables

One directive per HTML rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Place every `<li>` within `<ul>`, `<ol>`, or `<menu>`, and every `<dt>` within `<dl>`.
- Provide every data table with `<th>` header cells; tables declaring `role="presentation"`, `role="none"`, or `aria-hidden="true"` are exempt.
- Never use `<table>` for layout, including tables declaring `role="presentation"` or `role="none"`; arrange the layout with CSS.
- Never include semantic markup in a layout table: no `<caption>`, `<th>`, non-vacant `summary`, or `<td>` declaring `headers` or `scope`.
- Reference only header cells in the `headers` attribute of a `<td>`: each value must be the `id` of a `<th>` in the row or column of that cell; prefer `scope` on `<th>` for simple tables; values containing `{`, `}`, `(`, `)`, `[`, `]`, or `$` are exempt as template expressions.
- Declare `scope` or `id` on every `<th>`, so that assistive technologies associate it with its data cells.
