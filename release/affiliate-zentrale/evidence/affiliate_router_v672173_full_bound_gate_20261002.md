# Affiliate Router 6.72.173 – exact bound full gate

Date: 2026-10-02
Branch: affiliate-release-current
Workflow run: 36986376949
Tested head: 3b9df40d5fdcdfac25ea98d886eeb11730691899
Source manifest SHA-256: e9c760bec991257fa99cc500e1dd305a5389de262baa714c1547ef036ccd821d
Test installer SHA-256: df758023fea67c6fbe71c7a5b825584d4b29fa950f74ec6a0f27c7abddc8650f
Workflow artifact id: 11217004651
Workflow artifact digest: sha256:693f3f396afbb321c44edf1f375326270516879a6995adeca223c6088d062e95

## Exact source and protected-baseline checks

- Governance/source/start binding: PASS
- Exact 6.72.172 -> 6.72.173 plugin delta: PASS
- Allowed plugin delta only: trait-ppar-ebay.php catalog validator, main version metadata, readme release line
- PHP lint: 21/21 PASS
- Protected 6.72.171/6.72.172 performance/function files byte-identical: PASS
- Main router changed only by version metadata: PASS
- eBay trait changed only inside ebay_portal_catalog(): PASS
- 6.72.170 exact-GTIN request-cache/rootfix preserved: PASS
- 6.72.171 request-local category/target/control/health/image/eBay caches preserved: PASS
- 6.72.172 housekeeping preserved: PASS
- Dynamic 6.72.173 catalog validation present: PASS

## Functional regression gates

- Existing provider and banner regressions: PASS
- WordPress 7.1.2 + MariaDB activation: PASS
- 6.72.172 -> 6.72.173 frontend query behavior byte-identical: PASS
- 6.72.170 exact-GTIN WordPress/MariaDB positive/negative gate: PASS
- Recovery sweep + housekeeping WordPress/MariaDB gate: PASS
- Product deals + partner analytics WordPress/MariaDB gate: PASS
- Manual single-upload importer WordPress/MariaDB gate: PASS
- Current frontend smoke: PASS

## Package verification

- Deterministic installer source file count: 27 PASS
- Source -> ZIP byte identity: 27/27 PASS
- Fresh-unpack PHP lint: 21/21 PASS
- ZIP integrity: PASS
- Test installer SHA-256: df758023fea67c6fbe71c7a5b825584d4b29fa950f74ec6a0f27c7abddc8650f

## Result

FULL_BOUND_GATE_672173_PASS

No plugin source was changed by the gate runner.
No previous performance optimization was removed or overwritten.
No functional reduction is authorized.

Real WordPress install/readback remains required before treating 6.72.173 as live-installed.
