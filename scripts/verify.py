from __future__ import annotations

import json
import importlib.util
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
    "data/public-sources.json",
    "data/projection-report.json",
    "docs/license-policy.md",
    "docs/public-private-boundary.md",
    "docs/private-public-sync-model.md",
    "docs/design-basis.md",
    "docs/projection-closeout.md",
    "docs/automation-validation.md",
    "docs/source-policy.md",
    "exports/README.md",
    "exports/research-engineering-bookmarks-public.html",
    "scripts/build_public_bookmarks.py",
    "scripts/build_projection_report.py",
    "scripts/simulate_user_flow.py",
]

ALLOWED_HTML_EXPORTS = {"exports/research-engineering-bookmarks-public.html"}
FORBIDDEN_SUFFIXES = {".htm", ".jsonl", ".sqlite", ".db"}
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
LOCAL_URL_PREFIXES = ("http://127.", "http://localhost", "http://192.168.", "https://127.", "https://localhost", "https://192.168.")


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
        for key in ("id", "label", "zh_label", "description"):
            if not item.get(key):
                fail(f"taxonomy item missing {key}")
        if item["id"] in seen:
            fail(f"duplicate taxonomy id: {item['id']}")
        seen.add(item["id"])
    if len(seen) < 10:
        fail("taxonomy is too thin for the public bookmark catalog")


def verify_sources() -> None:
    categories = {item["id"] for item in load_json("data/taxonomy.json")["taxonomy"]}
    data = load_json("data/public-sources.json")
    if data.get("schema_version") != 1:
        fail("public sources schema_version must be 1")
    seen = set()
    seen_urls = set()
    sources = data.get("sources", [])
    if len(sources) < 100:
        fail("public sources catalog is too thin to be useful")
    for source in data.get("sources", []):
        for key in ("id", "title", "url", "category", "source_type", "public_safe", "official_or_canonical"):
            if key not in source:
                fail(f"source missing {key}")
        if source["id"] in seen:
            fail(f"duplicate source id: {source['id']}")
        seen.add(source["id"])
        if source["url"] in seen_urls:
            fail(f"duplicate source url: {source['url']}")
        seen_urls.add(source["url"])
        if source["category"] not in categories:
            fail(f"unknown source category: {source['category']}")
        parsed = urlparse(source["url"])
        if parsed.scheme != "https" or not parsed.netloc:
            fail(f"source URL must be https: {source['id']}")
        if source["public_safe"] is not True:
            fail(f"public source must be public_safe=true: {source['id']}")
        if source["official_or_canonical"] is not True:
            fail(f"public source must be official_or_canonical=true: {source['id']}")
        blob = " ".join(str(source.get(key, "")) for key in ("id", "title", "url", "source_type")).lower()
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.lower() in blob:
                fail(f"forbidden pattern leaked into public source {source['id']}: {pattern}")


def verify_projection_report() -> None:
    sources_data = load_json("data/public-sources.json")
    report = load_json("data/projection-report.json")
    if report.get("schema_version") != 1:
        fail("projection report schema_version must be 1")
    public_sources = len(sources_data["sources"])
    if report["source_baseline"]["source_entries"] != sources_data["counts"]["source_entries"]:
        fail("projection report source entry count does not match public-sources.json")
    if report["public_projection"]["public_sources"] != public_sources:
        fail("projection report public source count does not match public-sources.json")
    if report["public_projection"]["html_links"] != public_sources:
        fail("projection report HTML link count does not match public source count")
    if report["boundary"]["private_source_repository"] != "research-bookmarks":
        fail("projection report private source boundary is wrong")
    if report["boundary"]["resource_intelligence_repository"] != "resource-radar":
        fail("projection report resource intelligence boundary is wrong")


def verify_no_raw_browser_exports() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() == ".html" and rel not in ALLOWED_HTML_EXPORTS:
            fail(f"raw/private html export is not allowed in public repo: {rel}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"raw/private export-like file is not allowed in public repo: {rel}")


def load_builder():
    spec = importlib.util.spec_from_file_location("build_public_bookmarks", ROOT / "scripts" / "build_public_bookmarks.py")
    if spec is None or spec.loader is None:
        fail("cannot load scripts/build_public_bookmarks.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_generated_bookmarks() -> None:
    builder = load_builder()
    rendered = builder.build()
    output = (ROOT / "exports" / "research-engineering-bookmarks-public.html").read_text(encoding="utf-8")
    if rendered != output:
        fail("public bookmark HTML is not up to date; run scripts/build_public_bookmarks.py")
    lowered = output.lower()
    for pattern in FORBIDDEN_PATTERNS:
        if pattern.lower() in lowered:
            fail(f"forbidden pattern leaked into public HTML: {pattern}")
    for prefix in LOCAL_URL_PREFIXES:
        if prefix in lowered:
            fail(f"local/private URL leaked into public HTML: {prefix}")
    link_count = output.count("<DT><A ")
    source_count = len(load_json("data/public-sources.json")["sources"])
    if link_count != source_count:
        fail(f"HTML link count {link_count} does not match source count {source_count}")
    if link_count < 100:
        fail("public bookmark HTML is too thin to be useful")


def verify_language_links() -> None:
    english = (ROOT / "README.md").read_text(encoding="utf-8")
    chinese = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    if "English | [简体中文](README.zh-CN.md)" not in english:
        fail("README.md language switch is missing or inconsistent")
    if "[English](README.md) | 简体中文" not in chinese:
        fail("README.zh-CN.md language switch is missing or inconsistent")


def verify_relationship_docs() -> None:
    combined = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in [
            "README.md",
            "README.zh-CN.md",
            "docs/private-public-sync-model.md",
            "docs/public-private-boundary.md",
            "docs/design-basis.md",
            "docs/automation-validation.md",
        ]
    )
    for phrase in ["research-bookmarks", "resource-radar", "public-safe", "private"]:
        if phrase not in combined:
            fail(f"relationship docs missing required phrase: {phrase}")
    for phrase in [
        "System context",
        "open-resource-governance/docs/system-topology.md",
        "public bookmark-output lane",
        "系统位置",
        "公开书签产出 lane",
    ]:
        if phrase not in combined:
            fail(f"relationship docs missing system-context phrase: {phrase}")
    stale_phrases = [
        "may remain private while it is staged",
        "可以暂时保持 private",
    ]
    for phrase in stale_phrases:
        if phrase in combined:
            fail(f"stale public-visibility phrase remains: {phrase}")


def main() -> None:
    verify_required_files()
    verify_taxonomy()
    verify_sources()
    verify_projection_report()
    verify_no_raw_browser_exports()
    verify_generated_bookmarks()
    verify_language_links()
    verify_relationship_docs()
    print("research-bookmarks-public verification passed")


if __name__ == "__main__":
    main()
