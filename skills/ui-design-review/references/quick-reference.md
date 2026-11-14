# Quick Reference — Full Rule Set

Load this file for a UI review or audit pass, or when a category needs detail beyond the priority table in `SKILL.md`. Rules are grouped by the priority order used there; each entry names the rule, states the requirement, and cites the originating guidance where one applies.

## 1. Accessibility (Critical)

- `color-contrast` — Minimum 4.5:1 for normal text, 3:1 for large text (Material Design).
- `focus-states` — Visible focus rings on interactive elements, 2–4 px (Apple HIG, Material Design).
- `alt-text` — Descriptive alternative text for meaningful images.
- `aria-labels` — Accessible name for icon-only controls; `accessibilityLabel` in native interfaces (Apple HIG).
- `icon-context` — Semantics follow use, not glyph: decorative icons beside visible text are hidden from the accessibility tree, meaningful icons need a text alternative, icon controls need a name and applicable state.
- `keyboard-nav` — Tab order matches visual order; full keyboard support (Apple HIG).
- `form-labels` — Use a `label` element associated by its `for` attribute.
- `skip-links` — Skip to main content for keyboard users.
- `heading-hierarchy` — Sequential h1 to h6, no skipped level.
- `color-not-only` — Never convey information by colour alone; add an icon or text.
- `dynamic-type` — Support system text scaling; avoid truncation as text grows (Apple Dynamic Type, Material Design).
- `reduced-motion` — Honour `prefers-reduced-motion`; reduce or disable animation when requested (Apple Reduced Motion API, Material Design).
- `voiceover-sr` — Meaningful label and hint values with a logical reading order for screen readers (Apple HIG, Material Design).
- `escape-routes` — Provide cancel or back in dialogs and multi-step flows (Apple HIG).
- `keyboard-shortcuts` — Preserve system and accessibility shortcuts; offer keyboard alternatives to dragging (Apple HIG).
- `focus-not-obscured` — Sticky UI, overlays, and banners must not hide the keyboard-focused control (WCAG 2.2 AA).
- `focus-not-obscured-enhanced` — Keep the entire focused component visible (WCAG 2.2 AAA).
- `focus-appearance` — Verify indicator area and 3:1 state contrast; a visible focus ring alone is insufficient (WCAG 2.2 AAA).
- `dragging-alternative` — Every author-controlled drag action needs a single-pointer and keyboard alternative (WCAG 2.2 AA).
- `web-target-size` — Web pointer targets need 24×24 CSS px or a documented exception; do not substitute native units (WCAG 2.2 AA).
- `consistent-help` — Repeated help mechanisms stay in the same relative order across a set of pages (WCAG 2.2 A).
- `redundant-entry` — Reuse information already supplied in the same process unless re-entry is essential (WCAG 2.2 A).
- `accessible-authentication` — Allow password managers and paste, and provide a non-cognitive authentication path (WCAG 2.2 A and AA). The enhanced AAA criterion is not represented.
- `auto-rotation-controls` — Carousels and moving content need pause or stop controls and must stop on focus or reduced motion (WAI).
- `contextual-live-badge-updates` — Announce a changed count or status as a complete contextual phrase without moving focus; use one appropriate live status region and atomic updates only when needed.

## 2. Touch and Interaction (Critical)

- `touch-target-size` — Minimum 44×44 pt (Apple) or 48×48 dp (Material); extend the hit area beyond the visual bounds when needed.
- `touch-spacing` — Minimum 8 px or 8 dp between targets (Apple HIG, Material Design).
- `hover-vs-tap` — Use click or tap for primary interactions; never rely on hover alone.
- `loading-buttons` — Disable the control during an asynchronous operation and show progress.
- `error-feedback` — Clear error messages near the problem.
- `cursor-pointer` — Add a pointer cursor to clickable elements on the web.
- `gesture-conflicts` — Avoid horizontal swipe on main content; prefer vertical scroll.
- `tap-delay` — Use `touch-action: manipulation` to reduce the inherited tap delay on the web.
- `standard-gestures` — Use platform-standard gestures consistently; never redefine swipe-back or pinch-zoom (Apple HIG).
- `system-gestures` — Do not block system gestures (Apple HIG).
- `press-feedback` — Visual feedback on press: ripple or highlight (Material state layers).
- `haptic-feedback` — Use haptics for confirmations and important actions; avoid overuse (Apple HIG).
- `gesture-alternative` — Never rely on gesture-only interaction; provide visible controls for critical actions.
- `safe-area-awareness` — Keep primary targets away from the notch, cutout, gesture bar, and screen edges.
- `no-precision-required` — Avoid interaction that demands pixel-accurate taps.
- `swipe-clarity` — Swipe actions must show an affordance or hint.
- `drag-threshold` — Apply a movement threshold before starting a drag.

## 3. Performance (High)

- `image-optimization` — Use modern formats (WebP, AVIF), responsive sources (`srcset`, `sizes`), and lazy loading for non-critical assets.
- `image-dimension` — Declare width and height or use `aspect-ratio` to prevent layout shift.
- `font-loading` — Use `font-display: swap` or `optional` to avoid invisible text; reserve space to reduce layout shift (Material Design).
- `font-preload` — Preload only critical fonts; avoid preloading every variant.
- `critical-css` — Prioritise above-the-fold styles, inline or loaded early.
- `lazy-loading` — Lazy load non-hero components through dynamic import or route-level splitting.
- `bundle-splitting` — Split code by route or feature to reduce initial load and time to interactive.
- `third-party-scripts` — Load third-party scripts asynchronously or deferred; remove unnecessary ones (Material Design).
- `reduce-reflows` — Batch layout reads before writes; avoid frequent read/write alternation.
- `content-jumping` — Reserve space for asynchronous content.
- `lazy-load-below-fold` — Use `loading="lazy"` for below-the-fold images and heavy media.
- `virtualize-lists` — Virtualise lists of 50 or more items.
- `main-thread-budget` — Keep per-frame work under roughly 16 ms; move heavy tasks off the main thread (Apple HIG, Material Design).
- `progressive-loading` — Use skeleton placeholders instead of long blocking spinners for operations exceeding one second (Apple HIG).
- `input-latency` — Keep input latency under roughly 100 ms (Material responsiveness standard).
- `tap-feedback-speed` — Provide visual feedback within 100 ms of a tap (Apple HIG).
- `debounce-throttle` — Debounce or throttle high-frequency events such as scroll, resize, and input.
- `offline-support` — Provide offline messaging and a basic fallback where applicable.
- `network-fallback` — Offer degraded modes for slow networks.

## 4. Style Selection (High)

- `style-match` — Match the style to the product type.
- `consistency` — Use the same style across all pages and screens.
- `no-emoji-icons` — Use vector icons, never emoji, as structural icons.
- `color-palette-from-product` — Choose the palette from the product and industry context.
- `effects-match-style` — Align shadows, blur, and radii with the chosen style.
- `platform-adaptive` — Respect platform idioms for navigation, controls, typography, and motion.
- `state-clarity` — Make hover, pressed, and disabled states visually distinct while staying on-style (Material state layers).
- `elevation-consistent` — Use a consistent elevation scale for cards, sheets, and dialogs; avoid arbitrary shadow values.
- `dark-mode-pairing` — Design light and dark variants together to keep brand, contrast, and style consistent.
- `icon-style-consistent` — Use one icon family and visual language across the product.
- `system-controls` — Prefer native controls; customise only where branding requires it (Apple HIG).
- `blur-purpose` — Use blur to signal background dismissal, not as decoration (Apple HIG).
- `primary-action` — One primary action per screen; subordinate secondary actions (Apple HIG).

## 5. Layout and Responsive (High)

- `viewport-meta` — Declare `width=device-width, initial-scale=1`; never disable zoom.
- `mobile-first` — Design mobile-first, then scale up.
- `breakpoint-consistency` — Use systematic breakpoints, for example 375, 768, 1024, and 1440 px.
- `readable-font-size` — Minimum 16 px body text on mobile, which also avoids automatic zoom on iOS.
- `line-length-control` — 35–60 characters per line on mobile, 60–75 on desktop.
- `horizontal-scroll` — No horizontal scroll on mobile; content must fit the viewport width.
- `spacing-scale` — Use a 4 pt or 8 dp incremental spacing system (Material Design).
- `touch-density` — Keep component spacing comfortable for touch: neither cramped nor wasteful.
- `container-width` — Consistent maximum width on desktop.
- `z-index-management` — Define a layered z-index scale rather than arbitrary values.
- `fixed-element-offset` — Fixed bars must reserve padding for the content beneath them.
- `scroll-behavior` — Avoid nested scroll regions that compete with the main scroll.
- `viewport-units` — Prefer `dvh` units over `100vh` on mobile.
- `orientation-support` — Keep the layout readable and operable in landscape.
- `content-priority` — Show core content first on mobile; fold or hide secondary content.
- `visual-hierarchy` — Establish hierarchy through size, spacing, and contrast rather than colour alone.
- `compact-label-overflow` — Choose badge, status tag, filter chip, or removable value from its semantics; keep essential labels available and disclose unavoidable truncation to pointer and keyboard users.
- `chip-collection-reflow` — Wrap a collection before shrinking labels; make a `+n` overflow summary an operable disclosure rather than hiding values.

## 6. Typography and Colour (Medium)

- `line-height` — Use 1.5 to 1.75 for body text.
- `line-length` — Limit to 65–75 characters per line.
- `font-pairing` — Match heading and body font personalities.
- `font-scale` — Use a consistent type scale, for example 12, 14, 16, 18, 24, 32 px.
- `contrast-readability` — Darker text on light backgrounds.
- `text-styles-system` — Use the platform type system: iOS Dynamic Type styles, or Material type roles such as display, headline, title, body, and label.
- `weight-hierarchy` — Reinforce hierarchy with weight: 600–700 for headings, 400 for body, 500 for labels (Material Design).
- `color-semantic` — Define semantic colour tokens such as primary, secondary, error, surface, and on-surface rather than raw hex values in components.
- `color-dark-mode` — Dark mode uses desaturated or lighter tonal variants, not inverted colours; test contrast separately (Apple HIG, Material Design).
- `color-accessible-pairs` — Foreground and background pairs must meet 4.5:1 (AA) or 7:1 (AAA); verify with a tool (WCAG, Material Design).
- `color-not-decorative-only` — Functional colour such as error red or success green must be accompanied by an icon or text.
- `truncation-strategy` — Prefer wrapping over truncation; when truncating, use an ellipsis and expose the full text through a tooltip or expansion (Apple HIG).
- `letter-spacing` — Respect per-platform default tracking; avoid tight tracking on body text (Apple HIG, Material Design).
- `number-tabular` — Use tabular or monospaced figures for data columns, prices, and timers to prevent layout shift.
- `whitespace-balance` — Use whitespace deliberately to group and separate, avoiding visual clutter (Apple HIG).
- `heading-line-balance` — Use balanced wrapping on short headings as a progressive, user-agent-controlled heuristic; keep natural wrapping readable and never force final words together with blanket nonbreaking spaces.
- `long-token-wrapping` — Let URLs, identifiers, and user content reflow with `overflow-wrap: anywhere` and a shrinkable flex or grid text child; do not apply `word-break: break-all` to ordinary prose.

## 7. Animation (Medium)

- `duration-timing` — Choose shared motion tokens by distance, complexity, platform, and user context; verify that feedback stays responsive instead of treating one duration range as universal.
- `transform-performance` — Animate transform and opacity only; avoid animating width, height, top, or left.
- `loading-states` — Match feedback to the expected wait; avoid flashing indicators for near-instant work and unexplained waits for slow work.
- `excessive-motion` — Animate at most one or two key elements per view.
- `easing` — Decelerate on arrival, accelerate on departure, and use linear motion only for genuinely constant-rate progress or rotation.
- `motion-meaning` — Every animation expresses a cause-effect relationship rather than decoration (Apple HIG).
- `state-transition` — State changes animate smoothly rather than snapping.
- `continuity` — Screen transitions maintain spatial continuity through shared elements or directional slides (Apple HIG).
- `parallax-subtle` — Use parallax sparingly, honour reduced motion, and never cause disorientation (Apple HIG).
- `spring-physics` — Prefer spring or physics-based curves for natural feel (Apple HIG).
- `exit-faster-than-enter` — Exit animations run at roughly 60–70 per cent of the entrance duration (Material Design).
- `stagger-sequence` — Stagger item entrance by 30–50 ms; avoid all-at-once or sluggish reveals (Material Design).
- `shared-element-transition` — Use shared element or hero transitions for visual continuity between screens.
- `interruptible` — Animations must be interruptible; a tap or gesture cancels the running animation immediately (Apple HIG).
- `no-blocking-animation` — Never block input during an animation; the interface stays interactive (Apple HIG).
- `fade-crossfade` — Use crossfade for content replacement within the same container (Material Design).
- `scale-feedback` — Apply a subtle scale of 0.95 to 1.05 on press for tappable elements and restore it on release.
- `gesture-feedback` — Drag, swipe, and pinch must track the pointer in real time (Material Motion).
- `hierarchy-motion` — Use translate and scale direction to express hierarchy: enter from below for deeper content, exit upward for back (Material Design).
- `motion-consistency` — Unify duration and easing tokens globally so all animation shares one rhythm.
- `opacity-threshold` — Fading elements should not linger below 0.2 opacity; fade fully or remain visible.
- `modal-motion` — Dialogs and sheets animate from their trigger source for spatial context (Apple HIG, Material Design).
- `navigation-direction` — Forward navigation animates left or up, backward animates right or down, consistently (Apple HIG).
- `layout-shift-avoid` — Animation must not cause reflow or layout shift; use transform for position changes.
- `cancellable-state-transitions` — Rapid state changes must cancel or replace the prior micro-interaction safely, set the final state explicitly, and never depend on an animation-end event for correctness.

## 8. Forms and Feedback (Medium)

- `input-labels` — Every input carries a visible label, not a placeholder substitute.
- `error-placement` — Show a specific error below the related field and connect it with `aria-describedby`.
- `submit-feedback` — Show loading, then success or error, on submit.
- `ime-composition-enter` — For custom Enter shortcuts on the web, cancel the handled default before the composition guard; keep input-method confirmation separate from submission, preserve newline and modifier policy, and provide an explicit submit control.
- `required-indicators` — Mark required fields.
- `empty-states` — Provide a helpful message and an action when no content exists.
- `toast-dismiss` — Auto-dismiss toasts after three to five seconds.
- `confirmation-dialogs` — Confirm before destructive actions.
- `input-helper-text` — Provide persistent helper text below complex inputs (Material Design).
- `disabled-states` — Disabled elements use reduced opacity of 0.38 to 0.5, a cursor change, and a semantic attribute (Material Design).
- `progressive-disclosure` — Reveal complex options progressively (Apple HIG).
- `inline-validation` — Validate on blur, not on every keystroke (Material Design).
- `input-type-keyboard` — Use semantic input types so mobile shows the correct keyboard.
- `password-toggle` — Provide a show and hide toggle for password fields (Material Design).
- `autofill-support` — Use `autocomplete` and `textContentType` so the system can fill values.
- `undo-support` — Allow undo for destructive or bulk actions (Apple HIG).
- `success-feedback` — Confirm completed actions with brief visual feedback (Material Design).
- `error-recovery` — Error messages include a recovery path: retry, edit, or help.
- `multi-step-progress` — Show a step indicator or progress bar and allow going back (Material Design).
- `form-autosave` — Long forms auto-save drafts to prevent data loss.
- `sheet-dismiss-confirm` — Confirm before dismissing a sheet or dialog with unsaved changes (Apple HIG).
- `error-clarity` — Errors state cause and remedy, not merely that input is invalid.
- `field-grouping` — Group related fields with a fieldset and legend, or clear visual grouping (Material Design).
- `read-only-distinction` — Read-only must be visually and semantically distinct from disabled (Material Design).
- `focus-management` — After a failed submission with multiple errors, focus the error summary; without a summary, focus the first invalid field.
- `error-summary` — Place a focusable summary at the top after a failed submission, link each item to its field, and retain inline errors.
- `touch-friendly-input` — Mobile inputs are at least 44 px high (Apple HIG).
- `destructive-emphasis` — Destructive actions use the semantic danger colour and are visually separated from primary actions.
- `toast-accessibility` — Toasts must not steal focus; announce them with `aria-live="polite"` (WCAG).
- `aria-live-errors` — Form errors use a live region or `role="alert"` (WCAG).
- `contrast-feedback` — Error and success colours meet 4.5:1 (WCAG, Material Design).
- `timeout-feedback` — A request timeout shows clear feedback with a retry option (Material Design).

## 9. Navigation (High)

- `bottom-nav-limit` — At most five bottom destinations, each with an icon and label (Material Design).
- `drawer-usage` — Use a drawer for secondary navigation, never for primary actions (Material Design).
- `back-behavior` — Back navigation is predictable and preserves scroll and state (Apple HIG, Material Design).
- `deep-linking` — Every key screen is reachable by link or URL (Apple HIG, Material Design).
- `tab-bar-ios` — Use a bottom tab bar for top-level navigation on iOS (Apple HIG).
- `top-app-bar-android` — Use a top app bar with a navigation icon as the primary structure on Android (Material Design).
- `nav-label-icon` — Navigation items carry both icon and text label; icon-only navigation harms discoverability (Material Design).
- `nav-state-active` — Highlight the current location through colour, weight, or indicator.
- `nav-hierarchy` — Separate primary navigation from secondary navigation clearly (Material Design).
- `modal-escape` — Dialogs and sheets offer a clear dismissal affordance, including swipe-down on mobile (Apple HIG).
- `search-accessible` — Search is easily reachable and offers recent or suggested queries (Material Design).
- `breadcrumb-web` — Use breadcrumbs for hierarchies three or more levels deep (Material Design).
- `state-preservation` — Returning back restores scroll position, filters, and input.
- `gesture-nav-support` — Support system gesture navigation without conflict (Apple HIG, Material Design).
- `tab-badge` — Use badges sparingly for unread or pending state and clear them on visit.
- `overflow-menu` — Move excess actions into an overflow menu rather than cramming.
- `bottom-nav-top-level` — Bottom navigation serves top-level screens only; never nest sub-navigation within it (Material Design).
- `adaptive-navigation` — Prefer a sidebar at 1024 px and above and bottom or top navigation below that (Material Adaptive).
- `back-stack-integrity` — Never silently reset the navigation stack or jump to the home screen (Apple HIG, Material Design).
- `navigation-consistency` — Navigation placement stays the same across all pages.
- `avoid-mixed-patterns` — Do not mix tab, sidebar, and bottom navigation at the same hierarchy level.
- `modal-vs-navigation` — Dialogs must not carry primary navigation flows (Apple HIG).
- `focus-on-route-change` — Move focus to the main region after a page transition (WCAG).
- `persistent-nav` — Core navigation remains reachable from deep pages (Apple HIG, Material Design).
- `destructive-nav-separation` — Dangerous actions are visually and spatially separated from ordinary navigation items.
- `empty-nav-state` — When a destination is unavailable, explain why rather than hiding it (Material Design).

## 10. Charts and Data (Low)

- `chart-type` — Match the chart to the data: line for trend, bar for comparison, pie or donut for proportion.
- `color-guidance` — Use accessible palettes; avoid red and green alone as a pair (WCAG, Material Design).
- `data-table` — Provide a table alternative; charts alone are not accessible (WCAG).
- `pattern-texture` — Supplement colour with pattern, texture, or shape so data is distinguishable without colour.
- `legend-visible` — Always show a legend, positioned near the chart rather than below a fold (Material Design).
- `tooltip-on-interact` — Provide tooltips or data labels showing exact values on hover or tap.
- `axis-labels` — Label axes with units and a readable scale; avoid truncated or rotated labels on mobile.
- `responsive-chart` — Charts reflow or simplify on small screens (Material Design).
- `empty-data-state` — Show a meaningful empty state with guidance, not a blank chart (Material Design).
- `loading-chart` — Use a skeleton instead of an empty axis frame while data loads.
- `animation-optional` — Chart entrance animation honours reduced motion; data is readable immediately (Apple HIG).
- `large-dataset` — Aggregate or sample beyond roughly one thousand points and offer drill-down (Material Design).
- `number-formatting` — Format numbers, dates, and currencies for the reader's locale (Apple HIG, Material Design).
- `touch-target-chart` — Interactive chart elements have at least a 44 pt tap area or expand on touch (Apple HIG).
- `no-pie-overuse` — Avoid pie or donut charts beyond five categories; switch to a bar chart.
- `contrast-data` — Data marks meet 3:1 against the background; data labels meet 4.5:1 (WCAG).
- `legend-interactive` — Legends toggle series visibility (Material Design).
- `direct-labeling` — For small datasets, label values directly to reduce eye travel.
- `tooltip-keyboard` — Tooltip content is keyboard-reachable and never hover-only (WCAG).
- `sortable-table` — Data tables support sorting with `aria-sort` reflecting the current state (WCAG).
- `axis-readability` — Axis ticks are not cramped; skip ticks automatically on small screens.
- `data-density` — Limit information density per chart and split into several charts when needed.
- `trend-emphasis` — Emphasise the trend over decoration; avoid heavy gradients and shadows that obscure the data.
- `gridline-subtle` — Keep grid lines low-contrast so they do not compete with the data.
- `focusable-elements` — Interactive data marks are keyboard-navigable (WCAG).
- `screen-reader-summary` — Provide a text summary or accessible name describing the chart's key insight (WCAG).
- `error-state-chart` — A load failure shows an error message with a retry action, not a broken or empty chart.
- `export-option` — Offer data export where the product is data-heavy.
- `drill-down-consistency` — Drill-down preserves a clear path back and a hierarchy breadcrumb.
- `time-scale-clarity` — Time series label their granularity and allow switching it.