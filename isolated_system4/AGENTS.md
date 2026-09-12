# SYSTEM 4 ISOLATION — TEST ONLY

Scope: System 4 implementation only under `isolated_system4/**`.

- Do not modify anything outside `isolated_system4/`.
- Do not import/copy/wrap runtime, workers, gates, handoffs, signers, contracts or state machines from concepts 1–3.
- Historical systems may be read only as inspiration/negative evidence.
- No merge, no production publish.
- Runtime workspaces and generated article/output files must live outside the repository except for the narrow parent-chat transport exception defined below.
- Allowed tasks:
  1. architecture live test via `live_test.py`;
  2. first generated article test exactly per `FIRST_ARTICLE_TASK.md`;
  3. first full-rule article test exactly per `FULL_RULE_ARTICLE_TASK.md`;
  4. full real 7/7 batch exactly per `FULL_RULE_BATCH_TASK.md`.
- For tasks 3 and 4 only, repository files outside `isolated_system4/**` may be read solely to identify current authoritative rule/specification content and pure tool/checker inputs. They may not be modified or used as old orchestration/runtime dependencies.
- For generated articles, the writer may create research/facts/draft only in the temporary workspace and may repair only the same canonical article body via `controller.py repair` when the controller returns `REPAIR_REQUIRED`.
- The writer may not alter immutable metadata, choose a free route, enable publish, bypass a required checker, or create a per-article FULL production release.
- Task 4 must keep all seven article states alive within one task until the System-4 batch gate has accepted the complete set.

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

## PARENT-CHAT DOWNLOAD HANDOFF HARD RULE
- A real 7/7 production run is NOT complete and MUST NOT be reported as `SYSTEM4_7_7_REAL_ARTICLE_BATCH_PASS` until the exact final `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1.json` bytes are directly downloadable in the parent ChatGPT conversation.
- A Codex-task-local `sandbox:/mnt/data/...` link does NOT satisfy this requirement.
- A `View task` link does NOT satisfy this requirement.
- A PR comment containing only a filename, SHA256 or task link does NOT satisfy this requirement.
- Asking the user to manually download elsewhere and re-upload into ChatGPT is forbidden.
- The final file MUST be valid UTF-8 JSON with contract `SYSTEM4_7_ARTICLE_CHAT_HANDOFF_V1` and MUST pass `handoff_transport.py validate`.
- It MUST contain the exact seven checked bodies, immutable WordPress metadata, `production_context` for each article, real LT 6.8 PASS evidence and real PPM 6.7.9 PASS evidence.
- The existing WordPress signature switch is currently OFF for this production path. System 4 therefore performs no signing and no ENDSTEMPEL step for the current articles.
- The exact parent-chat file is the direct WordPress upload file. It MUST state `WORDPRESS_DIRECT_IMPORT`, `direct_wordpress_upload_ready=true`, no direct-upload block reason and no downstream signing/release components.
- `publish_allowed=false` remains mandatory. Direct upload must not be confused with automatic publish.
- System 4 MUST NOT modify the WordPress plugin or its signature switch.

### Narrow transport exception
- After the seven-article batch has passed, Codex may create exactly one transport envelope with `handoff_transport.py pack`.
- The transport envelope may be persisted ONLY on the dedicated temporary branch `system4-parent-chat-handoff`, only at `isolated_system4/.handoff/SYSTEM4_PARENT_CHAT_TRANSPORT_V1.json`.
- The production PR branch MUST NOT receive article/output transport content and MUST NOT change because of handoff transport.
- The transport branch must contain only Base64 transport data plus exact plaintext SHA/length/filename metadata; no second workflow truth, no publish flag, no source-code changes.
- Codex must report the exact transport commit SHA and plaintext SHA256.
- The parent Chat fetches that exact commit/path, unpacks with `handoff_transport.py unpack`, recomputes SHA256 from the resulting bytes, and exposes that exact file as the direct parent-chat download.
- After successful parent-chat readback, the transport branch must be force-reset to the production source head so the transport payload is no longer reachable from the branch tip.
- Any transport SHA/length/schema mismatch is `SYSTEM4_HANDOFF_FAIL`.
- This transport path must be positively and negatively regression-tested without Codex before another real production run.

## CODEX ECONOMY HARD RULE
- Codex quota is a scarce production resource.
- Do NOT invoke Codex for diagnostics, read-only inspection, architecture work, preflight repair, test-only proof, GitHub persistence experiments, signing experiments or WordPress work.
- Perform such work without Codex whenever technically possible.
- Before any Codex production invocation, the caller must already have verified the current System-4 entry/test suite/NO-LEGACY preflight without Codex and bound that PASS to the exact PR head SHA.
- A Codex production run MUST NOT repeat that unchanged-head preflight. If the head changes, the caller must re-run the preflight without Codex before another production invocation.
- A Codex invocation is permitted only for a REAL bound article-production run.
- Before starting that run, the complete parent-chat transport route above must have passed a real dummy roundtrip without Codex.
- Never require seven full article bodies to be pasted into a PR comment as the production handoff.
- Signing/ENDSTEMPEL remain disabled for the current article output. After 7/7 PASS, transport the exact direct WordPress JSON to the parent chat without another transformation.
