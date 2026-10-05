# Affiliate Router 6.72.188 — ADCELL promotion category route contract research

## Status
ROUTE_NAME_PROVEN_PARAMETER_CONTRACT_OPEN_NO_SOURCE_FIX_ALLOWED

## Proven live facts
- Existing live Router is 6.72.186.
- Positive control `/affiliate/promotion/getPromotionTypeBanner` GET returns HTTP 200 and the real HKM banner pool.
- Banner 322674 carries `promotionCategoryId=14727`, but the banner response carries no category name.
- `/affiliate/promotion/getPromoCategories` returns HTTP 405 with `undefined method "getPromoCategories"` on both GET and POST.
- `/affiliate/promotion/getPromotionCategories` returns HTTP 400 with `validation error` on both GET and POST under the tested parameter set.
- Therefore `getPromotionCategories` is a real ADCELL method while `getPromoCategories` is not.
- Other guessed variants tested in the bounded read-only route-family probe returned `undefined method` and are rejected.

## Official documentation research
- ADCELL exposes API v2 documentation at https://www.adcell.de/api/v2.
- The official documentation is authentication-gated and is not publicly readable without ADCELL API/account login.
- Public web and public GitHub searches did not produce an authoritative parameter contract for `getPromotionCategories`.

## Current interpretation
The transport/root cause is now narrower than before:
1. Method name in current 6.72.188 source is wrong.
2. The real method name is `getPromotionCategories`.
3. The exact required request parameters/body contract is not yet proven.
4. No source change is allowed until that validation contract is read from authenticated ADCELL documentation or otherwise directly proven without guessing.

## Release state
- 6.72.188 remains NOT RELEASEABLE.
- Existing provider-neutral `provider_topic_*` output seam remains conceptually separate and is not reverted by this evidence.
- No change to banner ranking, frontend hotpaths, AWIN, eBay, Digistore24 or Idealo is authorized.
- No more endpoint-name probing is required.
- Next work is documentation/contract research only.

## Evidence inputs
- Live ADCELL POST proof 2026-10-05T15:44:00Z.
- Live ADCELL category route-family probe 2026-10-05T15:51:05Z.
- Official ADCELL API v2 documentation entry page.


## Public research exhaustion
Research after the live route-family proof found no public authoritative parameter contract for `/affiliate/promotion/getPromotionCategories`.

- Official ADCELL API v2 documentation is reachable but authentication-gated.
- Public web search, GitHub code search and archive/cache search produced no authoritative request schema for this method.
- Public HKM/ADCELL promotion pages confirm the programme and banner inventory but do not expose the promotion-category API request schema.
- Existing live probe already received a structured validation payload: response `data` had index `0`, but the diagnostic summarizer preserved only the key and discarded the value.
- Therefore the next and only justified diagnostic step is to repeat the same already-proven `getPromotionCategories` request and preserve the existing validation detail from `data[0]`.
- This step must not try alternative parameter names, start a sync, write database state, follow tracking links, or modify production source.
