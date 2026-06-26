# Bookmark Projection Closeout

This repository is not a hand-maintained bookmark dump. It is the public-safe
projection of a private bookmark baseline.

## Source baseline

The current projection is based on the private source file:

```text
research_engineering_bookmarks_2026-06-26_v1.2_final.html
```

The private source repository records:

- 389 private bookmark entries;
- 95 private browser folders;
- the v1.2 final audit;
- private import and declassification evidence.

Those private files are intentionally not copied into this public repository.

## Public projection

This repository publishes:

- `data/taxonomy.json` — public-safe top-level resource taxonomy;
- `data/public-sources.json` — filtered official/canonical public sources;
- `data/projection-report.json` — aggregate projection evidence;
- `exports/research-engineering-bookmarks-public.html` — generated browser-importable HTML.

Current public projection:

```text
389 private entries
-> 328 public-safe sources
-> generated browser-importable HTML
-> verification + user-flow simulation
```

## What was implemented from review

- HTML is an output artifact, not the long-term source of truth.
- Structured public source records are the public source of truth.
- Low-trust, local-only, private-overlay, and hard-excluded resources stay out
  of the public projection.
- The taxonomy is aligned with the resource-radar universal domain model.
- The public repository includes an importable artifact, not only abstract docs.
- Verification checks structure, determinism, link count, forbidden patterns,
  local/private URL prefixes, and credential-looking text.
- User-flow simulation checks that a user can consume the generated artifact.

## Remaining intentional limits

- This repository does not check whether every external site is live at runtime.
- It does not certify commercial licensing of third-party websites.
- It does not expose private folder structure or private preference data.
- It does not run broad discovery, scoring, freshness metabolism, or lifecycle
  automation; that belongs in `resource-radar`.
- It does not auto-promote new sources from private imports into public output.

## Update loop

```text
private bookmark source
-> review and declassify
-> update data/public-sources.json
-> regenerate HTML
-> regenerate projection report
-> verify
-> simulate user flow
```

Commands:

```bash
python -B scripts/build_public_bookmarks.py
python -B scripts/build_projection_report.py
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```
