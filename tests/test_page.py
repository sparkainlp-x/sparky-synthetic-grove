"""Static checks for the standalone page (standard library only)."""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
SITE_FILES = ("index.html", "sparky-beaver.webp")
MAX_IMAGE_BYTES = 500_000
BANNED = re.compile(
    r"\b(proven|validated|production[- ]ready|quantum advantage|real[- ]world performance|"
    r"medical|clinical|diagnos\w*|therap\w*|conscious\w*|qubits?|QPU|QEC|free[- ]energy|overunity|investors?)\b",
    re.IGNORECASE,
)
# Emoji and pictographic or decorative symbol blocks that the page must not use.
SYMBOLS = re.compile("[\u2190-\u21ff\u2300-\u23ff\u25a0-\u27bf\u2b00-\u2bff\U0001f000-\U0001faff\ufe0f]")


class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str | None]]] = []
        self.scripts: list[str] = []
        self.text: list[str] = []
        self._in_script = False
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        self._in_script = tag == "script"
        self._in_style = tag == "style"

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._in_script = self._in_style = False

    def handle_data(self, data):
        if self._in_script:
            self.scripts.append(data)
        elif not self._in_style:
            self.text.append(data)


class PageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.doc = _Collector()
        cls.doc.feed(cls.html)

    def attrs(self, tag: str) -> list[dict[str, str | None]]:
        return [a for t, a in self.doc.tags if t == tag]

    def test_site_files_exist_and_image_is_small(self) -> None:
        for name in SITE_FILES:
            self.assertTrue((ROOT / name).is_file(), name)
        self.assertLess((ROOT / "sparky-beaver.webp").stat().st_size, MAX_IMAGE_BYTES)
        self.assertEqual((ROOT / "sparky-beaver.webp").read_bytes()[8:12], b"WEBP")

    def test_language_and_images_are_described(self) -> None:
        self.assertEqual(self.attrs("html")[0].get("lang"), "en")
        images = self.attrs("img")
        self.assertTrue(images)
        for img in images:
            self.assertTrue((img.get("alt") or "").strip(), img)
            self.assertIn(img["src"], SITE_FILES)
        for canvas in self.attrs("canvas"):
            self.assertEqual(canvas.get("role"), "img")
            self.assertTrue(canvas.get("aria-label"))

    def test_controls_are_keyboard_reachable_and_labelled(self) -> None:
        labels = {a.get("for") for a in self.attrs("label")}
        for inp in self.attrs("input"):
            self.assertIn(inp.get("id"), labels)
        for button in self.attrs("button"):
            self.assertEqual(button.get("type"), "button")
            self.assertNotIn("tabindex", button)
        self.assertIn(":focus-visible", self.html)
        self.assertTrue(any(a.get("class") == "skip" for a in self.attrs("a")))

    def test_reduced_motion_is_respected(self) -> None:
        self.assertIn("@media (prefers-reduced-motion: reduce)", self.html)
        self.assertIn("matchMedia('(prefers-reduced-motion: reduce)')", self.html)
        self.assertIn("let paused = reduceMotion.matches;", self.html)

    def test_no_external_requests_or_trackers(self) -> None:
        for tag, attrs in self.doc.tags:
            for key in ("src", "srcset", "data", "poster"):
                value = attrs.get(key) or ""
                self.assertNotRegex(value, r"^(https?:)?//", (tag, key))
            if tag == "link":
                self.fail(f"unexpected <link>: {attrs}")
            if tag == "script":
                self.assertNotIn("src", attrs)
        for attrs in self.attrs("a"):
            href = attrs.get("href") or ""
            if href.startswith("http"):
                self.assertTrue(href.startswith("https://github.com/sparkainlp-x/"), href)
        self.assertIn("Content-Security-Policy", self.html)
        self.assertNotRegex(self.html, r"\b(fetch|XMLHttpRequest|WebSocket|sendBeacon|navigator\.connection)\b")

    def test_no_emoji_badges_or_banned_claims(self) -> None:
        self.assertIsNone(SYMBOLS.search(self.html), "decorative symbol or emoji found")
        text = " ".join(self.doc.text)
        self.assertIsNone(BANNED.search(text), BANNED.search(text))
        self.assertIn("synthetic", text.lower())
        self.assertIn("Jean-François Brisson, Spark AI NLP", text)

    @unittest.skipUnless(shutil.which("node"), "node is not installed")
    def test_inline_script_parses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.js"
            path.write_text("\n".join(self.doc.scripts), encoding="utf-8")
            result = subprocess.run(["node", "--check", str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
