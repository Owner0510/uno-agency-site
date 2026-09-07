# Animation & Interaction Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring UNO Agency's hero text, scroll-in reveals, and hover states up to the animation-quality bar of increate.ca, using GSAP + ScrollTrigger, without changing page structure or content.

**Architecture:** Two CDN `<script>` tags (GSAP core + ScrollTrigger) load at the end of `<body>`, right before the site's existing inline `<script>` block. All new animation code lives inside that same existing inline block. No build step, no bundler — matches the site's current single-static-HTML-file architecture.

**Tech Stack:** GSAP 3.12.7 (`gsap.min.js`, `ScrollTrigger.min.js`) via `cdn.jsdelivr.net`, vanilla JS, existing site CSS.

## Global Constraints

- Every task touches **both** `index.html` (root, Ukrainian default) and `eng/index.html` (English default) — they are independent static files with near-identical structure; changes must be applied to both, in the same session, so they never drift (established pattern from the earlier photo-path and icon fixes in this repo).
- No new npm/build dependency — GSAP loads from CDN only.
- `prefers-reduced-motion: reduce` must fully disable all new motion (instant end-state, no exceptions).
- No scroll-hijacking / smooth-scroll library. Native scroll only.
- Nothing in this plan touches: FAQ accordion logic, lightbox (`openImg`/`closeImg`), form validation/submit, `toggleLang()` navigation, video-thumb play/pause logic. These must still work identically after every task.
- Spec reference: `docs/superpowers/specs/2026-09-07-animation-polish-design.md`

---

### Task 1: Load GSAP + ScrollTrigger from CDN

**Files:**
- Modify: `index.html` (insert before the `<script>` tag that currently opens the site's main inline script block — search for the line directly above `// ── MODAL ──`)
- Modify: `eng/index.html` (same insertion point, same search anchor)

**Interfaces:**
- Produces: global `gsap` and `ScrollTrigger` objects, available to all inline `<script>` code below the insertion point, in both files.

- [ ] **Step 1: Insert the CDN script tags in `index.html`**

Find this exact block (it's the opening of the final inline script, immediately preceded by the closing `</section>`/HTML of the page and followed by `// ── MODAL ──`):

```html
<script>

// ── MODAL ──
```

Replace it with:

```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.7/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.7/dist/ScrollTrigger.min.js"></script>
<script>
gsap.registerPlugin(ScrollTrigger);

// ── MODAL ──
```

- [ ] **Step 2: Insert the same block in `eng/index.html`**

Same search-and-replace as Step 1, applied to `eng/index.html` (its `<script>` opening tag is a few lines earlier in the file due to shorter English text elsewhere, but the same `// ── MODAL ──` anchor identifies the spot).

- [ ] **Step 3: Verify GSAP loads with no console errors**

```bash
cd "/Users/serhiihatlan/Desktop/Cloude Code/uno-agency-site" && python3 -m http.server 8940 >/tmp/uno-verify.log 2>&1 &
sleep 1
```

Then, using the browser tool: navigate to `http://localhost:8940/`, and run in `javascript_tool`:

```js
JSON.stringify({gsap: typeof gsap, ScrollTrigger: typeof ScrollTrigger, gsapVersion: gsap.version})
```

Expected: `{"gsap":"function","ScrollTrigger":"function","gsapVersion":"3.12.7"}` — and `read_console_messages` shows no errors.

Repeat for `http://localhost:8940/eng/`.

- [ ] **Step 4: Commit**

```bash
git add index.html eng/index.html
git commit -m "$(cat <<'EOF'
feat: load GSAP + ScrollTrigger from CDN

Foundation for the animation-polish work — no visible behavior
change yet, just makes gsap/ScrollTrigger available to the site's
existing inline script.
EOF
)"
```

---

### Task 2: Hero headline word-stagger reveal

**Files:**
- Modify: `index.html` (add code right after the `gsap.registerPlugin(ScrollTrigger);` line added in Task 1)
- Modify: `eng/index.html` (same)

**Interfaces:**
- Consumes: `gsap` (Task 1)
- Produces: nothing consumed by later tasks — self-contained.

Both files' hero markup is identical in structure:

```html
<h1>
  <span class="uk">Залучаємо клієнтів та збільшуємо продажі через рекламу та контент в соціальних мережах</span>
  <span class="en">We attract clients and increase sales through social media advertising and content</span>
</h1>
```

`.en` is `display:none` by default in both files; `eng/index.html` flips it visible via a separate existing IIFE that adds `body.classList.add('en-mode')`. Splitting and animating both spans unconditionally (regardless of which is visible) is simplest and harmless — GSAP tweening `opacity`/`transform`/`filter` on a hidden element does nothing visible and throws no error.

- [ ] **Step 1: Add the hero word-split animation to `index.html`**

Insert this immediately after `gsap.registerPlugin(ScrollTrigger);`:

```js
// ── HERO HEADLINE REVEAL ──
(function(){
  const heroSpans = document.querySelectorAll('#hero h1 > span');
  const mmHero = gsap.matchMedia();
  mmHero.add('(prefers-reduced-motion: no-preference)', () => {
    heroSpans.forEach(span => {
      const words = span.textContent.trim().split(/\s+/);
      span.innerHTML = words.map(w => `<span class="hw">${w}</span>`).join(' ');
      gsap.fromTo(span.querySelectorAll('.hw'),
        {y:24, opacity:0, filter:'blur(6px)'},
        {y:0, opacity:1, filter:'blur(0px)', duration:.7, ease:'power3.out', stagger:.045, delay:.1}
      );
    });
  });
})();
```

Add this CSS rule next to the existing `.hero-l` rules (find `.hero-l` in the `<style>` block and add immediately after its closing `}`):

```css
.hero-l h1 .hw{display:inline-block;will-change:transform,opacity,filter}
```

- [ ] **Step 2: Apply the same two changes to `eng/index.html`**

Same JS block after its `gsap.registerPlugin(ScrollTrigger);`, same CSS rule after `.hero-l`.

- [ ] **Step 3: Verify word-split and animation ran**

Browser tool, on `http://localhost:8940/`:

```js
JSON.stringify({
  wordCount: document.querySelectorAll('#hero h1 .uk .hw').length,
  firstWordOpacity: getComputedStyle(document.querySelector('#hero h1 .uk .hw')).opacity
})
```

Expected: `wordCount` > 0 (matches the number of words in the Ukrainian headline), `firstWordOpacity` is `"1"` after the animation has had time to run (the browser tool call itself introduces enough delay).

Repeat on `http://localhost:8940/eng/`, checking `#hero h1 .en .hw` instead (English is the visible span there).

- [ ] **Step 4: Verify reduced-motion disables it**

Using `resize_window` with `colorScheme` doesn't control `prefers-reduced-motion` — instead use `javascript_tool` to confirm the matchMedia guard exists, and manually confirm via `emulateMedia`-style check is not available in this tool; instead verify by reading the code path: `mmHero.add('(prefers-reduced-motion: no-preference)', ...)` means the split+animate code **only ever runs** when the OS does *not* request reduced motion. When reduced motion **is** requested, the callback never runs, so `span.innerHTML` is untouched and the plain text renders immediately and statically — confirm this by reading the shipped code, no live emulation needed for this step since the guard is structural (the animation code path is unreachable under reduced motion, not merely visually suppressed).

- [ ] **Step 5: Commit**

```bash
git add index.html eng/index.html
git commit -m "$(cat <<'EOF'
feat: word-stagger reveal on hero headline

Word-by-word blur+slide-in on page load, skipped entirely under
prefers-reduced-motion via gsap.matchMedia.
EOF
)"
```

---

### Task 3: Replace scroll-reveal engine (IntersectionObserver → GSAP ScrollTrigger)

**Files:**
- Modify: `index.html` (CSS: remove `.reveal`/`.reveal.visible`/`.rev-slider .reveal,.vid-slider .reveal` rules, update reduced-motion rule; JS: replace the `IntersectionObserver` block)
- Modify: `eng/index.html` (same)

**Interfaces:**
- Consumes: `gsap`, `ScrollTrigger` (Task 1)
- Produces: nothing consumed by later tasks.

Current CSS to remove (three rules, found via `grep -n '\.reveal'`):

```css
.reveal{opacity:0;transform:translateY(18px);transition:opacity .5s ease,transform .5s ease}
.reveal.visible{opacity:1;transform:none}
```
and
```css
.rev-slider .reveal,.vid-slider .reveal{opacity:1;transform:none}
```

Current reduced-motion rule to edit (remove `.reveal` from the selector list — everything else in it stays):

```css
.reveal,.hero-badge-dot,.faq-ico,.faq-a{transition:none;animation:none}
```
becomes:
```css
.hero-badge-dot,.faq-ico,.faq-a{transition:none;animation:none}
```

Current JS to remove (found via `grep -n 'REVEAL ON SCROLL'`):

```js
// ── REVEAL ON SCROLL ──
const io=new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target);}
  });
},{threshold:.06,rootMargin:'0px 0px -36px 0px'});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
```

- [ ] **Step 1: Remove the three CSS rules in `index.html`, edit the reduced-motion rule**

As shown above — delete the two `.reveal`/`.reveal.visible` lines and the `.rev-slider .reveal,.vid-slider .reveal` line; edit the reduced-motion selector list to drop `.reveal`.

- [ ] **Step 2: Replace the JS block in `index.html`**

Replace the `// ── REVEAL ON SCROLL ──` block shown above with:

```js
// ── REVEAL ON SCROLL (GSAP ScrollTrigger) ──
(function(){
  // Elements inside horizontal sliders are already on-screen — show immediately, no scroll-trigger.
  document.querySelectorAll('.rev-slider .reveal, .vid-slider .reveal').forEach(el=>{
    gsap.set(el, {opacity:1, y:0, scale:1});
  });

  const revealGroups = [
    {selector:'.svc-card.reveal', stagger:.12},
    {selector:'.founder-card.reveal', stagger:.15},
    {selector:'.trust-card.reveal', stagger:.08},
    {selector:'.proc-card.reveal', stagger:.08},
    {selector:'.rev-card.reveal', stagger:.1},
    {selector:'.video-thumb.reveal', stagger:.06},
    {selector:'.cs-wrap.reveal, .ref-band.reveal, .split-deal.reveal', stagger:.1}
  ];

  const mmReveal = gsap.matchMedia();
  mmReveal.add({
    reduced: '(prefers-reduced-motion: reduce)',
    mobile: '(prefers-reduced-motion: no-preference) and (max-width: 640px)',
    desktop: '(prefers-reduced-motion: no-preference) and (min-width: 641px)'
  }, (context) => {
    const {reduced, mobile} = context.conditions;

    if(reduced){
      document.querySelectorAll('.reveal').forEach(el => gsap.set(el, {opacity:1, y:0, scale:1}));
      return;
    }

    revealGroups.forEach(({selector, stagger}) => {
      const els = gsap.utils.toArray(selector).filter(el => !el.closest('.rev-slider, .vid-slider'));
      if(!els.length) return;
      gsap.set(els, {opacity:0, y: mobile ? 16 : 28, scale: mobile ? 1 : .94});
      ScrollTrigger.batch(els, {
        start: 'top 92%',
        onEnter: batch => gsap.to(batch, {
          opacity:1, y:0, scale:1,
          duration: mobile ? .4 : .6,
          ease: mobile ? 'power2.out' : 'back.out(1.4)',
          stagger: mobile ? stagger * .5 : stagger
        })
      });
    });
  });
})();
```

- [ ] **Step 3: Apply the same CSS and JS changes to `eng/index.html`**

- [ ] **Step 4: Verify reveal groups animate on scroll (desktop)**

```bash
pkill -f "http.server 8940" 2>/dev/null
cd "/Users/serhiihatlan/Desktop/Cloude Code/uno-agency-site" && python3 -m http.server 8940 >/tmp/uno-verify.log 2>&1 &
sleep 1
```

Browser tool: navigate to `http://localhost:8940/`, scroll to the Services section, then:

```js
const cards = document.querySelectorAll('.svc-card');
JSON.stringify(Array.from(cards).map(c => getComputedStyle(c).opacity))
```

Expected: all `"1"` (cards have entered viewport and animated to full opacity). Scroll to Founders and Case Studies sections and repeat for `.founder-card` and `.cs-wrap`.

- [ ] **Step 5: Verify mobile gets the lighter variant**

`resize_window` to `preset: "mobile"`, reload, scroll to Services, run the same opacity check — expect the same end state (`opacity: "1"`), confirming the mobile branch also completes (the visual difference is timing/scale, not end-state, so this check proves the branch executed without error). Then `resize_window` back to `preset: "desktop"`.

- [ ] **Step 6: Verify reduced-motion shows content instantly, no scroll needed**

Read-through check (same reasoning as Task 2 Step 4): under `prefers-reduced-motion: reduce`, `mmReveal`'s `reduced` branch runs `gsap.set(...)` on **all** `.reveal` elements unconditionally, independent of scroll position — so content is fully visible immediately on load, not gated on scrolling into view. This is verifiable by reading the code path (the `if(reduced){...; return;}` branch never touches `ScrollTrigger`).

- [ ] **Step 7: Regression-check nothing else broke**

Browser tool, both files: confirm the FAQ accordion still opens/closes (`toggleFaq`), the lightbox still opens on a case-study image click (`openImg`), and no new console errors appear anywhere on the page (`read_console_messages`).

- [ ] **Step 8: Commit**

```bash
git add index.html eng/index.html
git commit -m "$(cat <<'EOF'
feat: replace scroll-reveal with GSAP ScrollTrigger

Swaps the single global IntersectionObserver + CSS-transition fade
for per-section ScrollTrigger batches with stagger + scale-in.
Reduced-motion and mobile get lighter/instant variants via
gsap.matchMedia. Slider-contained cards keep their existing
always-visible behavior.
EOF
)"
```

---

### Task 4: Hover micro-interactions (cards + buttons)

**Files:**
- Modify: `index.html` (CSS only)
- Modify: `eng/index.html` (CSS only)

**Interfaces:**
- Consumes: nothing (pure CSS, no GSAP).
- Produces: nothing consumed by later tasks.

Scope: only the elements actually validated in the brainstorming preview — service cards (which already have `svg` icons) and founder cards get a lift+shadow; primary/secondary buttons get lift+glow. `.trust-card`, `.proc-card`, `.rev-card`, `.video-thumb` already have their own distinct hover treatments (border-color change, overlay darkening, play-icon scale) and are intentionally left untouched to avoid fighting with existing behavior.

- [ ] **Step 1: Add card hover CSS to `index.html`**

Find `.svc-card:hover{background:var(--light2)}` and add immediately after it:

```css
.svc-card{transition:background .2s,transform .2s,box-shadow .2s}
.svc-card:hover{transform:translateY(-4px);box-shadow:0 14px 28px rgba(23,24,26,.12)}
.svc-icon svg{transition:transform .25s ease}
.svc-card:hover .svc-icon svg{transform:scale(1.12) rotate(-4deg)}
```

Find `.founder-card{border:1px solid var(--border-l);border-radius:16px;padding:40px;background:rgba(23,24,26,.03);transition:border-color .2s}` and change its `transition` value to include the new properties:

```css
.founder-card{border:1px solid var(--border-l);border-radius:16px;padding:40px;background:rgba(23,24,26,.03);transition:border-color .2s,transform .2s,box-shadow .2s}
```

Then add immediately after the existing `.founder-card:hover{border-color:rgba(23,24,26,.2)}`:

```css
.founder-card:hover{transform:translateY(-4px);box-shadow:0 14px 28px rgba(23,24,26,.1)}
```

(Two `.founder-card:hover` rules is valid CSS — the later one's declared properties merge with the earlier one's for elements matching both; `border-color` from the first rule still applies.)

- [ ] **Step 2: Add button hover CSS to `index.html`**

Find `.btn-p{display:inline-block;background:var(--o);color:#fff;padding:15px 30px;border-radius:10px;font-size:16px;font-weight:700;transition:background .2s;white-space:nowrap}` and change to:

```css
.btn-p{display:inline-block;background:var(--o);color:#fff;padding:15px 30px;border-radius:10px;font-size:16px;font-weight:700;transition:background .2s,transform .2s,box-shadow .2s;white-space:nowrap}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(200,82,26,.35)}
```

Find `.btn-g{display:inline-block;background:transparent;color:#fff;padding:15px 30px;border-radius:10px;font-size:16px;font-weight:700;border:1.5px solid rgba(255,255,255,.2);transition:.2s;white-space:nowrap}` and add immediately after it:

```css
.btn-g:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(255,255,255,.08)}
```

Find `.btn-g-dark{display:inline-block;background:transparent;color:var(--dark);padding:15px 30px;border-radius:10px;font-size:16px;font-weight:700;border:1.5px solid rgba(23,24,26,.25);transition:.2s;white-space:nowrap}` and add immediately after it:

```css
.btn-g-dark:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(23,24,26,.12)}
```

- [ ] **Step 3: Apply the same CSS additions to `eng/index.html`**

Same four insertions, same anchor strings (all identical in both files).

- [ ] **Step 4: Verify via real `:hover` in the browser**

Browser tool, `http://localhost:8940/`: use `computer` with action `hover` on a `.svc-card`, then read its computed `transform` and the icon `svg`'s computed `transform` — both should be non-`none`. Repeat for `.btn-p` (the "Залишити заявку" hero button).

- [ ] **Step 5: Commit**

```bash
git add index.html eng/index.html
git commit -m "$(cat <<'EOF'
feat: hover lift/glow on service cards, founder cards, buttons

Scoped to elements with no pre-existing hover treatment of their
own — trust/proc/rev/video-thumb cards keep their current hover
behavior untouched.
EOF
)"
```

---

### Task 5: Full guardrail + regression verification pass

**Files:** none modified — verification only, both files.

- [ ] **Step 1: Reduced-motion, both languages**

This re-confirms Task 2 Step 4 and Task 3 Step 6 hold together, on both files, not just in isolation.

Browser tool: navigate to `http://localhost:8940/`, then `http://localhost:8940/eng/`. For each, read the source of the two `matchMedia` blocks (hero + reveal) via:

```js
JSON.stringify({hasReducedGuardHero: document.documentElement.outerHTML.includes("prefers-reduced-motion: no-preference"), hasReducedGuardReveal: document.documentElement.outerHTML.includes("prefers-reduced-motion: reduce")})
```

Expected: both `true` on both pages.

- [ ] **Step 2: Mobile viewport, both languages**

`resize_window` to `preset: "mobile"`. Reload each page. Confirm no horizontal scrollbar appears and no console errors:

```js
JSON.stringify({scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth})
```

Expected: `scrollWidth <= clientWidth` (no horizontal overflow introduced by the new animations). `resize_window` back to `preset: "desktop"` when done.

- [ ] **Step 3: Existing functionality regression, both languages**

For each of `http://localhost:8940/` and `http://localhost:8940/eng/`:
- FAQ: click a `.faq-q`, confirm its parent `.faq-item` gains class `open`.
- Lightbox: click a case-study image, confirm `#imgLb` gains class `open` and `#imgLbImg`'s `src` is non-empty; click the close button, confirm `open` is removed.
- Language toggle: click `.lang-btn`, confirm navigation to the other file (`/eng` or `/`).
- Form: confirm the required-field/format `oninput` handlers on `#fName`/`#fPhone`/`#fTg` still strip disallowed characters (type an invalid character, confirm it's stripped).

- [ ] **Step 4: Stop the local test server**

```bash
pkill -f "http.server 8940" 2>/dev/null
```

No commit for this task — it's verification-only. If any check fails, fix it as part of the task whose code caused the failure (Task 2, 3, or 4) and re-commit there, not here.

---

### Task 6: Deploy

**Files:** none — git operations only.

- [ ] **Step 1: Confirm working tree matches expectations**

```bash
cd "/Users/serhiihatlan/Desktop/Cloude Code/uno-agency-site" && git status --short && git log --oneline -6
```

Expected: clean working tree, the 4 feature commits from Tasks 1–4 at the top of `git log`.

- [ ] **Step 2: Ask the user for explicit go-ahead before pushing**

This changes the live production site (`uno-agency.com`) — per this session's established pattern (photo-path fix, icon fix), push only after explicit confirmation in chat, not automatically.

- [ ] **Step 3: Push**

```bash
git fetch origin && git log --oneline main..origin/main
```

If empty (no new remote commits), push directly:

```bash
git push origin main
```

If not empty, rebase first (`git pull --rebase origin main`, resolving/stashing any local uncommitted changes first per this repo's established practice) before pushing.

- [ ] **Step 4: Verify live**

Browser tool: navigate to `https://uno-agency.com/` and `https://uno-agency.com/eng/`, confirm the hero animates on load and no console errors appear.

---

## Self-Review Notes

- **Spec coverage:** hero word-stagger (Task 2) ✓, section stagger+scale reveal replacing IntersectionObserver (Task 3) ✓, card hover lift+icon-rotate and button hover lift+glow (Task 4) ✓, reduced-motion guardrail (Tasks 2 & 3, re-verified in Task 5) ✓, mobile-lighter variant via matchMedia (Task 3, re-verified in Task 5) ✓, no scroll-hijacking (never introduced) ✓, both files kept in sync (every task) ✓, existing functionality unaffected (Task 5 Step 3) ✓, deploy only on explicit confirmation (Task 6) ✓.
- **Placeholder scan:** no TBD/TODO; every step has complete, real code or a real command with real expected output.
- **Type/naming consistency:** `revealGroups`/`mmReveal`/`mmHero` names are used consistently within their own task and don't need to be referenced across tasks (each task's script block is self-contained, wrapped in its own IIFE) — verified no cross-task naming collisions (`mmHero` in Task 2 vs `mmReveal` in Task 3 are deliberately distinct).
