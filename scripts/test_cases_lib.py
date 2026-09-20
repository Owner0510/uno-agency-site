import unittest

from cases_lib import category, clean_title, render_blocks, select_cases, slugify, teaser


def row(title, tags="Facebook ADS", n=1, **kw):
    blocks = [{"type": "paragraph", "id": str(i), "text": "x" * 50} for i in range(n)]
    return {"title": title, "tags": tags, "geo": "", "niche": "", "desc": "", "blocks": blocks, **kw}


class Titles(unittest.TestCase):
    def test_clean_title(self):
        self.assertEqual(clean_title(" 𝗧𝗔𝗧𝗧𝗢𝗢 𝗔𝗥𝗧𝗜𝗦𝗧 "), "TATTOO ARTIST")
        self.assertEqual(clean_title("Lilico - **Бухгалтерські**"), "Lilico - Бухгалтерські")

    def test_slugify_is_ascii(self):
        s = slugify("Школа танців Dance Cult Studio")
        self.assertEqual(s, "shkola-tanciv-dance-cult-studio")
        self.assertTrue(s.isascii() and not s.startswith("-") and not s.endswith("-"))
        self.assertEqual(slugify("Дитячі велосипеди  Biky | Магазин"), "dytyachi-velosypedy-biky-mahazyn")


class Categories(unittest.TestCase):
    def test_category(self):
        self.assertEqual(category("Facebook ADS"), "meta")
        self.assertEqual(category("Google ADS"), "smm")
        self.assertEqual(category("Facebook ADS, SMM Instagram"), "both")
        self.assertEqual(category(""), "")


class Selection(unittest.TestCase):
    def test_drops_unfinished(self):
        out = select_cases([row("(НЕ ЗАВЕРШЕНО) X"), row("(НЕ ЗАВЕРШЕНО)Y"), row("Good")])
        self.assertEqual([c["title"] for c in out], ["Good"])

    def test_cool_cat_keeps_fuller(self):
        out = select_cases([row("Cool Cat Fence", n=2), row("Cool Cat Fence (встановлення парканів)", n=5)])
        self.assertEqual([c["title"] for c in out], ["Cool Cat Fence (встановлення парканів)"])

    def test_golf_keeps_one_and_inherits_tag(self):
        golf = "Всеукраїнська федерація гольфу"
        out = select_cases([row(golf, tags="", n=6), row(golf, tags="Google ADS", n=5)])
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["cat"], "smm")
        self.assertEqual(len(out[0]["blocks"]), 6)

    def test_unique_slugs(self):
        out = select_cases([row("A"), row("A"), row("B")])
        self.assertEqual([c["slug"] for c in out], ["a", "a-2", "b"])


class Teaser(unittest.TestCase):
    def test_uses_desc(self):
        c = {"desc": r"Отримали **637** заявок з бюджету \$3,328", "blocks": []}
        self.assertEqual(teaser(c), "Отримали 637 заявок з бюджету $3,328")

    def test_falls_back_to_first_long_paragraph(self):
        short = {"type": "paragraph", "text": "коротко"}
        long_ = {"type": "paragraph", "text": "Слово " * 60}
        t = teaser({"desc": "", "blocks": [short, long_]})
        self.assertTrue(t.endswith("…"))
        self.assertLessEqual(len(t), 161)


IMG = {"a.png": {"src": "/assets/cases/img/a.webp", "w": 800, "h": 600}}


class Render(unittest.TestCase):
    def test_heading_and_escape(self):
        h = render_blocks([{"type": "heading_2", "text": "Про <b>бізнес</b>"}], IMG, "T")
        self.assertIn("<h2>Про &lt;b&gt;бізнес&lt;/b&gt;</h2>", h)

    def test_lists_are_grouped(self):
        b = [{"type": "bulleted_list_item", "text": "one"}, {"type": "bulleted_list_item", "text": "two"}]
        h = render_blocks(b, IMG, "T")
        self.assertEqual(h.count("<ul>"), 1)
        self.assertEqual(h.count("<li>"), 2)

    def test_callout_and_columns(self):
        h = render_blocks([{"type": "callout", "icon": "✔️", "text": "hi"}], IMG, "T")
        self.assertIn('<aside class="callout">', h)
        cols = {"type": "column_list", "children": [
            {"type": "column", "children": [{"type": "paragraph", "text": "l"}]},
            {"type": "column", "children": [{"type": "paragraph", "text": "r"}]}]}
        h = render_blocks([cols], IMG, "T")
        self.assertIn('<div class="cols">', h)
        self.assertEqual(h.count('<div class="col">'), 2)

    def test_image(self):
        b = [{"type": "image", "image_local": "/x/y/a.png"}]
        h = render_blocks(b, IMG, "Кейс")
        for part in ('src="/assets/cases/img/a.webp"', 'loading="lazy"', 'width="800"', 'height="600"', 'alt="Кейс'):
            self.assertIn(part, h)

    def test_missing_image_raises(self):
        with self.assertRaises(KeyError):
            render_blocks([{"type": "image", "image_local": "/x/missing.png"}], IMG, "T")

    def test_video_and_empty_paragraph_skipped(self):
        self.assertEqual(render_blocks([{"type": "video", "video_url": ""}, {"type": "paragraph", "text": ""}], IMG, "T").strip(), "")


if __name__ == "__main__":
    unittest.main()
