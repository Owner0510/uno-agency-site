# Animation & interaction polish — design

## Context

Reference: https://increate.ca — dark, heavily-animated agency site built on
WordPress + GSAP 3.12.7 + ScrollTrigger + SplitText (Club GreenSock) +
MotionPathPlugin. Goal: bring UNO Agency's animation/interaction quality to
the same polish level, without adopting its structure or its paid GSAP
plugins.

Current state (`index.html`, `eng/index.html` — two near-duplicate static
HTML files, no JS animation library):
- `.reveal` class: `opacity:0; transform:translateY(18px)`, faded in via a
  single `IntersectionObserver` (index.html:1669) with a plain CSS
  `transition`. No stagger, no easing curve beyond default `ease`.
- Buttons/cards have simple `background`/`transition:.2s` hover, no
  lift/shadow/icon motion.
- No JS animation dependency of any kind today.

## Scope

**In scope:** animation and micro-interaction quality only. Keep the
existing page structure, sections, and content (hero → services → founders
→ case studies → reviews → FAQ → contact → footer) exactly as-is.

**Out of scope (explicit, user-confirmed):** copying increate.ca's
structure — vertical section labels, portfolio-hover-reveal cards,
sticky/pinned scroll-storytelling sections. No structural changes.

## Decisions made during brainstorming (validated live in-browser)

| Element | Decision |
|---|---|
| Hero headline reveal | Word-by-word stagger: `y:24→0, opacity:0→1, blur:6px→0`, `power3.out`, `stagger:.045s` |
| Section/card scroll-reveal | Replace single-shot `IntersectionObserver` fade with GSAP ScrollTrigger: `y:28→0, scale:.94→1, opacity:0→1`, `back.out(1.4)`, `stagger:.12–.15s` per card group |
| Card hover (services/founders/case studies) | `translateY(-4px)` + `box-shadow:0 14px 28px rgba(23,24,26,.12)`; icon `scale(1.12) rotate(-4deg)` |
| Button hover (`.btn-p`, `.btn-g`) | `translateY(-2px)` + colored glow shadow `0 10px 24px rgba(200,82,26,.35)`, background darkens as it does today |

## Architecture

- **Dependency:** GSAP core + ScrollTrigger loaded from a CDN
  (`cdn.jsdelivr.net/npm/gsap@3.12.7/...`) via two `<script>` tags before
  the existing inline `<script>` block, `defer`red so they don't block
  first paint. No build step, no bundler — matches the site's existing
  "single static HTML file" architecture.
- **No SplitText/MotionPath (paid plugins):** word-splitting for the hero
  is a ~5-line vanilla JS function (`text.split(' ').map(...)`), same
  technique validated in the brainstorm preview.
- **Reveal mechanism:** existing `IntersectionObserver` block
  (index.html:1669) is replaced by one `ScrollTrigger` call per section
  (services grid, founders grid, case-study grid, reviews, FAQ list),
  each driving a staggered GSAP timeline over that section's `.reveal`
  elements — not a single global `ScrollTrigger.batch`, since sections
  differ in card count/layout and each needs its own stagger timing. The
  `.reveal` CSS class and its base `opacity:0;transform:translateY(18px)`
  styles are removed once GSAP owns the initial/animated state, to avoid
  the two systems fighting each other.
- **Hover states:** pure CSS (`transition`/`:hover`), no JS — matches what
  was validated in-browser (real `:hover`, no click-triggered simulation).
  Consistent with the existing pattern (buttons/cards already use
  CSS-only hover).
- **Two-file duplication:** `index.html` and `eng/index.html` are
  independent files today (confirmed pattern from the earlier photo-path
  and icon fixes in this same session) — every change here is applied to
  both, same as those prior fixes. No shared-file refactor is in scope.

## Guardrails

- `prefers-reduced-motion: reduce` — all new GSAP-driven animations must
  resolve to their end state instantly (no stagger, no transform) under
  this media query, same guarantee the current `.reveal`/`.faq-a` block
  already gives. Achieved via `gsap.matchMedia()` with a
  `(prefers-reduced-motion: no-preference)` context wrapping all
  scroll/hero animations, mirroring the existing `@media
  (prefers-reduced-motion:reduce)` CSS block's intent.
- Mobile — `ScrollTrigger.matchMedia()` breakpoint (`max-width: 640px`)
  shortens stagger and drops the scale-in to a plain fade, to keep it light
  on low-end phones.
- No scroll-hijacking or smooth-scroll library (Lenis etc.) — native
  scroll only, animations trigger off scroll position via ScrollTrigger,
  never take over the scroll itself. Confirmed increate.ca doesn't use one
  either.
- GSAP script tags use `defer` — no render-blocking.

## Testing / verification

No test framework in this repo (static HTML site). Verification is manual,
same approach used earlier in this session (local `python3 -m http.server`
+ DOM/JS inspection via the browser tool, since screenshot capture has
proven flaky in this environment):

- [ ] Hero animates on load in both `index.html` and `eng/index.html`
- [ ] Each `.reveal`-equivalent section animates in once, on first scroll
      into view (not on every re-entry — matches current one-shot behavior)
- [ ] Card and button hover states verified via real `:hover` (not just
      reading CSS)
- [ ] `prefers-reduced-motion: reduce` (via `resize_window` /
      `emulateMedia` in the browser tool) — confirm no motion, content
      fully visible immediately
- [ ] Narrow viewport (375px) — confirm the lighter mobile variant runs,
      no jank
- [ ] No console errors, GSAP/ScrollTrigger load correctly from CDN
- [ ] Existing functionality unaffected: FAQ accordion, lightbox, form
      validation, language toggle — all still work after the reveal
      mechanism swap
