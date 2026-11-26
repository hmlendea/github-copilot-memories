---
description: "Use when writing or editing C# code. Covers line splitting and indentation rules."
applyTo: "**/*.{cs}"
---
## C#

### Line Splitting & Indentation

- Multi-clause `if` exceeding 72 characters: one clause per line; place `&&`/`||` at line end; indent continuations 4 spaces. Never split within 72 characters.
- Multi-line `return`: place `return` alone; indent the expression; place operators at line end.
- Properties: one per line, separated from adjacent members by one blank line. Place each accessor body on its own line.
- Parameter/argument list exceeding 96 characters: retain the signature prefix on the opening line; place every item on its own 4-space-indented line; place the closing `)` on the same line as the last item. Never mix inline and continued items, and never place the closing `)` on its own line.
- Never end a line with `=>`. When an expression body leaves the signature line, `=>` begins the next line, followed by the start of the expression.
- Expression-body layout uses this precedence after parameter wrapping:
  1. Multi-line object initialiser: conclude the signature with `=> new()`; place `{` on the next line; close with `};`.
  2. Other multi-line expression: place `=>` and the first expression line on the line after the signature (after the closing `)` line when parameters are wrapped), indented 4 spaces beyond the signature's first line; indent further expression lines 4 spaces beyond the `=>` line; place operators at line end. Never substitute a block-body `return`.
  3. Single-line expression: when the signature plus expression exceeds 96 characters, place `=>` and its expression on the next line, indented 4 spaces beyond the signature's first line; otherwise retain them on the signature line.
- Arguments of a multi-line call are indented 4 spaces beyond the line that opens the call, never aligned with it.

Expression bodies:
```csharp
internal static bool ContainsSensitiveData(string? value)
    => value is not null && CardCandidate().Matches(value).Any(match => HasValidCardChecksum(match.Value));

internal static string OptionCollectionMustBeExplicit(
    string optionName)
    => string.Create(
        CultureInfo.InvariantCulture,
        $"The {optionName} collection must be explicit.");
```

Never:
```csharp
internal static bool ContainsSensitiveData(string? value) =>
    value is not null && CardCandidate().Matches(value).Any(match => HasValidCardChecksum(match.Value));
```
