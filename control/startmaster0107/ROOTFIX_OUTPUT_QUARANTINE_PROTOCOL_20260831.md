# STARTMASTER0107 – ROOTFIX OUTPUT-QUARANTÄNE / ZWANGSSTRASSE – PROTOKOLL 2026-08-31

## Ziel
Nur Ergebnisse, die nachweislich durch die gebundene Produktionsstraße gelaufen sind, dürfen jemals als sichtbares Projektergebnis gelten. Alles außerhalb der Straße ist technisch wertlos und bleibt Quarantäne/Müll. Wächter bleiben vollständig fachblind und dürfen Inhalt oder Qualität weder prüfen noch verändern.

## Analyse des fehlgeschlagenen 7er-Laufs

### A. Start-/Geschwindigkeitsproblem
Beobachtet: zu Beginn wurden bereits bekannte Infrastrukturkomponenten wiederholt gesucht oder erneut geprüft, unter anderem LanguageTool. Das war unnötig, weil hash-identische PASS-Belege bereits vorlagen.

Umsetzung:
- hash-identische PASS-Belege wiederverwenden;
- bekannte gebundene Komponenten direkt verwenden;
- unveränderte Infrastruktur nicht neu rediscovern;
- nur batch- und artikelabhängige Prüfungen neu ausführen;
- bestehende Parallelverarbeitung unverändert lassen.

Status: UMGESETZT in `START_OPTIMIZATION_POLICY_20260831.json`.

### B. Worker sah falschen/alten Step
Beobachtet: GitHub `main` war auf 107007 gebunden, ein Worker materialisierte dennoch 107001. Der exakte technische Ursprung des veralteten Workerstands ist nicht vollständig bewiesen. Bewiesen ist die Sicherheitslücke: Vor Sekunde 1 gab es keinen zwingenden Nachweis `Worker-HEAD == aktueller origin/main` plus aktuelle State-/Bundle-Bindung.

Umsetzung:
- `worker_freshness_guard.py` prüft vor Capsule-Materialisierung aktuellen HEAD gegen `origin/main`, STARTMASTER, Root/State, Step und Bundle-Hashes;
- Abweichung blockiert vor jeder Facharbeit;
- kein Rücksprung auf älteren Step.

Status: UMGESETZT.

### C. Falsche ZIP / falsche Artikel am Ende
Root Cause: Der offizielle Workflow war geschützt, aber die Chat-Ausgabe war nicht mechanisch an einen gültigen Workflow-Receipt und exakte Output-Hashes gebunden. Dadurch konnte außerhalb der Produktionsstraße eine eigene ZIP/Artikelmenge erzeugt und fälschlich als Ergebnis präsentiert werden.

Das war kein Fehler der bewährten Artikelregeln. Die Regeln wurden umgangen.

Umsetzung:
- Chat-Ausführungsautorität = NONE;
- Chat-Projektresultat-/Ausgabeautorität = NONE;
- alle 107007-Ergebniskandidaten ausschließlich unter `.pferde-quarantine/`;
- 107007-PASS muss `BOUND_WORKER`, vollständigen Workflow-PASS, aktuellen Batch-Hash und exakte Output-Hashes binden;
- danach nur unsichtbare Staging-Zone `.pferde-release-staging/`;
- 107008 darf nur exakt diese staged Dateien reviewen;
- sichtbare Freigabe erst nach gültigem 107008-PASS UND erfolgreichem Re-Arm;
- sichtbares Ergebnis nur unter `.pferde-release/<batch>/` plus `PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2`;
- alles andere = `QUARANTINE_INVALID_NEVER_SURFACE_AS_PROJECT_RESULT`.

Status: UMGESETZT.

## Verbindliche Anforderungen und Status

1. Vergangenen Lauf auf Optimierungen analysieren – ERLEDIGT.
2. Alle zulässigen Optimierungen umsetzen – ERLEDIGT, ausschließlich technisch.
3. Fehleranalyse inkl. ZIP/falscher Artikelausgabe – ERLEDIGT.
4. Fehler künftig verhindern – TECHNISCH UMGESETZT über Freshness + Quarantäne + zweistufige Release-Bindung.
5. NICHTS außerhalb der Straße darf in Produktion/Projektresultat gelangen – UMGESETZT: Autorität = NONE, ungebundene Outputs ungültig.
6. Außerhalb erzeugtes Material direkt Quarantäne/Müll – UMGESETZT.
7. Alle Grundregeln unangetastet – BESTÄTIGT.
8. Wächter nur dumme fachblinde Gehilfen – BESTÄTIGT; Domain-/Quality-Authority = NONE.
9. Nichts darf Inhalt/Qualität beeinflussen – BESTÄTIGT; neue Guards arbeiten nur mit Herkunft, State, Hash, Receipt, Pfad und Status.
10. Chat jede Projektfreiheit nehmen – GEBUNDEN: Execution/Output Authority = NONE.
11. Ab Sekunde 1 Zwangsjacke – UMGESETZT durch offiziellen Runtime-Entry + Freshness vor Capsule-Materialisierung.
12. Umsetzung in einem zusammenhängenden Rootfix – UMGESETZT auf einem Branch/PR.
13. Worker-Frischeprüfung – UMGESETZT.
14. Einzige Ausgabeinstanz – UMGESETZT: finaler Release-Receipt.
15. Keine Erfolgsaussage ohne Release-Beleg – GEBUNDEN in 107007/107008.
16. Exakte Herkunftskette Input → Worker → Workflow → Receipt → Hash → Release – UMGESETZT.
17. Negativtests für stale Worker und Chat-/Fremdoutput – TESTMATRIX IMPLEMENTIERT.
18. Positive/negative/Gesamtregression – lokale technische Tests + bestehende GitHub-Hardlock-Regressionschecks vorgeschrieben vor Merge.

## Unveränderte Fachbereiche
Durch diesen Rootfix wurden KEINE Regeln geändert für:
- Recherche / Quellen / Fact-Packs / Claims;
- Artikeltext / Struktur / Titel / Keywords;
- LanguageTool;
- PPM;
- PSERC;
- PSTE;
- SEO;
- Dubletten/Kannibalisierung;
- Design;
- WordPress-Inhalt;
- Publish.

## Neue technische Komponenten
- `control/output-quarantine/OUTPUT_VISIBILITY_POLICY.json`
- `control/output-quarantine/worker_freshness_guard.py`
- `control/output-quarantine/output_release_gate.py`
- `control/output-quarantine/runtime_entry_gate.py`
- `control/output-quarantine/final_review_visibility_guard.py`
- `control/output-quarantine/test_output_quarantine.py`
- `control/startmaster0107/START_OPTIMIZATION_POLICY_20260831.json`

## Sichtbarkeitskette
1. Sekunde 1: offizieller Runtime-Entry.
2. Worker-Frische PASS.
3. Gebundene 107007-Straße.
4. Fachworkflow unverändert vollständig PASS.
5. Kandidaten nur `.pferde-quarantine/`.
6. Receipt bindet Batch + Outputs + Hashes + `BOUND_WORKER`.
7. Technische Vorbereitung nur `.pferde-release-staging/` – noch NICHT sichtbar.
8. 107008 reviewt ausschließlich diese staged Dateien.
9. 107008 PASS + Runtime-Re-Arm.
10. Erst jetzt byteidentische Kopie nach `.pferde-release/<batch>/`.
11. Nur `PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2` macht diese Dateien zu sichtbaren Projektresultaten.

## Status dieses Protokolls
Implementierung auf Rootfix-Branch vollständig gebunden. Vor produktiver Aktivierung zwingend: lokale positive/negative Tests, GitHub `hardlock` + `hardlock-base` PASS, Merge auf `main`, Post-Merge-Verifikation. Vor diesen Nachweisen keine Behauptung „produktiv/wasserdicht“.
