# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR HERO LIVE PASS / GLOSSAR BREADCRUMB ABSTAND LIVE PASS, INHALTSKETTE LIVE FAIL (JOURNAL FEHLT) / DESIGN 1.50.499 LOKAL HART POSITIV+NEGATIV PASS, LIVE OFFEN / AUTOMATION-SANDBOX LIVE PASS / TERM-EXTRACTOR LIVE PASS / PORTALSEITEN-AUSSCHLUSS 1.3.4 LIVE PASS / CORE 1.3.5 LOKAL HART POSITIV+NEGATIV+MUTATION PASS, LIVE OFFEN / AUTO-PUBLISH AUS

## LIVE bestätigt – nicht regressieren

- Einzelbegriffe öffnen: **PASS**.
- Glossar-Fließtext: **0 Links – PASS**.
- rechte Ocker-Oberkante: **dünn – PASS**.
- Glossar-Breadcrumb Position/Abstand: **LIVE PASS**. Nicht verändern.
- Glossar-Hero: breites Bild + weicher Übergang: **LIVE PASS**.
- Automation-Sandbox: **LIVE PASS**; `ok:true`, alle Positiv-/Negativtests `true`, `production_write_performed:false`.
- Produktion scharf: **AUS**.
- Auto-Publish: **AUS**.
- Pool-Refresh: **LIVE PASS technisch**.
- Core 1.3.2/1.3.3 Term-Extractor: **LIVE PASS**; 14 PSTE-Rohfundstellen wurden auf 9 fachliche Kopfbegriffe reduziert.
- Core 1.3.4 Portalseiten-Ausschluss: **LIVE PASS**. Nutzer-Screenshot: Pool 9, alle 9 `AUSGESCHLOSSEN_PORTALSEITE`, `Portal-Seite=JA`, `Kannibalisierung=NEIN`.

## Breadcrumb – Design 1.50.499

Aktueller LIVE-Fehler auf Glossar-Einzelbegriffen: `Pferde Journal` fehlt in der Breadcrumb-Kette. Korrekt ist:

`Startseite > Pferde Journal > Glossar > Pferd & Biologie > Bandmaß`

Design `1.50.499` ist lokal hart positiv/negativ geprüft, aber bis Installation + Nutzer-Screenshot **LIVE OFFEN**. Der bereits live abgenommene Abstand wurde nicht verändert.

Paket: `PFERDE_ATELIER_DESIGN_V1.50.499_GLOSSAR_JOURNAL_BREADCRUMB_INSTALLIEREN.zip`

SHA-256: `7167d1e6fe7a13e4967b08e367ce30305ff0cfe9faf73ef9846ac7106c58e982`

## Core 1.3.5 – Retained-Backlog + Gate-Hardlock

Paket: `UNIVERSAL_GLOSSARY_ENGINE_1.3.5_BACKLOG_GATE_HARDLOCK_INSTALLIEREN.zip`

SHA-256: `09b56ab1027b5af50f37247f9f20260cc86d07d0edfc10bee4e2ae9d0ec3d78f`

### Zweck

1. Nach ausgeschlossenen Portal-/Kategorie-Treffern im bereits gespeicherten PSTE-Rückstand weiter suchen, bis geeignete Glossarkandidaten gefunden sind oder der lokale Backlog endet.
2. Dieselben SEO-/Bestands-Gates zwingend an **Discovery**, **Research-Paket-Eingang** und unmittelbar **PRE-PUBLISH** erneut ausführen.
3. Ein Research-Paket darf weder einen neuen Kandidaten aus dem Nichts erzeugen noch Kandidat A durch ein Paket für Kandidat B ersetzen.
4. SANDBOX darf niemals produktiv schreiben.

### Retained-PSTE-Scanner

- benutzt `PSTE_Repository::reanalyzeRetainedBacklogBatch()` ausschließlich lokal;
- `provider_calls` muss exakt `0` sein, sonst `BLOCKED`;
- Batchgröße 40;
- maximal 10 Batches je Refresh = maximal 400 lokal geprüfte Backlog-Zeilen pro Refresh;
- Cursor persistent und an Context-/Baseline-Fingerprint gebunden;
- Cursor-Rücksprung, fehlender Context oder kein Fortschritt -> fail closed;
- neue PSTE-Planungsthemen werden erneut extrahiert und vollständig gegen Kategorie/Portalseite/Dublette/Kannibalisierung geprüft;
- ausgeschlossene Treffer zählen **nicht** zum Zielbestand geeigneter Kandidaten.

### Research- und Publish-Hardlock

- Research-Paket für unbekannten/nicht gebundenen Kandidaten -> `TARGET_NOT_IN_POOL`;
- Research-Provider-Paket muss exakt zum aktuell bearbeiteten Kandidaten passen, sonst `RESEARCH_PACKAGE_TARGET_MISMATCH`;
- Kategorie-/Portalseiten-/Kannibalisierungs-Gate wird beim Research-Paket-Eingang erneut ausgeführt;
- derselbe Gate-Check läuft unmittelbar vor jedem WordPress-Write erneut;
- eine Portal-/Kategorieseite, die **erst nach Research und vor Publish** entsteht, blockiert dadurch noch den Publish;
- bestehende Glossarbeiträge bleiben als `BESTAND` gezielt updatefähig und behalten ihre ID.

### Harte lokale Positiv-/Negativprüfung

Exakt gegen die **verpackte ZIP** erneut ausgeführt:

- 14 bekannte LIVE-Rohfundstellen -> 9 Kopfbegriffe PASS;
- Kategorie- und Portalseiten-Gates PASS;
- Retained-PSTE: erster Portal-Treffer wird ausgeschlossen, Scanner findet später echte Kandidaten PASS;
- Provider-Call-Verstoß -> BLOCKED PASS;
- Context unvollständig -> kein Repository-Aufruf PASS;
- Cursor-Regressionsschutz PASS;
- kein Fortschritt -> BLOCKED PASS;
- 10-Batch-/400-Zeilen-Sicherheitsgrenze PASS;
- unbekanntes Research-Paket -> keine Pool-Injektion PASS;
- Research-Paket-Zielwechsel -> QUARANTÄNE PASS;
- Portal-/Artikelkollision am Research-Eingang -> blockiert PASS;
- stale `GEPRUEFT` + Portal-Kollision PRE-PUBLISH -> blockiert PASS;
- neue Portalseite nach Research/vor Publish -> **0 Writes**, blockiert PASS;
- SANDBOX + Auto-Publish -> **0 Writes** PASS;
- ARMED ohne Auto-Publish -> **0 Writes** PASS;
- ARMED + Auto-Publish -> Write erst nach allen Gates PASS;
- WP-Write-Fehler -> QUARANTÄNE PASS;
- korrupter Readback bestehender Beitrag -> Rollback Titel/Inhalt/Meta PASS;
- 50 Beiträge in einem simulierten WordPress-Lauf -> **50/50 PASS**;
- vollständige End-to-End-Kette Discovery -> Research -> SANDBOX -> ARMED Publish PASS.

### Mutationstest

8 kritische Schutzmechanismen wurden jeweils absichtlich entfernt/gebrochen. Alle 8 Mutanten wurden vom Test erkannt und liefen **ROT**:

1. Research-Intake-Gate entfernt;
2. PRE-PUBLISH-Gate entfernt;
3. unbekannte Research-Pakete dürfen Kandidaten erzeugen;
4. Research-Zielbindung entfernt;
5. spezifischer Sperrstatus wird überschrieben;
6. PSTE-Provider-Call-Vertrag deaktiviert;
7. WP-Readback-Prüfung deaktiviert;
8. SANDBOX darf durch Auto-Publish scharf werden.

Ergebnis: **8/8 Sicherheitsmutanten erkannt**.

### Regression / Verpackung

- PHP-Lint aller 3 Plugin-PHP-Dateien PASS;
- ZIP-Lesetest PASS;
- ZIP-Stamm `universal-glossary-engine/` PASS;
- Dateibestand wie 1.3.4: 3 Dateien;
- `class-uge-pferde-content-pack.php` gegenüber 1.3.4 bytegleich;
- Tests nach ZIP-Bau erneut gegen exakt aus ZIP extrahierte Bytes PASS.

## Harte Grenze / NEXT ACTION

1. Design `1.50.499` bleibt bis LIVE-Screenshot offen.
2. Core `1.3.5` ist **lokal hart PASS**, aber noch **kein LIVE-PASS**.
3. Core `1.3.5` über `1.3.4` installieren.
4. Produktion scharf und Auto-Publish bleiben **AUS**.
5. `Pool jetzt aktualisieren` ausführen. Erwartung: die 9 ausgeschlossenen Portalseiten bleiben ausgeschlossen und der Retained-PSTE-Scanner sucht dahinter weiter.
6. Prüftabelle + Discovery-Zeile real lesen. Erst danach echten Kandidaten durch Research/SANDBOX weiterführen.
7. Kein automatischer Publish bis zum vollständigen realen End-to-End-Beweis.
