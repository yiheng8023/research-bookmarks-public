# research-bookmarks-public

English | [简体中文](README.zh-CN.md)

Public-safe bookmark catalogue and browser-importable HTML export.

## Role

This repository owns and maintains its structured public sources, taxonomy,
deterministic browser exporter, aggregate report, and browser-importable
artifact.

## Current snapshot

- 335 public-safe links across 97 bookmark folders.
- The latest naming, classification, ownership, and redundancy review is in
  [the catalogue audit](docs/catalog-audit-2026-07-17.md).

## Core files

- `data/public-sources.json`: maintained public catalogue.
- `data/taxonomy.json`: public taxonomy.
- `exports/research-engineering-bookmarks-public.html`: browser-importable export.
- `data/projection-report.json`: generated counts and boundary checks.

## Occasional update

Run these commands only when the public catalogue changes:

```bash
python -B scripts/build_public_bookmarks.py
python -B scripts/build_projection_report.py
python -B scripts/verify.py
python -B scripts/simulate_user_flow.py
```

## Privacy and contributions

`research-bookmarks` may propose reviewed public-safe candidates, but this
repository decides what it admits. Do not submit raw private bookmarks, folder
paths, browsing history, account or session data, credentials, private notes,
or local URLs. Small source and taxonomy corrections can be proposed through a
normal GitHub issue or pull request; this project has no formal support or
release schedule. Security and privacy reports should follow [SECURITY.md](SECURITY.md).

## Sponsor

Sponsorship is voluntary and supports occasional maintenance. It does not buy
support priority, source admission, features, releases, or technical influence.

- CNY: scan the WeChat Pay or Alipay code below.
- Other supported currencies: use the
  [PayPal payment link](https://www.paypal.com/ncp/payment/LNTF8KXGJXMZY).

Verify the displayed recipient before confirming a payment.

<table>
  <tr>
    <td align="center"><strong>WeChat Pay (CNY)</strong><br><img src="docs/assets/sponsoring/wechat-pay.png" alt="WeChat Pay sponsorship QR code" width="280"></td>
    <td align="center"><strong>Alipay (CNY)</strong><br><img src="docs/assets/sponsoring/alipay.png" alt="Alipay sponsorship QR code" width="280"></td>
  </tr>
</table>
