# Public Catalog Audit — 2026-07-17

## Scope

The audit covered every public catalogue record, taxonomy placement,
canonical address, title, entry role, market scope, ownership-evidence state,
source type, exact-URL uniqueness, URL health, and private/public admission
boundary.

## Results

- 334 public-safe records use 334 unique canonical HTTPS URLs.
- Domains 09, 11, and 14 are populated after correcting the historical
  taxonomy-alias failure.
- Workspace/common-entry and domestic/international folders are views, not
  resource owners. No public record uses category 00, and region wording is
  absent from canonical titles.
- SourceForge was removed because its low-trust private classification
  conflicted with the public admission claim.
- One institution/account-adjacent student entrypoint was removed.
- Eight separately reviewed public candidates were admitted: Cursor,
  OpenCode, two Qoder entrypoints, two TRAE entrypoints, WorkBuddy, and
  SpaceXAI.
- Claude Code, Arena AI, and Qianwen use reviewed canonical URLs with address
  lineage retained in `previous_urls`.
- `official_or_canonical` is now derived from a controlled source type;
  reviewed community, secondary, and public-knowledge references are no
  longer mislabeled as official.

## Ownership Evidence

- 20 sources have reviewed brand-level evidence.
- 7 sources have reviewed legal-entity evidence.
- 307 sources remain `needs_review`.

The pending records remain public-safe but do not claim a verified legal
owner. Their product, canonical host, admission basis, and review state are
explicit so later evidence review is deterministic.

## URL Health Snapshot

- 259 reachable by the unauthenticated check or reviewed canonical redirect;
- 50 automation-limited responses (`403`, `405`, or `429`), not treated as
  dead links;
- 17 require follow-up after timeout or other ambiguous responses;
- 8 newly admitted candidates have no automated snapshot yet.

## Independence Boundary

This file records a one-time reviewed reconciliation. The public repository
continues to build and verify from its own `data/public-sources.json`; it has no
runtime dependency on the private repository and contains no raw private
bookmark hierarchy.

## Verification

```text
python -B scripts/build_public_bookmarks.py
python -B scripts/build_projection_report.py
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```
