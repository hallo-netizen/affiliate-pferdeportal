TEMPORARY HOBBYROOM TASK ONLY. DELETE BEFORE CANDIDATE ACCEPTANCE.

SCOPE
- Work only on PR224 branch.
- No merge. No production start. No new architecture.
- Do not change Textmaschine, LanguageTool rules, PPM/PSERC/PSTE, SEO/link/table/design rules, WordPress or publish safety.

FORENSIC BASELINES
- pre-PR217 successful workflow reference: ffcd7c8dc6451236d58002939421bf9b6b489538
- PR217 merge: 7fcae6ad09e002903d44ff3800e6f22d9679d92e
- current main: 5f996d5574b5b4bb33bac917c375d9539d7bf8a8
- current real live blocker after fresh article generation: LANGUAGETOOL_UNRESOLVED_FINDINGS:47 in fachworkflow_proof_handoff.py.

ROOT-CAUSE QUESTION
Determine whether PR217 correctly removed worker self-PASS authority but accidentally moved real Fachworkflow work/correction stages out of the worker and into the aggregate checker at the wrong lifecycle position.

STAGE MATRIX
For each stage compare PRE-PR217 vs CURRENT: actual executor, correction responsibility, final validator, lifecycle position, machine evidence.
Stages: research_fact_pack; textmachine_article_type_structure; table_contract; internal_links; languagetool; ppm; pserc; pste; duplicate_cannibalization; seo; design_format; publish_safety.

THREE KISS ALTERNATIVES TO EVALUATE
A. Restore work/check boundary: worker performs existing Fachworkflow work and needed correction loops; worker never issues PASS; existing aggregate handoff remains sole PASS authority and independently verifies final result.
B. Keep current small worker; aggregate returns findings bound to the same current_item for correction by same worker, then the same aggregate check is rerun. No new room, route or controller.
C. Keep aggregate unchanged; 107007 explicitly requires worker to produce a checker-ready final article using existing bound tools/work steps before handoff, with no worker-authored stage PASS proofs.

EVALUATE EACH
- smallest change
- new architecture yes/no
- new worker freedom yes/no
- similarity to last successful workflow
- risk to other stages
- preserves worker_pass_authority=NONE
- preserves stage_proofs=[]
- preserves all_other_actions=DENY
- preserves current_item/article/batch/slot/hash bindings
- preserves publish=false and mandatory 107008

IMPLEMENTATION RULE
Only if one alternative is clearly KISS-better and needs no new architecture, implement only that smallest candidate in existing files. Otherwise make no functional change.

HARD LOCAL POSITIVE TESTS ON THE SAME FINAL HEAD
1. Realistic fresh article containing intentional LanguageTool findings can be corrected through the allowed work path.
2. Final aggregate checker executes real LanguageTool and accepts only zero unresolved findings.
3. Clean article passes aggregate.
4. Existing PPM/PSERC path remains real and bound.

HARD LOCAL NEGATIVE TESTS
1. Worker-authored PASS claim is rejected.
2. stage_proofs other than [] are rejected.
3. Article handed to final checker with remaining LT findings is rejected.
4. Wrong article/batch/slot/hash/context is rejected as before.
5. Worker navigation/state/publish attempt is rejected.
6. LanguageTool runtime/JAR/hash tamper is rejected.
7. No Fachregel may be weakened to make tests pass.

REGRESSION
- codex_current_action.py selftest
- fachworkflow_proof_handoff.py selftest
- complete existing HOBBYRAUM_M01_M33_REGRESSION.py / M01-M36 to GESAMT PASS
- existing hardlock/hardlock-base where valid on PR checkout; a main-only production preflight is not a candidate failure.

WHOLE-WORKFLOW NEGATIVE REVIEW
Before acceptance, prove for every old stage that no stage disappeared, gained duplicate/conflicting authority, or moved to a lifecycle point that prevents its original correction loop. Do not mark a stage covered unless there is machine evidence, including indirect PPM/PSERC/PSTE coverage.

FINAL REPORT ONLY
1. Root-cause thesis: confirmed / partly / rejected.
2. A/B/C evaluation with pros/cons.
3. Chosen alternative or no change.
4. Changed files.
5. Exact POS/NEG results.
6. M01-M36 result.
7. Other affected stages besides LanguageTool.
8. Full rebuild required: yes/no + one sentence.
9. New architecture or legacy baggage introduced: must be NO, otherwise BLOCK.

DELETE THIS TEMPORARY FILE BEFORE FINAL CANDIDATE ACCEPTANCE.
