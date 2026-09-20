#!/usr/bin/env python3
"""Build /cases/ from the Notion export.

    python3 scripts/build_cases.py --src "<main checkout>/Сайт UNO/cases"

Reads cases_full.json + images/, writes assets/cases/img/*.webp, cases/index.html
and cases/<slug>/index.html, and updates the case counter on the landing.
"""
import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

from cases_lib import render_blocks, select_cases, teaser

ROOT = Path(__file__).resolve().parent.parent
CATS = {"meta": "Meta Ads", "smm": "SMM", "both": "Meta Ads + SMM"}
MAX_W, QUALITY = 1400, 80
FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,600"
         "&family=Geologica:wght@300;400;600&family=Onest:wght@400;500;600&display=swap")


def e(s):
    return html.escape(s or "", quote=True)


def image_blocks(blocks):
    for b in blocks:
        if b["type"] == "image":
            yield b
        yield from image_blocks(b.get("children", []))


def to_webp(src, dest):
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    im.save(dest, "WEBP", quality=QUALITY, method=4)
    return im.width, im.height


def good_cover(m):
    """A screenshot works as a card cover only if it is tall enough and not a thin strip."""
    return m["h"] >= 300 and 0.5 <= m["w"] / m["h"] <= 2.5


def head(title, desc):
    return (f'<!DOCTYPE html>\n<html lang="uk">\n<head>\n<meta charset="UTF-8"/>\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"/>\n'
            f'<title>{e(title)}</title>\n<meta name="description" content="{e(desc)}"/>\n'
            f'<meta name="robots" content="noindex, nofollow"/>\n'
            f'<link rel="icon" type="image/svg+xml" href="/favicon.svg"/>\n'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"/>\n'
            f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>\n'
            f'<link href="{FONTS}" rel="stylesheet"/>\n<link href="/assets/cases.css" rel="stylesheet"/>\n'
            f'</head>\n<body>\n')


NAV = ('<header class="nav"><div class="wrap"><a class="logo" href="/redesign/" aria-label="UNO Agency, на головну">'
       'UNO <i>Agency</i></a><div class="nav-r"><a href="/cases/">Усі кейси</a>'
       '<a class="pill" href="/redesign/#contact">Заявка <span aria-hidden="true">↗</span></a></div></div></header>\n')
FOOT = ('<footer><div class="wrap">© UNO Agency · Meta Ads · TikTok Ads · SMM</div></footer>\n'
        '<script src="/assets/cases.js" defer></script>\n</body>\n</html>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="folder with cases_full.json and images/")
    ap.add_argument("--allow-missing", action="store_true",
                    help="skip missing/unreadable screenshots (listed at the end) instead of failing")
    args = ap.parse_args()
    src = Path(args.src)
    raw = json.loads((src / "cases_full.json").read_text(encoding="utf8"))
    cases = select_cases(raw)

    problems, skipped = [], []
    if any(c["cat"] == "" for c in cases):
        problems += [f"no category: {c['title']}" for c in cases if c["cat"] == ""]

    out_img = ROOT / "assets" / "cases" / "img"
    if out_img.exists():
        shutil.rmtree(out_img)
    out_img.mkdir(parents=True)

    img, total, case_imgs = {}, 0, {}
    for c in cases:
        n = 0
        for b in image_blocks(c["blocks"]):
            key = b.get("image_local", "").rsplit("/", 1)[-1]
            if key in img:
                case_imgs.setdefault(c["slug"], []).append(img[key])
                continue
            path = src / "images" / key
            n += 1
            dest = out_img / f"{c['slug']}-{n}.webp"
            try:
                if not key or not path.is_file() or path.stat().st_size == 0:
                    raise FileNotFoundError("missing or empty")
                w, h = to_webp(path, dest)
            except Exception as ex:
                n -= 1
                msg = f"{c['title']}: {key or '(no file)'} ({type(ex).__name__}: {ex})"
                (skipped if args.allow_missing else problems).append(msg)
                b["type"] = "skipped"
                continue
            total += dest.stat().st_size
            img[key] = {"src": f"/assets/cases/img/{dest.name}", "w": w, "h": h}
            case_imgs.setdefault(c["slug"], []).append(img[key])
    if problems:
        sys.exit("BUILD FAILED:\n  " + "\n  ".join(problems))

    cases_dir = ROOT / "cases"
    if cases_dir.exists():
        shutil.rmtree(cases_dir)
    counts = {k: sum(1 for c in cases if c["cat"] == k) for k in CATS}

    for i, c in enumerate(cases):
        same = [x for x in cases if x["cat"] == c["cat"]]
        j = same.index(c)
        prev_c = same[j - 1] if j > 0 else None
        next_c = same[j + 1] if j + 1 < len(same) else None
        pn = ""
        if prev_c:
            pn += f'<a href="/cases/{prev_c["slug"]}/"><small>← Попередній</small>{e(prev_c["title"])}</a>'
        if next_c:
            pn += f'<a href="/cases/{next_c["slug"]}/"><small>Наступний →</small>{e(next_c["title"])}</a>'
        meta = "".join(f"<span><b>{lbl}:</b> {e(v)}</span>" for lbl, v in
                       (("Гео", c["geo"]), ("Ніша", c["niche"])) if v)
        page = (head(f'{c["title"]} — кейс UNO Agency', teaser(c) or c["title"]) + NAV +
                f'<main><section class="case-head wrap"><p class="crumbs"><a href="/cases/">Кейси</a> / '
                f'<a href="/cases/#{c["cat"]}">{CATS[c["cat"]]}</a></p><h1>{e(c["title"])}</h1>'
                f'<div class="meta"><span><b>{CATS[c["cat"]]}</b></span>{meta}</div></section>'
                f'<article class="wrap"><div class="case-body">{render_blocks(c["blocks"], img, c["title"])}</div>'
                f'<div class="case-foot"><div class="pn">{pn}</div>'
                f'<a class="pill lg" href="/redesign/#contact">Обговорити мій проєкт <span aria-hidden="true">↗</span></a>'
                f'</div></article></main>\n' + FOOT)
        d = cases_dir / c["slug"]
        d.mkdir(parents=True)
        (d / "index.html").write_text(page, encoding="utf8")

    cards = []
    for c in cases:
        cover = next((m for m in case_imgs.get(c["slug"], []) if good_cover(m)), None)
        cv = (f'<div class="cover"><img src="{cover["src"]}" width="{cover["w"]}" height="{cover["h"]}" '
              f'loading="lazy" decoding="async" alt=""/></div>') if cover else ""
        geo = f'<span>{e(c["geo"])}</span>' if c["geo"] else ""
        cards.append(
            f'<a class="card" data-cat="{c["cat"]}" href="/cases/{c["slug"]}/">{cv}<div class="card-b">'
            f'<div class="tags"><span class="c">{CATS[c["cat"]]}</span>{geo}</div>'
            f'<h2>{e(c["title"])}</h2><p>{e(teaser(c))}</p><span class="more">Дивитись кейс →</span></div></a>')
    chips = (f'<button class="chip" data-f="all" aria-pressed="true">Усі<b>{len(cases)}</b></button>' +
             "".join(f'<button class="chip" data-f="{k}" aria-pressed="false">{v}<b>{counts[k]}</b></button>'
                     for k, v in CATS.items()))
    index = (head("Кейси — UNO Agency", "Реальні кейси UNO Agency: Meta Ads, SMM і їх поєднання. Цифри, скріни, підхід.") + NAV +
             f'<main><section class="hero wrap"><p class="kick">Кейси</p>'
             f'<h1>Результати, які можна <em>перевірити</em></h1>'
             f'<p class="lead">Ми не просто «крутили рекламу» чи «вели Instagram»: занурювались у бізнес, будували стратегію, '
             f'запускали рекламу, створювали контент і приводили клієнтів. Тут — частина наших кейсів зі скрінами.</p></section>'
             f'<section class="wrap"><div class="chips" role="group" aria-label="Фільтр кейсів">{chips}</div>'
             f'<div class="grid">{"".join(cards)}</div></section></main>\n' + FOOT)
    (cases_dir / "index.html").write_text(index, encoding="utf8")

    landing = ROOT / "redesign" / "index.html"
    if landing.exists():
        s = landing.read_text(encoding="utf8")
        s2 = re.sub(r"<!--cases-count-->.*?<!--/cases-count-->", f"<!--cases-count-->{len(cases)}<!--/cases-count-->", s)
        if s2 != s:
            landing.write_text(s2, encoding="utf8")

    print(f"cases: {len(cases)} (meta {counts['meta']}, smm {counts['smm']}, both {counts['both']})")
    print(f"images: {len(img)}, total {total / 1e6:.1f} MB")
    if skipped:
        print(f"SKIPPED {len(skipped)} screenshots (re-fetch them and rebuild):")
        print("  " + "\n  ".join(skipped))


if __name__ == "__main__":
    main()
