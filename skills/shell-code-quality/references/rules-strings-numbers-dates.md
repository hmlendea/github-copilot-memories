# Shell Rules: Strings, Numbers And Dates

One directive per Shell rule in this area. Explicit local instructions prevail; see the [rule catalogue](../SKILL.md#rule-catalogue) for precedence notes.

- Replace a string literal repeated 3 or more times with a `readonly` constant (`readonly CUSTOMER_MESSAGE='creating customer'`), referenced as `"${CUSTOMER_MESSAGE}"`.
