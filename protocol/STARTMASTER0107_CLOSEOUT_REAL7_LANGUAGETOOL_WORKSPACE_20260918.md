# STARTMASTER0107 — Abschluss-/Nachholprüfung 2026-09-18 — REAL7 LanguageTool / Workspace-Verlust

Dieses Dokument ist **Historie/Nachweis**, keine CURRENT- oder NEXT-ACTION-Wahrheit.

## Frisch geprüfte Autoritäten

- Bürotür/Pointer: `control/CURRENT_STARTMASTER.json`
- Navigation: `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`
- einzige Current-Autorität: `control/startmaster0107/CURRENT_STATE.json`
- aktueller geprüfter Main vor diesem Bookkeeping-PR: `df30a8cf7a157ee4eba979e272ad3d1eb76a5544`
- Dispatcher PR #107 / `codex-chat-launcher`: derselbe Head
- Post-Merge-Acceptance auf diesem Stand: Run `35380544689` = SUCCESS, 40/40

## Tatsächlicher Real-Run-Endstand

Der user-freigegebene reale 7er-Codex-Lauf passierte den reparierten Startweg erfolgreich und erreichte Artikel 0 bis Fullcheck und Same-Article-Repair.

Terminaler Befund PR107 issuecomment `5734550696`:
- `FULL:languagetool:LANGUAGETOOL_FINDING`
- wiederholter Fullcheck blieb `REPAIR_REQUIRED`
- 36 LanguageTool-Befunde
- erster Befund: `GERMAN_WORD_REPEAT_RULE`
- Kontext: `Deutschland Club Suchen Suchen App Shop`
- 0/7 abgeschlossen
- Artikel 1 nicht gestartet
- Publish: NO

Der anschließende Fortsetzungsauftrag bewies mit PR107 issuecomment `5734597579`:
- `EXISTING_ARTICLE0_WORKSPACE_NOT_AVAILABLE`
- der identische temporäre Artikel-0-Workspace ist nicht mehr verfügbar
- sichere Fortsetzung dieses konkreten Runs ist deshalb unmöglich
- keine Rekonstruktion aus historischen/Recovery-Artikeln erlaubt

## Nachgeholte dauerhafte Änderungen

1. `CURRENT_STATE.json` vom veralteten PRECODEX-Zustand auf den echten Real-Run-Endstand nachgezogen.
2. Erster aktueller Blocker ist jetzt der verlorene Artikel-0-Workspace nach realem LanguageTool-Repair-Blocker.
3. Genau eine NEXT ACTION gebunden: frischen kompletten 7er-Lauf über den kanonischen gebundenen Parent starten; alle Artikel NEW; jeden Artikel bis PASS im selben Task/Workspace reparieren; erst dann advance; final durable Datei in Parent-Chat; kein Publish.
4. `START_HERE` ausschließlich auf den neuen CURRENT_STATE-Hash nachgebunden.
5. Notfall-Übergabe von veraltetem dynamischem Starttext auf reinen Wegweiser reduziert.

## Zielvertrag

`control/startmaster0107/ZIELVERTRAG_REASONING_MEDIUM_MAX_STARTMASTER0107.json` bleibt **unverändert**.

Ziel bleibt: Medium wo möglich, aber niemals Research-Vollständigkeit, Fact-Bindung, LanguageTool, PPM, PSERC, PSTE, Design, Publish-Sicherheit oder Package-Preflight für Kosten/Tempo abschwächen.

## Warum

- Der vorherige CURRENT_STATE behauptete weiterhin `EXPLICIT_CODEX_APPROVAL_MISSING`, obwohl die Freigabe erteilt und der echte Codex-Lauf bereits bis zum LanguageTool-Repair gelaufen war.
- Die Übergabedatei enthielt einen inzwischen falschen alten Startbefehl und hätte im nächsten Chat erneut eine konkurrierende Wahrheit erzeugt.
- KISS-Lösung: keine neue Architektur; nur Current nachziehen, START_HERE-Hash binden, Übergabe zum Wegweiser machen und diesen Verlauf protokollieren.

## Tests / Evidence

- PR #327 gemergt auf `df30a8cf7a157ee4eba979e272ad3d1eb76a5544`.
- System-4-Acceptance `35380544689`: SUCCESS 40/40.
- Realer Codex-Start danach: Parent/Point-0/Root/Worker erfolgreich bis Artikel-0-Fullcheck/Repair.
- Dispatcher-Hardlock-Fehlläufe `35380791034` und `35380776177` sind **keine Produktions-PASS-Evidence**; sie blockierten erwartungsgemäß alte Dispatcher-PR-Diffs mit `IMMUTABLE_SECURITY_PATH_CHANGE_BLOCKED`.

## Protokollcheck

- Fehler: NACHGEHOLT
- Protokoll: NACHGEHOLT
- Warum: NACHGEHOLT
- Current-Autorität: NACHGEHOLT
- Bürotür/Einstiegspunkt: NACHGEHOLT
- Frischecheck: DELTA GEPRÜFT
- Hobbyraum: PASS — nur Testausführung, keine Current-Wahrheit
- Zielvertrag: PASS — unverändert
- Archiv: NICHT BETROFFEN
- Eine Wahrheit: PASS
- Tests: PASS für den belastbaren Stand; Realproduktion selbst bleibt offen
- Plugins: NICHT BETROFFEN
