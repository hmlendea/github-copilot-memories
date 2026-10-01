---
name: structured-data-query
description: Use when only specific fields or records are required from JSON, YAML, XML, CSV, API responses, manifests, lock files, or other structured data.
---

Query structure; do not read or return the entire source.
- Select only required fields, records, counts, and relationships.
- Prefer structured tools: `jq` for JSON; `yq` for YAML; format-aware parsers for XML/CSV.
- Verify tool availability. If absent, use a standard-library parser; do not install a dependency solely for extraction.
- Preserve types and parse errors. Never parse structured data with regex when a parser exists.
- Read the complete source only when it is minor or its complete structure is necessary.
- For edits, use a structured API where practical; inspect the affected region and validate the resulting document.
