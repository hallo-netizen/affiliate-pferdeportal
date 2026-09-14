# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR HERO LIVE PASS / BREADCRUMB-ABSTAND LIVE PASS / DESIGN 1.50.499 LOKAL HART PASS, LIVE OFFEN / AUTOMATION-SANDBOX LIVE PASS / PORTALSEITEN-AUSSCHLUSS 1.3.4 LIVE PASS / CORE 1.3.5 LIVE FAIL / CORE 1.3.6 LOKAL HART POSITIV+NEGATIV+MUTATION PASS, LIVE OFFEN / AUTO-PUBLISH AUS

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

Realer Nutzerreadback nach Installation:

`PSTE-Rückstand: REFRESH_LIMIT_REACHED · lokal verarbeitet: 400 · promotet: 4 · Provider-Aufrufe: 0 · geeignet: 0`

Damit ist 1.3.5 ausdrücklich **nicht abgenommen**.

Nachgewiesene Fehler:
1. künstliches Gesamtlimit von 10 × 40 = 400 Retained-Datensätzen beendete den Refresh, obwohl der Backlog nicht vollständig verarbeitet war;
2. Kandidatenleser las pro Refresh nur ein begrenztes Planning-Fenster und konnte spätere Themen verpassen;
3. eine tiefe Verarbeitung im Browser-/PHP-Aufruf wäre wegen Timeout/502/504 nicht nachhaltig.

## Core 1.3.6 – ASYNC RESUME HARDLOCK

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.3.6_ASYNC_RESUME_HARDLOCK_INSTALLIEREN.zip`

SHA-256: `d489d0cd7e9549c4dd868a8167d476b5eca2bb952be40e635bdb6bb1288fec5d`

### Maschinenvertrag

`Start/Refresh -> persistenter Discovery-Job -> viele kleine Worker-Schritte -> TARGET_REACHED oder echter BACKLOG_COMPLETE -> Research -> PRE-PUBLISH -> WordPress-Readback -> Publish`

- Browser-Klick startet nur den Job; 0 schwere Retained-Aufrufe im Browserrequest.
- ein Worker verarbeitet maximal 1 Retained-Batch à 20 + höchstens 1 Planning-Seite à 25.
- kein Gesamtlimit 400/500.
- Cursor + Phase persistent.
- 1.3.5-LIVE-Cursor 400 wird bei Upgrade übernommen; erster neuer Aufruf beginnt bei 400, nicht 0.
- Recovery-Event wird vor schwerer Arbeit gesetzt.
- 504/Exception -> `RETRY_WAIT`; gleicher Cursor wird wieder aufgenommen.
- parallele Worker werden durch Lock geblockt.
- Lock-TTL berücksichtigt PHP `max_execution_time`.
- internes Request-Zeitbudget 12 Sekunden; zusätzliche Planning-Arbeit wird ggf. auf nächsten Worker verschoben.
- bei echtem Backlog-Ende folgt ein finaler vollständiger Planning-Drain.
- erst dann `BACKLOG_COMPLETE`, falls kein Zielkandidat gefunden wurde.
- Discovery `RUNNING/RETRY_WAIT/BLOCKED` sperrt Research und Publish fail-closed.
- Research-Intake und PRE-PUBLISH führen Kategorie-/Portalseiten-/Kannibalisierungs-Gates erneut aus.
- nach Discovery-Abschluss wird die Kette über einen separaten Continue-Hook fortgesetzt; der reguläre Tages-Cron kann diesen Sofortimpuls nicht verschlucken.

### Harte lokale Prüfung 1.3.6 – exakt gegen verpackte ZIP

Positiv:
- Kandidat an Planning-Position 675 gefunden; 700 Planning-Themen sichtbar verarbeitet – PASS.
- Retained-Verarbeitung >400 ohne künstlichen Stopp – PASS.
- alter LIVE-Cursor 400 migriert und exakt bei 400 fortgesetzt – PASS.
- echter Backlog mit 620 Datensätzen vollständig verarbeitet + finaler Planning-Drain – PASS.
- End-to-End Discovery -> Research -> SANDBOX -> ARMED -> WP-Readback -> Publish – PASS.
- 50 simulierte WordPress-Beiträge: 50/50 PASS.
- SANDBOX: 0 produktive Writes – PASS.

Negativ:
- simulierter HTTP 504 bei Cursor 200 -> RETRY_WAIT, Cursor bleibt 200, Folgeworker setzt bei 200 fort – PASS.
- Provider-Call im retained-local-Vertrag -> BLOCKED – PASS.
- kein Fortschritt -> Retry, nach 5 Fehlern BLOCKED – PASS.
- paralleler Worker -> LOCKED, kein zweiter PSTE-Aufruf – PASS.
- unbekanntes/falsch gebundenes Research-Paket -> blockiert – PASS.
- neue Portal-Seite nach Research, vor Publish -> 0 Writes – PASS.
- Discovery noch RUNNING in ARMED+Auto-Publish -> Publish gesperrt – PASS.
- WP-Readback kaputt -> QUARANTÄNE/Rollback – PASS.

Mutationstest: **11/11** absichtlich gebrochene Sicherheitsmechanismen wurden erkannt und liefen ROT, darunter künstliches 400er-Limit, Browser-Schwerarbeit, fehlendes Timeout-Recovery, verlorener 1.3.5-Cursor, deaktivierter Provider-Vertrag, fehlender Lock, fehlende Research-/PRE-PUBLISH-Gates, Package-Injektion, fehlendes Discovery-Fail-Closed und umgangener WP-Readback.

Verpackung:
- 3 Plugin-Dateien wie 1.3.5.
- `class-uge-pferde-content-pack.php` bytegleich zu 1.3.5.
- PHP-Lint PASS.
- ZIP-Lesetest PASS.
- Update-Stamm `universal-glossary-engine/` PASS.
- komplette Tests nach ZIP-Bau erneut gegen exakt extrahierte ZIP-Bytes PASS.

## NEXT ACTION

1. Core 1.3.6 über 1.3.5 installieren.
2. Produktion scharf und Auto-Publish bleiben AUS.
3. `Pool jetzt aktualisieren` einmal klicken.
4. Erwartung: Browser kehrt sofort zurück; Discovery-Zeile wechselt auf `RUNNING` und der Cursor läuft im Hintergrund vom übernommenen Stand weiter.
5. Kein LIVE-PASS, bevor realer Readback zeigt, dass Cursor >400 weiterläuft bzw. ein echter Kandidat oder `BACKLOG_COMPLETE` erreicht wird.
6. Design 1.50.499 separat per Screenshot prüfen.
