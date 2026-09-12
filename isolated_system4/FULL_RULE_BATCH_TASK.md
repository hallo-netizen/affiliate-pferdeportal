# SYSTEM 4 — REAL 7/7 ARTICLE PRODUCTION RUN

No merge. No publish. No signing in this run.

## PRECONDITION — COMPLETED WITHOUT CODEX
Before Codex is invoked, the caller must have already verified on the exact current PR head SHA:
1. `python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v` = PASS;
2. existing NO-LEGACY machine proof = PASS;
3. System-4 entry/current snapshot = clean;
4. the exact parent-chat transport has passed a real positive and negative dummy roundtrip WITHOUT Codex;
5. the WordPress handoff schema is current for Portal SEO Editorial Plan Compiler 0.28.22 / PPM 6.7.9 pre-import review;
6. the seven article bodies will not be pasted into a PR comment and will not be persisted on the production PR branch.

A Codex-task-local `sandbox:/mnt/data/...` link, a `View task` link, a filename-only PR comment or a SHA-only PR comment is NOT a parent-chat handoff.
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
- Do not modify the production PR branch during the production run. The only repository write allowed is the post-batch temporary transport exception defined below on `system4-parent-chat-handoff`.
- `publish_allowed=false` always.

## Execution path — NO CUSTOM ORCHESTRATOR
All seven article workspaces/states must exist in one temporary parent workspace in this SAME Codex task. Do not split the seven articles across tasks.

The checker path is fixed:
`controller.py ingress -> research -> facts -> context -> draft -> fullcheck -> [same-article repair -> controller.py repair -> fullcheck]* -> OUTPUT_GATE_REQUIRED`

Hard execution rules:
- `controller.py fullcheck` is the ONLY checker orchestrator.
- Do NOT call LanguageTool 6.8 directly.
- Do NOT call PPM 6.7.9 directly.
- Do NOT create or execute custom orchestration scripts/wrappers.
- Do NOT add an LT/PPM precheck before production context or before `fullcheck`.
- A normal LT/PPM/content finding must travel through the controller as `REPAIR_REQUIRED`.
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

## Mandatory handoff file — exact JSON for Chat + WordPress PREIMPORT review
Create exactly one plaintext file:
`SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json`

It must pass:
`python3 isolated_system4/handoff_transport.py validate SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json`

Exact top-level contract:
- `contract = SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1`
- `batch_sha256`
- `publish_allowed=false`
- `signing_deferred=true`
- `batch_gate_status=SYSTEM4_BATCH_FULL_PASS_COLLECTED`
- `no_legacy_status=PASS`
- `test_suite_status=PASS`
- `wordpress_review`
- exactly seven `articles` in snapshot order

`wordpress_review` must state:
- JSON / `application/json`
- intended next step `WORDPRESS_PREIMPORT_REVIEW`
- plugin `Portal SEO Editorial Plan Compiler`
- plugin version verified against `0.28.22`
- PPM version verified against `6.7.9`
- `direct_wordpress_upload_ready=false`
- block reason `REQUIRES_PSERC_IMPORT_ENVELOPE_AND_SUPERVISOR_AUTHENTICITY`
- downstream components `[fact_pack_bundle, production_plan, workflow_release]`

Each article row must contain exactly:
- index
- title
- target_keyword
- category
- article_type
- plan_slot
- final_draft_sha256
- revision_count
- exact final checked `body`
- exact immutable `production_context` containing fact_pack + production_plan_item
- real LanguageTool 6.8 PASS / zero unresolved findings
- real PPM 6.7.9 technical/content-quality/aggregate PASS

This handoff is the complete source for the following WordPress pre-import review. It is deliberately NOT falsely labelled as a direct WordPress upload package; PSERC import-envelope/Supervisor authenticity is checked/built after the parent-chat handoff.

## Mandatory parent-chat transport
After the plaintext handoff validates:
1. run `python3 isolated_system4/handoff_transport.py pack SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json SYSTEM4_PARENT_CHAT_TRANSPORT_V1.json`;
2. create/update ONLY the dedicated temporary branch `system4-parent-chat-handoff` from the exact production source head;
3. write ONLY `isolated_system4/.handoff/SYSTEM4_PARENT_CHAT_TRANSPORT_V1.json` on that branch;
4. push that transport branch; do NOT change the production PR branch;
5. report the exact transport commit SHA, exact path, plaintext SHA256, byte length and production source head.

The parent Chat will fetch exactly that commit/path, unpack it with `handoff_transport.py unpack`, recompute the resulting plaintext SHA256, and only then expose the resulting `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` as the direct ChatGPT download. After readback, the parent Chat force-resets `system4-parent-chat-handoff` to the production source head.

Invalid handoffs:
- Codex-only `sandbox:/mnt/data/...`;
- `View task` links;
- filename/SHA/task-link only;
- asking the user to manually download and re-upload;
- writing article/output transport content to the production PR branch;
- any SHA/length/schema mismatch.

## Terminal return
Return exactly one of:

`SYSTEM4_7_7_REAL_ARTICLE_BATCH_PASS`
ONLY if the seven articles and batch passed AND the transport branch push succeeded. Include transport commit SHA/path, plaintext SHA256, byte length and production source head. Parent-chat delivery is still independently verified by the caller before the overall workflow is declared complete.

or `SYSTEM4_HANDOFF_FAIL` if article/batch production succeeded but transport creation/push failed;

or the FIRST genuine non-repairable current System-4 controller/checker/tool/integrity blocker with exact stage, status/error and source.

No commentary stops. No repairable-finding stops. No signing. No WordPress. No merge. No publish.
