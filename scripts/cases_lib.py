"""Pure logic for the cases pages: selecting, slugging, categorising and rendering Notion blocks."""
import html
import json
import re
import unicodedata

UK = {
    "а": "a", "б": "b", "в": "v", "г": "h", "ґ": "g", "д": "d", "е": "e", "є": "ye", "ж": "zh", "з": "z",
    "и": "y", "і": "i", "ї": "yi", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o", "п": "p",
    "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "c", "ч": "ch", "ш": "sh", "щ": "shch",
    "ь": "", "ю": "yu", "я": "ya", "ъ": "", "ы": "y", "э": "e", "ё": "yo",
}

# Titles that appear twice in Notion; the fuller page wins.
DUPLICATE_GROUPS = [
    {"Cool Cat Fence", "Cool Cat Fence (встановлення парканів)"},
    {"Всеукраїнська федерація гольфу"},
]


def clean_title(t):
    t = unicodedata.normalize("NFKC", t).replace("*", "")
    return re.sub(r"\s+", " ", t).strip()


def slugify(t):
    out = "".join(UK.get(ch, ch) for ch in clean_title(t).lower())
    out = re.sub(r"[^a-z0-9]+", "-", out)
    return out.strip("-")


def category(tags):
    fb = "facebook" in tags.lower()
    smm = "smm" in tags.lower()
    google = "google" in tags.lower()
    if fb and smm:
        return "both"
    if fb:
        return "meta"
    if google or smm:
        return "smm"
    return ""


def _size(row):
    return len(json.dumps(row["blocks"], ensure_ascii=False))


def select_cases(raw):
    rows = []
    for r in raw:
        title = clean_title(r["title"])
        if title.startswith("(НЕ ЗАВЕРШЕНО)"):
            continue
        rows.append({**r, "title": title})

    keep = []
    for group in DUPLICATE_GROUPS:
        members = [r for r in rows if r["title"] in group]
        if len(members) > 1:
            best = max(members, key=_size)
            if not best["tags"]:
                best["tags"] = next((m["tags"] for m in members if m["tags"]), "")
            keep.append(best)
    dropped = {id(r) for g in DUPLICATE_GROUPS for r in rows if r["title"] in g}
    keep_ids = {id(r) for r in keep}
    final = [r for r in rows if id(r) not in dropped or id(r) in keep_ids]

    seen, out = {}, []
    for r in final:
        base = slugify(r["title"]) or "case"
        seen[base] = seen.get(base, 0) + 1
        slug = base if seen[base] == 1 else f"{base}-{seen[base]}"
        out.append({
            "title": r["title"], "slug": slug, "cat": category(r["tags"]), "geo": r.get("geo", ""),
            "niche": r.get("niche", ""), "desc": r.get("desc", ""), "blocks": r["blocks"],
        })
    return out


def teaser(case):
    d = case.get("desc", "").replace("**", "").replace("\\$", "$").strip()
    if d:
        return d
    for b in case["blocks"]:
        t = b.get("text", "").strip()
        if b["type"] == "paragraph" and len(t) >= 40:
            return t if len(t) <= 160 else t[:160].rsplit(" ", 1)[0] + "…"
    return ""


def _e(s):
    return html.escape(s or "", quote=True)


def render_blocks(blocks, img, title):
    out, i = [], 0
    while i < len(blocks):
        b = blocks[i]
        t = b["type"]
        if t in ("bulleted_list_item", "numbered_list_item"):
            tag = "ul" if t == "bulleted_list_item" else "ol"
            items = []
            while i < len(blocks) and blocks[i]["type"] == t:
                kids = render_blocks(blocks[i].get("children", []), img, title)
                items.append(f"<li>{_e(blocks[i].get('text'))}{kids}</li>")
                i += 1
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        if t in ("heading_1", "heading_2", "heading_3"):
            level = {"heading_1": 2, "heading_2": 2, "heading_3": 3}[t]
            out.append(f"<h{level}>{_e(b.get('text'))}</h{level}>")
        elif t == "paragraph":
            if b.get("text", "").strip():
                out.append(f"<p>{_e(b['text'])}</p>")
        elif t == "callout":
            icon = _e(b.get("icon"))
            kids = render_blocks(b.get("children", []), img, title)
            out.append(f'<aside class="callout"><span class="ico" aria-hidden="true">{icon}</span>'
                       f'<div><p>{_e(b.get("text"))}</p>{kids}</div></aside>')
        elif t == "quote":
            out.append(f"<blockquote>{_e(b.get('text'))}</blockquote>")
        elif t == "divider":
            out.append("<hr/>")
        elif t == "image":
            key = b["image_local"].rsplit("/", 1)[-1]
            m = img[key]
            out.append(f'<img src="{m["src"]}" width="{m["w"]}" height="{m["h"]}" loading="lazy" '
                       f'decoding="async" alt="{_e(title)} — скрін результатів"/>')
        elif t == "column_list":
            cols = "".join(
                f'<div class="col">{render_blocks(c.get("children", []), img, title)}</div>'
                for c in b.get("children", []) if c["type"] == "column")
            out.append(f'<div class="cols">{cols}</div>')
        # video and unknown blocks: skipped (video links are empty in the export)
        i += 1
    return "".join(out)
