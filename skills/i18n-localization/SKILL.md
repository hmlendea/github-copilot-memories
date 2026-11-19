---
name: i18n-localization
description: "Use when adding interface text, adding or shipping a locale, reviewing translation files, or building localisation into an application. Covers key and placeholder verification, CLDR plural categories, ICU syntax, hardcoded-string detection, and pseudo-locale review."
---

Verify the translation layer rather than translate text. Inspect files and generate a pseudo-locale; a translation service is never a substitute for a translator.

## Translation Files

Pair each target locale file with the source file of the same namespace and check:
- absent, empty, or orphaned keys;
- placeholders added, renamed, or dropped against the source; a translator may relocate a placeholder but never rename it;
- malformed message syntax (unbalanced ICU braces, malformed select and plural blocks);
- plural and select constructs without an `other` branch;
- an ICU `=0` branch replaced with a branch that can never match;
- plural categories the target locale requires and the file omits, per CLDR (Russian and Polish require `few` and `many`; Arabic requires six forms).

Follow CLDR plural categories for the target locale; never copy the source locale's categories into a locale that requires others.

## Message Composition

- Never concatenate translated fragments; one message per sentence with named placeholders, and positional indices where the argument order can vary.
- Derive currency from the data and pass the locale to every formatter; an interface locale must not determine a monetary or temporal format.

## Source Scan

Scan the source for literal user-facing text outside the translation function, literal text rendered conditionally, concatenation with translated strings, and date, number, or currency formatting without a locale.

## Pseudo-Locale Review

Generate a pseudo-locale that accents, pads by anticipated translation growth, and brackets every string whilst preserving placeholders and message syntax. Traverse the interface in it: plain text indicates an untranslated string, a truncated bracket indicates a layout defect, and interleaved brackets indicate concatenation.

## Discipline

Never machine-translate to satisfy a check: an absent translation falls back to the source language, whereas an erroneous one ships silently. Record gaps for a translator instead.
