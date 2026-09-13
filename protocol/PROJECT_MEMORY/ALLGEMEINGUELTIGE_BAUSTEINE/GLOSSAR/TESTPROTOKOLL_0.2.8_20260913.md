# GLOSSAR – TESTPROTOKOLL 0.2.8 – 2026-09-13

## Status

0.2.8: **TECHNISCHER ÜBERGABEKANDIDAT HARDTEST PASS**.

Pferde-LIVE-PASS: **OFFEN** bis Installation des exakt geprüften ZIPs und realem Nutzer-Readback.

0.2.7 bleibt **LIVE FAIL / BLOCKED / NICHT VERWENDEN**.
0.2.6 bleibt historische Zwischenversion / nicht verwenden.

## Warum 0.2.8 notwendig wurde

Der reale Nutzer-Readback von 0.2.7 widerlegte vier frühere technische PASS-Aussagen:
- Hero/Bild nicht responsiv;
- AJAX-Trefferliste falsch positioniert;
- Kategorieseiten erreichten nicht den echten Kategorie-Renderer;
- Einzelbegriff-Links lieferten keine belastbare echte Glossarseite.

Die frühere Testkette war unzureichend, weil sie u. a. das Pferde-Design nur durch einen Stub repräsentierte und den real möglichen Upgradepfad 0.2.6 → 0.2.7 nicht abdeckte.

## RED → GREEN

Vor Produktänderung wurden die Fehlerklassen reproduzierbar ROT gemacht.

Minimaler RC-Fix:
1. AJAX-Vorschlagscontainer in das positionierte Suchformular gebunden;
2. Hero von fester 360px-Logik auf echte proportionale Bildskalierung umgestellt;
3. Rewrite-Schema 5 → 6, damit beschädigte Schema-5-Zustände neu aufgebaut werden.

0.2.8 final unterscheidet sich vom vollständig geprüften 0.2.8-rc1 ausschließlich durch den Versionsidentifier in `universal-glossary-engine.php`.

## Echter Design-Integrationsnachweis

Verwendeter echter Pferde-Design-Stand: **1.50.469**.

Exakter Hauptcode SHA-256:
`580fa6c7f5566f29df9254ce92f687a4831554e1d84bf03fbd936bb7577edfe5`

Der Code wurde aus 22 gebundenen Fixture-Chunks rekonstruiert. Der CI-Lauf akzeptiert ihn nur bei exakt diesem SHA und erfolgreichem PHP-Lint.

Es wurde kein `Pferde_Template_Kit`-Stub als Realnachweis verwendet.

## Finaler Hardtest

Workflow:
`.github/workflows/glossar-028-final-hardtest.yml`

Run:
`34755984363`

Getesteter Head:
`d14f6bff7f660cc6461208e8153fbdf237f0d609`

Jobs – alle SUCCESS:
- Browser final: `103720316319`
- Fresh final: `103720316220`
- Update 0.2.6 → 0.2.8: `103720316226`
- Update 0.2.7 → 0.2.8: `103720316230`
- Real Design 1.50.469 final: `103720316084`
- Gated package: `103720510869`

## Bewiesene Positivfälle

- WordPress + MySQL + Astra Fresh-Runtime;
- exakte Version 0.2.8 und Rewrite-Schema 6;
- Startseiten-Topgap-Fix bleibt erhalten;
- browsergemessene responsive Hero-Skalierung bei 1200 / 900 / 720 / 500 px;
- AJAX liefert reale Treffer und die sichtbare Trefferbox sitzt direkt unter dem Suchfeld;
- echte Glossar-Kategorieseite enthält `.uge-category-head` und keine Home-Hero-/Home-Tools-Marker;
- echter Einzelbegriff enthält `<article class="uge-single-wrap">`, H1 und erwarteten Sentinel-Inhalt;
- A–Z, Preview, Duplicate Guard und bestehende Regressionen;
- gleichnamige Kategorie und gleichnamiger Begriff bleiben getrennt;
- normaler WordPress-Beitrag bleibt unverändert;
- echte Updates aus 0.2.6 und 0.2.7 über WordPress-Updater;
- gezielt zerstörter Rewritezustand unter Schema 5 wird durch Schema 6 wiederhergestellt;
- echter Designcode 1.50.469 ist aktiv und hashgebunden.

## Bewiesene Negativfälle

- unbekannter Glossarbegriff → 404;
- Draft-Begriff nicht öffentlich → 404;
- keine fremde/blanke HTTP-200-Seite als Einzelbegriff akzeptiert;
- Kategorieseite darf nicht Home-Hero oder Home-Tools enthalten;
- kein Kategorie-/Begriff-Slug-Collision-Leak;
- kein globaler Eingriff in normale WordPress-Beiträge;
- kein Paketjob vor grünen technischen Gates.

## Exaktes Paket

Actions-Artefakt:
- ID: `10318015702`
- Name: `universal-glossary-engine-0.2.8-gated-tested`
- Outer artifact digest: `sha256:d404bd537f53bffb5a4a894c5ad4758ac5723524323638a6dd1e1b5fbb061b68`

Installierbares inneres ZIP:
`universal-glossary-engine-0.2.8.zip`

SHA-256 inneres ZIP:
`9bdda56baccfb4f7af5ff512fe37cb23d6117eb9cc56bb3e5f059b168b4f1db1`

Das heruntergeladene Actions-Artefakt und das darin enthaltene ZIP wurden lokal erneut geprüft: ZIP-Integrität, Hash, Version, Schema 6 und PHP-Lint PASS.

## Grenze des PASS

Dies ist ein **technischer Kandidaten-PASS**, kein Pferde-LIVE-PASS.

Erst nach Installation exakt dieses ZIPs auf Pferde Atelier und realem Readback dürfen die realen Live-Fehler geschlossen werden.

Die exakte historische Einzelursache der früheren weißen Live-Seite ist rückwirkend nicht bewiesen. Bewiesen ist die Fehlerklasse sowie die Absicherung beider real ausgegebenen Vorgängerpfade 0.2.6 und 0.2.7.
