# Design Basis

`research-bookmarks-public` exists so people can use the bookmark lane without inheriting a private browser profile.

## Source Model

The private source of truth is `research-bookmarks`. It can contain full browser exports, personal folder structure, review notes, private overlays, and non-public context.

This repository is the public-safe projection:

```text
research-bookmarks
  -> full private imports and review evidence
  -> declassification/filtering gate
  -> research-bookmarks-public
  -> structured public sources + generated browser-importable HTML
```

## Design Rules

1. Public output must be useful, not merely illustrative.
2. Public output must be generated from structured data.
3. The generated HTML is a product artifact, not the source of truth.
4. Local services, account/session URLs, private preferences, low-trust fallback links, and hard-excluded vendors must not enter the public projection.
5. `resource-radar` owns discovery, scoring, lifecycle, and wider automation. This repository owns the public-safe bookmark catalog and import/export contract.

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

The current public projection is based on the private
`research_engineering_bookmarks_2026-06-26_v1.2_final.html` baseline. The
private source keeps the full import and audit evidence; this public repository
keeps only structured public-safe sources, aggregate projection evidence, and
generated browser-importable output.

See [`projection-closeout.md`](projection-closeout.md).
