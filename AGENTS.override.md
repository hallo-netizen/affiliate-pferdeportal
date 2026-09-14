# SYSTEM 4 — ISOLATED CODEX ROOT OVERRIDE — TEST ONLY

Marker: `SYSTEM4_ISOLATED_ROOT_ENTRY_V3`

This file exists only for the dedicated branch `hobbyroom/system4-true-single-room-v1` and intentionally replaces the repository-root `AGENTS.md` for Codex instruction discovery on this branch. The immutable repository `AGENTS.md` must remain unchanged.

## Mandatory first executable command

There is no free route selection on this branch. The parent machine owns the complete pre-Codex entrance.

For every real System-4 production batch the machine MUST, before any Codex worker starts:

1. resolve the exact bound metadata batch;
2. build one machine-owned source request pool per article;
3. technically fetch/verify or otherwise machine-acquire the real source snapshots;
4. bind the immutable prewrite rails per article (identity, slot, category, link/quality binding);
5. create `SYSTEM4_POINT0_SNAPSHOT_V2` with `machine_point0.py`;
6. start each article only through the root gate.

Production root for article index `N`:

`python3 isolated_system4/root_entry.py start-point0 <POINT0_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO> <N>`

Only after `SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY` may Codex be attached through:

`python3 isolated_system4/codex_entry.py worker-start <WORKSPACE_OUTSIDE_REPO>`

Codex free web search is forbidden. It receives only the article-specific Point-0 research pool and may not mutate machine prewrite rails. `external_web_search_allowed=false` and `machine_prewrite_mutation_allowed=false` are mandatory dispatch properties.

The older `start` / `start-stdin` commands are historical acceptance surfaces only and are not valid production starts.

Historical acceptance markers retained for root-integrity verification only:

`python3 isolated_system4/root_entry.py start <BOUND_SNAPSHOT_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO>`

`python3 isolated_system4/root_entry.py start-stdin <WORKSPACE_OUTSIDE_REPO>`

SYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` before or instead of the System-4 root entry.

Before the System-4 root entry, Codex must not run searches, diagnostics, repository inspection, alternative gates, STARTMASTER/H7/H8/ACM/System3 routes, or repair commands. If the machine/root entry returns BLOCKED/FAIL, stop fail-closed.

## Isolation

- Runtime workspaces, research, facts, drafts and generated output live outside the repository.
- Repository implementation changes, when explicitly authorized, are restricted to `isolated_system4/**`; this override itself is the sole root-level branch instruction artifact.
- Do not modify `AGENTS.md`, `control/cloud-entry-gate/**`, STARTMASTER state, Textmaschine, PPM/PSERC/PSTE rules, WordPress plugin, theme/CSS or design authorities.
- No legacy orchestration/runtime dependency is permitted in the System-4 execution path.
- No merge. No publish. `publish_allowed=false` remains mandatory.

## After root-entry PASS

Follow only the bound System-4 state/phase and the controller transitions. `isolated_system4/controller.py fullcheck` is the only production-check orchestrator. LanguageTool 6.8 and PPM 6.7.9 may run only through that path. Repairable findings must stay on the same article and use `controller.py repair`; do not restart or broadly rewrite the article.

A production run is terminally complete only after batch gate PASS and exact `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` creation, validation, inline transport and byte-exact parent-chat reconstruction. No repository artifact/push is a valid handoff.
