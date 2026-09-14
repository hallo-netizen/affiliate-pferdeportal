# GLOSSAR – FEHLERQUELLEN

STAND: 2026-09-14
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR DAS PFERDE-ATELIER-GLOSSAR

## LIVE bestätigte Frontend-Bereiche

- Einzelbegriffe öffnen: PASS.
- Fließtext 0 Links: PASS.
- rechte Ockerlinie dünn: PASS.
- Breadcrumb-Abstand: PASS.
- Hero: PASS.
- eigene Hauptsuchwelt `Glossar`: PASS.

Diese Bereiche nicht bei der Produktionsumstellung regressieren.

## GLOSSAR-AUTO-013 – alter autonomer Automationsweg

STATUS: **ABGELÖST / HISTORISCHE FEHLERKETTE**

Reale technische Fehlerkette:
- Core 1.3.5: LIVE FAIL durch künstliches 400er-Gesamtlimit;
- Core 1.3.6: LIVE FAIL; Promotions vorhanden, Planning konnte verdrängt werden;
- Core 1.3.7: LIVE FAIL; Zustand `PLANNING`, aber Folgeworker hing praktisch an WP-Cron;
- Core 1.3.8: lokaler harter Positiv-/Negativ-/Mutationstest PASS, aber **kein LIVE-PASS**.

1.3.8 wurde nicht real als selbstlaufende Produktionsstrecke abgenommen. Der Nutzer hat den gesamten autonomen Text-/Workerweg am 2026-09-14 als verbindlichen Produktionsansatz verworfen.

Diese Fehlerkette bleibt als technische Lernhistorie erhalten, ist aber **keine aktuelle NEXT ACTION**.

## GLOSSAR-IMPORT-014 – neuer JSON-Produktionsweg noch nicht gebaut

STATUS: **AKTIV / BLOCKED BIS IMPLEMENTIERUNG UND TEST**

Zielweg:
`WDB -> Chat-Text -> JSON-Batch -> Glossar-Importer -> WordPress-Draft -> Readback`.

Aktuell fehlt noch der technische Beweis für:
- versionierten JSON-Batchvertrag;
- WDB-ID-/Slug-/Bestandsbindung;
- Textregelprüfung 150–200 Wörter / keine Zwischenüberschriften / 0 Bodylinks;
- Relations-/Portalzielprüfung;
- Draft-only Write;
- echter WordPress-Readback;
- Rollback/BLOCK bei Mismatch;
- Negativschutz normaler Posts/Pages;
- exakter ZIP-Positiv-/Negativ-/Regressionstest.

Daher darf der neue Produktionsweg noch **nicht PASS** genannt werden.

## PASS-GRENZE

Erst der fertig gebaute und gegen die exakten ZIP-Bytes hart getestete JSON-Importer plus realer WordPress-Testbatch kann `GLOSSAR-IMPORT-014` schließen.

Aktuelle Arbeit ausschließlich aus `HOBBYRAUM.md`; Produktionsregeln ausschließlich aus `PRODUKTIONSREGELN.md`.