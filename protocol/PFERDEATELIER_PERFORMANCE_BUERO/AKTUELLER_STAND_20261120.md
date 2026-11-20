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


## Messung nach Deaktivierung der vier Diagnose-/Analyseplugins – 20.11.2026 12:27

Datei: `pferdeatelier-performance-gesamtanalyse-20261120-122703.json`

Bestätigt:
- aktive Plugins jetzt: 36
- die vier deaktivierten Plugins sind nicht mehr in der aktiven Pluginliste
- Performance Diagnose Safe 6.0.0 bleibt aktiv
- Affiliate-Zentrale 6.72.362 und Template Kit 1.50.616 unverändert aktiv

Vorheriger dokumentierter Stand (08:06):
- p95 ca. 10.039 ms
- Browser-TTFB Ø ca. 5.679 ms
- LCP Ø ca. 6.152 ms
- Peak Memory ca. 212 MB
- maximale interne Cache-Hits 138.483
- Pferdesättel ca. 11.576 ms Wall / ca. 3.690 ms CPU / 320 Queries

Nach Deaktivierung:
- p95 6.267 ms
- Browser-TTFB Ø 4.154 ms
- LCP Ø 4.575 ms
- Peak Memory 214 MB
- maximale interne Cache-Hits 138.943
- Pferdesättel 4.925 ms Wall / 3.116 ms CPU / 327 Queries

Delta des Messblocks:
- p95 ca. -37,6 %
- TTFB ca. -26,9 %
- LCP ca. -25,6 %
- Pferdesättel Wall-Time ca. -57,5 %
- Pferdesättel CPU ca. -15,6 %
- Peak Memory praktisch unverändert
- Cache-Hits praktisch unverändert
- Queryzahl auf Pferdesättel praktisch unverändert

Bewertung:
- Die vier Plugins bleiben deaktiviert. Es ist kein Performance-Nachteil sichtbar; der gemessene Lauf ist deutlich besser.
- Weil vier Plugins gleichzeitig deaktiviert wurden und Server-/Requestzeiten schwanken, ist damit NICHT bewiesen, welches einzelne Plugin welchen Anteil verursacht hat.
- Die unverändert extrem hohen Cache-Hits zeigen: die große wiederholte interne Arbeit im Kategorie-/Produktpfad ist weiterhin vorhanden. Der Hauptengpass ist damit nicht beseitigt.
- Kein Rückbau der vier Plugins nötig.

Nächster KISS-Schritt:
- keine weitere Diagnose-Plugin-Runde;
- als nächstes kleine Design-/Frontend-Helfer auf Zusammenführung bzw. Doppelung prüfen, beginnend mit `Canonical Table Contract V1` und `Pferde Atelier – Anzeigenmarkt & Journal Breadcrumbs`;
- erst Quell-/Funktionsprüfung, dann Änderung.


## Ursachenanalyse nach Referenzlauf 20.11.2026 – Hauptursache eingegrenzt

### 1. Bewiesene Hauptursachenfamilie
Die tiefe Kategorie-Langsamkeit sitzt weiterhin im serverseitigen Kategorie-Produktpfad innerhalb von `the_content`.

Beweis aus dem Profil:
- `/ausruestung/`: Ø 3.120,78 ms, davon `the_content` Ø 958,917 ms.
- `/ausruestung/ausruestung-sattel/`: Ø 5.365,90 ms, davon `the_content` Ø 2.326,703 ms.
- `/ausruestung/ausruestung-sattel/pferdesaettel/`: Ø 7.373,52 ms, davon `the_content` Ø 5.394,826 ms = 73,1 %.
- Pferdesättel hatte dabei weniger DB-Zeit als die Ebene Sattel, aber deutlich mehr CPU- und interne Cachearbeit.
- externe HTTP-Zeit auf diesen Zielrequests: 0 ms.

Aktueller Lauf nach Deaktivierung der vier Diagnoseplugins bestätigt denselben Strukturunterschied:
- Pferdesättel: 4.925,27 ms / CPU 3.116,02 ms / 327 Queries / 138.943 Cache-Hits / 10.530 Misses.
- Satteldecken: 2.960,25 ms / CPU 2.240,42 ms / 318 Queries / 85.599 Cache-Hits / 10.526 Misses.
- Differenz: nur 4 zusätzliche Cache-Misses und 9 Queries, aber 53.344 zusätzliche Cache-Hits und rund 876 ms zusätzliche CPU.
- Beide Requests laden denselben Plugin-/Theme-Dateibestand sowie 36 Scripts / 30 Styles.

Schluss:
Die tiefe Seite braucht nicht wesentlich mehr verschiedene Daten. Sie verarbeitet/liest bereits geladene Daten wesentlich häufiger. Das ist ein CPU-/Wiederholungsproblem im Inhalts-/Produktauswahlpfad, kein primärer Netzwerk-, Asset- oder DB-Miss-Fehler.

### 2. Exakter Quellpfad
Template 1.50.616:
`auto_append_category_tiles_to_content()` -> `render_category_level_v150269()` -> drei Shortcodes:
- `category_product_1`
- `category_product_2`
- `category_product_3`

Affiliate 6.72.362:
`pp_affiliate_slot` -> `shortcode_affiliate_slot` -> `render_affiliate_slot` -> `render_affiliate_slot_for_context` -> `select_campaign_for_slot` -> `select_category_product_campaign_fast_v672171`.

Der gemeinsame Kandidatenaufbau `category_product_shared_rank_base()` wird bereits einmal request-lokal gebaut. Danach läuft für jeden der drei Slots erneut ein eigener Auswahlpfad über die breite Kandidatenbasis:
- slot-spezifische Placement-Prüfung,
- Relevanzband-Bildung,
- Control/Health,
- Provider-Cohort,
- Providerstrategie,
- Bildprüfung,
- strikte Relevanz,
- Shared-Offer/GTIN-Bewertung,
- Provider-Mix,
- bei Bedarf Portal-Fallback.

Mehrere einzelne Gates besitzen bereits request-lokale Ergebnis-Caches. Trotzdem werden die Kandidatenlisten und die nachgelagerten Auswahlstufen pro Slot erneut durchlaufen.

### 3. Historischer Gegenbeweis / gleiche Ursachenfamilie
6.72.171 hatte exakt diesen Problemtyp bereits adressiert:
- historischer Snapshot: 2.012 Produktzeilen, 710 Kandidaten je Slot.
- Shared-Ranking/Wiederverwendung reduzierte isolierte Gesamtarbeit von 1.248,595 auf 249,597 ms (-80,01 %).
- Leaf-Pfad 587,812 -> 59,572 ms (-89,87 %).
- ausgewählte Kampagnen, Reihenfolge, Kandidatenzahl und HTML-Hashes blieben identisch.

Spätere fachlich notwendige Erweiterungen ab 6.72.226/237 haben hinter dem Shared-Base wieder zusätzliche Mehranbieter-, Relevanzband-, Fallback- und Providerarbeit ergänzt. Diese Funktionen bleiben fachlich erforderlich; die Lösung darf sie nicht entfernen.

### 4. Bereits behobene Teilursachen – nicht erneut anfassen
- Template 1.50.616: Child-Page-N+1 bereits beseitigt (813 -> 0 identische Query-Familie).
- Affiliate 6.72.361: verlorene Cross-Slot-Wiederverwendung im eBay Provider-Cohort wiederhergestellt; gleicher Output.
- Affiliate 6.72.362: quadratische GTIN-Prüfung in `multiprovider_reorder_candidates()` auf Set-Lookup umgestellt; isolierter Pfad deutlich schneller, Ausgabe identisch.
Diese Fixes sind real, aber die aktuellen ~139.000 Cache-Hits beweisen, dass weitere Restarbeit im breiten Kategorie-Produktpfad bleibt.

### 5. Gefundene echte Neben-Doppelungen – nicht mit Hauptursache verwechseln
Im aktuellen Quellstand wurden weitere echte Wiederholungen gefunden:
- `campaign_control_base_allows_delivery()` prüft den Provider direkt und `control_partner_gate()` prüft denselben Provider bei vorhandener Partner-ID nochmals.
- der historische Incident-Pfad `category_product_incident_inactive_auto_allowed()` liest für inaktive Kandidaten wiederholt dieselben Incident-Optionen; der 2.012-Zeilen-Historien-Snapshot selbst wird nur einmal pro Request aufgebaut.
- `ebay_public_checkpoint_allows_business_campaign()` normalisiert/sortiert die vollständige BUSINESS-ID-Liste pro erstmals geprüftem eBay-Kandidaten erneut.
- GTIN-Metadaten werden in mehreren späteren Mehranbieter-Stufen erneut abgefragt; die zugrundeliegenden Daten sind im WordPress-Request meist schon im Cache.

Diese Punkte sind real, aber lokale Größenordnungsprüfungen zeigen für einzelne dieser Teilstücke nur Millisekunden bis niedrige zweistellige Millisekunden. Sie werden deshalb nicht als mehrsekündiger Root Cause verkauft und nicht einzeln mit neuen Pluginversionen abgearbeitet.

### 6. Harte Ausschlüsse
Nicht als Hauptursache der tiefen Kategorie belegt:
- externe Provider-HTTP-Aufrufe,
- Footer/Shutdown,
- fehlende Designassets,
- Template-Child-N+1,
- reine Queryanzahl,
- fehlender persistenter Object Cache,
- die vier deaktivierten Diagnoseplugins,
- Astra allein.

Server-/Hostlast kann absolute Zeiten schwanken lassen, erklärt aber nicht den reproduzierbaren URL-/Kandidaten-abhängigen CPU-/Cacheunterschied.

### 7. Zulässiger nächster Rootfix-Ansatz
Kein weiterer Mikrofix.

Nächster technischer Kandidat ist ein gemeinsamer request-lokaler **Kategorie-Produkt-Bundle-Pfad** für `category_product_1..3`:
- Shared Base weiterhin einmal.
- slot-unabhängige Kandidatenarbeit einmal je Kandidat.
- slot-spezifische Placement-/Veto-/Positionsregeln bleiben getrennt.
- alle drei Endergebnisse werden in einem gemeinsamen Durchlauf berechnet und danach nur noch Slot 1/2/3 entnommen.
- keine Freigabe-, Source-, Health-, Bild-, Provider-, GTIN-, Relevanz- oder Fallbackregel entfernen.

Vor einer installierbaren Version zwingend:
1. exakter Alt/Neu-Funktionsdiff,
2. historischer 2.012-Zeilen-/710-Kandidaten-Snapshot A/B,
3. Outputidentität für alle drei Slots und alle Provider-Modi,
4. Positiv-/Negativfälle für unterschiedliche Slot-Placements,
5. Veto/Health/Source/Bild/Fallback identisch,
6. danach erst eine Testversion und ein Live-Messlauf.

Dieser Ansatz geht an die bewiesene Hauptursachenfamilie statt weitere einzelne Symptome zu reparieren.


## Rootfix-Kandidat 6.72.363 – wiederholte Frontend-Lesezugriffe – 20.11.2026

### Exakter Ursachenbeweis
Auf Basis des exakt installierten 6.72.362-Codes (6.72.361-Paket + dokumentierter einzelner GTIN-Set-Patch) wurde der Kategorie-Produktpfad lokal mit 709 Produktkandidaten nachgestellt. Die Größenordnung 709 entspricht dem bereits dokumentierten breiten historischen Pferdesättel-Kandidatenband.

6.72.362 erzeugte in diesem echten Codepfad über category_product_1..3:
- get_option: 2.339
- get_post_meta: 4.936
- home_url: 2.024
- current_time: 709
- ausgewählte Kampagnen: camp-20000 / camp-20011 / camp-20022

Die mehrfach gelesenen Werte sind innerhalb eines normalen Frontend-Requests invariant:
- Control-Settings
- Provider-Channel-State
- Provider-Access-State
- idealo-Settings
- Amazon-Settings
- lokale Portal-ID
- eBay SAFE-Checkpoint-Mitgliedschaft
- bereits aufgelöste Produkt-GTINs
- aktuelles Datum für Kampagnenlaufzeit

Zusätzlich primte der eBay-Source-Cache in Slot 2/3 erneut Post-Metadaten, obwohl die bestehende Source-Allow-Entscheidung für dieselbe Kampagne bereits request-lokal vorlag.

### Lokaler KISS-Kandidat 6.72.363
Eine zentrale Cache-Erlaubnis entscheidet einmalig, ob request-lokale Wiederverwendung sicher ist. Sie ist nur auf normalen Frontend-Requests aktiv. Bei Admin, AJAX, REST, Cron, WP-CLI, externem Object-Cache oder dynamischen Option-/Cache-/Shortcode-Filtern bleibt der historische ungecachte Pfad.

Nach der Änderung im identischen 709-Kandidaten-Test:
- get_option: 2.339 -> 6
- get_post_meta: 4.936 -> 3.710
- home_url: 2.024 -> 1
- current_time: 709 -> 1
- ausgewählte Kampagnen unverändert: camp-20000 / camp-20011 / camp-20022

Reduktion:
- direkte Optionslesungen ca. -99,7 %
- Meta-Lesungen ca. -24,8 %
- wiederholte Portal-URL-Lesungen praktisch vollständig entfernt
- wiederholte Tagesauflösung praktisch vollständig entfernt

Diese Zahlen sind lokale Originalcode-Aufrufzahlen, keine Behauptung über die spätere Live-Millisekundenersparnis.

### Verhaltensprüfung
- 50 normale Matrixfälle über alle fünf Provider-Modi, Hybrid/Produktstrategie, unterschiedliche Slot-Belegung, doppelte GTINs und Partnerfälle: 0 Auswahlabweichungen.
- 20 dynamische Filterfälle: 0 Auswahlabweichungen; Cache fällt wie vorgesehen auf Altweg zurück.
- 9 künstliche Zustandsänderungen zwischen Slot 1/2/3 bei aktivem Dynamic-Fail-safe: 0 Auswahlabweichungen.
- 31 wiederholte breite Originalcode-Läufe vor der finalen Sicherheitsrefaktorierung: identische Auswahl; lokale Medianzeit im Stub-Harness ca. 151,5 -> 115,9 ms. Diese Zeit ist nur ein isolierter lokaler Größenordnungswert.
- frisches finales ZIP: repräsentative Alt/Neu-Abnahme über sechs Provider-/Slot-Kombinationen PASS.

### Strukturschutz finales ZIP
Paket: PFERDEATELIER_AFFILIATE_6.72.363_PERFORMANCE_KISS_TEST.zip
SHA-256: e63a5a6138857dc9e210f64204144ae0da6abde63bd343c620434afb120273cc
- Dateien 66 -> 66
- PHP-Lint 23/23 PASS
- Funktionen 1.562 -> 1.563
- entfernt 0
- neu genau 1: category_product_static_read_cache_allowed_v672363
- statisch gezählte Hook-Registrierungen 194 -> 194
- entfernte Hooks 0
- hinzugefügte Hooks 0
- keine neue Datenbank-/Post-/Option-Schreiblogik
- funktional geänderte Dateien: Control, eBay-Checkpoint/Source-Prime, idealo/GTIN, Output-Portal-ID, Provider-State und Hauptdatei; Readme nur Version/Dokumentation.

### Entscheidung
6.72.363 ist ein TESTKANDIDAT, kein bewiesener Live-Performance-Erfolg.
Der Kandidat darf als nächster einzelner KISS-Schritt über 6.72.362 installiert werden.
Danach exakt dieselbe Performance-Gesamtanalyse ausführen und besonders vergleichen:
- Pferdesättel Wall/CPU
- Cache-Hits
- Satteldecken als Referenz
- p95/TTFB/LCP
- Produktausgabe Slot 1/2/3

Nur bei identischer Funktion und realer Verbesserung wird 6.72.363 als neuer Stand behalten.
