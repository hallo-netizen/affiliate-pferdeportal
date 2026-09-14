# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR HERO LIVE PASS / BREADCRUMB-ABSTAND LIVE PASS / DESIGN 1.50.499 LOKAL HART PASS, LIVE OFFEN / AUTOMATION-SANDBOX LIVE PASS / PORTALSEITEN-AUSSCHLUSS 1.3.4 LIVE PASS / CORE 1.3.5 LIVE FAIL / CORE 1.3.6 LIVE FAIL / CORE 1.3.7 LIVE FAIL / CORE 1.3.8 LOKAL HART POSITIV+NEGATIV+MUTATION PASS, LIVE OFFEN / AUTO-PUBLISH AUS

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

## Core 1.3.5 / 1.3.6 / 1.3.7 – LIVE FAIL

### 1.3.5
Realer Readback: `REFRESH_LIMIT_REACHED · lokal verarbeitet 400 · promotet 4 · geeignet 0`.
Künstliches 400er-Limit verworfen.

### 1.3.6
Realer Readback: `RUNNING · Phase RETAINED · Cursor 475 · processed 400 · promotet 4 · Planning-Seiten 0 · geeignet 0`.
Promotions wurden erzeugt, aber Planning konnte verdrängt werden.

### 1.3.7
Realer Nutzer-Screenshot 2026-09-14 15:46:

`RUNNING · Phase PLANNING · Cursor 475 · Backlog durchlaufen 475 · promotet 4 · Planning-Seiten 0 · Provider-Aufrufe 0 · geeignet 0`

Damit ist 1.3.7 ausdrücklich **LIVE FAIL**.

### Verifizierte Ursache 1.3.7

Die fachliche Phase war nun korrekt auf `PLANNING` gebunden. Der nächste Worker wurde aber weiterhin primär über einen zukünftigen WP-Cron-Single-Event angetrieben. WP-Cron läuft nicht als eigener Dauerprozess, sondern benötigt einen späteren WordPress-Request. Dadurch konnte der persistente Job korrekt auf `PLANNING` stehen, ohne dass die nächste Planning-Seite tatsächlich abgearbeitet wurde.

Das ist für die geforderte vollständige Automatisierung unzureichend.

## Core 1.3.8 – LOOPBACK DRIVER HARDLOCK

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.3.8_LOOPBACK_DRIVER_HARDLOCK_INSTALLIEREN.zip`

SHA-256: `dc8850eb1b67006fefaafeb27679973932982f891f6ec84a9702bfd4532277f1`

### Neuer Worker-Vertrag

`Start/Resume -> bounded Worker -> persistierter Checkpoint -> abgesicherter Nonblocking-Loopback -> nächster bounded Worker`

WP-Cron bleibt nur noch Recovery-Fallback.

Harte Änderungen:

- jeder erfolgreiche `RUNNING`-Worker startet den nächsten Schritt selbst über einen internen REST-Loopback;
- Loopback ist `blocking=false`, Timeout <= 1 s;
- interner Endpoint ist mit zufälligem 64-Hex-Secret + `hash_equals` geschützt;
- `wp_loaded`-Watchdog stößt einen seit >=15 s festhängenden `RUNNING`-Job erneut an;
- Loopback-Fehler werden gespeichert und in der Automation-Oberfläche als `Worker-Fehler` sichtbar;
- WP-Cron-Recovery bleibt bei Transportfehler gesetzt;
- `RETRY_WAIT` (z.B. 502/504) wird nicht rekursiv gehämmert;
- Admin-Status zeigt zusätzlich `Loopback: N`;
- Fachlogik aus 1.3.7 bleibt: Planning hat bei offenen Promotions Vorrang vor Retained.

### Harte lokale Prüfung – exakt gegen den 1.3.7-LIVE-Fehler

Exakter Ausgangszustand reproduziert:
`PLANNING / cursor 475 / processed 400 / promoted 4 / planning_pages 0`.

Positiv:
- Watchdog erzeugt selbst den Loopback-Dispatch – PASS.
- erster Loopback verarbeitet Planning-Seite 1 – PASS.
- vor dieser Planning-Seite kein weiterer Retained-Aufruf – PASS.
- echter Glossarkandidat aus Planning wird übernommen – PASS.
- Ziel erreicht -> Loopback-Kette stoppt – PASS.
- mehrere Planning-Seiten: Seite 1 -> selbstständiger Dispatch -> Seite 2 -> selbstständiger Dispatch -> Seite 3 – PASS.
- kein Retained-Aufruf zwischen offenen Planning-Seiten – PASS.
- stale RUNNING-State wird wieder angestoßen – PASS.
- frischer State erzeugt keinen Dispatch-Sturm – PASS.

Negativ/Sicherheit:
- falsches Loopback-Secret -> abgewiesen – PASS.
- Loopback-Transportfehler -> sichtbar gespeichert, kein Fake-Planning – PASS.
- bei Loopback-Fehler bleibt Cron-Recovery gesetzt – PASS.
- HTTP 504 -> RETRY_WAIT, Cursor unverändert, keine schnelle Loopback-Schleife – PASS.
- Provider-Call-Verstoß -> BLOCKED – PASS.
- No-progress -> Retry-Limit -> BLOCKED – PASS.
- Parallelworker-Lock – PASS.
- Research-/PRE-PUBLISH-/Readback-Gates weiterhin PASS.

### Regression / End-to-End

- Kandidat hinter >500 Planning-Einträgen – PASS.
- echter Backlog 620 bis BACKLOG_COMPLETE – PASS.
- Discovery -> Research -> SANDBOX -> ARMED -> WP-Readback -> Publish – PASS.
- SANDBOX 0 produktive Writes – PASS.
- ARMED ohne Auto-Publish 0 Writes – PASS.
- späte neue Portalseite vor Publish blockiert – PASS.
- 50 simulierte WordPress-Beiträge: 50/50 PASS.
- Package-/Portal-/Kategorie-/Migration-/Extractor-Regression PASS.

Exakt gegen die fertige ZIP extrahiert und erneut ausgeführt:
- 93 explizite PASS-Zeilen, 0 explizite FAIL-Zeilen;
- Extraktor- und Migrationstest Exit 0;
- PHP-Lint aller 3 Plugin-Dateien PASS;
- ZIP-Lesetest PASS;
- ZIP-Stamm `universal-glossary-engine/` PASS;
- Content-Pack gegenüber 1.3.7 bytegleich.

### Mutationstest 1.3.8

6 neue Driver-Sicherheitsmechanismen einzeln absichtlich beschädigt; alle 6 wurden erkannt und liefen ROT:

1. Worker startet keinen Folge-Loopback;
2. REST-Worker setzt Kette nicht fort;
3. Watchdog deaktiviert;
4. Secret-Prüfung umgangen;
5. Loopback fälschlich blockierend;
6. Cron-Fallback bei Loopback-Fehler entfernt.

Ergebnis: **6/6 Mutanten erkannt**.

## NEXT ACTION

1. Core `1.3.8` über `1.3.7` installieren.
2. Produktion scharf und Auto-Publish bleiben AUS.
3. Kein manueller Pool-Neustart erforderlich: vorhandener Zustand `PLANNING / 475 / 4 / 0` wird übernommen.
4. Automation-Seite laden. Erwartung: `Loopback` steigt und `Planning-Seiten` wird >0 oder ein konkreter `Worker-Fehler` erscheint.
5. Erst dieser reale Readback entscheidet LIVE PASS/FAIL.
6. Design 1.50.499 separat per Screenshot prüfen.
