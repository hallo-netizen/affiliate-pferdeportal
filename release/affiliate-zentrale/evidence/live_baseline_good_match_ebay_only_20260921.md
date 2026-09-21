# AFFILIATE LIVE BASELINE – GOOD MATCH / EBAY ONLY

Captured: 2026-09-21T12:55:00+02:00
Source of current visual truth: user live visual check after installing 6.72.132.
No WordPress mutation performed for this capture.

## CURRENT GOOD BASELINE — PRESERVE
- Exactly 3 product cards visible.
- All 3 products are thematically appropriate / matching.
- Provider mix is wrong: all 3 visible cards are eBay.
- Idealo is not visible.
- This state MUST be preserved before any further provider-mix fix.
- Product relevance/selection quality is explicitly considered GOOD and MUST NOT regress.

## IMPORTANT SOURCE DISCREPANCY
Public indexed/search-visible page content still shows an older provider mix on at least one Reithelme page (eBay / idealo / eBay). This public indexed representation is stale relative to the user's current live visual check and MUST NOT be used as current live truth.

## CHANGE FREEZE
Before any provider-mix change:
1. Do not modify product relevance logic.
2. Do not change renderer/CSS/JS.
3. Do not delete or rebuild product inventory.
4. Do not overwrite current good eBay selections.
5. Idealo work must be additive/restorative only and must preserve three matching cards.

## PERFORMANCE
A direct external curl timing attempt from the analysis container could not resolve pferde-atelier.de and is therefore NOT a valid performance measurement.
No performance PASS/FAIL is claimed yet.
Performance must be measured through an actually reachable external path/browser or from the live server without changing WordPress state.
