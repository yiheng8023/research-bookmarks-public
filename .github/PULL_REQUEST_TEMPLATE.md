## Summary

Describe the public-safe problem and the bounded change.

## Verification

- [ ] Generated artifacts were rebuilt when structured data changed.
- [ ] `python -B scripts/verify.py` passes.
- [ ] `python -B scripts/simulate_user_flow.py` passes.
- [ ] English and Chinese guidance remain aligned when user-facing behavior changed.

## Public-data boundary

- [ ] No raw private bookmarks, folder paths, browsing history, account/session data, credentials, or private review notes are included.
- [ ] New sources have an explicit admission basis, provenance, ownership status, and URL-health status.
