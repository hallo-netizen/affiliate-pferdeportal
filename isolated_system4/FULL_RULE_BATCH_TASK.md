# SYSTEM 4 — REAL 7/7 ARTICLE PRODUCTION RUN

No merge. No publish. No signing in this run.

## PRECONDITION — COMPLETED WITHOUT CODEX
This file describes a REAL production run, not a diagnostic/test-only Codex task.

Before Codex is invoked, the caller must have already verified on the exact current PR head SHA:
1. `python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v` = PASS;
2. existing NO-LEGACY machine proof = PASS;
3. System-4 entry/current snapshot = clean;
4. the exact handoff transport has been end-to-end proven WITHOUT Codex by delivering a real dummy file into the parent ChatGPT conversation and making its bytes directly downloadable there;
5. the seven article bodies will not be pasted into a PR comment and will not be persisted as ordinary repository article content.

A Codex-task-local `sandbox:/mnt/data/...` link, a `View task` link, a filename-only PR comment or a SHA-only PR comment is NOT proof of a retrievable parent-chat handoff.

If any precondition is unproven: DO NOT START CODEX.
If the PR head changes after preflight: re-run the preflight WITHOUT CODEX before any new production run.

### Codex economy consequence
The production Codex task MUST NOT rerun the unchanged-head unittest/NO-LEGACY preflight, perform architecture diagnostics, experiment with handoff transport, or redesign anything. Those tasks belong outside Codex.

## Fixed input
Use exactly `isolated_system4/live_fixture/wordpress_snapshot.json` and all seven real `Beratung` items in existing order/index 0..6.

## Hard isolation
- Follow root `AGENTS.md`, `isolated_system4/AGENTS.md`, and current full-rule semantics already proven by `FULL_RULE_ARTICLE_TASK.md`.
- Do not import/copy/wrap/call/exec or runtime-depend on STARTMASTER, H7/H8/Single-Door, ACM, System3, legacy handoffs, runtime bridges, gates, state machines, receipt/proof/package chains, repair routes or old signers.
- Files outside `isolated_system4/**` are READ-ONLY and only for current authoritative rule/specification or pure-tool inputs permitted by System 4.
- Do not reuse old article bodies, recovery articles, old fact packs, old research, old stage proofs or old production artifacts as content sources.
- Do not modify repository files during the production run.
- `publish_allowed=false` always.

## Execution path — NO CUSTOM ORCHESTRATOR
All seven article workspaces/states must exist in one temporary parent workspace in this SAME Codex task. Do not split the seven articles across tasks.

The checker path is fixed:
`controller.py ingress -> research -> facts -> context -> draft -> fullcheck -> [same-article repair -> controller.py repair -> fullcheck]* -> OUTPUT_GATE_REQUIRED`

Hard execution rules:
- `controller.py fullcheck` is the ONLY checker orchestrator.
- Do NOT call LanguageTool 6.8 directly. The controller may internally use the exact hash-bound persistent LT 6.8 worker implemented by `production_checks`; this does not relax or duplicate the LT check.
- Do NOT call PPM 6.7.9 directly.
- Do NOT create or execute custom orchestration scripts/wrappers (including `/tmp/system4_run.py`) that preflight/check/abort outside the controller.
- Do NOT add an LT/PPM precheck before production context or before `fullcheck`.
- A normal LT/PPM/content finding must travel through the controller as `REPAIR_REQUIRED`; it must never become an ad-hoc `RuntimeError`, `raise`, `exit`, batch restart or terminal task failure.
- On `REPAIR_REQUIRED`, edit only the SAME canonical article body for the exact reported first defect, submit the revised body only with `controller.py repair`, then rerun `controller.py fullcheck`. `controller.py draft` is forbidden in `REPAIR_REQUIRED`.
- Do not restart already-passed articles.
- Only a genuine non-repairable controller/tool/integrity blocker may terminate the batch.

## Per item — indexes 0..6
For each exact snapshot item:
1. indexed ingress for the exact item;
2. FRESH research and FRESH facts in temporary workspace;
3. bind current valid production context using only permitted authoritative/pure-tool data;
4. generate a genuinely new German `Beratung` draft for exact title/target keyword;
5. submit SAME draft and run controller FULL production check;
6. all quality/safety checks remain mandatory and unchanged: current content/Textmaschine rules, actual PPM 6.7.9 content validator, current SEO/PSERC/PSTE bindings, mandatory table rule, exact internal-link rule, absolute external-link prohibition, real fail-closed LanguageTool 6.8, immutable metadata, publish safety and NO-LEGACY;
7. repair only via the controller `REPAIR_REQUIRED -> controller.py repair -> fullcheck` loop above;
8. passed state must remain `phase=OUTPUT_GATE_REQUIRED`, `checks.status=PASS`, `checks.mode=FULL_PRODUCTION`, `checks.checked_draft_sha256 == draft_sha256`, valid `production_context`, `released=false`, `release_prepared=null`, `publish_allowed=false`;
9. BASIC checks never substitute FULL; never call per-article release/finalize.

## After seven FULL PASS
Run exactly one batch collection over the same seven live state files:

`python3 isolated_system4/batch_gate.py collect isolated_system4/live_fixture/wordpress_snapshot.json <batch-output-dir> <state0.json> <state1.json> <state2.json> <state3.json> <state4.json> <state5.json> <state6.json>`

Required:
- `SYSTEM4_BATCH_FULL_PASS_COLLECTED`
- article_count = 7
- batch SHA = `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
- `publish_allowed=false`

Signing / ENDSTEMPEL / WordPress release is DEFERRED.

## Mandatory handoff to parent ChatGPT conversation — ONE REAL FILE
Create exactly one file/artifact named:
`SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json`

It must contain:
- contract `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1`;
- batch_sha256;
- publish_allowed=false;
- signing_deferred=true;
- batch_gate_status;
- no_legacy_status from the head-bound preflight;
- test_suite_status from the head-bound preflight;
- exactly seven rows in snapshot order, each with index, title, target_keyword, category, article_type, plan_slot, final_draft_sha256, revision_count, exact final checked body, real LanguageTool 6.8 PASS/zero unresolved findings, and real PPM 6.7.9 technical/content-quality/aggregate PASS.

The workflow is NOT complete when Codex merely creates that file in its own sandbox.
The exact final bytes must be transferred into the parent ChatGPT conversation as a directly downloadable file without requiring the user to open GitHub/Codex, manually download elsewhere, or re-upload anything.
The parent Chat must recompute SHA256 from the received bytes and compare it to the Codex-produced SHA256.
Only after that equality check may final workflow PASS be reported.

The following are explicitly INVALID handoffs:
- `sandbox:/mnt/data/...` that works only inside the Codex task;
- `View task` links;
- PR comments containing only filename/SHA/task link;
- asking the user to manually download from Codex/GitHub and upload back into ChatGPT.

If exact produced bytes cannot be delivered to the parent ChatGPT conversation, terminal status is:
`SYSTEM4_HANDOFF_FAIL`
Article-generation or batch-gate PASS must not be promoted to final workflow PASS.

## Terminal return
Return exactly one of:

`SYSTEM4_7_7_REAL_ARTICLE_BATCH_PASS`
ONLY after the exact final JSON bytes are directly downloadable in the parent ChatGPT conversation and parent-chat SHA256 verification matches;

or `SYSTEM4_HANDOFF_FAIL` if article/batch production succeeded but parent-chat delivery did not;

or the FIRST genuine non-repairable current System-4 controller/checker/tool/integrity blocker with exact stage, status/error and source.

No commentary stops. No repairable-finding stops. No signing. No WordPress. No merge. No publish.
