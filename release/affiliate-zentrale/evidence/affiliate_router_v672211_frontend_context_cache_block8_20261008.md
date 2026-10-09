# Affiliate Router 6.72.211 – frontend context cache block 8 hardtest

Date: 2026-10-08 / final gate 2026-10-09
Base manifest: 3ac981ddd070120b687a6d8f33e3c3375630a4dd953c31ecd6385c270a4ede68
Candidate manifest: 9f15bf679f44456c18c32aa6e04504e87248bc2748cfbca880532318915d311f

## Scope

Performance block through Block 8, including AFF-ERR-064 fix, AJAX lifecycle reduction, shared frontend campaign query/normalization reuse and request-local content/category context reuse.

No ranking, matching, provider, slot, veto, publish, category, design, tracking or workflow behavior change.

## Local positive / negative / regression

- PHP lint: 22/22 PASS.
- AFF-ERR-064 local regression: PASS.
- Foreign AJAX affiliate hooks: 207 -> 75.
- Public frontend campaign query: 2 -> 1.
- Campaign meta normalization: repeated work halved.
- Repeated content-context call returns identical array before/after.
- Repeated category-context call returns identical array before/after.
- Public frontend repeated content context: post type/title/slug/terms/content resolution 2 -> 1.
- Public frontend repeated term ancestry work across content + category context: get_ancestors(category) 4 -> 2 and get_term(category) 4 -> 2 in the fixture.
- Public frontend wp_strip_all_tags context work: 4 -> 2 in the fixture.
- Admin path: unchanged.

## WordPress / MariaDB final gate

GitHub Actions run: 37897225202

- WordPress 7.1.2 plugin activation: PASS.
- MariaDB 10.11: PASS.
- Automation health invariants: PASS.
- Backend/textlink/DB hard positive-negative regression: 59 PASS / 0 FAIL.
- Exact plugin version 6.72.211 active: PASS.
- Package source -> ZIP identity: PASS 28/28.
- Exact tested installer: AFFILIATE_ZENTRALE_6.72.211.zip.
- Installer SHA-256: 6776600d7627bf767d81bc1a295ea2273f650fb6f291fe2b399131b628c44b00.
- Installer bytes: 812444.
- Workflow artifact ID: 11600791937.

## Result

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
WORDPRESS_MARIADB_POSITIVE_NEGATIVE_REGRESSION_PASS.
EXACT_TESTED_INSTALLER_READY.
NO_PLUGIN_SOURCE_CHANGE_AFTER_BLOCK8.
