# Affiliate Router 6.72.211 – AJAX/Renderer local hardtest

Date: 2026-10-08
Base: exact released 6.72.210 source, manifest 8b3552ff93d482525e41bd0d279a609d8dd538bf672313ba29574a07f33992bf.

## Scope

One runtime file changed: `affiliate-portal-router/pferdeportal-affiliate-router.php`.
No workflow, architecture, ranking, provider, slot definition, veto, publish, category, design or tracking change.

## AFF-ERR-064

- 6.72.210 negative reproduction: normal banner path emits the undefined-variable warning: PASS.
- 6.72.211 positive: normal banner receives `Anzeige` from the selected banner creative type without warning: PASS.
- Product slots do not receive banner labelling: PASS.
- Glossary single, breed single and overview/category-wide special paths unchanged: PASS.
- Redundant `category_large_banner_slot()` renderer call removed; slot normalization reused: PASS.

## AJAX runtime reduction

Hook-registration harness against exact old/new main source:

- Normal frontend: 142 -> 142 hooks; hook multiset identical: PASS.
- Normal admin: 207 -> 207 hooks; hook multiset identical: PASS.
- admin-ajax: 207 -> 119 hooks.
- admin-ajax `admin_init`: 13 -> 0.
- admin-ajax `init`: 31 -> 9.
- existing `wp_ajax_ppar_ebay_canonical_tick`: 1 -> 1, preserved.

Removed on unrelated AJAX only: admin menus/notices/admin-post handlers plus lifecycle, migration, scheduling and cleanup registrations not required to dispatch the preserved Affiliate AJAX endpoint.

## Package regression

- Source files: 28.
- Changed plugin files versus 6.72.210: 1/28, main PHP only.
- PHP lint: 22/22 PASS.
- Fresh-unpack PHP lint: 22/22 PASS.
- Local ZIP SHA-256: `27a729762ab18d84166a3712a512ae0855fd27e68872ae2c4cacbd4b5b7b0f6a`.
- Candidate source manifest SHA-256: `a3b5be638796ded1070e53c7386f5ecc819e9ec7a08d650c4d217c6406da5bb6`.

## Gate status

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE. NO_INSTALL.
