# AFF-ERR-065 — Existing Affiliate Source: bounded red-green evidence

Date: 2026-10-13
Branch: affiliate-release-current
Current generation at source proof: 311
Exact source manifest SHA-256: f11687daa1f11d8ff98a3c0d62a720dac170dd95edddf39eba04530e858c44cf
Release: FORBIDDEN. Historical released 6.72.211 ZIP remains unchanged.

## Existing WordPress/MariaDB runtime
Existing workflow: .github/workflows/affiliate-v672195-hardtest.yml
WordPress 7.1.2; MariaDB 10.11; PHP 8.3.
Actual plugin methods through WordPress wp eval-file. Test-only identical original post_inline_banner matrix was supplied since real Template Kit 1.50.612 was not installed in isolated CI.

- Article plan READY with no actual products, valid standby suppressed: RED 38379811116, GREEN 38380374323.
- Historical saved READY plan with no preplanned standby: RED 38380655622, GREEN 38381089066.
- Verified generic horse-product rank missing for normal post: RED 38381357138, GREEN 38381644711.
- Invalid eBay BUSINESS source remains blocked; 499h stale idealo blocked, fresh idealo eligible: GREEN 38381884894.
- Reitstiefel vs unrelated lower-tier Gerten blocked; equal-ranked eBay/idealo category mix preserved: GREEN 38382020308.
- Final CI 38382020308: existing backend WP/MariaDB tests 59/59 PASS; all bound AFF-ERR-065 targeted positive/negative tests PASS; PHP/source manifest PASS. Installer packaging SKIPPED, release-check SKIPPED while release_allowed=false.

## Exact minimal source scope
- Existing includes/trait-ppar-article-plans.php: actual rendered products first, preplanned second different valid banner only when no cards, one-time old postmeta standby recovery; no global replan.
- Existing pferdeportal-affiliate-router.php: last relevance tier only for normal post_bottom_products and auto_verified original eBay/idealo product sources; existing independent policy/source/health/VETO and exact-ID checks not bypassed.
- Existing source manifest, CURRENT and existing CI updated. No new architecture, no table, no new frontend HTTP or installer.

## Blocking real-world gates
- Actual provider-source/policy/route/checkpoint/expiry for published eBay rows has not been verified on live/test.
- Actual idealo feed import after historical 499.2h age has not been verified.
- Exact currently installed version/source after local 6.72.226 packets unknown; earlier Oct 12 data was 6.72.224.
- Actual Template Kit 1.50.612 integration, live category/article HTML, and end-to-end performance not independently certified.
- Category relevance strict-tier preserved, no forced unrelated fallback.

Status: PARTIAL_LOCAL_ROOTFIX_PASS / REAL_LIVE_TEST_PROVIDER_GATE_OPEN / NO_RELEASE.
