# Pferdeatelier eBay – QA7 Versionskorrektur 6.72.320

Stand: 10.11.2026. **Nur isolierte Testfassung, kein Produktiv-Release.**

## Ursache
Die zuvor ausgegebene QA7-ZIP enthielt trotz QA7-Funktionsstand weiterhin die ursprüngliche WordPress-Pluginversionsnummer **6.72.319** an allen maßgeblichen Stellen. Dadurch konnte WordPress die neue Version nicht anhand einer höheren Pluginversion erkennen. Nutzer hat dies berechtigt beanstandet.

## KISS-Korrektur
Original der bereits geprüften QA7-ZIP `Pferdeatelier_eBay_QA7_TEST.zip` physisch geöffnet und **nur** zwei Dateien angepasst:
- `affiliate-portal-router/pferdeportal-affiliate-router.php`: Plugin-Header `Version: 6.72.320` und interne Konstante `const VERSION = '6.72.320';`
- `affiliate-portal-router/readme.txt`: `Stable tag: 6.72.320` und erste Zeile `V6.72.320 QA7 NUR TEST`

Alle **anderen 64/66 Dateien sind byteidentisch** mit QA7. Historische Versionshinweise im bestehenden eBay-Quelltext bleiben unverändert; keine zusätzlichen Regeln, Worker, Tabellen oder Codekorrekturen.

## Physisch geprüfte neue Datei
- Name: `Pferdeatelier_Affiliate_6.72.320_QA7_TEST.zip`
- Ablage: `/pferdeatelier/PLUGINS/QA/Pferdeatelier_Affiliate_6.72.320_QA7_TEST.zip` (persönliche Library)
- Dateigröße: **5.367.324 Bytes**
- SHA256: `e54018da41f23d3cbeba462e60c0abfdb540bb4e294f8bf43a02418e80b4a637`
- **66/66** ZIP-Einträge und CRC: PASS; **23/23** PHP-Syntaxprüfungen: PASS
- Plugin-Hauptdateiname und ZIP-Wurzelverzeichnis unverändert, damit das bestehende Plugin ersetzt statt ein zweites installiert wird.
- Chat-Download direkt bereitgestellt.

## Release-Grenze
Die neue **6.72.320** ist weiterhin **QA7-Testfassung**; kein echter WordPress/MariaDB-Gesamtproduktionsnachweis, kein Wechsel von CURRENT, keine Live-Installation oder Veränderung von WordPress-/Affiliate-Daten durch diese Arbeit. Die alten QA7-Artefakte bleiben erhalten, nicht gelöscht. Das vollständige QS-Protokoll liegt zusätzlich als `Pferdeatelier_Affiliate_6.72.320_QA7_TEST_PRUEFUNG.json` im Library-Pluginbüro.
