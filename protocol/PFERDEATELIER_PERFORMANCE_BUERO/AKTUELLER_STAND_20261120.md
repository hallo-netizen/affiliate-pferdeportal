# Pferdeatelier – Performance-Büro – aktueller Stand

Stand: 2026-11-20
Branch: `affiliate-release-current`

## Zweck dieses Büros
Zentrale Arbeitsstelle für die weitere Performance-Verschlankung des Pferdeateliers. Ab jetzt werden neue Performance-Entscheidungen hier fortgeführt, statt weitere parallele Einzelstände anzulegen.

## Verbindliche Regeln
1. KISS: möglichst kleine, klar prüfbare Schritte.
2. Keine neue Plugin-Lösung nur zur Diagnose.
3. Keine Produktionsfunktion entfernen oder zurückbauen, solange nicht bewiesen ist, dass sie entbehrlich ist.
4. Jede Performance-Änderung nur behalten, wenn die Funktion gleich bleibt und die Messung gleich oder besser wird.
5. Keine Ursache raten; erst prüfen, dann ändern.
6. Astra bleibt vorerst bestehen. Entfernung nur nach echtem A/B-Beweis ohne Redesign-Risiko.
7. Kubio darf erst entfernt werden, wenn die verbliebenen Kubio-Seiten/Inhalte vollständig migriert sind.

## Aktueller Live-Stand
- Affiliate-Zentrale: 6.72.362
- Affiliate Portal Template Kit: 1.50.616
- Performance Diagnose Safe: 6.0.0
- Astra: 4.14.3
- Aktive Plugins: ca. 40
- Template 1.50.616 bleibt geschützt; der frühere Child-Page-N+1-Block wurde nachweislich beseitigt.
- 6.72.362 enthält den Fix gegen die nachgewiesene quadratische GTIN-/Multiprovider-Arbeit. Die Seite bleibt trotzdem zu langsam; die Hauptursache ist noch nicht abschließend beseitigt.

## Letzte Gesamtmessung
Datei: `pferdeatelier-performance-gesamtanalyse-20261120-080648.json`

Belegte Größenordnung:
- PHP/WordPress Requests p95: ca. 10.039 ms
- Browser TTFB Ø: ca. 5.679 ms
- LCP: ca. 6.152 ms
- Peak Memory: ca. 212 MB
- 26 überfällige Cron-Ereignisse
- kein persistenter Object Cache
- maximale interne Cache-Zugriffe: 138.483
- `/ausruestung/ausruestung-sattel/pferdesaettel/`: ca. 11.576 ms Wall-Time, ca. 3.690 ms CPU, 320 Queries, 138.483 interne Cache-Hits

Wichtig: hohe Hook-/Datei-/Pluginzahlen allein gelten nicht als Kausalbeweis.

## Testkopie – Erkenntnisstand
Testdomain: `https://pferde.oliver-beil.de`

Bewiesen:
- Domainrouting ist korrekt.
- `wp-config.php` enthält keine feste `WP_HOME`/`WP_SITEURL`-Bindung.
- Die ausgegrauten URL-Felder wurden durch IONOS Single Sign-On verursacht. Nach dessen Deaktivierung wurden die Felder wieder editierbar.
- Astra, Kubio und das Pferde-Template-Kit sind in der Kopie vorhanden.
- Astra-CSS und das Template-Kit-CSS werden ausgeliefert.
- Das fehlende Seitendesign war zunächst kein CSS-Fehler: WordPress zeigte auf `/` die Beitragsübersicht statt der Seite `Start`.
- Nach Zuordnung von `Start` als statische Homepage erschien das Seitendesign wieder.
- Danach fehlten weiterhin Hauptnavigation und Footer-Menüs. Im ausgelieferten HTML war im Hauptmenü nur `Startseite` vorhanden; der erwartete Footer wurde nicht vollständig ausgegeben.
- Damit ist die aktuelle Testkopie nicht als verlässliche 1:1-Baseline geeignet. Es fehlen bzw. greifen einzelne WordPress-/Theme-Zuordnungen trotz Restore nicht identisch.

Entscheidung:
- Diese Testkopie vorerst nicht weiter als Hauptbaustelle reparieren.
- Keine Menüs/Footer manuell nachbauen, nur um die Kopie passend zu machen.
- Für weitere Performance-Arbeit lieber die vorhandene zweite Testseite verwenden oder auf Live nur sehr kleine, reversibel geprüfte Schritte durchführen.

## Nächste Arbeitsstrategie
### Stufe 1 – kleine Plugin-Schritte
Zuerst prüfen, welche aktiven Plugins nachweislich nur Diagnose/Admin/Wartung leisten und für das öffentliche Frontend nicht benötigt werden. Kandidaten werden vor Deaktivierung gegen Hooks/Funktionen geprüft. Keine Sammeldeaktivierung ohne Funktionsbeweis.

Besonders zu prüfen:
- Pferdeatelier eBay – Ein-Klick-Sichtbarkeitsdiagnose
- SEO-Quellpaket Exporter
- WordPress Speicheranalyse
- weitere reine Diagnose-/Wartungswerkzeuge

Inaktive Diagnoseplugins können später aus dem Bestand entfernt werden; ihre bloße Inaktivität erklärt aber keine Frontend-Laufzeit.

### Stufe 2 – Doppelungen
Zwei aktive HivePress-Suchplugins sind vorhanden:
- Pferde Atelier HivePress Anzeigensuche 2.1.5-ajax-category-label
- Pferde Atelier – HivePress Anzeigensuche 1.0.1

Ziel: prüfen, ob eines vollständig durch das andere ersetzt wird. Nur dann auf eines reduzieren.

### Stufe 3 – Design-Plugins zusammenfassen
Mögliche Kandidaten für eine Zusammenführung in das zentrale Template Kit:
- Canonical Table Contract V1
- Anzeigenmarkt & Journal Breadcrumbs
- weitere kleine reine Design-/Frontend-Helfer

Vor Zusammenführung zwingend:
- Quellcode/Funktionen vergleichen
- prüfen, ob eigene Daten/Shortcodes/Hooks existieren
- Frontend vorher/nachher vergleichen
- nur zusammenführen, wenn die Ausgabe und Funktion identisch bleiben

### Stufe 4 – größere Komponenten
- Kubio erst nach Migration der verbliebenen Kubio-Seiten entfernen.
- Astra vorerst behalten.
- Universal Product Knowledge + Universal Product Comparison erst später als mögliche Konsolidierung prüfen.

## Nächster konkreter Schritt
Auf der zweiten Testseite oder – falls diese identisch genug ist – zuerst genau die kleinen aktiven Diagnose-/Admin-Plugins prüfen und einen sicheren ersten Deaktivierungskandidaten bestimmen. Danach identische Frontend-/Funktionsprüfung und Performance-Vergleich. Erst dann der nächste Kandidat.

## Historische Evidenz
Bestehende Performance-Nachweise bleiben gültig und werden nicht dupliziert, insbesondere:
- `release/affiliate-zentrale/evidence/PFERDEATELIER_PERFORMANCE_GESAMTBEWEIS_20261119.md`
- `release/affiliate-zentrale/evidence/PFERDEATELIER_PERFORMANCE_VOLLAUDIT_20261119.md`
- `release/affiliate-zentrale/evidence/PFERDEATELIER_PERFORMANCE_STAND_20261119_1504.md`


## Prüfung der vier kleinen Plugin-Kandidaten – 20.11.2026

Ergebnis: Keines der vier Plugins ist für die öffentliche Frontend-Funktion des Pferdeateliers erforderlich. Alle vier sind Diagnose-, Analyse- oder Exportwerkzeuge.

1. Pferdeatelier eBay – Ein-Klick-Sichtbarkeitsdiagnose 1.0.0
- Zweck laut Pluginbeschreibung: nur lesender Gesamtabgleich bestehender eBay-Freigaben mit Quellenfrische, Ausgabeobjekten und WordPress-Kampagnen.
- Keine Suche, keine Änderungen.
- Einstufung: Backend-Diagnosewerkzeug; keine Frontend-Funktion.
- Maßnahme: kann deaktiviert bleiben und nur bei einer gezielten eBay-Diagnose wieder aktiviert werden.

2. WordPress Speicheranalyse 1.1.0
- Zweck: Speicher-/Dateianalyse; read-only, optional bestätigte Löschung einzelner Dateien ausschließlich im WPvivid-Backupordner.
- Einstufung: Wartungs-/Analysewerkzeug; keine Frontend-Funktion.
- Maßnahme: deaktivierbar; bei Bedarf für Speicherprüfung wieder aktivieren.

3. SEO-Quellpaket Exporter 1.0.0
- Zweck: exportiert ausschließlich installierte Quellverzeichnisse von SEO-Themenengine und SEO-Redaktionsplan-Compiler als read-only ZIP mit SHA-256-Manifest.
- Einstufung: reiner Entwickler-/Exporthelfer; keine Frontend-Funktion.
- Maßnahme: deaktivierbar; nur für einen erneuten Quellpaket-Export wieder aktivieren.

4. DBStorage Insights 1.2.0
- Zweck: analysiert Datenbankgröße, Autoload-Optionen, Transients, verwaiste Daten, Tabellen-Overhead, Uploads sowie Plugin-/Theme-Speichernutzung.
- Einstufung: Backend-Analysewerkzeug; keine Frontend-Funktion.
- Besonderheit: Im Performance-Bericht ist das Plugin trotz reinem Analysezweck mit 17 registrierten Hooks und 28 geladenen Dateien im Request-Footprint sichtbar. Das beweist nicht, dass es Hauptursache der Langsamkeit ist, aber es läuft im aktiven Stack mit.
- Maßnahme: deaktivierbar; nur bei Datenbank-/Speicheranalyse wieder aktivieren.

Verbindliche Entscheidung:
- Performance Diagnose Safe bleibt als Messwerkzeug aktiv.
- Die vier oben genannten Plugins dürfen als erster KISS-Schritt deaktiviert werden.
- Nicht löschen, solange ihre erneute Diagnosefunktion noch nützlich sein kann.
- Nach Deaktivierung nur Funktionsgleichheit und Messwerte prüfen; keine weiteren Änderungen gleichzeitig.
