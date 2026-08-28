# Affiliate-Zentrale V6.63.0 — exact pre-release staging

Status: **LOCAL HARD PASS / NOT PUBLICLY RELEASED**

Baseline installer: Affiliate-Zentrale V6.62.0, SHA-256 `1b154321f9731787243bb4068a7ad1df73f16837005e655e5b165a09b47ba200`.

Final local pre-release installer: `affiliate-zentrale_v6.63.0_EBAY_PRIVATE_GATE_DS24_PRE_RELEASE_HARD_VERIFIED.zip`, SHA-256 `1409de807518a197bbfffb46ea8360f5e956c109c9e6e1e25e6d8af667cca9ab`.

Exact plugin delta versus V6.62.0: 5 paths, 0 removed. New `includes/trait-ppar-digistore24.php`; changed `includes/trait-ppar-ebay-run.php`, `includes/trait-ppar-output-objects.php`, `pferdeportal-affiliate-router.php`, `readme.txt`. The other 15 files are byte-identical to V6.62.0.

The delta is reconstructable from the patch files in this directory plus `trait-ppar-digistore24.php.gz.b64`. Decode the latter with `base64 -d | gzip -d` and place it at `includes/trait-ppar-digistore24.php`; its uncompressed SHA-256 is `0cbea907287351e4789ae4791be2b61c604db2510775246c08e0a2499cd7166d`.

Local source tree: 33 suites / 514 assertions PASS, 0 FAIL. PHP lint 15/15. Exact final ZIP fresh-unpack: file-list + byte identity 21/21, same 33-suite runner 514/514, PHP lint 15/15.

The eBay rootfix preserves the existing run UUID and completed BUSINESS evidence and revalidates only the PRIVATE tail before the final public gate. The current live V6.62 failure signature is `private_public_gate_failed` at `public_verify`; the old full-restart button is deliberately not used.

Digistore24 remains banner-only and live-gated. Public release remains blocked until the eBay live recovery reaches terminal success, coverage is re-exported, and the real Digistore read-only API/payload/vendor-banner E2E passes.
