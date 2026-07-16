# research-bookmarks-public

English | [简体中文](README.zh-CN.md)

Independent public-safe resource catalogue and browser-bookmark artifact.

## Repository Role

This repository owns its structured public sources, public taxonomy,
declassification policy, deterministic exporter, aggregate evidence, and
browser-importable artifact. It does not require a central hub, private
checkout, or external discovery service to build, verify, or publish its
current catalogue.

## Source Model

```text
data/public-sources.json                  public catalogue truth
data/taxonomy.json                        public taxonomy truth
          |
          v
scripts/build_public_bookmarks.py
scripts/build_projection_report.py
          |
          v
exports/research-engineering-bookmarks-public.html
data/projection-report.json               derived evidence
```

The current 328-source catalogue has historical lineage from a reviewed
private 389-entry snapshot dated 2026-06-26. That lineage does not create a
live dependency or synchronization contract. Later private records are absent
until individually reviewed and admitted here.

## Private Input Boundary

`research-bookmarks` independently owns private bookmark truth. It may propose
explicitly reviewed public-safe candidates. This repository performs its own
admission and verification; it never mirrors raw private data and never
inherits private source authority by path.

## What This Repository Provides

- `data/public-sources.json`: reviewed official or canonical public sources.
- `data/taxonomy.json`: broad public resource taxonomy.
- `exports/research-engineering-bookmarks-public.html`: deterministic Netscape
  bookmark artifact.
- `data/projection-report.json`: derived aggregate and boundary evidence.
- local verification and user-flow simulation.

## Verification

Regenerate:

```bash
python -B scripts/build_public_bookmarks.py
python -B scripts/build_projection_report.py
```

Verify:

```bash
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```

All correctness checks are local. GitHub Actions may repeat them as a
convenience, but it is not repository truth or a required runtime dependency.

## Safety Boundary

Public output must contain only reviewed public-safe official or canonical
sources. Raw browser exports, private folder structure, local URLs, account or
session data, personal preferences, low-trust fallbacks, and credential-like
content are prohibited.
