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
- For generated articles, the writer may create research/facts/draft only in the temporary workspace and may repair only the same draft when the controller returns a repairable FAIL.
- The writer may not alter immutable metadata, choose a free route, enable publish, bypass a required checker, or create a per-article FULL production release.
- Task 4 must keep all seven article states alive within one task until the System-4 batch gate has accepted the complete set.

## CODEX ECONOMY HARD RULE
- Codex quota is a scarce production resource.
- Do NOT invoke Codex for diagnostics, read-only inspection, architecture work, preflight repair, test-only proof, GitHub persistence experiments, signing experiments or WordPress work.
- Perform such work without Codex whenever technically possible.
- Before any Codex production invocation, the caller must already have verified the current System-4 entry/preflight without Codex.
- A Codex invocation is permitted only for a REAL bound article-production run.
- Before starting that run, the caller must also have a confirmed mechanism that returns ONE real retrievable output file/artifact containing the completed batch. If that file handoff is not confirmed, DO NOT START CODEX.
- Never require seven full article bodies to be pasted into a PR comment as the production handoff.
- Signing/ENDSTEMPEL/WordPress are deferred until after a real 7/7 article batch exists.
