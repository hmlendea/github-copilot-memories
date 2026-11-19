Generate or revise the Steam Workshop page description (BBCode) for this repository using `templates/workshop-description.bbcode`, and write it to `description/steam-workshop.bbcode` in the repository root.

## Strict Template Fidelity Mode (Default)

Strict fidelity applies to every Steam Workshop page description creation or revision and overrides conflicting instructions. Strict fidelity applies **only to personal repositories owned by the current git user** (GitHub owner type `User` and owner matching the current git user); organisation-owned repositories and repositories owned by another user are out of strict-fidelity scope. If the user explicitly requests the templates, strict fidelity applies regardless of repository ownership.

### Generation Contract

**MANDATORY INCLUSION RULE:** Every block marked with `<!-- Only if ... -->` in the template MUST be included in the final description when its condition is satisfied. Do not omit conditional blocks whose conditions are met. Remove the entire conditional block, including its heading, body, example rows, and directive comment, only when the condition is NOT met.

1. Start from `templates/workshop-description.bbcode` and process it from top to bottom.
2. Write the result to `description/steam-workshop.bbcode` in the repository root, creating the `description/` directory when it does not exist. Never write the description to any other path or file name.
3. Preserve the initial banner block, the closing donate banner, line order, blank lines, BBCode tags, whitespace within tags, and every fixed image and link URL.
4. All fixed prose lives in the template. Copy it byte-for-byte, and change only placeholders, `Repeat` lines, and the conditional blocks expressly gated by a directive comment.
5. The description must invariably commence with the three introductory images (the header animation, the funding button, and the repository button) and must invariably conclude with the closing donate banner. Neither block may be removed, reordered, or partially emitted.
6. Every non-Steam outbound link must be wrapped in the Steam link filter exactly as written: `https://steamcommunity.com:/linkfilter/?url=<TARGET>`. The `:/linkfilter/` segment is intentional and must never be normalised or corrected.
7. Steam Workshop descriptions are BBCode, not Markdown and not HTML. Use only BBCode tags.
8. Duplicate a `Repeat` line only once per evidenced record, then remove the example placeholder.
9. Remove every template comment from the delivered description.
10. The description must not contain hidden text, keyword stuffing, unverified claims, or content that violates the Steam Workshop rules.

### Placeholders

| Placeholder | Replacement |
|-------------|-------------|
| `[[FUNDING_URL]]` | The author's funding page link used by the header button and the announcement banner. Resolve it from `.github/FUNDING.yml`: use the `custom` field value verbatim; when `custom` is absent or devoid of a value, use the `github` field as `https://github.com/sponsors/<github>`. When the user or repository explicitly provides a funding link, use that verbatim. Never invent one. It appears twice and must be identical in both positions. |
| `[[DONATE_PAGE_URL]]` | The author's dedicated donation page linked by the closing donate banner. Resolve it from documented author evidence, for example the `.html` donation page the announcement banner links to. When the author has no separate donation page, reuse the resolved `[[FUNDING_URL]]` value. It appears once, in the closing banner. |
| `[[REPOSITORY_URL]]` | The canonical repository URL, for example `https://github.com/<owner>/<repo>`. |
| `[[ABOUT]]` | The About body: a one- or two-sentence statement of what the item is and which game it targets. |
| `[[CAPABILITY]]` | One principal, evidenced capability, prioritising user outcomes over implementation details. The template supplies the `Repeat` marker. |
| `[[INSTALLATION_BADGES]]` | The installation badge block (see Installation Badges). At least one badge is mandatory. |
| `[[UPGRADE_INSTRUCTIONS]]` | The evidenced upgrade procedure when it requires more than repeating the installation command. |
| `[[REQUIREMENTS]]` | Requirements beyond the base game, such as DLC, expansions, or other mods, as evidenced. |
| `[[SUPPORTED_GAME_VERSION]]` | The evidenced game version the item supports, for example `3.14.*` or `1.9.2`; see Compatibility Section. |
| `[[LOAD_ORDER]]` | Required load order or placement guidance as evidenced; rendered as the `[h2]Load Order[/h2]` sub-section of Compatibility. |
| `[[INCOMPATIBLE_MOD_URL]]` | The incompatible mod link, resolved in priority order: its Steam Workshop page, otherwise its Nexus Mods page, otherwise its GitHub repository. |
| `[[INCOMPATIBLE_MOD_NAME]]` | The incompatible mod name. |
| `[[INCOMPATIBLE_MOD_REASON]]` | A concise, evidenced reason for the incompatibility. |
| `[[LANGUAGE]]` | The human-readable language name, for example `English` or `German`. |
| `[[LOCALE_CODE]]` | The standards-compliant locale identifier, for example `en` or `de`. |
| `[[TRANSLATION_STATUS]]` | The translation completeness, see Compatibility Section. |
| `[[RELATED_MOD_URL]]` | The related mod link, resolved in priority order: its Steam Workshop page, otherwise its Nexus Mods page, otherwise its GitHub repository. |
| `[[RELATED_MOD_NAME]]` | The related mod name. |
| `[[RELATED_MOD_DESCRIPTION]]` | A concise description of the related mod. |
| `[[ADDITIONAL_SUPPORT]]` | An optional evidenced support-channel line, such as a documented forum, discussion board, or support document. |
| `[[TROUBLESHOOTING]]` | Evidenced diagnostic procedures and resolutions, placed inside the Support section. |
| `[[FAQ_DOCUMENT_LINK]]` | The verified repository-relative path of the existing FAQ document. |
| `[[PROJECT_NAME]]` | The human-friendly project name. |
| `[[GITHUB_REPO_USERNAME]]` | The GitHub repository owner. |
| `[[GITHUB_REPO_NAME]]` | The GitHub repository name. |
| `[[DEFAULT_BRANCH]]` | The repository default branch; do not presume `master` or `main`. |
| `[[STEAM_WORKSHOP_ID]]` | The Steam Workshop item identifier, used only by the installation badge. |
| `[[LICENSE_TITLE]]` | The repository licence title, taken from `LICENSE` without inference. The template links it to the `LICENSE` file on `[[DEFAULT_BRANCH]]`. |
| `[[LICENSE_SUFFIX]]` | ` or later` only when the licence text or SPDX expression explicitly grants later versions; otherwise empty. |
| `[[FUNDING_PREFIX]]` | `[url=https://steamcommunity.com:/linkfilter/?url=[[FUNDING_URL]]]funding it[/url] or ` when `.github/FUNDING.yml` exists; otherwise empty. |

### Fixed Assets

These template values are fixed and MUST NOT be changed:

| Asset | Fixed value |
|-------|-------------|
| Header animation | `https://i.imgur.com/8I8Im27.gif` |
| Funding button | `https://i.imgur.com/ZW5bp28.png` |
| Repository button | `https://i.imgur.com/UPNlpGj.png` |
| Announcement banner file | `announcement_donation.png` |
| Donation asset base URL | `https://raw.githubusercontent.com/hmlendea/more-cultural-names/master/assets/en` (hardcoded; never parameterised) |
| Closing banner file | `banner_donate.png` |
| Store badge path | `https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/` |
| Link filter prefix | `https://steamcommunity.com:/linkfilter/?url=` |

### Mandatory Sections

The description MUST contain exactly these sections, in this order:

| Section | Heading | Body |
|---------|---------|------|
| About | `[h1]About[/h1]` | `[[ABOUT]]` |
| Capabilities | `[h1]Capabilities[/h1]` | `[list]` of repeatable `[*][[CAPABILITY]]` |
| Installation | `[h1]Installation[/h1]` | `[[INSTALLATION_BADGES]]`, then the conditional `[h2]Upgrading[/h2]` sub-section |
| Contributing | `[h1]Contributing[/h1]` | Fixed prose directing contributors to the GitHub repository || Support | `[h1]Support[/h1]` | Fixed prose |
| Project Engagement | `[h1]Project Engagement[/h1]` | Fixed prose |
| License | `[h1]License[/h1]` | Fixed prose with the resolved licence values |

Section headings and prose are template content; never reword, retitle, reorder, or omit them.

### Conditional Sections

Each conditional section is gated by its own directive comment in the template. Include it only with evidence, and remove it together with its heading, body, and directive comment when the condition is unmet.

| Section | Condition |
|---------|-----------|
| Upgrading | The upgrade procedure requires more than repeating the installation command. |
| Requirements | More than the base game is required, such as DLC, expansions, or other mods. |
| Compatibility | Compatibility with other mods, or with a game version, is material to users. |
| Incompatible mods | One or more specific mods are known to be incompatible; otherwise the block is omitted entirely. |
| Load Order | A required load order or placement is evidenced; rendered as the `[h2]Load Order[/h2]` subsection of Compatibility. |
| Localised languages | The item ships translated text, or a localisation directory, translation files, or documented locale list exists; the language list then lives inside Compatibility. |
| FAQ | A repository FAQ document exists (`FAQ.md`, `docs/faq.md`, or `docs/FAQ.md`); the FAQ sentence then lives inside Support. |
| Related Mods | Related mods exist. |
| Troubleshooting | Recurring, evidenced problems have diagnostic procedures or resolutions; the procedures then live inside Support. |
| Additional support | An evidenced support channel, forum, discussion board, or support document exists. |

Never invent a section, a problem, or a related mod, and never emit a vacant section. `Features` is never a section, because `Capabilities` is mandatory; place capability content in the repeatable `[[CAPABILITY]]` line instead. `Known Limitations` is never a section; state limits in `Compatibility` or `Support` when they are material. `Troubleshooting`, `Localisation`, `Changelog`, and `FAQ` are never standalone sections; their content lives inside `Support` or `Compatibility` as described below. `Load Order` is never a top-level section; it is the `[h2]Load Order[/h2]` subsection of Compatibility.

### Installation Section

The Installation section contains the distribution badge block, followed by the conditional Upgrading sub-section when an upgrade requires more than repeating the installation. There is no Manual Installation or Uninstallation sub-section; the badges and the game launcher cover both.

### Requirements Section

Include the Requirements section only when more than the base game is required. When the item runs on the base game with no extra DLC, expansion, or dependency, remove the section together with its heading and directive comment, and do not emit a vacant heading.

### Compatibility Section

The Compatibility prose is fixed in the template and is used whenever it applies. It consists of gated blocks and paragraphs:

| Block | Condition |
|-----------|-----------|
| `This mod is [b]OS-agnostic[/b] and works on any operating system.` | The mod genuinely is OS-agnostic. |
| `Game version: [b][[SUPPORTED_GAME_VERSION]][/b].` | The supported game version is evidenced. The version is enclosed in `[b][/b]`, never in `[code][/code]`. |
| `The subsequent languages are currently supported:` followed by the language list | The item ships translated text, or a localisation directory, translation files, or documented locale list exists. |
| `Translations are welcome. See the GitHub repository for the translation process.` | A documented translation contribution process exists. |
| `Incompatible mods:` followed by the incompatible-mod list | One or more specific mods are known to be incompatible. Omit the whole block when none are known. |
| `[h2]Load Order[/h2]` with `[[LOAD_ORDER]]` | A required load order or placement is evidenced. |

- Start from this fixed prose rather than composing free-form compatibility text.
- Replace the OS-agnostic paragraph with the evidenced platform support when the mod is **not** OS-agnostic, for example when it ships platform-specific binaries.
- The game-version sentence is mandatory whenever a supported game version is evidenced. Never invent a version, and never widen a version range beyond what the repository or Workshop page states.
- The language list is part of Compatibility, not a separate section. Emit one `[*]` line per supported language in the form `Language (locale): status`, ordered by translation completeness from highest to lowest, using a standards-compliant locale identifier where available. Never invent a language, a locale, or a completeness figure.
- The incompatible-mod list names each known incompatible mod as `Name: reason`, and links it in priority order: its Steam Workshop page, otherwise its Nexus Mods page, otherwise its GitHub repository. Never invert it into a compatibility claim: there is no sentence asserting blanket compatibility. When no incompatibility is known, remove the entire block with its heading and directive comment.
- The fixed prose uses the inline emphasis tags `[b]OS-agnostic[/b]` and `[b][[SUPPORTED_GAME_VERSION]][/b]`. Retain them in the corresponding positions, and do not add emphasis elsewhere.
- Add evidenced DLC or dependency statements as additional sentences only when they are material, and never contradict the fixed prose.
- The prose has already passed the `english-language` dictionary; when revising it, re-apply the dictionary rather than reintroducing a recorded source word such as `should`, `such`, or `outcome`.

### Translation Status

`[[TRANSLATION_STATUS]]` must state the completeness as one of these evidenced forms:

| Status | Meaning |
|--------|---------|
| `Complete` | Every translatable string is translated. |
| `Partial (NN%)` | A proportion of the translatable strings is translated, with `NN` taken from counted keys or the documented percentage. |
| `In progress` | Translation is under way with no reliable completeness figure. |
| `Minimal` | Only a small, documented subset is translated. |
| `Planned` | A locale is declared or scaffolded but not yet translated. |

Derive the status from translation files, a documented locale list, or a translation platform. When the completeness cannot be determined for a listed locale, use `In progress` rather than a fabricated percentage.

### Support Section

The Support prose is fixed in the template and additionally carries the former Troubleshooting and FAQ content, in this order:

1. The issue-tracker sentence and the GitHub-primary sentence, which are fixed and never removed.
2. The FAQ sentence, retained only when a repository FAQ document exists. `[[FAQ_DOCUMENT_LINK]]` resolves to the verified repository-relative path of that document.
3. `[[TROUBLESHOOTING]]`, retained only when recurring, evidenced problems have diagnostic procedures or resolutions.
4. `[[ADDITIONAL_SUPPORT]]`, retained only when an additional evidenced support channel exists.

There is no standalone Troubleshooting, FAQ, Changelog, or Localisation section.

### Contributing Section

The Contributing prose is fixed in the template and directs contributors to GitHub, which is the only supported contribution channel. It links the repository, the Contributing Guidelines when `CONTRIBUTING.md` exists, and the issue tracker when one exists. There is no welcome paragraph; the section opens directly with the contributions-managed sentence.

Do not add a contribution checklist, a pull-request workflow, or any other guidance to this section; it points readers to the repository rather than duplicating repository policy.

### Related Mods Section

Each related mod uses the format `Name: description`. Resolve its link in this priority order:

1. The mod's Steam Workshop page: `https://steamcommunity.com/sharedfiles/filedetails/?id=<id>` (a Steam URL, so never link-filtered).
2. When no Steam Workshop page is known, its Nexus Mods page, wrapped in the Steam link filter.
3. When neither is known, its GitHub repository, wrapped in the Steam link filter.

Never invent a link or a related mod.

### Installation Badges

The Installation section contains a distribution badge block. Every badge follows this exact form:

```
[url=<BADGE_TARGET>][img]https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/<STORE>.png[/img][/url]
```

Rules:

- The internal path segment is invariably `/badges/stores/`, not `/badges/`, `/install_from_`, or any other location.
- A badge for the Steam Workshop item itself links directly to `https://steamcommunity.com/sharedfiles/filedetails/?id=<id>` and is never wrapped in the link filter, because it is a Steam URL.
- Every non-Steam badge target is wrapped in the link filter: `https://steamcommunity.com:/linkfilter/?url=<TARGET>`.
- At least one badge is mandatory, because this section is mandatory.
- Order the badges: Steam Workshop, Nexus Mods, Paradox Mods, GitHub, then any additional evidenced store.

Layout rules:

- A maximum of three badges per line.
- Every badge line begins with exactly four leading spaces.
- Badges on the same line are separated by exactly one space and nothing else.
- A wrapped badge line keeps the same four leading spaces and the same single space that would have separated it on the previous line, so every line but the last ends with exactly one trailing space.
- The final badge line may end with at most one trailing space.
- Never wrap or split a single badge across lines.

Reference layout with three badges on one line:

```
    [url=https://steamcommunity.com/sharedfiles/filedetails/?id=[[STEAM_WORKSHOP_ID]]][img]https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/steam-workshop.png[/img][/url] [url=https://steamcommunity.com:/linkfilter/?url=https://nexusmods.com/[[NEXUS_MODS_GAME_ID]]/mods/[[NEXUS_MODS_ID]]][img]https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/nexus.png[/img][/url] [url=https://steamcommunity.com:/linkfilter/?url=https://github.com/[[GITHUB_REPO_USERNAME]]/[[GITHUB_REPO_NAME]]/releases][img]https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/github.png[/img][/url]
```

Reference layout with a fourth badge overflowing to a second line: the first line keeps its four-space prefix, its three badges, and its single trailing space, and the second line repeats the four-space prefix for the remaining badge.

### Content Constraints

- Use BBCode only, within the Steam-tolerated subset: `[h1]`, `[h2]`, `[h3]`, `[b]`, `[i]`, `[u]`, `[list]`/`[*]`, `[url]`, `[img]`, `[table]`/`[tr]`/`[th]`/`[td]`, `[quote]`, `[code]`, `[hr][/hr]`, and `[noparse]`.
- Contain no vacant heading, no unresolved placeholder, and no template comment.
- Refrain from repeating the header or footer blocks; they are supplied by the template.
- Keep Hub-side formatting usable: no nested lists deeper than one level, no unsupported CSS, no external scripts, no broken image hosts.

### Failure Handling

- If a required value (repository URL, funding link, asset base URL, licence title, Steam Workshop identifier, or at least one distribution channel) remains indeterminate after evidence collection, cease generation and request one concise clarification question. Never invent a URL, identifier, or asset host.
- Do not produce a partial description.

### Mandatory Validation Prior to Final Output

- The output file is `description/steam-workshop.bbcode` relative to the repository root.
- The output commences with the exact header block from `templates/workshop-description.bbcode`, byte-for-byte after placeholder substitution.
- The output concludes with the exact closing donate banner from the template.
- The About, Capabilities, Installation, Contributing, Support, Project Engagement, and License sections are present, in that order, with their template headings and prose.
- The Installation section carries the badge block and no Manual Installation or Uninstallation sub-section.
- The Requirements section is present only when more than the base game is required.
- The Capabilities section carries a non-vacant list of evidenced capabilities.
- The Compatibility section carries the fixed OS-agnostic and game-version prose, the language list, the incompatible-mod list when known, and the `[h2]Load Order[/h2]` subsection when evidenced, with the game version enclosed in `[b][/b]`.
- The Compatibility section carries no blanket multi-mod compatibility claim, and no development-platform paragraph.
- The Contributing section opens with the contributions-managed sentence and carries no welcome paragraph.
- The Support section carries the issue-tracker and GitHub-primary sentences, the conditional FAQ sentence, the conditional troubleshooting procedures, and the conditional additional-support line.
- No standalone Troubleshooting, FAQ, Changelog, or Localisation section exists.
- Every included conditional block is evidenced, and every excluded block is removed entirely with its directive comment.
- No template comment or `Repeat` example remains.
- The Installation section contains at least one badge in the exact store-badge form, with at most three badges per line, a four-space prefix on every badge line, and a single trailing space on every line but the last.
- Every fixed URL, image URL, tag, and blank line from the template is present verbatim.
- Every `[[PLACEHOLDER]]` is resolved; no placeholder, template comment, or unused example remains.
- Every outbound link is wrapped in the Steam link filter, except Steam-hosted links.
- Only BBCode is used; no Markdown syntax and no literal HTML.
- No secret, credential, personal datum, or private endpoint is exposed.

If a Steam Workshop description previously exists, preserve any content that is correct and up to date, and revise only what has changed or is absent. If none exists, create one from scratch.
