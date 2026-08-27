# Affiliate-Zentrale V6.60.0 – Multi-Provider idealo Final

## Binding
The existing multi-provider target contract remains authoritative. eBay is the independent existing provider; idealo is the second independent provider; Amazon remains prepared for a later adapter.

## Final behavior
- Upgrade default remains `ebay_only`; installation alone changes no existing public eBay output.
- Modes: ebay_only, idealo_only, separate, combined, automatic.
- Separate mode needs no cross-provider matching.
- Combined/automatic mode merges only on exact normalized GTIN intersection. No title/image/category/fuzzy/AI matching.
- Missing provider URL means no button.
- Provider failures are isolated; idealo refresh/API failures preserve Last-Good and do not stop eBay.
- Exact idealo public mapping is limited to Reithelme, Reitstiefel and Gerten; broad Reitbekleidung remains staged-only.
- idealo tracking timestamp placeholders are replaced only at real click time.
- Automatic refresh uses partner API metadata, feed hash, ETag/Last-Modified, 304 and 429 handling; concrete full-feed URL is never guessed.

## Real feed evidence
Feed 2747 / Adspace 568313: 515,554 rows, 0 malformed, 655 matching staged products. Exact public-map source scope 187 rows; all 187 have GTIN identity. Live V6.57 isolation proof: 655 PASS / 0 WARN.

## Regression proof
- 1,000 randomized ebay_only candidate selections identical to V6.58.
- 1,000 randomized ebay_only provider-cohort decisions identical to V6.58.
- Single-provider article and category markup byte-identical to V6.58.
- Critical workflow files byte-identical: eBay run, output objects, provider registry, frontend JS, eBay portal catalog, portal structure.
- PHP lint 14/14; fresh installer/source parity 19/19; ZIP structure PASS.

## Scope
Changed plugin files only: frontend.css, article-plans trait, eBay trait (mode guards only), idealo trait, main plugin version/wiring, readme. Designplugin untouched; eBay run/heartbeat/safe-gap workflow untouched.