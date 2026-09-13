# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-13
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## GLOSSAR-FE-001 – Abstand oberhalb Hero zu groß
STATUS: LIVE PASS / 2026-09-13

NUTZER-READBACK:
Abstand nach oben war bereits mit 0.2.7 korrekt.

0.2.8 enthält keinen neuen Eingriff in diesen Punkt; Regression ist im finalen Hardtest grün.

Keine weitere Änderung ohne neuen realen Befund.

## GLOSSAR-FE-002 – Hero-Bild nicht responsive
STATUS: 0.2.7 LIVE FAIL / 0.2.8 TECHNISCHER FIX PASS / LIVE-READBACK 0.2.8 OFFEN

NUTZER-READBACK 0.2.7:
real nicht responsiv.

ROOTCAUSE-KLASSE HART REPRODUZIERT:
0.2.7 hielt oberhalb 720px den Hero auf fester 360px-/Absolute-Layoutlogik. Der frühere Acceptance-Test prüfte nur CSS-Zeichenfolgen und keine realen Browsermaße.

0.2.8 TECHNISCH:
Hero/Bild auf proportionale Skalierung umgestellt. Browsermessung unter echtem Design 1.50.469 bei 1200 / 900 / 720 / 500 px PASS.

Finaler Beleg:
Run `34755984363`, Browser `103720316319`, Real Design `103720316084`.

**Nicht geschlossen**, bis realer Pferde-Live-Readback mit exakt 0.2.8 PASS meldet.

## GLOSSAR-FE-003 – AJAX-Suche Frontenddarstellung kaputt
STATUS: 0.2.7 LIVE FAIL / 0.2.8 TECHNISCHER FIX PASS / LIVE-READBACK 0.2.8 OFFEN

NUTZER-READBACK 0.2.7:
AJAX-Trefferliste lag falsch über dem Hero statt direkt am Suchfeld.

ROOTCAUSE HART REPRODUZIERT:
`.uge-search-suggestions` lag außerhalb des positionierten `.uge-search-form`, obwohl die Trefferliste absolut positioniert war. Der alte Test bewies nur die JSON-Antwort.

0.2.8 TECHNISCH:
Treffercontainer ist an das Suchformular gebunden. Der echte Browserlauf tippt eine reale Suche ein, prüft Trefferinhalt sowie x/y/Breite der sichtbaren Trefferbox auf 1200 / 900 / 720 / 500 px.

Finaler Beleg:
Run `34755984363`, Real Design `103720316084` → `REAL_DESIGN_AJAX_PASS`.

**Nicht geschlossen**, bis realer Pferde-Live-Readback mit exakt 0.2.8 PASS meldet.

## GLOSSAR-ROUTE-004 – Einzelbegriffe liefern keine echte Glossarseite
STATUS: 0.2.7 LIVE FAIL / 0.2.8 TECHNISCHE REPARATUR PASS / LIVE-READBACK 0.2.8 OFFEN

NUTZER-READBACK 0.2.7:
Links auf Einzelbegriffe funktionierten nicht.

FEHLERKLASSE HART REPRODUZIERT:
Der frühere Hardtest hatte den real möglichen Pfad 0.2.6 → 0.2.7 ausgelassen. 0.2.6 und 0.2.7 verwenden beide Rewrite-Schema 5. Ein gezielt beschädigter Schema-5-Rewritezustand wurde beim Update auf 0.2.7 deshalb nicht zwingend neu aufgebaut. Außerdem wurde bewiesen, dass HTTP 200 allein kein gültiger Einzelbegriff-Nachweis ist.

0.2.8 TECHNISCH:
Rewrite-Schema 6 erzwingt den nötigen Neuaufbau. Sowohl 0.2.6 → 0.2.8 als auch 0.2.7 → 0.2.8 wurden aus gezielt zerstörtem Rewritezustand über den WordPress-Updateweg geprüft. Die Einzelroute muss danach HTTP 200 **plus** `<article class="uge-single-wrap">`, korrektes H1 und erwarteten Inhalt liefern.

Finaler Beleg:
Run `34755984363`:
- 0.2.6 → 0.2.8 `103720316226` SUCCESS
- 0.2.7 → 0.2.8 `103720316230` SUCCESS
- Real Design `103720316084` SUCCESS.

Die **exakte historische Live-Rootcause** der früheren weißen Seite wird nicht rückwirkend behauptet. Bewiesen und repariert ist die reproduzierbare Fehlerklasse.

**Nicht geschlossen**, bis realer Pferde-Live-Readback mit exakt 0.2.8 PASS meldet.

## GLOSSAR-ROUTE-005 – Kategorieseiten erreichen nicht den echten Kategorie-Renderer
STATUS: 0.2.7 LIVE FAIL / 0.2.8 TECHNISCHE REPARATUR PASS / LIVE-READBACK 0.2.8 OFFEN

NUTZER-READBACK 0.2.7:
Kategorieseiten erschienen identisch zur Startseite.

HART REPRODUZIERT:
Saubere Kategorieausgabe ist eindeutig von der Startseite verschieden: `.uge-category-head` vorhanden; `.uge-hero` und `.uge-tools` fehlen. Unter beschädigtem Schema-5-Rewritezustand konnte der Kategoriepfad den echten Renderer verfehlen.

0.2.8 TECHNISCH:
Schema 6 repariert die gezielt beschädigten Vorgängerzustände. Fresh, beide Upgradepfade und echter Design-Browser verlangen den echten Kategorie-Renderer und schließen Home-Hero/Home-Tools negativ aus.

Finaler Beleg:
Run `34755984363`, Jobs `103720316220`, `103720316226`, `103720316230`, `103720316084` SUCCESS.

**Nicht geschlossen**, bis realer Pferde-Live-Readback mit exakt 0.2.8 PASS meldet.

## GLOSSAR-FE-006 – Frühere Testumgebung war kein echter Design-Integrationstest
STATUS: TESTLÜCKE GESCHLOSSEN / 0.2.8 TECHNISCH PASS

ALTER BEFUND:
`exact-0.2.6-test/02_boot.sh` nutzte real WordPress, MySQL und Astra, aber nur einen selbstgebauten Pferde-Design-Stub. Dieser Runner darf weiterhin nicht als echter Design-Integrationsnachweis interpretiert werden.

NEUER HARTER NACHWEIS:
Der 0.2.8-Endtest rekonstruiert und aktiviert den exakten realen Pferde-Design-Hauptcode 1.50.469 mit SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`

Danach läuft die reale Browser-/Positiv-/Negativprüfung unter genau diesem Code.

Beleg:
Run `34755984363`, Job `103720316084` SUCCESS.

## ÜBERGREIFENDER STATUS

0.2.6: historische Zwischenversion / **nicht verwenden**.

0.2.7: **LIVE FAIL / BLOCKED / nicht verwenden**.

0.2.8: **TECHNISCHER KANDIDAT HARDTEST PASS / PFERDE-LIVE-READBACK OFFEN**.

Finaler technischer Lauf:
`34755984363`, Head `d14f6bff7f660cc6461208e8153fbdf237f0d609`.

Exaktes installierbares Paket:
`universal-glossary-engine-0.2.8.zip`

SHA-256:
`9bdda56baccfb4f7af5ff512fe37cb23d6117eb9cc56bb3e5f059b168b4f1db1`

Actions-Artefakt ID `10318015702`.

Die Fehler FE-002, FE-003, ROUTE-004 und ROUTE-005 bleiben als **Live offen** geführt, bis der Nutzer exakt 0.2.8 auf Pferde Atelier real geprüft hat.
