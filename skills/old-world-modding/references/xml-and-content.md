# XML and Content

All XML content belongs under the mod's `Infos/` directory. Use the installed `Reference/XML/` files as templates; they are not runtime files.

| Suffix | Purpose | Example |
|--------|---------|---------|
| `-add` | Create new content or a new entry | `nation-add.xml` |
| `-append` | Add lines to an existing element or collection | `spriteGroup-append.xml` |
| `-change` | Modify existing content and fields | `nation-change.xml` |

Preserve the original root and element names. Use unique `zType` identifiers and update every reference to the new identifier. Text is commonly stored in a `text-<language>-<source>-<suffix>.xml` file with language-tagged values; copy the installed pattern rather than inventing a schema.

For basic XML edits, a text editor is sufficient. For each change, enable the mod, read `Logs/output.txt`, and resolve the first error before interpreting later errors. Test changes in a new game because loaded saves may retain old data.
