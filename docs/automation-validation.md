# Automation Validation

This repository validates the public bookmark loop as a user-facing artifact:

```text
structured public sources
  -> deterministic bookmark exporter
  -> deterministic projection report
  -> checked-in browser-importable HTML
  -> user-flow simulation
  -> GitHub Actions verification
```

## Commands

Regenerate the HTML:

```bash
python -B scripts/build_public_bookmarks.py
python -B scripts/build_projection_report.py
```

Check that the export is up to date and public-safe:

```bash
python -B scripts/verify.py
```

Simulate a user consuming the repository:

```bash
python -B scripts/simulate_user_flow.py
```

## What The Simulation Proves

- The generated HTML exists.
- The projection report exists and matches the structured source counts.
- It is deterministic from `data/public-sources.json`.
- The HTML link count matches the structured source count.
- The projection has a meaningful folder taxonomy.
- Local/private URL prefixes do not leak.
- Hard-excluded vendors and low-trust patterns do not leak.
- Credential-looking patterns do not appear in the generated HTML.

## What It Does Not Prove

- It does not verify every external website is live at runtime.
- It does not certify commercial licensing of third-party websites.
- It does not prove the private source repository is safe to publish.
- It does not replace `resource-radar` discovery, scoring, lifecycle, and broader projection tests.
