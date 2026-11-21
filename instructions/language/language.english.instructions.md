---
description: "Use for English prose, code identifiers, literals, comments, or documentation, and for localisation, terminology revision, or strict contextual word replacement. Requires the `english-language` skill."
applyTo: "**"
---

## English

When generating, editing, reviewing, or localising English text, invoke the `english-language` skill and apply its British spelling, Latin-ancestry preference, and contextual vocabulary replacements.

Mandatory: this instruction applies to every file that is edited or generated, whatever its type, and not only Markdown files. Invoke the skill before finishing any edit and review the result against it.

Completeness: apply the entire dictionary. The shared records are exhaustive, so every matching word, variant, and derivative in British-spelling candidates, Latin-ancestry candidates, and contextual replacement records must be applied. Applying only part of a dictionary, or stopping after an arbitrary subset, is incomplete work. Volume and length never shorten the pass.

The only permitted non-applications are the skill exemptions: a change that would break a public or external contract or compatibility, an established proper noun or product name, and a replacement that no fluency-aware reading can integrate. Each exemption applied must be listed explicitly in the completion summary, together with its reason. Remaining unchanged text that the dictionary covers and no exemption explains is a defect.

Scope: every human-readable English string, including prose and documentation, code identifiers (variable, parameter, function, method, class, type, constant, enumeration, field, property, event, module, package, file, directory, branch, and tag names), string literals, comments, doc comments, log, error, and exception messages, user-interface and localisation strings and keys, test names, descriptions, and expectations, test and fixture data, and commit messages. Apply the rules to any such text wherever it appears, in code and outside it.
