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
