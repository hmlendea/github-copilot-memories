# Kotlin Rules: Strings And Regular Expressions

One directive per Kotlin rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Never repeat a string literal 3 or more times; extract it into a `const val`. Literals of 5 or fewer characters, and literals composed only of letters, digits, and `_`, are exempt.
- Limit the complexity of each regular expression to at most 20.
- Never test for vacant lines with a `MULTILINE` regular expression (`RegexOption.MULTILINE`, `Pattern.MULTILINE`, `(?m)`) that accepts a zero-length string (`^$`) without also testing whether the entire input is vacant.
- Use negated character classes instead of reluctant quantifiers (`<[^>]+>` instead of `<.+?>`).
- Never repeat a character within a character class, including via overlapping ranges (`[0-99]`) or an unescaped `-`.
- Never apply `*` or `+` to sub-expressions that accept a zero-length string.
- Group alternatives combined with anchors (`^(?:a|b|c)$` instead of `^a|b|c$`).
- Use only syntactically valid regular expressions; to treat text literally, escape it or use `RegexOption.LITERAL`.
- Never place Unicode grapheme clusters within character classes; use alternation instead.
