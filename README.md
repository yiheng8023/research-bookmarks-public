# research-bookmarks-public

English | [简体中文](README.zh-CN.md)

Public-safe bookmark catalog, source taxonomy, and browser-importable HTML projection for research, engineering, knowledge work, and resource discovery.

Note: `public` describes the content boundary. The repository may remain private while it is staged, but its contents are maintained as public-safe so it can be published later without exposing private bookmark data.

## Repository Role

This repository owns the public-safe bookmark projection. It provides:

- a reusable taxonomy;
- a structured public source catalog;
- deterministic generation of browser-importable bookmark HTML;
- validation and user-flow simulation for the public artifact.

It is not a dump of a user's private browser bookmarks.

## What This Repository Provides

- `data/taxonomy.json`: broad resource taxonomy aligned with the resource-radar domain model.
- `data/public-sources.json`: reviewed public-safe official or canonical sources.
- `exports/research-engineering-bookmarks-public.html`: generated bookmark HTML that users can import into a browser.
- `scripts/build_public_bookmarks.py`: deterministic exporter from structured sources to HTML.
- `scripts/simulate_user_flow.py`: user-facing importability and safety simulation.
- Public/private boundary, source policy, design basis, and sync model docs.

## What This Repository Does Not Own

- Complete personal browser bookmarks.
- Browsing history, private folders, private notes, account state, or subjective preferences.
- Raw private bookmark imports; those belong in `research-bookmarks`.
- Discovery, scoring, lifecycle analysis, summarization, or broad automation; those belong in `resource-radar`.
- Curated agent Skill approval; that belongs in the curated Skills repository.

## Relationship To The Paired Repositories

```text
research-bookmarks
  -> private source of truth for complete imports, overlays, audits, and declassification inputs

research-bookmarks-public
  -> public-safe taxonomy, structured official/canonical sources, deterministic HTML export

resource-radar
  -> discovery, normalization, scoring, lifecycle state, summaries, and broader projections

open-resource-governance
  -> public governance hub and launch/readiness material
```

Do not run blind bidirectional sync. Private-to-public promotion must be filtered, reviewed, and regenerated through this repository's exporter.

## Design Basis

The design follows four constraints:

1. Users need a real importable bookmark artifact, not only abstract rules.
2. HTML is useful as an output, but structured data must remain the source.
3. Public projections must not leak local services, account/session URLs, private preferences, or low-trust fallback resources.
4. `resource-radar` can automate discovery and lifecycle, but this repository remains the public bookmark projection lane.

See [docs/design-basis.md](docs/design-basis.md).

## Layout

```text
data/taxonomy.json                         Public resource taxonomy
data/public-sources.json                   Public-safe official/canonical source catalog
docs/design-basis.md                       Why this repository exists and how it is split
docs/automation-validation.md              Validation and user-flow simulation contract
docs/public-private-boundary.md            Public/private bookmark boundary
docs/private-public-sync-model.md          Safe promotion and sync model
docs/source-policy.md                      Source admission policy
exports/research-engineering-bookmarks-public.html
                                            Generated browser-importable bookmark HTML
scripts/build_public_bookmarks.py          Deterministic exporter
scripts/simulate_user_flow.py              User-flow simulation
scripts/verify.py                          Structure, safety, and determinism checks
```

## Verification

Regenerate:

```bash
python -B scripts/build_public_bookmarks.py
```

Verify:

```bash
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```

GitHub Actions runs verification on pull requests and pushes to `main`.

## Update Rules

1. Edit `data/public-sources.json`, not the generated HTML.
2. Regenerate `exports/research-engineering-bookmarks-public.html`.
3. Run verification and user-flow simulation.
4. Keep complete private bookmarks in `research-bookmarks`.
5. Use `resource-radar` for broader discovery, scoring, lifecycle, and future automated replenishment.

## Safety Boundaries

This repository is public-safe by design. If a bookmark exposes personal preference, private context, non-official endorsement, local service state, account/session data, or low-trust fallback behavior, keep it in `research-bookmarks` or a private review queue.
