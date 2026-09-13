# BÜRO GLOSSAR – CURRENT_STATE

STAND: 2026-09-13
STATUS: BLOCKED / 0.2.7 LIVE FAIL / TESTSYSTEM UNZUREICHEND

## Belastbarer aktueller Stand

- Büro `GLOSSAR` steuert das öffentliche Pferde-Atelier-Glossar.
- Fachwahrheit bleibt in `../WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/`.
- Vorhandene WordPress-Seite `Glossar` bleibt Hauptseite.
- Das bestehende Pferde-Designplugin bleibt unangetastet.
- `main` bleibt unangetastet.

## Realer Nutzer-Readback 2026-09-13

Installierter/prüfter Stand 0.2.7:
- Abstand oberhalb Startseiten-Hero: **PASS**.
- Hero/Bild responsive: **FAIL**.
- AJAX-Suche sichtbare Darstellung: **FAIL**.
- Kategorieseiten: **FAIL**, erscheinen real wie Startseite statt echter Kategorieansicht.
- Links auf Einzelbegriffe: **FAIL**.

Damit ist 0.2.7 **BLOCKED und nicht abgenommen**.

## Warum der frühere technische PASS nicht gilt

Die frühere Hardtest-Kette war für die reale Abnahme unzureichend:
- Pferde-Design wurde im WordPress-Runner nur durch einen kleinen Stub vertreten;
- Responsivität wurde durch Quelltext-Grep statt reale Browserbreiten geprüft;
- AJAX prüfte die JSON-Antwort, nicht die sichtbare Position der Trefferliste;
- Kategorieprüfung bewies nur saubere isolierte Route, nicht den tatsächlichen Updatepfad aus allen ausgegebenen Vorgängerversionen;
- der reale Übergabepfad 0.2.6 → 0.2.7 wurde nicht geprüft.

## Hart reproduzierte aktuelle Fehler

Autoritative Details:
`FEHLERQUELLEN.md`.

Diagnose-Run:
`34749713877`, Job `103703878642`.

Bewiesen:
- AJAX-Dropdown ist im ausgelieferten Code falsch verankert;
- Hero bleibt oberhalb 720px in fester 360px-/Absolute-Layoutlogik;
- saubere Kategorieansicht unterscheidet sich eindeutig von Startseite;
- 0.2.6 und 0.2.7 besitzen beide Rewrite-Schema 5;
- beschädigter Schema-5-Rewritezustand heilt beim echten WordPress-Update 0.2.6 → 0.2.7 nicht;
- Einzelbegriff kann dabei HTTP 200 liefern, ohne echtes Glossar-Artikelmarkup;
- Kategorie kann statt Kategorieausgabe auf 301 laufen.

## Kein aktueller Übergabekandidat

0.2.7: BLOCKED / nicht verwenden.
0.2.6: historische Zwischenversion / nicht verwenden.

Es existiert aktuell **kein freigegebener neuer ZIP-Kandidat**.

## Nächster belastbarer Schritt

Ausschließlich `HOBBYRAUM.md` folgen:
1. neue reale Acceptance-Schranken zuerst gegen den fehlerhaften Iststand ROT machen;
2. echtes Pferde-Designplugin statt Stub einbinden;
3. Browserbasierte AJAX-/Responsive-Prüfung;
4. Routing-/Rendererprüfung aus 0.2.6 und 0.2.7;
5. erst danach minimaler Fix;
6. kein ZIP vor vollständigem ROT→GRÜN-Nachweis positiv und negativ.
