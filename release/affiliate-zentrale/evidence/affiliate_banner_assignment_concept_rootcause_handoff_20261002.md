# Affiliate-Zentrale – Banner-Zuordnung Konzept-/Rootcause-Handoff – 2026-10-02

## Zweck
Durable delta record for the current Affiliate-Zentrale workstream. This file is evidence/history only, not CURRENT truth. Sole current authority remains control/release-governance/CURRENT_RELEASE.json.

## Latest user binding
Do not continue with another Schabracken-specific microfix, release gate or install attempt.
First inspect the full assignment concept and compare the failing Schabracken path with pages where banner assignment already works.
No guessing. No fix before the first exact divergence is proven.

## Authoritative current/source at closeout check
- Branch: affiliate-release-current
- Source authority: release/affiliate-zentrale/current/affiliate-portal-router/
- Source manifest: release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt
- Source file count: 27
- Candidate before this closeout delta: 6.72.180
- 6.72.180 is a version-only repack of the 6.72.179 functional code.
- release_allowed remains false.

## What happened in this chat
1. Live 6.72.176 Schabracken readback remained FAIL.
2. Historical test fixture defect was proven: the old Schabracken test forced hub2, while the real WordPress hierarchy AUSRUESTUNG > SATTEL > SCHABRACKEN is design type category.
3. 6.72.177 added a Schabracken-specific replan candidate.
4. Review of the target system found a cross-layer identity inconsistency:
   - local output target catalog stores pages as page:<ID>
   - campaigns/automation use page:<slug>
   - 6.72.177 compared those layers inconsistently.
5. 6.72.178 introduced a central ID/slug target identity resolver and real WordPress target-URL confirmation.
6. Hard negative testing found a duplicate hierarchical slug ambiguity.
7. 6.72.179 hardened the resolver fail-closed and required replacement campaign page_id equality.
8. Direct local plugin-method tests on the packaged code reported 74/74 positive/negative checks, but this is not a WordPress/MariaDB full-gate and is not a live proof.
9. 6.72.180 changed only version/release metadata so different install/proof states do not share one version number.
10. The user explicitly rejected further Klein-Klein and required a concept-level comparison before any additional fix or release gate.

## Important correction to prior work
Local helper/direct-method PASS must not be treated as proof that the complete banner assignment concept is correct.
The complete path to compare is:
creative source
-> safety/control gates
-> target evidence/classification
-> real target identity
-> design page type/context
-> slot selection
-> persisted output object
-> campaign target keys/page_id
-> runtime exact target matching
-> renderer/mount
-> final public HTML.

The comparison must use at least:
- failing real Schabracken/Schabrackendesigner path;
- one or more real pages where the same banner concept works;
- exact persisted target/campaign state for each;
- positive and negative/fail-closed states.

## Current unresolved problem
The first exact divergence between a working banner-assignment path and the failing Schabracken path has NOT yet been proven end-to-end on the current 6.72.180 source/state.
Therefore no further source fix, new version, full release-gate or install is authorized yet.

## Single next action
READ-ONLY compare the complete target-assignment chain for Schabrackendesigner/Schabracken against at least one known-working banner/page pair and identify the first exact divergence. Record concrete values at every stage. Stop at the first proven difference. No fix before that proof.

## Do not touch
- no new plugin version;
- no installer/release promotion;
- no Schabracken-only special case;
- no eBay visual resize work unless a measured performance regression is proven;
- no rollback of 6.72.171 performance hardlocks;
- no provider/eBay/Idealo/GTIN/housekeeping/render semantics changes;
- no protocol/STARTMASTER routing for this Affiliate workstream.
