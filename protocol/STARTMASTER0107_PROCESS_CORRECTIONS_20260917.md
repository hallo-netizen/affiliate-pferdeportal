# STARTMASTER0107 – Prozesskorrekturen 2026-09-17

Status: **HISTORISCHE PROTOKOLL-/FEHLEREVIDENZ. Keine CURRENT_STATE, keine NEXT ACTION.**

## 1. Unzulässiger Codex-Einsatz für Implementierung

Im Chat wurde irrtümlich PR-Kommentar `5717881317` mit einem `@codex`-Implementierungsauftrag für die globale Werkstatt ausgelöst.

Das war prozessual falsch. Codex ist in System 4 ausschließlich für echte gebundene Artikelproduktion nach ausdrücklicher Nutzerfreigabe zulässig, nicht für Implementierung, Tests, Diagnose, Architektur oder Handoff-Arbeit.

Der Codex-Task stoppte fail-closed noch vor Ausführung, weil die notwendige Parent-Start-Autorisierung für diese Invocation fehlte. Ergebnis:
- keine Kommandos ausgeführt;
- keine Dateien durch diesen Codex-Task gelesen oder verändert;
- keine Tests durch diesen Codex-Task ausgeführt;
- kein Commit durch diesen Codex-Task;
- kein Produktionslauf und kein Publish.

Dauerhafte Korrektur:
- `isolated_system4/AGENTS.md` bleibt Autorität für die Codex-Economy-Grenze;
- `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`, `CURRENT_STATE.json` und die aktuelle Übergabe nennen ausdrücklich: **Codex nur für reale gebundene Artikelproduktion nach Nutzerfreigabe.**

## 2. Versehentlicher TEMP-Issue

Während der GitHub-Dateiarbeit wurde versehentlich Issue `#287` mit Titel `TEMP` erzeugt. Er enthielt keine Projektinformation und wurde unmittelbar als `not_planned` geschlossen.

Keine Runtime-, Fach-, Test-, Plugin-, Status- oder Produktionswirkung.

## 3. Konsequenz

Diese Ereignisse sind reine Prozesshistorie und dürfen weder als aktueller Blocker noch als Statusquelle verwendet werden. Operative Wahrheit bleibt ausschließlich:

`control/startmaster0107/PFERDE_ATELIER_START_HERE.json` → `control/startmaster0107/CURRENT_STATE.json` → FRISCHECHECK → NEXT ACTION.
