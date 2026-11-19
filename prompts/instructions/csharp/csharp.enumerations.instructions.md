---
description: "Use when creating or editing a C# enumeration or enumeration class, or when choosing between a plain enum and an enumeration class. Obligates the `csharp-enumerations` skill, which holds the canonical enumeration-class template and its rules."
applyTo: "**/*.cs"
---

## Mandatory Skill

Every C# enumeration and enumeration class is governed by the `csharp-enumerations` skill. Invoking that skill is mandatory, not optional: read `skills/csharp-enumerations/SKILL.md` before creating or revising an enum or an enumeration class, and apply it in full. Do not author an enumeration class from memory or from a partial reading of the skill.

The skill holds the namespace placement rule, the selection rule between a plain `enum` and an enumeration class, the canonical enumeration-class template, and the structural rules that template must satisfy.
