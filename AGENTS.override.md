# SYSTEM 4 — ISOLATED CODEX ROOT OVERRIDE — TEST ONLY

Marker: `SYSTEM4_ISOLATED_ROOT_ENTRY_V3`

This file exists only for the dedicated branch `hobbyroom/system4-true-single-room-v1` and intentionally replaces the repository-root `AGENTS.md` for Codex instruction discovery on this branch. The immutable repository `AGENTS.md` must remain unchanged.

## Mandatory first executable command

There is no free route selection on this branch.

For a real bound System-4 production task, the FIRST shell command must pass the exact bound snapshot JSON through stdin to:

`python3 isolated_system4/root_entry.py start-stdin <WORKSPACE_OUTSIDE_REPO>`

For local/prebound acceptance only:

`python3 isolated_system4/root_entry.py start <BOUND_SNAPSHOT_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO>`

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
