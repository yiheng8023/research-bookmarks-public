# research-bookmarks-public

English | [简体中文](README.zh-CN.md)

Public-safe official-source bookmark directory and taxonomy seed for resource discovery, knowledge-graph planning, and browser-independent bookmark portability.

## Repository Role

This repository is a public-safe bookmark catalog. It provides reusable taxonomy, official source directories, and import/export conventions that can seed broader resource discovery systems.

It is not a dump of a user's browser bookmarks.

## What This Repository Provides

- A public-safe taxonomy for research, engineering, knowledge, and tool resources.
- Official-source bookmark examples.
- Validation for public-safe source metadata.
- A boundary model for private bookmark overlays.
- A reusable input lane for resource-radar discovery.

## What This Repository Does Not Own

- Personal browser bookmarks.
- Browsing history, notes, private folders, account state, or preferences.
- Non-official personal recommendations unless explicitly reviewed for public release.
- Resource scoring, repository lifecycle analysis, or GitHub-specific discovery automation; use resource-radar for that.
- Curated agent Skill approval; use a curated Skills repository for that.

## Relationship To Private Bookmarks

Recommended model:

```text
research-bookmarks-public
  -> owns public-safe taxonomy, official sources, import/export contracts

private bookmarks repository
  -> owns complete personal bookmarks, private notes, non-official resources, preferences, and browser exports
  -> may consume the public taxonomy
  -> may promote reviewed official sources back through a declassification gate
```

Do not run blind bidirectional sync. Private-to-public promotion must be filtered and reviewed.

## Relationship To Resource Radar

This repository can provide high-level source categories and official entry points to resource-radar. Resource-radar remains responsible for discovery, normalization, scoring, lifecycle state, deduplication, reports, and candidate routing.

## Layout

```text
data/taxonomy.json                  Public taxonomy seed
data/official-sources.example.json  Official-source examples
docs/                               Boundaries, source policy, sync model
exports/                            Export/import contract notes
scripts/verify.py                   Structure and public-safety checks
```

## Verification

Run:

```bash
python -B scripts/verify.py
```

GitHub Actions runs the same verification on pull requests and pushes to `main`.

## Update Rules

1. Prefer official source pages and canonical project documentation.
2. Keep private browsing history, private notes, subjective rankings, and personal folders out of this repository.
3. Use resource-radar for broad discovery and lifecycle automation.
4. Use a private overlay for complete personal bookmark management.

## Safety Boundaries

This repository is designed to become public. If a bookmark exposes personal preference, private context, non-official endorsement, account state, or browsing behavior, keep it in a private overlay.
