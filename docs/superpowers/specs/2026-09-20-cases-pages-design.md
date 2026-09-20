# Cases catalog and case pages — design

Date: 2026-09-20. Branch: `redesign-one`. Status: draft for user review.

## Goal

Move the cases from the public Notion page
(`malleable-alligator-555.notion.site/ADS-SMM-fa9974957ad88332b92181da469742ca`)
onto the site as real pages, in the visual language of `/redesign/`
(dark cinematic, Geologica / Cormorant / Onest, sun + grain).
The landing shows a few cases; a separate `/cases/` page opens all of them.
The text and screenshots are moved as written in Notion, not rewritten.

## Decisions already made with the user

- Style: the new redesign look, not a Notion clone. Structure follows Notion:
  gallery of cards with filters, and a case page with text and screenshots in the Notion order.
- Separate page for all cases; the landing shows part of them and links to the rest.
- Page stays `noindex` until the user approves going live.
- Filters are the three views of the Notion page: **Meta Ads**, **SMM**, **Meta Ads + SMM**.
  Verified on the public page: the "SMM" view is exactly the 18 rows tagged `Google ADS` in
  the database (the option is named "Google ADS" but holds SMM cases).

## Data

| Source | Use |
|---|---|
| Notion connector, data source `collection://7d397495-7ad8-8302-83a0-87b47742a009` | Row list, properties (Tags, Geo, Niche, LTV, Description), freshness check, missing videos |
| `Сайт UNO/cases/cases_full.json` (local, gitignored) | Block content (headings, lists, callouts, columns, image refs) |
| `Сайт UNO/cases/images/` (local, gitignored, 262 files, 245 MB) | Screenshots |
| Public page cards | Cover images for catalog cards (Notion API image links live only 5 minutes) |

Rules for what is included:

- Drop rows starting with `(НЕ ЗАВЕРШЕНО)` (3 rows).
- Drop duplicates, keeping the fuller page: `Cool Cat Fence` (2 rows), `Всеукраїнська федерація гольфу` (2 rows, one has no tag).
- Category from Tags: `Facebook ADS` → Meta Ads; `Google ADS` → SMM; both → Meta Ads + SMM;
  no tag (one golf row) → decided by the kept duplicate.
- Expected result: about 46–48 cases.
- Card teaser = Notion `Description` when present (for example "2 985 заявок по $6,96 за ліда");
  otherwise the first paragraph of the page, trimmed.

## Build

One script, `scripts/build_cases.py`, run by hand, output committed:

1. Read JSON + images, apply the rules above, write `cases/data.json` (metadata only).
2. Convert screenshots to WebP (max 1400 px wide, quality about 80) into `assets/cases/img/<slug>-<n>.webp`.
   Raw files never enter git. Target total size: under 40 MB (to be measured; if larger, lower quality or width).
3. Generate `cases/index.html` and `cases/<slug>/index.html` (static, no framework).
   Slugs are transliterated ASCII so URLs work on GitHub Pages.
4. Fail loudly (non-zero exit, message) if a referenced image is missing or a slug repeats.

## Pages

**`/cases/`** — hero ("Кейси", one line of context from Notion), filter chips
(Усі · Meta Ads · SMM · Meta Ads + SMM, with counts), card grid.
Card: cover, title, tags, geo, teaser. Filtering is client-side (about 15 lines of JS),
the selected filter is kept in the URL hash so a filtered view can be shared.
Without JS all cards are visible.

**`/cases/<slug>/`** — title, tags/geo/niche, then the Notion blocks in order:
headings, paragraphs, lists, callouts, dividers, quotes, images (columns become a responsive grid).
Screenshots open in a lightbox. Footer: previous / next case in the same category,
and the lead form CTA (link to `/redesign/#contact`).

**`/redesign/` landing** — the cases block shows the 7 strongest cases (already designed
with real numbers) plus a button "Дивитись усі N кейсів →" to `/cases/`. The featured card keeps
its placeholder until real Ads Manager screenshots are chosen from the moved ones.

## Videos

Notion has 83 video blocks but the local export has empty links. They are skipped in the first
release (the case page simply has no video block). A second step reads them through the Notion
connector and embeds them; not a blocker for this spec.

## Accessibility and performance

- Cards are real links; filter chips are buttons with `aria-pressed`.
- Images have alt text (case title + "скрін результатів"), `loading="lazy"`, explicit width/height.
- Reduced motion respected; no animation is required to read content.

## Verification (run, not read)

- `build_cases.py` exits 0 and prints counts per category; the counts match the Notion views
  (Notion currently lists 52 rows; the 18 SMM rows and the exclusions above are checked by name).
- Real browser screenshots: `/cases/` desktop and 390 px, one text-heavy case, one image-heavy case, filter click.
- No horizontal scroll at 390 px; no 404 in the network list; every `img` loads.
- Lead CTA links go to the working form.

## Out of scope

English version, indexing / sitemap, editing case texts, redaction of client names on screenshots
(screenshots move as they are on the already-public Notion page), Meta Pixel.

## Open items for the owner

1. Some Notion numbers disagree with the numbers used on the site (toys ROAS 1366% vs 1532% from
   revenue/spend; Cool Cat 280% vs 496%). Moved as written; please confirm which is right before going live.
2. Client names may be visible on some screenshots. Publishing them is the owner's call.
3. Which cases go on the landing (default: the 7 already designed).
