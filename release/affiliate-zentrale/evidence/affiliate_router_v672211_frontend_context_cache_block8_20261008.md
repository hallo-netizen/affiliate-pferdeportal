# Affiliate Router 6.72.211 – frontend context cache block 8 local hardtest

Date: 2026-10-08
Base manifest: 3ac981ddd070120b687a6d8f33e3c3375630a4dd953c31ecd6385c270a4ede68
Candidate manifest: 9f15bf679f44456c18c32aa6e04504e87248bc2748cfbca880532318915d311f

## Scope

One-file performance-only change in `pferdeportal-affiliate-router.php`.
Public frontend requests now keep request-local immutable caches for `get_content_context()` and `get_category_archive_context()`.
Admin/Cron/REST/CLI/AJAX are explicitly excluded through the existing frontend-cache eligibility rule.

## Local positive / negative / regression

- PHP lint: 22/22 PASS.
- Repeated content-context call returns identical array before/after.
- Repeated category-context call returns identical array before/after.
- Public frontend repeated content context: post type/title/slug/terms/content resolution 2 -> 1.
- Public frontend repeated term ancestry work across content + category context: `get_ancestors(category)` 4 -> 2 and `get_term(category)` 4 -> 2 in the fixture.
- Public frontend `wp_strip_all_tags` context work: 4 -> 2 in the fixture.
- Admin: all counted calls remain exactly unchanged.

No ranking, matching, provider, slot, veto, publish, category, design, tracking, schema or returned context data changed.

## Result

LOCAL_POSITIVE_NEGATIVE_REGRESSION_PASS.
REPEATED_FRONTEND_CONTEXT_BUILD_WORK_HALVED_FOR_IDENTICAL_CONTENT_OR_CATEGORY_CONTEXT.
WORDPRESS_MARIADB_CURRENT_GATE_OPEN.
NO_RELEASE. NO_INSTALL.
