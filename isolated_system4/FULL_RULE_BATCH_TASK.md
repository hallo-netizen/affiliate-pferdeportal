# SYSTEM 4 — FULL REAL 7/7 BATCH TEST

TEST ONLY. No merge. No publish. No production write.

## Fixed input
Use exactly `isolated_system4/live_fixture/wordpress_snapshot.json` and all seven real `Beratung` items in their existing order/index 0..6.

## Hard isolation
- Follow root `AGENTS.md`, `isolated_system4/AGENTS.md`, and the current full-rule semantics already proven by `FULL_RULE_ARTICLE_TASK.md`.
- Do not import/copy/wrap/call/exec or runtime-depend on STARTMASTER, H7/H8/Single-Door, ACM, System3, legacy handoffs, runtime bridges, gates, state machines, receipt/proof/package chains, repair routes or old signers.
- Files outside `isolated_system4/**` are READ-ONLY and only for current authoritative rule/specification or pure-tool inputs already allowed by the full-rule task.
- Do not reuse old article bodies, recovery articles, old fact packs, old research, old stage proofs or old production artifacts as content sources.
- No changes outside `isolated_system4/**` from this Codex task.
- `publish_allowed=false` always.

## Before article generation
Run the current System-4 tests relevant to this branch, including current `isolated_system4/test_*.py` tests and the NO-LEGACY machine proof. Any genuine regression blocks the batch.

## One-task persistence rule
All seven article workspaces and states must exist in one parent temporary workspace in this SAME Codex task. Do not split the seven articles across separate Codex tasks.

## Per-item execution — indexes 0 through 6
For each exact real snapshot item:
1. Use the indexed System-4 ingress for that exact item. One canonical state per article.
2. Create FRESH research and FRESH facts in the temporary workspace. Do not use old article/recovery/fact content.
3. Bind the current valid production context for that article using only current authoritative rule/specification/pure-tool data permitted by System 4.
4. Generate a genuinely new German `Beratung` draft for the exact bound title and target keyword.
5. Submit through the current System-4 controller and run `fullcheck`.
6. Binding remains: current Textmaschine/content rules, actual PPM/content validator inputs, current article-level SEO/PSERC/PSTE rules already bound in System 4, mandatory table rule, exact internal-link rule, absolute external-link prohibition, real fail-closed LanguageTool, immutable metadata, publish safety, NO-LEGACY.
7. If FULL check returns a repairable FAIL, modify only the SAME draft for the exact reported first defect; resubmit and rerun FULL check. Continue until PASS or first genuine non-repairable current checker/tool blocker.
8. A passed article must remain at `phase=OUTPUT_GATE_REQUIRED`, with `checks.status=PASS`, `checks.mode=FULL_PRODUCTION`, `checks.checked_draft_sha256 == draft_sha256`, valid `production_context`, `released=false`, `release_prepared=null`, and `publish_allowed=false`.
9. Do not call BASIC check as substitute for FULL. Do not call per-article FULL release/prepare/finalize.

## After all seven FULL PASS
Run the current batch gate over the same seven live state files:

`python3 isolated_system4/batch_gate.py collect isolated_system4/live_fixture/wordpress_snapshot.json <batch-output-dir> <state0.json> <state1.json> <state2.json> <state3.json> <state4.json> <state5.json> <state6.json>`

Required result:
- `SYSTEM4_BATCH_FULL_PASS_COLLECTED`
- article_count = 7
- batch SHA = `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
- `publish_allowed=false`
- `next_required=SIGNED_WORKFLOW_RELEASE`

Do not create or fake `WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED`. System 4 has no such signing authority.

## Narrow durable proof exception — hashes only
After batch-gate PASS, persist ONLY:
`isolated_system4/batch_proof/7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a/SYSTEM4_7_7_FULL_BATCH_PROOF.json`

The proof must contain no article body, research, facts, state JSON, credentials, signatures, import package or legacy package. It must contain only:
- contract/status;
- batch SHA;
- PR/head SHA used before the run;
- seven article rows in snapshot order, each with title, plan_slot, final_draft_sha256, revision_count, check_evidence_sha256;
- System-4 test-suite result;
- NO-LEGACY result;
- batch-evidence SHA256 calculated from the temporary batch-gate evidence;
- `publish_allowed=false`;
- `next_required=SIGNED_WORKFLOW_RELEASE`.

The seven article bodies and `system4_batch_evidence.json` remain temporary task outputs and MUST NOT be committed to GitHub. GitHub persistence is proof-only.

## Mandatory remote proof persistence gate
A local Codex commit is NOT durable evidence and MUST NOT be reported as PASS.

After writing the single proof file:
1. `git add` only that proof file (plus only a separately justified minimal System-4 fix/test if required by this task).
2. Commit locally.
3. Push HEAD to exactly `hobbyroom/system4-true-single-room-v1`.
4. Run `python3 isolated_system4/proof_persistence_guard.py verify hobbyroom/system4-true-single-room-v1`.
5. Terminal batch PASS is allowed only on exact `SYSTEM4_PROOF_REMOTE_PASS:<same-local-head>`.

If push/persistence is unavailable, return `SYSTEM4_HARD_BLOCKER:REMOTE_PROOF_PERSISTENCE_UNAVAILABLE`; never claim 7/7 PASS.

## Article handoff to chat
Because article bodies are not durable GitHub proof, return the seven final article bodies to the calling chat as task output in seven clearly delimited blocks, each with title, plan_slot and final_draft_sha256. Do not truncate or substitute old article bodies. This handoff is for file assembly/preview only and is not production authority.

## Terminal return
Return only one of:

`SYSTEM4_7_7_FULL_BATCH_PASS`
with all seven titles, plan slots, final draft SHA256 values, revision counts, test-suite/NO-LEGACY results, exact batch-gate result, durable REMOTE proof path/commit, `SYSTEM4_PROOF_REMOTE_PASS:<commit>`, `publish_allowed=false`, exact next boundary `SIGNED_WORKFLOW_RELEASE_REQUIRED`, followed by the seven final article blocks;

or the first genuine non-repairable current System-4 checker/tool/persistence blocker with exact item index/title/error/source.

Do not stop for commentary or any repairable draft defect.