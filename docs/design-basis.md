# Design Basis

`research-bookmarks-public` exists so people can use the bookmark lane without inheriting a private browser profile.

## Source Model

`data/public-sources.json` and `data/taxonomy.json` are this repository's own
public source surfaces. `research-bookmarks` is an optional source of reviewed
declassification candidates, not a runtime dependency or authority provider.

This repository is the public-safe projection:

```text
optional reviewed candidate
  -> repository-local admission and declassification gate
  -> structured public sources
  -> generated browser-importable HTML
```

## Design Rules

1. Public output must be useful, not merely illustrative.
2. Public output must be generated from structured data.
3. The generated HTML is a product artifact, not the source of truth.
4. Local services, account/session URLs, private preferences, low-trust fallback links, and hard-excluded vendors must not enter the public projection.
5. This repository owns its public-safe catalogue and import/export contract;
   general-purpose discovery or ranking is optional external input, never a
   required control plane.

## Why HTML Is Checked In

Browser bookmark import still expects Netscape bookmark HTML in many browsers. Keeping a generated HTML export in the repository gives developers and users a direct artifact they can download and import.

The checked-in HTML must stay deterministic. If `data/public-sources.json` changes, run:

```bash
python -B scripts/build_public_bookmarks.py
python -B scripts/build_projection_report.py
```

Then verify:

```bash
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```

## v1.2 Baseline Closeout

The current public projection is based on the private `v1.2-final` bookmark
baseline lineage. The private source keeps the full import, later private
overlays, and audit evidence; this public repository keeps only structured
public-safe sources, aggregate projection evidence, and generated
browser-importable output. It is not a live mirror of the current private
bookmark overlay.

See [`projection-closeout.md`](projection-closeout.md).
