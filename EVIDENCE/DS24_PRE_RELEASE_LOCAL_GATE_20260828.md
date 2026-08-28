# Digistore24 pre-release local full-workflow gate

**Date:** 2026-08-28  
**Status:** `LOCAL_HARD_PASS_PENDING_LIVE_API_AND_EBAY_TERMINAL`  
**Release:** **NOT RELEASED / DO NOT INSTALL**

## Baseline

- Tested baseline is byte-identical to a fresh unpack of the released Affiliate-Zentrale V6.62.0 installer.
- Candidate staging ZIP roundtrip is byte-identical to the tested candidate source tree.
- Exact plugin diff scope versus V6.62.0: exactly 3 files: new `includes/trait-ppar-digistore24.php`, changed `includes/trait-ppar-output-objects.php`, changed `pferdeportal-affiliate-router.php`.

## Protected workflow areas

Byte-identical to V6.62.0: eBay canonical run/provider/account-deletion, idealo, central automation suite, creative library, provider registry, network sync/provider intake, frontend CSS/JS, eBay portal catalog, portal structure, readme.

## Negative findings caught and fixed before release

1. **Central automation starvation:** a Digistore API `WP_Error` could prevent the shared cursor from advancing and starve Awin/ADCELL. Negative reproduced; final contract returns provider-local `partial`/non-`WP_Error`, so the central cycle continues.
2. **Non-Digistore output regression:** an early Digistore output hardlock could affect normal banners. Negative reproduced; final provider-specific guard leaves 10 non-Digistore output cases identical.
3. **Two-step activation defect:** the initial candidate required `Speichern & API prüfen` and then a second Save. Negative reproduced; final flow keeps requested activation behind the fingerprint/API gate and fulfills it automatically only after a successful read-only test. Explicitly unchecked remains disabled.
4. **Semantic evidence loss:** the initial candidate dropped marketplace description before automatic page targeting. Negative identified against the real provider-neutral classifier; final flow preserves headline + description + category. Exact horse-health/back fixture targets the correct page.
5. **Unapproved marketplace candidate risk:** the initial candidate did not explicitly reject `pending`/`rejected` marketplace entries. Negative reproduced; final flow fails closed on an explicit non-`approved` status while remaining compatible with payloads that omit the status field.

## Positive/negative suites

- Digistore core/API/credential/automation: **64/64 PASS**
- Vendor support/banner import: **24/24 PASS**
- Digistore output hardlock: **4/4 PASS**
- Actual provider-neutral semantic target classifier: **6/6 PASS**
- Non-Digistore output regression matrix: **10/10 identical**
- PHP lint: **15/15 PASS**
- Full-workflow meta gate: **42/42 PASS**

## Hard contracts verified

- Digistore is banner-only: `portal_banner` only; never product campaign, HivePress listing, or product card.
- No Digistore-specific cron; existing central automation clock only.
- Read-only GET API allow-list only: `listMarketplaceEntries`, `getMarketplaceEntry`, `getUserInfo`.
- API key only in `X-DS-API-KEY`; API redirects disabled; response size limited.
- Key fingerprint must match the successfully tested key before automation can schedule.
- `Speichern & API prüfen` can fulfill a checked enable request in one flow only after the read-only API test succeeds; an unchecked provider remains off.
- Explicitly `pending`/`rejected` marketplace entries cannot become automatic candidates.
- Marketplace description is preserved as real semantic evidence for the existing provider-neutral page classifier.
- Manual partnership confirmation required before vendor banner import.
- HTTPS support page only, fetched through WordPress safe HTTP.
- Tracking URL limited to HTTPS `checkout-ds24.com` / `www.checkout-ds24.com` `redir/content/link` paths.
- `[PARTNER_LINK]` fallback uses standard Digistore promolink from `main_product_id` + tested affiliate ID.
- No automatic public activation during marketplace discovery/import.
- eBay `external_tick_v2` / single-worker contract remains unchanged.

## Still required before release

- Real read-only API test with the user's Digistore API key on the live WordPress installation.
- Inspect real `listMarketplaceEntries` / `getMarketplaceEntry` payload for support/promolink fields; do not assume undocumented fields.
- Real vendor support-page/banner import test with one approved partnership.
- eBay canonical run must be terminal before installing a new Affiliate-Zentrale build.
- Then rerun the complete local negative/positive/full-workflow gate on the exact final installer and its fresh unpack.

**NO PLUGIN RELEASE IS AUTHORIZED YET.**
