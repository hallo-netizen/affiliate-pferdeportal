# Digistore24 rebuild – local pre-release evidence

Date: 2026-08-28
Status: LOCAL_HARD_PASS_PENDING_LIVE_API_AND_EBAY_TERMINAL
Release: NOT RELEASED / DO NOT INSTALL

## Baseline
Released V6.62.0 ZIP SHA-256: `1b154321f9731787243bb4068a7ad1df73f16837005e655e5b165a09b47ba200`
Candidate remains version 6.62.0 internally; no release version bump.

## Exact diff scope
1. NEW `includes/trait-ppar-digistore24.php`
2. CHANGED `includes/trait-ppar-output-objects.php` – Digistore24 banner-only guard only
3. CHANGED `pferdeportal-affiliate-router.php` – adapter require/use/register only

All previously protected eBay/idealo/automation/creative/provider/frontend/catalog/readme files are byte-identical to released V6.62.0.

## Local tests
- Digistore core/API/credential/automation: 72/72 PASS
- Vendor support/banner import: 52/52 PASS
- Output contract + 10 non-Digistore regression cases: 27/27 PASS
- Real provider-neutral semantic classifier fixtures: 8/8 PASS (including negative evidence-loss reproduction)
- Central automation cursor integration: 8/8 PASS
- Full plugin bootstrap: 8/8 PASS
- Full workflow static/meta gate: 41/41 PASS
- PHP lint: 15/15 PASS
- Internal staging ZIP roundtrip: file set + bytes identical, 20/20 files
- Fresh-unpack PHP lint: 15/15 PASS

Known documented regressions are covered by negative/positive fixtures: generic Digistore output leakage, provider-local WP_Error cursor starvation, semantic description loss, untested-key activation, non-approved marketplace entries, missing partnership gate, unsafe tracking/support URLs.

## Current eBay live screenshot supplied by operator
Screenshot time: 28.08.2026 16:47 local. Canonical run `74b8372b-f48` remains ACTIVE / NON-TERMINAL. Visible stage `gapfill_select`; selection subphase `business_materialize`; detailed BUSINESS catalog coverage `91/311`, `220` missing; external_tick package 591. Therefore: no plugin switch, no restart, no Digistore live install.

## Still open before release
1. eBay canonical run reaches terminal state without intervention.
2. Fresh portal coverage export after eBay terminal and comparison to previous null point.
3. Real read-only Digistore24 API test with operator key.
4. Inspect actual live `listMarketplaceEntries` / `getMarketplaceEntry` payload for support/promolink fields; no undocumented field is assumed in current code.
5. Real approved-vendor support-page/banner import test.
6. Build final versioned installer only after those gates, then rerun NEGATIVE + POSITIVE + full workflow + fresh-unpack/hash on that exact installer.

## Candidate file SHA-256 manifest
- `assets/ebay-portal-catalog-v2.json` `4eecef55a3033a4691f8a832eba5fb1657cdb15826ee47d366dccbaabfbb1fa2`
- `assets/frontend.css` `e3be38feb1ad51d1a35bf45a02f1e35381ff9796fe1d8456266cca631030b861`
- `assets/frontend.js` `6d7a9bf87f6ae3f671499a2479382db6b3268a69d7aabbca4b7e80905e5ed509`
- `assets/portal-structure-v279.json` `b86a160e6b8cf720077830422ca6b574203ce171fdc65d357fe9c6bed039c2e0`
- `includes/trait-ppar-article-plans.php` `f4c7675cf005dca85eeb0c62abc780c5bb331cfc94bff1734e42854087b769fa`
- `includes/trait-ppar-automation-suite.php` `c531d35be4bf7fed06efcd530e7c34007dc0393986ce6324c16323b8b066b2cc`
- `includes/trait-ppar-awin-programme-gate.php` `399a28ae0c3f6d934ef3393d54ad421c4ed97e9ef0de32733aba83e77eca2255`
- `includes/trait-ppar-control-contract.php` `333955301482ab0c58337976a0170c9263001268d8e43af6bc41211a654dbb83`
- `includes/trait-ppar-creative-library.php` `4b0db590f52d10695b50a95fddf64d0419771da72fbabf55eae41c4709b45638`
- `includes/trait-ppar-digistore24.php` `50f09f7a0f069bdf8f07b8f760090aa514a9f07f6fc5a5ad6a515c9420957082`
- `includes/trait-ppar-ebay-account-deletion.php` `059e086a69020d97e7f4be1044aa2dc1c45deff580f8f0002cd090293f03924b`
- `includes/trait-ppar-ebay-run.php` `f0bb63b37ac06f6896abc9d7bdc2c6f3918747ebc11bd5a7b49561efbfe304c8`
- `includes/trait-ppar-ebay.php` `c6c6a1c05766bb79af8cc6ff68ee549c1fa3ed31ac801118e601aaaecd324276`
- `includes/trait-ppar-idealo.php` `e16c9ff51df5d715f312c2c0a40e1cf3b872493e73d6972e854b0b671b699836`
- `includes/trait-ppar-network-sync.php` `b22b442c7d2087d012668d090ba8d1e4f6cc9969c6a1f5d4115b310c518e9f85`
- `includes/trait-ppar-output-objects.php` `f9f7675e6a9e3672c763f0d88b5570d8816964080b4b877600b7a39986d1d92a`
- `includes/trait-ppar-provider-intake.php` `99cf318e4399eb92ff00234350ec568f9d258bfb383da8c15edf092498638a49`
- `includes/trait-ppar-provider-registry.php` `253a22b3360d0f759f2481fb6620bb6e2b62c67dfdba0d3290b56cfab0c0d53c`
- `pferdeportal-affiliate-router.php` `94db0f20d7f789ec7fc2410a441c6146e7954058af58620ddb3a0a9d59f54712`
- `readme.txt` `0bdaf3b2689c7631b4d0d0512e3035dd83cd9dbfc19f04b61eb4fdb1aa545b9f`

## GitHub recovery payloads
The unreleased reconstructed source is persisted on staging branch `ds24-rebuild-20260828`; it is not a release branch and must not be installed.

- `includes/trait-ppar-digistore24.php.gz.b64` SHA-256 (encoded text): `45ba51dfdad88d4984c569388636cd1c03d26175600f5d87bcd11b496827097d`
- Decoding with `base64 -d | gzip -dc` reproduces `includes/trait-ppar-digistore24.php` SHA-256 `50f09f7a0f069bdf8f07b8f760090aa514a9f07f6fc5a5ad6a515c9420957082`.
- `ds24_rebuild_tests.tar.gz.b64` SHA-256 (encoded text): `13d2252a1ffd1a4fce8158385e80c29ae2a28436d1f1be8f3fb3d91b3a528f7e`.
- Two unified patches reconstruct the only two changed baseline files. Apply them only to the released V6.62.0 baseline with ZIP SHA-256 `1b154321f9731787243bb4068a7ad1df73f16837005e655e5b165a09b47ba200`.
