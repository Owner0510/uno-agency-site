# Cases catalog and case pages — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate `/cases/` (filterable catalog) and one static page per case from the Notion export, in the `/redesign/` visual language, and link the landing to it.

**Architecture:** A Python generator (`scripts/build_cases.py`, pure logic in `scripts/cases_lib.py`) reads `cases_full.json` + local screenshots, converts screenshots to WebP, and writes static HTML plus one shared stylesheet and one shared script. No framework, no runtime dependencies on the site.

**Tech Stack:** Python 3 + Pillow (already installed, used for the hero photo), plain HTML/CSS/JS, `unittest` for the logic tests.

## Global Constraints

Copied from `docs/superpowers/specs/2026-09-20-cases-pages-design.md`:

- Style = `/redesign/` (Geologica / Cormorant Garamond italic / Onest, dark cinematic, sun + grain; tokens copied from `redesign/index.html`).
- Filters: Meta Ads, SMM, Meta Ads + SMM (+ "Усі"). `Facebook ADS` → Meta Ads; `Google ADS` → SMM; both tags → Meta Ads + SMM.
- Drop rows whose title starts with `(НЕ ЗАВЕРШЕНО)`; drop duplicates keeping the fuller page (`Cool Cat Fence` ×2, `Всеукраїнська федерація гольфу` ×2).
- Screenshots → WebP, max width 1400 px, quality about 80, into `assets/cases/img/`. Raw files never enter git (`Сайт UNO/` is gitignored and lives only in the main checkout).
- Slugs: ASCII transliteration, unique.
- Pages are `noindex, nofollow`. Text moved as written, not rewritten. Videos skipped (their links are empty in the export).
- Accessibility: cards are real links, chips are buttons with `aria-pressed`, images have alt/width/height/`loading="lazy"`, without JS all cards are visible, reduced motion respected.
- Fail loudly (non-zero exit) on a missing image or a repeated slug.
- Deviation from spec (simplification): card cover = the case's first screenshot, not a Notion cover; a case without screenshots gets a typographic card.

Source data path (main checkout, gitignored): `/Users/serhiihatlan/Desktop/Cloude Code/uno-agency-site/Сайт UNO/cases` (contains `cases_full.json` and `images/`). Passed to the script with `--src`.

## File Structure

| File | Responsibility |
|---|---|
| `scripts/cases_lib.py` | Pure functions: `clean_title`, `slugify`, `category`, `select_cases`, `teaser`, `render_blocks`. No file IO. |
| `scripts/test_cases_lib.py` | Unit tests for the above using small synthetic data. |
| `scripts/build_cases.py` | IO: read JSON, convert images, write HTML/CSS/JS, update landing counter. |
| `assets/cases.css` | All styles for `/cases/` and case pages. |
| `assets/cases.js` | Filter chips (hash-synced) and screenshot lightbox. |
| `cases/index.html`, `cases/<slug>/index.html` | Generated output, committed. |
| `assets/cases/img/*.webp` | Generated output, committed. |
| `redesign/index.html` | Adds "Дивитись усі N кейсів →" button and count marker. |

---

### Task 1: Pure logic with tests

**Files:**
- Create: `scripts/cases_lib.py`
- Test: `scripts/test_cases_lib.py`

**Interfaces:**
- Produces: `clean_title(t: str) -> str`, `slugify(t: str) -> str`, `category(tags: str) -> str` (`"meta" | "smm" | "both" | ""`), `select_cases(raw: list[dict]) -> list[dict]` (each item: `title, slug, cat, geo, niche, desc, blocks`), `teaser(case: dict) -> str`, `render_blocks(blocks: list[dict], img: dict[str, dict], title: str) -> str` where `img[basename] = {"src": "/assets/cases/img/x.webp", "w": int, "h": int}`.

- [ ] **Step 1: Write the failing tests** — `scripts/test_cases_lib.py` covering:
  - `clean_title(" 𝗧𝗔𝗧𝗧𝗢𝗢 𝗔𝗥𝗧𝗜𝗦𝗧 ") == "TATTOO ARTIST"`; `clean_title("Lilico - **Бухгалтерські**") == "Lilico - Бухгалтерські"`.
  - `slugify("Школа танців Dance Cult Studio") == "shkola-tanciv-dance-cult-studio"`; result is ASCII and contains no leading/trailing dash.
  - `category("Facebook ADS") == "meta"`, `category("Google ADS") == "smm"`, `category("Facebook ADS, SMM Instagram") == "both"`, `category("") == ""`.
  - `select_cases`: given raw rows for `(НЕ ЗАВЕРШЕНО) X` (dropped), two `Cool Cat Fence` variants (only the one with more blocks stays), two golf rows (one with empty tags and one `Google ADS`: one stays and its category is `smm`), and two rows with the same title `A` (slugs `a` and `a-2`).
  - `teaser`: uses `desc` with `**` removed and `\$` → `$`; falls back to first paragraph ≥ 40 chars cut at 160 chars with an ellipsis.
  - `render_blocks`: heading_2 → `<h2>`; two consecutive `bulleted_list_item` → one `<ul>` with two `<li>`; `callout` with icon → `<aside class="callout">`; `column_list` with two `column` children → `<div class="cols">` with two `<div class="col">`; an `image` whose `image_local` basename is in `img` → `<img ... loading="lazy" width height alt>`; an image not in `img` raises `KeyError`; `video` → empty string; text is HTML-escaped (`<b>` in text appears as `&lt;b&gt;`).

- [ ] **Step 2: Run and confirm failure**

Run: `cd scripts && python3 -m unittest test_cases_lib -v`
Expected: `ModuleNotFoundError: No module named 'cases_lib'`.

- [ ] **Step 3: Implement `scripts/cases_lib.py`** to satisfy the tests (Ukrainian→Latin transliteration table; NFKC normalize; `select_cases` drops by `startswith("(НЕ ЗАВЕРШЕНО)")` after cleaning, resolves the two duplicate groups by explicit `DUPLICATE_GROUPS` list of cleaned titles keeping the entry with the largest JSON-serialised `blocks`, lets a kept entry with empty tags inherit the tag of its dropped sibling, then assigns unique slugs).

- [ ] **Step 4: Run tests and confirm they pass**

Run: `cd scripts && python3 -m unittest test_cases_lib -v`
Expected: all tests `ok`.

- [ ] **Step 5: Commit** — `git add scripts/cases_lib.py scripts/test_cases_lib.py && git commit -m "feat(cases): pure logic for selecting and rendering cases"`.

---

### Task 2: Generator (images + pages)

**Files:**
- Create: `scripts/build_cases.py`, `assets/cases.css`, `assets/cases.js`
- Generates: `assets/cases/img/*.webp`, `cases/index.html`, `cases/<slug>/index.html`

**Interfaces:**
- Consumes: everything from Task 1.
- Produces: CLI `python3 scripts/build_cases.py --src <dir>`; prints `cases: N (meta a, smm b, both c)`, `images: M, total X MB`; exit 1 with a clear message on a missing image or repeated slug. Updates `<!--cases-count-->…<!--/cases-count-->` in `redesign/index.html`.

- [ ] **Step 1: Write `assets/cases.css`** — tokens copied from `redesign/index.html` `:root`; page hero; chip row (`.chip[aria-pressed=true]` filled orange); grid `repeat(auto-fill,minmax(300px,1fr))`; card (cover `aspect-ratio:16/10; object-fit:cover; object-position:top`, tag row, title, teaser, geo); case article (max-width 860px text, `.cols` grid `repeat(auto-fit,minmax(240px,1fr))` with `img{width:100%}`), `.callout`, lists, `h2` in Geologica; lightbox overlay; footer nav (prev/next + CTA); `@media (prefers-reduced-motion:reduce)`; no horizontal overflow at 390 px.
- [ ] **Step 2: Write `assets/cases.js`** — chips: read `location.hash` (`#meta|#smm|#both`), set `aria-pressed`, toggle `hidden` on cards by `data-cat`, update hash; lightbox: click on `.case-body img` opens a full-size overlay closed by click/Escape.
- [ ] **Step 3: Write `scripts/build_cases.py`** — argparse `--src`; load `cases_full.json`; `select_cases`; for each image block find `SRC/images/<basename of image_local>` (error if missing), convert with Pillow (RGB, max width 1400, WebP q80) to `assets/cases/img/<slug>-<n>.webp`, build `img` map; render `cases/<slug>/index.html` (head with `noindex`, fonts link, `/assets/cases.css`, header with logo → `/redesign/`, article, prev/next among same category, CTA → `/redesign/#contact`) and `cases/index.html` (hero, chips with counts, cards linking to `/cases/<slug>/`); update the landing counter; print the summary.
- [ ] **Step 4: Run it**

Run: `python3 scripts/build_cases.py --src "/Users/serhiihatlan/Desktop/Cloude Code/uno-agency-site/Сайт UNO/cases"`
Expected: exit 0; `cases: 46–48`; a category split whose SMM count is 18 minus the 3 unfinished and the duplicate (15–16); total image size printed. If total > 40 MB, lower quality to 72 or width to 1200 and re-run.

- [ ] **Step 5: Commit** — `git add scripts assets cases redesign && git commit -m "feat(cases): generate catalog and case pages"`.

---

### Task 3: Landing link

**Files:**
- Modify: `redesign/index.html` (cases section)

- [ ] **Step 1:** After the six-card `.cases` grid add a centered row with `<a class="pill" href="/cases/">Дивитись усі <!--cases-count-->N<!--/cases-count--> кейсів <span class="ar" aria-hidden="true">↗</span></a>`.
- [ ] **Step 2:** Re-run Task 2 Step 4 so the counter is filled; confirm `grep -c "cases-count" redesign/index.html` prints `2`.
- [ ] **Step 3: Commit** — `git commit -am "feat(redesign): link landing cases to /cases/"`.

---

### Task 4: Verification in a real browser

Run, do not read.

- [ ] **Step 1:** Start `redesign-preview` server (`.claude/launch.json`, `--directory` = the worktree) and open `/cases/`.
- [ ] **Step 2:** Desktop and 390 px screenshots of `/cases/`; click each chip and confirm the visible card count equals the chip's count; reload with `#smm` and confirm the filter is restored.
- [ ] **Step 3:** Open one text-heavy and one image-heavy case at desktop and 390 px; confirm no horizontal scroll (`document.documentElement.scrollWidth === innerWidth`), all `img` have `naturalWidth > 0`, and no 4xx in `performance.getEntriesByType("resource")`.
- [ ] **Step 4:** Click a screenshot: lightbox opens, Escape closes it.
- [ ] **Step 5:** Submit-free check that the case CTA points to `/redesign/#contact`.
- [ ] **Step 6:** Fix what the screenshots show in one batch; re-verify once; commit.
- [ ] **Step 7:** Report to the user; do not push (production deploy is the user's decision).

---

## Self-Review

- Spec coverage: data rules → Task 1; build/images/pages → Task 2; landing → Task 3; verification list → Task 4; videos skipped and out-of-scope items untouched. The spec's "cover from Notion" is replaced by first screenshot (recorded under Global Constraints).
- Placeholders: none; the implementations are written in this session against the exact tests and commands above.
- Type consistency: `select_cases` returns `cat` (used by `category`-based counts, chips and `data-cat`); `render_blocks(blocks, img, title)` matches Task 2 usage.
