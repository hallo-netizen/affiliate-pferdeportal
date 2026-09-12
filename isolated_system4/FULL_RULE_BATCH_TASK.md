# SYSTEM 4 — REAL 7/7 ARTICLE PRODUCTION RUN

No merge. No publish. No signing in this run.

## PRECONDITION — COMPLETED WITHOUT CODEX
Before Codex is invoked, the caller must have already verified on the exact current PR head SHA:
1. `python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v` = PASS;
2. existing NO-LEGACY machine proof = PASS;
3. System-4 entry/current snapshot = clean;
4. the direct parent-chat inline handoff has passed positive and negative local tests WITHOUT Codex;
5. the final handoff schema is bound as the direct unsigned WordPress JSON while the existing WordPress signature switch is OFF;
6. no repository branch/push/file persistence is used for article-output handoff.

A Codex-task-local `sandbox:/mnt/data/...` link, a filename-only result, a SHA-only result or asking the user to download from Codex/GitHub is NOT a parent-chat handoff.
If any precondition is unproven: DO NOT START CODEX.
If the production head changes after preflight: re-run the preflight WITHOUT CODEX before any new production run.

### Codex economy consequence
The production Codex task MUST NOT rerun the unchanged-head unittest/NO-LEGACY preflight, perform architecture diagnostics, experiment with handoff transport, signing, ENDSTEMPEL or WordPress-plugin work.

## Fixed input
Use exactly `isolated_system4/live_fixture/wordpress_snapshot.json` and all seven real `Beratung` items in existing order/index 0..6.

## Hard isolation
- Follow root `AGENTS.md`, `isolated_system4/AGENTS.md`, and current full-rule semantics already proven by `FULL_RULE_ARTICLE_TASK.md`.
- Do not import/copy/wrap/call/exec or runtime-depend on STARTMASTER, H7/H8/Single-Door, ACM, System3, legacy handoffs, runtime bridges, gates, state machines, receipt/proof/package chains, repair routes or old signers.
- Files outside `isolated_system4/**` are READ-ONLY and only for current authoritative rule/specification or pure-tool inputs permitted by System 4.
- Do not reuse old article bodies, recovery articles, old fact packs, old research, old stage proofs or old production artifacts as content sources.
- Do not modify the production PR branch during the production run.
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

Signing / ENDSTEMPEL are NOT executed for the current article output because the existing WordPress signature switch is temporarily OFF.

## Mandatory final file — exact JSON for Chat + direct WordPress upload
Create exactly one canonical compact UTF-8 JSON file:
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
- `intended_next_step=WORDPRESS_DIRECT_IMPORT`
- plugin `Portal SEO Editorial Plan Compiler`
- plugin version verified against `0.28.22`
- PPM version verified against `6.7.9`
- `direct_wordpress_upload_ready=true`
- `direct_upload_block_reason=null`
- `required_downstream_components=[]`

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

This exact file is the final current article output. The parent Chat exposes it unchanged as one download and the user uploads that same JSON unchanged to WordPress. No signature step and no second WordPress transformation occur in between. `publish_allowed=false` remains unchanged; upload is not auto-publish.

## Mandatory direct parent-chat inline relay — NO REPOSITORY HANDOFF
After the final JSON validates:
1. canonicalize it once with `python3 isolated_system4/handoff_transport.py canonicalize SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.canonical.json` and use that canonical file as the definitive WordPress file;
2. run `python3 isolated_system4/handoff_transport.py inline-pack SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.canonical.json SYSTEM4_PARENT_CHAT_INLINE_V1.txt`;
3. return the complete contents of `SYSTEM4_PARENT_CHAT_INLINE_V1.txt` verbatim in the normal terminal Codex completion response;
4. do not create any handoff branch, commit, push, repository file, artifact or external-storage copy;
5. the user performs no intermediate download.

The parent Chat extracts the exact BEGIN/END envelope from the completed task result, runs `handoff_transport.py inline-unpack` locally, verifies SHA256/length/schema/canonical equality, and exposes exactly the reconstructed `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` as the single ChatGPT download.

Invalid handoffs:
- any `git push`, repository branch/commit/file transport, or external-storage handoff;
- Codex-only `sandbox:/mnt/data/...`;
- filename/SHA/task-link only;
- asking the user to manually download and re-upload;
- any Base64/XZ/SHA/length/schema/canonical mismatch;
- `WORDPRESS_PREIMPORT_REVIEW`;
- `direct_wordpress_upload_ready=false`;
- adding signing/ENDSTEMPEL as a current-output dependency.

## Terminal return
Return exactly one of:

`SYSTEM4_7_7_REAL_ARTICLE_BATCH_PASS`
ONLY if the seven articles and batch passed AND the complete inline envelope is present in the same terminal completion response. Include plaintext SHA256 and byte length before the envelope. Parent-chat delivery is still independently verified by the caller before the overall workflow is declared complete.

or `SYSTEM4_HANDOFF_FAIL` if article/batch production succeeded but canonicalization/inline-pack failed;

or the FIRST genuine non-repairable current System-4 controller/checker/tool/integrity blocker with exact stage, status/error and source.

No commentary stops. No repairable-finding stops. No signing. No ENDSTEMPEL. No plugin changes. No merge. No publish. No repository handoff.
