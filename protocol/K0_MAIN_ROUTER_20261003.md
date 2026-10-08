# K0 main router evidence — 2026-10-03

Purpose: make `K0:start` deterministic in fresh chats.

Main-level router:
`K0_START_HERE.md`

Pinned K0 branch:
`konzept0-portal-neutral-20261002`

Pinned K0 current:
`konzept0-portal-neutral-20261002:K0_CURRENT_STATE.json`

Forbidden fallback for K0:
- `concept_agent/START_HERE.md`
- `control/startmaster0107/CURRENT_STATE.json` on main
- K8/K9/K10 current files
- archive/chat history

This protocol file also causes the existing deterministic entrance `hardlock` PR check to execute for the router change.

Restore evidence 2026-10-04: `K0_START_HERE.md` restored byte-for-byte from `b45791dc575027253db3d8d85f803ed12dc68e42`; no K0 production, rule, design, Current, or STARTMASTER change.
Reapply evidence 2026-10-05: restore only the proven K0 wrong-entry block/return behavior in `main:K0_START_HERE.md`; no Current, workflow, engine, rule, plugin, WordPress, LT, PPM, design or architecture change.
