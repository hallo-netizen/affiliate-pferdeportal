# SYSTEM 4 — TRUE SINGLE ROOM

Status: **BLOCKED / isolated prototype / test only.** No merge, no production publish.

## Current blocker
The real 7/7 article generation and batch gate completed successfully on head `eaa83db95c4f40e345114696ed96596b6b920912`, but the required parent-ChatGPT file handoff FAILED.

Codex produced `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` and reported SHA256 `7dd9d71d9096c89a7538c2deed4dd845b2ff8980b51617c7600b81fc2f64428f`, but exposed it only through a Codex-task-local `sandbox:/mnt/data/...` reference. Those exact bytes were not directly downloadable in the parent ChatGPT conversation. Therefore the overall workflow is NOT PASS.

No new Codex production run is allowed until the exact handoff transport is proven end-to-end WITHOUT Codex by delivering a real dummy file directly into the parent ChatGPT conversation and verifying its bytes there.

## Current whole path
WordPress JSON metadata batch -> indexed ingress item 0..6 -> one persistent canonical state per article -> research -> facts -> draft -> `controller.py fullcheck` -> same-article `controller.py repair` when required -> `fullcheck` -> output gate -> 7-item batch gate -> exact one-file parent-chat handoff -> parent-chat SHA256 verification -> only then workflow PASS.

## Hard handoff invariant
- Codex task-local sandbox link = FAIL.
- `View task` link = FAIL.
- PR filename/SHA/task-link only = FAIL.
- Asking the user to manually download elsewhere and re-upload into ChatGPT = FAIL.
- Final PASS requires the exact generated JSON bytes to be directly downloadable in the parent ChatGPT conversation and their SHA256 to match the Codex-produced SHA256.

This requirement is bound in `AGENTS.md`, `FULL_RULE_BATCH_TASK.md`, and regression-tested by `test_codex_economy_contract.py`.

## Article/checker state
The real run reached terminal article/batch production PASS before the handoff boundary. LanguageTool 6.8, PPM 6.7.9, metadata/publish/link/content gates and batch integrity remained mandatory. No WordPress import or publish was performed.

## Codex economy
Codex is reserved for real bound article production only. Diagnostics, architecture, preflight, handoff experiments, signing and WordPress work must not consume Codex when they can be performed outside Codex.

Before another real Codex run:
1. prove the exact parent-chat downloadable-file transport WITHOUT Codex;
2. run the exact-head System-4 test/NO-LEGACY preflight WITHOUT Codex;
3. only then permit another production run.

## NEXT ACTION
Repair and prove only the parent-chat handoff transport without regenerating articles and without spending Codex. Until that is proven, status remains `SYSTEM4_HANDOFF_FAIL` / BLOCKED.
