# CODEX 107001 – FESTER PRÜFAUFTRAG

Arbeite ausschließlich den bereits gebundenen 107001-Rootfix ab.

## Reihenfolge
1. Minimalen Rootfix ausschließlich in `PSTE_0.56.25/includes/class-pste-breadth-research-queue.php` umsetzen.
2. Positiv-/Negativprüfung gegen den bestehenden Breadth-Queue-Vertrag.
3. LIVE24-Quota-Replay: Ziel 40 nur durch tatsächlich nutzbare eindeutige Themen; blockierte Zeilen zählen nie; Provider-Aufrufe im Readiness-Gate bleiben 0.
4. Planning-Readiness-Regeln unverändert prüfen.
5. Danach vollständige bestehende Gesamtworkflow-Regression:
   - title naturalness
   - attribute/SEO independence
   - planning readiness
   - LIVE24 quota replay
   - breadth queue contract
   - PSTE diversity boundary
   - PSTE rootcause regression
   - PSTE/PSERC title batch parity
   - PSERC full regression
   - generation retention
   - generation retention workflow
   - combined capability

## Hart verboten
- keine neue Architektur
- keine Änderung an Fach-/Inhalts-/Qualitäts-/Titel-/Keyword-/Design-/PPM-/LanguageTool-/Dubletten-/Kannibalisierungs-/Publish-Regeln
- retained backlog bleibt vor Provider
- keine Wiederholung bereits unverändert bestandener Infrastruktur-/Hardlock-Prüfungen
- kein zusätzlicher Workflowweg

107001 nur PASS melden, wenn Rootfix + Positiv/Negativ + Gesamtworkflow tatsächlich PASS sind.
Sonst ausschließlich den konkreten BLOCKED-/USER_ACTION_REQUIRED-Grund zurückgeben.
