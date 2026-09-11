# SYSTEM 4 — ISOLATED CODEX TEST ENTRANCE

This branch exists only for the isolated System 4 prototype test.

Before any repository-wide workflow, STARTMASTER, capsule, production preflight, handoff or legacy gate: do not execute them on this branch.

System 4 implementation may exist only under `isolated_system4/**` and must follow `isolated_system4/AGENTS.md`.

Allowed bound tasks on this branch:
1. First architecture live test:
   `python3 isolated_system4/live_test.py isolated_system4/live_fixture/wordpress_snapshot.json`
2. First generated article test:
   follow `isolated_system4/FIRST_ARTICLE_TASK.md` exactly.
3. First full-rule article test:
   follow `isolated_system4/FULL_RULE_ARTICLE_TASK.md` exactly.

For task 3 only, Codex may READ repository files outside `isolated_system4/**` solely to identify current authoritative rule texts/specifications and pure checker/tool inputs. It may not modify, import, execute, wrap, call or runtime-depend on old orchestration/workflow code. All implementation changes remain inside `isolated_system4/**`.

Rules:
- no modification outside `isolated_system4/**`;
- generated runtime/article/output files must stay in a temporary directory outside the repository unless a task explicitly says otherwise;
- no import/copy/wrap/reuse of runtime, handoffs, workers, gates, signers, contracts or state machines from concepts 1–3;
- no legacy Cloud Entry or STARTMASTER on this branch;
- no merge;
- no production;
- no publish;
- if the bound task fails, return the first actual System 4 blocker and stop.

This branch-specific entrance is test isolation only. It does not change `main` or any productive workflow.
