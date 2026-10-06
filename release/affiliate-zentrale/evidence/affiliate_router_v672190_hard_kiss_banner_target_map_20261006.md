# Affiliate Router 6.72.190 — HARD KISS Banner Target Map

## HARD RULE
Automatic banners:
Import -> destination URL -> one-time mapping to fixed portal targets -> store.

Runtime:
- reads stored target map only;
- no destination URL classification;
- no provider-topic precedence;
- no general banner fallback;
- no stored target map = no banner play.

## Performance / database
- no new table;
- no new column;
- no URL history;
- no new frontend DB query;
- no frontend HTTP for destination mapping;
- affected banners are loaded once after an import batch with one batched identity query;
- repeat mapping reuses the same target record;
- target mapping creates no extra creative rows.

## Real WordPress/MariaDB proof
Run: 37443761578 — SUCCESS.

PASS:
- Reithelme destination maps once;
- fixed Reithelme target stored;
- runtime reads stored Reithelme target;
- Schabracken destination maps once;
- fixed Schabracken target stored;
- banner without stored target is not played;
- runtime does not infer destination;
- repeat reuses the same fixed target;
- repeat creates no additional target records;
- no database row growth from target mapping.

Marker:
HARD_KISS_WORDPRESS_MARIADB_PASS

## Final installer
Path:
release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.190.zip

SHA256:
1a4939c91f60a7f526bc713f63719cb1cd3da88d575b7b2ec79cf063f530c1e3

Bytes:
797945

Binding commit:
edcbd500f1429fda5bbcc55aed9c83d784d0bdc2

Final ZIP gates:
- source manifest identity: 27/27 PASS;
- fresh-unpack byte identity: 27/27 PASS;
- PHP lint: 21/21 PASS.

## Upgrade
6.72.190 has its own one-time banner target-map resync state/hook so a previous 6.72.189 done-state cannot suppress rebuilding the fixed mappings.

Live installation remains manual and is not claimed as complete.
