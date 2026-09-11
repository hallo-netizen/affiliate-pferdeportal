# SYSTEM 4 — TRUE SINGLE ROOM

Status: isolated prototype / test only. No merge, no production, no publish.

No runtime, handoff, gate, state machine, signer or worker contract from concepts 1–3 is imported as System-4 orchestration. Existing domain tools may be used only as hash-bound pure validators/rule inputs.

## Current whole path
WordPress JSON metadata batch -> same indexed ingress for item 0..N-1 -> ONE persistent canonical state per article -> research -> fact check -> draft -> FULL production checks -> repair of the SAME draft if FAIL -> output gate.

After every article of the same WordPress batch has independently reached `OUTPUT_GATE_REQUIRED` with `FULL_PRODUCTION/PASS`, `batch_gate.py` may collect exactly the complete snapshot-bound set into one immutable batch evidence set.

The next boundary is intentionally external:

`SIGNED_WORKFLOW_RELEASE_REQUIRED`

System 4 does not forge or self-approve `WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED`, does not own the private signing key and does not claim a WordPress-ready production package before that external signed release exists.

## Authority
- Chat: start/status only.
- Writer: research/facts/draft only when the fixed phase permits it.
- Controller: only article routing authority; route is fixed.
- Checkers: read-only; PASS/FAIL + evidence only.
- Batch gate: read-only validation of completed article states plus deterministic evidence collection.
- External tools: data/verdict only; no route/rule/publish authority.
- `publish_allowed=false` is mandatory.

## Single-room invariant
Each article identity and its immutable WordPress metadata exist once in its `state.json`. Repair changes only the same draft. Internal production stages do not pass the article through new workflow rooms/packages/receipts.

The batch boundary does not rewrite articles. It verifies that every state belongs to the same original WordPress snapshot and batch, has FULL-PASS evidence bound to the current draft hash, then writes uniquely named `ARTICLE_<plan_slot>.md` evidence plus `system4_batch_evidence.json`.

## Current proof level
- First real `Beratung` article: full-rule PASS with real PPM 6.7.9 and LanguageTool binding; mandatory table/internal-link rules proven with positive/negative checks.
- Indexed ingress: one existing entrance can bind each of the seven current WordPress items; default remains item 0.
- Batch gate: local positive/negative suite PASS for complete-set collection and fail-closed tamper/missing/partial/basic/publish cases.
- Obsolete one-article FULL release/finalize path: hard-blocked.
- Existing repository hardlock CI on current branch head: PASS.

## Not yet production PASS
Six remaining current batch articles have not yet been freshly generated and FULL-checked in System 4. A valid external signed workflow release and the final WordPress production envelope/endstamp still remain outside the proven System-4 boundary. The old WXR output is retained only for the earlier BASIC architecture test and is not the current production output contract.
