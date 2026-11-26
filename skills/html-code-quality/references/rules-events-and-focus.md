# HTML Rules: Events, Keyboard And Focus

One directive per HTML rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Ensure every element declaring `aria-activedescendant` can receive focus by the Tab key: use an inherently focusable element or declare `tabindex="0"`.
- Never use `<a>` as a button: declare on every anchor an `href` leading to a genuine destination, never an absent `href`, `#`, or `javascript:void(0)`, and use `<button>` for in-page actions.
- Never declare `tabindex="0"` or a positive `tabindex` on a non-interactive element; omit it, or use `tabindex="-1"` solely for programmatic focus.
- Never declare `accesskey`; its key combinations conflict with browser, operating system, and assistive technology key combinations and vary by browser.
- Never declare event attributes (`onclick`, `onkeydown`, `onmouseover`, and similar) on non-interactive elements, for example `<p>`, `<li>`, `<h1>` to `<h6>`, or `<img>`; use an interactive element instead.
- Never declare interactive event attributes (`onclick`, `onkeydown`, `onkeyup`, `onkeypress`, `onmousedown`, `onmouseup`) on `<div>`, `<span>`, or `<footer>` unless the element also declares an interactive role (`button`, `checkbox`, `link`, `menuitem`, `menuitemcheckbox`, `menuitemradio`, `option`, `radio`, `searchbox`, `switch`, `textbox`) and implements keyboard and focus management; prefer the native interactive element.
- Ensure every element with an interactive ARIA role can receive focus: use a natively focusable element or declare `tabindex="0"`.
- Assign `tabindex` only `0` or `-1`; positive values disrupt the natural focus order.
- Pair every mouse event attribute with its keyboard equivalent: `onmouseover` with `onfocus`, `onmouseout` with `onblur`, and `onclick` with `onkeydown`, `onkeyup`, or `onkeypress` that manages Enter and Space; `<button>`, `<a>`, and `<input type="button">` or `<input type="submit">` are exempt, whereas `role="button"` is not.
