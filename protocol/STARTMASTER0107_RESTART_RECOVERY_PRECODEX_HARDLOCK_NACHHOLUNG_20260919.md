# STARTMASTER0107 — Nachholprotokoll Restart-Recovery / Pre-Codex-Start-Hardlock

Stand: 19.09.2026

Rolle dieses Dokuments: historischer Nachweis / WAS + WARUM. Keine CURRENT- oder NEXT-ACTION-Autorität.

## Anlass

Der reale REAL7-Lauf erreichte Artikel 0 / REPAIR_REQUIRED / Revision 1 und wurde anschließend durch CODEX_USAGE_LIMIT beendet. Die exakten Artikelbytes und detaillierten LanguageTool-Findings waren außerhalb des temporären Codex-Workspaces nicht dauerhaft verfügbar.

Damit war bewiesen:
- Same-Article-Repair funktioniert innerhalb eines lebenden Workspaces;
- Cross-Task-/Process-Death-Recovery war produktiv nicht bewiesen;
- wiederkehrende Startfehler mussten zusätzlich vor jedem Codex-Start hart manifestiert werden.

## Bereits gebaute und getestete Lösung

Test-Commit:
`f9281d903d7c0381e7a83f24c3ffa1e5d4fcfc5e`

System4A-Acceptance:
Run `35430672460` — SUCCESS.

Dort vorhanden und getestet:
- `isolated_system4/workspace_recovery_capsule.py`
- `isolated_system4/restart_repair_probe.py`
- erweiterter `isolated_system4/test_repair_continuity.py`
- `control/startmaster0107/PRE_CODEX_START_HARDLOCK.json`
- `control/startmaster0107/PRE_CODEX_START_RECEIPT.json`
- `control/startmaster0107/pre_codex_start_hardlock.py`
- `isolated_system4/parent_start.py` (minimaler Preflight-Aufruf vor Erzeugung des temporären Run-/Workspace)

Der Restart-Test prüft insbesondere:
- REPAIR_REQUIRED vor simuliertem Prozessabbruch;
- vollständige Recovery-Capsule mit Hashes;
- neuer Prozess / neuer Workspace;
- identische Artikelidentität;
- identischer Draft-SHA vor Restart;
- identischer Checks-/Findings-Hash vor Restart;
- Reparatur im wiederhergestellten Workspace;
- Revision steigt exakt;
- Rückkehr zu CHECK_REQUIRED;
- Publish bleibt false.

## Pre-Codex-Start-Hardlock

Der getestete Start-Hardlock manifestiert die historisch wiederkehrenden Startfehler als Pflicht-Guards, darunter:
- STALE_MAIN_HASH
- DISPATCHER_HEAD_DRIFT
- HARDLOCK_BASE_NOT_FRESH_PASS
- START_HERE_STATE_HASH_DRIFT
- WRONG_STEP_OR_POINT0_BYPASS
- MANUAL_SOURCE_REQUEST_OR_WORKSPACE
- CODEX_BOUND_CAPSULE_MISSING
- OLD_OR_RECOVERY_ARTICLE_AS_NEW
- TEMP_WORKSPACE_LOSS
- NEXT_ARTICLE_BEFORE_PREVIOUS_PASS
- REPAIRABLE_FINDING_TERMINALIZED
- CODEX_USAGE_LIMIT_ACTIVE
- CODEX_GITHUB_AUTH_ASSUMPTION
- OUTPUT_ONLY_IN_TMP
- PUBLISH_WITHOUT_SEPARATE_APPROVAL

Der Hardlock verlangt außerdem einen frischen PASS-Receipt für exakt den autorisierten Head, Dispatcher-Head, hardlock-base, Nutzerfreigabe, Codex-Kapazität, Restart-Recovery und Durable-Evidence-Transport.

## Warum noch nicht fertig

Die Lösung ist auf dem Test-Commit bewiesen, aber nicht auf aktuellem Main integriert. Der damalige Test-Receipt steht absichtlich auf BLOCKED, weil Cross-Task-Durable-Transport im produktiven Pfad noch nicht als PASS gebunden war.

Der Test-Branch wurde später zurückgesetzt; er ist daher keine aktuelle Arbeitswahrheit.

## Zielvertrag unverändert

Keine Textmaschinen-, PPM-, LanguageTool-, Design-, SEO-, WordPress- oder Publish-Regel wurde für diese Lösung geändert.

Die operative CURRENT-/NEXT-ACTION-Wahrheit bleibt ausschließlich:
`control/startmaster0107/CURRENT_STATE.json`
