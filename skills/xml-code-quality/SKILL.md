---
name: xml-code-quality
description: "Use when editing or reviewing XML documents or configuration, including Maven POMs, Spring bean definitions, Hibernate configuration, Android manifests, web.xml, and web.config, for TODO and FIXME comments, commented-out markup, prolog placement, deprecated POM properties, system-scoped dependencies, JMS connection restoration, listener container shutdown, schema generation, or analyser diagnostics, and to apply the complete XML rule catalogue: naming, layout, and comments, and platform APIs. Preserves encoding detection, portable dependency resolution, message delivery, and database schemas even without analyser diagnostics."
---

# XML Code Quality

Apply each relevant section prior to editing and verify it prior to completion. These are preventive requirements, not merely responses to analyser diagnostics. Do not refactor unrelated code or install analysers solely for this checklist.

Use the [XML security instructions](../../instructions/xml/xml.security.instructions.md) for security guidance and the [PolyGlot dictionary instructions](../../instructions/polyglot/polyglot.dictionary.instructions.md) for `PGDictionary.xml` files. Load them if absent from context. Required external contracts, including published schemas, framework descriptors, and generated files, take precedence; report exceptions rather than silently weakening a rule.

## Rule Catalogue

The `references/rules-*.md` files contain one directive per XML quality and reliability rule (9 rules); the [security instructions](../../instructions/xml/xml.security.instructions.md) contain the 16 security rules. Load every reference whose topic the change touches, and the security instructions for any security-relevant change.

- Precedence: explicit local instructions and required external contracts prevail over a catalogue directive. Report each conflict instead of silently selecting a policy.
- Markers: **Local precedence** records a local deviation.
- Known deviations: none. No local instruction conflicts with a catalogue directive; the common coding and naming instructions, including their `TODO` comment format, do not apply to XML files.

| Concern | Threshold |
| --- | --- |
| Credential names | Element, attribute, and property names containing `password`, `passwd`, `pwd`, or `passphrase` |

| Topic | Reference |
| --- | --- |
| `TODO` and `FIXME` comments, commented-out markup, `<?xml` prolog placement | [rules-naming-and-layout.md](references/rules-naming-and-layout.md) |
| Maven `${pom.*}` properties and `system` scope, Spring JMS connection factories and listener containers, Hibernate schema generation | [rules-platform-apis.md](references/rules-platform-apis.md) |

## Verification

- Review every applicable section and rule reference, not just the reported diagnostic.
- Execute existing focused checks for the changed files, for example XML well-formedness or schema validation, Maven or Android manifest validation, and framework configuration tests the repository already uses.
- Verify prolog placement, credential handling, exported Android components, and framework settings where affected. Report unexecuted checks and unresolved diagnostics; do not present static inspection as runtime verification.
