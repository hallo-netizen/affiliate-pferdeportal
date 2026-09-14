# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-14
STATUS: GLOSSAR HERO LIVE PASS / GLOSSAR BREADCRUMB ABSTAND LIVE PASS, INHALTSKETTE LIVE FAIL (JOURNAL FEHLT) / DESIGN 1.50.499 LOKAL HART POSITIV+NEGATIV PASS, LIVE OFFEN / AUTOMATION-SANDBOX LIVE PASS / TERM-EXTRACTOR LIVE PASS / PORTALSEITEN-AUSSCHLUSS 1.3.4 LIVE PASS / AUTO-PUBLISH AUS

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

## Neuer LIVE-Fehler – Glossar-Breadcrumb unterschlägt Pferde Journal

Nutzer-Screenshot auf `Bandmaß` zeigt aktuell:

`Startseite > Glossar > Pferd & Biologie > Bandmaß`

Fachlich korrekt ist:

`Startseite > Pferde Journal > Glossar > Pferd & Biologie > Bandmaß`

Der Fehler betrifft **den Breadcrumb-Inhalt**, nicht den bereits live abgenommenen Abstand.

### Verifizierte Ursache

Die Glossar-Kategorie-Startseite hängt bereits korrekt unter `Pferde Journal`. Die Sonderzweige in `current_breadcrumb_crumbs()` für:

- `is_tax('uge_group')`
- `is_singular('uge_term')`

bauten jedoch jeweils eine neue Basis direkt aus `Startseite + Glossar` und verloren dadurch `Pferde Journal`.

## Design-Kandidat 1.50.499 – gemeinsame Journal-Basis für Glossar-Breadcrumbs

Paket: `PFERDE_ATELIER_DESIGN_V1.50.499_GLOSSAR_JOURNAL_BREADCRUMB_INSTALLIEREN.zip`

SHA-256: `7167d1e6fe7a13e4967b08e367ce30305ff0cfe9faf73ef9846ac7106c58e982`

Änderung ausschließlich in `pferde-template-kit.php`:

- Version `1.50.498 -> 1.50.499`.
- neue gemeinsame Basis `glossary_breadcrumb_base_v150499()`:
  `Startseite > Pferde Journal > Glossar`.
- `uge_group` hängt den aktuellen Glossar-Bereich an.
- `uge_term` hängt Glossar-Bereich + aktuellen Begriff an.
- keine CSS-, Abstands-, Hero-, Glossar-Inhalts- oder Linkregel geändert.

### Harte lokale Positivprüfung 1.50.499

Runtime-Prüfung gegen die echten privaten Pluginmethoden in einem WordPress-Stubszenario:

1. Glossar-Single `Bandmaß` exakt:
   `Startseite > Pferde Journal > Glossar > Pferd & Biologie > Bandmaß` -> **PASS**.
2. Linkziele Journal / Glossar / `uge_group` korrekt, aktueller Begriff unverlinkt -> **PASS**.
3. `Pferde Journal` exakt einmal in der Crumb-Liste -> **PASS**.
4. gerendertes Breadcrumb-Markup + JSON-LD enthält vollständige Kette -> **PASS**.
5. `uge_group` exakt:
   `Startseite > Pferde Journal > Glossar > Pferd & Biologie` -> **PASS**.
6. Glossar-Übersicht bleibt:
   `Startseite > Pferde Journal > Glossar` -> **PASS**.
7. normale WordPress-Seite bleibt ohne Journal-Leak unverändert -> **PASS**.
8. fehlende `/journal/`-Seite verursacht keinen Fatal/kaputten Link -> **PASS**.

### Harte lokale Negativprüfung 1.50.499

- Journal im `uge_term`-Zweig absichtlich entfernt -> Test **ROT** mit alter falscher Kette erkannt.
- Journal im `uge_group`-Zweig absichtlich entfernt -> Test **ROT**.
- Journal absichtlich doppelt eingefügt -> Test **ROT**.

### Regression / Verpackung 1.50.499

- Dateibestand 1.50.498: 500 Dateien.
- Dateibestand 1.50.499: 500 Dateien.
- geändert exakt `pferde-template-kit.php`; andere 499 Dateien bytegleich.
- PHP-Lint aller 5 PHP-Dateien -> **PASS**.
- ZIP-Stamm `affiliate-portal-template-kit/` -> **PASS**.
- ZIP-Lesetest -> **PASS**.
- Versionsheader + `const VERSION`: 1.50.499 -> **PASS**.

## Automation – aktueller Stand

Core 1.3.4 ist live bestätigt. Die ersten 9 PSTE-Kopfbegriffe werden korrekt wegen vorhandener starker Portal-Hauptseiten ausgeschlossen. Kein Research/Text/Publish für diese 9.

Beim Weiterprüfen wurde zusätzlich eine noch offene Sicherheitslücke für einen künftigen Core-Stand erkannt: Kategorie-/Portalseiten-Gates müssen nicht nur beim Discovery-Pool, sondern erneut am Research-Paket-Eingang und unmittelbar PRE-PUBLISH gebunden werden. Bis das hart positiv/negativ geschlossen ist, bleibt Auto-Publish AUS.

## NEXT ACTION

1. Design `1.50.499` installieren.
2. `Bandmaß` real prüfen. Erwartung exakt:
   `Startseite > Pferde Journal > Glossar > Pferd & Biologie > Bandmaß`.
3. Abstand muss gegenüber dem live abgenommenen Stand unverändert bleiben.
4. Erst nach Nutzer-Screenshot Design LIVE PASS.
5. Danach Automation weiter: Gates an Discovery + Research-Paket + PRE-PUBLISH vereinheitlichen und Retained-PSTE-Pool tiefer scannen.
6. Produktion scharf und Auto-Publish bleiben bis zum vollständigen End-to-End-Livebeweis AUS.
