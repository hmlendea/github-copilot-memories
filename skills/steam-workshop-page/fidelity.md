# Steam Workshop Description Template Fidelity

This rule applies **only to personal repositories owned by the current git user** — repositories whose GitHub owner is a personal account (`owner.type == "User"`) and whose owner matches the current git user. Organisation-owned repositories and repositories owned by another user are out of strict-fidelity scope; fixed template fidelity is not enforced for them. Confirm repository ownership prior to generating or revising a Workshop description:

```bash
git -C <repo_root> remote get-url origin
gh api repos/<owner>/<repo> --jq .owner.type   # must return "User"
gh api user --jq .login                        # current git user; fallback: git config github.user
```

When the user explicitly requests the template, this rule applies regardless of who owns the repository or whether it is personal.

When generating or revising a Steam Workshop page description from the template, the following rule is absolute.

## Fixed Content Is Immutable

**All template content outside of `[[PLACEHOLDER]]` tokens must be copied byte-for-byte into the output.** This includes:

- The initial banner line: the header animation, the funding button, and the repository button, in that order
- The blank lines separating the header line, the announcement image, and the body
- Every image URL, including the `i.imgur.com` assets, the hardcoded `raw.githubusercontent.com/hmlendea/more-cultural-names/master/assets/en/` donation-asset base, and the donation banners
- Every link wrapper, including `https://steamcommunity.com:/linkfilter/?url=`
- The stray space within the header's first `[/url]` chain
- The closing donate banner as the final content block
- The output file location and name: `description/steam-workshop.bbcode` in the repository root
- The fixed section headings `[h1]About[/h1]`, `[h1]Capabilities[/h1]`, `[h1]Installation[/h1]`, `[h1]Support[/h1]`, `[h1]Project Engagement[/h1]`, and `[h1]License[/h1]`, in that order, plus `[h1]Contributing[/h1]` when the section is included
- The fixed Contributing guidelines sentence, when the section is included
- The License sentence structure: `This project is being distributed under the [url=<LICENSE_URL>]<LICENCE>[/url]<suffix>.`, with no separate licence sentence
- The fixed Compatibility sentence `This mod is compatible with <GAME_NAME> <SUPPORTED_GAME_VERSION> on all operating systems.`, when the section is included, with no emphasis tags on the version
- The `[h2]Load Order[/h2]` subsection of Compatibility, when evidenced
- The incompatible-mod list block, or its full omission when no incompatibility is known
- The fixed Support issue-tracker sentence: `For support, please [url=<ISSUES_URL>]submit an issue[/url] on [url=<REPOSITORY_URL>]GitHub[/url]. None of the other channels are actively monitored, which may result in delayed responses.`
- The fixed Support FAQ sentence, when included: `See the [url=<FAQ_URL>]FAQ[/url] for responses to frequent inquiries.`
- The fixed Support troubleshooting sentence, when included: `See the [url=<TROUBLESHOOTING_URL>]Troubleshooting Guide[/url] for diagnostic procedures and resolutions to recurring problems.`
- The fixed License sentence: `This mod is distributed under the [url=<LICENSE_URL>]<LICENCE>[/url]<suffix>.`
- The introductory sentence of every included conditional block, such as the Compatibility sentence `The subsequent languages are currently supported:`
- The store-badge URL prefix `https://raw.githubusercontent.com/hmlendea/readme-assets/master/badges/stores/`
- Trailing newline behaviour exactly as written in the template

## What May Change

Only these elements may be modified during generation:

1. **Scalar placeholders** — `[[UPPER_SNAKE_CASE]]` tokens replaced with single evidence-based values
2. **Content placeholders** — `[[ABOUT]]`, `[[CAPABILITY]]`, `[[INSTALLATION_BADGES]]`, `[[UPGRADE_INSTRUCTIONS]]`, `[[REQUIREMENTS]]`, `[[GAME_NAME]]`, `[[SUPPORTED_GAME_VERSION]]`, `[[LANGUAGE]]`, `[[LOCALE_CODE]]`, `[[TRANSLATION_STATUS]]`, `[[INCOMPATIBLE_MOD_URL]]`, `[[INCOMPATIBLE_MOD_NAME]]`, `[[INCOMPATIBLE_MOD_REASON]]`, `[[LOAD_ORDER]]`, `[[TROUBLESHOOTING_DOCUMENT_LINK]]`, `[[FAQ_DOCUMENT_LINK]]`, `[[RELATED_MOD_URL]]`, and the remaining evidenced-content tokens expanded per the rules
3. **Repeatable examples** — a line marked `<!-- Repeat ... -->` duplicated once per evidenced record, then stripped of its example placeholder
4. **Conditional blocks** — an `<!-- Only if ... -->` block included or removed in its entirety, including its heading, body, and directive comment
5. **Template comments** — every `<!-- ... -->` comment stripped from the delivered description
6. **Fixed URLs inside link filters** — only the resolved target of the placeholder changes; the filter prefix and wrapper never change

`[[FUNDING_URL]]` and `[[DONATE_PAGE_URL]]` are distinct template positions. The first drives the header button and the announcement banner; the second drives the closing banner only. They resolve to the same value only when the author has no separate donation page.

`[[ADDITIONAL_SUPPORT]]` and every `<!-- Only if ... -->` block are removed together with their surrounding blank lines when their condition is unmet; they never become vacant sections. A `<!-- Repeat ... -->` line is duplicated only for evidenced records and never survives as an example placeholder.

## What Must Never Change

- ❌ Removing, reordering, or truncating the header or footer blocks
- ❌ Removing, reordering, or retitling the mandatory About, Capabilities, Installation, Contributing, Support, Project Engagement, or License section
- ❌ Rewording the Contributing, Support, Project Engagement, or License prose
- ❌ Reinstating the removed Contributing contributions-managed or issue-tracker sentence
- ❌ Dropping the merged Support sentence's GitHub-primary clause or reinstating it as the superseded standalone sentence
- ❌ Emitting a separate licence sentence, or any `for additional information` sentence, in the License section
- ❌ Reinstating the removed development-platform paragraph, the removed blanket multi-mod compatibility claim, or a dictionary source word such as `should`, `such`, or `outcome`
- ❌ Promoting `Load Order` to a top-level section, or reinstating the removed Contributing welcome paragraph
- ❌ Reinstating the removed game-version line, the removed OS-agnostic paragraph, or enclosing a version in `[code][/code]`
- ❌ Emitting the Requirements section when only the base game is required
- ❌ Changing the store-badge path from `/badges/stores/` to any other location
- ❌ Placing more than three badges on one line, distributing badges unevenly across lines, omitting the four-space prefix, or dropping the single trailing space on a wrapped badge line
- ❌ "Correcting" `https://steamcommunity.com:/linkfilter/?url=` into a plain URL
- ❌ Removing the space after the first header button's `[/img]`
- ❌ Rewording or reformatting fixed template content
- ❌ Rewording the unified compatibility sentence or adding emphasis inside it
- ❌ Emitting a standalone Troubleshooting, FAQ, Changelog, or Localisation section, or a Manual Installation or Uninstallation sub-section
- ❌ Writing the description to any path or file name other than `description/steam-workshop.bbcode`
- ❌ Adding content prior to the header or subsequently to the closing banner
- ❌ Replacing BBCode with Markdown or HTML
- ❌ Changing the fixed `i.imgur.com` asset identifiers

## Synchronisation

When the Workshop description is committed to the repository, update the README section that documents Workshop publication and any packaging documentation that references the page body. Preserve each document's template-defined heading, fixed prose, order, and whitespace, and replace only permitted placeholders or conditional content.

## Enforcement

This rule is validated by the `steam-workshop-page` skill. Any output that alters the fixed header or footer blocks will be rejected and must be regenerated from the exact template source.