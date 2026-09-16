# SYSTEM 4 ISOLATION — TEST ONLY

Scope: System 4 implementation only under `isolated_system4/**`.

- Do not modify anything outside `isolated_system4/` except the authoritative Campus/control/protocol files required for status, audit and handoff documentation.
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
- For tasks 3 and 4 only, repository files outside `isolated_system4/**` may be read solely to identify current authoritative rule/specification content and pure tool/checker inputs. They may not be used as old orchestration/runtime dependencies.
- For generated articles, the bound worker may create research/facts/draft only in the temporary workspace and may repair only the same canonical article body via `controller.py repair` when the controller returns `REPAIR_REQUIRED`.
- The worker may not alter immutable metadata, choose a free route, enable publish, bypass a required checker, or create a per-article FULL production release.
- For a batch run, all input items must reach a terminal accepted state before `batch_gate` may collect the batch. Processing may be sequential or bounded internally; no item may be silently dropped, duplicated or replaced.

## SINGLE-BUTTON START-TO-FILE ACCEPTANCE HARD RULE

The complete acceptance route is fixed and machine-enforced:

`Parent/Chat → Point-0 → Root → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → vollständige Textmaschine → Repair → Batch → Handoff → Datei`

- Only `start-point0` is a valid acceptance entry.
- `root_entry start`, `start-stdin`, direct Controller entry, direct Worker entry and every entry behind Point-0/Root/Supervisor are BLOCKED for complete acceptance.
- The Controller alone determines the next permitted step. A caller/worker/test MUST NOT freely choose, skip, reorder or synthesize a later phase.
- The acceptance test uses the bound deterministic **Testworker only**. It MUST NOT call `codex_entry.py` and MUST NOT start a Codex model.
- Production may use Codex as the fachliche worker under the separate production target/approval rules; this does not authorize Codex in the acceptance test.
- The Testworker MUST validate the current Point-0 → Root → Supervisor → `worker_dispatch` binding before reading article work state or generating research/facts/draft bytes.
- A test that starts behind any mandatory boundary, injects a prepared Controller state, fabricates a receipt or skips a mandatory station is a component/regression test only and MUST NOT be reported as complete start-to-file PASS.
- A deterministic Testworker may replace the live production writer only at the already bound Worker interface. It MUST NOT replace Point-0, Root, Supervisor, Controller, machine bindings, real LanguageTool/PPM, Batch, Handoff or file delivery.
- Every change to critical System-4 runtime or its acceptance route MUST rerun the complete positive/negative protection ring and the full real-tool corridor on the exact resulting remote head before that head can be called PASS.

## FRESH ARTICLE PER E2E RUN HARD RULE

- Every complete End-to-End acceptance run MUST create a genuinely new article during that run.
- No prepared article body, frozen candidate, recovery article, fixture body or article body from a prior run may be used as the E2E article.
- The Testworker generation proof MUST bind the body to the current run identity and the current bound research/facts/context/authoring contract.
- Known historical/recovery/fixture body hashes are BLOCKED.
- Reusing the same generated body twice in the same run is BLOCKED.
- A static topic/body that was once fresh MUST NOT silently become the next run's fresh article. Freshness is a per-run machine property, not a filename or prose claim.
- Freshness guards are acceptance requirements; bypass or missing freshness proof is test FAIL.

## TEXTMASCHINE + DESIGN IMMUTABILITY HARD RULE

- The existing Textmaschine/content-rule authority is READ-ONLY. System 4 MUST NOT edit, relax, extend, reinterpret, normalize, replace or shadow Textmaschine rules, directly or indirectly.
- The current PPM 6.7.9 production package, article-type/content rules, table contract, WordPress plugin, theme/CSS and existing design selectors are READ-ONLY. No change to them is authorized by System 4.
- System 4 may only present one candidate article to the unchanged existing checks and may only PASS or BLOCK based on their already-existing contract. It must never "fix" the Textmaschine by introducing substitute writing/design rules.
- Existing design is equally immutable. System 4 MUST NOT write CSS, add inline styles, change classes, change heading levels, change table styling, change theme/plugin files, or transform article HTML after the writer produced it.
- `design_guard.py` is validation-only. It binds the supplied `article_type` generically to the existing `ppm-type-*` selector convention and validates the already-existing production/design boundary. Known type-specific constraints remain guards for that type only and MUST NOT become a hardcoded allowlist.
- The final WordPress importer receives the exact checked article bytes. Therefore no downstream stage is permitted to repair, normalize, decorate or restyle the body.
- Any proposal requiring a Textmaschine-rule change or design change is outside System 4 and must stop as `BLOCKED_TEXTMASCHINE_OR_DESIGN_IMMUTABLE`; it must not be implemented here.

## TEXTMASCHINE DETAIL-COVERAGE ACCEPTANCE HARD RULE

- A wrapper PASS, a sample of rules or a count of green test files is NOT proof of full Textmaschine coverage.
- The exact SHA-bound PPM 6.7.9 package is the rule/test authority for the PPM portion of the Textmaschine.
- Its current hard-rule registry contains 557 registered rules and its coverage matrix contains 557 mappings. Acceptance MUST fail closed if registry and matrix do not match exactly.
- Every registered rule MUST resolve to its specified positive original test and negative original test. `UNKNOWN`, `UNMAPPED`, `UNTESTED`, missing test file, skipped original test or failed original test is acceptance FAIL.
- Every original `test-*.php` in the bound PPM package is mandatory. System 4 MUST NOT replace an original test with a local substitute and MUST NOT silently exclude a red original test.
- Each original PPM test MUST execute in a fresh byte-identical extraction of the exact pinned PPM package so a mutating negative test cannot contaminate a later test.
- If an original test requires a package-defined runner/bootstrap/baseline/signature context, the acceptance runner MUST reproduce that original context; it MUST NOT modify, weaken or patch the original test/rule to make it green.
- Full Textmaschine PASS may be claimed only after all mandatory detail gates and their positive/negative proofs have actually executed successfully in the current run.

## RESEARCH → FACTS → ARTICLE HARD BOUNDARY

- Production Codex and the acceptance Testworker occupy the same single fachliche Worker interface; the acceptance Testworker does not create a second workflow route.
- No independent Chat writer or legacy worker is reintroduced.
- `RESEARCH_REQUIRED` accepts only `SYSTEM4_RESEARCH_EVIDENCE_V1`: real source title, HTTP(S) URL, retrieval time, captured evidence text and `snapshot_sha256=SHA256(evidence)`.
- `FACT_CHECK_REQUIRED` accepts only `SYSTEM4_FACTS_EVIDENCE_V1`: at least two distinct claims, each bound to an accepted research `source_id` and an exact `evidence_text_sha256`.
- The production `canonical_fact_pack_v1` must contain the same accepted source metadata and the same accepted core claims. A worker may not self-certify a source-free `SOURCE_VERIFIED_PRODUCTION_READY` fact pack.
- The production context must be bound before a FULL-production draft can pass. BASIC architecture tests remain isolated test-only and do not define the production content path.
- Every FULL-production article must carry fact traces that resolve to its bound fact pack. Unknown or missing fact IDs are BLOCKED.
- These guards do not replace or rewrite existing Textmaschine/content rules, LanguageTool 6.8 or PPM 6.7.9; they only prevent unproven research/facts from reaching those unchanged checks.
- Multi-article batches additionally pass System-4 cross-article distinctness/repetition guards. A single-article batch is valid and skips only comparisons that mathematically require a second article.
- A repair may correct only the same article and must remain close to the previously checked body; a broad rewrite in `REPAIR_REQUIRED` is BLOCKED.

## SINGLE CHECKER ORCHESTRATOR HARD RULE

- `isolated_system4/controller.py fullcheck` is the ONLY production checker orchestrator.
- LanguageTool 6.8 and PPM 6.7.9 must be invoked only through that bound `fullcheck` path via `production_checks.run_all` for the real article corridor.
- Do NOT create a second checker/orchestrator for the real article path.
- The original PPM internal test suite may be executed as an acceptance pre-gate to prove the pinned Textmaschine package itself; that package audit is not an alternate article checker.
- A repairable LanguageTool/PPM/content finding is NOT a terminal process error. The Controller must return `REPAIR_REQUIRED`; repair only the same canonical article via `controller.py repair`, then rerun `fullcheck`.
- `controller.py draft` is forbidden once a state is in `REPAIR_REQUIRED`; only `controller.py repair` may accept revised body bytes for that same bound article.
- The repair transition must not mutate the bound production context, metadata, research or facts. Draft-dependent LT/PPM evidence is regenerated/rebound only inside the next `fullcheck`.
- The internal hash-bound persistent LanguageTool 6.8 worker is permitted solely as an implementation detail of `production_checks.run_all`; it must use the exact pinned LT 6.8 distribution and fail closed/fallback to the exact pinned CLI. It is not a second checker/orchestrator and may not disable or bypass any rule.

## REPAIR RETURN / CONTINUATION HARD RULE

- Every repairable finding MUST be returned to its authoritative owner stage and MUST continue on the same bound article/work item.
- `raise`, `exit`, task abort, batch restart or terminal BLOCK solely because a repairable finding occurred is forbidden.
- Every repairable return MUST produce a machine-verifiable continuation receipt binding at minimum: error identity/hash, owner/target stage, repair cycle, the same bound work item, `terminal=false` and `continuation_required=true`.
- Missing, stale, mismatched or tampered continuation receipt is acceptance FAIL.
- Body, metadata, link/context and research/facts return paths require positive and negative regression coverage.
- Only a genuine non-repairable `FULL_CHECK_HARD_BLOCK`, tool/runtime failure, integrity/security failure, identity/binding/hash failure, forbidden publish attempt or other explicitly non-repairable machine blocker may terminate the run.
- A repair receipt does not authorize a free route; after repair the Controller again determines the next permitted step.

## DIRECT PARENT-CHAT FILE HANDOFF HARD RULE

- A real production/acceptance batch is NOT complete until the parent ChatGPT conversation can expose the exact final `SYSTEM4_WORDPRESS_HANDOFF_V1.json` as a normal chat file/download.
- The final WordPress handoff contract is `SYSTEM4_WORDPRESS_HANDOFF_V1` and the filename is `SYSTEM4_WORDPRESS_HANDOFF_V1.json`.
- The transport relay contract may be `SYSTEM4_PARENT_CHAT_INLINE_V2`; the relay is transport only and is not the final WordPress file contract.
- The handoff contains exactly the checked articles from the bound input snapshot, in input order, with count `1..N`; it has no fixed production count and no article-type allowlist.
- The user must never be asked to treat a GitHub Actions artifact, repository file, internal temp path or hash as the completed parent-chat delivery.
- No repository branch, commit, push, artifact, PR-file or external storage by itself satisfies the terminal file-handoff criterion.
- The final file MUST be valid UTF-8 JSON with contract `SYSTEM4_WORDPRESS_HANDOFF_V1` and MUST pass `handoff_transport.py validate`.
- It MUST contain every checked body, immutable WordPress metadata, `production_context` for each article, real LanguageTool 6.8 PASS evidence and real PPM 6.7.9 PASS evidence.
- The final handoff validator rechecks bound fact packs/fact traces, unchanged-design boundaries and, when count > 1, cross-article distinctness/repetition.
- `publish_allowed=false` remains mandatory. Direct WordPress upload readiness MUST NOT be confused with automatic publish or with successful parent-chat delivery.
- System 4 MUST NOT modify the WordPress plugin or its signature switch as part of acceptance.

### Bound inline relay

- After the complete bound batch has passed, create and validate the canonical compact UTF-8 WordPress handoff.
- `handoff_transport.py inline-pack` may use `SYSTEM4_PARENT_CHAT_INLINE_V2` and multiple ordered Base64/XZ parts as required for transport safety.
- The parent reconstructs via `handoff_transport.py inline-unpack`, validates part order/count, compressed SHA, plaintext SHA, byte length, schema and canonical bytes, and exposes the resulting exact `SYSTEM4_WORDPRESS_HANDOFF_V1.json` in the chat.
- Any missing/duplicate/reordered/tampered part or Base64/XZ/SHA/length/schema/canonical mismatch is `SYSTEM4_HANDOFF_FAIL`.
- No second WordPress transformation occurs after reconstruction; the reconstructed exact JSON is the file the user uploads unchanged.
- Terminal Gesamt-PASS is forbidden until this exact file is actually available in the parent chat.

## CODEX ECONOMY HARD RULE

- Codex quota is a scarce production resource.
- Do NOT invoke Codex for acceptance tests, diagnostics, read-only inspection, architecture work, preflight repair, handoff experiments, signing experiments or WordPress work.
- Perform such work without Codex whenever technically possible.
- Before any Codex production invocation, the caller must already have verified the current System-4 entry/test suite/NO-LEGACY preflight without Codex and bound that PASS to the exact production head SHA.
- A Codex production run MUST NOT repeat that unchanged-head preflight. If the head changes, the caller must re-run the preflight without Codex before another production invocation.
- A Codex invocation is permitted only for a REAL bound article-production run and only after explicit user approval for that new production run.
- Never require article bodies to be pasted manually, downloaded by the user, or moved through a repository branch.
- Signing/ENDSTEMPEL remain disabled for the current article output unless the authoritative production contract changes them.
