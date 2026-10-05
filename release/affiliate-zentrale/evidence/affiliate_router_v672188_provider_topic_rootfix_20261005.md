# Affiliate Router 6.72.188 — provider-neutral banner topic rootfix

## Status
ROOT_CAUSE_2_PROVEN_FIX_IMPLEMENTED_GATES_OPEN

## Proven live starting point
The installed live Router 6.72.186 was diagnosed read-only on 2026-10-05.

- ADCELL promo 322674 / programme 10787 is active.
- The promotion row carries promotionCategoryId 14727.
- The old category-name request returned HTTP 405.
- Therefore the Creative-Library stored 322674 as a general banner fallback on page:95.
- Guardian promo 185797 showed the same missing category-name condition and was selected on Reithelme and Schabracken.
- No direct or inherited manual assignment caused the live result.

## 6.72.187 result and newly proven gap
6.72.187 corrected only the ADCELL category transport: getPromoCategories GET -> POST and added a one-time ADCELL resync.

Targeted transport/normalization harness: 9/9 PASS.

Further exact source inspection then proved that this was not sufficient for the live completion condition:

- automation_adcell_banner_rows() can now place the real category name into title/description/payload;
- changed source bytes reset old derived topic_targets through creative_library_upsert();
- however the productive portal_banner path calls output_banner_destination_classification();
- that path first reuses a stored edge and otherwise classifies through real destination URL;
- the output-object code contains zero consumers of promotion_category_name / promotion_category_id;
- ADCELL banner destination remains the tracking URL, so without another trusted signal the planner would fall back to the general pool again.

Therefore 6.72.187 is not a releasable fix for this incident even if its POST transport works.

## 6.72.188 provider-neutral fix
The fix does not add an ADCELL-only ranking rule.

1. Import seam
   - Provider rows may carry provider_topic_id, provider_topic_name and provider_topic_source.
   - ADCELL is the first provider to fill this seam from its official promotion category.
   - The signal is stored in the existing Creative-Library payload.
   - Banner source hashing includes this provider-topic payload so topic changes cannot be treated as unchanged source.

2. Central output seam
   - output_banner_provider_topic_classification() is provider-neutral.
   - It accepts only an explicit provider topic with a non-empty source marker.
   - It does not use fuzzy/free semantic guessing.
   - It maps only when the normalized provider topic equals exactly one allowed real portal target slug or leaf label.
   - More than one exact target => no provider-topic classification.
   - Partial word matches => no provider-topic classification.
   - On no unique exact match, the existing destination/general-fallback path remains unchanged.

3. Reimport
   - 6.72.188 has its own one-time ADCELL topic resync state/hook so an installation that already touched 6.72.187 cannot suppress the corrected reimport.
   - After each completed ADCELL programme run, the existing full-pool replanning hook is re-armed.
   - No provider HTTP is added to frontend rendering.

## Real portal target proof
Canonical portal structure contains:

- page Reithelme, slug reithelme.
- derivative categories FAQ Reithelme / reithelme-faq, Beratung Reithelme / reithelme-beratung, Vergleich, Pflege, Kosten.
- page Schabracken, slug schabracken.
- derivative categories use distinct longer names/slugs.

Thus provider topic Reithelme has one exact target: page:186.
Provider topic Schabracken has one exact target: page:193.
Derivative categories do not steal the plain product topic.

## Focused local positive/negative harness
Standalone exact-matcher harness: 8/8 PASS.

- Reithelme -> page:186 PASS.
- Schabracken -> page:193 PASS.
- missing topic -> no mapping PASS.
- missing source -> no mapping PASS.
- partial topic "Reithelm Angebote" -> no mapping PASS.
- duplicate exact target -> fail closed PASS.
- plain Reithelme is not stolen by FAQ category PASS.
- explicit "FAQ Reithelme" can match the FAQ target PASS.
- PHP syntax of the harness PASS.

## Source identity
- Candidate version: 6.72.188.
- Source file count: 27.
- Current source manifest SHA256: 5045724a7d546ea2e193538d586175a8ccb9449ab16d873a5e13d5fb85411c6c.
- All 27 current files were read back and SHA256-checked against the manifest.
- The two large JSON files that fetch_file does not return as text were checked separately through their exact Git blob contents and also match.

## Existing CI readback
Legacy banner workflows automatically triggered on the new source.

They prove only what actually ran:
- current 6.72.188 source can be packaged into a ZIP by the legacy ZIP jobs;
- those jobs then stop on their old hard-coded 6.72.182/6.72.183 source/version assertions;
- PHP lint and WordPress/MariaDB steps are skipped after that old-version failure.

No full-source PHP 21/21, WordPress/MariaDB, final ZIP or live 6.72.188 PASS is claimed from those stale workflows.

## Release gate remains open
Required before release:
1. Full current-source PHP syntax gate.
2. Full WordPress/MariaDB positive + negative banner workflow on exact 6.72.188.
3. Exact ZIP built from the proven 27-file source and fresh-unpack byte identity.
4. Same WordPress/MariaDB gate from that exact ZIP.
5. Install exact ZIP on live.
6. Wait for/execute the bounded ADCELL resync chain.
7. Read back 322674 Creative-Library provider topic and target edge.
8. Read back Reithelme page 186 and verify it no longer falls to Guardian because exact provider-topic 322674 is absent.
9. Read back Schabracken page 193 independently; no Schabracken-specific creative may be invented.

Release remains blocked until these gates pass.
