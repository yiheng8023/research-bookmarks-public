from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_public_bookmarks  # noqa: E402


class BookmarkHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.folders = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag.lower() == "a" and attrs_dict.get("href"):
            self.links.append(attrs_dict["href"] or "")
        if tag.lower() == "h3":
            self.folders += 1


def fail(message: str) -> None:
    print(f"USER FLOW FAILED: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    output = ROOT / "exports" / "research-engineering-bookmarks-public.html"
    generated = build_public_bookmarks.build()
    if not output.is_file():
        fail("generated bookmark HTML is missing")
    existing = output.read_text(encoding="utf-8")
    if generated != existing:
        fail("generated bookmark HTML is not deterministic or not up to date")

    parser = BookmarkHTMLParser()
    parser.feed(existing)
    sources = build_public_bookmarks.load_json(ROOT / "data" / "public-sources.json")["sources"]
    if len(parser.links) != len(sources):
        fail(f"HTML link count {len(parser.links)} does not match source count {len(sources)}")
    if len(parser.links) < 100:
        fail("public projection is too thin to be useful")
    if parser.folders < 10:
        fail("public projection lacks a meaningful folder taxonomy")

    lowered = existing.lower()
    for pattern in build_public_bookmarks.FORBIDDEN_PATTERNS:
        if pattern.lower() in lowered:
            fail(f"forbidden public-safety pattern leaked: {pattern}")
    for prefix in build_public_bookmarks.LOCAL_URL_PREFIXES:
        if prefix in lowered:
            fail(f"local/private URL prefix leaked: {prefix}")
    if re.search(r"(?i)(password|secret|token|api[_-]?key|sessionid|cookie)\s*[:=]", existing):
        fail("credential-looking text leaked into exported bookmarks")

    print(f"USER FLOW OK: {len(parser.links)} public-safe links across {parser.folders} bookmark folders")


if __name__ == "__main__":
    main()

