# SYSTEM 4 — REAL 7/7 ARTICLE PRODUCTION RUN

No merge. No publish. No signing in this run.

## PRECONDITION — BEFORE CODEX IS STARTED
This file describes a REAL production run, not a diagnostic/test-only Codex task.

The caller must verify BEFORE invoking Codex:
1. current System-4 entry/preflight is clean without Codex;
2. one supported, real, retrievable task file/artifact can be returned to Chat at the end;
3. the seven article bodies will NOT be pasted into a PR comment and will NOT be persisted as repository article content.

If the real-file/artifact handoff is not confirmed, DO NOT START CODEX. Do not spend Codex quota to discover or debug the handoff.

## Fixed input
Use exactly `isolated_system4/live_fixture/wordpress_snapshot.json` and all seven real `Beratung` items in their existing order/index 0..6.

## Hard isolation
- Follow root `AGENTS.md`, `isolated_system4/AGENTS.md`, and the current full-rule semantics already proven by `FULL_RULE_ARTICLE_TASK.md`.
- Do not import/copy/wrap/call/exec or runtime-depend on STARTMASTER, H7/H8/Single-Door, ACM, System3, legacy handoffs, runtime bridges, gates, state machines, receipt/proof/package chains, repair routes or old signers.
- Files outside `isolated_system4/**` are READ-ONLY and only for current authoritative rule/specification or pure-tool inputs already allowed by the full-rule task.
- Do not reuse old article bodies, recovery articles, old fact packs, old research, old stage proofs or old production artifacts as content sources.
- Do not modify repository files during the production run.
- `publish_allowed=false` always.

## Preflight — exactly once before generation
Run:
`python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v`

Also run the existing NO-LEGACY machine proof. If either fails, return the exact genuine blocker. Do not redesign or repair unrelated architecture inside this Codex run.

## One real production task
All seven article workspaces/states must exist in one temporary parent workspace in this SAME Codex task. Do not split the seven articles across separate tasks.

For indexes 0..6, in snapshot order:
1. Use the indexed System-4 ingress for the exact item.
2. Create FRESH research and FRESH facts. Never use old article/recovery/fact content.
3. Bind the current valid production context using only current authoritative rule/specification/pure-tool data permitted by System 4.
4. Generate a genuinely new German `Beratung` draft for the exact bound title and target keyword.
5. Submit the SAME draft through the current System-4 controller and run FULL production check.
6. Required real bindings remain: current content/Textmaschine rules, actual PPM 6.7.9 content validator, current article-level SEO/PSERC/PSTE rules already bound in System 4, mandatory table rule, exact internal-link rule, absolute external-link prohibition, real fail-closed LanguageTool 6.8, immutable metadata, publish safety and NO-LEGACY.
7. On a repairable FAIL, edit only that SAME draft for the exact reported defect and rerun the same checker. Continue until PASS or the first genuine non-repairable checker/tool blocker.
8. A passed article must remain `phase=OUTPUT_GATE_REQUIRED`, `checks.status=PASS`, `checks.mode=FULL_PRODUCTION`, `checks.checked_draft_sha256 == draft_sha256`, valid `production_context`, `released=false`, `release_prepared=null`, `publish_allowed=false`.
9. Never substitute BASIC checks and never call per-article release/finalize.

## After seven FULL PASS
Run the existing batch gate over the same seven state files:

`python3 isolated_system4/batch_gate.py collect isolated_system4/live_fixture/wordpress_snapshot.json <batch-output-dir> <state0.json> <state1.json> <state2.json> <state3.json> <state4.json> <state5.json> <state6.json>`

Required:
- `SYSTEM4_BATCH_FULL_PASS_COLLECTED`
- article_count = 7
- batch SHA = `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
- `publish_allowed=false`

Signing / ENDSTEMPEL / WordPress release is deliberately DEFERRED and must not be attempted in this run.

## Mandatory handoff to Chat — ONE REAL FILE
Create exactly one file/artifact named:
`SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json`

It must contain:
- contract `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1`;
- batch_sha256;
- publish_allowed=false;
- signing_deferred=true;
- batch_gate_status;
- no_legacy_status;
- test_suite_status;
- exactly seven article rows in snapshot order, each with index, title, target_keyword, category, article_type, plan_slot, final_draft_sha256, revision_count, exact final checked article body verbatim, real LanguageTool 6.8 PASS/zero unresolved findings, and real PPM 6.7.9 technical/content-quality/aggregate PASS.

Return the supported retrievable file/artifact reference plus its SHA256 only. Do NOT paste the seven full article bodies into the PR conversation. Do NOT commit the article bodies to the repository.

## Terminal return
Return exactly one of:

`SYSTEM4_7_7_REAL_ARTICLE_BATCH_PASS`
with the retrievable `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` file/artifact reference and SHA256;

or the FIRST genuine non-repairable current System-4 preflight/checker/tool blocker with exact stage, error/status and source.

Do not stop for commentary or repairable article defects. No signing. No WordPress work. No merge. No publish.
