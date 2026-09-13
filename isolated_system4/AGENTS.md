# SYSTEM 4 ISOLATION — TEST ONLY

Scope: System 4 implementation only under `isolated_system4/**`.

- Do not modify anything outside `isolated_system4/`.
- Do not import/copy/wrap runtime, workers, gates, handoffs, signers, contracts or state machines from concepts 1–3.
- Historical systems may be read only as inspiration/negative evidence.
- No merge, no production publish.
- Runtime workspaces and generated article/output files must live outside the repository.
- Allowed tasks:
  1. architecture live test via `live_test.py`;
  2. first generated article test exactly per `FIRST_ARTICLE_TASK.md`;
  3. first full-rule article test exactly per `FULL_RULE_ARTICLE_TASK.md`;
  4. a real bound article batch exactly per `FULL_RULE_BATCH_TASK.md`.
- A production batch contains exactly the non-empty item set supplied by its bound metadata snapshot. System 4 has NO fixed article count and NO artificial maximum count. Any finite `1..N` batch must follow the same path; counts such as 1, 7, 25 or 1000 are regression fixtures only.
- `article_type` is input metadata, not a System-4 allowlist. System 4 MUST NOT hardcode `Beratung` or any other type as the only permitted production type. New types must flow through the same generic controller/batch/handoff path and are accepted or blocked by the unchanged authoritative type/content/design rules.
- For tasks 3 and 4 only, repository files outside `isolated_system4/**` may be read solely to identify current authoritative rule/specification content and pure tool/checker inputs. They may not be modified or used as old orchestration/runtime dependencies.
- For generated articles, the writer may create research/facts/draft only in the temporary workspace and may repair only the same canonical article body via `controller.py repair` when the controller returns `REPAIR_REQUIRED`.
- The writer may not alter immutable metadata, choose a free route, enable publish, bypass a required checker, or create a per-article FULL production release.
- For a batch run, all input items must reach a terminal accepted state before `batch_gate` may collect the batch. Processing may be sequential or bounded internally; no item may be silently dropped, duplicated or replaced.

## TEXTMASCHINE + DESIGN IMMUTABILITY HARD RULE
- The existing Textmaschine/content-rule authority is READ-ONLY. System 4 MUST NOT edit, relax, extend, reinterpret, normalize, replace or shadow Textmaschine rules, directly or indirectly.
- The current PPM 6.7.9 production package, article-type/content rules, table contract, WordPress plugin, theme/CSS and existing design selectors are READ-ONLY. No change to them is authorized by System 4.
- System 4 may only present one candidate article to the unchanged existing checks and may only PASS or BLOCK based on their already-existing contract. It must never "fix" the Textmaschine by introducing substitute writing/design rules.
- Existing design is equally immutable. System 4 MUST NOT write CSS, add inline styles, change classes, change heading levels, change table styling, change theme/plugin files, or transform article HTML after the writer produced it.
- `design_guard.py` is validation-only. It binds the supplied `article_type` generically to the existing `ppm-type-*` selector convention and validates the already-existing production/design boundary. Known type-specific constraints, such as the documented `Beratung` H2 rule, remain guards for that type only and MUST NOT become an allowlist that blocks new article types merely because System 4 has not seen them before. It performs ZERO mutation.
- The final WordPress importer receives the exact checked article bytes. Therefore no downstream stage is permitted to repair, normalize, decorate or restyle the body.
- Any future proposal that requires a Textmaschine-rule change or design change is outside System 4 and must stop as `BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE`; it must not be implemented here.

## RESEARCH -> FACTS -> ARTICLE HARD BOUNDARY
- Codex remains the single fachliche worker: it researches, creates the facts/fact pack, writes the article and performs controller-requested same-article repairs.
- No independent Chat writer or legacy worker is reintroduced.
- `RESEARCH_REQUIRED` accepts only `SYSTEM4_RESEARCH_EVIDENCE_V1`: real source title, HTTP(S) URL, retrieval time, captured evidence text and `snapshot_sha256=SHA256(evidence)`.
- `FACT_CHECK_REQUIRED` accepts only `SYSTEM4_FACTS_EVIDENCE_V1`: at least two distinct claims, each bound to an accepted research `source_id` and an exact `evidence_text_sha256`.
- The production `canonical_fact_pack_v1` must contain the same accepted source metadata and the same accepted core claims. Codex may not self-certify a source-free `SOURCE_VERIFIED_PRODUCTION_READY` fact pack.
- The production context must be bound before a FULL-production draft can pass. BASIC architecture tests remain isolated test-only and do not define the production content path.
- Every FULL-production article must carry fact traces that resolve to its bound fact pack. Unknown or missing fact IDs are BLOCKED.
- These guards do not replace or rewrite the existing Textmaschine/content rules, LanguageTool 6.8 or PPM 6.7.9; they only prevent unproven research/facts from reaching those unchanged checks.
- Multi-article batches additionally pass System-4 cross-article distinctness/repetition guards. A single-article batch is valid and skips only comparisons that mathematically require a second article.
- A repair may correct only the same article and must remain close to the previously checked body; a broad rewrite in `REPAIR_REQUIRED` is BLOCKED.

## SINGLE CHECKER ORCHESTRATOR HARD RULE
- `isolated_system4/controller.py fullcheck` is the ONLY production checker orchestrator.
- LanguageTool 6.8 and PPM 6.7.9 must be invoked only through that bound `fullcheck` path via `production_checks.run_all`.
- Do NOT run LanguageTool or PPM directly before/after `fullcheck`.
- Do NOT create or execute custom Python/shell orchestration wrappers such as `/tmp/system4_run.py` for checker sequencing.
- A repairable LanguageTool/PPM/content finding is NOT a terminal process error. The controller must return `REPAIR_REQUIRED`; repair only the same canonical article via `controller.py repair`, then rerun `fullcheck`.
- `controller.py draft` is forbidden once a state is in `REPAIR_REQUIRED`; only `controller.py repair` may accept revised body bytes for that same bound article.
- The repair transition must not mutate the bound production context, metadata, research or facts. Draft-dependent LT/PPM evidence is regenerated/rebound only inside the next `fullcheck`.
- The internal hash-bound persistent LanguageTool 6.8 worker is permitted solely as an implementation detail of `production_checks.run_all`; it must use the exact pinned LT 6.8 distribution and fail closed/fallback to the exact pinned CLI. It is not a second checker/orchestrator and may not disable or bypass any rule.
- `raise`, `exit`, task abort or batch restart for a repairable finding is forbidden.
- Only a genuine `FULL_CHECK_HARD_BLOCK`, tool/runtime failure, integrity failure or other non-repairable controller/batch-gate blocker may terminate the run.

## DIRECT PARENT-CHAT FILE HANDOFF HARD RULE
- A real production batch is NOT complete until the parent ChatGPT conversation can reconstruct and expose the exact final `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json` as a normal chat download.
- The handoff contract contains exactly the checked articles from the bound input snapshot, in input order, with count `1..N`; it has no fixed production count and no article-type allowlist.
- The user must never be asked to download anything from GitHub or from the Codex task UI.
- No repository branch, commit, push, artifact, PR-file or external storage is part of the file handoff.
- `git push`, a temporary handoff branch, repository persistence of article/output bytes, and a Codex-local `sandbox:/mnt/data/...` link are forbidden as handoff mechanisms.
- The final file MUST be valid UTF-8 JSON with contract `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` and MUST pass `handoff_transport.py validate`.
- It MUST contain every checked body, immutable WordPress metadata, `production_context` for each article, real LT 6.8 PASS evidence and real PPM 6.7.9 PASS evidence.
- The final handoff validator rechecks bound fact packs/fact traces, unchanged-design boundaries and, when count > 1, cross-article distinctness/repetition.
- The existing WordPress signature switch is currently OFF for this production path. System 4 therefore performs no signing and no ENDSTEMPEL step for the current articles.
- The exact parent-chat file is the direct WordPress upload file. It MUST state `WORDPRESS_DIRECT_IMPORT`, `direct_wordpress_upload_ready=true`, no direct-upload block reason and no downstream signing/release components.
- `publish_allowed=false` remains mandatory. Direct upload must not be confused with automatic publish.
- System 4 MUST NOT modify the WordPress plugin or its signature switch.

### Bound inline relay
- After the complete bound batch has passed, create the final JSON in canonical compact UTF-8 form and validate it.
- Run `handoff_transport.py inline-pack`. The relay uses `SYSTEM4_PARENT_CHAT_INLINE_V2` and may contain as many ordered Base64/XZ parts as required. The per-part size is bounded for transport safety; the production article count is not.
- The complete ordered relay is returned only in the normal terminal Codex completion response between the exact V2 BEGIN/END markers. It is not written to or pushed into any repository location.
- The parent Chat extracts all parts, runs `handoff_transport.py inline-unpack`, validates part order/count, compressed SHA, plaintext SHA, byte length, schema and canonical bytes, and exposes the resulting `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2.json` directly in this chat.
- Any missing/duplicate/reordered/tampered part or Base64/XZ/SHA/length/schema/canonical mismatch is `SYSTEM4_HANDOFF_FAIL`.
- No second WordPress transformation occurs after reconstruction; the reconstructed exact JSON is the file the user uploads unchanged.

## CODEX ECONOMY HARD RULE
- Codex quota is a scarce production resource.
- Do NOT invoke Codex for diagnostics, read-only inspection, architecture work, preflight repair, handoff experiments, signing experiments or WordPress work.
- Perform such work without Codex whenever technically possible.
- Before any Codex production invocation, the caller must already have verified the current System-4 entry/test suite/NO-LEGACY preflight without Codex and bound that PASS to the exact PR head SHA.
- A Codex production run MUST NOT repeat that unchanged-head preflight. If the head changes, the caller must re-run the preflight without Codex before another production invocation.
- A Codex invocation is permitted only for a REAL bound article-production run and only after explicit user approval for that new production run.
- Never require article bodies to be pasted manually, downloaded by the user, or moved through a repository branch.
- Signing/ENDSTEMPEL remain disabled for the current article output. After complete-batch PASS, relay only the V2 inline parts so the parent chat can reconstruct the exact direct WordPress JSON.
