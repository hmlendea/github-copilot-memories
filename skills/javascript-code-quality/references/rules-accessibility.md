# JavaScript Rules: Accessibility

One directive per JavaScript rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Provide alternative text (`alt`, `aria-label`, `aria-labelledby`, or `title`) for `img`, `area`, `input type="image"`, and `object` elements.
- Pair every mouse event handler with a keyboard equivalent (`onClick` with `onKeyDown`, `onMouseOver` with `onFocus`, `onMouseOut` with `onBlur`).
- Provide a `title` attribute for every `iframe`.
- Provide captions (`<track kind="captions">`) for `audio` and `video` elements.
- Set a valid BCP 47 `lang` attribute on the `html` element.
- Provide headers (`<th>`) in every data table.
- Never use `<table>` for layout; use CSS.
- Ensure every `headers` attribute on a table cell references the `id` of a header in that table.
- Provide alternative content within every `<object>` element.
- Assign only valid values to ARIA properties.
- Provide every property that an element's ARIA role requires.
- Use only ARIA properties that the element's role supports.
- Use semantic HTML elements (`<button>`, `<nav>`) rather than ARIA roles on generic elements.
- Use only valid, non-abstract ARIA roles.
- Never assign an ARIA role that duplicates the element's implicit role (`<button role="button">`).
- Ensure elements with `aria-activedescendant` are focusable via the tab key (`tabIndex`).
- Never assign ARIA roles or properties to elements that do not support them (`meta`, `html`, `script`, `style`).
- Never set `aria-hidden` on focusable elements.
- Provide accessible content for every anchor.
- Use valid `autocomplete` values on form fields that collect personal data.
- Set `tabIndex` only to `0` or `-1`.
- Never assign interactive ARIA roles to non-interactive elements.
- Never assign non-interactive ARIA roles to interactive elements.
- Never use anchors as buttons; use `<button>` for actions and a valid `href` for navigation.
- Never set `tabIndex` on non-interactive elements.
- Never use the `accesskey` attribute.
- Never attach interactive event handlers to non-interactive elements (`<li>`, `<main>`, `<h1>`).
- Never attach interactive event handlers to static elements (`<div>`, `<span>`) without an appropriate role.
- Provide accessible content for every heading element.
- Never include redundant words (`image`, `photo`, `picture`) in `alt` text.
- Ensure elements with interactive roles are focusable.
- Ensure every `<label>` contains text content and is associated with a control.
