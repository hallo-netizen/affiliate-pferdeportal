# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-28
STATUS: HD-001 V1.9.0 STAGE HARDLOCK LOKAL PASS / LIVE-ABNAHME OFFEN

## Aktueller belastbarer Stand

V1.8.9 hat nach READ_ONLY_PREVIEW-Übernahme unerwartet einen bereits ausgeführten Deployment-Zustand gezeigt. Das wird als realer Blocker behandelt.

Codeprüfung:
- geführte POST-Aktionen waren nicht serverseitig auf die exakt aktuelle Stage hart gebunden;
- stale Downstream-Pakete wurden bei Upstream-Ersatz nicht vollständig invalidiert.

V1.9.0 behebt genau diese beiden Punkte:
- exakter Stage-Guard für jeden Guided-Schritt;
- Downstream-Invalidierung bei neuem/korrigiertem Upstream-Stand;
- aktiver Deployment-Run schützt seinen Rollback-Anker und blockiert Upstream-Ersatz bis Rollback.

Lokale Prüfung:
- 241/241 PASS;
- Fresh-Unpack 241/241 PASS;
- Runtime PHP 17/17 PASS;
- Runtime-Parität 22/22 PASS;
- exakter READ_ONLY_PREVIEW→stale Deployment Regressionstest PASS/BLOCKED wie erwartet.

Keine Gesamt-Abnahme.

## NEXT ACTION

V1.9.0 installieren → vorhandenen Test-Deployment-Run zurückrollen → READ_ONLY_PREVIEW erneut übernehmen → live beweisen: Stage structure_ready/finale Prüfung, kein Deployment-Sprung.
