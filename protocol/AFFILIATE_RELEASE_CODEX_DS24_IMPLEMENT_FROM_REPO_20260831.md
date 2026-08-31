# AFFILIATE-ZENTRALE V6.64.0 — Repository-native Codex task: Digistore24 automation

Stand: 2026-08-31
Repository: `hallo-netizen/affiliate-pferdeportal`
Branch: `affiliate-release-current`
Workstream: `AFFILIATE_ZENTRALE`

## Why this task exists

Codex Cloud works from the connected Git repository. Do **not** require local attachments, pasted source files, ZIPs, Base64 payloads, or files outside the repository. All implementation context for this task is in the current repository.

## Mandatory first read

Before changing anything, read:

1. `control/release-governance/CURRENT_RELEASE.json`
2. `protocol/AFFILIATE_RELEASE_MASTER_CURRENT.md`
3. `release/affiliate-zentrale/evidence/digistore24_automatic_partner_banner_gate_v6640_static.txt`
4. `release/affiliate-zentrale/evidence/digistore24_getaffiliatecommission_schema_v6640.txt`
5. current source files:
   - `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-digistore24.php`
   - `release/affiliate-zentrale/current/affiliate-portal-router/includes/trait-ppar-output-objects.php`

Proceed only while governance still says:
- `workstream=AFFILIATE_ZENTRALE`
- `mode=ENFORCED`
- `active_candidate.version=6.64.0`
- `active_candidate.status=WORKING`
- `active_candidate.release_allowed=false`
- `execution_state.state=RUNNING_BOUND_RELEASE_GATES`
- `execution_state.authorized_next_action=RUN_BOUND_RELEASE_GATES`
- active work branch is `affiliate-release-current`.

If any of those changed, fail closed and report the exact mismatch. Do not create a new branch.

## Single implementation goal

Finish the already-bound Digistore24 banner automation **inside the existing architecture** so that the normal path is as automatic as the documented Digistore24 API permits, while all publication remains fail-closed.

Digistore24 stays **banner-only**. It must never become a product/listing source.

## Required behavior

### 1. Read-only API contract

Keep the provider read-only. Existing methods `getUserInfo`, `listMarketplaceEntries`, and `getMarketplaceEntry` remain read-only. Add/support `getAffiliateCommission` as a read-only GET call.

For `getAffiliateCommission`:
- use the currently tested own `affiliate_id` only;
- accept only 1..50 canonical numeric `product_ids` per request;
- reject foreign/mismatching affiliate identity before network I/O;
- reject empty, malformed, or >50 product-id sets before network I/O;
- bind the returned proof to the currently tested API-key fingerprint.

The documented response fields used by the gate are:
- `product_id`
- `product_is_active`
- `approval_status`
- `commission_rate` when available.

Do not invent undocumented response fields.

### 2. Automatic affiliation proof

For each candidate Marketplace product used by automation, store a read-only affiliation proof derived from `getAffiliateCommission`.

Automatic publication is allowed only when the proof is fresh and says:
- `approval_status=approved`
- `product_is_active=true`
- proof belongs to the current tested credential fingerprint and current affiliate identity.

Fail closed for:
- `pending`
- `rejected`
- `new`
- missing commission row
- inactive product
- stale proof
- credential change
- affiliate-id mismatch
- API error.

Use a maximum proof age of 2 days. A stale proof must be refreshed before publication.

Manual partnership confirmation may remain as a manual-import/admin fallback, but it must **not** authorize automatic publication.

### 3. Bounded automatic Marketplace selection

Extend the existing central automation dispatch; do not add a provider-specific cron or parallel worker architecture.

The Digistore cycle must be bounded per central automation run and must not starve other providers.

Only consider Marketplace entries relevant to the Pferde-/Reitsport portal using the already existing relevance/targeting mechanisms. Do not invent relevance when the data is insufficient.

Use real Marketplace performance/commission data only where present. Never synthesize missing conversion, earnings, or commission data.

### 4. Vendor creative page and real banners

The Marketplace API does not document a banner/support-page URL. Therefore:
- do not invent one;
- allow a valid HTTPS vendor support/creative URL to be stored once for a Marketplace entry;
- reuse that stored URL on later automation cycles;
- if no validated URL exists, the automatic cycle may mark the candidate as requiring the one-time URL input, but must continue processing other candidates instead of stopping the entire provider.

Import only real vendor banners that pass the existing Digistore tracking-link and image gates.

No product cards, listings, pseudo-banners, generated placeholder banners, or scraped arbitrary consumer pages.

### 5. Automatic target and slot assignment

Do not create a Digistore-specific placement architecture.

After a real banner is imported and its asset/tracking data is verified, use the existing central output/target/slot classification to decide where it belongs in the portal.

The target and slot must come from the existing portal/output model. Missing or ambiguous target/slot stays inactive.

### 6. Full publication revalidation

Before any Digistore banner becomes public, reuse the existing full output revalidator. The final gate must include the existing checks for at least:
- global/provider veto / emergency off state;
- provider identity;
- `creative_type=banner`;
- source kind / source binding;
- current Digistore affiliation proof (`approved + active + fresh + same credentials`);
- tracking URL;
- image URL / downloaded asset / hash / actual dimensions as required by current output code;
- current topic/portal target;
- current design slot;
- current source fingerprint.

Do not add a weaker Digistore-only shortcut.

### 7. Two-phase Last-Known-Good safety

A newly materialized Digistore candidate starts inactive/draft.

It must **not** supersede an already published conflict object merely by being materialized or by passing an earlier generic banner activator.

Required order:
1. materialize new candidate as draft/inactive;
2. run provider-specific final Digistore affiliation check plus the complete central output revalidation;
3. persist the new object as `published` successfully;
4. only then supersede/disable the previous conflict object.

If persistence fails, roll back the new campaign/output activation and preserve Last-Known-Good.

If an earlier generic shutdown/activation path temporarily marks an unapproved Digistore candidate active, the later Digistore final gate must roll it back to inactive/draft before request end.

### 8. Scope restrictions

Do not change:
- eBay source/router/run code;
- idealo behavior;
- deal-radar semantics outside what is strictly needed for this Digistore block;
- product-source routing;
- OTTO/Kelkoo/Kaufland/Amazon source preparation;
- `.github/workflows/**`;
- archived sources;
- immutable governance/test files;
- plugin version solely for this task;
- any frontend design rule unrelated to the existing banner slot classifier.

Do not create another plugin, worker, scheduler, queue, source truth, or architecture.

## Required tests

Run PHP lint for every changed PHP file.

Add or run a focused local harness that proves at least all of these states:

Positive:
- exact `getAffiliateCommission` GET request built with own affiliate ID and valid product IDs;
- approved + active affiliation proof is stored credential-bound;
- fresh approved + active proof can pass the provider gate;
- valid verified banner can reach full central revalidation;
- successful persistence publishes the new output and only then supersedes the previous conflict object.

Negative:
- foreign affiliate ID blocked before network call;
- 0 product IDs blocked;
- >50 product IDs blocked;
- malformed product ID blocked;
- pending/rejected/new blocked;
- inactive product blocked;
- missing row blocked;
- stale proof blocked/refreshed before publication;
- changed API-key fingerprint invalidates prior proof;
- failed output persistence rolls campaign/output back and preserves Last-Known-Good;
- an earlier generic activation cannot leave an unapproved Digistore candidate public at request end.

Run with strict error reporting (`E_ALL`) where the existing test harness permits it.

## Manifest and governance binding

After code/tests pass:

1. Recompute the SHA-256 values from the **actual changed current source**.
2. Update `release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt` so it exactly matches the direct committed 25-file current source tree.
3. Compute SHA-256 of that manifest.
4. Update only the current manifest binding fields in `control/release-governance/CURRENT_RELEASE.json` that must follow the new source manifest.
5. Keep:
   - `active_candidate.version=6.64.0`
   - `active_candidate.status=WORKING`
   - `active_candidate.release_allowed=false`
   - `explicit_scope_product_deals_partner_analytics.status=PENDING`.
6. Do not alter historical PASS evidence or pretend it is bound to the changed source.
7. `git diff --check` must pass.

Commit the source + manifest + governance binding in one commit if the environment permits. If Codex's cloud handoff requires its normal task commit/PR mechanism, keep the diff limited to the authorized files and report the resulting commit/diff for review.

## Completion output

Only after all required local tests pass, report:
- changed paths;
- exact test results;
- final source SHA-256 for both PHP files;
- final `CURRENT_SOURCE_SHA256.txt` SHA-256;
- governance binding status;
- `release_allowed=false`;
- explicit statement that real Digistore24/WordPress/MariaDB live proof is still pending.

Do not build a final installer ZIP and do not rerun already-passed eBay gates.