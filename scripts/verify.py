from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "README.zh-CN.md",
    "NOTICE",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".github/FUNDING.yml",
    ".github/workflows/validate.yml",
    "data/taxonomy.json",
    "data/official-sources.example.json",
    "docs/license-policy.md",
    "docs/public-private-boundary.md",
    "docs/private-public-sync-model.md",
    "docs/source-policy.md",
    "exports/README.md",
]

FORBIDDEN_SUFFIXES = {".html", ".htm", ".jsonl", ".sqlite", ".db"}


def fail(message: str) -> None:
    raise SystemExit(f"verify failed: {message}")


def require_file(path: str) -> None:
    candidate = ROOT / path
    if not candidate.is_file():
        fail(f"missing required file: {path}")


def verify_required_files() -> None:
    for path in REQUIRED_FILES:
        require_file(path)


def load_json(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def verify_taxonomy() -> None:
    data = load_json("data/taxonomy.json")
    if data.get("schema_version") != 1:
        fail("taxonomy schema_version must be 1")
    seen = set()
    for item in data.get("taxonomy", []):
        for key in ("id", "label", "description"):
            if not item.get(key):
                fail(f"taxonomy item missing {key}")
        if item["id"] in seen:
            fail(f"duplicate taxonomy id: {item['id']}")
        seen.add(item["id"])


def verify_sources() -> None:
    categories = {item["id"] for item in load_json("data/taxonomy.json")["taxonomy"]}
    data = load_json("data/official-sources.example.json")
    if data.get("schema_version") != 1:
        fail("official sources schema_version must be 1")
    seen = set()
    for source in data.get("sources", []):
        for key in ("id", "title", "url", "category", "source_type", "official"):
            if key not in source:
                fail(f"source missing {key}")
        if source["id"] in seen:
            fail(f"duplicate source id: {source['id']}")
        seen.add(source["id"])
        if source["category"] not in categories:
            fail(f"unknown source category: {source['category']}")
        parsed = urlparse(source["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"source URL must be https: {source['id']}")
        if source["official"] is not True:
            fail(f"public example source must be official=true: {source['id']}")


def verify_no_raw_browser_exports() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            rel = path.relative_to(ROOT).as_posix()
            fail(f"raw/private export-like file is not allowed in public repo: {rel}")


def verify_language_links() -> None:
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if "English | [简体中文](README.zh-CN.md)" not in english:
        fail("README.md language switch is missing or inconsistent")
    if "[English](README.md) | 简体中文" not in chinese:
        fail("README.zh-CN.md language switch is missing or inconsistent")


def main() -> None:
    verify_required_files()
    verify_taxonomy()
    verify_sources()
    verify_no_raw_browser_exports()
    verify_language_links()
    print("research-bookmarks-public verification passed")


if __name__ == "__main__":
    main()
