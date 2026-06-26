from __future__ import annotations

import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "data" / "public-sources.json"
TAXONOMY_PATH = ROOT / "data" / "taxonomy.json"
HTML_PATH = ROOT / "exports" / "research-engineering-bookmarks-public.html"
REPORT_PATH = ROOT / "data" / "projection-report.json"


class BookmarkHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links = 0
        self.folders = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self.links += 1
        if tag.lower() == "h3":
            self.folders += 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_report() -> dict:
    sources_data = load_json(SOURCES_PATH)
    taxonomy_data = load_json(TAXONOMY_PATH)
    sources = sources_data["sources"]

    parser = BookmarkHTMLParser()
    parser.feed(HTML_PATH.read_text(encoding="utf-8"))

    category_counts = Counter(source["category"] for source in sources)
    source_type_counts = Counter(source["source_type"] for source in sources)

    return {
        "schema_version": 1,
        "source_baseline": {
            "name": sources_data["source"],
            "source_entries": sources_data["counts"]["source_entries"],
            "selection_policy": sources_data["selection_policy"]
        },
        "public_projection": {
            "public_sources": len(sources),
            "taxonomy_nodes": len(taxonomy_data["taxonomy"]),
            "html_export": "exports/research-engineering-bookmarks-public.html",
            "html_links": parser.links,
            "html_folders": parser.folders
        },
        "excluded_by_rule": sources_data["counts"]["excluded_by_rule"],
        "category_counts": dict(sorted(category_counts.items())),
        "source_type_counts": dict(sorted(source_type_counts.items())),
        "boundary": {
            "private_source_repository": "research-bookmarks",
            "public_projection_repository": "research-bookmarks-public",
            "resource_intelligence_repository": "resource-radar",
            "public_rule": "Only public-safe official or canonical sources are projected here."
        },
        "notes": [
            "The public projection is generated from structured data, not hand-edited HTML.",
            "The private v1.2 browser export remains private; this report exposes only public-safe aggregate counts.",
            "Folder counts are export-parser counts and may differ from private browser folder-heading counts."
        ]
    }


def main() -> None:
    REPORT_PATH.write_text(
        json.dumps(build_report(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {REPORT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
