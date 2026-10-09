# Affiliate Router 6.72.211 – full release gate

Date: 2026-10-09
Source manifest SHA-256: 9f15bf679f44456c18c32aa6e04504e87248bc2748cfbca880532318915d311f

## Gate result

- Local performance positive/negative/regression: PASS.
- PHP lint: 22/22 PASS.
- AFF-ERR-064: PASS.
- Foreign AJAX affiliate hooks: 207 -> 75.
- Public frontend campaign query: 2 -> 1.
- Repeated campaign normalization: halved.
- Content/category request-local context reuse: functional equality PASS.
- WordPress 7.1.2 + MariaDB 10.11: PASS.
- Backend / DB positive-negative regression: 59 PASS / 0 FAIL.
- Source -> ZIP identity: PASS 28/28.
- No ranking, provider, slot, veto, publish, category, design, tracking or plugin workflow change.

## Final installer

- Final binding run: 37897835885
- File: AFFILIATE_ZENTRALE_6.72.211.zip
- SHA-256: f968f99ba0ae753361d7a7d952f3b2cab5e5029c447a1691b163d4ca88455751
- Bytes: 812444
- Repository path: release/affiliate-zentrale/artifacts/final/AFFILIATE_ZENTRALE_6.72.211.zip

## Result

FULL_RELEASE_GATE_PASS.
EXACT_TESTED_INSTALLER_REPOSITORY_BOUND.
PLUGIN_SOURCE_UNCHANGED_AFTER_BLOCK8.
