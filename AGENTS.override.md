# SYSTEM 4 — ISOLATED CODEX ROOT OVERRIDE

Marker: `SYSTEM4_ISOLATED_ROOT_ENTRY_V3`

The immutable repository `AGENTS.md` remains unchanged. For System-4 production this override is the higher, explicit route contract: there is exactly one executable production start and no legacy navigation.

## Mandatory first executable command

For a real System-4 production batch Codex MUST execute exactly:

`python3 isolated_system4/production_route.py start`

The parent machine MUST have materialized `.pferde-capsule/SYSTEM4_PRODUCTION_BINDING_V1.json` (or the path in `SYSTEM4_PRODUCTION_BINDING`) before Codex is attached. That binding contains only the already machine-built Point-0 path, the bound production snapshot path and the outside-repository run root. Missing or mismatched binding data is a hard block before article work.

After start, Codex MUST obtain every next action only through:

`python3 isolated_system4/production_route.py current`

The runner owns article order `0..N-1`, automatically creates each article workspace through the root gate, skips nothing, and advances only after the current article is at `OUTPUT_GATE_REQUIRED` with `FULL_PRODUCTION` PASS. After the final article it reports `SYSTEM4_PRODUCTION_BATCH_READY_FOR_FINISH`; then Codex executes exactly:

`python3 isolated_system4/production_route.py finish`

`finish` runs the real `batch_gate.py collect`, creates exactly one validated `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`, and returns its exact path/SHA/article count for 107008. No other batch or handoff route is valid.

## Parent-machine preparation before Codex

Before any Codex worker starts the machine MUST:

1. resolve the exact bound metadata batch;
2. build one machine-owned source request pool per article;
3. technically fetch/verify or otherwise machine-acquire the real source snapshots;
4. bind the immutable prewrite rails per article (identity, slot, category, link/quality binding);
5. create `SYSTEM4_POINT0_SNAPSHOT_V2` with `machine_point0.py`;
6. materialize the production binding consumed by `production_route.py start`.

The runner internally starts each article only through:

`python3 isolated_system4/root_entry.py start-point0 <POINT0_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO> <N>`

Only after `SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY` may the runner expose the article to Codex through the existing worker dispatch. Codex must not call `root_entry.py` directly in production.

Codex free web search is forbidden. It receives only the article-specific Point-0 research pool and may not mutate machine prewrite rails. `external_web_search_allowed=false` and `machine_prewrite_mutation_allowed=false` are mandatory dispatch properties.

The older `start` / `start-stdin` commands are historical acceptance surfaces only and are not valid production starts.

Historical acceptance markers retained for root-integrity verification only:

`python3 isolated_system4/root_entry.py start <BOUND_SNAPSHOT_OUTSIDE_REPO> <WORKSPACE_OUTSIDE_REPO>`

`python3 isolated_system4/root_entry.py start-stdin <WORKSPACE_OUTSIDE_REPO>`

SYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` before or instead of `production_route.py start`.

Before the System-4 production runner, Codex must not run searches, diagnostics, repository inspection, alternative gates, STARTMASTER/H7/H8/ACM/System3 routes, or repair commands. If the machine/runner returns BLOCKED/FAIL, stop fail-closed.

## Isolation

- Runtime workspaces, research, facts, drafts and generated output live outside the repository.
- Do not modify `AGENTS.md`, `control/cloud-entry-gate/**`, STARTMASTER state, Textmaschine, PPM/PSERC/PSTE rules, WordPress plugin, theme/CSS or design authorities from a worker run.
- No legacy orchestration/runtime dependency is permitted in the System-4 article execution path.
- No merge. No publish. `publish_allowed=false` remains mandatory.

## Repair

Follow only the bound System-4 state/phase and the controller transitions. `isolated_system4/controller.py fullcheck` is the only production-check orchestrator. LanguageTool 6.8 and PPM 6.7.9 may run only through that path.

A repairable finding stays on the same article/workspace and uses only the existing System-4 owner/repair path. `REPAIR_REQUIRED` means repair the exact reported defect and run the same real checker again. Upstream owner returns use the controller's existing controlled rollback. No `fachworkflow_handoff`, second executor, legacy submission loop or alternative repair mechanism is allowed in System-4 production.

## Batch / 107008 handoff

A production run is terminally complete only after `production_route.py finish` has produced and validated one exact `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2` for all bound articles. That V2 handoff is the sole content input to the downstream 107008 preparation bridge:

`python3 control/startmaster0107/system4_v2_release_bridge.py prepare <SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2_PATH>`

The bridge may only stage byte-/SHA-identical article bytes from the validated V2 handoff. It performs no content mutation, no new quality decision and no publish. The resulting prepared-release reference is the only allowed 107008 content input.
