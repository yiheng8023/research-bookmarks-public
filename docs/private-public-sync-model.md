# Private / Public Sync Model

Use this public-safe projection plus the private `research-bookmarks` source repository.

```text
research-bookmarks-public
  -> taxonomy, official sources, import/export contracts

research-bookmarks
  -> full bookmarks, private notes, non-official resources, preference data
```

Public-to-private sync is safe for taxonomy and official/canonical source seeds.

Private-to-public sync must be a filtered promote workflow. Do not mirror `research-bookmarks` into this public-safe repository.
