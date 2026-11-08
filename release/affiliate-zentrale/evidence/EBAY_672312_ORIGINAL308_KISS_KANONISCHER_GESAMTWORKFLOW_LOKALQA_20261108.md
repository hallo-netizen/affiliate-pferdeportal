# Pferdeatelier / eBay – Original 6.72.308 -> Kandidat 6.72.312: KISS-Gesamtworkflow lokal geprüft

**Status 08.11.2026: TESTPLUGIN ERSTELLT, LOKALES QUELL-/SIMULATIONSGATE PASS; KEINE PRODUKTIONS-/LIVE-FREIGABE.**

## Dateien dauerhaft in der Pferdeatelier-Pluginbibliothek

- Gesichertes und bytegenau geprüftes 308-Original: `/pferdeatelier/PLUGINS/AFFILIATE_ZENTRALE_6.72.308_URSACHENFIX_GESAMTTEST_NUR_TEST.zip`
- **Neue 6.72.312 installierbare ZIP für eine isolierte TEST-WordPress-Umgebung**: `/pferdeatelier/PLUGINS/QA/AFFILIATE_ZENTRALE_6.72.312_EBAY_GESAMTWORKFLOW_KISS_NUR_TEST.zip`
- Prüfbericht: `/pferdeatelier/PLUGINS/QA/EBAY_6.72.312_LOKALPRUEFUNG.md`
- QA-Belege, ausführbare PHP-Regressions-/Workflow-Simulationen sowie Vorher-Nachher-Fehlnachweis: `/pferdeatelier/PLUGINS/QA/EBAY_6.72.312_QA_BELEGE.zip`
- **SHA-256 312 ZIP:** `b2a5e0a648f237dc2b0237cbc15ccf95279e5cc601c78356784588fe0cee9635`
- Datei nach Ablage aus der Library **erneut materialisiert und bytegenau gegen Quelle verglichen: PASS**. 66/66 ZIP-Dateien, CRC PASS.

## Nachweisbarer Ursachenfehler

Bereits die originalbasierte 311-Quellfassung speicherte den endgültigen `getItem`-Refresh-/Wiederholungs-Cursor. **Die zentrale Fortschrittsfingerprint-Funktion wertete diesen Stand jedoch nicht aus.** Der kanonische Worker erkannte bei einem völlig normalen eBay-Timeout-Retry keinen Fortschritt, erhöhte seinen Null-Fortschritt-Zähler und konnte nach drei solchen Ticks den Gesamtlauf abbrechen.

Dies wurde im simulierten Original-311-Worker **reproduzierbar mit FAIL** nachgewiesen, bevor etwas verändert wurde. **6.72.312 korrigiert nur die EINE bereits bestehende kanonische Fortschrittskontrolle**, sodass sie alle gespeicherten Last-Mile-Refresh-Felder berücksichtigt. Keine zweite Speicherung, keine neue DB-Tabelle, kein zusätzlicher Worker, keine Frontend-HTTP-Requests. Außerdem zwei schon vorhandene sofortige PRIVATE-Returns auf reine kurze gesperrte Funktionen vereinfacht.

## Prüfstand NACH Erstellung aus der finalen 312-ZIP

- 23/23 PHP-Syntaxprüfungen PASS.
- 49/49 tatsächliche PHP-Quellfunktionsregressionen PASS.
- 311 simulierte aufeinanderfolgende Quell-Arbeitspakete durch die **echte kanonische Workerfunktion** plus Auswahl/Abdeckung/Öffentlich/Abschluss: PASS; monotone Position, kein falscher Reset.
- Drei Last-Mile-Retry-Ticks vor Fix Fehlfortschritt, nach Fix: PASS. Gleichzeitige Worker-/Sperr- und unbekannte/lokale Phasensperren: PASS.
- Echte eBay-Pagination-Funktion im Plugin mit lokal fingierten HTTP-Antworten (cURL28, 429/503, 401/403, kaputtes JSON, korrekte Folgeseiten, manipulierte Weiterleitungsziele): PASS.
- Gesamtes Plugin als WordPress-ähnliche Bootstrap-Simulation geladen, 143 Hooks registriert: PASS.
- Echte Quelle/Öffentlichkeit-Filterfunktion der Plugin-Hauptklasse mit lokalen gespeicherten BUSINESS-Kandidaten und ablehnenden/anderen Anbietern: PASS.
- Erst ZIP erstellt, dann vollständig entpackt und **alle oben stehenden Testskripte auf ZIP-Extraktion nochmals ausgeführt: PASS**.

## Sicherheit / präziser Grenzvermerk

**Keine wirkliche WordPress-/MariaDB-/HivePress-Installation oder reale eBay-Browse/getItem-Abfrage verfügbar und durchgeführt.** Die Simulation der 311 Arbeitspakete testet den realen zentralen Worker, aber die Fachphasen und HTTP-Antworten sind fixtures; sie beweist ausdrücklich nicht die reale Vollständigkeit der Produktabdeckung. Keine echte öffentliche Startseite/Produktkarte/Sitemap von WordPress getestet. `release_allowed=false`. Nicht produktiv installieren, nicht CURRENT_RELEASE ändern; zunächst isolierte Testumgebung mit echter WordPress-Datenbank/eBay-API End-to-End validieren.

**KISS:** Altes 308-Original unangetastet, bestehende 311-Gesamtkorrekturen erhalten, nur fünf von 66 Plugin-Dateien gegenüber 308 modifiziert; keine Änderung K0, idealo, Amazon, Designplugin, anderer Portale. Original niemals erneut vom Nutzer anfordern; zuerst in der gesicherten Library nachsehen.
