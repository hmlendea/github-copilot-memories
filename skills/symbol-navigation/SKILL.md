---
name: symbol-navigation
description: "Use when locating symbol definitions, references, implementations, call sites, or structurally similar code without reading broad file sets."
---

Navigate semantics prior to text, and acquire a map prior to acquiring source.
- Known symbol: use language-server definitions, references, implementations, or rename support first.
- Unfamiliar area: establish a structural outline of the relevant directory or file first, then fetch only the symbols the assignment concerns; the default preference is the smallest structural answer, not the complete file.
- Skip the broad enumeration, text search, complete-file read cycle for discovery when a structural query can return ranked symbols in one operation.
- Structural pattern: use an installed syntax-aware query tool; do not install one solely for the query.
- Text fallback: search exact identifiers within relevant file types and directories; return paths, line numbers, and minimal context.
- Read only the owning definition and discriminating call sites.
- Cease when the controlling path and required edit surface are established.
