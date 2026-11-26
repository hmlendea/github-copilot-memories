# HTML Rules: Text Alternatives, Forms And Media

One directive per HTML rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Declare `alt` on every `<img>`, and a non-vacant `alt` on every `<area>` and `<input type="image">`; use `alt=""` only for a decorative image that a CSS background image is unable to replace, or where the text would repeat adjacent text, and never an uninformative value, for example `alt="logo"`.
- Never include the words "image", "picture", or "photo" in `alt` text; screen readers announce the element as an image regardless.
- Declare a descriptive `title` on every `<frame>` and `<iframe>`.
- Provide accessible alternative content within every `<object>` element, for example descriptive text or an `<img>` with `alt`, for assistive technologies and user agents unable to display the resource.
- Provide every anchor with accessible content (visible text, an `aria-label`, or a `title`), and never conceal that content with `aria-hidden`.
- Provide every heading (`<h1>` to `<h6>`) with accessible content, and never conceal that content with `aria-hidden`.
- Associate every `<label>` with text and a control: enclose the control (`<input>`, `<meter>`, `<output>`, `<progress>`, `<select>`, `<textarea>`) together with the label text, or reference its `id` with `for`, using deterministic `id` values; custom elements are exempt.
- Assign `autocomplete` on `<input>`, `<select>`, and `<textarea>` only a valid token suited to the field, for example `name`, `email`, `tel`, `country`, or `cc-number`, never an undefined value (`foo`).
- Provide every `<video>` with a `<track>` of `kind="captions"` (for hearing-impaired users) or `kind="descriptions"` (for vision-impaired users), or at the very least `kind="subtitles"`, which serves translation rather than accessibility.
- Never declare `autoplay` on `<audio>` or `<video>`; declare `controls` so that users start playback themselves.
