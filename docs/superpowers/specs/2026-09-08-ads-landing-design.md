# /ads paid-traffic landing page — design

## Context

Reference: https://pinkbubble.agency/ads-short — a Ukrainian web-dev agency's
standalone advertorial page built for cold Meta/Instagram ad traffic (the
`fbclid`/`utm_*` params on the shared URL confirm it's a live ad-campaign
landing page, not part of their main site nav). Despite "VSL" appearing in
the URL slug, the live page has no video — it's a scroll-through,
screenshot-and-copy advertorial, not an actual video sales letter.

User's request: build the same kind of page for UNO Agency. Two rounds of
scoping corrected the initial direction — see "Explicit non-goals" below.

## Reference page — full structure (analyzed via live browse, 2026-09-08)

1. **Header**: minimal wordmark + colored dot logo, no nav links
2. **Hero**: headline ("Трафік в промислових масштабах") + one stat callout
   box ($150K+ ad budget managed monthly, on a solid blue block) + 4-item
   checklist with green checkmarks + black pill CTA button with a
   paper-plane icon ("обговорити проєкт")
3. **Problem section**: "Більшість бізнесів мають проблеми з трафіком:" —
   5 pain points as a plain list
4. **One-line pivot**: "Наш підхід кардинально відрізняється — тому ми
   швидко масштабуємо трафік, зберігаючи високий ROMI"
5. **"How our system works" — 3 cards**: unlimited creatives / full
   in-house production / library of proven formats from 8 years of data
6. **"High ROAS at distance" + "We replace your whole traffic team"**:
   explanatory copy + a 4-item checklist
7. **Case-study carousel, 6 cases**: each slide is a real Ads Manager
   dashboard screenshot (a literal spend/CPA/ROAS table screenshot, not a
   stock photo or mockup) with a bold stat caption below it (e.g. "182,926
   реєстрацій по ціні $1.18. Інвестовано в трафік — $215,000"). Dot
   pagination + prev/next arrow controls.
8. **Platforms row**: Meta / YouTube / Google logos
9. **Footer CTA band** + a persistent sticky "зв'язатись в telegram" button
10. **Lead modal** (opens on any CTA click): exactly 3 fields — Telegram
    handle/phone (free text), monthly ad budget (6-option dropdown), niche
    (6-option dropdown) — submit button, then a thank-you message. No
    name/email/company fields at all.

Visual language: white background, one blue accent + black CTA buttons +
green checkmarks, narrow centered single column, no dark mode, no heavy
animation — everything subordinated to conversion speed, not spectacle.
This is a deliberately different visual register from the increate.ca-
inspired dark/animated homepage work happening in parallel
(`worktree-design-refresh`) — that's expected, these are two different
page types with two different jobs.

## Explicit non-goals (corrected during brainstorming — do not re-add)

- **No founders' photo block.** Proposed by Claude as a "trust
  differentiator," explicitly rejected by the user: *"Нащо фото
  засновників? ти маєш зробити такий же ж сайт, як в конкурента!"* — the
  brief is fidelity to the reference's structure, not incidental
  embellishment.
- **No vertical section-label motif** (the increate-style device built for
  the homepage redesign). Same reasoning — that's a homepage-specific
  signature, not part of this reference, and the user rejected imported
  extras once already.
- **No interactive ROI calculator/quiz.** Discussed as an optional
  stretch idea, not requested, adds real engineering/testing surface to a
  page whose entire purpose is speed-to-conversion. Explicitly out of
  scope unless the user asks later.
- **No English version yet.** Reference is Ukrainian-only (a Ukrainian-
  audience ad campaign); user confirmed Ukrainian-only for now, EN can be
  added later from the same template if a non-UA campaign needs it.

## What UNO-izes it (the only two approved changes from a faithful clone)

1. **Brand colors, not pink bubble's colors**: `--o:#C8521A` (UNO's
   existing orange) replaces their blue accent everywhere it appears (stat
   box, checkmarks, links); `--dark:#17181A` (UNO's existing near-black)
   replaces their pure-black CTA buttons. Both variables already exist in
   `index.html`'s `:root` — reuse them verbatim, don't invent new hex
   values.
2. **Real UNO content** in every section — see below.

## Content mapping — reference section → UNO content

| Reference section | UNO content |
|---|---|
| Headline | Meta/TikTok Ads + SMM framing (not generic "web traffic") — draft: "Реклама, яка приносить продажі, а не лайки" or similar; final wording goes through `/loop` after first draft (see Copy below) |
| Hero stat box | Reuse existing homepage stats: `$2M+` budget managed / `$7M+` client revenue (already-proven numbers, no new claim to source) |
| Hero checklist (4) | Rewritten for Meta/TikTok/SMM: e.g. "Високий ROAS на дистанції", "Необмежена кількість креативів", "Працюємо з Meta, TikTok, Instagram", "Підхід, перевірений на реальних бюджетах" — adapted, not copied verbatim |
| Problem section (5 pts) | Rewritten for a paid-social context (single ad account with no testing system, creative fatigue/no refresh cadence, rising CPL, no clear attribution, agency that disappears after onboarding) |
| "How it works" 3 cards | UNO's actual working method: continuous creative testing, in-house production (UGC/motion), proven format library from real client history |
| "Replace your traffic team" checklist | Adapted 1:1 — this claim is generic enough to genuinely apply to UNO's service model |
| **Case carousel — 6 to 8 slides** | Pull straight from the existing homepage case data (`index.html` `.cs-slide` blocks) — real numbers already on the live site, e.g.: toy shop ($24,780 spend → 14,468 purchases, $1.71 CPA, **1366% ROAS**, $379,564 revenue); beauty/Canada (×26 return, 2646% ROAS, $29,225); lash supplies UA (1411% ROAS); real estate (2 sales, $210,000 total from $1,684 spend); language school Poland ($3.48 CPL from zero). Use whichever 6-8 read strongest for a Meta/TikTok Ads pitch (skip pure lead-gen/USA one if a shorter set is wanted — final selection is a build-time judgment call, not a spec decision) |
| Case image (dashboard screenshot) | **Placeholder for now** — a clearly-marked frame ("Заміни на реальний скрін кейсу") in the same visual slot, same pattern already used in `design-refresh` for the trust-badge/logo-wall placeholders. User has real screenshots "десятки... в ноушині" to swap in later, in a follow-up pass — not blocking this build |
| Platforms row | Meta / TikTok / Instagram logos (swap YouTube/Google for what UNO actually runs) |
| Lead form (3 fields) | Same 3 fields as the reference: Telegram handle/phone (free text) / budget (dropdown) / niche (dropdown) — see Form integration below for exact option values |

## Form integration — reuse the existing backend, no backend changes

The homepage's modal form (`index.html`, `submitModal()` → `sendLead()`)
already posts to a working, retried, tracked Google Apps Script endpoint:

```js
sendLead(name, phone, tg, email, service) // builds query params, GETs:
'https://script.google.com/macros/s/AKfycbxKAhhCP7qKwJ9BW4yZqgdtg_nA5bADqoT1Po_4sWKA6Zdphq_2Inq0MP_0CAJGtNthCg/exec?' + params
// 3 attempts with 1.5s/3s backoff, honeypot field, fbp/fbc/event_id tracking already wired in
```

This page reuses `sendLead()` verbatim (copy the function, same endpoint,
same retry logic) with a **new, page-specific submit function** — it does
not reuse `submitModal()`'s validation rules (those require name+phone,
which this form doesn't collect). New mapping:

- Telegram handle/phone field → `tg` param, and duplicated into `name` so
  the Sheet row has something readable in the name column (e.g. the raw
  handle) — no separate name field needed, matching the reference exactly.
- `phone` param → left empty (nothing else to put there; the tg field
  already captures a contact method).
- Niche dropdown → `service` param, values matching the reference's 6
  options (Онлайн-школа / Mobile Apps / SaaS / Нерухомість / Ecommerce /
  Послуги / Інше) — reuse verbatim, these are generic business niches, not
  reference-specific copy.
- Budget dropdown → **no existing param for this on the current
  endpoint.** Fold it into `service` as a suffix string at send time (e.g.
  `service = "${niche} · бюджет ${budgetLabel}"`) so it lands in the
  existing Sheet column without any Apps Script changes. This is a
  front-end-only integration — the deployed backend is not touched.
  Exact 6 options, copied verbatim from the reference (generic budget
  tiers, not reference-specific copy): "Не запускали рекламу раніше",
  "до $1 000", "$1 000 – 3 000", "$3 000 – 10 000", "$10 000 – 30 000",
  "$30 000+".
- Validation: require the Telegram field non-empty and both dropdowns
  selected before enabling submit (mirrors the reference's own behavior —
  its submit button is visibly disabled until all three fields are set).

## File / architecture

- New static file `/ads/index.html` at the repo root — same
  no-build-step, single-HTML-file architecture as the rest of the site
  (`index.html`, `eng/index.html`). Not linked from the main nav anywhere;
  reached only via direct/ad-campaign URL, exactly like the reference.
- `<meta name="robots" content="noindex, nofollow">` — this is an
  ad-landing page meant for paid traffic only, not organic search
  (matches the `noindex` decision already made for `/preview-redesign/`
  earlier this session, same reasoning: it's not a page that should show
  up in search results while it's a paid-campaign-specific variant).
- Self-contained CSS in the page (reusing `--o`/`--dark` and other
  existing CSS custom properties by value, since this is a standalone
  file with no shared stylesheet to import from).
- No GSAP/animation dependency — the reference has none, and this page's
  entire point is fast load + fast conversion for paid traffic, where
  every extra render-blocking script works against the goal.

## Copy process

Per this workspace's own rule for landing-page/ad copy: structure and
section-by-section content mapping (above) is locked by this spec, but
the actual headline/pain-point/CTA *wording* gets a `/loop` pass
(rubric → draft → critique → rewrite) as a follow-up step after the first
build, rather than being treated as final on first write.

## Testing / verification

No test framework in this repo (static HTML site, same as the rest).
Manual verification, same approach used throughout this session:
- [ ] `/ads/` loads with no console errors, `noindex` present
- [ ] All case numbers match the source-of-truth values in `index.html`'s
      existing case section (no transcription errors)
- [ ] Form: submit disabled until Telegram field + both dropdowns are
      filled; successful submit shows a thank-you state (mirroring the
      reference); a real test submission is visible in the same
      Sheet/Telegram channel the homepage form already delivers to
- [ ] Mobile viewport (375px) — no horizontal overflow, carousel usable
      by touch/swipe or visible prev/next controls
- [ ] Placeholder case-image frames are visually unmistakable as
      placeholders (not mistaken for missing/broken images)
