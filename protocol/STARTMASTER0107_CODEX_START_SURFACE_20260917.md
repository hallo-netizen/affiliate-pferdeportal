# STARTMASTER0107 – dauerhafte Codex-Startfläche

Datum: 2026-09-17

## Zweck

Jeder neue Chat muss einen realen Codex-Cloud-Task starten können, ohne Plugin-Suche, Actions-Ersatz oder Legacy-Route.

## Bewiesener Mechanismus

Ein Top-Level-Kommentar `@codex ...` auf einer offenen GitHub-PR startet über den vorhandenen `chatgpt-codex-connector[bot]` einen Codex-Task. PR #238 enthält historische Positivbelege dieses Mechanismus.

## Dauerregel

Die autoritative Startfläche muss eine offene Draft-PR sein, deren Head der in `CURRENT_STATE.json` benannte aktuelle Arbeitsbranch ist. START_HERE und CURRENT_STATE nennen deren PR-Nummer ausdrücklich.

Vor Start:
1. PR offen prüfen.
2. PR-Head muss dem aktuellen Arbeitsbranch entsprechen.
3. Top-Level-PR-Kommentar muss schreibbar sein.
4. Den exakten gebundenen 107007-Launch und SHA nennen.
5. Codex muss den SHA vor Ausführung selbst prüfen und bei Abweichung hart abbrechen.

Verboten als Ersatz: GitHub Actions, alte Fachworkflow-Strecke, `codex_current_action.py`, worker-authored PASS, Auto-Publish.
