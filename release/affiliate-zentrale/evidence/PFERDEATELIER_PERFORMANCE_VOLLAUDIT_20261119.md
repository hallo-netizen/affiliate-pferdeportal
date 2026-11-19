# Pferdeatelier – Performance-Vollaudit 2026-11-19

Status: **VOLLAUDIT / KEINE PRODUKTIONSÄNDERUNG / KEINE NEUE DIAGNOSEVERSION FREIGEGEBEN**

## Gebundene Evidenz
- Library: `/pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_PERFORMANCE_VOLLAUDIT_20261119.md`
- SHA-256: `8722ccee7b7cd3d9f6cf04af8bb9c57a55a0cb7234f2cd10672a58bce4ef191d`
- Semantiktest: `/pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_COHORT_CACHE_SEMANTIK_20261119.json`
- SHA-256: `e857bb881d85126c41bc0689627df263f24be4f4960dd0b9198caf14bcdb86e9`

## Aktueller realer Ursachenprofil-Lauf
Performance Diagnose Safe 6.0.0, Affiliate 6.72.359, Template 1.50.616.

- /ausruestung/: Ø 3120.78 ms; the_content Ø 958.917 ms; DB Ø 606.93 ms; Cache hits Ø 55,574.
- /ausruestung/ausruestung-sattel/: Ø 5365.90 ms; the_content Ø 2326.703 ms; DB Ø 966.62 ms; Cache hits Ø 81,959.
- /ausruestung/ausruestung-sattel/pferdesaettel/: Ø 7373.52 ms; the_content Ø 5394.826 ms; DB Ø 728.92 ms; Cache hits Ø 138,129.
- OPcache ~99.11%; target frontend has 0 external HTTP ms.
- wp_footer hook Ø ~33 ms; shutdown Ø ~247 ms.

Conclusion: the deep-category delta concentrates in server-side content/PHP work, not in footer or external provider HTTP; DB alone does not explain the delta.

## Template protection
Template 1.50.616 remains protected:
- measured child-page N+1: 813 queries / 2102.67 ms -> 0.
- 721 -> 721 named functions; removed 0; one body changed.
- independent semantic simulation: 50,000 lookups + 5,000 mutation checks, 0 mismatches.

## Historical contract
6.72.171 explicitly introduced request-local reuse because category_product_1..3 often reached the expensive eBay seller/title diversity stage with the same ordered candidate set.
Snapshot A/B:
- total 1248.595 -> 249.597 ms (-80.01%)
- selected campaigns/order/candidate counts/HTML hashes identical.

6.72.176 preserved the performance path. 6.72.208 did not change ranking/product output.

## Later required behavior
6.72.226+ added legitimate product fallback/multi-provider behavior and 6.72.237 distinguishes article product-mode behavior from numbered portal product slots. These features are protected and must not be rolled back.

## Concrete lost reuse in 6.72.359
Current `ebay_filter_ranked_product_candidates_provider_cohort($candidates,$slot_type)` uses the exact slot name in its request-local cache key.

Inside this function, slot type affects output only via `ebay_product_output_mode_for_slot()`; for category_product_1, _2 and _3 that helper returns the same effective mode under all five global modes.

Thus identical category candidate lists are forced into three cache builds even though the function result is identical.

Independent simulation of cache identity `effective mode + candidate fingerprint`:
- 30,000 calls
- modes separate/combined/automatic/ebay_only/idealo_only
- 0 output mismatches
- identical category trio: 3 builds -> 1 build in all modes
- synthetic 710-candidate isolated benchmark: about 19–20 ms -> 6.7–8.1 ms.
The benchmark is not a live-server wall-time prediction.

## Not yet modified
- `multiprovider_prefer_shared_offer_cards`: possible repeated work, but no live-input proof yet.
- `product_fill_verified_portal_fallback_v672226`: contains real slot-specific gates; no blind cross-slot memoization permitted.
- DB schema/cache plugin/server config: no speculative changes.

## Diagnostic decision
6.1 is **SHELVED / DO NOT INSTALL**. 6.0 remains the diagnostic reference. No new diagnostic plugin is required by this audit.

## Next permitted production work
Only after full local gate: restore the lost request-local cohort reuse using an identity that preserves effective provider mode and exact candidate identity. No removal of 6.72.226/237 functionality. One actual Affiliate candidate only after function/hook diff, provider regressions, semantic output equality, PHP lint and ZIP integrity pass.
