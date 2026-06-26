from __future__ import annotations

import argparse
import html
import json
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TAXONOMY = ROOT / "data" / "taxonomy.json"
DEFAULT_SOURCES = ROOT / "data" / "public-sources.json"
DEFAULT_OUTPUT = ROOT / "exports" / "research-engineering-bookmarks-public.html"

FORBIDDEN_PATTERNS = [
    "baidu",
    "百度",
    "文心",
    "ernie",
    "pan.baidu",
    "kms",
    "破解",
    "盗版",
    "茶杯狐",
    "freeok",
    "423down",
    "grizzly",
    "crxsoso",
    "ruancang",
    "musicfree",
    "office tool plus",
    "autodesk8",
    "30aitool",
    "msdn 我告诉你",
    "逆向",
]

LOCAL_URL_PREFIXES = (
    "http://127.",
    "http://localhost",
    "http://192.168.",
    "https://127.",
    "https://localhost",
    "https://192.168.",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def taxonomy_map(taxonomy: dict) -> dict[str, dict]:
    seen: set[str] = set()
    mapped: dict[str, dict] = {}
    for item in taxonomy.get("taxonomy", []):
        item_id = item.get("id")
        if not item_id:
            raise ValueError("taxonomy item missing id")
        if item_id in seen:
            raise ValueError(f"duplicate taxonomy id: {item_id}")
        seen.add(item_id)
        mapped[item_id] = item
    return mapped


def validate_source(source: dict, categories: dict[str, dict]) -> None:
    for key in ("id", "title", "url", "category", "source_type", "public_safe", "official_or_canonical"):
        if key not in source:
            raise ValueError(f"source missing {key}: {source!r}")
    if source["category"] not in categories:
        raise ValueError(f"unknown category for {source['id']}: {source['category']}")
    parsed = urlparse(source["url"])
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(f"public bookmark URL must be https: {source['id']}")
    if source["url"].lower().startswith(LOCAL_URL_PREFIXES):
        raise ValueError(f"local/private URL leaked: {source['id']}")
    if source["public_safe"] is not True:
        raise ValueError(f"source must be public_safe=true: {source['id']}")
    if source["official_or_canonical"] is not True:
        raise ValueError(f"source must be official_or_canonical=true: {source['id']}")
    blob = " ".join(str(source.get(key, "")) for key in ("id", "title", "url", "source_type")).lower()
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.lower() in blob:
            raise ValueError(f"forbidden pattern leaked into public source {source['id']}: {pattern}")


def validate_sources(data: dict, taxonomy: dict) -> list[dict]:
    if data.get("schema_version") != 1:
        raise ValueError("public sources schema_version must be 1")
    categories = taxonomy_map(taxonomy)
    seen_ids: set[str] = set()
    seen_urls: set[str] = set()
    sources = data.get("sources", [])
    if len(sources) < 100:
        raise ValueError("public bookmark projection should contain at least 100 sources")
    for source in sources:
        validate_source(source, categories)
        if source["id"] in seen_ids:
            raise ValueError(f"duplicate source id: {source['id']}")
        if source["url"] in seen_urls:
            raise ValueError(f"duplicate source URL: {source['url']}")
        seen_ids.add(source["id"])
        seen_urls.add(source["url"])
    return sources


def render_bookmarks(taxonomy: dict, sources: list[dict]) -> str:
    categories = taxonomy_map(taxonomy)
    by_category: dict[str, list[dict]] = defaultdict(list)
    for source in sources:
        by_category[source["category"]].append(source)

    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        "<!-- Public-safe generated bookmark projection. Edit data/public-sources.json, then run scripts/build_public_bookmarks.py. -->",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>Research and Engineering Public Sources</TITLE>",
        "<H1>Research and Engineering Public Sources</H1>",
        "<DL><p>",
        "    <DT><H3>Research and Engineering Public Sources</H3>",
        "    <DL><p>",
    ]

    ordered = sorted(categories.values(), key=lambda item: (item.get("order", 999), item["id"]))
    for category in ordered:
        bucket = sorted(by_category.get(category["id"], []), key=lambda item: (item["source_type"], item["title"], item["url"]))
        if not bucket:
            continue
        label = category.get("zh_label") or category.get("label") or category["id"]
        lines.append(f"        <DT><H3>{html.escape(label)}</H3>")
        lines.append("        <DL><p>")
        by_type: dict[str, list[dict]] = defaultdict(list)
        for source in bucket:
            by_type[source["source_type"]].append(source)
        for source_type in sorted(by_type):
            lines.append(f"            <DT><H3>{html.escape(source_type)}</H3>")
            lines.append("            <DL><p>")
            for source in by_type[source_type]:
                title = html.escape(source["title"])
                url = html.escape(source["url"], quote=True)
                lines.append(f'                <DT><A HREF="{url}">{title}</A>')
            lines.append("            </DL><p>")
        lines.append("        </DL><p>")
    lines.extend(["    </DL><p>", "</DL><p>", ""])
    return "\n".join(lines)


def build(taxonomy_path: Path = DEFAULT_TAXONOMY, sources_path: Path = DEFAULT_SOURCES) -> str:
    taxonomy = load_json(taxonomy_path)
    sources_data = load_json(sources_path)
    sources = validate_sources(sources_data, taxonomy)
    return render_bookmarks(taxonomy, sources)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--taxonomy", type=Path, default=DEFAULT_TAXONOMY)
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Fail if the generated HTML is not up to date.")
    args = parser.parse_args(argv)

    rendered = build(args.taxonomy, args.sources)
    if args.check:
        existing = args.output.read_text(encoding="utf-8") if args.output.exists() else None
        if existing != rendered:
            print(f"bookmark export is not up to date: {args.output}", file=sys.stderr)
            return 1
        print("public bookmark export is up to date")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"wrote {args.output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

