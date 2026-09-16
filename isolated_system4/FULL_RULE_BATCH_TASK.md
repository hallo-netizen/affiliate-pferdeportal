# SYSTEM 4 — REAL BOUND ARTICLE BATCH PRODUCTION RUN

No merge. No publish. No signing in this run.

## PRECONDITION — COMPLETED WITHOUT CODEX
Before Codex is invoked, the caller must have already verified on the exact current PR head SHA:
1. `python3 -m unittest discover -s isolated_system4 -p 'test_*.py' -v` = PASS;
2. existing NO-LEGACY machine proof = PASS;
3. System-4 entry/current snapshot = clean;
4. the final `SYSTEM4_WORDPRESS_HANDOFF_V1` plus `SYSTEM4_PARENT_CHAT_INLINE_V2` relay have passed positive and negative local tests WITHOUT Codex;
5. the final handoff schema is bound as the direct unsigned WordPress JSON while the existing WordPress signature switch is OFF;
6. no repository branch/push/file persistence is used for article-output handoff.

A Codex-task-local `sandbox:/mnt/data/...` link, a filename-only result, a SHA-only result or asking the user to download from Codex/GitHub is NOT a parent-chat handoff.
If any precondition is unproven: DO NOT START CODEX.
If the production head changes after preflight: re-run the preflight WITHOUT CODEX before any new production run.

### Codex economy consequence
The production Codex task MUST NOT rerun the unchanged-head unittest/NO-LEGACY preflight, perform architecture diagnostics, experiment with handoff transport, signing, ENDSTEMPEL or WordPress-plugin work.

## UNIVERSAL BATCH CONTRACT — NO FIXED COUNT, NO ARTICLE-TYPE ALLOWLIST
The production input is one bound WordPress metadata snapshot supplied for this run.

Hard rules:
- Its `items` list MUST be non-empty and `item_count == len(items)`.
- The complete production batch is exactly that bound item list, in that order.
- System 4 has NO fixed article count and NO artificial maximum count. It must process any finite `1..N` input batch under the same code path.
- Counts used by tests or historic fixtures (for example 1, 7, 25, 1000) are regression examples only and MUST NOT become production limits.
- `article_type` comes from each bound input item. System 4 has NO `Beratung` allowlist and MUST NOT reject a new type merely because it has not appeared in System-4 code before.
- Type-specific content/design validity is decided by the unchanged authoritative Textmaschine/PPM/design rules for that bound type.
- No item may be dropped, duplicated, silently substituted or moved to another batch.

## TEXTMASCHINE + DESIGN ARE IMMUTABLE
This task is NOT authorization to change the existing Textmaschine or design.

Hard rules:
- Textmaschine/content-rule authority is READ-ONLY. Do not edit, relax, extend, reinterpret, normalize, replace or shadow any current Textmaschine rule.
- PPM 6.7.9 package/rules, current table contract, PSERC/PSTE rule inputs, WordPress plugin, theme/CSS and design selectors are READ-ONLY.
- Do not add a substitute authoring rule because a checker rejects a draft. Repair only the exact defect inside the same article while remaining under the unchanged current rules.
- Do not create CSS, inline styles, new design classes, alternate heading hierarchy, alternate table classes, theme/plugin changes or any downstream HTML normalization.
- Existing production markup is mandatory exactly because the importer writes the checked body unchanged. `design_guard.py` binds the supplied `article_type` generically to the existing `ppm-type-*` selector convention. Known type-specific constraints, including the documented `Beratung` H2 rule, apply only to their own type and are not a System-4 allowlist.
- `design_guard.py` performs PASS/BLOCK only and ZERO mutation. It must never repair or restyle the article.
- If satisfying System 4 would require any Textmaschine-rule or design change, terminate with `BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE` instead of changing anything.

## Bound input
Set `SNAPSHOT` to the exact bound WordPress metadata snapshot for this production run. The regression fixture `isolated_system4/live_fixture/wordpress_snapshot.json` may be used only in tests; its historical size/type mix is not the production contract.

## Hard isolation
- Follow root `AGENTS.md`, `isolated_system4/AGENTS.md`, and current full-rule semantics already proven by `FULL_RULE_ARTICLE_TASK.md`.
- Do not import/copy/wrap/call/exec or runtime-depend on STARTMASTER, H7/H8/Single-Door, ACM, System3, legacy handoffs, runtime bridges, gates, state machines, receipt/proof/package chains, repair routes or old signers.
- Files outside `isolated_system4/**` are READ-ONLY and only for current authoritative rule/specification or pure-tool inputs permitted by System 4.
- Do not reuse old article bodies, recovery articles, old fact packs, old research, old stage proofs or old production artifacts as content sources.
- Do not modify the production PR branch during the production run.
- `publish_allowed=false` always.

## Execution path — NO CUSTOM ORCHESTRATOR
All bound input items belong to one logical batch. Their workspaces/states live in one temporary parent workspace for this Codex task. They may be processed sequentially or in bounded internal windows to conserve resources, but every input item must end with its own bound state and the batch gate must receive the complete set.

The checker path for every item is fixed:
`controller.py ingress -> research -> facts -> context -> draft -> fullcheck -> [same-article repair -> controller.py repair -> fullcheck]* -> OUTPUT_GATE_REQUIRED`

Hard execution rules:
- `controller.py fullcheck` is the ONLY checker orchestrator.
- Do NOT call LanguageTool 6.8 directly.
- Do NOT call PPM 6.7.9 directly.
- Do NOT create or execute custom orchestration scripts/wrappers.
- Do NOT add an LT/PPM precheck before production context or before `fullcheck`.
- A normal LT/PPM/content finding must travel through the controller as `REPAIR_REQUIRED`.
- On `REPAIR_REQUIRED`, edit only the SAME canonical article body for the exact reported first defect, submit the revised body only with `controller.py repair`, then rerun `controller.py fullcheck`. `controller.py draft` is forbidden in `REPAIR_REQUIRED`.
- A broad rewrite in `REPAIR_REQUIRED` is forbidden and is mechanically blocked by repair-continuity checks.
- Do not restart already-passed articles.
- Only a genuine non-repairable controller/tool/integrity blocker may terminate the batch.

## Mandatory research/fact boundary — Codex does the work, controller decides progression
For every bound article Codex performs the complete fachliche chain itself. There is no Chat writer and no legacy research worker.

### Research stage
Create one JSON document with exactly the System-4 research evidence contract:
- `contract = SYSTEM4_RESEARCH_EVIDENCE_V1`
- `sources` contains the actual sources Codex researched for this article.
- Every source contains a real `source_id`, meaningful `source_title`, HTTP(S) `source_url`, `retrieved_at`, the captured source `evidence` text and `snapshot_sha256 = SHA256(evidence)`.
- Synthetic labels without an actual URL/evidence snapshot are forbidden.
- Submit this document to `controller.py research`. Do not continue unless it passes.

### Facts stage
From only the accepted research document create:
- `contract = SYSTEM4_FACTS_EVIDENCE_V1`
- at least two distinct claims;
- each claim has `fact_id`, an accepted research `source_id`, concrete `statement`, concrete `evidence_text`, and `evidence_text_sha256 = SHA256(evidence_text)`.
Submit this document to `controller.py facts`. Do not continue unless it passes.

### Production context stage
Create the current `canonical_fact_pack_v1` and production-plan item using the unchanged current fachliche specifications for the bound `article_type`. The fact pack must contain the same accepted source metadata and the same accepted core claims. `controller.py context` must bind it before any FULL-production draft can pass. A source-free/self-certified `SOURCE_VERIFIED_PRODUCTION_READY` pack is forbidden and blocks here.

## Per bound item
For each input item by its exact index:
1. indexed ingress for that exact item;
2. FRESH research and FRESH facts using the mandatory structured evidence contracts above;
3. bind current valid production context from exactly those accepted research/facts and only permitted authoritative/pure-tool data;
4. generate a genuinely new German draft for the exact bound `article_type`, title and target keyword using the unchanged current Textmaschine/content rules; article fact traces must resolve to its bound fact pack; existing production HTML/design contract must remain unchanged;
5. submit SAME draft and run controller FULL production check;
6. all quality/safety checks remain mandatory and unchanged: current content/Textmaschine rules, actual PPM 6.7.9 content validator, current SEO/PSERC/PSTE bindings, applicable table rule, exact internal-link rule, absolute external-link prohibition, real fail-closed LanguageTool 6.8, immutable metadata, unchanged design contract, publish safety and NO-LEGACY;
7. repair only via the controller `REPAIR_REQUIRED -> controller.py repair -> fullcheck` loop above;
8. passed state must remain `phase=OUTPUT_GATE_REQUIRED`, `checks.status=PASS`, `checks.mode=FULL_PRODUCTION`, `checks.checked_draft_sha256 == draft_sha256`, valid `production_context`, `released=false`, `release_prepared=null`, `publish_allowed=false`;
9. BASIC checks never substitute FULL; never call per-article release/finalize.

## After complete FULL PASS
Run exactly one batch collection over the complete set of live state files from the bound snapshot:

`python3 isolated_system4/batch_gate.py collect "$SNAPSHOT" <batch-output-dir> <state-json>...`

Required:
- `SYSTEM4_BATCH_FULL_PASS_COLLECTED`
- `article_count == item_count` from the bound snapshot
- returned batch SHA equals the bound snapshot batch SHA
- `publish_allowed=false`
- unchanged-design guard PASS on every article, with `design_mutation_performed=false`
- for count > 1, cross-article distinctness/repetition PASS; for count == 1, the same guard functions PASS without inventing a second article.

Signing / ENDSTEMPEL are NOT executed for the current article output because the existing WordPress signature switch is temporarily OFF.

## Mandatory final file — exact WordPress JSON for Chat + direct WordPress upload
Create exactly one canonical compact UTF-8 JSON file:
`SYSTEM4_WORDPRESS_HANDOFF_V1.json`

It must pass:
`python3 isolated_system4/handoff_transport.py validate SYSTEM4_WORDPRESS_HANDOFF_V1.json`

Exact top-level contract:
- `contract = SYSTEM4_WORDPRESS_HANDOFF_V1`
- `batch_sha256`
- `publish_allowed=false`
- `signing_deferred=true`
- `batch_gate_status=SYSTEM4_BATCH_FULL_PASS_COLLECTED`
- `no_legacy_status=PASS`
- `test_suite_status=PASS`
- `wordpress_review`
- `articles` = exactly the complete bound input item set in input order, count `1..N`

`wordpress_review` must state:
- JSON / `application/json`
- `intended_next_step=WORDPRESS_DIRECT_IMPORT`
- plugin `Portal SEO Editorial Plan Compiler`
- plugin version verified against `0.28.23`
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

The final handoff validator re-runs System-4 fact-pack/fact-trace and unchanged-design guards for every row and the batch distinctness/repetition guards where applicable. A bad source-free fact pack, design-drifted body or templated multi-article batch cannot be transported merely because hashes/checker status fields look valid.

This exact `SYSTEM4_WORDPRESS_HANDOFF_V1.json` is the final current batch output. The parent Chat exposes it unchanged as one download and the user uploads that same JSON unchanged to WordPress. No signature step, no design transformation and no second WordPress transformation occur in between. `publish_allowed=false` remains unchanged; upload is not auto-publish.

## Mandatory direct parent-chat inline relay — NO REPOSITORY HANDOFF
After the final JSON validates:
1. canonicalize it once with `python3 isolated_system4/handoff_transport.py canonicalize SYSTEM4_WORDPRESS_HANDOFF_V1.json SYSTEM4_WORDPRESS_HANDOFF_V1.canonical.json` and use that canonical V1 file as the definitive WordPress file;
2. run `python3 isolated_system4/handoff_transport.py inline-pack SYSTEM4_WORDPRESS_HANDOFF_V1.canonical.json SYSTEM4_PARENT_CHAT_INLINE_V2.txt`;
3. `inline-pack` produces the transport-only `SYSTEM4_PARENT_CHAT_INLINE_V2` envelope as one or many ordered JSON part rows between the V2 BEGIN/END markers. There is no production article-count limit tied to the number of relay parts;
4. return the complete ordered contents of `SYSTEM4_PARENT_CHAT_INLINE_V2.txt` verbatim in the normal terminal Codex completion response;
5. do not create any handoff branch, commit, push, repository file, artifact or external-storage copy;
6. the user performs no intermediate download.

The parent Chat extracts every V2 relay part, runs `handoff_transport.py inline-unpack`, verifies part count/order, compressed SHA, plaintext SHA, byte length, schema and canonical equality, and exposes exactly the reconstructed `SYSTEM4_WORDPRESS_HANDOFF_V1.json` as the ChatGPT download. `SYSTEM4_PARENT_CHAT_INLINE_V2` is transport only; it is never the final WordPress payload contract.

Invalid handoffs:
- any `git push`, repository branch/commit/file transport, or external-storage handoff;
- Codex-only `sandbox:/mnt/data/...`;
- filename/SHA/task-link only;
- asking the user to manually download and re-upload;
- any missing/duplicate/reordered/tampered part or Base64/XZ/SHA/length/schema/canonical mismatch;
- any content/design normalization between FULL PASS and WordPress;
- `WORDPRESS_PREIMPORT_REVIEW`;
- `direct_wordpress_upload_ready=false`;
- adding signing/ENDSTEMPEL as a current-output dependency.

## Terminal return
Return exactly one of:

`SYSTEM4_BOUND_BATCH_PASS`
ONLY if every bound input article and the complete batch passed AND the complete V2 relay is present in the same terminal completion response. Include article count, plaintext SHA256, byte length and relay part count before the relay. Parent-chat delivery is still independently verified by the caller before the overall workflow is declared complete.

or `SYSTEM4_HANDOFF_FAIL` if article/batch production succeeded but canonicalization/inline-pack failed;

or the FIRST genuine non-repairable current System-4 controller/checker/tool/integrity blocker with exact stage, status/error and source.

No commentary stops. No repairable-finding stops. No signing. No ENDSTEMPEL. No plugin changes. No Textmaschine-rule changes. No design changes. No merge. No publish. No repository handoff.
