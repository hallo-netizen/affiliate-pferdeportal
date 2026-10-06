# Affiliate Router 6.72.189 — import-only destination URL rootfix

## Status
SOURCE_FIXED_LOCAL_IMPORT_SIM_PASS_RELEASE_GATES_OPEN

## User decision / KISS contract
Banner relevance uses the real destination URL as the primary reusable signal.
A destination is resolved only when a banner is new, when its tracking URL changed, or when an older banner has never passed the new URL check.
The resolved destination is persisted in the existing Creative-Library destination_url field and reused afterwards.

Hard performance/database rules:
- no frontend HTTP;
- no new frontend DB query;
- no frontend destination reclassification;
- no new table;
- no new column;
- no URL history/cache table;
- no repeated destination request for an unchanged banner;
- existing image hash/dimensions must not be invalidated merely because a derived destination URL was learned.

## Source delta
1. Creative Library has one import-only destination resolver:
   - first decodes destination parameters locally when possible;
   - otherwise uses HEAD only;
   - no response body download;
   - max four redirect hops;
   - request-local in-memory dedupe;
   - import/admin/cron/CLI/AJAX context only.
2. ADCELL banner import performs one batched read of existing banner destination/tracking/provenance rows for the programme.
3. Same tracking URL + stored resolved destination => reuse with zero destination HTTP.
4. Same tracking URL + prior tracking_checked => zero destination HTTP.
5. Old tracking_fallback/unknown rows are checked once on their next import.
6. Changed tracking URL => exactly one new bounded import-time resolution path.
7. Failed resolution stores the tracking URL plus provenance tracking_checked in the already existing payload provenance field; no extra history field is created.
8. A derived resolved destination is excluded from source freshness hashing, so learning the URL does not force image re-verification.
9. When an existing row learns a better destination, only destination/provenance and derived topic mapping state are updated; image verification evidence remains untouched.
10. ADCELL banner import no longer depends on a separate getPromotionCategories request. promotionCategoryId/name remain optional provider metadata if directly present in the banner response.
11. Output runtime treats resolved_redirect as semantic evidence and tracking_checked as non-semantic fallback. No runtime URL resolution was added.

## Local simulation
Isolated PHP import/cache simulation executed locally on 2026-10-06.

PASS cases:
- new banner => exactly 1 URL check;
- new banner => resolved merchant destination persisted;
- unchanged banner => 0 additional URL checks;
- unchanged banner => persisted destination reused;
- changed tracking URL => exactly 1 new URL check;
- new unresolvable banner => exactly 1 attempt;
- unchanged previously-unresolvable banner => 0 additional URL checks;
- frontend context => 0 HTTP checks;
- storage shape remains existing tracking_url + destination_url + provenance only;
- isolated PHP syntax harness PASS.

The simulation is not a substitute for the full WordPress/MariaDB release gate.

## Source binding
- version: 6.72.189
- source file count: 27
- source manifest SHA256: 38a02094e522ae7a565921271fe5b63c7928c433625728a8fa30009ff58b7829
- final installer: absent
- release_allowed: false

## Remaining gates
Run the normal bound source/WordPress/MariaDB/performance gates on this exact manifest, then exact ZIP/fresh-unpack/byte-identity gates, then live install + bounded ADCELL resync + public Reithelme/Schabracken readback.

The former successful-response proof for getPromotionCategories/category 14727 is no longer a release prerequisite because that extra category request is no longer in the active ADCELL banner import path.
