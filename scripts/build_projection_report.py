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
    ownership_counts = Counter(source["ownership"]["status"] for source in sources)
    review_counts = Counter(source["review_status"] for source in sources)
    health_counts = Counter(source["url_health"]["status"] for source in sources)

    return {
        "schema_version": 1,
        "source_baseline": {
            "name": sources_data["source"],
            "lineage": sources_data.get("source_lineage", {}),
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
        "ownership_status_counts": dict(sorted(ownership_counts.items())),
        "review_status_counts": dict(sorted(review_counts.items())),
        "url_health_counts": dict(sorted(health_counts.items())),
        "audit": {
            "reviewed_at": sources_data["audit"]["reviewed_at"],
            "ownership_pending": ownership_counts.get("needs_review", 0),
            "removed_sourceforge": sources_data["audit"]["removed_sourceforge"],
            "removed_account_adjacent_entry": sources_data["audit"]["removed_account_adjacent_entry"],
            "canonical_url_updates": sources_data["audit"]["canonical_url_updates"],
            "new_public_candidates_admitted": sources_data["audit"]["new_public_candidates_admitted"]
        },
        "boundary": {
            "catalog_repository": "research-bookmarks-public",
            "catalog_authority": "data/public-sources.json",
            "private_candidate_source": "research-bookmarks (optional reviewed candidates only)",
            "dependency_mode": "independent; no live private sync or external control plane required",
            "public_rule": "Only reviewed public-safe sources with an explicit admission basis are projected here; official and secondary source types remain distinct."
        },
        "notes": [
            "The public projection is generated from structured data, not hand-edited HTML.",
            "The private baseline and later private overlays remain private; this report exposes only public-safe aggregate counts.",
            "This repository is not a live mirror of the current private bookmark overlay.",
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
