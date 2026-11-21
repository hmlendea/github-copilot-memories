---
description: "Use when writing or editing C# code. Covers line splitting and indentation rules."
applyTo: "**/*.{cs}"
---
## C#

### Line Splitting & Indentation

- Multi-clause `if` exceeding 72 characters: one clause per line; place `&&`/`||` at line end; indent continuations 4 spaces. Never split within 72 characters.
- Multi-line `return`: place `return` alone; indent the expression; place operators at line end.
- Properties: one per line, separated from adjacent members by one blank line. Place each accessor body on its own line.
- Parameter/argument list exceeding 96 characters: retain the signature prefix on the opening line; place every item on its own 4-space-indented line; align closing `)` with the signature. Never mix inline and continued items.
- Long expression-bodied signature: place `=>` on the next line, indented 4 spaces, followed by its expression.
- Multi-line expression body: end the signature with `=>`; indent expression lines 4 spaces; place operators at line end. Never substitute a block-body `return`.
- Multi-line initialiser body: end the signature with `=> new()`; start `{` on the next line; close with `};`.
- Signature plus expression exceeding 96 characters: place `=>` and the expression on the next line, indented 4 spaces, even when the expression alone fits one line.
