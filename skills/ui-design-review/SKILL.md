---
name: ui-design-review
description: "Use when designing, building, reviewing, or repairing user interfaces, or when UI work must be verified before delivery. Covers accessibility, touch and interaction, performance, style selection, layout and responsive behaviour, typography and colour, animation, forms and feedback, navigation, and charts, with a prioritised rule set, a native and mobile pre-delivery checklist, and a browser-driven audit procedure that reports evidence-ranked findings."
---

# UI Design Review

Prioritised, evidence-based procedure for assessing and repairing interface quality across web, mobile, and desktop. The rule set is ordered by user impact so review effort is allocated where it matters, and every finding must be grounded in something observed rather than assumed.

## Invocation

Apply when the request concerns:
- designing a new page, screen, or component, or choosing a colour, typography, spacing, or layout system;
- reviewing or auditing an interface for accessibility, responsiveness, consistency, or perceived quality;
- repairing a specific UI defect such as overflow, cramped tap targets, unclear states, or poor contrast;
- implementing navigation, animation, responsive behaviour, chart rendering, or form feedback.

Do not apply to backend logic, API or database design, non-visual performance work, infrastructure, or non-visual scripting, unless the change alters how something looks, moves, feels, or is interacted with.

## Rule Priorities

Work from priority 1 downward; each priority subsumes the ones beneath it. Full rule text lives in `references/quick-reference.md` and loads on demand.

| Priority | Category | Impact | Key requirements | Anti-patterns |
|---|---|---|---|---|
| 1 | Accessibility | Critical | Contrast 4.5:1, alternative text, keyboard navigation, accessible names | Removing focus rings, icon-only controls without labels |
| 2 | Touch and interaction | Critical | 44×44 pt or 48×48 dp minimum, 8 px minimum spacing, loading feedback | Hover-only interactions, zero-duration state changes |
| 3 | Performance | High | Modern image formats, lazy loading, reserved space, layout stability | Layout thrashing, cumulative layout shift |
| 4 | Style selection | High | Product-appropriate style, consistency, vector icons | Mixed flat and skeuomorphic styling, emoji as icons |
| 5 | Layout and responsiveness | High | Mobile-first breakpoints, viewport declaration, no horizontal scroll | Fixed pixel containers, disabled zoom, horizontal scroll |
| 6 | Typography and colour | Medium | 16 px base, 1.5 line height, semantic colour tokens | Body text below 12 px, grey on grey, raw hex values in components |
| 7 | Animation | Medium | Context-appropriate timing, motion that conveys meaning, spatial continuity | One duration for every transition, animating width or height, no reduced-motion support |
| 8 | Forms and feedback | Medium | Visible labels, errors adjacent to the field, helper text, progressive disclosure | Placeholder-only labels, errors only at the top, overwhelming upfront |
| 9 | Navigation | High | Predictable back behaviour, five or fewer bottom destinations, deep linking | Overloaded navigation, broken back behaviour, no deep links |
| 10 | Charts and data | Low | Legends, tooltips, accessible colour | Colour as the sole carrier of meaning |

## Procedure

### Step 1: Establish Context

Determine before assessing anything:
- **Product type and audience** — the platform idiom and the expected interaction density.
- **Technology stack** — read the manifest (`package.json`, `pubspec.yaml`, `composer.json`, `*.xcodeproj`, `Package.swift`, or Windows desktop project files). Never presume a stack; a wrong presumption misroutes every stack-specific recommendation.
- **Platform** — web, native mobile, or desktop, because touch targets, safe areas, and gesture conventions differ.
- **Reading direction** — right-to-left interfaces change icon mirroring, carousel direction, motion paths, and chart orientation.

### Step 2: Review the Live Interface First

When a running target exists, observe it before reading source. Screenshots, console output, and measured values are the primary evidence; source code explains a defect already observed. Read code only to explain or locate a fix.

1. **Baseline** — open the interface at a desktop viewport, confirm it renders, and record console errors, which frequently explain visual defects.
2. **Interaction** — exercise the primary flow: click, open menus and dialogs, submit forms with valid and invalid input, toggle tabs and disclosures. Confirm that hover, active, disabled, loading, empty, and error states exist and differ, and that destructive actions are guarded.
3. **Responsiveness** — inspect at 375, 768, 1024, 1440, and 1920 px, capturing each tier. Look for horizontal scroll, clipped or overlapping content, media that shrinks instead of reflowing, undersized targets, and navigation that fails to collapse.
4. **Visual quality** — judge spacing rhythm, alignment, type scale, consistent radii, shadows and borders, image quality, and colour harmony.
5. **Accessibility** — traverse the interface by keyboard only. Focus must be visible, ordered, and untrapped; headings must be sequential; every control must carry a name; contrast must meet 4.5:1 for body text and 3:1 for large text and non-text elements; reduced motion must be honoured.
6. **Robustness** — stress with long strings, empty data, slow responses, and invalid input. Content must degrade gracefully rather than break the layout.
7. **Health** — recheck the console and network for failed requests, missing assets, and oversized payloads.

### Step 3: Automated Heuristic Pass

When a browser is available, run the bundled audit to obtain viewport screenshots and a baseline heuristic report before the manual pass:

```bash
node skills/ui-design-review/scripts/design-audit.mjs --url http://localhost:3000 --out audit-output
node skills/ui-design-review/scripts/design-audit.mjs --file ./index.html --out audit-output
```

The script requires Playwright and no model context. It reports horizontal overflow, unsized media, small tap targets, missing focus indicators, missing accessible names, heading structure, viewport and language declarations, console errors, and an approximate contrast count. Contrast results are approximate: treat them as leads, never as a verdict. The script exits with status 2 when high-severity findings exist, so it can gate a pipeline.

### Step 4: Stack-Specific Guidance

Apply the category requirements through the platform idiom of the detected stack, for example a native mobile toolkit, a component library with its own theming model, or a utility-first web framework. Do not transplant web rules into a native interface without checking the platform equivalents.

### Step 5: Native and Mobile Checklist

For native or mobile application interfaces, read `references/pro-rules.md` and complete its pre-delivery checklist before declaring the work finished.

## Reporting

Rank findings by severity and lead with the fix. Each finding states the observation, the principle it violates, and the remedy, in that order.

```
## Design Review — <page or URL>
**Verdict:** <deliverable / deliverable after fixes / requires revision>  ·  Viewports: 375/768/1024/1440/1920

### Blockers
- <observation> → <why it fails> → <the fix>  · evidence: <screenshot, console entry, measured value>

### High
### Medium
### Minor
### Sound Decisions
```

Rules:
- Report only what was observed. If the interface could not be opened, state this plainly and report the heuristic results alone.
- Distinguish defects from preferences; only blockers and high findings justify withholding delivery.
- State when a recommendation comes from general guidance rather than a verified match for the product and platform.
- Never reproduce credentials, personal data, or private endpoints in findings or exported reports.

## Attribution

The rule set, the pre-delivery checklist, and the audit script derive from [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), distributed under the MIT licence, Copyright (c) 2024 Next Level Builder. The prose is adapted to this repository's British English conventions. Rule identifiers retain their upstream form so findings remain traceable to that source.