---
description: "Use for Romanian prose, code identifiers, literals, comments, or documentation, and for text generation, editing, translation, or review. Requires the `romanian-language` skill."
applyTo: "**"
---

## Romanian

When generating, editing, reviewing, or translating Romanian text, invoke the `romanian-language` skill and apply its Latin-ancestry preference and contextual word replacements.

Mandatory: this instruction applies to every file containing Romanian text that is edited or generated, whatever its type, and not only Markdown files. Invoke the skill before finishing any edit and review the result against it.

Completeness: apply the entire dictionary. Every word replacement record in the skill applies to all variants and derivatives of the word, so no matching form, variant, or derivative may remain unreviewed. Applying only part of the dictionary, or stopping after an arbitrary subset, is incomplete work. Volume and length never shorten the pass.

The only permitted non-applications are the skill exemptions: a change that would break a public or external contract or compatibility, an established proper noun or product name, and a replacement that no fluency-aware reading can integrate. A record with a comment that limits its scope applies only within that scope. Each exemption applied must be listed explicitly in the completion summary, together with its reason. Remaining unchanged text that the dictionary covers and no exemption explains is a defect.

Scope: every human-readable Romanian string, including prose and documentation, code identifiers (variable, parameter, function, method, class, type, constant, enumeration, field, property, event, module, package, file, directory, branch, and tag names), string literals, comments, doc comments, log, error, and exception messages, user-interface and localisation strings and keys, test names, descriptions, and expectations, test and fixture data, and commit messages. Apply the rules to any such text wherever it appears, in code and outside it.
