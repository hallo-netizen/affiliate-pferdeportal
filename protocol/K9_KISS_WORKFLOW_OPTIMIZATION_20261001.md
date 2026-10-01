# K9 KISS workflow optimization — 2026-10-01

## Scope
Only orchestration/transport/test repetition is optimized. Article content, K9 station concept, LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL, WordPress verification and publish_allowed=false remain unchanged.

## Measured waste on the completed 16-article run
- K9 greenfield selftest: 63 completed runs, about 3191 runner-seconds total.
- K9 finalizer: 13 runs, about 1144 runner-seconds total.
- Station receiver: 9 runs, about 980 runner-seconds total.
- Write packager: 7 runs, about 97 runner-seconds total.
The dominant waste was repeated software regression/finalization work around state changes, not article writing itself.

## KISS changes
1. Full selftest is triggered by code/config changes, not runtime/state/warehouse/final-file churn.
2. In auto-chain, the full software suite runs only at explicit entry; inherited station hops do not repeat it.
3. Submission acceptance and finalization no longer rerun the generic unittest suite.
4. Writer/repair packaging runs the complete K9 writing/table preflight before accepting a draft.
5. Repair worker is bound to repair all already reported findings in one pass and may not stop after the first finding.
6. Chat worker Current/CHAT_ENTRY gains a hard exact-route lock: no supervisor actions, no code changes, all other actions denied.
7. Finalizer still runs the real PSERC -> ENDSTEMPEL -> WordPress verification path.
8. Finalizer creates runtime/CHAT_DELIVERY.json and uploads the exact verified WordPress JSON as k9-wordpress-final-json. Current STOP points to DELIVER_FINAL_WORDPRESS_FILE_IN_CHAT.

## PSERC decision
PSERC remains because it is the final integration/binding gate. What is removed is surrounding duplicate generic regression execution. The final quality path remains LT 6.8 + PPM 6.7.9 during article check and one final PSERC/ENDSTEMPEL/WordPress integration pass.

## Invariants unchanged
- RESEARCH -> WRITE -> CHECK -> REPAIR/CHECK -> PSERC -> ENDSTEMPEL -> WordPress file -> STOP.
- No quality threshold changed.
- No content rule removed.
- No publish permission enabled.
- Completed articles are not reopened.

## Writer root-cause closure
The completed 16-article history proved that the Writer had K9/editorial rules, but several exact PPM 6.7.9 authoring constraints only became visible after the article was written. This caused avoidable write -> check -> repair loops and allowed repair passes to create new downstream PPM findings.

K9 now extracts the exact authoring authority directly from the unchanged, hash-bound PPM 6.7.9 package before every WRITE and REPAIR job:
- exact content-structure-language contract;
- exact article-type definition;
- exact static PPM constants;
- exact derived table-value/source-trace requirements;
- exact PPM package SHA-256.

The bound rule object is hash-sealed into the job input and the packager fails closed if it is missing or changed. No PPM rule, threshold, content rule or quality gate is altered. This is earlier rule visibility, not a replacement checker and not a second PPM execution.

## Intake duplicate removed
The intake workflow previously ran the full software unittest suite and then immediately dispatched the station receiver, which ran the same suite again at explicit production entry. Intake now performs intake only; the existing receiver keeps the single explicit start regression check. No production or quality gate is removed.

## Chat-switch drift closure
The route lock is now present in every chat-sensitive state:
- active worker job: execute only the exact bound runtime job;
- automatic transition: system routing only, no supervisor/code/repair authority;
- failed finalizer: report the blocker only, no implicit repair authority;
- successful STOP: deliver the verified WordPress file in chat only.

A finalizer failure can therefore no longer silently turn the next chat into a system-repair session. A repair requires a new explicit user instruction.

## Current authority aligned
The already completed 16-article STOP was still carrying the obsolete next action RUN_ONE_CLEAN_AUTO_CHAIN_CONFIRMATION_WITHOUT_MIDRUN_FIXES. It is now aligned to terminal delivery only:
- next action: DELIVER_FINAL_WORDPRESS_FILE_IN_CHAT;
- code/supervisor/repair authority: denied;
- all other actions: denied;
- exact final file/hash/article count retained unchanged.

## Green evidence
- KISS duplicate-loop removal commit: ebc3cc304025e28d6fc46a6420f1e2d5537497f5 — selftest run 36787389250 SUCCESS.
- Exact hash-bound PPM 6.7.9 authoring rules before WRITE/REPAIR: 0d428c33d90eef4c1f0b615df9b59091c19beb8a — selftest run 36788030881 SUCCESS.
- Duplicate intake regression removal: 923b997da8c91efdca212634d4cc69bcab88596f — selftest run 36788193650 SUCCESS.
- Hard route lock for all chat-sensitive states: f6ee65716a7ad245115ed6ad5787abbb2103c9a1 — selftest run 36788384493 SUCCESS.
- Terminal Current aligned to chat-delivery-only: c705794b9988ce619ecace77e03563dc4b6f3f6f.

All green selftests include the unchanged K9 transition contract, PPM 6.7.9 regressions, PSERC negative/positive regression, terminal truth/fact traces and runtime-entry validation.

## WordPress handoff root cause and fix
The repeated WordPress failure was not an article failure and not a PSERC content failure. K9 delivered the signed ENDSTEMPEL package (PSERC_APPROVED_PRODUCTION_PACKAGE_V1) as the user-facing WordPress file. The existing K9 WordPress verifier only proved that the ENDSTEMPEL package contained WordPress-ready article data; it did not prove that the outer uploaded file matched the importer contract.

Error history confirms the distinction:
- PSERC_APPROVED_PRODUCTION_PACKAGE_V1 was rejected immediately with PSERC_SYSTEM4_CONTRACT_INVALID.
- SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2 was also rejected immediately.
- The proven 0.28.27 exporter in concept_agent/konzept8_verbot/engine/k8_wordpress_export.py emits SYSTEM4_WORDPRESS_HANDOFF_V1.

K9 now preserves the ENDSTEMPEL package unchanged as signed evidence and adds one deterministic final transport adapter:
ENDSTEMPEL package -> SYSTEM4_WORDPRESS_HANDOFF_V1 -> chat/download.

The adapter copies the already-final article bytes, metadata, fact pack and production-plan item without rewriting content. It binds the actual ledger revision count, exact body SHA-256, LT PASS, PPM 6.7.9 PASS, plugin version 0.28.27 and publish_allowed=false. The terminal receipt and chat delivery now point to the SYSTEM4_WORDPRESS_HANDOFF_V1 file; the signed ENDSTEMPEL file remains separately referenced as evidence.

## Editorial rule added after user review — post-table recap
Applies only to future WRITE/REPAIR output; the already imported 16-article batch is not changed.

Directly after the single article table and before the table section closes:
- exactly one short prose paragraph;
- 1–2 sentences;
- 12–35 words;
- briefly reflect/summarize the table;
- no new facts;
- not a second conclusion.

The rule is writer-visible in contracts/K9_WRITING_RULES.json and fail-closed in k9_write_packager.py before a draft can be accepted.

## KISS phase 2 — PSERC and compact handoffs
PSERC no longer executes LanguageTool 6.8 or the PPM 6.7.9 content validator a second time after CHECK PASS. It verifies the immutable article hash against the stored LT/PPM/writing PASS evidence, verifies fact/source traces, scope, plan_slot/canonical identity and category, and reuses the already bound evidence for ENDSTEMPEL. No article content is rewritten.

WordPress -> K9 accepts the compact PSERC_TEXTMACHINE_METADATA_BATCH_V2 directly. The historical full snapshot remains backward-compatible only.

K9 -> WordPress emits PFERDE_ATELIER_WORDPRESS_IMPORT_V1 with only article_id, plan_slot, title, slug, target_keyword, category, article_type and body, plus minimal batch/count/publish metadata. The signed ENDSTEMPEL package remains internal evidence.
\n

## PSERC immutable-article prerequisite closed
Historical evidence showed one completed article (plan slot 5999b9b0...) had two facts (PH_F3/PH_F4) whose real source carried the legacy source id TEST_REITBET. The writer packager deliberately skipped trace insertion for placeholder-looking source IDs, and old PSERC later inserted those traces.

Future WRITE/REPAIR packaging now binds traces for every bound research fact before LT/PPM, including legacy TEST_/dummy/example/placeholder source IDs when they resolve to a real bound source. PSERC uses the same source-label rule and only verifies; it never repairs or mutates article content. The PSERC scope regression now uses one immutable real article fixture that already satisfies this prerequisite instead of the historical mixed 16-article batch.

