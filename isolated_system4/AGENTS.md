# SYSTEM 4 ISOLATION — TEST ONLY

Scope: System 4 implementation only under `isolated_system4/**`.

- Do not modify anything outside `isolated_system4/`.
- Do not import/copy/wrap runtime, workers, gates, handoffs, signers, contracts or state machines from concepts 1–3.
- Historical systems may be read only as inspiration/negative evidence.
- No merge, no production, no publish.
- Runtime workspaces and generated article/output files must live outside the repository unless a bound task explicitly authorizes a narrow proof-only exception under `isolated_system4/**`.
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

## CODEX ECONOMY HARD RULE
- Codex quota is a scarce production resource.
- Do NOT invoke Codex for diagnostics, read-only inspection, architecture work, preflight repair, test-only proof, GitHub persistence experiments, signing experiments or WordPress work.
- Perform such work without Codex whenever technically possible.
- Before any Codex production invocation, the caller must already have verified the current System-4 entry/test suite/NO-LEGACY preflight without Codex and bound that PASS to the exact PR head SHA.
- A Codex production run MUST NOT repeat that unchanged-head preflight. If the head changes, the caller must re-run the preflight without Codex before another production invocation.
- A Codex invocation is permitted only for a REAL bound article-production run.
- Before starting that run, the caller must also have a confirmed mechanism that returns ONE real retrievable output file/artifact containing the completed batch. If that file handoff is not confirmed, DO NOT START CODEX.
- Never require seven full article bodies to be pasted into a PR comment as the production handoff.
- Signing/ENDSTEMPEL/WordPress are deferred until after a real 7/7 article batch exists.
