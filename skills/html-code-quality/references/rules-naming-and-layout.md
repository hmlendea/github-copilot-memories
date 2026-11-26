# HTML Rules: Naming, Layout And Comments

One directive per HTML rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Resolve every `TODO` comment in an HTML file prior to completion; record outstanding activity in the issue tracker rather than in the file.
- Resolve every `FIXME` comment in an HTML file prior to completion; correct the defect it marks or record it in the issue tracker rather than in the file.
- Never retain commented-out HTML elements, attributes, scripts, or other markup within `<!-- -->`; delete it, as version control history preserves it.
- Declare `<!DOCTYPE html>` prior to the `<html>` element of every page, so that browsers apply standards mode rather than quirks mode.
- Include a `<title>` element within the `<head>` of every page; browser tabs, search results, and assistive technologies identify the page by it.
- Declare `lang` on the `<html>` element, and start every `lang` and `xml:lang` value on an element containing text with a valid two-letter ISO 639-1 language code (`en`, `en-GB`, `es`), never a misspelt or undefined code (`engl`, `xx`).
- Assign every `id` attribute a value unique within the document; duplicate values invalidate label associations, ARIA references, fragment links, and `getElementById` calls.
- Never nest `<script>` elements; the browser terminates the outer script at the first `</script>` and displays the rest as page content.
