# Codex Auditauftrag – Kategorie-Workflow V1.6.1 HARDLOCK

Prüfe unabhängig und fail-closed:
1. Kein kostenpflichtiger Global-Call ohne gültige hashgebundene `initial_human_sight_review`.
2. Kein kostenpflichtiger Detail-Call ohne gültige hashgebundene `global_gap_human_review` und passende Global-Paket-Bindung.
3. `DEFERRED` darf weder Detailresearch noch READY/FINAL schließen.
4. Jede Änderung nach einem Sichtreview muss dessen Hash invalidieren.
5. FINAL benötigt zusätzlich `human_sight_review` auf unverändertem finalen Review-Scope.
6. Keine WordPress-/HivePress-Content-Write-APIs.
7. DataForSEO nur über die dokumentierten drei Endpoints.
8. Rootfix bleibt erhalten: finales Content-Blatt >=3 reale node-gebundene Longtails; tragfähige FAQ/Tipps/Beratung/Ausrüstung usw. dürfen Content-Kategorien sein.

Keine Änderung ohne konkreten reproduzierbaren Befund. Ergebnis: PASS oder BLOCKED mit Datei/Zeile/Testfall.
