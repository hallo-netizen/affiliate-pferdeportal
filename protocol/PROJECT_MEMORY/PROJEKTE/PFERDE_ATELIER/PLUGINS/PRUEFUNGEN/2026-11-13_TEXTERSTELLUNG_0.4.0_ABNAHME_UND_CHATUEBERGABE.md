# Pferdeatelier – Texterstellung 0.4.0: Abnahme und Übergabe

**13.11.2026 – Nur installierbare Testfassung. Keine Live-Freigabe.**

## Verbindlicher neuer Stand

**Ein WordPress-Plugin `Texterstellung`, eigener Hauptmenüpunkt in der linken Navigation**, acht Unterpunkte: Übersicht, Recherche, Redaktionsplan, Sofortartikel, Titelerstellung, K0-Export, Rückimport, Diagnose. Nicht mehr unter Werkzeuge.

- Ein zentraler Freigabe-/Auftragsdatensatz pro Thema; getrennte, begrenzte Worker. Keine neue SEO-Entscheidung nach der Redaktion. Gleiches Regal für Sofortartikel.
- **DataForSEO:** bestehender PHP-Treiber aus PSTE isoliert übernommen, Eingabe pro WordPress-Testportal; Zugangsdaten verschlüsselt im *eigenen* Plugin oder lesend aus alten WP-Optionen. Kostenpflichtige Abfrage nur nach ausdrücklichem Klick. Keine eigenständige neue SEO-Freigabe durch DataForSEO.
- **Redaktionsplan:** externes, eingefrorenes Einmal-Entscheidungspaket mit recherchierten Keywords, lokalem WordPress-Artikelbestand, Auftragsbestand und Kategorien. Rücklauf kann `FREI`, `BELEGT`, `KLAERUNG` lauten; bei `FREI` eine belegte Kategorie, Suchintention und Artikelart. Nicht genehmigte Themen werden nicht für K0 freigegeben. Ein fehlerhafter Einzelposten stoppt andere nicht; korrigierbare Dateicharge bleibt erhalten. Optional einmalige manuelle Einzelfreigabe im selben Schritt, aber gesperrt, sobald der externe Redakteur den Kandidaten übernommen hat.
- **Titelerstellung:** bestehendes externes `PSTE_RAW_KEYWORD_MINI_BATCH_V1` mit eingefrorenen übrigen Feldern.
- **K0:** unverändert `PSERC_TEXTMACHINE_METADATA_BATCH_V2` mit genau `title,target_keyword,category,article_type,plan_slot`; Aufträge werden reserviert, nicht gelöscht. Keine Doppelentnahme.
- **Rückimport:** bestehender externer `PFERDE_ATELIER_WORDPRESS_IMPORT_V1`/System4-Vertrag mit technischer Kennungsprüfung; WordPress-Entwurf, kein automatisches Publizieren. Fehlerhafte Rückläufe einzeln angehalten.
- **Diagnose für den Entwickler/Assistenten:** eigene linke Unterseite mit gesondertem JSON-Download, technische Ereignisse, Fehlerkennungen, tatsächliche Statuswechsel, Kennungen/Batchbelege. Keine vollständigen Artikeltexte, Passwörter oder automatische Übermittlung. Keine eigene SEO- oder K0-Qualitätsprüfung.
- **Portalneutraler Ablauf:** dieselbe Pluginquelle benutzt lokale WP-Kategorien/Datensätze pro Website; getrennte Testdaten auf jeder WP-Installation. Historischer K0-Rückgabename noch mit Pferdeatelier-Bezeichnung, nur aus unverändertem Originalvertrag.

## Prüfung

**151 unterschiedliche lokale PHP-Testfälle** über sechs Gruppen (35 historische Original-/Sicherheitstests; 28 DataForSEO/Titel/Altfreigaben; 31 WP-Menüseiten/20er-Charge; 5 Isolation fehlerhafter Rückläufe; 27 Entwicklerdiagnose; 25 neuer Gesamtablauf mit externer Einmalredaktion). Zusätzliche Aktion/Diagnose-Download-Gegenproben bestanden. PHP-Syntax aller 6 PHP-Dateien geprüft; ZIP-Paket acht Einträge, CRC OK. Dies sind lokale WordPress-Nachbildungen, **keine** echte WordPress- oder K0-Abnahme.

Neuer Test der Redaktionskette: 20 Recherchethemen -> 15 FREI, 3 BELEGT, 2 KLÄRUNG -> 15 externe Titel -> K0-Datei mit fünf Feldern -> zuerst 10, dann 5 simulierte Entwürfe -> identischer Zweitimport erzeugt keine weiteren Entwürfe. Ein falscher Kategorieentscheid angehalten; andere Themen liefen; korrigierte Rückgabe unter derselben Quelle wieder aufgenommen.

**Paket:** `Texterstellung_0.4.0_TEST_INSTALLIEREN.zip`, 34.346 Bytes, SHA256 `8a5c2faf39081e05d5610bb4757e9d4f6d8eaaa8f52ca0771007be0ab6c8c3c5`. WP-Pluginordner `texterstellung`, Pluginheader Name: Texterstellung, Version: 0.4.0-test, PHP >=8.1. Eigener Top-Level-Menüpunkt ist im Quellcode über `add_menu_page` umgesetzt, 8 WordPress-Untermenüs über `add_submenu_page`; alter `add_management_page`-Pfad entfernt.

Die Originaldateien unverändert (neue Datei wurde aus einer eigenen Kopie gebaut):
- PSTE 0.57.144.50 QA SHA256 `7fc98a17e4c2319a66afd23c0ad944a07b4492e7a9982933205f29069fdcd121`
- PSERC 0.28.71 QA SHA256 `fd80f7ec3451b437be0eaeedabf2142c5eb1b5130939f7b8dba3b3a2f9d2b59f`
- Texterstellung 0.3.0 SHA256 `9fe7d4a3e4f168bace01f014ff4f358db2f01b6b8b9e532734f2085bfbb91974`

## Noch nicht nachgewiesen – NICHT als fertig behaupten

1. Die **vollständige automatische** historische PSTE-Fachklassifizierung ist nicht 1:1 im Pilot ersetzt. Die redaktionelle Freigabe ist **einmalig, aber derzeit extern per JSON oder manuell**. Der vollständige Workflow ist so bedienbar und testbar; automatische Gleichwertigkeit wäre ein gesonderter tatsächlicher Quell-/Echtbeweis.
2. Der echte DataForSEO-Provider wurde nicht über Internet kontaktiert. Provider-Verhalten in Tests simuliert.
3. Ein echter K0-Lauf auf dem neuen lokal erzeugten `plan_slot`/Auftrags-ID-Vertrag ist **nicht** gelaufen. Dieser Rücklauf könnte noch eine Kompatibilitätssperre aufdecken.
4. Das Paket wurde **noch nicht** in einer echten WordPress-Testinstallation aktiviert, und echte Datenbank-/Datei-/PHP-Laufumgebung auf dem Testserver sind noch nicht abgenommen.
5. Kein Nachweis der vollen Gleichwertigkeit aller 125 alten PSTE/PSERC-PHP-Dateien. Übernommen wurden die für die beschriebene Kette nötigen Teile. Die Migration bestehender Altfreigaben respektiert fehlende Pflichtfelder; die 61 historischen Freigaben sind nicht automatisch produktionsbereit.

## Nächste Schritte für den neuen Chat ohne Grundsatzneubau

1. Diese Datei + verbindlichen Zielvertrag (Regeln 1–20) und Protokoll auf GitHub lesen. **Nur** die neue 0.4.0-ZIP verwenden, alte Zwischen-ZIPs nicht installieren.
2. Nutzer installiert das Plugin ausschließlich auf isolierter Test-WordPress-Seite mit `WP_ENVIRONMENT_TYPE=staging` oder passender Testdomain. **Er** deaktiviert dort bei Bedarf frühere Plugins, Live nicht anfassen. Das neue Plugin bearbeitet niemals Bestandsdateien der Altplugins.
3. WordPress links: **Texterstellung → Diagnose** und ersten JSON-Bericht herunterladen; dann **Sofortartikel** und gesamte Strecke mit echten WordPress-Kategorien probieren; bei Fehlern zweiten JSON-Bericht herunterladen.
4. Eine echte Redaktionsrunde inkl. Keyword-Recherche, 20er-Charge und tatsächlichem K0-Export/Rücklauf prüfen. Noch ausstehende Slot-/K0-Kompatibilität anhand der Diagnosedaten genau lokalisieren.
5. Falls automatische redaktionelle Entscheidung als zwingend identisch verlangt wird: vor Behauptung der Gleichwertigkeit den bisherigen PSTE-Einmalentscheidungsweg nach Quellbeleg übertragen; keine zweite SEO-Nachprüfung und keine neuen Worker.

**Wichtig:** Dieses GitHub-Dokument ist ein Arbeitsprotokoll im Draft-PR, keine neue Campus-CURRENT-Autorität, kein Live-Freigabebeschluss.
