# Exports

This directory contains generated export artifacts and documents export/import contracts.

`research-engineering-bookmarks-public.html` is a deterministic public-safe Netscape bookmark HTML export generated from `data/public-sources.json`.

Do not edit generated HTML by hand. Regenerate it with:

```bash
python -B scripts/build_public_bookmarks.py
```

Do not commit raw browser exports here unless they have been filtered for public release. Raw exports often contain private folders, account-specific URLs, local context, and personal browsing patterns.
