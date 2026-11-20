# 20.11.2026 – Hobbydepot: Nutzerdatei exakt geprüft und v0.4.24.16

Eingabe `texterstellung-mini-gespeicherter-auftrag.json` mit `batch_id=mini-20261120094038-87239ec1a38a`, genau 20 gesicherte CATEGORY-Ergebnisse, keiner mit Fehler, alle `next=EDITORIAL`. Darin 3 FACH und 17 REDAKTIONSBUERO, kein noch ausstehender CATEGORY-Lauf.

Original `TXE_Workshop::seoImport` aus Version 0.4.24.15 im lokalen WordPress-Stub mit ALLEN 20 Originaleinträgen ausgeführt: EDITORIAL speichert 20/20 ohne Fehler, 17 KLAERUNG schließen bereits ab. Vor Reparatur gab TITLE für die 17 ordnungsgemäß abgeschlossenen Klärungsfälle `MINI_FINAL_DECISION_ALREADY_COMPLETED` und 17 HELD. Das war **ein realer reproduzierter Fehler**.

Die bestehende Funktion behandelt in 0.4.24.16 nur diese 17 Titelpositionen als SKIPPED, sofern EDITORIAL mit BELEGT/KLAERUNG bereits verbindlich abgeschlossen und TITLE leer ist. Anderslautende Felder bleiben gesperrt. K0-Schreiber und DataForSEO unverändert. Zweiter Fehler: `mini-import` war nicht Teil von `sections()`, weshalb die sichtbaren Links in der alten Version auf Übersicht umleiteten; repariert über zwei eigene Register MINI-Export / MINI-Import, Korrektur des Rückwegs und der Ansichtsnavigation.

**Exakte Original-PHP-Abnahme:** EDITORIAL `saved=20,held=0`; TITLE `saved=3,skipped=17,held=0`; Original-K0-Export `3 × exakt 5 Felder`, signierter Host-Beleg `www.hobby-depot.de`. 3 bereits entschiedene FACH-Keywords unverändert. 17 KLAERUNG werden NICHT zu unpassenden Artikelaufträgen freigegeben. Ablehnung manipulierter Originalquelle und fremder Quellensignatur bestätigt. Kontrollierte lokale WordPress-Mocks – **kein Live-WordPress-Import und keine neue K0-Textproduktion**.

ZIP `Texterstellung_Hobbydepot_0.4.24.16_MINI_IMPORT_UND_20ER_ABNAHME.zip`, SHA256 `02a64838912992724c0391ebe53fcb5563df51f5242b283f4f42c6a169236b73`, 518914 Byte, 86 von 87 Quelldateien identisch zu 0.4.24.15. 6 Testreihen mit **175 PASS**, 78 PHP-Lint, 8 JSON-Parse, 87 ZIP CRC. Keine DataForSEO-Abfrage.

Abgelegte Dateien in `/Hobby Depot/Plugin-Büro/`:
- `Texterstellung_Hobbydepot_0.4.24.16_MINI_IMPORT_UND_20ER_ABNAHME.zip`
- `Hobbydepot_MINI_EDITORIAL_20_THEMEN_2026-11-20.json`
- `Hobbydepot_MINI_TITLE_20_THEMEN_2026-11-20.json`
- `Hobbydepot_MINI_0.4.24.16_ORIGINALTEST_NACHWEIS.json`
- `Hobbydepot_MINI_0.4.24.16_TESTQUELLEN.zip`
- `Hobbydepot_MINI_0.4.24.16_KURZBERICHT.md`
- `Texterstellung-CURRENT.md` aktualisiert.

**Nächste echte Schritte:** Backup -> 0.4.24.16 über Plugin 0.4.24.15 -> MINI-Import Redaktionsergebnis -> MINI-Import Titelergebnis -> K0-Export 3 Aufträge. KEINE neue Recherche und KEIN neuer MINI-Export. Bei Importabweichung Diagnose ausgeben, nicht neue Entscheidungen treffen.
