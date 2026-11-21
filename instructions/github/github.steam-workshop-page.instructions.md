---
description: "Use for every `steam-workshop.bbcode` file. Obligates the agent to apply the `steam-workshop-page` skill, which provides the canonical BBCode template, rules file, output path, fidelity contract, and validator."
applyTo: "**/steam-workshop.bbcode"
---

## Mandatory Skill

Every `steam-workshop.bbcode` file is governed by the `steam-workshop-page` skill. Invoking that skill is mandatory, not optional: read `skills/steam-workshop-page/SKILL.md` before creating or revising any such file, and apply it in full — its scope precondition, generation procedure, documentation synchronisation, fidelity contract, and validation pipeline. Do not create or revise a `steam-workshop.bbcode` file from memory or from any partial reading of the skill.

Use the canonical template `skills/steam-workshop-page/templates/workshop-description.bbcode` for every Steam Workshop page description, and its rules `skills/steam-workshop-page/rules/workshop-description.md`.

Write the generated description to `description/steam-workshop.bbcode` in the repository root, creating the `description/` directory when it does not exist. Never use another path or file name.

The description must commence with the fixed header block and conclude with the fixed donate banner, and the template must remain exactly as written apart from the placeholders.