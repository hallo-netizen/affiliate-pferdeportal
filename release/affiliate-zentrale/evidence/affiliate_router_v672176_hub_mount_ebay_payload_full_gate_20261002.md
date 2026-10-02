# Affiliate Router 6.72.176 – hub mount and eBay card payload full gate

Date: 2026-10-02
Branch: affiliate-release-current
Workflow run: 36997283155
Targeted WordPress/MariaDB simulation run: 36997037385
Source manifest SHA-256: c01945cbd0e9aa4b107018260bfc833a8fc4f69aaee1f0e7a73f96391c2ffb4d
Final installer SHA-256: 32f7bfd0cb316ebbb0e130d0ab310019d66cdbdebe0ce6085fa0ed2f1ec0b79b

## Targeted result

- Real hub2 server mount of hub_after_cards: PASS.
- Direct hub_after_cards renderer: PASS.
- Duplicate guard: PASS.
- Empty hub slot on fresh request: PASS.
- eBay BUSINESS category/hub product-card description omitted from delivered card HTML: PASS.
- 12k synthetic long description reduced by about 12,074 bytes per tested card while title/image/price/seller/CTA remain: PASS.
- Non-eBay card descriptions preserved: PASS.
- PRIVATE eBay detail descriptions preserved: PASS.
- Existing performance hardlocks preserved: PASS.

## Full gate

- Exact delta versus released 6.72.175: PASS.
- All non-rootfix plugin files byte-identical to released 6.72.175: PASS.
- PHP lint 21/21: PASS.
- Existing provider/banner regressions: PASS.
- AF-077 target-selection regression: PASS.
- Existing frontend regression: PASS within the intentional 6.72.176 HTML-output scope.
- 6.72.170 exact-GTIN regression: PASS.
- Recovery/housekeeping regression: PASS.
- Product deals/partner analytics: PASS.
- Manual single-upload importer: PASS.
- Fresh unpack/source ZIP byte identity 27/27: PASS.
- Current frontend smoke: PASS.

FULL_BOUND_GATE_672176_HUB_EBAY_PASS
