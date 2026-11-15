# Pferdeatelier – Texterstellung 0.4.9: HARD RULE – alte Wege physisch entfernt

**Datum:** 15.11.2026. **Nur isoliertes WordPress-Testplugin, keine Live-/Produktionsfreigabe.**

## Echte Problemursache (WordPress 0.4.7)
User-Diagnose 15.11.2026, 08:54:21 UTC, oliver-beil.de: `txe_seo_export` blockiert durch `PSERC_PLAN_NOT_PROVEN_COMPLETE`; `WORDPRESS`, `PSTE_PLAN`, `EDITORIAL_PLAN` vollständig, PSERC_ACTIVE_PLAN unvollständig/veraltet, Inventar 1.034. 61 alte Aufträge, davon 1 FREI/60 METADATEN_OFFEN. Alte PSERC-Redaktionsplanung war vertraglich abgeschafft und durfte nie ein MINI-Download-Gate sein.

## 0.4.8 nicht installieren: war nur UMGEHEN, nicht ENTFERNEN
Version 0.4.8 wurde explizit zurückgezogen; sie enthielt alte Fachentscheidungswege und 27 PSERC-Dateien. Abgelöst durch **0.4.9-kiss-hard-prune-qa.1** nach Datei-für-Datei-Bereinigung und eigener erneuter Simulation.

## Physisch entfernt, nicht nur gesperrt
- 0.4.8 ZIP: 173 Dateien. 0.4.9 ZIP: **96 Dateien**. Im direkten ZIP-Diff sind **79 alte Dateien physisch gelöscht**, 2 reine zentrale Leseadapter ergänzt, 14 Dateien verändert, 80 Bestanddateien byteidentisch.
- Kompletter alter PSTE-MINI-Workflow und ehemaliges PSTE-Admin-Menü als Quelldateien entfernt; alte getrennte SEO/Kategorie/Titel- und Sofortartikel-Hooks/Actions samt altem Kategorie-Reconcile-Cron entfernt.
- **18** nicht benötigte PSERC-Klassen entfernt, darüber hinaus die früheren Plan-Speicher-/Existing-Content-Klassen sowie **70** nicht aufgerufene Methoden in den nötigen technischen K0-Quelldateien gelöscht. Nur **7** originale technische K0-Klassen (Slot, Signatur, Original-Importer) verbleiben; keine neue PSERC-Redaktionsplanung/keine alte PSERC-Planleseprüfung im MINI.
- Nicht mehr aufgerufener alter `pre_reserved`-Zweig aus dem Original-Slotallocator samt erneuter PSTE-FREI-Abfrage physisch entfernt.
- Doppelt abgefragte historische Titelbestätigung bei schon eingefrorenem MINI-Ergebnis aus der technischen Slotbuchung entfernt. Alte Quellen werden lediglich zur einmaligen anfänglichen Migration in ein leeres WP-Regal gelesen.
- Unnötiger zweiter K0-als-Artikel-Freigabeimport (`BESTEHENDE_FREIGABE`) samt abweichender Kategoriebuchung gelöscht. Originaler K0-Export und originaler WordPress-Draft-Import unverändert nutzbar.
- Alter Kategorien-Gap-Monitor und undefinierte `categoryRefreshCron`-Klassenvariable aus dem Erstimport entfernt; zuvor echter potenzieller PHP-Abbruch.
- Nicht referenzierte PSTE/PSERC-Verträge, Klassen, unbenutzte Wartungs-Funktionen, alte geplante Wartungs-Crons, alte rohe Keyword- und Planungsanzeige entfernt.
- Die originalen für die PSTE-Recherche wirklich referenzierten Research-Klassen bleiben; keine zweite fachliche Entscheidung von dort im gemeinsamen MINI. Wiederaufnahme je CATEGORY/EDITORIAL/TITLE aus genau einem WP-Register.

## Lokal tatsächlich ausgeführter Testumfang
**105/105** Funktions- und Strukturprüfungen + **84/84** PHP-Syntaxprüfungen. Darunter: WP inert ohne Bestätigung (3), bestätigter Start (11), originaler Recherche-Boot (16), initialer Import der tatsächlichen 61 Titel mit anschließendem 20er-Lauf (18), erneuter 20er-Lauf aus bereits gefülltem Regal bei 1.034 synthetischen WordPress-Beiträgen (18), neue Keywords mit drei MINI-Befunden und Schaf/Ziege/Wild ausgeschlossen (13), ORIGINAL-WordPress-Draft-Importer inkl. Replay/Teilfehler (10), **tatsächlich originaler technischer PSERC-Slotallocator** mit simuliertem PPM-Snapshot (10), vier 1.034er-Inventurvarianten mit PSERC gültig/alt/fehlend/defekt (4), echter simulierter WordPress-Handler für MINI-Download (1; 20 Themen/1095 Bestandszeilen), physische Altweg-Strukturprüfung (1).
Die 18er-Szenarien enthalten in Folgephasen teilweise dieselben Prüfungen; sie unterscheiden sich beim Start aus leerem und aus bereits gefülltem Regal. **Es gibt keine echte WordPress-/MySQL- oder DataForSEO-Ausführung dieser 0.4.9, keinen echten signierten PPM-6.7.9-Pfad und keinen externen K0-Lauf.** Kein Produktivversprechen.

## Vollständige installierbare TEST-ZIP und Büro
Datei: `Texterstellung_KISS_0.4.9_TEST_HARD_RULE_BEREINIGT.zip`
SHA256: `f9b328d9fe4bc97fd30409e383d6e4f572f206474716d56d5e5fec9c0a32ee09`, 553013 Bytes, 96 Dateien; ZIP CRC PASS; der Upload ins alte private Plugin-Büro wurde byteidentisch zurückgelesen.
Bestehender privater Büroordner: `/pferdeatelier/PLUGINS/ARBEITSRAUM_PSTE_KISS/` mit TEST-ZIP, TESTBERICHT.md, GESAMTSIMULATION.json, DATEI_AUDIT.json. Keine GitHub-PR gemergt, keine LIVE-WP-Modifikation.

## Einziger noch notwendiger echter Test
Auf **isolierter** oliver-beil.de-Testinstallation 0.4.9 statt 0.4.7 installieren, vorher Backup, **ersetzen, nicht löschen** (61 persistierte Aufträge bewahren), `Texterstellung -> Redaktionsplan -> MINI-Gesamtauftrag herunterladen`, 20 Themen. Bei Fehler genau eine aktualisierte Diagnose. Keine Produktion/K0-Veröffentlichung. `production_release_allowed=false`, `real_wordpress_e2e_passed=false`.