# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-13
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13

NUTZER-READBACK:
Der obere Abstand wurde real als korrekt bestätigt. Spätere technische Kandidaten dürfen diesen Punkt nicht regressieren.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: 0.2.8 LIVE FAIL / TECHNISCHE KORREKTUR AB 0.2.9 PASS / PFERDE-LIVE-READBACK NEUER STAND OFFEN

NUTZER-READBACK 0.2.8:
„Bild höher geworden aber kein responsive.“

TECHNISCHE ABSICHERUNG:
Das Bild selbst ist Größenanker (`width:100%`, `height:auto`), ohne künstliche feste Bildhöhe. Der reale Browser unter echtem Design 1.50.469 prüft responsive Geometrie. 0.2.10-rc7 übernimmt diese grüne Regression.

**Live nicht geschlossen**, bis Nutzer den neuen installierten Stand real bestätigt.

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung
STATUS: 0.2.7 LIVE FAIL / SPÄTERE TECHNISCHE REGRESSION PASS / LIVE-NEUBEWERTUNG BEI NÄCHSTER INSTALLATION

AJAX-Eingabe, Treffer und Position wurden in den bestehenden Browser-/Regressionstests technisch grün gehalten. Kein neuer realer Nutzer-Fail hierzu dokumentiert.

## GLOSSAR-ROUTE-004 – Einzelbegriffe / Links laufen ins Leere
STATUS: 0.2.8 LIVE FAIL / 0.2.10-rc7 TECHNISCHER KLICKBARKEITSBEWEIS PASS / PFERDE-LIVE OFFEN

NUTZER-READBACK 0.2.8:
„Einzelartikel laufen immer noch ins Leere.“

TECHNISCHE ABSICHERUNG:
- direkter Request-Binder aus der 0.2.9-Linie bleibt Regressionsteil;
- 0.2.10-rc7 rendert Einzelbegriffe auch dann, wenn der normale WordPress-Main-Loop im Test absichtlich geleert wird;
- der echte Browser klickt tatsächlich gerenderte Links statt nur HTTP-Codes zu prüfen.

Beleg Run `34762048546`, Real-Design-Job `103736483696`:
- `UGE0210_EXISTING_SINGLE_CLICK_PASS`
- `UGE0210_NEW_CLUSTER_CLICK_CHAIN_PASS`
- `UGE0210_SINGLE_SURVIVES_EMPTY_MAIN_LOOP_PASS`
- `UGE0210RC7_REAL_DESIGN_CLICKABILITY_BREADCRUMB_LOOP_POISON_PASS`

Klickkette:
`Gesundheit → Hufbein` sowie `Gesundheit → Hufrehe → Strahlfäule → Hufabszess → Gesundheit`.

**Fehlerklasse technisch abgesichert; Pferde-Live-Fehler bleibt offen bis Nutzer-Readback.**

## GLOSSAR-ROUTE-005 – Kategorien nicht dem Glossar-Design angepasst
STATUS: 0.2.8 LIVE FAIL / KORRIGIERTE ACCEPTANCE TECHNISCH PASS / PFERDE-LIVE OFFEN

Die frühere Acceptance war fachlich falsch, weil sie Kategorien ohne Hero/Tools als PASS definierte. Verbindlich ist: eigener Kategorieinhalt plus vollständiger Glossar-Rahmen mit Hero, Suche/A–Z und Icon-Navigation.

0.2.10-rc7 hält die korrigierte Kategorie-Regression grün. **Live nicht geschlossen.**

## GLOSSAR-FE-006 – Echter Design-Integrationstest
STATUS: TECHNISCHE TESTLÜCKE GESCHLOSSEN

Relevante Glossar-Runtime wird unter dem rekonstruierten echten Pferde-Design-Hauptcode 1.50.469 ausgeführt, SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`.

0.2.10-rc7 Real-Design-Job: `103736483696` SUCCESS.

## GLOSSAR-REG-007 – Direktrouting zerstörte Draft-Preview
STATUS: 0.2.9 RC1 ROT / REPARIERT / REGRESSION PASS

Der Direktbinder fing zunächst eine authentifizierte WordPress-Draft-Preview ab. Die Regression erkannte 404; danach wurden native Preview-Query-Parameter ausgenommen. `REG_PREVIEW_PASS` bleibt Teil der grünen Regression.

## GLOSSAR-PROD-008 – Cluster konnte nicht vollständig veröffentlichen
STATUS: 0.2.10-rc6 FAIL / 0.2.10-rc7 REPARIERT / TECHNISCH PASS

BEFUND:
RC6 hatte die drei neuen Pack-Begriffe als plugin-eigene Entwürfe angelegt, die Veröffentlichung stoppte jedoch an der bestehenden UGE-Publikationspolicy.

ROOT CAUSE:
Für veröffentlichte Glossarbegriffe ist eine gültige primäre Portal-Kategorie Pflicht. In der RC6-Packstrecke fehlte diese `primary_category_id`-Bindung.

KORREKTUR RC7:
Vor Erzeugung/Publikation wird die reale veröffentlichte Portal-Seite `Gesundheit` geprüft, einschließlich realer Design-Kategorieerkennung soweit verfügbar. Danach wird `primary_category_id` für jedes Pack-Mitglied gesetzt. Die normale Publikationspolicy wird nicht umgangen.

Beleg:
- Builder `build-0.2.10-rc7.sh`
- Run `34762048546`
- Fresh `103736483608` SUCCESS
- Real Design `103736483696` SUCCESS
- `UGE0210RC7_RELATED_CLUSTER_LINKS_PASS`

## GLOSSAR-LAYOUT-009 – Breadcrumb-Achse im echten Design
STATUS: 0.2.10-RC-LINIE REPARIERT / RC7 TECHNISCH PASS

Der Glossar-Breadcrumb muss sich in die reale universelle Breadcrumb-Achse des Designplugins einordnen und darf keine parallele eigene Achse erzeugen.

RC7-Browsergeometrie unter echtem Design 1.50.469 weist für Startseite, Kategorie und Einzelbegriff dieselbe Breadcrumb-Achse aus.

Beleg Job `103736483696`:
`UGE0210_PFERDE_BREADCRUMB_AXIS_PASS`.

## GLOSSAR-PKG-010 – Aktueller RC7 hat kein gated Übergabepaket
STATUS: OFFEN / BLOCKER

Der erfolgreiche Workflow `34762048546` endet absichtlich mit:
`UGE0210RC7_HARD_GATES_PASS_NO_PACKAGE`.

Daher existieren für 0.2.10-rc7 noch **kein freigegebenes Installations-ZIP und kein Paket-SHA**. Es darf kein rc7-Paket aus einem ungebundenen Nebenbau ausgegeben oder als `CURRENT.zip` synchronisiert werden.

## ÜBERGREIFENDER STATUS

- 0.2.6: historisch / nicht verwenden.
- 0.2.7: LIVE FAIL / nicht verwenden.
- 0.2.8: LIVE FAIL / nicht verwenden.
- 0.2.9: letzter vorhandener gated technischer Kandidat, aber als CURRENT/NEXT ACTION durch aktive 0.2.10-Entwicklung abgelöst; kein bestätigter Pferde-LIVE-PASS.
- 0.2.10-rc1 bis rc6: Entwicklungs-/Diagnosestufen, nicht ausgeben.
- 0.2.10-rc7: **TECHNISCHE HARDTESTS PASS / NO PACKAGE / PFERDE-LIVE OFFEN.**

Run: `34762048546`
Getesteter Head: `1e74b7454e84f97182dbb185614371a48157bc21`

Die realen Nutzerfehler FE-002, ROUTE-004 und ROUTE-005 werden erst durch einen realen Nutzer-Readback eines regelkonform paketierten neuen Stands geschlossen.
