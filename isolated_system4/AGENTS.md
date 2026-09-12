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
  4. full real 7/7 batch exactly per `FULL_RULE_BATCH_TASK.md`.
- For tasks 3 and 4 only, repository files outside `isolated_system4/**` may be read solely to identify current authoritative rule/specification content and pure tool/checker inputs. They may not be modified or used as old orchestration/runtime dependencies.
- For generated articles, the writer may create research/facts/draft only in the temporary workspace and may repair only the same canonical article body via `controller.py repair` when the controller returns `REPAIR_REQUIRED`.
- The writer may not alter immutable metadata, choose a free route, enable publish, bypass a required checker, or create a per-article FULL production release.
- Task 4 must keep all seven article states alive within one task until the System-4 batch gate has accepted the complete set.

## RESEARCH -> FACTS -> ARTICLE HARD BOUNDARY
- Codex remains the single fachliche worker: it researches, creates the facts/fact pack, writes the article and performs controller-requested same-article repairs.
- No independent Chat writer or legacy worker is reintroduced.
- `RESEARCH_REQUIRED` accepts only `SYSTEM4_RESEARCH_EVIDENCE_V1`: real source title, HTTP(S) URL, retrieval time, captured evidence text and `snapshot_sha256=SHA256(evidence)`.
- `FACT_CHECK_REQUIRED` accepts only `SYSTEM4_FACTS_EVIDENCE_V1`: at least two distinct claims, each bound to an accepted research `source_id` and an exact `evidence_text_sha256`.
- The production `canonical_fact_pack_v1` must contain the same accepted source metadata and the same accepted core claims. Codex may not self-certify a source-free `SOURCE_VERIFIED_PRODUCTION_READY` fact pack.
- The production context must be bound before the draft body is accepted.
- Every article must carry fact traces that resolve to its bound fact pack. Unknown or missing fact IDs are BLOCKED.
- These guards do not replace or rewrite the existing Textmaschine/content rules, LanguageTool 6.8 or PPM 6.7.9; they only prevent unproven research/facts from reaching those unchanged checks.
- A batch must additionally pass the System-4 cross-article distinctness check. The known 7er failure class — one reusable sentence/paragraph template across different topics — is BLOCKED before collection/handoff.
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
- A real 7/7 production run is NOT complete until the parent ChatGPT conversation can reconstruct and expose the exact final `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` as a normal chat download.
- The user must never be asked to download anything from GitHub or from the Codex task UI.
- No repository branch, commit, push, artifact, PR-file or external storage is part of the file handoff.
- `git push`, a temporary handoff branch, repository persistence of article/output bytes, and a Codex-local `sandbox:/mnt/data/...` link are forbidden as handoff mechanisms.
- The final file MUST be valid UTF-8 JSON with contract `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1` and MUST pass `handoff_transport.py validate`.
- It MUST contain the exact seven checked bodies, immutable WordPress metadata, `production_context` for each article, real LT 6.8 PASS evidence and real PPM 6.7.9 PASS evidence.
- The final handoff validator rechecks the bound fact packs/fact traces and cross-article distinctness; a previously seen source-free or template-reuse batch cannot become a valid Chat/WordPress file merely because transport hashes are correct.
- The existing WordPress signature switch is currently OFF for this production path. System 4 therefore performs no signing and no ENDSTEMPEL step for the current articles.
- The exact parent-chat file is the direct WordPress upload file. It MUST state `WORDPRESS_DIRECT_IMPORT`, `direct_wordpress_upload_ready=true`, no direct-upload block reason and no downstream signing/release components.
- `publish_allowed=false` remains mandatory. Direct upload must not be confused with automatic publish.
- System 4 MUST NOT modify the WordPress plugin or its signature switch.

### Bound inline relay
- After the seven-article batch has passed, create the final JSON in canonical compact UTF-8 form and validate it.
- Run `handoff_transport.py inline-pack` to create exactly one `SYSTEM4_PARENT_CHAT_INLINE_V1` text envelope using XZ/LZMA2 + Base64.
- The envelope is returned only in the normal terminal Codex completion response between the exact BEGIN/END markers. It is not written to or pushed into any repository location.
- The inline envelope must be at most 60000 characters or the handoff fails closed with `INLINE_ENVELOPE_TOO_LARGE`.
- The parent Chat extracts that inline envelope from the completed task result, runs `handoff_transport.py inline-unpack` locally, validates schema/SHA/length/canonical bytes, and exposes the resulting `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` directly in this chat.
- Any Base64/XZ/SHA/length/schema/canonical mismatch is `SYSTEM4_HANDOFF_FAIL`.
- No second WordPress transformation occurs after reconstruction; the reconstructed exact JSON is the file the user uploads unchanged.

## CODEX ECONOMY HARD RULE
- Codex quota is a scarce production resource.
- Do NOT invoke Codex for diagnostics, read-only inspection, architecture work, preflight repair, handoff experiments, signing experiments or WordPress work.
- Perform such work without Codex whenever technically possible.
- Before any Codex production invocation, the caller must already have verified the current System-4 entry/test suite/NO-LEGACY preflight without Codex and bound that PASS to the exact PR head SHA.
- A Codex production run MUST NOT repeat that unchanged-head preflight. If the head changes, the caller must re-run the preflight without Codex before another production invocation.
- A Codex invocation is permitted only for a REAL bound article-production run and only after explicit user approval for that new production run.
- Never require seven full article bodies to be pasted manually, downloaded by the user, or moved through a repository branch.
- Signing/ENDSTEMPEL remain disabled for the current article output. After 7/7 PASS, relay only the compact inline envelope so the parent chat can reconstruct the exact direct WordPress JSON.
