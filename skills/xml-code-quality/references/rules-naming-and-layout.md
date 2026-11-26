# XML Rules: Naming, Layout And Comments

One directive per XML rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Resolve every `TODO` comment in an XML file prior to completion; record outstanding activity in the issue tracker rather than in the file.
- Resolve every `FIXME` comment in an XML file prior to completion; correct the defect it marks or record it in the issue tracker rather than in the file.
- Never retain commented-out XML elements, attributes, or other markup within `<!-- -->`; delete it, because version control history preserves it.
- Place the `<?xml ... ?>` prolog, where present, at the very start of the file, with nothing preceding it, not even a comment or whitespace, so that parsers can determine the encoding of files other than UTF-8 and UTF-16.
