# /ads Paid-Traffic Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `/ads/index.html`, a standalone, no-nav, `noindex` static landing page for paid Meta/TikTok ad traffic, structurally matching pinkbubble.agency/ads-short section-for-section but with UNO's brand colors, UNO's real case data, and a 3-field lead form wired to UNO's existing Apps Script backend.

**Architecture:** Single self-contained static HTML file (no build step, no shared stylesheet — matches `index.html`/`eng/index.html`'s existing pattern), reusing UNO's `--o`/`--dark` CSS custom properties by value and the homepage's proven `sendLead()` / case-carousel JS patterns verbatim.

**Tech Stack:** Plain HTML/CSS/vanilla JS. No frameworks, no build tooling, no new dependencies. Font: Inter (already used site-wide via Google Fonts, same `<link>` pattern as `index.html`).

## Global Constraints

- Structure/copy skeleton must match pinkbubble.agency/ads-short's section order and content shape (spec's explicit brief: fidelity to the reference, not creative reinterpretation).
- **Do not add:** a founders'-photo block, the increate-style vertical section-label motif, or an interactive ROI calculator — all three were proposed during brainstorming and explicitly rejected by the user.
- Colors: `--o:#C8521A` (orange) replaces the reference's blue accent (stat box, links); `--dark:#17181A` replaces the reference's black CTA buttons. Checkmark icons stay green (`#22c55e`) — that's a neutral UI convention in the reference, not "their" brand color, so it's not part of the recolor.
- Ukrainian only, no English toggle, no `.uk`/`.en` class-pair pattern — unlike the rest of the site, this page has exactly one language.
- `<meta name="robots" content="noindex, nofollow">` — paid-traffic-only page, not meant for organic search.
- No GSAP, no animation library, no scroll-reveal system — the reference has none, and this page's whole job is fast load + fast conversion.
- Case-study screenshots are placeholders this round (dashed-border frame + "Заміни на реальний скрін кейсу" label) — real Ads Manager screenshots come later, out of scope for this plan.
- Form must reuse the exact `sendLead(name, phone, tg, email, service)` function and Apps Script URL already live in `index.html` (copied verbatim — no backend changes). Budget dropdown value gets folded into the `service` param as `"${niche} · бюджет ${budgetLabel}"` since the endpoint has no dedicated budget field.
- Every step in this plan produces real, complete code — no `index.html` line-number references need to shift between tasks because this is a **new file being built up section by section**, so each task's HTML is appended after the previous task's closing point (explicit anchors given in each task).

---

## File Structure

One file for the whole page:
- Create: `/ads/index.html` — everything (styles, markup, JS) lives here, following the site's existing single-file-per-page convention. No new files, no shared assets beyond what's already at the site root (`favicon.svg`, Google Fonts CDN).

Tasks build this one file incrementally: Task 1 creates it with `<head>` + CSS foundation + hero; Tasks 2–6 each append one section (marked by an HTML comment anchor so later tasks have an exact, unambiguous insertion point); Task 7 is a full-page verification pass with no new markup.

---

### Task 1: Page skeleton, CSS foundation, and hero section

**Files:**
- Create: `/ads/index.html`

**Interfaces:**
- Produces: the file itself, ending in `<!-- SECTION:PROBLEM -->` as the last line before `</body>`, so Task 2 has an exact anchor to insert before. Produces CSS custom properties `--o`, `--o2`, `--dark`, `--dark2`, `--light`, `--muted`, `--r`, `--W` on `:root`, reused by every later task.

- [ ] **Step 1: Create the file with head, CSS foundation, and hero section**

```html
<!doctype html>
<html lang="uk">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>UNO Agency — реклама в промислових масштабах</title>
<meta name="description" content="Meta ADS, TikTok ADS та SMM для бізнесів по всьому світу. Реальні кейси, високий ROAS, підхід без вигорання креативів."/>
<meta name="robots" content="noindex, nofollow"/>
<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="preload" as="style" onload="this.onload=null;this.rel='stylesheet'"/>
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet"/></noscript>
<style>
:root{
  --o:#C8521A;
  --o2:#e05e1e;
  --dark:#17181A;
  --dark2:#1E1F22;
  --light:#F4F3F0;
  --muted:rgba(23,24,26,.55);
  --border:rgba(23,24,26,.12);
  --green:#22c55e;
  --r:14px;
  --W:720px;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;background:#fff;color:var(--dark);line-height:1.5;-webkit-font-smoothing:antialiased}
.W{max-width:var(--W);margin:0 auto;padding:0 24px}
section{padding:56px 0}
h1{font-size:clamp(30px,5vw,44px);font-weight:900;line-height:1.12;letter-spacing:-0.02em}
h2{font-size:clamp(22px,3.4vw,30px);font-weight:800;line-height:1.18;letter-spacing:-0.015em}
h3{font-size:17px;font-weight:800;line-height:1.3}
p{color:var(--muted)}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}

.logo-row{display:flex;align-items:center;gap:8px;padding-top:32px;margin-bottom:36px}
.logo-dot{width:14px;height:14px;border-radius:50%;background:var(--o)}
.logo-word{font-size:15px;font-weight:800}

.hero-stat{background:var(--o);color:#fff;border-radius:var(--r);padding:20px 24px;display:flex;align-items:center;gap:18px;margin:24px 0 28px;flex-wrap:wrap}
.hero-stat-num{font-size:34px;font-weight:900;letter-spacing:-0.02em;white-space:nowrap}
.hero-stat-lbl{font-size:13.5px;line-height:1.4;opacity:.92}

.check-list{list-style:none;display:flex;flex-direction:column;gap:12px;margin-bottom:32px}
.check-list li{display:flex;align-items:flex-start;gap:10px;font-size:15px}
.check-ico{width:20px;height:20px;flex-shrink:0;margin-top:1px}

.btn-cta{display:inline-flex;align-items:center;gap:10px;background:var(--dark);color:#fff;padding:16px 28px;border-radius:100px;font-size:15px;font-weight:700;border:none;cursor:pointer;transition:background .2s,transform .2s}
.btn-cta:hover{background:var(--dark2);transform:translateY(-1px)}
.btn-cta svg{width:16px;height:16px;flex-shrink:0}

@media(max-width:480px){
  .hero-stat{flex-direction:column;align-items:flex-start;gap:6px}
}
</style>
</head>
<body>

<!-- ════ HEADER ════ -->
<div class="W">
  <div class="logo-row">
    <div class="logo-dot"></div>
    <div class="logo-word">UNO Agency</div>
  </div>
</div>

<!-- ════ 1. HERO ════ -->
<section id="hero">
  <div class="W">
    <h1>Реклама, яка приносить продажі, а не лайки</h1>

    <div class="hero-stat">
      <div class="hero-stat-num">$7M+</div>
      <div class="hero-stat-lbl">виручки згенеровано для клієнтів через Meta ADS, TikTok ADS та SMM</div>
    </div>

    <ul class="check-list">
      <li>
        <svg class="check-ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#22c55e"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Високий ROAS на дистанції, без різких провалів
      </li>
      <li>
        <svg class="check-ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#22c55e"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Необмежена кількість креативів щомісяця
      </li>
      <li>
        <svg class="check-ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#22c55e"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Працюємо з Meta, TikTok, Instagram
      </li>
      <li>
        <svg class="check-ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#22c55e"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Підхід, перевірений на реальних бюджетах клієнтів
      </li>
    </ul>

    <button class="btn-cta" onclick="openLeadModal()">
      обговорити проєкт
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
    </button>
  </div>
</section>

<!-- SECTION:PROBLEM -->
</body>
</html>
```

- [ ] **Step 2: Verify the file renders with no errors**

```bash
python3 -m http.server 8960 &
sleep 1
```

Then, using the browser tool: navigate to `http://localhost:8960/ads/`, run `read_console_messages` (expect no errors), and confirm via `javascript_tool`:

```js
JSON.stringify({
  title: document.title,
  h1: document.querySelector('h1').textContent,
  statNum: document.querySelector('.hero-stat-num').textContent,
  checklistCount: document.querySelectorAll('.check-list li').length,
  ctaText: document.querySelector('.btn-cta').textContent.trim()
})
```

Expected: `{"title":"UNO Agency — реклама в промислових масштабах","h1":"Реклама, яка приносить продажі, а не лайки","statNum":"$7M+","checklistCount":4,"ctaText":"обговорити проєкт"}`

- [ ] **Step 3: Commit**

```bash
git add ads/index.html
git commit -m "$(cat <<'EOF'
feat: add /ads landing page skeleton, CSS foundation, hero

First section of the pinkbubble.agency-inspired paid-traffic
landing page — head/meta (noindex, since this is ad-campaign-only,
not organic-search content), CSS custom properties reusing UNO's
existing --o/--dark brand colors, and the hero section (headline,
stat callout, 4-item checklist, CTA).

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Problem section + pivot line + "how it works" 3-card grid

**Files:**
- Modify: `/ads/index.html` — insert before the `<!-- SECTION:PROBLEM -->` comment left by Task 1

**Interfaces:**
- Consumes: `.W`, `.check-list`/`.check-ico` CSS from Task 1 (reused for the problem list).
- Produces: ends with `<!-- SECTION:ROAS -->` as the new anchor for Task 3.

- [ ] **Step 1: Add CSS for this section, inside the existing `<style>` block, right before its closing `</style>` tag**

```css
.pain-list{list-style:none;display:flex;flex-direction:column;gap:10px;margin:20px 0 0}
.pain-list li{display:flex;align-items:flex-start;gap:10px;font-size:15px;color:var(--muted)}
.pain-ico{width:20px;height:20px;flex-shrink:0;margin-top:1px;color:var(--o)}
.pivot{font-size:17px;font-weight:600;margin-top:24px}
.pivot b{color:var(--o)}

.how-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}
.how-card{border:1px solid var(--border);border-radius:var(--r);padding:24px 20px}
.how-card h3{margin-bottom:8px}
.how-card p{font-size:13.5px;line-height:1.55}

@media(max-width:720px){
  .how-grid{grid-template-columns:1fr}
}
```

- [ ] **Step 2: Insert the section markup, replacing `<!-- SECTION:PROBLEM -->` with this block followed by the same comment moved to the end**

```html
<!-- ════ 2. PROBLEM ════ -->
<section id="problem">
  <div class="W">
    <h2>Більшість бізнесів мають проблеми з рекламою:</h2>
    <ul class="pain-list">
      <li><svg class="pain-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>Один рекламний акаунт без системи тестування</li>
      <li><svg class="pain-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>Креативи не оновлюються і швидко вигорають</li>
      <li><svg class="pain-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>Ціна за лід постійно росте</li>
      <li><svg class="pain-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>Немає чіткої аналітики — незрозуміло, що працює</li>
      <li><svg class="pain-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>Агенція зникає одразу після підключення</li>
    </ul>
    <p class="pivot">Наш підхід <b>кардинально відрізняється</b> — тому ми швидко масштабуємо рекламу, зберігаючи високий ROAS.</p>

    <div class="how-grid">
      <div class="how-card">
        <h3>Необмежена кількість креативів</h3>
        <p>Постійно тестуємо велику кількість унікальних креативів. Навіть коли все працює добре — ми продовжуємо тестувати.</p>
      </div>
      <div class="how-card">
        <h3>Повний продакшн</h3>
        <p>Від сценарію до монтажу — все робимо самі. Вам не потрібні окремі монтажери й копірайтери.</p>
      </div>
      <div class="how-card">
        <h3>База перевірених форматів</h3>
        <p>Роками збираємо базу креативів і зв'язок, що дають результат. Стартуємо з того, що вже працює.</p>
      </div>
    </div>
  </div>
</section>

<!-- SECTION:ROAS -->
```

- [ ] **Step 3: Verify**

Using the browser tool at `http://localhost:8960/ads/`, `read_console_messages` (expect no errors), then:

```js
JSON.stringify({
  painCount: document.querySelectorAll('.pain-list li').length,
  howCardCount: document.querySelectorAll('.how-card').length,
  pivotHasO: getComputedStyle(document.querySelector('.pivot b')).color
})
```

Expected: `painCount: 5`, `howCardCount: 3`, `pivotHasO` resolves to `rgb(200, 82, 26)` (the `--o` orange).

- [ ] **Step 4: Commit**

```bash
git add ads/index.html
git commit -m "$(cat <<'EOF'
feat: add /ads problem section and how-it-works cards

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: "High ROAS" explanation + "replace your traffic team" checklist

**Files:**
- Modify: `/ads/index.html` — insert before `<!-- SECTION:ROAS -->`

**Interfaces:**
- Consumes: `.check-list`/`.check-ico` from Task 1, `.W`/`h2`/`p` from Task 1.
- Produces: ends with `<!-- SECTION:CASES -->` as the anchor for Task 4.

- [ ] **Step 1: Add CSS, before the closing `</style>`**

```css
.roas-block{background:var(--light);border-radius:var(--r);padding:28px 24px;margin:24px 0}
.roas-block p{color:var(--dark);font-size:15px;line-height:1.6;margin-bottom:12px}
.roas-block p:last-child{margin-bottom:0}
.roas-block b{color:var(--o)}
```

- [ ] **Step 2: Insert the section, replacing `<!-- SECTION:ROAS -->`**

```html
<!-- ════ 3. HIGH ROAS ════ -->
<section id="roas">
  <div class="W">
    <h2>Тримаємо високий ROAS на дистанції</h2>
    <div class="roas-block">
      <p>Постійно <b>аналізуємо кожну зв'язку</b> — на основі даних розробляємо ще кращі гіпотези для наступних кампаній.</p>
      <p>Одночасно крутимо <b>багато креативів</b>, щоб реклама працювала стабільно, довго і з мінімальними коливаннями в окупності.</p>
    </div>

    <h2>Замінюємо вам цілий відділ маркетингу</h2>
    <ul class="check-list" style="margin-top:20px">
      <li>
        <svg class="check-ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#22c55e"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Беремо на себе всю роботу з акаунтами й блокуваннями
      </li>
      <li>
        <svg class="check-ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#22c55e"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Перевірені налаштування та структури кампаній
      </li>
      <li>
        <svg class="check-ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#22c55e"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Щоденний аналіз і звітність по результатах
      </li>
      <li>
        <svg class="check-ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#22c55e"/><path d="M8 12l3 3 5-6" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Докручуємо лендінги і пишемо ТЗ на нові сторінки
      </li>
    </ul>
  </div>
</section>

<!-- SECTION:CASES -->
```

- [ ] **Step 3: Verify**

```js
JSON.stringify({
  roasBlockText: document.querySelector('.roas-block').textContent.length > 50,
  teamCheckCount: document.querySelectorAll('#roas .check-list li').length
})
```

Expected: `roasBlockText: true`, `teamCheckCount: 4`.

- [ ] **Step 4: Commit**

```bash
git add ads/index.html
git commit -m "$(cat <<'EOF'
feat: add /ads ROAS explanation and traffic-team checklist

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Case-study carousel with real UNO data (placeholder screenshots)

**Files:**
- Modify: `/ads/index.html` — insert before `<!-- SECTION:CASES -->`

**Interfaces:**
- Consumes: `.W` from Task 1.
- Produces: `csMove(dir)`, `csGo(i)`, `csUpdate()` JS functions and `#csTrack`/`#csDots` DOM ids — self-contained to this page, no cross-task consumers. Ends with `<!-- SECTION:PLATFORMS -->` as the anchor for Task 5.

Case data below is copied verbatim from the real numbers already live on the homepage (`index.html`'s `.cs-slide` blocks) — not invented for this page.

- [ ] **Step 1: Add CSS, before the closing `</style>`**

```css
.cs-wrap{position:relative;overflow:hidden;margin-top:28px}
.cs-track{display:flex;transition:transform .45s cubic-bezier(.4,0,.2,1)}
.cs-slide{min-width:100%;border:1px solid var(--border);border-radius:var(--r);overflow:hidden}
.cs-shot{aspect-ratio:16/10;background:repeating-linear-gradient(45deg,#f7f6f4,#f7f6f4 10px,#efeeec 10px,#efeeec 20px);border:2px dashed var(--border);display:flex;align-items:center;justify-content:center;text-align:center;padding:20px}
.cs-shot span{font-size:13px;color:var(--muted);font-weight:600}
.cs-cap{padding:18px 20px}
.cs-tag{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--o);margin-bottom:8px}
.cs-cap p{color:var(--dark);font-size:15px;line-height:1.5}
.cs-cap p b{color:var(--o)}

.cs-nav{display:flex;align-items:center;justify-content:center;gap:16px;margin-top:18px}
.cs-arrow{width:40px;height:40px;border-radius:50%;background:var(--dark);border:none;color:#fff;font-size:18px;cursor:pointer;transition:.2s;display:flex;align-items:center;justify-content:center;line-height:1}
.cs-arrow:hover{background:var(--dark2)}
.cs-dots{display:flex;gap:7px;align-items:center}
.cs-dot{width:7px;height:7px;border-radius:50%;background:var(--border);cursor:pointer;transition:.3s}
.cs-dot.active{background:var(--o);width:20px;border-radius:4px}
```

- [ ] **Step 2: Insert the section, replacing `<!-- SECTION:CASES -->`**

```html
<!-- ════ 4. CASES ════ -->
<section id="cases">
  <div class="W">
    <h2>Результати, які можна виміряти</h2>

    <div class="cs-wrap">
      <div class="cs-track" id="csTrack">

        <div class="cs-slide">
          <div class="cs-shot"><span>Заміни на реальний скрін кейсу<br/>(Ads Manager · магазин іграшок)</span></div>
          <div class="cs-cap">
            <div class="cs-tag">🛍 Meta ADS · E-commerce · Україна</div>
            <p><b>1366% ROAS.</b> Витрачено $24,780, отримано 14,468 покупок по $1.71, виручка — <b>$379,564</b></p>
          </div>
        </div>

        <div class="cs-slide">
          <div class="cs-shot"><span>Заміни на реальний скрін кейсу<br/>(Ads Manager · beauty, Канада)</span></div>
          <div class="cs-cap">
            <div class="cs-tag">💋 Meta ADS · Beauty · Канада</div>
            <p>Відмовились від трафіку на сайт, зробили ставку на ціль «Повідомлення» — <b>2646% ROAS</b>, $29,225 заробітку з $1,104 витрат</p>
          </div>
        </div>

        <div class="cs-slide">
          <div class="cs-shot"><span>Заміни на реальний скрін кейсу<br/>(Ads Manager · товари для вій)</span></div>
          <div class="cs-cap">
            <div class="cs-tag">💄 Meta ADS · E-commerce · Україна</div>
            <p>Ретаргетинг лояльних клієнтів і робота з повторними покупками — <b>1411% ROAS</b> при бюджеті $23,296</p>
          </div>
        </div>

        <div class="cs-slide">
          <div class="cs-shot"><span>Заміни на реальний скрін кейсу<br/>(Ads Manager · продаж котеджів)</span></div>
          <div class="cs-cap">
            <div class="cs-tag">🏡 Meta ADS · E-commerce · Україна · 44 міс LTV</div>
            <p>Проєкт з нульовими результатами перетворили на масштабований бізнес — <b>1088% ROAS</b>, ₴2,090,534 виручки</p>
          </div>
        </div>

        <div class="cs-slide">
          <div class="cs-shot"><span>Заміни на реальний скрін кейсу<br/>(Ads Manager · нерухомість)</span></div>
          <div class="cs-cap">
            <div class="cs-tag">🏘 Meta ADS · Нерухомість · Україна</div>
            <p>Довгий цикл рішення — побудували воронку від прогріву до заявки. З $1,684 витрат — <b>$210,000</b> суми продажів</p>
          </div>
        </div>

        <div class="cs-slide">
          <div class="cs-shot"><span>Заміни на реальний скрін кейсу<br/>(Ads Manager · beauty, запис)</span></div>
          <div class="cs-cap">
            <div class="cs-tag">💇 Meta ADS · Beauty · Канада</div>
            <p>Стабільний потік нових клієнтів на запис через сегментацію й ретаргетинг — <b>29 міс LTV</b> клієнта, $41,664 бюджету</p>
          </div>
        </div>

        <div class="cs-slide">
          <div class="cs-shot"><span>Заміни на реальний скрін кейсу<br/>(Ads Manager · мовна школа)</span></div>
          <div class="cs-cap">
            <div class="cs-tag">📚 Meta ADS · EdTech · Польща</div>
            <p>Старт з нуля — без сайту й кабінету. Відео «з лицем» + безкоштовний урок — <b>$3.48</b> за лід, 1,124 ліди</p>
          </div>
        </div>

      </div><!-- /cs-track -->

      <div class="cs-nav">
        <button class="cs-arrow" onclick="csMove(-1)">←</button>
        <div class="cs-dots" id="csDots"></div>
        <button class="cs-arrow" onclick="csMove(1)">→</button>
      </div>
    </div><!-- /cs-wrap -->
  </div>
</section>

<script>
var csIdx=0;
var csSlides=document.querySelectorAll('.cs-slide');
var csTotal=csSlides.length;

function csMove(dir){
  csIdx=(csIdx+dir+csTotal)%csTotal;
  csUpdate();
}
function csGo(i){csIdx=i;csUpdate();}
function csUpdate(){
  document.getElementById('csTrack').style.transform='translateX(-'+csIdx*100+'%)';
  document.querySelectorAll('.cs-dot').forEach(function(d,i){d.classList.toggle('active',i===csIdx);});
}
(function(){
  var el=document.getElementById('csDots');
  if(!el) return;
  for(var i=0;i<csTotal;i++){
    var d=document.createElement('div');
    d.className='cs-dot'+(i===0?' active':'');
    (function(idx){d.onclick=function(){csGo(idx);};})(i);
    el.appendChild(d);
  }
  var track=document.getElementById('csTrack');
  var startX=0;
  if(track){
    track.addEventListener('touchstart',function(e){startX=e.touches[0].clientX;},{passive:true});
    track.addEventListener('touchend',function(e){
      var dx=e.changedTouches[0].clientX-startX;
      if(Math.abs(dx)>50) csMove(dx>0?-1:1);
    });
  }
})();
</script>

<!-- SECTION:PLATFORMS -->
```

- [ ] **Step 3: Verify carousel logic works**

```js
JSON.stringify({
  slideCount: document.querySelectorAll('.cs-slide').length,
  dotCount: document.querySelectorAll('.cs-dot').length,
  firstDotActive: document.querySelector('.cs-dot').classList.contains('active')
})
```

Expected: `slideCount: 8`, `dotCount: 8`, `firstDotActive: true`.

Then click the right arrow (`.cs-arrow` second one, or call `csMove(1)` via `javascript_exec`) and re-check:

```js
csMove(1);
JSON.stringify({
  trackTransform: document.getElementById('csTrack').style.transform,
  activeDotIndex: Array.from(document.querySelectorAll('.cs-dot')).findIndex(d=>d.classList.contains('active'))
})
```

Expected: `trackTransform: "translateX(-100%)"`, `activeDotIndex: 1`.

- [ ] **Step 4: Commit**

```bash
git add ads/index.html
git commit -m "$(cat <<'EOF'
feat: add /ads case-study carousel with real UNO case data

8 cases, numbers copied verbatim from the live homepage's own case
section (index.html .cs-slide blocks) — no invented figures.
Screenshot slots are placeholders (dashed frame, clearly labeled)
until real Ads Manager screenshots are added in a follow-up pass.
Carousel JS (drag/dots/touch-swipe) reuses the proven pattern
already running on the homepage.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Platforms row + footer CTA band + sticky Telegram button

**Files:**
- Modify: `/ads/index.html` — insert before `<!-- SECTION:PLATFORMS -->`

**Interfaces:**
- Consumes: `.W`, `.btn-cta` from Task 1.
- Produces: ends with `<!-- SECTION:MODAL -->` as the anchor for Task 6. Introduces `.sticky-cta` (fixed-position, always visible after this task).

- [ ] **Step 1: Add CSS, before the closing `</style>`**

```css
.platform-row{display:flex;gap:14px;margin-top:24px;flex-wrap:wrap}
.platform-pill{border:1px solid var(--border);border-radius:100px;padding:10px 20px;font-size:14px;font-weight:700;color:var(--dark)}

.footer-cta{background:var(--dark);color:#fff;border-radius:var(--r);padding:40px 28px;text-align:center;margin:0 24px}
.footer-cta h2{color:#fff}
.footer-cta p{color:rgba(255,255,255,.65);margin:12px 0 24px}
.footer-cta .btn-cta{background:var(--o)}
.footer-cta .btn-cta:hover{background:var(--o2)}

.sticky-cta{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid var(--border);padding:12px 24px;display:flex;justify-content:center;z-index:50;box-shadow:0 -4px 20px rgba(0,0,0,.06)}
.sticky-cta .btn-cta{width:100%;max-width:400px;justify-content:center;background:var(--o)}
.sticky-cta .btn-cta:hover{background:var(--o2)}
body{padding-bottom:76px}
```

- [ ] **Step 2: Insert the section, replacing `<!-- SECTION:PLATFORMS -->`**

```html
<!-- ════ 5. PLATFORMS ════ -->
<section id="platforms">
  <div class="W">
    <h2>Запустимо вам всі джерела трафіку</h2>
    <p style="margin-top:8px">Ллємо трафік з Meta, TikTok, Instagram — щоб ваш проєкт отримав максимум обʼєму і легше масштабувався</p>
    <div class="platform-row">
      <div class="platform-pill">Meta</div>
      <div class="platform-pill">TikTok</div>
      <div class="platform-pill">Instagram</div>
    </div>
  </div>
</section>

<!-- ════ 6. FOOTER CTA ════ -->
<section id="footer-cta">
  <div class="footer-cta">
    <h2>Потрібна команда, яка дає результат на дистанції?</h2>
    <p>Залишайте заявку — напишемо в Telegram, обговоримо проєкт і надішлемо більше інформації про послуги</p>
    <button class="btn-cta" onclick="openLeadModal()">
      обговорити проєкт
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
    </button>
  </div>
</section>

<!-- ════ STICKY CTA ════ -->
<div class="sticky-cta">
  <button class="btn-cta" onclick="openLeadModal()">
    зв'язатись в telegram
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></svg>
  </button>
</div>

<!-- SECTION:MODAL -->
```

- [ ] **Step 3: Verify**

```js
JSON.stringify({
  platformCount: document.querySelectorAll('.platform-pill').length,
  stickyVisible: getComputedStyle(document.querySelector('.sticky-cta')).position,
  bodyPaddingBottom: getComputedStyle(document.body).paddingBottom
})
```

Expected: `platformCount: 3`, `stickyVisible: "fixed"`, `bodyPaddingBottom: "76px"`.

- [ ] **Step 4: Commit**

```bash
git add ads/index.html
git commit -m "$(cat <<'EOF'
feat: add /ads platforms row, footer CTA, sticky Telegram button

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Lead modal — 3-field form wired to the existing Apps Script endpoint

**Files:**
- Modify: `/ads/index.html` — insert before `<!-- SECTION:MODAL -->`, and add the `openLeadModal()`/`closeLeadModal()`/`sendLead()`/`submitLeadForm()` functions referenced by every CTA button added in Tasks 1, 3, and 5 (`onclick="openLeadModal()"`).

**Interfaces:**
- Consumes: nothing new from earlier tasks besides the already-placed `onclick="openLeadModal()"` calls.
- Produces: `openLeadModal()`, `closeLeadModal()`, `sendLead(name, phone, tg, email, service)`, `submitLeadForm()` — final functions for this page, nothing later depends on them.

- [ ] **Step 1: Add CSS, before the closing `</style>`**

```css
.modal-overlay{position:fixed;inset:0;background:rgba(23,24,26,.5);display:none;align-items:center;justify-content:center;z-index:100;padding:20px}
.modal-overlay.open{display:flex}
.modal-box{background:#fff;border-radius:var(--r);padding:28px 24px;max-width:420px;width:100%;position:relative;max-height:90vh;overflow-y:auto}
.modal-close{position:absolute;top:16px;right:16px;width:32px;height:32px;border-radius:50%;background:var(--light);border:none;cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center}
.modal-box h3{font-size:19px;margin-bottom:20px;padding-right:32px}
.f-label{display:block;font-size:13px;font-weight:700;margin-bottom:6px;margin-top:16px}
.f-label:first-of-type{margin-top:0}
.f-input,.f-select{width:100%;padding:13px 14px;border:1.5px solid var(--border);border-radius:10px;font-size:14px;font-family:inherit;background:#fff}
.f-input:focus,.f-select:focus{outline:none;border-color:var(--o)}
.f-submit{width:100%;background:var(--dark);color:#fff;border:none;padding:15px;border-radius:10px;font-size:15px;font-weight:700;cursor:pointer;margin-top:20px;transition:background .2s}
.f-submit:disabled{background:var(--border);cursor:not-allowed}
.f-submit:not(:disabled):hover{background:var(--dark2)}
.f-note{font-size:11.5px;color:var(--muted);margin-top:10px;text-align:center}
#leadOk{display:none;text-align:center;padding:20px 0}
#leadOk svg{width:48px;height:48px;color:var(--green);margin:0 auto 12px}
```

- [ ] **Step 2: Insert the modal markup and JS, replacing `<!-- SECTION:MODAL -->`**

```html
<!-- ════ LEAD MODAL ════ -->
<div class="modal-overlay" id="leadModal" onclick="if(event.target===this) closeLeadModal()">
  <div class="modal-box">
    <button class="modal-close" onclick="closeLeadModal()">✕</button>
    <div id="leadFormBox">
      <h3>Заповніть форму і ми напишемо вам в Telegram</h3>

      <label class="f-label" for="lTg">Ваш @нікнейм або номер в Telegram</label>
      <input class="f-input" type="text" id="lTg" placeholder="@нікнейм або номер" oninput="updateSubmitState()"/>

      <label class="f-label" for="lBudget">Який ваш місячний рекламний бюджет?</label>
      <select class="f-select" id="lBudget" onchange="updateSubmitState()">
        <option value="">Оберіть ваш місячний бюджет</option>
        <option value="Не запускали рекламу раніше">Не запускали рекламу раніше</option>
        <option value="до $1 000">до $1 000</option>
        <option value="$1 000 – 3 000">$1 000 – 3 000</option>
        <option value="$3 000 – 10 000">$3 000 – 10 000</option>
        <option value="$10 000 – 30 000">$10 000 – 30 000</option>
        <option value="$30 000+">$30 000+</option>
      </select>

      <label class="f-label" for="lNiche">Яка у вас ніша?</label>
      <select class="f-select" id="lNiche" onchange="updateSubmitState()">
        <option value="">Ваша ніша</option>
        <option value="Онлайн-школа">Онлайн-школа</option>
        <option value="Mobile Apps / SaaS">Mobile Apps / SaaS</option>
        <option value="Нерухомість">Нерухомість</option>
        <option value="Ecommerce">Ecommerce</option>
        <option value="Послуги">Послуги</option>
        <option value="Інше">Інше</option>
      </select>

      <!-- Honeypot: люди цього поля не бачать і не заповнюють, боти заповнюють усе
           підряд. Непорожнє значення = бот, заявка тихо відкидається на сервері. -->
      <input type="text" id="hpField" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"
             style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0;pointer-events:none"/>

      <button class="f-submit" id="lSubmit" onclick="submitLeadForm()" disabled>обговорити проєкт</button>
      <p class="f-note">Натискаючи кнопку, ви погоджуєтесь з обробкою персональних даних</p>
    </div>
    <div id="leadOk">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
      <h3 style="padding-right:0">Дякуємо! Ми напишемо вам найближчим часом.</h3>
    </div>
  </div>
</div>

<script>
function openLeadModal(){
  document.getElementById('leadModal').classList.add('open');
  document.body.style.overflow='hidden';
}
function closeLeadModal(){
  document.getElementById('leadModal').classList.remove('open');
  document.body.style.overflow='';
}
document.addEventListener('keydown',function(e){if(e.key==='Escape') closeLeadModal();});

function updateSubmitState(){
  var tg=document.getElementById('lTg').value.trim();
  var budget=document.getElementById('lBudget').value;
  var niche=document.getElementById('lNiche').value;
  document.getElementById('lSubmit').disabled = !(tg && budget && niche);
}

async function sendLead(name, phone, tg, email, service){
  const eventId = 'lead_' + Date.now() + '_' + Math.random().toString(36).slice(2,8);
  try {
    if(typeof fbq === 'function') fbq('track', 'Lead', {}, {eventID: eventId});
  } catch(e){}
  const ck = n => (document.cookie.split(';').map(c=>c.trim()).find(c=>c.startsWith(n+'=')) || '').split('=')[1] || '';
  const hp = (document.getElementById('hpField')||{}).value || '';
  const _p = new URLSearchParams({
    name, phone, tg: tg||'', email: email||'', service: service||'',
    event_id: eventId, ua: navigator.userAgent,
    fbp: ck('_fbp'), fbc: ck('_fbc'),
    source_url: location.href, hp
  });
  const url = 'https://script.google.com/macros/s/AKfycbxKAhhCP7qKwJ9BW4yZqgdtg_nA5bADqoT1Po_4sWKA6Zdphq_2Inq0MP_0CAJGtNthCg/exec?'+_p;

  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const r = await fetch(url);
      if (r.ok) return;
      console.error('lead → Apps Script: HTTP', r.status, 'спроба', attempt);
    } catch(e){ console.error('lead → Apps Script:', e, 'спроба', attempt); }
    if (attempt < 3) await new Promise(res => setTimeout(res, attempt * 1500));
  }
  console.error('lead → Apps Script: ЗАЯВКА НЕ ДОСТАВЛЕНА після 3 спроб', {name, phone});
}

function submitLeadForm(){
  var tg=document.getElementById('lTg').value.trim();
  var budgetLabel=document.getElementById('lBudget').value;
  var niche=document.getElementById('lNiche').value;
  if(!tg || !budgetLabel || !niche) return;
  var service = niche + ' · бюджет ' + budgetLabel;
  sendLead(tg, '', tg, '', service);
  document.getElementById('leadFormBox').style.display='none';
  document.getElementById('leadOk').style.display='block';
}
</script>

<!-- SECTION:END -->
```

- [ ] **Step 3: Verify the modal open/close/validation flow**

```js
openLeadModal();
const beforeFill = document.getElementById('lSubmit').disabled;
document.getElementById('lTg').value = '@testuser';
document.getElementById('lTg').dispatchEvent(new Event('input'));
document.getElementById('lBudget').value = 'до $1 000';
document.getElementById('lBudget').dispatchEvent(new Event('change'));
document.getElementById('lNiche').value = 'Ecommerce';
document.getElementById('lNiche').dispatchEvent(new Event('change'));
const afterFill = document.getElementById('lSubmit').disabled;
JSON.stringify({modalOpen: document.getElementById('leadModal').classList.contains('open'), beforeFill, afterFill})
```

Expected: `modalOpen: true`, `beforeFill: true`, `afterFill: false`.

Then close it (`closeLeadModal()` via `javascript_exec`) and confirm `document.getElementById('leadModal').classList.contains('open')` is `false`.

Do **not** actually click submit in this verification step — that would send a real test lead to the live Apps Script endpoint/Telegram channel. A real end-to-end submission check happens once, deliberately, in Task 7.

- [ ] **Step 4: Commit**

```bash
git add ads/index.html
git commit -m "$(cat <<'EOF'
feat: add /ads lead modal wired to the existing Apps Script endpoint

3-field form (Telegram handle, budget, niche) matching the
pinkbubble.agency reference exactly. Reuses sendLead() verbatim
from the homepage — same endpoint, same 3-attempt retry, same
honeypot/fbp/fbc tracking. No backend changes: budget is folded
into the existing `service` param since the endpoint has no
dedicated budget field.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Full-page verification pass

**Files:** none — verification only, no new markup.

- [ ] **Step 1: Serve and load both the full page and confirm no console errors**

```bash
python3 -m http.server 8960 &
sleep 1
```

Browser tool: navigate to `http://localhost:8960/ads/`, `read_console_messages` with `onlyErrors: true` — expect empty.

- [ ] **Step 2: Confirm every section from the spec is present, in order**

```js
JSON.stringify(Array.from(document.querySelectorAll('section')).map(s => s.id))
```

Expected: `["hero","problem","roas","cases","platforms","footer-cta"]`

- [ ] **Step 3: Mobile viewport check (375px) — no horizontal overflow**

Using the browser tool's `resize_window` with `width: 375, height: 812`, reload, then:

```js
JSON.stringify({docWidth: document.documentElement.scrollWidth, viewport: window.innerWidth})
```

Expected: `docWidth === viewport === 375`. If not, identify the overflowing element (`document.elementFromPoint` at the right edge, or check `.hero-stat`/`.how-grid`/`.cs-slide` widths) and fix before proceding — this is the same overflow-check discipline used throughout this session's other pages.

Reset viewport afterward (`resize_window` preset `desktop`).

- [ ] **Step 4: Placeholder frames are visually unmistakable**

```js
JSON.stringify({
  placeholderCount: document.querySelectorAll('.cs-shot').length,
  placeholderText: document.querySelector('.cs-shot span').textContent
})
```

Expected: `placeholderCount: 8`, `placeholderText` contains "Заміни на реальний скрін".

- [ ] **Step 5: One real end-to-end form submission**

This is the only step in the whole plan that should actually hit the live Apps Script endpoint — do it once, deliberately, with an obviously-test value so it's easy to spot and ignore in the Sheet/Telegram channel:

Fill the form with `lTg = "@TEST-ads-landing-verification"`, budget = "до $1 000", niche = "Інше", then click the real submit button (`document.getElementById('lSubmit').click()`, or a real `computer` click).

Confirm the UI shows the thank-you state:

```js
JSON.stringify({formHidden: getComputedStyle(document.getElementById('leadFormBox')).display, okShown: getComputedStyle(document.getElementById('leadOk')).display})
```

Expected: `formHidden: "none"`, `okShown: "block"`.

Tell the user afterward that a test lead tagged `@TEST-ads-landing-verification` was sent through the real pipeline, so they can spot and ignore it in the Sheet/Telegram channel rather than mistaking it for a real inquiry.

- [ ] **Step 6: Stop the test server**

```bash
pkill -f "http.server 8960"
```

- [ ] **Step 7: Commit (only if Step 3 required a fix; otherwise this task has nothing to commit)**

If Step 3 needed a CSS fix:

```bash
git add ads/index.html
git commit -m "$(cat <<'EOF'
fix: resolve mobile horizontal overflow on /ads

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

## Self-Review Notes

- **Spec coverage:** hero (stat/checklist/CTA) ✓ Task 1, problem+pivot+how-it-works ✓ Task 2, ROAS+team-replacement ✓ Task 3, case carousel with real data + placeholders ✓ Task 4, platforms+footer+sticky CTA ✓ Task 5, 3-field form wired to existing endpoint ✓ Task 6, full verification incl. mobile + one real submission ✓ Task 7. Explicit non-goals (founders' photo, vertical labels, calculator, English version) — none present in any task, confirmed by re-reading the spec's "Explicit non-goals" section against every task's markup.
- **Placeholder scan:** no TBD/TODO; every step has complete HTML/CSS/JS or a real command with a real expected value. The case-image `.cs-shot` divs are *intentional, spec-mandated* placeholders (not plan placeholders) — they're fully-specified, styled, labeled elements, not "fill in later" instructions to the plan's reader.
- **Type/naming consistency:** `openLeadModal()`/`closeLeadModal()` referenced by every CTA button across Tasks 1, 3, and 5 match the function names actually defined in Task 6 exactly. `sendLead(name, phone, tg, email, service)` signature in Task 6 matches its single caller (`submitLeadForm()`, same task) exactly. `csMove`/`csGo`/`csUpdate`/`csTrack`/`csDots` are self-contained within Task 4, no other task references them.
