# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED / isolated prototype / test only.** No merge, no production, no publish.

Current blocker: **no new Codex invocation is allowed until a real retrievable one-file batch handoff is confirmed before launch and the exact current head has passed the non-Codex preflight.**

The latest slow production attempt exposed one concrete orchestration defect outside the System-4 controller: an ad-hoc temporary wrapper ran a separate LanguageTool preflight and converted a normal repairable LT finding into `RuntimeError('LT_FINDINGS_PRE_CONTEXT')`. The core controller itself already handles `production_checks.RepairRequired` correctly as `REPAIR_REQUIRED`.

That defect is now hard-blocked by the System-4 execution contract: `controller.py fullcheck` is the only production checker orchestrator; direct LT/PPM prechecks and custom checker wrappers are forbidden; repairable findings repair only the same draft and rerun only that article; passed articles are not restarted.

No runtime, handoff, gate, state machine, signer or worker contract from concepts 1–3 is imported as System-4 orchestration. Existing domain tools may be used only as hash-bound pure validators/rule inputs.

## Current immediate goal
Produce the exact seven current `Beratung` articles through the existing System-4 path and obtain one real retrievable batch file. Article production has priority. Signing, ENDSTEMPEL and WordPress live import are deliberately deferred until after a real 7/7 article batch exists.

## Current whole path
WordPress JSON metadata batch -> same indexed ingress for item 0..N-1 -> ONE persistent canonical state per article -> research -> fact check -> draft -> `controller.py fullcheck` -> repair of the SAME draft if `REPAIR_REQUIRED` -> output gate -> 7-item batch gate -> one real batch file to Chat.

LanguageTool 6.8 and PPM 6.7.9 remain mandatory and unchanged inside the bound FULL check. No direct precheck may duplicate them outside the controller.

The later external signed workflow release / ENDSTEMPEL / WordPress envelope remains outside the currently active System-4 work and must not be pulled forward into article production.

## Authority
- Chat: start/status and file handoff only; no PASS authority.
- Writer: research/facts/draft only when the fixed phase permits it.
- Controller: only article routing/check orchestration authority; route is fixed.
- Checkers: read-only; PASS/FAIL + evidence only.
- Batch gate: read-only validation of completed article states plus deterministic evidence collection.
- External tools: data/verdict only; no route/rule/publish authority.
- `publish_allowed=false` is mandatory.

## Codex economy
Codex is reserved for one REAL bound article-production run only. Diagnostics, architecture, preflight, test-only proof, GitHub persistence experiments, handoff experiments, signing and WordPress work must not consume Codex when they can be done otherwise.

The unittest/NO-LEGACY/entry preflight must be completed without Codex and bound to the exact PR head. An unchanged-head production run must not repeat that preflight. The production task must not invent wrapper scripts, direct LT/PPM prechecks or restart already-passed articles.

Before a future Codex start, a supported real-file/artifact return path must already be confirmed. Seven full article bodies must not be returned as a giant PR comment.

## Single-room invariant
Each article identity and its immutable WordPress metadata exist once in its `state.json`. Repair changes only the same draft. Internal production stages do not pass the article through new workflow rooms/packages/receipts.

The batch boundary does not rewrite articles. It verifies that every state belongs to the same original WordPress snapshot and batch and has FULL-PASS evidence bound to the current draft hash.

## Current durable proof level
- First real `Beratung` article: full-rule PASS with real PPM 6.7.9 and LanguageTool binding; mandatory table/internal-link rules proven with positive/negative checks.
- Indexed ingress: one existing entrance can bind each of the seven current WordPress items; default remains item 0.
- Batch gate: positive/negative suite covers complete-set collection and fail-closed tamper/missing/partial/basic/publish cases.
- Repair continuity regression: explicit positive test for LT `RepairRequired -> same-draft repair -> FULL PASS`; explicit negative test for genuine tool failure -> hard fail-closed; 7-item test proves one repair causes exactly one extra FULL check and does not restart the other six articles.
- Codex economy contract regression: direct LT/PPM calls, custom checker wrappers, duplicate unchanged-head preflight and the known `LT_FINDINGS_PRE_CONTEXT` abort pattern are forbidden by the bound task/AGENTS contract.
- Obsolete one-article FULL release/finalize path: hard-blocked.
- Signature bridge remains deferred; no production/live WordPress PASS is claimed.

## Non-Codex verification performed for the speed fix
Local deterministic verification of the changed execution contract:
- positive 7/7 repair-continuity mirror: PASS; only item 2 repaired; check calls `1/1/2/1/1/1/1` = 8 total;
- genuine LanguageTool runtime failure: hard-block PASS;
- immutable metadata tamper: blocked PASS;
- execution-contract positive/negative assertions: 3/3 PASS;
- locally tested AGENTS and FULL_RULE_BATCH_TASK bytes match the committed Git blob SHAs exactly.

This proof validates the orchestration fix without spending Codex. It does **not** claim a new real LT/PPM 7/7 production PASS; that requires the later real production run.

## Not yet production PASS
A current real 7/7 System-4 batch with one retrievable output file is not yet proven. No signed workflow release, ENDSTEMPEL, WordPress-ready package, WordPress write or publish is claimed.

## NEXT ACTION
1. Do not start Codex.
2. Run/fresh-confirm the exact-head System-4 unittest + NO-LEGACY preflight without Codex.
3. Confirm a real retrievable one-file task handoff without Codex.
4. Only then launch exactly one real 7/7 Codex production run per `FULL_RULE_BATCH_TASK.md`.
5. Accept only the real file plus 7/7 FULL evidence; otherwise BLOCK.

Historical details and executed tests from the 2026-09-12 chat are recorded in `PROTOKOLL_CLOSEOUT_20260912.md`.
