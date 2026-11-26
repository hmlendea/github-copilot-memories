# HTML Rules: ARIA Roles And Properties

One directive per HTML rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Assign every `aria-*` attribute a value its definition permits: `true` or `false` for boolean states, a defined token for enumerated properties (for example `aria-live="polite"`), a number for numeric properties, and existing `id` values for identifier references.
- Never declare a role identical to the element's implicit role, for example `<button role="button">` or `<ul role="list">`; the sole permitted redundant role is `navigation` on `<nav>`.
- Declare every state and property that an element's ARIA role requires, for example `aria-checked` on `role="checkbox"`.
- Never declare an ARIA role or `aria-*` attribute on unsupported, predominantly non-visible elements, for example `<html>`, `<head>`, and `<meta>`.
- Declare only the `aria-*` attributes that the element's role supports, each spelt correctly; never, for example, `aria-checked` on `role="link"`.
- Prefer the native HTML element to an ARIA role that reproduces its semantics, for example `<button>` instead of `role="button"`, `<nav>` instead of `role="navigation"`, and `<img>` instead of `role="img"`.
- Assign `role` only valid, non-abstract ARIA roles; never an undefined value or the abstract roles `command`, `composite`, `input`, `landmark`, `range`, `roletype`, `section`, `sectionhead`, `select`, `structure`, `widget`, or `window`.
- Never declare `aria-hidden="true"` on a focusable element, for example `<a href>`, `<button>`, a form control, or an element with a non-negative `tabindex`; assistive technologies would otherwise conceal an element that keyboard users can still focus.
- Never assign a non-interactive ARIA role (for example `article`, `heading`, `img`, `listitem`, or `presentation`) to an interactive element (`<a href>`, `<button>`, `<input>`, `<select>`, `<textarea>`).
- Never assign an interactive ARIA role (for example `button`, `checkbox`, `link`, or `textbox`) to a non-interactive element (`<p>`, `<img>`, `<h1>` to `<h6>`, `<ul>`, `<li>`); use the native interactive element instead.
- Where a page contains more than one `<nav>` or `<aside>` element, or more than one element with an identical landmark role (`application`, `banner`, `complementary`, `contentinfo`, `form`, `main`, `navigation`, `search`), distinguish each by a unique `aria-label` or `aria-labelledby`.
- Include the visible text of every interactive element within its accessible name; an `aria-label` or `aria-labelledby` that differs from the visible text confuses screen reader users and obstructs voice control users.
