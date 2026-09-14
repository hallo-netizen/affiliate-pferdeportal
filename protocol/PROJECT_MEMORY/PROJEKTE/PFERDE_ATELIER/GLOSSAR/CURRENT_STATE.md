# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR HERO LIVE PASS / BREADCRUMB-ABSTAND LIVE PASS / DESIGN 1.50.499 LOKAL HART PASS, LIVE OFFEN / AUTOMATION-SANDBOX LIVE PASS / PORTALSEITEN-AUSSCHLUSS 1.3.4 LIVE PASS / CORE 1.3.5 LIVE FAIL / CORE 1.3.6 LIVE FAIL / CORE 1.3.7 LOKAL HART POSITIV+NEGATIV+MUTATION PASS, LIVE OFFEN / AUTO-PUBLISH AUS

## LIVE bestätigt – nicht regressieren

- Glossar-Einzelbegriffe öffnen: PASS.
- Fließtext: 0 Links – PASS.
- rechte Ocker-Oberkante dünn – PASS.
- Glossar-Breadcrumb Abstand – LIVE PASS; nicht verändern.
- Glossar-Hero – LIVE PASS.
- Automation-Sandbox – LIVE PASS; `production_write_performed:false`.
- Core 1.3.4 Portalseiten-Ausschluss – LIVE PASS: 9/9 aktuelle Begriffe `AUSGESCHLOSSEN_PORTALSEITE`.
- Produktion scharf: AUS.
- Auto-Publish: AUS.

## Design 1.50.499 – LIVE offen

Fehler: Glossar-Einzelbreadcrumb unterschlägt `Pferde Journal`.
Korrekt: `Startseite > Pferde Journal > Glossar > Bereich > Begriff`.
Design 1.50.499 ist lokal hart positiv/negativ geprüft; LIVE-Abnahme fehlt noch.

## Core 1.3.5 – LIVE FAIL

Realer Readback:

`REFRESH_LIMIT_REACHED · lokal verarbeitet 400 · promotet 4 · geeignet 0`

Das künstliche 400er-Limit war fachlich falsch und wurde verworfen.

## Core 1.3.6 – LIVE FAIL

Realer Nutzerreadback nach Installation:

`PSTE-Rückstand: RUNNING · Phase: RETAINED · Cursor: 475 · lokal verarbeitet: 400 · promotet: 4 · Planning-Seiten: 0 · Provider-Aufrufe: 0 · geeignet: 0`

Damit ist 1.3.6 ausdrücklich **nicht abgenommen**.

### Reproduzierte Ursache

1. 1.3.6 führte einen Retained-Batch aus und versuchte Planning nur noch im verbleibenden Request-Zeitbudget.
2. War der PSTE-Retained-Aufruf langsam, wurde Planning auf den nächsten Request verschoben.
3. Der nächste Worker begann jedoch wieder mit Retained statt mit dem offenen Planning-Schritt.
4. Ergebnis: Promotions konnten entstehen (`promotet: 4`), ohne je in den Glossarpool eingelesen zu werden (`Planning-Seiten: 0`, `geeignet: 0`).
5. Zusätzlich ist `processed` kein verlässlicher Fortschrittsersatz für den Cursor: live lief der Cursor 400 -> 475, während `processed` bei 400 blieb.

## Core 1.3.7 – PLANNING HANDOFF HARDLOCK

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.3.7_PLANNING_HANDOFF_HARDLOCK_INSTALLIEREN.zip`

SHA-256: `b2fdd472365d6ce2ed4dbdeb02f5ef46bf7eea4001f30b28d9c3adc458f350aa`

### Maschinenvertrag

`Refresh -> persistenter Discovery-Job -> Retained ODER Planning je Worker -> TARGET_REACHED oder echter BACKLOG_COMPLETE -> Research -> PRE-PUBLISH -> WordPress-Readback -> Publish`

Harte Änderungen gegenüber 1.3.6:

- Zustandsvertrag `UGE_PSTE_DISCOVERY_STATE_V3`.
- Pro Worker exakt **eine schwere Einheit**: Retained-Batch **oder** Planning-Seite.
- `promoted > 0` erzwingt sofort Phase `PLANNING`.
- Planning muss vollständig abgearbeitet werden, bevor der nächste Retained-Batch laufen darf.
- vorhandener 1.3.6-LIVE-Zustand mit `cursor=475 / processed=400 / promoted=4 / planning_pages=0` wird selbstheilend zuerst nach Planning migriert – auch wenn ein bereits geplanter Worker ohne neuen Buttonklick weiterläuft.
- Cursor-Fortschritt wird separat als `traversed` / `Backlog durchlaufen` gespeichert und angezeigt; PSTE-`processed` bleibt nur Diagnosewert.
- Timeout/502/504-Recovery, Lock, Provider-0-Vertrag, Research-Gate, PRE-PUBLISH-Gate und WordPress-Readback bleiben fail-closed.

### Harte lokale Positivprüfung – exakt gegen den LIVE-Fehler

- 1.3.6-LIVE-Zustand `475 / 400 / 4 / 0` reproduziert – PASS.
- Upgrade ohne neuen Browserklick auf V3 – PASS.
- vor Planning **kein weiterer Retained-Aufruf** (`repo_calls=0`) – PASS.
- bereits promotierter echter Begriff wird aus Planning übernommen – PASS.
- `TARGET_REACHED` – PASS.
- Bericht: `cursor=475`, `traversed=475`, `processed=400` – PASS.
- API-Fall `cursor 400 -> 475`, `processed=0`, `promoted=4` – PASS; Planning erhält zwingend Vorrang.
- mehrere Planning-Seiten laufen ohne Retained-Aufruf dazwischen – PASS.
- dynamischer Kandidat erst hinter Planning-Position 675, erst nach Promotion erzeugt – gefunden; Scan >500 – PASS.
- echter Backlog 620 vollständig + finaler Planning-Drain -> `BACKLOG_COMPLETE` – PASS.
- HTTP 504 bei Cursor 200 -> `RETRY_WAIT`, danach wieder Cursor 200 -> Fortschritt – PASS.
- paralleler Worker -> `LOCKED` – PASS.
- Provider-Call im lokalen Backlog -> `BLOCKED` – PASS.
- kein Fortschritt -> Retry-Limit -> `BLOCKED` – PASS.

### End-to-End / Regression

- Discovery -> Research -> SANDBOX -> ARMED -> WP-Readback -> Publish – PASS.
- späte Portalseiten-Kollision -> 0 Writes – PASS.
- SANDBOX -> 0 produktive Writes – PASS.
- ARMED ohne Auto-Publish -> 0 produktive Writes – PASS.
- ARMED + Auto-Publish -> Publish erst nach allen Gates – PASS.
- WP-Write-/Readback-Fehler -> Quarantäne/Rollback – PASS.
- 50 simulierte WordPress-Beiträge -> **50/50 PASS**.
- Extractor, Legacy-Migration, Kategorie-/Portalseiten-Gates, Paketvalidierung – Regression PASS.

### Mutationstest

7 kritische Mechanismen einzeln absichtlich gebrochen; alle 7 wurden vom LIVE-Repro-/Backlog-Test erkannt und liefen ROT:

1. alte Promotions beim Upgrade nicht zuerst ins Planning;
2. `promoted > 0` erzwingt kein Planning;
3. Planning-Datensätze werden nicht in den Pool übernommen;
4. Planning verliert Vorrang vor Retained;
5. Cursor-Fortschritt wird nicht als `traversed` gespeichert;
6. Provider-0-Vertrag deaktiviert;
7. Parallelworker-Lock deaktiviert.

Ergebnis: **7/7 Mutanten erkannt**.

### Fertige ZIP geprüft

Nach ZIP-Bau wurden alle Tests erneut gegen exakt aus der fertigen ZIP extrahierte Bytes ausgeführt:

- Backlog/LIVE-Repro PASS
- Cycle-Modi PASS
- vollständige E2E-Automationskette PASS
- Extractor PASS
- Migration PASS
- Research-/Publish-Gates PASS
- Portalseiten-Gate PASS
- Publish/Readback inkl. 50/50 PASS
- Sandbox-Vertrag PASS
- PHP-Lint aller 3 Plugin-Dateien PASS
- ZIP-Lesetest PASS
- Stamm `universal-glossary-engine/` PASS
- Content-Pack bytegleich zu 1.3.6 PASS

## NEXT ACTION

1. Core `1.3.7` über `1.3.6` installieren.
2. Produktion scharf und Auto-Publish bleiben AUS.
3. Kein Neustart bei 0: der vorhandene Live-Zustand muss übernommen werden.
4. Erwartung zuerst: Phase `PLANNING`; `Planning-Seiten` muss steigen, bevor der Cursor erneut im Retained-Backlog weiterläuft.
5. Danach entweder echter Kandidat oder sauberer Wechsel zurück zu `RETAINED`.
6. Kein LIVE-PASS vor diesem realen Readback.
7. Design 1.50.499 separat per Screenshot prüfen.
