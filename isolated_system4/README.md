# SYSTEM 4 — NAVIGATION ONLY

Diese Datei ist **keine CURRENT_STATE** und enthält bewusst keine eigene dynamische Statuswahrheit.

## Verbindlicher Einstieg

`control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
→ `control/startmaster0107/CURRENT_STATE.json`
→ FRISCHECHECK
→ dortige `entry_for_continuation.next_action`

## Verbindliche statische Quellen

- Zielvertrag: `isolated_system4/ZIELVERTRAG_SYSTEM4_MACHINE_POINT0_WORKER_DISPATCH_20260916.md`
- Hard Rules: `isolated_system4/AGENTS.md`
- Globale Werkstatt-Invariante: `isolated_system4/GLOBAL_WORKSHOP_RULE_20260917.md`

## Harte Regel

Branch, Head, Test-/Run-Stand, Blocker und NEXT ACTION dürfen **nicht** aus dieser README abgeleitet werden. Sie müssen immer frisch über START_HERE → CURRENT_STATE bestimmt werden.

Kein Merge. Kein Auto-Publish. `publish_allowed=false`.
