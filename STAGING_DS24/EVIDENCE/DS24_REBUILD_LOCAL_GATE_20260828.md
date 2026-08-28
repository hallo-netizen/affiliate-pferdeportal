# Digistore24 reconstructed candidate – local full-workflow gate

**Date:** 2026-08-28  
**Branch target:** `ds24-rebuild-20260828` (staging only, never release/main)  
**Status:** `LOCAL_HARD_PASS_PENDING_EBAY_TERMINAL_LIVE_API_VENDOR_E2E`  
**Release:** **NOT RELEASED / DO NOT INSTALL**

## 1. Binding baseline

- Released Affiliate-Zentrale baseline: **V6.62.0 KISS eBay Orchestrator**.
- Exact uploaded baseline ZIP SHA-256: `1b154321f9731787243bb4068a7ad1df73f16837005e655e5b165a09b47ba200`.
- Rebuild started from a fresh unpack of that exact ZIP.
- Candidate version deliberately remains `6.62.0`; no release bump is claimed.
- `EBAY_RUNTIME_BUILD` remains `6.56.0-safe-gap-churn-revalidation-rootfix-20260827`.

## 2. Exact candidate diff scope

Exactly three plugin paths differ from released V6.62.0:

1. **NEW** `includes/trait-ppar-digistore24.php`
2. **CHANGED** `includes/trait-ppar-output-objects.php`
3. **CHANGED** `pferdeportal-affiliate-router.php`

All other 17 plugin files remain byte-identical to the released baseline. Protected byte-identical areas include eBay canonical run/provider/account-deletion, idealo, central automation, creative library, provider registry, network sync/provider intake, portal catalogs, frontend CSS/JS, article plans, control contract and readme.

Final changed-file SHA-256:

- `includes/trait-ppar-digistore24.php`: `c295c54e9fcc62b4817b7f29d33a2de2d340ade4e5909ebb1ae1aed8b6b1edf5`
- `includes/trait-ppar-output-objects.php`: `f9f7675e6a9e3672c763f0d88b5570d8816964080b4b877600b7a39986d1d92a`
- `pferdeportal-affiliate-router.php`: `266d27da7fe6beb83d733d4d335a430f5218930485bad99b6328eb7e1fc5321d`

## 3. Binding Digistore24 architecture

- Digistore24 is a **banner-only provider**.
- Never create/product-route a Digistore product campaign, product card, HivePress listing or portal listing.
- No Digistore-specific cron. Existing central automation cursor only.
- Read-only API allow-list only: `listMarketplaceEntries`, `getMarketplaceEntry`, `getUserInfo`.
- API key only in `X-DS-API-KEY`; no API redirects; bounded time/response size.
- Current key must match the successfully tested key fingerprint before automatic work.
- `Speichern & API prüfen` fulfills a checked enable request only after the read-only API test succeeds; unchecked remains disabled.
- Explicit `new`, `pending`, `rejected` marketplace status fails closed. Payloads omitting status remain compatible as documented by the earlier binding candidate.
- Marketplace headline + description + category are preserved as semantic evidence for the existing provider-neutral target classifier.
- Manual partnership confirmation is mandatory before vendor banner import.
- Vendor support page must be explicit HTTPS; implicit redirects are disabled so an HTTPS start URL cannot silently downgrade.
- Vendor banner image must itself be HTTPS before import.
- Tracking URL is HTTPS on `checkout-ds24.com` / `www.checkout-ds24.com`, path contract `redir|content|link`, and must carry the Affiliate-ID proven by the current tested API key.
- `[PARTNER_LINK]` fallback uses `main_product_id` + the tested Affiliate-ID.
- Imported creatives start `review`, `selected=0`; normal banner materialization remains inactive/draft. No automatic public activation.
- A Digistore provider-local failure returns `partial`/non-`WP_Error`, so the shared automation cursor continues to Awin/ADCELL/etc.

## 4. Negative findings reproduced and fixed during reconstruction

### F1 – Generic manual/legacy campaign path could bypass “banner-only”

**NEGATIVE reproduced on exact pre-hardening reconstruction:** a campaign with `network=digistore24`, `creative_type=product`, valid title/image/url/page and active flag returned complete, remained active after sanitization and was not counted as blocked.

**FIX:** the shared `campaign_is_complete()` gate now fails closed for Digistore unless the campaign is a banner in `image_link` mode with an accepted Digistore tracking URL. This protects manual, legacy and injected campaign records in addition to the output-object planner.

**POSITIVE:** identical product fixture now `complete=false`, blocked count `1`, active forced false; type is not silently converted.

**REGRESSION:** 10 representative non-Digistore campaign shapes (Awin, ADCELL, eBay, idealo, direct/manual; banner/product) are behavior-identical before/after.

### F2 – Generic Digistore banner could bypass tracking hardlock

**NEGATIVE reproduced:** pre-hardening candidate accepted (a) a Digistore-labelled banner pointing to `evil.example`, and (b) a Digistore HTML-mode banner with no validated tracking URL.

**FIX:** same shared completeness gate requires `image_link` plus `digistore24_tracking_url_allowed()` for every Digistore campaign.

**POSITIVE:** both exact negative fixtures are now blocked and forced inactive; a valid Digistore banner remains complete and active when explicitly enabled.

### F3 – Explicit vendor link could carry somebody else’s affiliate ID

**NEGATIVE reproduced:** prior tracking validator accepted `https://www.checkout-ds24.com/redir/321/other_aff` because only host/path were checked.

**FIX:** accepted explicit tracking links must contain the Affiliate-ID belonging to the currently fingerprint-verified API key as an exact path segment. Substrings/case variants do not pass. `[PARTNER_LINK]` remains the safe placeholder path.

**POSITIVE:** current Affiliate-ID passes redir/content/link fixtures; wrong ID, substring attack and fingerprint mismatch fail closed.

### F4 – Vendor support/image transport was not fully HTTPS-fail-closed

**NEGATIVE reproduced:** prior vendor parser accepted an HTTP banner image; prior support fetch allowed three implicit redirects after validating only the initial HTTPS URL.

**FIX:** banner image must be HTTPS before import; support fetch uses `wp_safe_remote_get` with `redirection=0`, while existing 20s timeout and 2 MiB response cap remain unchanged.

**POSITIVE:** HTTP image is rejected before upsert; support fetch proves redirects disabled; secure banner import still succeeds.

## 5. Existing earlier negative findings retained

The reconstruction also retains the previously documented fixes and tests for:

- central automation starvation by a Digistore `WP_Error`;
- non-Digistore output regression caused by an overbroad Digistore output guard;
- two-step activation defect;
- marketplace description loss before semantic targeting;
- `pending`/`rejected` marketplace candidate risk.

## 6. Final source-tree test result

Final source tree, after all F1–F4 hardening:

- Digistore core/API/credential/automation: **72/72 PASS**
- Vendor support/banner import: **53/53 PASS**
- Output hardlock + non-Digistore output regression: **27/27 PASS**
- Provider-neutral semantic classifier: **8/8 PASS**
- Central automation cursor integration: **8/8 PASS**
- Full plugin bootstrap: **8/8 PASS**
- Generic campaign runtime hardlock NEG/POS + non-DS regression: **24/24 PASS**
- Tracking/Affiliate-ID NEG/POS: **8/8 PASS**
- Support transport/image NEG/POS: **7/7 PASS**
- Static/full-workflow meta gate: **45/45 PASS**

**Combined source-tree gate: 260/260 PASS.**

Candidate PHP lint: **15/15 PASS**.

## 7. Internal archive / Fresh-Unpack gate

Internal test archive only (not released, not user-facing):

`affiliate-zentrale_v6.62.0_DS24_REBUILD_INTERNAL_DO_NOT_INSTALL.zip`

SHA-256: `99b22ffe755e9b46bee7265d9166999c3d129a88fc598cc096c4d247b99a37a9`

- Source files: 20
- Fresh-unpack files: 20
- Byte-for-byte archive roundtrip: **20/20 PASS**
- Fresh-unpack PHP lint: **15/15 PASS**
- Entire functional/negative/regression/meta suite rerun against the exact fresh-unpacked archive: **260/260 PASS**

Therefore the tested archive is byte-identical to the tested source tree, but remains an **internal non-release artifact**.

## 8. Test-harness corrections encountered

For audit completeness, two test-harness expectations required updates after intentional hardening; these were not plugin regressions:

1. The full-workflow meta test initially expected the main router diff to contain only the three adapter-registration lines. After F1/F2 the test correctly failed until its allowed diff was narrowed to the registration lines **plus the exact new Digistore runtime hardlock block**. Rerun PASS.
2. After F3 the campaign-runtime fixture initially lacked a seeded tested-key fingerprint, so even its valid Digistore banner correctly failed the new tracking gate. The fixture was corrected to represent a successfully tested connection; NEG/POS and non-Digistore regression reran PASS.

No production code was weakened to satisfy either test.

## 9. eBay live-run protection

Last user-supplied live screenshot (28.08.2026 17:35 MESZ) still showed canonical run `74b8372b-f48` **non-terminal**, stage `gapfill_select`, subphase `business_prune`, package `630`, BUSINESS sources `3264`, active/materialized `225/225`, public BUSINESS coverage `91/311` with `220` missing.

No live WordPress plugin was installed, switched, restarted or modified during this Digistore local work. No eBay run/cursor/checkpoint file is changed in the candidate.

## 10. Open release gates – release remains forbidden

Still required before any release:

1. eBay canonical run `74b8372b-f48` must reach a terminal state without manual reset.
2. New portal coverage export after eBay terminal and comparison to the prior null point.
3. Real read-only Digistore API test with the user’s existing API key.
4. Inspect real `listMarketplaceEntries` / `getMarketplaceEntry` payload; do not assume undocumented support/promolink fields.
5. Real vendor support/banner import with one genuinely approved partnership.
6. If the live payload/vendor test requires a fix: reproduce NEGATIVE, apply minimal fix, rerun POSITIVE and the **entire** workflow gate again.
7. Only then create the actual release version/installer/master and rerun final Fresh-Unpack/hash/integrity gate on those exact release artifacts.

**FINAL LOCAL STATUS: `LOCAL_HARD_PASS_PENDING_EBAY_TERMINAL_LIVE_API_VENDOR_E2E`.**  
**PLUGIN RELEASE AUTHORIZED: NO.**
