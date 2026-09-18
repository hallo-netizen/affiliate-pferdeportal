# SYSTEM 4 — CODEX ROOT OVERRIDE — CURRENT 107007 PARENT START

Marker: `SYSTEM4_ISOLATED_ROOT_ENTRY_V3`

This override is the Codex instruction authority for the current System-4 production route. It must stay aligned with the current bound 107007 bundle. The repository-root `AGENTS.md` remains unchanged.

## Mandatory first production command

There is no free route selection. For the current 107007 production step, the existing System-4 parent owns the complete pre-Codex entrance.

The first executable project production command is exactly:

`python3 isolated_system4/parent_start.py start-current-bound`

No manual SOURCE_REQUESTS path, runtime-root path, workspace path, article index or provider argument may be supplied for the normal current production start.

The parent must:

1. resolve the exact current bound metadata batch;
2. load the generation-bound `SOURCE_REQUESTS.json` exclusively through `RUNTIME_INBOX_STATE.json`;
3. verify source-request ref/hash, batch, generation, item count, indexes, plan slots and non-empty per-item source pools;
4. copy exactly those bound source-request bytes into a freshly created external run root;
5. technically acquire the current source snapshots and bind the immutable prewrite rails;
6. create the current `SYSTEM4_POINT0_SNAPSHOT_V2`;
7. call the existing `system4_107007_batch.py start`, which starts index 0 only through the System-4 root gate;
8. stop at `SYSTEM4_107007_BATCH_ROOT_READY_STOP` with worker not started, `codex_invoked=false`, `advance_invoked=false` and `publish_allowed=false`.

A missing or mismatched source-request binding, wrong batch/generation/count/index/slot, empty pool, internal runtime path, existing runtime root, Point-0 mismatch, Head mismatch or manifest mismatch is fail-closed.

Only after the parent reports `SYSTEM4_PARENT_ROOT_READY_STOP` / `SYSTEM4_107007_BATCH_ROOT_READY_STOP` may Codex be attached to the machine-started current workspace through:

`python3 isolated_system4/codex_entry.py worker-start <WORKSPACE_OUTSIDE_REPO>`

Codex must use the workspace produced by the parent/batch receipt. Codex must never invent a workspace or select a free article index. After a real article PASS, only the existing batch adapter may advance to the next index.

## Root gate binding retained

The production root for article index `N` remains:

`python3 isolated_system4/root_entry.py start-point0 <POINT0_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO> <N>`

It is invoked by the bound System-4 parent/batch route. Codex must not manually replace `start-current-bound` with a free direct Root start for the current 107007 batch.

The older `start` / `start-stdin` commands are historical acceptance surfaces only and are not valid production starts.

Historical acceptance markers retained for root-integrity verification only:

`python3 isolated_system4/root_entry.py start <BOUND_SNAPSHOT_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO>`

`python3 isolated_system4/root_entry.py start-stdin <WORKSPACE_OUTSIDE_REPO>`

SYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` before or instead of the System-4 root entry.

For current 107007, `parent_start.py start-current-bound` is the only allowed normal production entrance. Do not insert cloud-entry, runtime-entry, current-action, Fachworkflow legacy handoff, STARTMASTER/H7/H8/ACM/System3 routes, diagnostics or alternative gates before it.

## NEW article rule

Every article in the current batch is fresh production work. Old article bodies, recovery articles, prior Codex task articles, historical handoffs, durable releases and `.pferde-release/**` are not production sources. Codex receives only the article-specific current Point-0 research pool and may not use free web search. `external_web_search_allowed=false` and `machine_prewrite_mutation_allowed=false` remain mandatory.

## Isolation

- Runtime workspaces, research, facts, drafts and generated output live outside the repository.
- Do not modify `AGENTS.md`, Textmaschine, PPM/PSERC/PSTE rules, WordPress plugin, theme/CSS, design authorities or publish rules.
- No legacy orchestration/runtime dependency is permitted in the current System-4 execution path.
- No merge. No publish. `publish_allowed=false` remains mandatory.

## After worker attachment

Follow only the bound System-4 state/phase and controller transitions. `isolated_system4/controller.py fullcheck` is the production-check orchestrator. LanguageTool 6.8 and PPM 6.7.9 may run only through that path. Repairable findings stay on the same article and use `controller.py repair`; do not restart or broadly rewrite the article.

A production run is terminally complete only after the complete batch PASS, exact `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`, bound 107008 final review, durable output release, existing GitHub-ENDSTEMPEL, real WordPress import-format verification, and byte-identical final file handoff to the parent chat. A `/tmp` path, Codex sandbox path, log or transient artifact is not a valid final handoff.
