# SYSTEM 4 — ISOLATED CODEX ROOT OVERRIDE — TEST ONLY

Marker: `SYSTEM4_ISOLATED_ROOT_ENTRY_V4_POINT0_ONLY`

This file exists only for the dedicated System-4 test branch and intentionally replaces the repository-root `AGENTS.md` for Codex instruction discovery on this branch. The immutable repository `AGENTS.md` must remain unchanged.

## Mandatory first executable command

There is exactly one production entrance.

For every real System-4 production run the machine MUST first create a hash-bound `SYSTEM4_POINT0_SNAPSHOT_V1` containing the exact production snapshot and the verified research source pool. The only root command is:

`python3 isolated_system4/root_entry.py start-point0 <POINT0_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO>`

`start` and `start-stdin` are forbidden and must fail closed with `ROOT_POINT0_REQUIRED`.

Only after `SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY` may Codex be attached as worker via the generated supervisor dispatch. Codex free web search is forbidden; research may use only the bound Point-0 source pool.

SYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` before or instead of the System-4 root entry.

Before the System-4 root entry, do not run searches, diagnostics, repository inspection, alternative gates, STARTMASTER/H7/H8/ACM/System3 routes, or repair commands.

If the root entry returns BLOCKED/FAIL, stop fail-closed. Do not choose another route.

## Isolation

- Runtime workspaces, research, facts, drafts and generated output live outside the repository.
- Repository implementation changes, when explicitly authorized, are restricted to `isolated_system4/**`; this override itself is the sole root-level branch instruction artifact.
- Do not modify `AGENTS.md`, `control/cloud-entry-gate/**`, STARTMASTER state, Textmaschine, PPM/PSERC/PSTE rules, WordPress plugin, theme/CSS or design authorities.
- No legacy orchestration/runtime dependency is permitted in the System-4 execution path.
- No merge. No publish. `publish_allowed=false` remains mandatory.

## After root-entry PASS

Follow only the bound System-4 state/phase and the controller transitions. `isolated_system4/controller.py fullcheck` is the only production-check orchestrator. LanguageTool 6.8 and PPM 6.7.9 may run only through that path. Repairable findings must stay on the same article and use `controller.py repair`; do not restart or broadly rewrite the article.

A production run is terminally complete only after batch gate PASS and exact `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` creation, validation, inline transport and byte-exact parent-chat reconstruction. No repository artifact/push is a valid handoff.
