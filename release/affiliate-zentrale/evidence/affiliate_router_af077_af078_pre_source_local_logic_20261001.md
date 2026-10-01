# Affiliate-Zentrale – AF-077 / AF-078 Repair Candidate Logic – Pre-Source Evidence

Date: 2026-10-01
Basis: exact current 6.72.173 source read-only diagnosis
Source manifest: e9c760bec991257fa99cc500e1dd305a5389de262baa714c1547ef036ccd821d

Status: PRE-SOURCE / ISOLATED LOCAL LOGIC PASS / NO PLUGIN SOURCE WRITE

## Protected baseline

All 6.72.170 exact-GTIN, 6.72.171 request-local performance caches and 6.72.172 housekeeping rules remain hardlocked.
No source change is authorized by this evidence alone.

## AF-078 PRIVATE candidate-gap rootfix

Current defect:
`ebay_run_verify_private_public()` skips every published listing outside an allowed candidate map before ownership/source validation.
An empty candidate map can therefore yield public=0, invalid=[] and PASS, followed by a checkpoint with empty `private_listing_ids`.

Proposed minimal behavior:
- inspect plugin-owned published eBay PRIVATE listings even when not present in the candidate map;
- a candidate-listed owned listing keeps the existing full validation behavior;
- a non-candidate owned listing that still passes the existing hard-negative/source/hash/manual/source-state/policy/route/target/freshness/end/content/image/taxonomy checks becomes `checkpoint_candidate_gap_valid_published` and blocks checkpoint commit;
- a non-candidate listing that is genuinely stale/ended/policy-blocked/manual-blocked/etc. remains allowed to stay outside the checkpoint;
- non-owned listings remain ignored;
- a genuinely empty valid inventory remains PASS.

Local PHP isolated simulation:
1. allowed valid listing -> PASS
2. empty candidate + valid published owned listing -> FAIL candidate gap
3. genuinely empty inventory -> PASS
4. stale outside candidate -> PASS
5. ended outside candidate -> PASS
6. manual-blocked outside candidate -> PASS
7. non-owned outside candidate -> PASS
8. candidate ID not published -> FAIL
9. listed valid candidate + additional valid published gap -> FAIL
10. listed candidate itself invalid -> FAIL

Result: AF078_SIM_ALL_PASS

Performance boundary:
The extra validation occurs only in canonical/background public verify, not the normal frontend hotpath.
The existing published-list bound remains max 1000/1001.

## AF-077 real-target evidence before generic domain gate

Current defect:
`output_classify_for_portal()` returns `creative_domain_signal_missing` before real portal targets are ranked.
A strong real target such as Schabrackendesigner -> Schabracken can therefore never reach its existing target evidence.

Proposed minimal behavior:
- safety remains first;
- manual veto/review remains first;
- negative creative evidence remains first and absolute;
- only when the specific creative has no generic portal-domain signal, inspect the real allowed target catalog for a strong unambiguous target edge;
- strong evidence may come from an exact destination/slug edge or a unique strong leaf-token containment such as `schabrackendesigner` -> `schabracken`;
- multiple strong target matches remain REVIEW;
- target veto/type restrictions remain unchanged;
- a strong unique real target is allowed to count as creative/domain evidence so existing downstream ranking still chooses the final target.

Local PHP isolated simulation:
- Schabrackendesigner -> Schabracken: PASS
- exact destination -> Trensen: PASS
- unrelated creative: no bypass
- ambiguous target match: no bypass
- target veto: no bypass
- wrong output target type: no bypass
- negative signal remains absolute
- manual veto remains absolute

Result: AF077_SIM_ALL_PASS

Performance check:
Current `output_portal_targets()` already has a request-local target cache (V6.72.50 timeout rootfix).
No new global DB/file/network lookup is required.
A synthetic 334-target pure target-evidence scan measured:
- 5,000 calls: 1,224.863 ms total
- approx. 0.244973 ms per call

This is only a micro-measurement of the proposed evidence scan, not a full WordPress performance gate.

## Release boundary

These are repair designs + isolated logic evidence only.
They are not a replacement for:
- exact current-source PHP lint,
- WordPress/MariaDB positive/negative regression,
- provider/banner regression,
- frontend regression,
- performance comparison,
- full bound release gate.

No plugin source was modified in this step.
