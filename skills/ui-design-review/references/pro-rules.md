# App UI Rules and Pre-Delivery Checklist

Load this file before delivering native or mobile application interfaces, or when an interface is reported as unprofessional and the cause is not evident from the priority table in `SKILL.md`.

**Scope:** every rule below targets native and mobile application interfaces. Web and desktop work uses `quick-reference.md`, because these tables presume touch targets, safe areas, and platform gesture conventions that do not transfer to pointer-driven layouts one to one.

These are frequently overlooked issues that make an interface appear unprofessional.

## Icons and Visual Elements

| Rule | Requirement | Avoid | Why it matters |
|---|---|---|---|
| No emoji as structural icons | Use vector icons. | Emoji for navigation, settings, or system controls. | Emoji rendering depends on the installed font, differs per platform, and cannot be controlled through design tokens. |
| Vector-only assets | Use SVG or platform vector icons that scale and support theming. | Raster icons that blur or pixelate. | Guarantees scalability, crisp rendering, and theme adaptability. |
| Contextual semantics | Derive semantics from use: hide decorative icons beside visible text from the accessibility tree, give meaningful standalone icons a text alternative, and give icon controls a name plus applicable selected, pressed, or expanded state. | Treating one icon name as permanently decorative, meaningful, or interactive. | The same glyph serves different purposes in different components. |
| Stable interaction states | Use colour, opacity, or elevation transitions for press states without changing layout bounds. | Layout-shifting transforms that move surrounding content or cause jitter. | Preserves smooth motion and perceived quality on mobile. |
| Correct brand logos | Use official assets and follow their usage guidelines for spacing, colour, and clear space. | Guessing paths, recolouring unofficially, or altering proportions. | Prevents brand misuse and platform compliance breaches. |
| Consistent icon sizing | Define icon sizes as tokens, for example small, medium at 24 pt, and large. | Arbitrary values such as 20, 24, and 28 pt mixed at random. | Maintains rhythm and hierarchy. |
| Stroke consistency | Keep one stroke width within a visual layer. | Mixing thick and thin strokes arbitrarily. | Inconsistent strokes reduce perceived polish. |
| Filled versus outline discipline | Use one icon style per hierarchy level. | Mixing filled and outline icons at the same level. | Preserves semantic clarity and stylistic coherence. |
| Touch target minimum | At least 44 pt on iOS and 48 dp on Android; expand the hit area when the visual icon is smaller. | Small icons without an expanded tap area, or one unit reused across platforms. | Matches platform guidance. |
| Icon alignment | Align icons to the text baseline with consistent padding. | Misaligned icons or uneven spacing. | Prevents subtle imbalance that lowers perceived quality. |
| Icon contrast | Meaningful icons and control boundaries need at least 3:1 against adjacent colours; decorative icons must carry no information. | Low-contrast icons that convey meaning or state. | Applies the non-text contrast requirement rather than a text-size rule. |

## Interaction

| Rule | Do | Do not |
|---|---|---|
| Tap feedback | Provide clear pressed feedback through ripple, opacity, or elevation within 80–150 ms. | Leave a tap without a visual response. |
| Animation timing | Use shared tokens chosen for distance, complexity, platform, and context. | Copy one duration and easing to every transition. |
| Accessibility focus | Keep screen-reader focus order identical to visual order with descriptive labels. | Leave controls unlabelled or focus traversal confusing. |
| Disabled state clarity | Use disabled semantics with reduced emphasis and no tap action. | Present controls that look tappable but do nothing. |
| Touch target minimum | Keep tap areas at least 44×44 pt on iOS or 48×48 dp on Android, expanding the hit area where the icon is smaller. | Use tiny targets or icon-only hit areas without padding. |
| Gesture conflict prevention | Keep one primary gesture per region and avoid nested tap or drag conflicts. | Overlap gestures so actions occur accidentally. |
| Semantic native controls | Prefer native interactive primitives with proper roles. | Use a generic container as a primary control without semantics. |

## Light and Dark Mode Contrast

| Rule | Do | Do not |
|---|---|---|
| Surface readability in light mode | Separate cards and surfaces from the background with sufficient opacity or elevation. | Use transparency so strong that hierarchy blurs. |
| Text contrast in light mode | Maintain at least 4.5:1 for body text against light surfaces. | Use low-contrast grey body text. |
| Text contrast in dark mode | Maintain at least 4.5:1 for normal text against dark surfaces; 3:1 applies only to large text and non-text elements. | Let muted normal text fall below the text threshold. |
| Border and divider visibility | Keep separators visible in both themes. | Define theme-specific borders that vanish in one mode. |
| State contrast parity | Keep pressed, focused, and disabled states equally distinguishable in both themes. | Define interaction states for one theme only. |
| Token-driven theming | Map semantic colour tokens per theme across surfaces, text, and icons. | Hardcode per-screen hex values. |
| Scrim and dialog legibility | Measure the composed result and use a scrim strong enough to isolate foreground content. | Reuse one opacity without checking the actual background. |

## Layout and Spacing

| Rule | Do | Do not |
|---|---|---|
| Safe-area compliance | Respect top and bottom safe areas for fixed headers, tab bars, and action bars. | Place fixed UI under the notch, status bar, or gesture area. |
| System bar clearance | Add space for status and navigation bars and the home indicator. | Let tappable content collide with system chrome. |
| Consistent content width | Keep a predictable content width per device class. | Mix arbitrary widths between screens. |
| 8 dp spacing rhythm | Use a consistent 4 or 8 dp system for padding, gaps, and section spacing. | Use random spacing increments without rhythm. |
| Readable text measure | Keep long-form text readable on large devices. | Run paragraphs edge to edge on tablets. |
| Section spacing hierarchy | Define clear vertical rhythm tiers, for example 16, 24, 32, and 48 dp by hierarchy. | Give similar levels inconsistent spacing. |
| Adaptive gutters | Increase horizontal insets at larger widths and in landscape. | Keep one narrow gutter for every size and orientation. |
| Scroll and fixed element coexistence | Add content insets so lists are not hidden behind fixed bars. | Let sticky headers or footers obscure scroll content. |

## Pre-Delivery Checklist

Verify every item before delivering application interface code. Begin with the process steps, then the per-area items.

### Process

- [ ] Ran only searches relevant to this interface.
- [ ] Reviewed categories 1 to 3 of `quick-reference.md` as a final pass.
- [ ] Tested at 375 px and in landscape orientation.
- [ ] Verified behaviour with reduced motion enabled and with the largest system text size.
- [ ] Checked dark mode contrast independently rather than assuming light-mode values carry over.
- [ ] Confirmed all touch targets reach 44 pt and that no content hides behind safe areas.

### Visual Quality

- [ ] No emoji used as icons.
- [ ] All icons come from one family and style.
- [ ] Official brand assets are used with correct proportions and clear space.
- [ ] Pressed states do not shift layout bounds or cause jitter.
- [ ] Semantic theme tokens are used consistently, with no ad-hoc per-screen colours.

### Interaction

- [ ] All tappable elements give clear pressed feedback.
- [ ] Touch targets meet the platform minimum of 44×44 pt on iOS or 48×48 dp on Android.
- [ ] Micro-interaction timing uses shared, platform-appropriate tokens and stays responsive.
- [ ] Disabled states are visually clear and non-interactive.
- [ ] Screen-reader focus order matches visual order and interactive labels are descriptive.
- [ ] Gesture regions avoid nested or conflicting interactions.

### Light and Dark Mode

- [ ] Primary text contrast reaches 4.5:1 in both modes.
- [ ] Normal primary and secondary text contrast reaches 4.5:1 in both modes.
- [ ] Dividers, borders, and interaction states are distinguishable in both modes.
- [ ] Dialog and drawer scrims are measured against the real background and preserve foreground legibility.
- [ ] Both themes were tested rather than inferred from one.

### Layout

- [ ] Safe areas are respected for headers, tab bars, and bottom action bars.
- [ ] Scroll content is not hidden behind fixed or sticky bars.
- [ ] Verified on a small phone, a large phone, and a tablet, in both orientations.
- [ ] Horizontal insets adapt to device size and orientation.
- [ ] The 4 or 8 dp rhythm holds at component, section, and page level.
- [ ] Long-form text measure stays readable on larger devices.

### Accessibility

- [ ] Decorative icons beside visible text are hidden from the accessibility tree.
- [ ] Meaningful images and icons without equivalent visible text have a text alternative.
- [ ] Icon controls have an accessible name and announce applicable state.
- [ ] Form fields have labels, hints, and clear error messages.
- [ ] Colour is never the only indicator.
- [ ] Reduced motion and dynamic text size are supported without layout breakage.
- [ ] Sticky UI and overlays do not obscure keyboard focus.
- [ ] Dragging and swipe-only interactions have button or keyboard alternatives.
- [ ] Authentication allows password managers and paste, with a non-cognitive alternative.
- [ ] Auto-rotating content has pause or stop controls and stops on focus or reduced motion.
- [ ] Failed forms retain inline field errors, and multi-error forms focus a linked error summary after submission.