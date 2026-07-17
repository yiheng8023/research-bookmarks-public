from __future__ import annotations

import hashlib
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
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SPONSORING.md",
    "SPONSORING.zh-CN.md",
    "SUPPORT.md",
    "SUPPORT.zh-CN.md",
    "docs/assets/sponsoring/wechat-pay.png",
    "docs/assets/sponsoring/alipay.png",
    ".github/CODEOWNERS",
    ".github/FUNDING.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/source.yml",
    ".github/ISSUE_TEMPLATE/taxonomy.yml",
    ".github/labels.yml",
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
    "docs/catalog-audit-2026-07-17.md",
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
ALLOWED_SOURCE_TYPES = {
    "official_product_site", "official_documentation", "canonical_repository",
    "primary_institutional_source", "standards_body", "public_knowledge_resource",
    "community_reference", "secondary_reference",
}
OFFICIAL_SOURCE_TYPES = {
    "official_product_site", "official_documentation", "canonical_repository",
    "primary_institutional_source", "standards_body",
}

SPONSORING_ASSETS = {
    "docs/assets/sponsoring/wechat-pay.png": "D8C213F1539CAD6C9FD23099736AECD06C722129AF24F77FE9F26563BBB9A05E",
    "docs/assets/sponsoring/alipay.png": "491EE27D52797818F1CCA756560BC239CF6150FE3327B0FD31728F7CE53327CD",
}
PAYPAL_URL = "https://www.paypal.com/ncp/payment/LNTF8KXGJXMZY"


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
    if data.get("schema_version") != 2:
        fail("public sources schema_version must be 2")
    seen = set()
    seen_urls = set()
    sources = data.get("sources", [])
    if len(sources) < 100:
        fail("public sources catalog is too thin to be useful")
    for source in data.get("sources", []):
        for key in (
            "id", "title", "url", "canonical_url", "canonical_host", "category", "subdomain",
            "product", "entry_role", "market_scope", "ownership", "review_status",
            "source_type", "admission_basis", "public_safe", "official_or_canonical",
            "last_checked_at", "url_health", "evidence_links",
        ):
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
        if source["canonical_url"] != source["url"] or source["canonical_host"] != parsed.netloc.lower():
            fail(f"canonical URL/host mismatch: {source['id']}")
        if source["source_type"] not in ALLOWED_SOURCE_TYPES:
            fail(f"invalid source_type: {source['id']}")
        if source["official_or_canonical"] is not (source["source_type"] in OFFICIAL_SOURCE_TYPES):
            fail(f"official_or_canonical conflicts with source_type: {source['id']}")
        ownership = source["ownership"]
        if ownership.get("status") not in {"needs_review", "brand_verified", "legal_entity_verified"}:
            fail(f"invalid ownership status: {source['id']}")
        if ownership.get("status") != "needs_review" and not ownership.get("evidence_links"):
            fail(f"verified ownership lacks evidence: {source['id']}")
        if source["url_health"].get("status") not in {"reachable", "automation_limited", "needs_follow_up", "not_checked"}:
            fail(f"invalid URL health status: {source['id']}")
        if source["category"] == "00_workspace_common_entrypoints":
            fail(f"workspace is a private projection view, not public resource ownership: {source['id']}")
        if any(token in source["title"] for token in ["中国站", "国际站", "国内入口", "国际入口", "海外"]):
            fail(f"region label must be modeled as market_scope, not title text: {source['id']}")
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
    if report["boundary"]["catalog_repository"] != "research-bookmarks-public":
        fail("projection report catalog repository boundary is wrong")
    if report["boundary"]["catalog_authority"] != "data/public-sources.json":
        fail("projection report catalog authority is wrong")
    if not report["boundary"]["dependency_mode"].startswith("independent"):
        fail("projection report must declare independent dependency mode")
    if report["audit"]["ownership_pending"] != sum(
        source["ownership"]["status"] == "needs_review" for source in sources_data["sources"]
    ):
        fail("projection report ownership-pending count is wrong")
    for category in [
        "09_philosophy_language_literature_humanities",
        "11_art_design_architecture_media_culture",
        "14_governance_institutions_public_policy",
    ]:
        if report["category_counts"].get(category, 0) == 0:
            fail(f"corrected taxonomy category is empty: {category}")


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


def verify_sponsoring_surface() -> None:
    readmes = {
        "README.md": (ROOT / "README.md").read_text(encoding="utf-8"),
        "README.zh-CN.md": (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
    }
    for rel, expected_hash in SPONSORING_ASSETS.items():
        actual_hash = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest().upper()
        if actual_hash != expected_hash:
            fail(f"sponsoring asset hash mismatch: {rel}")
        for readme, text in readmes.items():
            if rel not in text:
                fail(f"sponsoring asset is not rendered by {readme}: {rel}")

    for rel in ["README.md", "README.zh-CN.md", "SPONSORING.md", "SPONSORING.zh-CN.md"]:
        if PAYPAL_URL not in (ROOT / rel).read_text(encoding="utf-8"):
            fail(f"reviewed PayPal channel is missing from {rel}")


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
    for phrase in ["research-bookmarks", "independent", "public-safe", "private"]:
        if phrase not in combined:
            fail(f"relationship docs missing required phrase: {phrase}")
    for phrase in [
        "Repository Role",
        "public catalogue truth",
        "仓库职责",
        "公开目录真值",
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
    verify_sponsoring_surface()
    verify_relationship_docs()
    print("research-bookmarks-public verification passed")


if __name__ == "__main__":
    main()
