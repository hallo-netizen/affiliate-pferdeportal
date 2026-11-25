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


## KORREKTUR / SPERRE 6.72.363 – Inhaltsprüfung nach Nutzerforderung – 20.11.2026

Die zuvor als Testkandidat bezeichnete 6.72.363 wird ausdrücklich **NICHT installiert**.

### Grund der Sperre
Die vertiefte inhaltliche Prüfung hat einen echten Semantik-Risikofall gefunden:
- `idealo_maybe_upgrade_materialization()` liest `idealo_settings()`,
- schreibt danach `OPTION_NETWORK_IDEALO`,
- und verarbeitet im selben Request anschließend erneut idealo-Zustand.
Eine request-lokale Zwischenspeicherung über diese Schreibgrenze kann einen alten Wert weiterreichen. Damit ist der geforderte Beweis „keine Funktionsänderung“ für die bisherige 6.72.363 nicht erfüllt.

Zusätzlich ist der lokal gemessene Zeitgewinn des breiten 709-Kandidaten-Read-Cache-Ansatzes nur ca. 36 ms Median (ca. 151,5 -> 115,9 ms im isolierten Harness). Das ist real, erklärt aber die mehrsekündige Live-Restlast nicht ausreichend.

### Was trotz Sperre bewiesen wurde
Vergleich rekonstruierter exakter 6.72.362-Funktionsstand gegen 6.72.363:
- 1.562 -> 1.563 benannte Funktionen; entfernt 0.
- 212 -> 212 Hook-/Filter-/Shortcode-Registrierungen; Multimenge identisch.
- Schreibprimitive identisch in Anzahl: update_option 292, add_option 11, delete_option 41, update_post_meta 91, add_post_meta 2, delete_post_meta 14, wp_insert_post 3, wp_update_post 19, wp_delete_post 2, wpdb insert/update/delete/query unverändert.
- Kritische Fachfunktionen byte-/körperidentisch, u.a.:
  - multiprovider_reorder_candidates (6.72.362-GTIN-Set-Fix erhalten),
  - select_category_product_campaign_fast_v672171,
  - product_fill_verified_portal_fallback_v672226,
  - category_product_provider_mix_v672133,
  - ebay_filter_ranked_product_candidates_provider_cohort,
  - campaign_control_allows_delivery,
  - campaign_health_allows_delivery,
  - product_campaign_public_image_ready,
  - campaign_match_rank,
  - render_affiliate_slot_for_context,
  - select_campaign_for_slot.
Diese Belege zeigen, dass kein großer Fachblock entfernt wurde, reichen aber wegen des gefundenen Lese-Schreib-Lese-Risikos NICHT zur Freigabe der Version.

### Ursacheneinordnung aus echter Tiefendiagnose
Pferdesättel Profil:
- Request ca. 7.343 ms,
- CPU ca. 4.220 ms,
- gemessene DB ca. 781 ms,
- 320 Queries,
- 138.129 Object-Cache-Hits,
- 0 ms externe HTTP-Aufrufe.
- 124 gleiche Options-Einzelqueries zusammen ca. 176 ms.
- gesamte options-DB-Zeit ca. 237 ms.
- gesamte postmeta-DB-Zeit ca. 255 ms.
Damit kann das Entfernen wiederholter Options-/Meta-Lesungen allein den mehrsekündigen Rest nicht erklären.

Host-Snapshot im selben Diagnoseblock:
- Load Average ca. 205 / 200 / 223.
- OPcache aktiv, Hit Rate ca. 99,1 %.
Die hohe Hostlast kann absolute Zeiten stark verstärken; sie erklärt aber nicht allein den reproduzierbaren hierarchie-/kandidatenabhängigen Unterschied. Sie ist als zusätzlicher Verstärker, nicht als alleinige Ursache zu behandeln.

### Verbindliche Entscheidung
- 6.72.363: GESPERRT / NICHT INSTALLIEREN.
- Keine neue Pluginversion für diesen kleinen Read-Cache-Block.
- Keine Miniversionen nacheinander.
- Weitere Arbeit wird zu einem größeren, belegten Ursachenblock zusammengefasst.
- Nächster Kandidat erst, wenn:
  1. mehrsekündige Ursachenwirkung quantitativ plausibel ist,
  2. alle 6.72.361-Sicherheitsverträge inklusive Zustandswechsel zwischen Slots erhalten bleiben,
  3. 6.72.362-GTIN-Rootfix erhalten bleibt,
  4. Funktions-/Hook-/Schreib-/Provider-/Fallback-/Veto-/Health-/Bild-/Tracking-Verhalten inhaltlich identisch nachgewiesen ist,
  5. erst danach eine einzige Installationsdatei entsteht.


## Kubio/Astra-Prüfung – 20.11.2026

### Kubio
Belegt:
- Auf den normalen Kategorie-/Unterseiten des letzten PASSIV-Laufs werden keine Kubio-Frontend-CSS/JS-Assets ausgeliefert.
- Trotzdem werden im PHP-Request ca. 294 Kubio-Dateien geladen.
- Pferdesättel und Satteldecken laden denselben Kubio-Grundbestand, unterscheiden sich aber stark:
  - Pferdesättel 4.925 ms / CPU 3.116 ms / 138.943 Cache-Hits
  - Satteldecken 2.960 ms / CPU 2.240 ms / 85.599 Cache-Hits
- Damit ist Kubio als Ursache des route-/kandidatenabhängigen Mehrverbrauchs ausgeschlossen. Kubio kann nur Teil einer gemeinsamen Grundlast sein.
- Die Startseite lädt zusätzlich Kubio-Frontendassets, liegt mit CPU ca. 1.814 ms aber nicht über /ausruestung/ mit ca. 1.880 ms CPU.
- WXR-Stand: 13 saved_in_kubio-Marker, davon 12 mit Wert 1; 98 echte wp:kubio-Blöcke. Unter den betroffenen Seiten sind Start, Impressum, AGB, Datenschutz, Disclaimer, Werbebedingungen und weitere Seiten.
Entscheidung:
- Kubio NICHT jetzt auf Live deaktivieren.
- Permanente Entfernung nur nach Migration der verbleibenden Kubio-Blöcke.
- Ein A/B-Test durch temporäre Deaktivierung auf einer zweiten echten Testkopie ist sinnvoll, um die gemeinsame Grundlast zu quantifizieren. Er ist aber kein Rootfix-Test für Pferdesättel.

### Astra
Belegt:
- Astra ist aktives Theme; auf normalen Seiten werden astra-theme-css, astra-theme-js und astra-live-search geladen.
- Pferdesättel und Satteldecken laden denselben Astra-PHP-Grundbestand (ca. 244 Dateien) und dieselben Astra-Assets, unterscheiden sich trotzdem um ca. 1.965 ms Wall und 876 ms CPU.
- Astra ist damit nicht Ursache des route-/kandidatenabhängigen Hauptunterschieds.
- Das aktuelle Template-Kit ist fachlich stark an Astra gekoppelt. Exakte 1.50.616-Vorgängerstruktur enthält u.a. direkte Astra-Hooks/Filter für:
  - astra_content_before
  - astra_entry_top
  - astra_post_featured_image_condition
  - astra_featured_image_enabled
  - astra_primary_content_top
  - astra_related_posts_query_args / related posts
  - astra_footer_copyright
  - Header/Footer-Builder-Entkopplung
- Quellkommentar des Template-Kits: eigener Pferde-Atelier-Header ersetzt Astra-Header, Astra bleibt aber als Theme für Layout/Content aktiv.
Entscheidung:
- Astra jetzt NICHT deaktivieren/auskommentieren.
- Ein Themewechsel wäre kein sauberer Performance-A/B-Test, sondern verändert den Renderingvertrag und erfordert Design-/Hook-Umbau.
- Astra bleibt, solange kein eigener Theme-Ersatz mit identischer Ausgabe existiert.

### Kategorie-Renderer
Exakter Template-Kit-1.50.616-Code geprüft:
- auto_append_category_tiles_to_content -> render_category_level_v150269
- Template baut Seitentext/Kacheln und ruft dann category_affiliate_layout_v150341.
- category_real_affiliate_products_only_v150341 ruft exakt drei Shortcodes:
  category_product_1, category_product_2, category_product_3.
- Affiliate get_content_context() besitzt bereits request-lokalen Cache; die drei Shortcodes bauen den Seitenkontext daher nicht dreimal vollständig neu.
- Der genaue Anteil der pp_affiliate_slot-Callbacks am mehrsekündigen the_content-Block ist mit Diagnose 6.0 noch nicht direkt gemessen.

### Nächster einzelner KISS-Messschritt
Performance Diagnose Safe 6.1.0 existiert bereits und wurde genau für diese offene Attribution gebaut.
Es verändert keine Produktionsplugins/-daten und ergänzt:
- tatsächliche Laufzeit jedes Shortcodes inkl. pp_affiliate_slot mit type/intent,
- the_content-Prioritätsbänder,
- the_content-Callback-Inventar.
QA: keine neuen Post-/Meta-/Cron-/DB-Schreibwege; Shortcode- und the_content-Rückgabewerte in Sicherheitssimulation unverändert.

Damit soll genau EIN Profillauf die noch offene Frage entscheiden, bevor ein weiterer Produktionsplugin-Kandidat gebaut wird.


## Dauerhafte Diagnose-Version 7.0.0 – 20.11.2026

### Anlass
Die bisherige 6.1 deckte bereits den Großteil der WordPress-Performanceanalyse ab, hatte aber fünf Lücken, die zu erneuten Diagnose-Erweiterungen geführt hätten:
1. eingeloggte/Admin-Bar-Frontendrequests wurden nicht getrennt von anonymen Requests ausgewertet;
2. Astra/Kubio wurden nur als Datei-/Hook-Fußabdruck erfasst, nicht als Routenvergleich;
3. es gab keinen dauerhaft gespeicherten Vorher/Nachher-Referenzlauf;
4. Host-Load wurde nicht gegen sichtbare CPU-Kapazität normalisiert;
5. aktive Plugin-/Theme-Quellen wurden nicht vollständig als SHA-256-Fingerprints festgehalten.

### 7.0.0 ergänzt
- Frontendstatus: logged-in / anonymous / Admin-Bar / private-no-cache.
- Komponenten-Routenvergleich für Astra, Kubio, Affiliate, Template-Kit, HivePress, WPForms, Site Kit, Yoast.
- Komponenten-Asset-Zusammenfassung und Hook-Inventar in Profil-/Tiefenmodi.
- vollständige Fingerprints der Hauptdateien aller aktiven Plugins plus aktives Theme.
- sichtbare logische CPU-Anzahl und Load-per-CPU, sofern PHP diese Informationen lesen kann.
- eigener gespeicherter Referenzlauf und automatischer Vergleich identischer Routen: Dauer, CPU, Cache-Hits, Queries.
- expliziter Coverage-Vertrag: Für abgedeckte WordPress-Level-Fragen wird künftig dieselbe Diagnose weiterverwendet.
- Server-Level-Grenzen werden ausdrücklich ausgewiesen und dürfen NICHT zu einem weiteren WordPress-Diagnoseplugin führen.

### Sicherheitsbeweis 6.1 -> 7.0
- Klassenmethoden: 146 -> 157.
- entfernt: 0.
- bestehende Methoden vollständig unverändert: 137.
- geänderte bestehende Methoden: ausschließlich Diagnose-Session/Export/Snapshot/Auswertung/Adminoberfläche/Request-Kontext.
- Hook-/Filter-/Shortcode-Registrierungen: 34 -> 36.
- entfernt: 0.
- neu ausschließlich zwei eigene Admin-Aktionen für Referenz speichern/löschen.
- keine Post-, Postmeta-, Term-, Cron-, Cache-, Theme- oder Plugin-Aktivierungs-/Deaktivierungs-Schreibwege.
- neue Schreiboperation ausschließlich eigene Diagnose-Referenzoption.
- PASSIV liest für Kubio keinen zusätzlichen Seiteninhalt/Meta; Kubio-Inhaltsbeweis nur Profil/Tiefenanalyse, damit PASSIV sauber bleibt.
- lokaler Hilfsfunktions-Harness PASS: Komponenten-Routenvergleich, logged-in/private Gruppierung, Baseline-Deltas, Coverage-Vertrag.
- PHP-Lint PASS.
- ZIP-Test PASS.

### Paket
- Datei: PERFORMANCE_DIAGNOSE_SAFE_7.0.0_DAUERHAFT_ALL_IN_ONE.zip
- SHA-256: f90de7be50b886af631923673ab77d098cf5c5b4d964a6a447974794dab532d2
- gleicher Plugin-Ordner: pa-performance-diagnose-safe
- ersetzt die bisherige Diagnose; erzeugt kein zusätzliches paralleles Plugin.

### Verbindlicher Dauervertrag
Keine neue Diagnose-Pluginversion nur wegen einer neuen Performancefrage, solange die Frage innerhalb des dokumentierten WordPress-Level-Coverage-Vertrags liegt.

Harte Grenzen, die ein WordPress-Plugin nicht sicher vollständig messen kann:
- exakte CPU-Zeit jedes beliebigen fremden PHP-Callbacks ohne invasives Wrapping,
- PHP-FPM-Worker-Queue/Sättigung ohne Status-Endpunkt/Serverzugriff,
- Host-/Container-Throttling und Nachbarlast außerhalb des PHP-Prozesses,
- Kernel-/Paket-Netzwerkprofiling.

Für diese Punkte ist bei Bedarf Serverzugriff/Profiler nötig, NICHT ein weiteres Diagnoseplugin.


## Ursachenprofil 7.0.0 – 20.11.2026 15:53

Quelle: `pferdeatelier-performance-gesamtanalyse-20261120-155347.json`
Modus: PROFILE
Diagnose: 7.0.0
Affiliate: 6.72.362
Template Kit: 1.50.616
Astra: 4.14.3
Kubio: 2.9.5

### Direkter Hauptursachenbeweis
Pferdesättel:
- Gesamt 5967,34 ms
- CPU 3462,75 ms
- DB 730,03 ms
- 320 Queries
- 139002 Cache-Hits
- externe HTTP 0 ms

Satteldecken:
- Gesamt 3009,60 ms
- CPU 2126,22 ms
- DB 623,81 ms
- 311 Queries
- 85590 Cache-Hits
- externe HTTP 0 ms

Direkt gemessene Kategorie-Produktshortcodes:
Pferdesättel:
- category_product_1: 1684,421 ms
- category_product_2: 622,356 ms
- category_product_3: 691,347 ms
- Summe: 2998,124 ms

Satteldecken:
- category_product_1: 596,619 ms
- category_product_2: 66,034 ms
- category_product_3: 62,292 ms
- Summe: 724,945 ms

Differenz der drei Produktplätze: 2273,179 ms.
Gesamtdifferenz Pferdesättel vs. Satteldecken: 2957,74 ms.
Damit erklären die drei Kategorie-Produktplätze ca. 76,9 % des gesamten Seitenunterschieds direkt.

Zusätzlicher Slot `product_after_category_tiles`:
- Pferdesättel 447,486 ms
- Satteldecken 450,942 ms
=> praktisch identisch und damit kein Erklärer des Differenzproblems.

### Bedeutung
Der Hauptunterschied ist jetzt nicht mehr nur über `the_content` indirekt eingegrenzt, sondern direkt auf die Affiliate-Shortcodes `category_product_1..3` gemessen.
Besonders:
- Slot 1 trägt bei Pferdesättel 1684 ms.
- Slots 2/3 bleiben mit 622/691 ms ebenfalls sehr teuer.
- Bei Satteldecken fallen Slots 2/3 nach dem ersten Slot auf nur 66/62 ms.

Das beweist:
1. Slot 1 enthält teure gemeinsame Erstberechnung.
2. Die gemeinsame Wiederverwendung funktioniert bei kleinerem Kandidatenbestand weitgehend.
3. Bei breitem Pferdesättel-Bestand bleibt nach der gemeinsamen Erstberechnung weiterhin umfangreiche slotabhängige Kandidatenarbeit.
4. Der nächste Rootfix muss exakt diese Restarbeit hinter dem Shared-Base treffen; kein allgemeiner Plugin-/Theme-Fix.

### Astra/Kubio
Pferdesättel und Satteldecken laden denselben Grundbestand:
- Kubio ca. 294 inkludierte PHP-Dateien
- Astra ca. 244 inkludierte PHP-Dateien
- auf beiden Zielseiten keine Kubio-Frontendassets
- Astra-Assets auf beiden gleich

Damit sind Astra/Kubio als Ursache des ca. 2,96-s-Routenunterschieds ausgeschlossen.
Sie können Grundlast erzeugen, erklären aber nicht das bewiesene Kandidaten-/Slot-Skalierungsproblem.

### Weitere Systembefunde
- p95 5189 ms
- Browser-TTFB Ø 3796 ms
- LCP Ø 4165 ms
- Peak Memory 228 MB
- kein persistenter Object Cache
- Host-Load während Profil sehr hoch: ca. 145/145/151; CPU-Anzahl aus PHP nicht sichtbar
- OPcache kurz vor Messung neu gestartet; Messung deshalb nicht als saubere absolute Produktionsbenchmark behandeln.
- PROFILE liefert Ursachenattribution; PASSIV bleibt maßgeblich für saubere Wall-Time-Benchmarks.

### Entscheidung
- Kein neues Diagnoseplugin.
- Kein Astra-/Kubio-Umbau als nächster Schritt.
- Kein 6.72.363-Read-Cache-Ansatz.
- Nächster Produktionskandidat darf nur den direkt bewiesenen category_product_1..3-Restpfad optimieren.
- Fachlogik für Placement, Control, Health, Bilder, Provider, GTIN, Relevanzbänder, Mix und Fallback darf nicht reduziert werden.
- Vor Installation: Alt/Neu gegen breiten 709/710-Kandidaten-Bestand und mehrere Provider-/Fallback-/Placement-Zustände, 0 Ausgabeabweichungen.


## Fortsetzung nach Ursachenprofil 7.0 – exakter Live-6.72.362-Pfad – 20.11.2026

### Live-Quellstand exakt rekonstruiert
Basis war das gesicherte Paket `PFERDEATELIER_AFFILIATE_6.72.361_PERFORMANCE_ROOTFIX_FINAL_TEST.zip` plus ausschließlich der dokumentierte 6.72.362-GTIN-Set-Patch.

Die Rekonstruktion trifft die Fingerprints des aktuellen Live-Berichts exakt:
- Hauptdatei 839887 Byte / SHA-256 `173ca294b3c90621daa8a95d674bbdcb6c42e1cf6e5da55a52610c40ea16b040`
- eBay-Trait `d97756b0c73c791dfa10be636bebcbf1220d9c35f43f648e79638ac9b0ac2e83`
- eBay-Run `bac0dd05a8f128778b9c7e6e69634b51e3abcaaddcd23155b5050e48fd99fa0d`
- eBay-Deletion `65265a0dfb611936f4f5457d997ae018c65bffdd24e71d979875215a108a02fc`
- Digistore `f6f6e9ea787de07ee709c3da6fc4c9764d6993d53b6e33c4b5f102d706e3d488`

Damit beziehen sich die folgenden Aussagen auf den tatsächlich installierten 6.72.362-Code, nicht auf den veralteten release/current-Arbeitsstand.

### Direkt bewiesener Slotpfad
`select_category_product_campaign_fast_v672171`:
1. Shared Rank Base einmal request-lokal.
2. pro Slot Placement/Bands.
3. Control/Health.
4. eBay Provider Cohort.
5. Providerstrategie.
6. Bild.
7. Strict-Relevance-Guard.
8. Shared-Offer/GTIN.
9. Provider-Mix.
10. bei <3 Treffern Portal-Fallback.

Bereits request-lokal gecacht:
- Shared Rank Base
- Control-Basis und slotweites Control-Veto
- Health
- Bildfreigabe
- eBay Provider-Cohort-Ergebnis seit 6.72.361

### Verworfen: lokaler 6.72.364-GTIN-Kandidat
In `multiprovider_prefer_shared_offer_cards()` existiert zwar formal noch eine quadratische Zeile:
`array_intersect($gtins, array_keys($shown))`.

Isolierter Test:
- 4430 Alt/Neu-Semantikfälle, 0 Abweichungen.
- 710 Kandidaten: isolierter Funktionsblock ca. 96–248 ms alt vs. ca. 3–6 ms mit direktem Set-Lookup, je nach GTIN-Verteilung.

ABER der exakte Kategorie-Aufrufweg widerlegt die Live-Ursächlichkeit:
- Vor `multiprovider_prefer_shared_offer_cards()` läuft im eBay-Cohort bereits `multiprovider_reorder_candidates()`.
- In den einzigen Modi, in denen Shared-Offer die GTIN-Bewertung aktiviert (`combined`/`automatic`), setzt `multiprovider_reorder_candidates()` für die zurückgegebenen Kandidaten bereits `_ppar_product_provider_count`.
- Shared-Offer überspringt dann per `isset($candidate['_ppar_product_provider_count'])` seinen erneuten GTIN-Identitätsaufbau.
- Damit ist der isolierte quadratische Block im relevanten schnellen Kategoriepfad nicht als Hauptursache bewiesen.

Entscheidung:
- 6.72.364 NICHT ausgeben / NICHT installieren.
- Kein Produktionsfix aus einem isoliert schnellen, aber im Livepfad nicht nachgewiesenen Block.

### Ebenfalls geprüft und ausgeschlossen
`category_product_provider_mix_v672133`:
- sichere Index- statt array_shift-Variante über 1065 Fälle outputidentisch.
- bei 710 Kandidaten nur ca. 0,16 ms absoluter lokaler Gewinn.
=> nicht ursächlich genug, bleibt unverändert.

eBay-Titel-Dubletten-Vorfilterung:
- sichere Längenbucket-Variante auf 100/200/300 Kandidaten gemessen.
- nur wenige Prozent / wenige Millisekunden, teils sogar langsamer.
=> nicht anfassen.

### Was der 7.0-PROFILE-Lauf noch beweist
Pferdesättel vs. Satteldecken:
- gleiche Astra-/Kubio-Grundkomponenten.
- DB-Unterschied nur ca. 106 ms.
- externe HTTP 0 ms auf beiden.
- drei category_product-Slots erklären ca. 2273 ms bzw. 76,9 % der gesamten Routendifferenz.
- Pferdesättel: 139002 Cache-Hits.
- Satteldecken: 85590 Cache-Hits.
- Differenz: 53412 Cache-Hits bei nur geringem Query-/DB-Unterschied.

PROFILE hängt absichtlich keine cache-sensiblen Deep-Observer an. Deshalb stehen `targeted_trace.get_post_metadata` usw. im Profil auf 0; die 53412 zusätzlichen Cache-Hits können damit noch nicht einem internen Callsite-Zweig zugeordnet werden.

### Nächster EINZIGER Messschritt – vorhandenes Plugin, keine Neuinstallation
Mit der bereits installierten Performance Diagnose Safe 7.0:
- Modus `Frontend-Tiefenbeweis` / `deep_frontend`
- ausschließlich zwei Frontendseiten je einmal:
  1. /ausruestung/ausruestung-sattel/pferdesaettel/
  2. /ausruestung/ausruestung-sattel/satteldecken/
- danach stoppen und Gesamtanalyse JSON exportieren.

Ziel dieses einen Laufs:
- exakte Zahl `get_post_metadata`, `get_term`, `sanitize_key`
- gesampelte Top-Callsites mit Plugin + Datei + Funktion
- Querypattern-Attribution
- dadurch Beweis, ob Restlast aus Fallback, eBay-Cohort-Key-Aufbau, GTIN-Metadaten, Source-/Provider-Gates oder einem anderen konkreten Zweig stammt.

Der Tiefenlauf ist KEIN Wall-Time-Benchmark; die 7.0-Diagnose dokumentiert selbst, dass Deep-Observer Zusatzlast erzeugen. Für absolute Zeiten bleibt PROFILE/PASSIV maßgeblich. Der Deep-Lauf dient ausschließlich der Ursachenattribution.


## Rootfix-Kandidat 6.72.365 – Kategorieprodukt-Bundle – 20.11.2026

### Ausgangsbeweis / Ursache
Maßgeblich bleibt der saubere PROFILE-Lauf 7.0:
- Pferdesättel: category_product_1/2/3 zusammen 2998,124 ms.
- Satteldecken: dieselben drei Slots zusammen 724,945 ms.
- Differenz der drei Slots: 2273,179 ms = ca. 76,9 % der gesamten Routendifferenz.
- Slot 2/3 Pferdesättel bleiben mit 622/691 ms teuer, während Satteldecken nach Slot 1 auf 66/62 ms fällt.
Damit ist die wiederholte Kategorieprodukt-Nachbearbeitung direkt als Ursachenfamilie gemessen.

Wichtige Korrektur zum DEEP-Lauf 16:32:
- DEEP hängt selbst Beobachter an sanitize_key/get_post_metadata usw.
- 6.72.362 deaktiviert bei solchen dynamischen Filtern bewusst bestimmte Request-Caches.
- Die dort gemessenen absoluten sanitize_key-/Meta-Zahlen sind deshalb kein sauberer Produktions-Wall-Time-Beweis.
- DEEP bleibt für Callsite-/Breitenhinweise nutzbar; PROFILE bleibt Kausal-/Zeitreferenz.

### Exakter Quellstand
6.72.362 wurde aus dem gesicherten 6.72.361-Paket + ausschließlich dem dokumentierten 6.72.362-GTIN-Set-Patch rekonstruiert.
Fingerprints stimmen mit Live überein; Änderungen werden gegen diesen Stand geprüft.

### Was 6.72.365 ändert
Ausschließlich category_product_1..3:
- Die historische Nachbearbeitungssequenz bleibt identisch:
  eBay/Provider-Cohort
  -> Providerstrategie
  -> Bildfreigabe
  -> Strict-Relevance-Guard
  -> Shared-Offer/GTIN
  -> Provider-Mix.
- Wenn Slot 2/3 mit dem exakt gleichen vollständigen Kandidatenzustand und unveränderten Provider-/Amazon-Einstellungen kommen, wird nicht die komplette Nachbearbeitung erneut ausgeführt.
- Wiederverwendet wird nur ein Auswahlplan:
  geordnete Post-IDs + bestehende _ppar_product_provider_count-Markierung.
- Kandidaten selbst werden auf Cache-Treffer aus dem aktuellen Slot-Input neu zusammengesetzt.
- Schon eine beliebige Änderung im vollständigen Kandidatenarray erzeugt einen anderen Schlüssel und erzwingt den alten 6.72.362-Weg.
- Bei dynamischen Meta-/Option-/Shortcode-/Sanitizer-/Image-Filtern, externem Object Cache, Admin/AJAX/REST/Cron/CLI, fehlender Runtime-Normalisierung, fehlender/duplizierter Post-ID oder Nicht-Kategorie-Slot wird der historische Weg benutzt.

### Inhaltlicher Funktionsbeweis
- Die sechs wiederverwendeten Nachbearbeitungsschritte behandeln category_product_1, _2 und _3 in ihrem ausführbaren Code als dieselbe Slotfamilie; keine Sonderentscheidung nur für 1, 2 oder 3.
- Transitive Quellprüfung ab diesen sechs Schritten: 62 erreichbare Funktionen bis Tiefe 7.
- In diesem erreichbaren Auswahlbaum: 0 WordPress-Schreiboperationen (keine Option-/Meta-/Post-/Transient-/Cron-/direkte DB-Schreibung).
- Kandidatenmutation im alten Nachbearbeitungsweg: ausschließlich bestehende Request-Markierung _ppar_product_provider_count; kein Kampagneninhalt wird verändert.
- Genau diese Markierung wird im Auswahlplan erhalten; alle übrigen Felder stammen stets aus dem aktuellen Kandidatenarray.

Semantiktests:
- Auswahlplan-Mechanismus auf echtem 6.72.365-Code: 12.000 Zufallsfälle, 0 Abweichungen.
- Jede zufällige inhaltliche Änderung eines Kandidaten invalidierte den Schlüssel.
- Dynamic-filter / unnormalisiert / doppelte Post-ID / Nicht-Kategorie: Fastpath jeweils korrekt gesperrt.
- Provider-/GTIN-/Mix-Matrix mit den unveränderten historischen Funktionskörpern: 2.266 Fälle, 0 Ausgabeabweichungen.
- enthalten: alle fünf Provider-Modi, kleine/mittlere/breite Mengen bis 710 Kandidaten, veränderte Slot-Inputs, GTIN-/Amazon-/Providerzustände.

### Struktureller Funktionsschutz 6.72.362 -> 6.72.365
- Dateien 66 -> 66; entfernt 0; hinzugefügt 0.
- Geänderte Dateien nur Hauptdatei + readme.
- Benannte Funktionen 1552 -> 1555.
- bestehende Funktionen entfernt: 0.
- neu exakt 3 interne Performance-Helfer.
- bestehende Funktionskörper geändert: exakt 1, select_category_product_campaign_fast_v672171; dort wird die unveränderte historische Mittelsequenz lediglich an den neuen Helper delegiert.
- Gate-Reihenfolge Alt/Neu identisch:
  Control -> Health -> Cohort -> Providerstrategie -> Bild -> Relevanz -> Shared Offer -> Provider-Mix -> Fallback.
- Shared Base, Control, Health, Bild, Fallback, Strict Relevance, Provider Mix vollständig unverändert.
- sämtliche eBay-/idealo-/Amazon-Traits unverändert.
- 6.72.362-GTIN-Set-Fix bleibt unverändert erhalten.
- Hooks/Filter/Shortcodes 214 -> 214, Multimenge identisch.
- alle gezählten Produktions-Schreibwege identisch:
  update_option 290, add_option 7, delete_option 37,
  update_post_meta 80, add_post_meta 1, delete_post_meta 9,
  wp_insert_post 3, wp_update_post 12, wp_delete_post 1,
  set_transient 11, delete_transient 12,
  wp_schedule_event 9, wp_schedule_single_event 36, wp_clear_scheduled_hook 34.
- kein Schreib-Callsite hinzugefügt/entfernt.

### Kausaler lokaler Performance-A/B
Gleicher Postprocessing-Block dreimal (Alt) gegen einmal + Auswahlplan-Wiederverwendung (Neu), mit vollständigem Kandidaten-Hash und Planrekonstruktion:
- 43 Kandidaten: 0,675 -> 0,292 ms, -56,7 %.
- 196 Kandidaten: 15,123 -> 5,345 ms, -64,66 %.
- 710 Kandidaten: 283,821 -> 94,575 ms, -66,68 %.
Diese lokale Messung beweist die Wirkung exakt in dem geänderten Wiederholungsblock; sie ist keine Vorhersage der gesamten Live-Seitenzeit.

### Finales Paket
PFERDEATELIER_AFFILIATE_6.72.365_CATEGORY_PRODUCT_BUNDLE_ROOTFIX_TEST.zip
SHA-256: c4e84a067c11bc239e65502ec1ead75abc1aef71bbd3e6cf6a477e785b2e9902
- ZIP-Test PASS
- 66/66 Dateien nach Entpacken byteidentisch zum geprüften Kandidaten
- PHP-Lint 23/23 PASS
- exakt aus finaler ZIP erneut 12.000 Auswahlplan-Fälle: 0 Abweichungen.

### Bewusst NICHT aufgenommen
- 6.72.363 Read-Cache: gesperrt, Semantikrisiko idealo-Upgrade und zu kleiner Effekt.
- verworfener 6.72.364 Shared-Offer-GTIN-Mikrofix: isoliert schnell, aber im realen Kategoriepfad nicht ausreichend ursächlich.
- Provider-Mix array_shift: <1 ms / nicht relevant.
- doppelte Strategieprüfung: <1 ms / nicht relevant.
- eBay-Titel-Prefilter: wenige ms / nicht stabil besser.
- Designplugin-Zusammenlegung: kein spürbarer Performancebeweis.
- Astra/Kubio: nicht Ursache des routeabhängigen Hauptdeltas.

### Freigabevertrag
6.72.365 ist der erste installierbare Produktions-Testkandidat nach 6.72.362.
Nach Installation genau ein sauberer PROFILE/PASSIV-Vergleich gegen die bestehende Referenz.
Behalten nur wenn:
1. Produktausgabe/Provider/Fallback/Veto/Health/Bilder/Tracking unverändert,
2. category_product_2/3 und Gesamtroute real schneller,
3. keine neue Regression auf Satteldecken/anderen Referenzseiten.


## Zusatzvergleich Testumgebung vor 6.72.365 – Diagnose 21.11.2026 08:23

Quelle: pferdeatelier-performance-gesamtanalyse-20261121-082340.json
Modus: PASSIV
Testumgebung: oliver-beil.de
Affiliate: 6.72.362
Template Kit: 1.50.616
Astra: 4.14.3
Kubio: 2.9.5

### Codegleichheit
Die relevanten Produktionsquellen sind zwischen Test und Live identisch:
- Affiliate-Hauptdatei SHA-256 173ca294b3c90621daa8a95d674bbdcb6c42e1cf6e5da55a52610c40ea16b040
- Template Kit SHA-256 4daf54d7911833e29a60d9397ec824cd0c24232b3e927d3af2ebd65a754389aa
Damit ist der getestete 6.72.362-Codepfad derselbe.

### Testwerte
Pferdesättel Test:
- 3523,56 ms Wall
- 2804 ms CPU
- 117537 Cache-Hits
- 277 Queries
- 0 externe HTTP-Aufrufe

Live-Referenz vor 6.72.365:
- 4925,27 ms Wall
- 3116,02 ms CPU
- 138943 Cache-Hits
- 327 Queries

Differenz Test zu Live:
- Wall ca. 28,5 % niedriger
- CPU ca. 10,0 % niedriger
- Cache-Hits ca. 15,4 % niedriger
- Queries ca. 15,3 % niedriger

### Wichtig: kein 1:1-Benchmark
Die Umgebungen sind nicht identisch:
Test:
- WordPress 7.1.3
- WP_DEBUG aktiv
- WP-Cron aktiv
- kein Zend OPcache
- 48 aktive Plugins
- 64 sichtbare logische CPUs
- Load ca. 26-28, load_per_cpu ca. 0,41-0,44
- Datenbestand u.a.: wp_posts 7338, wp_postmeta 43802, ppar_ebay_items 6077, ppar_output_objects 3613, ppar_creative_library 1627

Live-Referenz:
- WordPress 7.1.5
- WP_DEBUG aus
- WP-Cron deaktiviert
- Zend OPcache aktiv, Hit Rate ca. 99,9 %
- 36 aktive Plugins
- rohe Host-Load im Referenzlauf ca. 263-309+ (CPU-Anzahl in der alten Diagnose nicht erfasst)
- Datenbestand größer: posts 10028, postmeta 90254, ppar_ebay_items 8114, ppar_output_objects 4389, ppar_creative_library 2356

Daher sind absolute Sekundenwerte zwischen Test und Live nicht als A/B-Beweis zulässig.

### Robuster gemeinsamer Befund
Trotz kleinerem Datenbestand und anderer Serverumgebung ist Pferdesättel auch auf Test der Request mit maximalen Cache-Hits:
- 117537 Hits.
Die Breiten-/Wiederholungsproblematik des Affiliate-Kandidatenpfads bleibt damit sichtbar.

Auf Test:
- Pferdesättel 117537 Cache-Hits
- Ausrüstung/Sattel 68155
- Ausrüstung 49999

Das stützt die bereits live bewiesene Skalierung mit breiterem Kategorieproduktbestand.

### Entscheidung
6.72.365 bleibt als nächster Produktions-Testkandidat freigegeben.
Der Testumgebungs-Lauf ändert den Funktionsvertrag nicht und liefert keinen Gegenbeweis.
Nach Installation auf Test und Live:
- jeweils PASSIV auf identischen Routen messen,
- absolute Test-vs-Live-Zeiten nicht gegeneinander werten,
- jeweils nur Vorher-vs-Nachher innerhalb derselben Umgebung vergleichen.


## Live-Abnahme 6.72.365 – Diagnose 21.11.2026 08:28

Quelle: pferdeatelier-performance-gesamtanalyse-20261121-082829.json
Modus: PASSIV
Live: pferde-atelier.de
Affiliate-Zentrale aktiv: 6.72.365
Template Kit: 1.50.616
Aktive Plugins: 36

### Harte Vorher-/Nachher-Werte auf Pferdesättel

Vorher 6.72.362:
- Wall 4925,27 ms
- CPU 3116,02 ms
- Cache-Hits 138943
- Queries 327

Nachher 6.72.365:
- Wall 5721,16 ms
- CPU 3264,16 ms
- Cache-Hits 139257
- Queries 320

Differenz:
- Wall +16,16 %
- CPU +4,75 %
- Cache-Hits +0,23 % = praktisch unverändert
- Queries -2,14 %

Der vertraglich erwartete Rückgang der extremen internen Cachezugriffe ist NICHT eingetreten. 6.72.365 ist damit als Performance-Rootfix live nicht bestätigt.

### Gesamtwerte nicht als Plugin-Erfolg wertbar
6.72.365-Lauf:
- p95 3930 ms
- TTFB Ø 3339 ms
- LCP Ø 3720 ms
- Peak 230 MB

Vorheriger 6.72.362-Lauf:
- p95 6267 ms
- TTFB Ø 4154 ms
- LCP Ø 4575 ms
- Peak 214 MB

Diese Gesamtverbesserung ist nicht dem Plugin zurechenbar:
- Server-Load war im neuen Lauf deutlich niedriger (ca. 90-141 statt ca. 263-340 im alten Referenzlauf).
- Der neue Lauf lag nur 122 Sekunden nach einem OPcache-Neustart.
- Zielseite Pferdesättel wurde trotz besserer Host-Situation langsamer.

### Nachgewiesener Versionskettenfehler

Lokaler Quellvergleich der vorhandenen Testpakete:
- 6.72.363 enthält category_product_static_read_cache_allowed_v672363 und die dazugehörigen request-lokalen Caches für unveränderte Options-/Meta-/Portal-/Datumszustände.
- 6.72.364 enthält diesen 6.72.363-Block NICHT mehr.
- 6.72.365 baut auf 6.72.364 auf und enthält ihn ebenfalls NICHT.
- 6.72.365 unterscheidet sich von 6.72.364 nur in drei Dateien: Hauptdatei, trait-ppar-idealo.php, readme.txt.
- Damit wurde die 6.72.363-Wiederholungsbremse beim Übergang zu 6.72.364 verloren und in 6.72.365 nicht wieder aufgenommen.

Zusätzlicher nachgewiesener Performance-Rückschritt:
- 6.72.363/6.72.364 prüfen bereits gesehene GTINs per direktem Set-Lookup.
- 6.72.365 stellt diese Stelle wieder auf array_intersect($gtins, array_keys($shown)) um.
- Semantik gleich, aber der bereits beseitigte lineare/Listen-Aufwand wurde wieder eingeführt.

### Entscheidung
Keine weitere Diagnose mit 6.72.365 nötig.
Nächster zulässiger Fix muss kumulativ sein:
1. 6.72.365 als Funktionsbasis behalten.
2. 6.72.363 request-lokale Invariant-Read-Caches vollständig wieder integrieren.
3. 6.72.364 direkten GTIN-Set-Lookup beibehalten.
4. 6.72.365 Bundle-Plan nur zusätzlich behalten; keine bestehende Funktion entfernen.
5. Vor Ausgabe Struktur-, Funktions-, Auswahl- und Mutationsregressionen gegen alle drei Vorgänger prüfen.


## 6.72.366 – bewiesener WordPress-Standardfilter-Rootfix – 21.11.2026

### Harte Ursache des 6.72.365-Live-Fehlschlags
6.72.365 sperrt seinen neuen category_product-Postprocess-Plan-Cache, sobald
`has_filter('http_request_host_is_external')` wahr ist.
Dieselbe Bedingung sperrt auch den vorhandenen request-lokalen Bildfreigabe-Cache.

WordPress registriert im Core standardmäßig:
`add_filter('http_request_host_is_external', 'allowed_http_request_hosts', 10, 2)`.
Die Live-Diagnose weist `multisite=false` aus.
Damit war die Sperrbedingung auf jeder normalen Live-Anfrage bereits durch WordPress selbst erfüllt – auch ohne Fremdplugin.
Folge: Der in 6.72.365 lokal bewiesene Bundle-Fastpath konnte auf Live nicht aktiv werden. Dies erklärt, warum Pferdesättel nach 6.72.365 weiterhin 139257 Cache-Hits hatte gegenüber 138943 auf 6.72.362.

### Korrektur
6.72.366 unterscheidet WordPress-Standardcallback von echten Fremd-/dynamischen Eingriffen:
- erlaubt: kein Callback
- erlaubt: ausschließlich `allowed_http_request_hosts`
- auf Multisite zusätzlich erlaubt: `ms_allowed_http_request_hosts`
- sobald irgendein weiterer/unbekannter Callback registriert ist: alter 6.72.365-Sicherheitsweg, kein Cache.

Dies gilt an beiden Stellen derselben Ursache:
1. category_product_postprocess_plan_cache_allowed_v672365
2. category_product_public_image_ready

Keine Ranking-, Auswahl-, Provider-, GTIN-, Fallback-, Control-, Health-, Bild-, Tracking- oder Renderingregel wird geändert.

### Kausale Simulation
WordPress-ähnlicher Hook-Harness:
- kein Hostfilter: Alt erlaubt / Neu erlaubt
- WordPress-Standardfilter allein: Alt sperrt / Neu erlaubt
- Standard + Fremdfilter: Alt sperrt / Neu sperrt
- Standard + Closure: Alt sperrt / Neu sperrt

710-Kandidaten-Simulation, 3 Kategorie-Slots:
- 6.72.365 unter WordPress-Standardhook: vollständiger Postprocess 3x
- 6.72.366: vollständiger Postprocess 1x + bestehender Auswahlplan 2x
- Ausgabe-Hash identisch
- Bildprüfungen 2130 -> 710
- lokaler Harness dieses Aktivierungsfehlers: 9,380 -> 4,721 ms (-49,67 %) bei identischer Ausgabe.
Dieser Harness misst die Aktivierung/Mehrfacharbeit, nicht die komplette Live-Seitenzeit.

Bereits bestehender und unveränderter 6.72.365-Postprocess-Beweis, der nun erstmals unter WordPress-Standardhook aktiv werden kann:
- 43 Kandidaten: 0,675 -> 0,292 ms (-56,7 %)
- 196 Kandidaten: 15,123 -> 5,345 ms (-64,66 %)
- 710 Kandidaten: 283,821 -> 94,575 ms (-66,68 %)

### Inhaltlicher Sicherheitsbeweis
12.000 randomisierte Guard-/Plan-Fälle:
- 0 Ausgabeabweichungen
- 0 Guard-Abweichungen
- wechselnde Slotinputs enthalten
- bei Fremdcallback bleibt der historische 3x-Weg erhalten.

### Byte-/Strukturschutz 6.72.365 -> 6.72.366
Finales, frisch entpacktes ZIP gegen exaktes Live-6.72.365-Paket:
- Dateien 66 -> 66
- entfernt 0
- hinzugefügt 0
- geänderte Dateien nur:
  - pferdeportal-affiliate-router.php
  - readme.txt
- benannte Funktionen: entfernt 0
- neu exakt 1:
  - category_product_http_host_filter_default_only_v672366
- geänderte bestehende Funktionen exakt 2:
  - category_product_postprocess_plan_cache_allowed_v672365
  - category_product_public_image_ready
- Hooks/Filter/Shortcodes 212 -> 212, exakt identisch
- Produktions-Schreibprimitive vollständig identisch:
  update_option 290, add_option 7, delete_option 37,
  update_post_meta 85, add_post_meta 2, delete_post_meta 10,
  wp_insert_post 3, wp_update_post 12, wp_delete_post 1,
  set_transient 11, delete_transient 12,
  wp_schedule_event 9, wp_schedule_single_event 36, wp_clear_scheduled_hook 34
- 23/23 PHP-Dateien Lint PASS
- ZIP 66/66 Dateien byteidentisch zum geprüften Arbeitsstand

### Paket
PFERDEATELIER_AFFILIATE_6.72.366_DEFAULT_HOST_FILTER_ROOTFIX_TEST.zip
SHA-256: f6da2e572c558b0126c2fe237d1ef832a8a1ce49e2c62123fb9f82dd4ad02b2f

### Entscheidung
6.72.366 ist installierbar.
Es repariert ausschließlich den bewiesenen, auf jeder WordPress-Anfrage wirksamen Fehlstopper von 6.72.365.
Keine 6.72.363-Rückkopie, kein verworfener 6.72.364-Mikrofix, keine zusätzliche Fachänderung.


## 2026-11-21 – Konsolidierung vor Live-Test 6.72.366

### Verbindliche Freigaberegel
- Keine neue Pluginversion wegen einzelner Vermutungen.
- Änderungen werden soweit sinnvoll gebündelt.
- Jede Performanceänderung braucht einen Kausalitätsbeweis.
- Byte-/Dateivergleiche allein reichen nicht. Zwingend ist zusätzlich ein inhaltlicher Alt/Neu-Funktionsnachweis.
- Kein vorhandener Funktionsweg darf zur Beschleunigung entfernt oder semantisch verändert werden.

### Bestehender Live-Datensatz 6.72.365 weiter ausgewertet
Quelle: pferdeatelier-performance-gesamtanalyse-20261121-082829.json, Performance Diagnose Safe 7.0.0 PASSIV.
- Pferdesättel: 5721,16 ms Wall, 3264,16 ms CPU, 139257 interne Cache-Hits, 320 Queries, 0 externe HTTP-Aufrufe.
- Ausrüstung/Sattel: 3942,33 ms Wall, 2563,55 ms CPU, 82101 Cache-Hits, 298 Queries.
- Schabracken: 3703,25 ms Wall, 2346,28 ms CPU, 87991 Cache-Hits, 320 Queries.
- Über die Frontend-Routen: Korrelation Cache-Hits↔CPU 0,857; Cache-Hits↔Wall 0,904; Queries↔CPU nur 0,442. Das ist ein starker Skalierungsbeleg, aber allein noch kein Kausalitätsbeweis.
- Dominante PASSIV-Phase ist loop_start→wp_footer: Pferdesättel 3977,27 ms; Ausrüstung/Sattel 2316,24 ms; Schabracken 1931,24 ms. Damit liegt die Hauptmehrarbeit im Inhalts-/Produktpfad, nicht in externen HTTP-Aufrufen.

### Kausalitätsbeweis 6.72.366
- 6.72.365 sperrt den bereits vorhandenen category_product-Postprocess-Plan und den Bildprüfungs-Cache, sobald irgendein Callback auf http_request_host_is_external registriert ist.
- WordPress registriert regulär allowed_http_request_hosts auf genau diesem Filter. Dadurch war der 6.72.365-Schnellweg auf normalen WordPress-Seiten faktisch blockiert.
- 6.72.366 ändert ausschließlich diese Freigabeentscheidung: WordPress-Standardcallback erlaubt; zusätzliche/unklare Callbacks behalten den historischen sicheren Pfad.
- Reproduktionsharness PASS: kein Filter, WordPress-Standard allein, Standard+Fremdcallback, Closure, Multisite-Fälle.
- 710-Kandidaten-Harness: Bildprüfungen 2130→710; Lauf 9,380→4,721 ms (-49,67 %), identischer Output.
- Bereits vorhandener 6.72.365-Postprocess-Beweis kann dadurch erstmals unter normalem WordPress aktiv werden: 710 Kandidaten 283,821→94,575 ms (-66,68 %) im isolierten Block.

### Inhaltlicher Funktionsschutz 6.72.365→6.72.366
- Auswahl-/Ranking-/Provider-/GTIN-/Fallback-/Veto-/Health-/Tracking-/Renderingregeln unverändert.
- category_product_shared_rank_base(), select_category_product_campaign_fast_v672171(), der eigentliche Postprocess-Ablauf und die Control-/Health-Regeln sind fachlich unverändert.
- Geändert ist nur, wann der bereits bestehende request-lokale Plan-/Bildcache verwendet werden darf.
- Bei unbekanntem oder zusätzlichem Filtercallback fällt 6.72.366 automatisch auf den historischen vollständigen Pfad zurück.
- 12000 randomisierte Guard-/Plan-Fälle: 0 Outputabweichungen, 0 Guard-Abweichungen außerhalb der gezielt korrigierten WordPress-Standardfilter-Erkennung.
- Hooks/Filter/Shortcodes unverändert 212→212; Produktions-Schreibwege unverändert; 23/23 PHP-Lint PASS. Diese Strukturbelege sind nur Zusatzbelege, nicht der alleinige Funktionsnachweis.

### Entscheidung
Nach Ausschöpfung des vorhandenen Diagnosedatensatzes gibt es derzeit keinen zweiten, gleich stark kausal belegten und funktionssicher belegten Produktionsfix, der seriös mit 6.72.366 gebündelt werden kann. Ein weiterer Codeeingriff wäre aktuell wieder Vermutung und ist deshalb gesperrt.

Nächster Schritt: genau einen Live-Test mit 6.72.366 und danach einen identischen PASSIV-Lauf für Pferdesättel. Erst dieser Live-A/B entscheidet, ob der belegte Schnellweg die reale Zielseite messbar entlastet. Vor diesem Ergebnis keine 6.72.367.


## 2026-11-21 – 6.72.367 konsolidierter semantisch abgesicherter Performance-Rootfix

6.72.366 ist widerrufen / NICHT INSTALLIEREN. Die breitere Inhaltsprüfung zeigte, dass die dort zusätzlich aktivierte request-lokale Bildresultat-Wiederverwendung für den geforderten semantischen Nachweis zu breit war, weil der WordPress-Standardpfad transitiv weitere filterbare URL-/Redirect-/Option-Zustände berührt.

### Finaler Kandidat 6.72.367
- Paket: PFERDEATELIER_AFFILIATE_6.72.367_KONSOLIDIERT_SEMANTIC_SAFE_PERFORMANCE_ROOTFIX.zip
- Library: /pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_AFFILIATE_6.72.367_KONSOLIDIERT_SEMANTIC_SAFE_PERFORMANCE_ROOTFIX.zip
- SHA-256: 88deb31196e7ed3134e5ff11654c4d522c09949cd21189eb44f52c332ee2e14e
- Prüfnachweis: /pferdeatelier/PLUGINS/PERFORMANCE/PFERDEATELIER_6.72.367_PRUEFNACHWEIS.md

### Kausalitätsbeweis
Live 6.72.365: Pferdesättel 5721,16 ms Wall, 3264,16 ms CPU, 139257 interne Cache-Hits; loop_start→wp_footer 3977,27 ms. 6.72.365 blockiert seinen vorhandenen category_product-Postprocess-Plan auf einer normalen WordPress-Single-Site, weil WordPress standardmäßig allowed_http_request_hosts auf http_request_host_is_external registriert.

Gezielter 710-Kandidaten-/3-Slot-Harness mit normalem WordPress-Standardfilter:
- 6.72.365: 3 vollständige Postprocess-Durchläufe.
- 6.72.367: 1 vollständiger Durchlauf + 2 exakt gebundene Plan-Replays.
- Bildprüfungen innerhalb dieses Testpfads: 1332 → 444.
- Alt/Neu-Ausgabehash identisch: b775de9f0e950581b56350ff0e374948b3ce16865351cfea8820c765620630b4.
Damit wird exakt die nachgewiesene wiederholte Arbeit reduziert.

### Inhaltlicher Funktionsbeweis
- 353 vorhandene Methoden in 6.72.365; 0 entfernt.
- 6.72.367 fügt 1 private Sicherheits-Hilfsmethode hinzu.
- Inhaltlich geändert wird ausschließlich die interne Freigabeentscheidung category_product_postprocess_plan_cache_allowed_v672365.
- category_product_public_image_ready ist wieder exakt 6.72.365-Semantik; kein zusätzlicher Bildresultat-Cache im WordPress-Standardfall.
- Auswahl, Control/Veto, Health, Fallback, eigentliche Bildentscheidung, Slot-Auswahl und Kampagnenauswahl sind inhaltlich unverändert.
- 12960 Gate-Kombinationen: 0 unerwartete Abweichungen.
- 60000 Alt/Neu-Ausgaben des betroffenen Postprocess-Pfads: 0 Ausgabeabweichungen.
- 30 dynamische Zustandswechsel-Fälle zwischen category_product_1/2/3 unter abgesicherten Sonderfiltern: 0 Abweichungen.
- Multisite, fremde Host-Callbacks sowie dynamische URL-/Redirect-/Option-/Meta-/Cache-/Sanitizer-/Shortcode-Filter fallen auf den historischen vollständigen Pfad zurück.

### Zusätzlicher Struktur-/Schreibschutz
- Dateien 66→66; entfernt 0; hinzugefügt 0; geändert nur Hauptdatei + readme.
- Actions 176→176, Filter 30→30, Shortcodes 6→6.
- Produktions-Schreibprimitive vollständig identisch.
- 23/23 PHP-Lint PASS.
- Finales ZIP erneut entpackt: 66/66 Dateien identisch zum geprüften Arbeitsstand.

### Nächster Live-Schritt
Nur 6.72.367 installieren. Danach keinen Ein-Seiten-Sondertest, sondern den vorhandenen Performance Diagnose Safe 7.0.0 als vollständigen PASSIV-Gesamtlauf über den bestehenden repräsentativen Seitenmix verwenden. Vor diesem Gesamtlauf keine weitere Affiliate-Version.


## 2026-11-21 – Live 6.72.367 ausgewertet / 6.72.368 gebündelter Kandidat

### Live-Befund 6.72.367
Quelle: pferdeatelier-performance-gesamtanalyse-20261121-101158.json, Performance Diagnose Safe 7.0.0 PASSIV.
- Affiliate 6.72.367 aktiv; Template Kit 1.50.616.
- Pferdesättel: 7307,94 ms Wall, 3567,25 ms CPU, 139257 Cache-Hits, 320 Queries, 0 externe HTTP-Aufrufe.
- 6.72.365 hatte auf derselben Route ebenfalls 139257 Cache-Hits und 320 Queries. Damit hat 6.72.367 den dominanten Wiederholungsblock live nicht reduziert.
- Wall-Time ist in diesem Lauf wegen hoher Serverlast und OPcache-Neustartnähe nicht als reine Pluginwirkung verwertbar. Der unveränderte Cache-Hit-/Query-Fingerabdruck ist dagegen robust.
- Dominante Phase bleibt loop_start→wp_footer; der Affiliate-/Produktpfad bleibt Ziel.

### Bereits gemessener Slot-Ursachenbeleg
Früherer Tiefenlauf:
- category_product_1 bis 1684,421 ms
- category_product_2 bis 622,356 ms
- category_product_3 bis 691,347 ms
- product_after_category_tiles 447,486 ms
Damit ist der wiederholte Produktpfad direkt gemessen.

### 6.72.368 – Ursachenfix
6.72.367 kann den kompletten Postprocess-Plan nur wiederverwenden, wenn die vollständige Kandidatenidentität gleich ist. Unterschiedliche Slot-Kandidatenlisten verhindern den Plan-Hit.
6.72.368 verwendet deshalb zusätzlich ausschließlich das slot-unabhängige Bild-Prüfergebnis je unveränderter Kampagne request-lokal wieder – hinter demselben strengen Dynamik-/Filter-Sicherheitsgate.
Jeder dynamische Meta-/Option-/Cache-/Sanitizer-/Shortcode-/URL-/Redirect-/Hostzustand fällt auf den historischen vollständigen Weg zurück.

### Kausalitätsbeweis
Absichtlich unterschiedliche Slotlisten aus einem 710er-Basispool:
- Größen 710 / 568 / 533
- Bildprüfungen 1811 → 710
- Reduktion 60,8 %
- Alt/Neu-Ergebnis identisch

Breite Zufallsmatrix:
- 60000 stabile Drei-Slot-Fälle: 0 Ausgabeabweichungen
- Bildprüfungen 2308885 → 1166642 (-49,47 %)
- 60000 dynamische Fälle: 0 Ausgabe- oder Aufruffolgeabweichungen; Cache dort aus
- bestehendes Postprocess-Gate: 100000 Alt/Neu-Gate-Fälle, 0 Abweichungen

### Inhaltlicher Funktionsschutz
- Named functions 1556 → 1557; entfernt 0; nur neue private Sicherheitsfunktion.
- Geänderte bestehende Funktionen nur:
  - category_product_postprocess_plan_cache_allowed_v672365
  - category_product_public_image_ready
- Auswahl, Ranking, Provider, Fallback, Veto, Health, Tracking, Rendering und Schreibregeln unverändert.
- Actions 176→176, Filter 30→30, Shortcodes 6→6.
- Alle Produktions-Schreibprimitive identisch.
- 23/23 PHP-Lint PASS.
- finales ZIP 66/66 Dateien identisch zum geprüften Arbeitsstand.

### Paket
- PFERDEATELIER_AFFILIATE_6.72.368_CATEGORY_IMAGE_REUSE_ROOTFIX_TEST.zip
- SHA-256: f81f5c0a2deee1775d6ee70ebea2ae6ca1ebc62e2ee0fc2a4daf621b22c64de8
- Library: /pferdeatelier/PLUGINS/PERFORMANCE/
- Prüfnachweis: PFERDEATELIER_6.72.368_PRUEFNACHWEIS.md

Relevanssi Live Ajax Search 2.6 wurde nach dem 6.72.367-Diagnoselauf separat vom Nutzer deaktiviert. Diese Änderung ist nicht Ursache oder Bestandteil des Affiliate-Fixes und wird erst im nächsten Gesamtlauf mitgemessen.

Nächster Schritt: nur 6.72.368 installieren; anschließend ein vollständiger PASSIV-Gesamtlauf über den bestehenden Seitenmix. Keine weitere Affiliate-Version davor.


## 2026-11-21 – 6.72.369 konsolidierter Performance-Rootfix

6.72.368 ist nur Zwischenstand und NICHT zu installieren. Finaler gebündelter Kandidat ist `PFERDEATELIER_AFFILIATE_6.72.369_KONSOLIDIERT_IMAGE_META_PERFORMANCE_ROOTFIX.zip`, SHA-256 `d1c99b5bc8b0b73b00ddd12bfa6931d1613094068444e5c5f69aa7e74412e98d`.

### Ausgangslage
PASSIV 6.72.367: Pferdesättel 7307,94 ms Wall, 3567,25 ms CPU, 139257 Cache-Hits, 320 Queries, 0 HTTP. Der Cache-/Query-Fingerabdruck ist gegen 6.72.365 unverändert; 6.72.367 hat den dominanten Wiederholungsblock live nicht reduziert. Wall-Time wird wegen hoher Serverlast/OPcache-Nähe nicht allein bewertet.

### Fix A – Produktbildprüfung gebündelt
Die slot-unabhängige strukturelle Bildentscheidung wird auf stabilen normalen Frontend-Requests jetzt über Kategorie-, Hub-, Journal-, feste und Artikel-Produktpfade request-lokal wiederverwendet.
- 100000 stabile Fälle: 0 Ausgabeabweichungen.
- 100000 dynamische Fälle: 0 Ausgabe-/Aufruffolgeabweichungen; Cache dort aus.
- 100000 mutierte Kampagnen: 0 Ausgabeabweichungen.
- 11 Produktplatz-Familien, 710er-Pool: 5395 → 710 Bildprüfungen (-86,84 %), Ausgabe identisch.
- Random: 11681501 → 2856178 Prüfungen (-75,55 %).
- Isolierter provider-/URL-artiger Laufzeittest: Median 3,346 → 1,754 ms (-47,60 %).

### Fix B – Kampagnen-Metadaten schmal lesen
Der alte öffentliche Kampagnen-Snapshot ließ WordPress sämtliche Metafelder der ausgewählten ap_campaign-Posts hydrieren, obwohl der anschließende Rankingpfad zunächst nur `ppar_campaign_data` benötigt. 6.72.369 deaktiviert die Voll-Hydrierung ausschließlich im sicheren Frontend GET/HEAD und liest exakt diesen Schlüssel. Bestehende WordPress-Cachewerte bleiben autoritativ; bei Filter/Object-Cache/Lesefehler gilt der historische Vollpfad.
- 100000 randomisierte Bestände: 0 Wertabweichungen; Testmodell 11821987 → 1542421 geladene Meta-Zeilen (-86,95 %).
- 710er-Modell mit 1 benötigten + 8 fremden Meta-Schlüsseln: 6390 → 710 (-88,89 %), gleiche Kampagnendaten.
- 100000 Fehler-/Fallbackfälle: 0 Abweichungen.
- 100000 serialisierte Meta-Werte: 0 Abweichungen.
- Der Tiefenlauf zeigt passend große Postmeta-Sammelarbeit; eine einzelne 160,82-ms-Sammelquery wird nur als Live-Kontext, nicht als alleiniger Besitzerbeweis verwendet.

### Gesamt-Funktionsschutz
- Named functions 1556 → 1561; entfernt 0; neu nur 5 private Performance-/Sicherheitshelfer.
- Dateien 66 → 66; entfernt 0; hinzugefügt 0; geändert nur Hauptdatei, Article-Plans-Trait und readme.
- Actions 176 → 176; Filter 30 → 30; Shortcodes 6 → 6.
- Sämtliche geprüften Produktions-Schreibwege exakt gleich.
- Auswahl, Ranking, Provider, Placement, Fallback, Veto/Control, Health, Tracking, Produktinhalt und Renderingregeln nicht entfernt.
- Design 1.50.616 und Diagnose 7.0.0 sind nicht Bestandteil des Pakets und unverändert.
- Arbeitsstand 23/23 PHP-Lint PASS; finales ZIP 66/66 identisch zum geprüften Arbeitsstand und erneut 23/23 PHP-Lint PASS.

### Bewusst nicht eingebaut
- wp_options-Wiederholungen: gemessen, aber noch nicht eindeutig einem sicheren Änderungsweg zugeordnet.
- init/Cron-Scheduling: nicht ausreichend pro Callback attribuiert.
- vollständiger Postprocess-Plan-Hash: isoliert nur ca. 1,6 ms für drei Slots.
- persistenter Objektcache: keine Infrastrukturänderung ohne eigenen Beweis.

### Nächster Live-Schritt
Nur 6.72.369 installieren. Danach genau ein vollständiger PASSIV-Gesamtlauf über den bestehenden Seitenmix. Dieser Lauf misst zugleich den bereits separat deaktivierten Relevanssi Live Ajax Search mit. Vor diesem Gesamtlauf keine weitere Affiliate-Version.


## 2026-11-21 – 6.72.369 widerrufen / 6.72.370 Query-Regression korrigiert

### Live-Beweis gegen 6.72.369
PASSIV-Lauf pferdeatelier-performance-gesamtanalyse-20261121-163945.json mit Affiliate-Zentrale 6.72.369:
- Pferdesättel: 1421 Queries statt 320 unter 6.72.367
- Ausrüstung/Sattel: 838 statt 298
- Trensen & Gebisse: 828 statt 296
- Satteldecken: 734 statt 311
Damit ist 6.72.369 als Gesamtfix widerlegt.

Gleichzeitig sinken bei Pferdesättel die internen Cache-Hits 139257 -> 131116. Der Bildcache reduziert also Wiederholungsarbeit, während der in 6.72.369 neu eingeführte schmale Kampagnen-Metadatenweg die Query-Explosion verursacht.

### Bewiesene Ursache
6.72.369 setzte im öffentlichen Kampagnen-Snapshot update_post_meta_cache=false und las anschließend ausschließlich ppar_campaign_data direkt. Diese Teilmenge wurde nicht als partieller WordPress-post_meta-Cache gespeichert. Spätere normale get_post_meta()-Zugriffe mussten deshalb pro Kampagnenpost den vollständigen Meta-Cache einzeln nachladen.

Exakter Methoden-Harness mit 710 Kampagnenposts:
- 25 % Folge-Metazugriffe: 6.72.369 = 187 Queries, 6.72.370 = 2
- 50 %: 362 vs. 2
- 75 %: 537 vs. 2
- 100 %: 712 vs. 2
- Kampagnenrecords in allen Fällen identisch

### 6.72.370
Der komplette Narrow-Meta-Fix aus 6.72.369 ist entfernt. Die drei relevanten Metadatenfunktionen sind wieder byte-identisch zu 6.72.367/6.72.368:
- ranked_campaign_posts_snapshot()
- ranked_campaign_raw_records_snapshot()
- campaign_from_post()

Es existiert in 6.72.370 kein update_post_meta_cache=false und kein Narrow-Meta-Helfer mehr.

Beibehalten wird nur die separat erneut getestete slotübergreifende Bildprüfung:
- exakte Methode aus 6.72.370 im Harness
- 100000 stabile Fälle: 0 Abweichungen
- 600000 historische Aufrufe -> 100000 reale Aufrufe (-83,33 % im Sechsfachmodell)
- 100000 dynamische Fälle: 0 Abweichungen, Cache vollständig aus
- 100000 Signatur-Mutationen: jede Änderung erzwingt Neuprüfung
- Sicherheitsgate 100000 Kombinationen gegen 6.72.367-Semantik: 0 Abweichungen

### Funktionsschutz
- benannte vorhandene PHP-Funktionen entfernt: 0
- neu gegenüber 6.72.367: nur 2 interne Performance-/Sicherheitshelfer
- PHP-Dateien 23 -> 23
- Actions 176 -> 176
- Filter 30 -> 30
- Shortcodes 6 -> 6
- Produktions-Schreibprimitive vollständig identisch
- Auswahl, Ranking, Provider, Placement, Fallback, Veto/Control, Health, Tracking, Produktinhalt und Rendering nicht entfernt
- Design 1.50.616 und Diagnose 7.0.0 unverändert

### Paket
PFERDEATELIER_AFFILIATE_6.72.370_QUERY_REGRESSION_CORRECTION.zip
SHA-256: 5c3f7b68479b2a8f2ab30b800602ac6242210f506437ac5dffc045b2c73eeecc

Finales ZIP:
- 66/66 Dateien identisch zum geprüften Arbeitsstand
- 23/23 PHP-Lint PASS
- Stable Tag 6.72.370

6.72.369 ist widerrufen und darf nicht weiterverwendet werden.
Nächster Schritt: nur 6.72.370 installieren; danach genau ein vollständiger PASSIV-Gesamtlauf. Harter Kontrollwert sind zuerst die Query-Zahlen der vier gleichen Produktseiten, nicht die Wall-Time allein.


## 2026-11-21 – 6.72.371 gebündelte Ursachenoptimierung

### Status
- 6.72.369 bleibt widerrufen.
- 6.72.370 ist der geprüfte Korrektur-/Sicherheitsstand, wurde aber vor dem nächsten Live-Lauf durch 6.72.371 als Installationskandidat supersediert.
- 6.72.371 baut auf 6.72.370 auf. Design 1.50.616 und Performance Diagnose Safe 7.0.0 bleiben unverändert.
- 6.72.371 ist lokal kausal + semantisch geprüft; ein Live-Gesamt-Speedup wird ausdrücklich erst nach PASSIV-Lauf behauptet.

### Root cause 1 – automatische Banner werden zu spät verworfen
Der allgemeine Rankingpfad normalisierte automatische Banner vollständig, bevor technische Ausschlussgründe griffen. 6.72.371 verwendet vor der Vollnormalisierung ausschließlich dieselben bereits existierenden zwingenden Ausschlussregeln:
- automatische, nicht erzwungene Banner: raw source muss output_object_v4 sein;
- exakter bestehender technischer Slotvertrag muss auf den gespeicherten Rohdaten erfüllt sein.
Forced/fixed Banner umgehen den Frühfilter wie historisch.

Beweise:
- 300000 zufällige Einzelfälle: 0 Alt/Neu-Abweichungen.
- 5000 Listen à 213 Kandidaten: 0 Ergebnislisten-Abweichungen.
- 500000 Source+Format-Fälle inkl. forced path: 0 Abweichungen.
- synthetische Vollnormalisierungen 500000 -> 26597 (-94,68 %) im Source+Format-Harness.
Diese Prozentzahl beweist nur die entfernte Arbeit des Blocks, nicht die Live-Seitenzeit.

### Root cause 2 – gleiche Control/Health-Basisprüfung pro Kampagne mehrfach je Slot
Die allgemeine öffentliche Slotverarbeitung prüfte dieselbe Kampagne in Hub/Journal/anderen Slots wiederholt gegen dieselbe Basis-Control- und Health-Entscheidung. Das bestehende sichere Request-Reuse-Prinzip war nur auf Kategorie-Produkte begrenzt.

6.72.371:
- Basis-Control einmal je stabile Kampagne/Request;
- Health einmal je stabile Kampagne/Request;
- Slot-Veto separat je Slot;
- dynamische Filter/Meta/Option/Cache/Sanitizer/Shortcode/URL/Redirect/Host-Zustände => exakter historischer Weg.

Breiter Harness:
- 100000 stabile Fälle: 0 Ausgabeabweichungen.
- Basisprüfungen -77,31 %, Health -76,39 %, Slotprüfungen -95,64 % im synthetischen Mix.
- 50000 dynamische Fälle: 0 Ausgabe- und Aufruffolgeabweichungen.

Realer eingebetteter Pferdeatelier-Historienbestand:
- 2012 Produktkampagnen im Snapshot, 1518 aktiv.
- 1985 Kampagnen liegen gleichzeitig auf hub_product_1/2/3.
- 895 Kampagnen liegen gleichzeitig auf journal_product_1/2/3.
- 5000 reale Zielkontexte / echte Placements:
  - Hub: 0 Ergebnisabweichungen; Basis -66,67 %, Health -65,67 %, Slot-Veto -94,11 %.
  - Journal: 0 Ergebnisabweichungen; Basis -66,67 %, Health -65,76 %, Slot-Veto -80,20 %.
Der historische Snapshot wird nur als Struktur-/Wiederholungsbeleg verwendet, nicht als Behauptung über aktuelle Live-Kampagnenzahlen.

### Beibehaltener 6.72.370-Bildcache
Exakte Methoden 6.72.370 -> 6.72.371 unverändert. Kein neuer Bildcache-Umbau.

### Query-Regression technisch ausgeschlossen
Die drei Metadatenmethoden, deren Änderung in 6.72.369 die Query-Explosion ausgelöst hatte, sind 6.72.370 -> 6.72.371 exakt unverändert:
- ranked_campaign_posts_snapshot()
- ranked_campaign_raw_records_snapshot()
- campaign_from_post()
Kein update_post_meta_cache=false, keine Narrow-Meta-Helfer.

### Gesamt-Funktionsschutz 6.72.370 -> 6.72.371
- PHP-Dateien 23 -> 23
- Dateien entfernt 0 / hinzugefügt 0
- vorhandene benannte Funktionen entfernt 0
- neu nur 2 interne Performance-/Sicherheitshelfer
- bestehende Funktionskörper geändert nur ranked_campaign_candidate_pool und ranked_campaigns_for_slot_uncached
- Actions 176 -> 176
- Filter 30 -> 30
- Shortcodes 6 -> 6
- Produktions-Schreibprimitive vollständig identisch
- 23/23 PHP-Lint PASS
- finales ZIP: 66/66 Dateien, 0 Hash-Abweichungen zum geprüften Arbeitsstand

### Paket
PFERDEATELIER_AFFILIATE_6.72.371_KONSOLIDIERT_ROOTCAUSE_PERFORMANCE.zip
SHA-256: 832b7b82f1b190e06250cab922b4e9ab6ee0abb7661097991ae7eca7ce87a456
Prüfnachweis: PFERDEATELIER_6.72.371_PRUEFNACHWEIS.md

### Bewusst nicht eingebaut
- persistenter Kampagnencache: vorhandene Revision nicht universell genug;
- erneuter schmaler Meta-Leser: wegen 6.72.369-Regression ausgeschlossen;
- gemeinsamer Hub-/Journal-Rankinglauf: fachlich möglich, aber vor Live-Nachweis nicht nötig;
- the_content-Rekursion: nicht bewiesen;
- Menücache-Umbau: nicht bewiesen;
- Options/init/Cron: ohne exakte Attribution nicht geändert;
- Relevanssi Core: nicht Hauptbottleneck.

### Nächster Live-Schritt
Nur 6.72.371 installieren. Danach genau ein vollständiger PASSIV-Gesamtlauf.
Harte Prüfungen zuerst:
1. Produktseiten-Queries dürfen nicht wieder in den 734–1421-Bereich der 6.72.369 zurückspringen.
2. Gleiche Routen: Queries, CPU, interne Cache-Hits und Inhaltsphase vergleichen.
3. Hub/Journal/Banner-Produktpfade müssen weniger feste Affiliate-Arbeit zeigen.
4. Wall-Time wegen schwankender Serverlast nur zusammen mit CPU/Queries/Cache/Phasen bewerten.


## 2026-11-22 – 6.72.371 WIDERRUFEN nach verschärftem Kausalitätstest

6.72.371 ist **NICHT FREIGEGEBEN und NICHT zu installieren**.

### Grund
Nach dem vom Nutzer geforderten verschärften Einzel-Kausalitätstest bestehen die beiden neuen 6.72.371-Änderungen zwar die Inhaltsgleichheit, aber nicht beide den geforderten Nachweis, dass sie die reale Performancebremse ursächlich und sicher beseitigen.

#### Fix A – Banner-Frühfilter
Semantik: bestanden, keine Ergebnisabweichungen.
Isolierter Laufzeittest mit exakter 6.72.370-`campaign_from_post()`-Methode zeigt aber:
- 0 % sicher aussortierte Banner: neuer Weg ca. 52,9 % langsamer
- 25 %: ca. 11,7 % langsamer
- 50 %: ca. 19,1 % schneller
- 75 %: ca. 51,4 % schneller
- 90 %: ca. 69,0 % schneller

Der aktuelle Live-Ausschussanteil ist mit den vorhandenen Diagnosedaten nicht bewiesen. Damit ist Fix A nicht universell performancepositiv und erfüllt den Zielvertrag nicht.

#### Fix B – allgemeine Control/Health-Wiederverwendung
Semantik: bestanden.
Der Tiefenlauf misst die Tabelle `slfo_ppar_control_decisions` jedoch über den gesamten Profil-Lauf nur mit 15 Queries / 15,72 ms. Das kann die mehrsekündige Frontendbremse nicht erklären. Der Fix reduziert Wiederholungsarbeit, ist aber nicht als relevante Hauptursache bewiesen.

### Konsequenz
- 6.72.371 widerrufen.
- 6.72.370 bleibt der query-sichere Korrektur-Ausgangspunkt.
- Kein neuer Installationskandidat, bis jeder enthaltene Fix einzeln die drei Bedingungen erfüllt:
  1. ursächlicher Performanceblock direkt bewiesen,
  2. keine bestehende Funktion zurückgenommen,
  3. Bytegleichheit aller unveränderten Teile + Inhaltsgleichheit der bewusst geänderten Teile.
- Fokus ab jetzt nur auf Sekundenblöcke des aktuellen Frontend-Ranking-/Provider-/Produktausgabepfads.


## 2026-11-22 – Kubio testweise deaktiviert / PASSIV-Auswertung

Quelle: `pferdeatelier-performance-gesamtanalyse-20261122-104555.json`

### Verifizierter Testzustand
- Kubio ist im neuen Lauf deaktiviert.
- Affiliate-Zentrale weiterhin 6.72.369.
- Template Kit 1.50.616 und Performance Diagnose Safe 7.0.0 unverändert.
- Aktive Plugins 35 -> 33.
- Zusätzlich gegenüber dem vorherigen Kubio-aktiv-Lauf nicht mehr aktiv: All-in-One WP Migration.
- Weitere Versionsänderungen: HivePress 1.8.2 -> 1.8.3; Texterstellung 0.4.45 -> 0.4.46.
- Deshalb ist der Lauf kein reiner Kubio-Allein-A/B-Test. Wall-Time-Deltas dürfen Kubio nicht allein zugerechnet werden.

### Bewiesener Kubio-Fußabdruck
Vorher mit Kubio:
- 266 registrierte Kubio-Callbacks.
- ca. 294 Kubio-Dateieinbindungen je typischer Frontendroute; über den ausgewerteten Messlauf 5.921.
- Frontend-Assets: 1 Kubio-Script + 2 Kubio-Styles; zusätzlich Kubio-Google-Fonts.

Nach Deaktivierung:
- Kubio nicht mehr in aktiver Pluginliste.
- Kubio-Datei-/Hook-/Asset-Fußabdruck entfällt.

Browser Startseite:
- Ressourcen 122 -> 109.
- DOM-Scripts 111 -> 99.
- Stylesheets 59 -> 54.
- Long Tasks 4 / 312 ms -> 1 / 87 ms.
- JS Heap ca. 83 MB -> ca. 36 MB.
- LCP 3409,3 ms -> 2931,8 ms.
Diese Browserverbesserung ist real, aber wegen weiterer gleichzeitiger Pluginänderungen nicht vollständig Kubio allein zurechenbar.

### Harte Gegenprobe gegen Kubio als Hauptursache
Pferdesättel:
- mit Kubio: 1421 Queries / 131116 Cache-Hits / 3585,26 ms CPU.
- ohne Kubio: 1422 Queries / 131274 Cache-Hits / 3984,08 ms CPU.

Ausrüstung/Sattel:
- mit Kubio: 838 Queries / 74419 Cache-Hits / 2577,89 ms CPU.
- ohne Kubio: 839 Queries / 74305 Cache-Hits / 2674,10 ms CPU.

Damit ist belegt:
- Kubio verursacht nicht die 6.72.369-Query-Explosion.
- Kubio verursacht nicht den dominanten 74k-131k internen Cachezugriffs-Fingerabdruck der Produktseiten.
- Die Hauptlast bleibt nach Kubio-Deaktivierung bestehen.

### Phasenvergleich
Mit Kubio -> ohne Kubio:
- plugins_loaded Ø 367,69 -> 274,44 ms.
- init Ø 475,42 -> 415,09 ms.
- wp_head Ø 350,91 -> 299,96 ms.
- wp_footer Ø 1823,20 -> 1684,30 ms.
- loop_start Ø 580,52 -> 614,18 ms.

Bewertung:
- Deaktivierung reduziert allgemeinen Grundballast.
- Kein Beweis, dass Kubio die mehrsekündige Hauptbremse verursacht.
- Serverlast war im Kubio-aus-Lauf deutlich höher (ca. 183-203 statt ca. 138-150), daher Wall-Time nicht isoliert bewertbar.

### Funktionsschutz Kubio
- Aus den PASSIV-Daten ist nicht bewiesen, dass keine Seite/Funktion auf Kubio-Inhalte angewiesen ist.
- `queried_object_has_kubio_blocks` und `queried_object_saved_in_kubio` liefern in der Diagnose null.
- Entscheidung: Kubio auf der Testseite vorerst deaktiviert lassen, aber NICHT löschen. Dauerhafte Entfernung erst nach separatem Inhalts-/Funktionsnachweis.

### Nächster kontrollierter Schritt
Keine weitere Plugin-Deaktivierung.

Testzustand einfrieren und nur:
- Affiliate-Zentrale 6.72.369 -> 6.72.370.

Begründung:
- 6.72.369-Query-Regression bereits live bewiesen.
- Ursache exakt bewiesen: abgeschaltete Meta-Cache-Vorladung führt zu hunderten Einzel-Nachladungen.
- 6.72.370 stellt den historischen Sammel-Metacache-Pfad wieder her.
- die drei betroffenen Metadatenfunktionen sind wieder byte-identisch zum sicheren 6.72.367/6.72.368-Stand.
- Funktions-/Hook-/Shortcode-/Schreibschutz für 6.72.370 dokumentiert.

Harte Abnahmekriterien nach Installation 6.72.370:
1. Pferdesättel Queries müssen vom aktuellen Bereich ~1422 deutlich zurück Richtung ~320.
2. Ausrüstung/Sattel vom aktuellen Bereich ~839 zurück Richtung ~298.
3. Cache-Hits, CPU und Inhaltsphase separat vergleichen.
4. Wall-Time nur zusammen mit CPU/Queries/Cache/Phasen bewerten.
5. Keine weitere Änderung gleichzeitig.


## 2026-11-22 – Template Kit 1.50.621: zwei offene Kubio-off-Layoutfehler gezielt korrigiert

Ausgangspunkt:
- letzter lokal geprüfter Kandidat: 1.50.620
- Live-Sichtprüfung: Hover ocker = PASS
- weiterhin offen: linker Inhaltsabstand auf Footer-/Rechtsseiten
- weiterhin offen: Abstand direkt unter „Kurzbedingungen“ auf Preise

### Bewiesene Ursache Preise
Der echte WordPress-Export von Seite 7731 enthält dreimal:
`<strong>Kurzbedingungen</strong><br><br>`

1.50.620 formatierte nur die Überschrift, ließ beide festen BR-Zeilenumbrüche aber bestehen.
Damit war der verbleibende Abstand technisch erklärt.

1.50.621 entfernt ausschließlich dieses direkt auf „Kurzbedingungen“ folgende BR-Doppel.
Prüfung gegen echten Exportinhalt:
- 3/3 Kurzbedingungen erkannt und umgebaut
- 0/3 BR-Doppel danach vorhanden
- sichtbarer Text unverändert
- alle 4 href-Ziele und Reihenfolge unverändert

### Footer-/Rechtsseiten: stabiler Inhaltsrand
1.50.620 legte den Seitenabstand auf `#content>.ast-container`.
Dieser äußere Astra/Kubio-Wrapper ist nicht die stabile sichtbare Textachse über alle Viewport-Zustände.

1.50.621 bindet die Breite stattdessen direkt an:
`article.page>.entry-content`

Für Impressum, AGB, Datenschutz, Disclaimer und Werbebedingungen:
- bestehende zentrale Inhaltsachse `--pftk-content-axis-width` (Fallback 900px)
- Mindest-Seitenrand 20px
- linksbündiger Inhalt
- unabhängig von wechselnder äußerer Astra/Kubio-Wrapperbreite

### Regressionsschutz
- Hauptplugin gegenüber 1.50.620 nur geändert: Versionsnummer + Require auf neue Layoutdatei
- 506 bestehende Dateien byte-identisch
- neue Datei: `includes/class-pftk-portal-content-layout-v150621.php`
- alle 11 PHP-Dateien Syntax PASS
- ZIP-Integrität PASS
- keine Datenbankoperation ergänzt
- Kubio-Batch/Rollback nicht verändert
- Hover-Regeln nicht verändert

Artefakte im Pferdeatelier-Designbüro:
- `PFERDE_ATELIER_DESIGN_1.50.621_FOOTER_RAND_KURZBEDINGUNGEN_NUR_TEST.zip`
- `PFERDE_ATELIER_DESIGN_1.50.621_PRUEFNACHWEIS.json`

Wichtig:
- Noch KEIN Live-PASS für die beiden sichtbaren Layoutpunkte.
- Live-PASS erst nach Sichtprüfung von 1.50.621.


## 2026-11-22 – Template Kit 1.50.622 LIVE

- Grundlage: 1.50.621; keine neue Architektur.
- Preise: unter jeder der drei Überschriften „Kurzbedingungen“ bleibt jetzt exakt ein Zeilenumbruch. Text und Links bleiben unverändert.
- Kubio Gesamtumstellung: Ursache des ausgegrauten Buttons korrigiert. Das HTML-Attribut disabled wird nur noch ausgegeben, wenn die Vorprüfung tatsächlich Fehler meldet.
- Aktueller WordPress-Export gegen die 11 fest definierten Kubio-Zielobjekte geprüft: 11/11 Typ, Status und Ausgangs-Hash passend.
- Read-only Werkzeug „Kubio Abhängigkeiten“ samt Inventory-Datei aus der Live-Fassung entfernt. Die einmalige „Kubio Gesamtumstellung“ bleibt bis zur ausgeführten und geprüften Migration erhalten.
- Anzeigenmarkt: gemeinsamer oberer Marktbereich für Anzeigenmarkt-Startseite und alle hp_listing_category-Unterseiten ergänzt. Enthält Startseitenlink, dynamische Navigation der obersten Anzeigenkategorien und auf Kategoriearchiven die bestehende Anzeigenmarkt-Banner-Schnittstelle. Der vorhandene Root-Banner wird auf der Anzeigenmarkt-Startseite nicht doppelt ausgegeben.
- Vorhandene untere Kategorien, Anzeigen und Suchausgabe bleiben unberührt.
- Paketprüfung: 10/10 PHP-Dateien Syntax PASS, ZIP-Integrität PASS, 503 bestehende Dateien byte-identisch.
- Artefakt: PFERDE_ATELIER_DESIGN_1.50.622_LIVE_KUBIO_MARKT_LAYOUT.zip
- Prüfnachweis: PFERDE_ATELIER_DESIGN_1.50.622_PRUEFNACHWEIS.json
- Status: technischer Kandidat PASS. Live-Sichtprüfung von Button und Anzeigenmarkt-Kopf steht noch aus; erst danach Live-PASS.


## 2026-11-22 – Template Kit 1.50.623 LIVE – Anzeigenmarkt-Korrektur vor Kubio-Gesamtumstellung

- Live-Sichtprüfung 1.50.622: Kubio-Gesamtumstellungsbutton = PASS/aktiv; Anzeigenmarkt weiterhin fehlerhaft.
- Ursache fehlender Anzeigenmarkt-Kopf: HivePress-Template 7784 "Listings" enthält noch Kubio-Image + Kubio-Shortcode. Bei deaktiviertem Kubio werden diese beiden Blöcke nicht ausgegeben. Dies ist exakt eines der 11 bereits bewachten Migrationsobjekte.
- Echte Transformation von Objekt 7784 erneut ausgeführt: Ergebnis-Hash ca664aa01f73e8f2023868b5cb55c61ad6463aba9b2a4b38ad82d090bb1698cd = erwarteter geprüfter Zielhash.
- Transformiertes Template enthält: Anzeigenmarkt-Bild, [pferde_atelier_anzeigenmarkt_intro], HivePress-Suche, Listings, Listing-Kategorien und [pferde_atelier_anzeigenmarkt_werbeplatz]; keine wp:kubio-Blöcke mehr.
- 1.50.622-Markt-Top-Hilfsklasse entfernt; sie war kein Ersatz für den echten, im Listings-Template liegenden Anzeigenmarkt-Kopf.
- Ursache zerschossener Direktwerbeplatz: anzeigenmarkt_werbeplatz_shortcode verschachtelte einen äußeren Link um start_ad_slot(), obwohl start_ad_slot() selbst bereits einen Link ausgibt. Zusätzlich stammte die Overlay-Gestaltung aus Startseiten-CSS, das auf /anzeigenmarkt/ nicht geladen wird. Dadurch wurde das Hintergrundbild korrekt gezeigt, Overlay-Text/Logo aber unformatiert darunter ausgegeben.
- 1.50.623 rendert den Anzeigenmarkt-Direktwerbeplatz deshalb als genau EIN fertiges Wide-Bannerbild in genau EINEM Link. Keine Overlay-CSS-/JS-Abhängigkeit und keine verschachtelten Links.
- 1.50.622-Korrekturen bleiben erhalten: genau eine Zeile nach Kurzbedingungen; Kubio-Button disabled nur bei echten Vorprüfungsfehlern.
- Paketdifferenz 1.50.622 -> 1.50.623: 505 gemeinsame Dateien byte-identisch; nur pferde-template-kit.php geändert; obsolete class-pftk-market-top-v150622.php entfernt.
- PHP-Syntax 9/9 PASS; ZIP-Integrität PASS.
- Verbindliche Reihenfolge: 1.50.623 installieren -> Werkzeuge/Kubio Gesamtumstellung Vorprüfung BESTANDEN kontrollieren -> Umstellung SOFORT ausführen, bevor weitere Änderungen an den 11 bewachten Objekten erfolgen -> Frontend prüfen -> erst danach weitere Designänderungen.
- Artefakt: PFERDE_ATELIER_DESIGN_1.50.623_LIVE_KUBIO_MARKT_KORREKTUR.zip
- Prüfnachweis: PFERDE_ATELIER_DESIGN_1.50.623_PRUEFNACHWEIS.json


## 2026-11-22 – Template Kit 1.50.624 Anzeigenmarkt-Ursachenfix

- Live-Screenshots 1.50.623 ausgewertet: oberer Anzeigenmarkt-Bereich war fachlich falsch rekonstruiert (neue Buttonleiste statt vorhandenem Original-Intro); Direktwerbeplatz zeigte korrektes Bild plus Rohtext darunter.
- Ursache Direktwerbeplatz exakt: `anzeigenmarkt-direkt-01` nutzte zwar den responsiven Renderer, der umgebende Anzeigenmarkt-Block trug aber nicht die vorhandene CSS-Scope-Klasse `pftk-direct-responsive-v150360`. Dadurch blieb der Overlay-Text im normalen Dokumentfluss unter dem Bild.
- 1.50.624 ergänzt genau diese bestehende Scope-Klasse. Lokaler Browser-Render: Overlay-Bounding-Box liegt vollständig innerhalb des Banner-Canvas; kein Rohtext mehr darunter.
- Die in 1.50.623 neu erfundene Anzeigenmarkt-Navigation wird vollständig entfernt.
- Root und alle `hp_listing_category`-Seiten erhalten wieder das bereits vorhandene Original-Intro `pftk-market-intro-v150279`: Seitenbild, Kicker „Finden, anbieten, verbinden“, Titel „Anzeigenmarkt“, Beschreibung, CTA-Bereich und bestehende Partnerbanner-Schnittstelle. Sichtbares Intro-Markup/CSS gegen 1.50.614 geprüft: identisch.
- Für Unterkategorien werden Seitenbild und Banner jetzt explizit an die echte Anzeigenmarkt-Rootseite gebunden, statt an die Term-ID.
- Anzeigenmarkt-Breadcrumb wird serverseitig zentral gerendert; der alte spätere JS-Payload des Zusatzplugins wird im Markt-Kontext entfernt. Reihenfolge: Breadcrumb (Priorität 1) -> Original-Intro (Priorität 2) -> bestehender HivePress-Inhalt.
- Preise/Kurzbedingungen unverändert aus 1.50.622/623: exakt eine Zeile Abstand.
- Kubio-Gesamtumstellungsbutton unverändert aktiv, wenn die bestehende 11/11-Vorprüfung besteht. Noch NICHT klicken, bis 1.50.624 live optisch geprüft ist.
- Kubio-Abhängigkeiten-Diagnose bleibt aus der Live-Fassung entfernt.
- Prüfungen: PHP 10/10 PASS, ZIP PASS, Root-Render PASS, Taxonomie-Render PASS, Direktbanner Browser-Render PASS, 505 gemeinsame Dateien byte-identisch; nur `pferde-template-kit.php` geändert, alte 1.50.623-Marktklasse durch 1.50.624-Dispatcher ersetzt.
- Artefakt: `PFERDE_ATELIER_DESIGN_1.50.624_LIVE_ANZEIGENMARKT_URSACHENFIX.zip`
- Prüfnachweis: `PFERDE_ATELIER_DESIGN_1.50.624_PRUEFNACHWEIS.json`


## 2026-11-22 – Template Kit 1.50.625 bereinigter Design-Ausgangspunkt

- Nutzer hat die Kubio-Gesamtumstellung auf der Testseite wieder vollständig rückgängig gemacht.
- 1.50.624 bleibt damit inhaltlicher/visueller Ausgangsstand.
- 1.50.625 entfernt die beiden Kubio-Werkzeuge aus dem Template-Kit: „Kubio Abhängigkeiten“ war in 1.50.624 bereits nicht mehr enthalten; „Kubio Gesamtumstellung“ wurde jetzt vollständig entfernt.
- Entfernt: `includes/class-pftk-kubio-batch-v150619.php` und dessen einzige Require-Zeile.
- Keine Migration, keine Datenbankänderung, keine Inhaltsänderung.
- Gegen 1.50.624: 506 gemeinsame Dateien, davon 505 byte-identisch; einzige gemeinsame geänderte Datei `pferde-template-kit.php` (Version + entfernte Require-Zeile/Altkommentar). Keine neue Datei hinzugefügt.
- PHP 9/9 PASS, ZIP PASS, keine Management-Page für die beiden Kubio-Werkzeuge mehr vorhanden.
- Anzeigenmarkt-, Preise-, Footer- und übriger Designcode aus 1.50.624 bleibt unverändert.
- Artefakt: `PFERDE_ATELIER_DESIGN_1.50.625_BEREINIGT_OHNE_KUBIO_WERKZEUGE.zip`
- Prüfnachweis: `PFERDE_ATELIER_DESIGN_1.50.625_BEREINIGT_PRUEFNACHWEIS.json`
- 1.50.625 ist ab jetzt der feste Ausgangspunkt für die nächste gebündelte Designrunde.


## 2026-11-22 – Template Kit 1.50.626 Preise-Hover-Regressionsfix

- Nutzer-Liveprüfung von 1.50.625: Preise-Hover wieder grün statt bestätigtem Ocker.
- Ursache im bereinigten Paket: Für Seite 7731 fehlte eine explizite seitenbezogene Hover/Fokus-Regel; dadurch konnte die grüne Theme/Kubio-Regel wieder gewinnen.
- 1.50.626 ergänzt ausschließlich für `body.page-id-7731` eine harte Button-Hover/Fokus-Regel: Hintergrund und Rand `#C89214`, Schrift weiß. Grundzustand bleibt unverändert dunkeloliv.
- Beide Kubio-Werkzeuge bleiben entfernt.
- Gegen 1.50.625: 506 gemeinsame Dateien; nur `pferde-template-kit.php` (Version) und `includes/class-pftk-portal-content-layout-v150622.php` (Preise-Hover-Regel) geändert; keine Dateien hinzugefügt oder entfernt.
- PHP 9/9 PASS, ZIP PASS.
- Artefakt: `PFERDE_ATELIER_DESIGN_1.50.626_PREISE_HOVER_OCKER_BEREINIGT.zip`
- Prüfnachweis: `PFERDE_ATELIER_DESIGN_1.50.626_PRUEFNACHWEIS.json`
- Dieser Ocker-Hover auf Preise ist ab jetzt als Regressionstest zu behandeln und darf bei weiteren Designänderungen nicht zurückfallen.


## 2026-11-22 – Template Kit 1.50.627 Kubio vollständig bereinigt + Preise-Hover

- Korrektur der falschen Aussage aus 1.50.625/626: Entfernt waren nur die eigenen Kubio-Werkzeuge; ein verbleibender Kubio-Menü-/Toolbar-Eintrag konnte weiterhin von anderer Quelle registriert werden.
- 1.50.627 bereinigt deshalb robust statt nur dateibasiert:
  - die alten eigenen Kubio-Werkzeuge bleiben entfernt;
  - falls `kubio/plugin.php` noch aktiv ist, wird es im Admin einmalig deaktiviert;
  - alle Admin-Menü-/Untermenüeinträge, deren Titel oder Slug „kubio“ enthält, werden mit maximal später Priorität entfernt;
  - alle Adminbar-Knoten, deren ID/Titel/Href „kubio“ enthält, werden ebenfalls entfernt;
  - der alte Template-Kit-spezifische Kubio-Frontend-Asset-Prune-Pfad wurde als nun überflüssiger Kubio-Sondercode entfernt.
- Preise-Hover wurde nicht mehr nur auf Buttons beschränkt:
  - normale Textlinks: Hover/Fokus `#C89214`;
  - Button-Controls: Hover/Fokus Hintergrund + Rahmen `#C89214`, Text weiß.
- Browser-Computed-Style-Test PASS: Textlink rgb(200,146,20); Button-Hintergrund rgb(200,146,20); Button-Text rgb(255,255,255).
- Admin-Kubio-Cleanup-Simulation PASS: Kubio-Menü/Untermenü entfernt, Nicht-Kubio-Werkzeuge bleiben erhalten, Kubio-Deaktivierung wird ausgelöst.
- Gegen 1.50.626 sind nur zwei Dateien verändert: `pferde-template-kit.php` und `includes/class-pftk-portal-content-layout-v150622.php`. Keine Datei hinzugefügt/gelöscht.
- PHP 9/9 PASS, ZIP PASS.
- Anzeigenmarkt-, Footer-/Rechtsseiten-, Preise-Inhalt, Affiliate-Logik und Datenstruktur bleiben unverändert.
- Artefakt: `PFERDE_ATELIER_DESIGN_1.50.627_BEREINIGT_KUBIO_PREISE_HOVER.zip`
- Prüfnachweis: `PFERDE_ATELIER_DESIGN_1.50.627_PRUEFNACHWEIS.json`
- Dieser Stand ersetzt 1.50.625/626 als bereinigte Designbasis.


## 2026-11-22 – Template Kit 1.50.628 Design-Helfer konsolidiert

- Ausgangspunkt: 1.50.627 = vom Nutzer sichtgeprüfter PASS-Stand.
- Vollständige aktive Pluginliste gegen reine Design-/Frontend-Helfer geprüft.
- Konsolidiert werden genau zwei separate Design-Helfer:
  1. `Pferde Atelier – Anzeigenmarkt & Journal Breadcrumbs` 1.1.1
  2. `Canonical Table Contract V1` 1.1.0
- Breadcrumbs: Journal war bereits zentral im Template-Kit. Für `hp_listing_category` ist jetzt die fehlende Anzeigenmarkt-Kette zentral ergänzt: Startseite -> Anzeigenmarkt -> vorhandene Taxonomie-Eltern -> aktueller Term. Keine neue, unbelegte Breadcrumb-Logik für einzelne Listings erfunden.
- Tabellen: der bereits bindende Template-Kit-Vertrag (dunkeloliv #35422A, 1px Zelltrenner, 2px Headertrenner) wird als zentraler Tabellenvertrag auch im Gutenberg-Editor geladen. Bestehende spezifischere Artikel-/Preise-Regeln behalten Vorrang.
- Nach Installation deaktiviert das Template-Kit die beiden alten Helfer nur, löscht sie aber nicht.
- Explizit NICHT zusammengeführt: `Pferde Atelier HivePress Anzeigensuche` 2.1.5-ajax-category-label und `Pferde Atelier – HivePress Anzeigensuche` 1.0.1. Beide enthalten Suchfunktion und sind kein reines Design; ihre mögliche Zusammenlegung gehört in einen separaten Funktions-/Plugin-Aufräumschritt.
- Weitere reine Design-Helfer wurden in der vollständigen Pluginliste nicht gefunden. Bildzentrale, Glossar, Pferderassen, Affiliate-Zentrale, HivePress, Relevanssi, Shortcodes usw. bleiben getrennte Funktionssysteme.
- Diff gegen 1.50.627: 506 gemeinsame Dateien, davon 505 byte-identisch. Geändert: nur `pferde-template-kit.php`. Neu: `assets/canonical-table-contract-v150628.css`. Keine bestehende Datei gelöscht.
- PHP 9/9 PASS, ZIP PASS.
- Artefakt: `PFERDE_ATELIER_DESIGN_1.50.628_KONSOLIDIERT_BREADCRUMB_TABELLEN.zip`
- Prüfnachweis: `PFERDE_ATELIER_DESIGN_1.50.628_PRUEFNACHWEIS.json`
- Wichtig: Die Original-CSS-Datei des alten Canonical-Table-Plugins war nicht als exportierbare Quelle verfügbar. Deshalb wurde keine Bytegleichheit dieser Alt-CSS behauptet; übernommen ist der bereits bindende Tabellenvertrag des aktuellen Template-Kits plus dessen Gutenberg-Ladeweg. Frontend-spezifische Template-Kit-Regeln bleiben unverändert.


## 2026-11-22 – Template Kit 1.50.629 Journal-Unterseiten Layout – NUR TEST

- Basis: 1.50.628 (optisch PASS auf Live/Test).
- Ausschließlich die acht redaktionellen Journal-Kategoriearchive werden geändert: pferde-verstehen, recht-finanzen-und-organisation, reiterleben-und-community, ausbildung-und-reitweisen, pferdeernaehrung-verstehen, pferdegesundheit-verstehen, alltags-pferde-haltungsformen, pferdewissen-grundlagen.
- Ausdrücklich ausgeschlossen: Pferderassen und Glossar (journal_role=reference).
- Änderung 1: vorhandener Kategoriename wird als H1 direkt in das vorhandene Hero-/Termbild gelegt; Astras separate Archivüberschrift wird in diesem Scope ausgeblendet.
- Änderung 2: der bereits vorhandene Affiliate-Banner mit Slot product_after_category_tiles wird nur verschoben: direkt unter das Hero. Es wird kein zweiter Banner erzeugt.
- Änderung 3: die bestehende untere Archiv-Paginierung bleibt bestehen; eine DOM-Kopie mit identischen Links wird zusätzlich oberhalb der Beiträge eingefügt.
- Zielreihenfolge geprüft: Hero -> Banner -> Paginierung oben -> Beiträge -> Paginierung unten.
- DOM-Vertragstest: Banneranzahl 1; Paginierungen 2; Linkziele oben/unten identisch.
- Diff gegen 1.50.628: 507 gemeinsame Dateien, 506 byte-identisch; ausschließlich pferde-template-kit.php geändert; keine Datei hinzugefügt/gelöscht.
- PHP 9/9 PASS; ZIP PASS.
- Artefakt: PFERDE_ATELIER_DESIGN_1.50.629_JOURNAL_UNTERSEITEN_LAYOUT_NUR_TEST.zip
- Prüfnachweis: PFERDE_ATELIER_DESIGN_1.50.629_PRUEFNACHWEIS.json
- Status: NUR TEST; visuelle Nutzerabnahme steht aus.


## 2026-11-22 – Template Kit 1.50.630 Journal Raster/Paginierung – NUR TEST

- Basis: 1.50.629 (Hero + integrierte Überschrift vom Nutzer PASS bestätigt).
- Scope unverändert: ausschließlich acht redaktionelle Journal-Kategoriearchive; Glossar und Pferderassen bleiben ausgeschlossen.
- Neu: exakt 8 echte Beiträge pro Archivseite über pre_get_posts. Paginierung erscheint damit nur, wenn tatsächlich mehr als 8 Beiträge vorhanden sind.
- Zielraster Desktop: 8 Beiträge + bereits vorhandene Amazon-Suchanzeige = 9 Rasterplätze = 3x3. Tablet bleibt 2-spaltig, Mobil 1-spaltig.
- Amazon: kein neuer Affiliate-Link und keine neue Affiliate-Entscheidung. Es wird ausschließlich der bereits vorhandene Amazon-Link übernommen; die bestehende Suchanzeige wird nur als formatgleiche Journal-Karte dargestellt und ans Rasterende gesetzt.
- Amazon-Karte: gleiche Bildhöhe 205px, gleiche Kartenbreite/Innenabstände, Kategorie-spezifischer Text, CTA 'Bei Amazon ansehen', vorhandene Disclosure bleibt erhalten.
- Banner: bestehender Slot product_after_category_tiles wird weiter nur verschoben, jetzt auf max. 1180px/Inhaltsbreite begrenzt; Bild darf nicht über die Body-Achse hinauswachsen.
- Paginierung: vorhandene untere Navigation wird direkt hinter das Beitragsraster verschoben; daraus wird eine identische obere Navigation direkt vor dem Raster geklont. Mittig, Sand-Hintergrund #F2E8D6, aktive/hover Seite Ocker #C89214.
- Hero + Überschrift aus 1.50.629 bleiben unverändert.
- Diff gegen 1.50.629: 507 gemeinsame Dateien, 506 byteidentisch; nur pferde-template-kit.php geändert; keine Datei hinzugefügt/entfernt.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS.
- Artefakt: PFERDE_ATELIER_DESIGN_1.50.630_JOURNAL_RASTER_PAGINATION_NUR_TEST.zip
- Prüfnachweis: PFERDE_ATELIER_DESIGN_1.50.630_PRUEFNACHWEIS.json
- Status: NUR TEST; visuelle Abnahme auf Testseite steht aus.


## 2026-11-22 – Template Kit 1.50.631 Journal 8 Beiträge + reduzierte Paginierung – NUR TEST

- Basis: 1.50.630.
- Nutzerprüfung 1.50.630: Hero/Banner/Amazon nahezu PASS; Paginierung zu aufwendig; 8-Beitragsgrenze sichtbar nicht wirksam.
- Ursache Beitragsgrenze: nur `posts_per_page=8` war gesetzt. Auf Archivseiten kann `posts_per_archive_page` anschließend einen anderen Wert wieder darüberlegen.
- Korrektur: für die acht redaktionellen Journal-Kategoriearchive jetzt `posts_per_page=8`, `posts_per_archive_page=8`, `nopaging=false`; Hook-Priorität auf 9999, damit spätere Standardwerte die Grenze nicht wieder überschreiben.
- Paginierung reduziert: keine äußere Box, keine Rahmen um Seitenzahlen, normale Links transparent; ausschließlich die aktive Seite erhält Ocker #C89214 mit weißer Schrift. Hover/Fokus nur ockerfarbene Schrift ohne Hintergrundfläche.
- Hero, Banner und Amazon-Kachel bleiben gegenüber 1.50.630 unverändert.
- Diff gegen 1.50.630: 507 gemeinsame Dateien, 506 byteidentisch; nur `pferde-template-kit.php` geändert; keine Dateien hinzugefügt/entfernt.
- PHP 9/9 PASS, JavaScript-Syntax PASS, ZIP-CRC PASS, statischer Vertragstest PASS.
- Artefakt: `PFERDE_ATELIER_DESIGN_1.50.631_JOURNAL_8_BEITRAEGE_PAGINATION_NUR_TEST.zip`
- Prüfnachweis: `PFERDE_ATELIER_DESIGN_1.50.631_PRUEFNACHWEIS.json`
- Status: NUR TEST; visuelle Nutzerabnahme steht aus.


## 2026-11-22 – Template Kit 1.50.632 Journal 8-Beiträge SQL-Endschutz – NUR TEST

- Basis: 1.50.631; Nutzer bestätigt Design der Journal-Unterseiten als PASS, einzig Beitragsanzahl weiterhin falsch.
- Ursache der bisherigen Fehlversuche: Begrenzung hing an indirekter Journal-Kategorieauflösung im frühen pre_get_posts-Pfad; sichtbarer Realtest zeigte, dass dieser Scope im echten Archiv nicht wirksam begrenzte.
- 1.50.632 verwendet deshalb direkte feste Journal-ID/Slug-Erkennung für exakt acht redaktionelle Archive und zusätzlich einen finalen post_limits-Endschutz auf PHP_INT_MAX.
- SQL-Seitenlänge wird direkt vor der Hauptabfrage auf exakt 8 gesetzt; Offset = (Seite-1)*8. Gleichzeitig bleiben posts_per_page/posts_per_archive_page auf 8 synchron, damit WordPress-Paginierung dieselbe Seitenlänge verwendet.
- Glossar und Pferderassen sind nicht im erlaubten Scope.
- Design-Schutz: kompletter Journal-CSS-Block und kompletter Journal-Layout-JavaScript-Block sind byteidentisch zu 1.50.631.
- Zusätzlich korrigiert: Pluginheader 1.50.631 hatte intern noch const VERSION=1.50.630; 1.50.632 trägt Header und interne Konstante konsistent 1.50.632.
- Diff gegen 1.50.631: 507 gemeinsame Dateien, 506 byteidentisch; nur pferde-template-kit.php geändert; keine Dateien hinzugefügt/gelöscht.
- PHP 9/9 PASS, ZIP-CRC PASS, statischer Scope/Offset-Vertrag PASS.
- Artefakt: PFERDE_ATELIER_DESIGN_1.50.632_JOURNAL_8_SQL_LIMIT_NUR_TEST.zip
- Prüfnachweis: PFERDE_ATELIER_DESIGN_1.50.632_PRUEFNACHWEIS.json
- Status: NUR TEST; sichtbare Nutzerabnahme der 8er-Grenze steht aus.


## 2026-11-22 – 1.50.632 Nutzerabnahme PASS / Live-Freigabe

- Nutzer hat 1.50.632 auf der Testseite sichtbar geprüft und als PASS bestätigt.
- Journal-Design PASS: Hero/Überschrift, Bannerbreite, Amazon-Kachel, Paginierung.
- Beitragsgrenze PASS: maximal 8 echte Beiträge pro Seite.
- 1.50.632 ist damit Live-freigegeben und ab jetzt verbindliche Designbasis.
- Archiviert als `PFERDE_ATELIER_DESIGN_1.50.632_LIVE_PASS.zip` plus Prüfnachweis im Design-Büro.
- Weitere Designänderungen bauen ausschließlich auf 1.50.632 auf.


## 2026-11-22 – Design 1.50.633 Einzelbeitrag Sidebar – NUR TEST

- Verbindliche Live-Basis bleibt 1.50.632 PASS.
- Neue Testversion 1.50.633 baut exakt darauf auf und betrifft nur klassische Einzelbeiträge.
- Desktop/Tablet ab 768 px: rechte Begleitspalte aus bereits vorhandener Anzeige, vorhandenem Produktblock (max. drei bereits geprüfte Produkte) und genau einem vorhandenen gleichkategorischen Astra-Weiterführungslink.
- Mobil unter 768 px bleibt unverändert; beim Wechsel auf Mobil werden die Originalelemente an ihre Ausgangspositionen zurückgesetzt.
- Keine neue Affiliate-Auswahl, keine neue URL, keine neue Query, kein neuer Helper, keine Änderung am Affiliate-Router; kein Sticky.
- 506/507 Dateien byteidentisch zu 1.50.632; PHP 9/9 PASS; JS PASS; ZIP PASS.
- Im Design-Büro gespeichert als PFERDE_ATELIER_DESIGN_1.50.633_EINZELBEITRAG_SIDEBAR_NUR_TEST.zip plus Prüfnachweis.
- Visuelle Abnahme steht aus.


## 2026-11-22 – Design 1.50.633 FAIL / 1.50.634 Reparatur

- 1.50.633 Einzelbeitrags-Sidebar vom Nutzer sichtbar als FAIL bewertet: Inhaltsspalte/Seitenachse gebrochen.
- Ursache im Designplugin: Header + Entry-Content wurden aus Astras Originalstruktur in einen neuen Layoutcontainer verschoben.
- 1.50.633 verworfen, nicht Live.
- 1.50.634 direkt aus 1.50.632 LIVE PASS neu gebaut: Original-Artikel-DOM bleibt vollständig bestehen; Sidebar nur als Geschwister von #primary; vorhandene Anzeige/Produkte nur geklont; bestehender Astra-Weiterlesen-Link wiederverwendet; Mobil <768px unverändert.
- Keine Änderung am Affiliate-Router, keine neue Query, keine neue Affiliate-URL, kein Sticky.
- 506/507 Dateien byteidentisch zu 1.50.632; PHP 9/9 PASS; JS PASS; ZIP PASS.
- 1.50.632 bleibt bis Nutzerabnahme von 1.50.634 der letzte LIVE-PASS-Fallback.


## 2026-11-22 – Design 1.50.635 Einzelbeitrag Sidebar Korrektur

- 1.50.634 war visuell noch nicht PASS: Resize-Grenze zu niedrig, Amazon-Doppelbeschriftung/Innenrahmen, CTA/Text unruhig, Produkte/Weiterlesen fehlten im Test.
- 1.50.635 korrigiert ausschließlich die Einzelbeitrags-Sidebar. Letzter Live-PASS bleibt 1.50.632.
- Sidebar nur ab 1000px und realer Containerbreite >=940px; darunter Original-Layout.
- Werbekachel: nur ein Ocker-WERBUNG, keine zweite Anzeige-/Disclosure-Zeile im Klon, keine Innenrahmen, CTA nowrap.
- Bis zu 3 Produktkarten werden ausschließlich aus dem vorhandenen Artikelplan bzw. dort bereits PASS-geprüften Kandidaten dargestellt; keine neue Produktsuche, keine Änderung am Affiliate-Router.
- Weiterführender Beitrag folgt expliziten semantic_related/further_information-K0-Verknüpfungen; genau ein Zielbeitrag.
- 506/507 Dateien byteidentisch zu 1.50.634; PHP 9/9 PASS; JS PASS; ZIP PASS.
- Im Design-Büro gespeichert als PFERDE_ATELIER_DESIGN_1.50.635_EINZELBEITRAG_SIDEBAR_KORREKTUR_NUR_TEST.zip plus Prüfnachweis.


## 2026-11-22 – Design 1.50.636 Sidebar-Sichtbarkeitsfix

- 1.50.635 Einzelbeitrags-Sidebar FAIL: komplett unsichtbar.
- Nachgewiesene Ursache: falsche Aktivierungsbedingung prüfte den noch auf Lesebreite begrenzten Astra-Container auf >=940px, bevor das Sidebar-Grid diesen Container überhaupt verbreitern konnte.
- 1.50.636 entfernt nur diese falsche Sperre. Sidebar aktiv ab Browserbreite 1000px; 1024px aktiv, 999px aus.
- Müsli-Testartikel belegt: vorhandener ready-Artikelplan mit ausgewähltem Produkt 16615 und weiteren PASS-Produkten; vorhandene semantic_related/further_information-Verknüpfungen.
- 506/507 Dateien byteidentisch zu 1.50.635; PHP 9/9 PASS; JS PASS; ZIP PASS.
- Im Design-Büro als 1.50.636 NUR TEST gespeichert; letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – Design 1.50.637 Sidebar-Hartfix

- 1.50.636 Einzelbeitrags-Sidebar sichtbar FAIL: doppelte Werbung, abgeschnittener Text, CTA-Umbruch, keine Produkte, kein Weiterführungsblock.
- Ursachen: kompletter Werbe-DOM geklont; Produkte im Design aus Rohmeta nachgebaut; Weiterführungsresolver nur fuer /category/-Links.
- 1.50.637: saubere Amazon-Karte nur mit vorhandenem Amazon-Link; genau ein WERBUNG-Kicker; CTA nowrap; keine Innenrahmen. Drei Produkte werden direkt ueber zentrale Router-Slots category_product_1/2/3 gerendert und nur visuell kompakt dargestellt. Weiterführungsresolver versteht nun auch normale Portalpfade und leitet daraus bestehende redaktionelle Kategorien ab.
- Originale Artikel-/Affiliate-Elemente bleiben unangetastet und werden nur bei aktiver Sidebar verborgen; unter 1000px Originalzustand.
- 506/507 Dateien byteidentisch zu 1.50.636; PHP 9/9 PASS; JS PASS; ZIP PASS. Kein visueller Chromium-PASS behauptet, da Browser im Container wegen DBus nicht zuverlässig startet.
- Design-Büro enthält 1.50.637 ZIP + Prüfnachweis. Letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – Design 1.50.638 Einzelbeitrag responsive Sidebar

- 1.50.637 noch nicht PASS: Amazon-Bild fehlte, Anbieter wurden falsch auf Amazon reduziert, mobile/Weiterführungs-Ausgabe unvollständig.
- 1.50.638: Amazon übernimmt vorhandenes Bild; Produkte zeigen vorhandene eBay/idealo/Amazon-Angebotslinks aus zentralem Artikelplan/Router-Slots; Weiterführung fällt bei fehlendem zweitem Post auf den redaktionell gesetzten Portalpfad zurück; unter 1000px Originalquellen sichtbar, fehlende Empfehlungen optional unter dem Artikel.
- 506/507 Dateien byteidentisch zu 1.50.637; PHP 9/9 PASS; JS PASS; ZIP PASS.
- Design-Büro enthält ZIP + Prüfnachweis. Letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – Design 1.50.639: reine Darstellung, keine Affiliate-Logik

- 1.50.639 trennt Design und Affiliate-Logik hart: keine category_product-Zusatzslots, keine Shortcode-Nachauswahl, keine Provider-Mischung, keine Rohmeta-Auswertung, keine neue Related-Query.
- Desktop/grosse Tablets klonen nur bereits ausgegebenen Artikel-Produktblock und Astras bereits ausgewählten echten Related-Post; Mobil zeigt die Originalausgaben.
- Amazon: vorhandener Link/Bild, kurze Copy `Passende Angebote entdecken`, sichtbare Amazon-Wortmarke, einzeilige CTA.
- Responsive nutzt zusaetzlich outerWidth, damit schmal gezogene Browserfenster trotz Zoom die Sidebar sicher abschalten.
- 506/507 Dateien byteidentisch zu 1.50.638; PHP 9/9 PASS; JS PASS; ZIP PASS. Letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – Design 1.50.640 sauberer Einzelbeitrags-Neuansatz

- 1.50.640 direkt aus 1.50.632 LIVE PASS gebaut; verworfene Sidebar-Testreihe 1.50.633–1.50.639 nicht fortgeführt.
- Nur Darstellung: Sidebar ab 1180px; Artikel bleibt 760px breit, Sidebar 280px, Gap 32px.
- Keine neue Affiliate-/Kategorie-/Related-Logik: 0 category_product Zusatzslots, 0 do_shortcode, 0 WP_Query/get_posts/url_to_postid/get_term_by im Sidebar-Code.
- Produkte: ausschließlich Klon des bereits gerenderten Artikel-Produktblocks; Mobil zeigt das Original. Originale werden nur nach erfolgreichem Klon auf breiter Ansicht verborgen.
- Related: ausschließlich vorhandene Astra-Related-Ausgabe; Featured-Images werden wieder sichtbar, Mobil zeigt Originalkarten.
- Amazon: vorhandener Link/Bild, kurze Copy `Passende Angebote entdecken`, sichtbare Wortmarke/Smile, einzeilige CTA.
- 506/507 Dateien byteidentisch zu 1.50.632; PHP 9/9 PASS; JS PASS; ZIP PASS. Letzter LIVE PASS bleibt 1.50.632.


## 2026-11-22 – Design 1.50.642 Weiterführende Beiträge

- 1.50.641 Nutzerprüfung: Responsive PASS, Amazon/Produkte sichtbar; Related fehlte.
- 1.50.642 ändert nur Related-Ausgabe: maximal 2 echte veröffentlichte Posts mit Bild. Kategorie-/Seitenziele werden nicht sichtbar ausgegeben.
- Grund für bisherigen Leerzustand belegt: exakte FAQ-Blattkategorien können nur den aktuellen Beitrag enthalten (Müsli FAQ und Heunetze FAQ im Export jeweils 1 veröffentlichter Post).
- Fallback bleibt innerhalb desselben bereits im Artikel verlinkten Hauptthemas und bewertet nur vorhandene veröffentlichte Beiträge; keine Kategoriezuordnung wird geändert.
- Responsive, Produkt- und Amazon-Ausgabe gegenüber 1.50.641 unverändert. 506/507 Dateien byteidentisch; PHP 9/9 PASS; JS PASS; ZIP PASS.
- Im Design-Büro gespeichert als 1.50.642 ZIP + Prüfnachweis.


## 2026-11-22 – Design 1.50.642 LIVE PASS

- Nutzer hat Designplugin 1.50.642 nach Sichtprüfung als PASS bestätigt.
- Einzelbeitrag: Responsive PASS, Amazon PASS, Produkte PASS, bis zu zwei weiterführende echte Beiträge mit Bild PASS.
- 1.50.642 ist für Live freigegeben und im Design-Büro als LIVE_PASS ZIP + Prüfnachweis gespeichert.
- Neue verbindliche Designbasis: 1.50.642. Historischer Fallback vor Einzelbeitragsumbau: 1.50.632.


## 2026-11-22 – Performanceaudit nach Plugin-Aufräumung: 6.72.369 als Query-Regression bestätigt

- Aktuell installiert laut Pluginliste: Affiliate-Zentrale 6.72.369, Template Kit 1.50.642, HivePress 1.8.3, Texterstellung 0.4.47; Kubio deaktiviert.
- Struktur ist tatsächlich schlanker: aktiver Pluginbestand 35 -> 31, Hook-Callbacks 6642 -> 6244, durchschnittliche Queries Gesamtmix 443 -> 394.
- Trotzdem aktueller Lauf langsamer; Server-Load ca. 150 -> ca. 281 ist ein separater globaler Wartezeitfaktor.
- Wichtigster belegter lokaler Fehler: 6.72.369 ist bereits durch den eigenen Live-A/B-Nachweis widerlegt. Produktseiten stiegen damals u.a. Pferdesättel 320 -> 1421 Queries, Sattel 298 -> 838, Trensen 296 -> 828, Satteldecken 311 -> 734.
- Aktueller Lauf reproduziert das Muster: Pferdesättel 1429 Queries, Sattel 846, Trensen 810.
- Ursache 6.72.369: update_post_meta_cache=false plus schmaler ppar_campaign_data-Leser verhindert die normale WordPress-Sammelbefüllung; spätere get_post_meta-Aufrufe laden Kampagnen-Metadaten einzeln nach.
- 6.72.370 entfernt ausschließlich diesen fehlerhaften schmalen Metadatenweg und stellt den historischen Sammelcache wieder her. Methoden-Harness 710 Kampagnenposts: 25/50/75/100 % Folgezugriffe 187/362/537/712 Queries -> jeweils 2; Kampagnenrecords identisch.
- 6.72.371 baut auf 6.72.370 auf und bündelt zusätzlich nachgewiesene redundante Control-/Health-Arbeit und frühe Banner-Aussortierung. Reale Pferdeatelier-Struktur-Simulation: 0 Ergebnisabweichungen; Hub/Journal deutliche Wiederholungsreduktion.
- Eigene Paketnachprüfung 22.11.: 66 Dateien, 23 PHP, Lint 23/23 PASS, Actions 176, Filter 30, Shortcodes 6. 369 -> 371: 1551 vorhandene Funktionskörper unverändert. Entfernt werden nur drei private Narrow-Meta-Hilfsfunktionen aus dem nachgewiesen fehlerhaften 6.72.369-Lesepfad; hinzu kommen zwei reine Request-Cache-Helfer. User-facing Kernfunktionen render_affiliate_slot_for_context, render_banner, build_click_tracking_url, campaign_slot_allowed, assignment_selection_for_slot, article_plan_apply_to_content, filter_the_content, select_category_product_campaign_fast_v672171 und category_product_postprocess_candidates_v672365 sind exakt unverändert.
- Produktions-Schreibprimitive 369 -> 371 unverändert; keine Änderung an Design-Plugin, Journal-Layout, HivePress, Texterstellung, Tracking, Auswahl-/Ranking-/Provider-/Placement-/Fallback-/Veto-/Health-/Renderingregeln.
- Journal-Design 1.50.629-632 betrifft nur acht redaktionelle Kategoriearchive; /journal/ Root fällt aus diesen Guards heraus. Daher aktuell kein Journal-Design-Rückbau.
- Nächster kontrollierter Schritt: ausschließlich Affiliate-Zentrale 6.72.371 installieren, keine weitere Änderung gleichzeitig; danach genau ein PASSIV-Gesamtlauf. Harte Kontrolle: Produktseiten müssen aus dem 6.72.369-Querybereich zurückfallen; Wall-Time wegen Serverlast nur sekundär bewerten.
- Freigegebenes Paket: PFERDEATELIER_AFFILIATE_6.72.371_KONSOLIDIERT_ROOTCAUSE_PERFORMANCE.zip, SHA-256 832b7b82f1b190e06250cab922b4e9ab6ee0abb7661097991ae7eca7ce87a456.


## 2026-11-23 – Affiliate-Zentrale 6.72.372 gebündelter Hotpath-Rootfix – lokal QA PASS

- Ausgangsbasis exakt installierte/freigegebene 6.72.371; Design 1.50.642 bleibt unangetastet.
- Ursachenprofil 22.11. 18:43 bestätigt Restlast im Affiliate-Produktpfad: Pferdesättel 8.539,76 ms / 3.526,40 ms CPU / 139.475 Cache-Hits / 310 Queries; category_product_1 Ø 1.984,10 ms, max. 7.585,31 ms. Der 6.72.369-Queryfehler bleibt behoben.
- 6.72.372 bündelt fünf ausschließlich dort belegte Wiederholungen: endgültige Produkt-Nichttreffer auf normalen Artikeln vor Vollnormalisierung, idealo-Strategie einmal je synchronem Listenaufruf, exakter eBay-Titellängenindex, kein erneutes eBay-Source-Prime bei bereits final gecachter Entscheidung, unmittelbar doppelte Providerprüfung im streng stabilen Control-Pfad nur einmal.
- Inhaltsbeweis Realbestand: 2.363 Produktkampagnen, Hit/Miss 4.726 Fälle 0 Abweichungen; 7.000 Legacy-Ausnahmen + 3.000 Sonder-Posttypen 0 Fehlablehnungen.
- idealo Realpool 1.010 / 617 idealo: products/comparison/hybrid 0 Ausgabeabweichungen, Strategie-Reads 617 -> 1 je Aufruf; Zustandswechsel zwischen Slots bleiben sichtbar; 500 Zufallsfälle 0 Abweichungen.
- eBay Realpool 393: Alt/Neu 315 Ausgaben, identischer Ausgabe-Hash; Paarprüfungen 78.355 -> 34.024 (-56,58 %), similar_text 21 -> 21; 53.444 mathematische Längenfälle + 250 Zufallslisten/12.725 Zeilen 0 Abweichungen.
- eBay Source: bei bereits final gecachtem post:<id>-Ergebnis bis 786 redundante Meta-Leseaufrufe pro späterem Prime vermeidbar; 16 Zustandsfälle 0 Ergebnisabweichungen.
- Control: 192 stabile Zustandskombinationen 0 Ausgabeabweichungen; dynamische/unsichere Zustände bleiben vollständig auf historischem Pfad.
- Gesamt-Funktionsschutz 6.72.371 -> 6.72.372: Dateien 66 -> 66, PHP 23 -> 23, Funktionen 1.564 -> 1.567, entfernt 0, Properties 61 -> 61, Actions 176 -> 176, Filter 30 -> 30, Shortcodes 6 -> 6; alle Produktions-Schreibprimitive identisch.
- Kritische Auswahl-/Ranking-/Fallback-/Veto-/Health-/Bild-/Tracking-/Rendering-/Artikel-Funktionen körperidentisch; andere Plugins nicht Bestandteil des Pakets.
- ZIP-Integrität PASS, PHP-Lint 23/23 PASS.
- Paket: PFERDEATELIER_AFFILIATE_6.72.372_GEBUENDELT_HOTPATH_ROOTFIX.zip
- SHA-256: 745c8fcb4d047794fed37182dcd1881cb35a36e84f83b7aa906b9755dd3ed1fb
- Voller Nachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.372.md
- Nächster kontrollierter Schritt: ausschließlich 6.72.372 installieren, danach genau ein PASSIV-Gesamtlauf. Kein weiterer gleichzeitiger Plugin-/Designumbau.


## 2026-11-23 – 6.72.372 LIVE: nur kleine Entlastung; 6.72.373 Provider-Image-DNS-Rootfix

- PASSIV 6.72.372: Pferdesättel 12.714,99 ms Wall / 3.579,54 ms CPU / 135.614 Cache-Hits / 310 Queries.
- 6.72.371 Vergleich: 8.463,96 / 3.745,47 / 139.475 / 310. Damit nur CPU ca. -4,4 % und Cache-Hits ca. -2,8 %; Query-Sicherheit bleibt erhalten, Hauptlast ungelöst.
- Neuer belegter Restmechanismus: product_campaign_public_image_ready() ruft nach der bereits provider-spezifischen Bildprüfung für jedes Produktbild wp_http_validate_url(); WordPress löst externe Hosts darin per gethostbyname() auf und prüft die IP.
- Realbestand: 2.166 aktive provider-validierte Bilder auf genau zwei realen Providerhosts (1.285 idealo cdn.idealo.com, 881 eBay ebayimg.com); 15 stale eBay-Bilder werden vorher weiterhin abgelehnt. Pferdesättel-spezifisch 1.010 aktive relevante Produktkampagnen (617 idealo / 393 eBay).
- 6.72.373 behält vollständige WordPress-Sicherheitsprüfung einmal je Providerhost und wiederverwendet ausschließlich deren Host-Ergebnis innerhalb desselben stabilen Requests. Jede URL behält Struktur/Credential/Portprüfung; dynamische/unsichere Zustände bleiben vollständig auf historischem Weg.
- Real Alt/Neu: 2.166 Fälle, 0 Ausgabeabweichungen, vollständige Prüfungen 2.166 -> 2.
- Dynamic-Fallback: 2.166 Fälle, 0 Abweichungen, 2.166 -> 2.166.
- 100.000 Randfälle: 0 Ausgabeabweichungen.
- Exakter PHP-Tokenvergleich 372 -> 373: Funktionen 1.563 -> 1.564, entfernt 0, 1.562 bestehende körperidentisch, geändert nur product_campaign_public_image_ready(), neu nur provider_product_image_http_validate_v672373().
- Actions 176 -> 176, Filter 30 -> 30, Shortcodes 6 -> 6, Produktions-Schreibwege identisch. Paket enthält ausschließlich Affiliate-Zentrale.
- ZIP 66 Dateien, PHP 23/23 PASS, 0 Hash-Abweichungen Arbeitsstand vs. finales ZIP.
- Paket: PFERDEATELIER_AFFILIATE_6.72.373_PROVIDER_IMAGE_DNS_ROOTFIX.zip
- SHA-256: 1a46c3f98b4df0cc5ac59eabe7962bcecd7d52513b58e7b6a9111aaf2b18aefe
- Nachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.373.md
- Nächster kontrollierter Schritt: ausschließlich 6.72.373 installieren und genau einen PASSIV-Gesamtlauf ausführen.


## 2026-11-24 – 6.72.373 LIVE bestätigt; 6.72.374 Provider-Control-Rootfix

- LIVE 6.72.373: Pferdesättel 3.486,00 ms Wall / 1.400,20 ms CPU / 135.789 Cache-Hits / 310 Queries. Gegen 6.72.372 (12.714,99 / 3.579,54 / 135.614 / 310) ist der DNS/Bild-Fix klar wirksam; interne Wiederholungsarbeit bleibt.
- Realbestand Pferdesättel: 1.010 Kandidaten in derselben relevanten Fallback-Stufe, 617 idealo + 393 eBay, alle mit Partner-ID.
- 6.72.373 prüft globalen Providerzustand wegen der eigenen Registry-/Access-Filter zweimal je Kandidat: 2.020 Provider-Gates.
- 6.72.374 erlaubt Wiederverwendung nur bei exakt bekannten eigenen Providerfiltern und stabiler Read-Surface. Unbekannte/dynamische Filter => historischer Einzelpfad.
- Echter Pool Alt/Neu: 0/1.010 Abweichungen; Provider-Gates 2.020 -> 2; Notstopp 1.010 -> 1; Portal 1.010 -> 1. Partner 2.020, Creative 393, Output 393, Einzelziel 2 bleiben identisch.
- Mindestzahl direkt abgeleiteter stabiler get_option/home_url-Lesewege: 10.548 -> 10.
- 500 Zustandsrequests / 17.426 Kandidaten: 0 Abweichungen.
- Dynamische Registry-/Access-/Partner-/Optionfilter plus wechselnde Providerzustände: 0 Abweichungen; Alt/Neu identische Einzelprüf-Aufrufzahlen.
- PHP-Tokenvergleich: 1.564 -> 1.570 Funktionen/Methoden; entfernt 0; 1.563 bestehende unverändert; geändert genau campaign_control_base_allows_delivery(); neu 6 Schutzhelfer.
- Actions 176, Filter 30, Shortcodes 6 und alle Produktions-Schreibprimitive identisch.
- Dateien 66 -> 66; nur Hauptdatei + Stable Tag geändert; keine andere Plugin-/Theme-/Core-Datei enthalten.
- ZIP 66/66, 0 Hashabweichungen nach Re-Extract, PHP 23/23 PASS.
- Paket: PFERDEATELIER_AFFILIATE_6.72.374_PROVIDER_CONTROL_ROOTFIX.zip
- SHA-256: 377683dd1e65ae586188e51f16e35e3a8f49d3257ea0cbfa516536c824dbe68b
- Prüfnachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.374.md
- Nächster kontrollierter Schritt: ausschließlich 6.72.374 installieren und genau einen PASSIV-Gesamtlauf ausführen.


## 2026-11-24 – 6.72.374 LIVE ausgewertet; 6.72.375 gebündelt freigegeben

- LIVE 6.72.374 bestätigt: Pferdesättel 3.495,84 ms Wall / 1.296,52 ms CPU / 135.828 Cache-Hits / 310 Queries.
- Gegen 6.72.373 sinkt CPU ca. 7,4 %, Cache-Hits und Queries bleiben praktisch unverändert. 6.72.374 ist sicher, aber der Hauptrest bleibt.
- Kein Einzel-Fix-Paket: vier belegte Restursachen wurden gemeinsam in 6.72.375 gebündelt.
- Realbestand Pferdesättel: 1.010 aktive Kandidaten, 617 idealo + 393 eBay.
- Doppelte ppar_campaign_data-Lesungen 1.091 -> 0.
- Incident-Optionslesungen 648 -> 8; dynamischer Filter behält 648 -> 648.
- voller Kandidaten-Metapfad 7.983 -> 1.010; dynamische/unsichere Kontexte behalten den historischen Einzelpfad.
- eBay Public Checkpoint 393 -> 1; checkpoint-spezifischer Filter behält 393 -> 393.
- gesamte reproduzierte Meta-/Optionslesungen im Realbestands-Hotpath 10.129 -> 1.033 (ca. -89,8 %).
- 2.721/2.721 Kampagnennormalisierungen identisch.
- 30/30 Provider-/Link-/Amazon-Kombinationen kompletter Postprocessing-Output Alt=Neu.
- 10 finale Slot-Randkombinationen: 0 Abweichungen.
- 10.000 Meta-Semantikfälle: 0 Abweichungen.
- external object cache / get_post_metadata / pre_option: historischer Pfad und Alt/Neu-Aufrufzahlen identisch.
- PHP-Tokenvergleich 1.570 -> 1.581 Funktionen/Methoden; entfernt 0; 1.555 bestehende unverändert; 15 gezielt geändert; 11 Schutzhelfer neu.
- Actions 176, Filter 30, Shortcodes 6 und Produktions-Schreibwege unverändert.
- Dateien 66 -> 66, keine fremden Plugin-/Theme-/Core-Dateien; PHP 23/23 PASS; ZIP 66/66, 0 Hashabweichungen.
- Paket: PFERDEATELIER_AFFILIATE_6.72.375_GEBUENDELT_META_READ_ROOTFIX.zip
- SHA-256: f0c813dc1b5d0de01e45f15b6a3f0bdf725ff721f6f7e3f71da10754e80c86a4
- Prüfnachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.375.md
- Büro-Ablage aktuell: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.375_GEBUENDELT_META_READ_ROOTFIX.zip
- Nächster Schritt: ausschließlich 6.72.375 installieren und genau einen PASSIV-Gesamtlauf ausführen; erst danach Live-Wirkung bewerten.


## 2026-11-24 – 6.72.375 LIVE ausgewertet

Messung: pferdeatelier-performance-gesamtanalyse-20261124-104853.json
- Affiliate-Zentrale 6.72.375 live aktiv; Source-Fingerprints von Hauptdatei/eBay/eBay-Run stimmen exakt mit dem ausgegebenen 6.72.375-Paket überein.
- Pferdesättel: 2.583,26 ms Wall / 1.214,68 ms CPU / 135.828 Cache-Hits / 310 Queries.
- Vergleich 6.72.374: 3.495,84 / 1.296,52 / 135.828 / 310.
- CPU ca. -6,3 %, Wall ca. -26,1 %, aber Server-Load gleichzeitig deutlich niedriger (ca. 82/101/84 -> 51/52/57). Der Wall-Gewinn ist daher NICHT vollständig 6.72.375 zurechenbar.
- Cache-Hits exakt unverändert: 135.828 -> 135.828; Queries 310 -> 310.
- Gemeinsame Vergleichsrouten zeigen im Mittel ebenfalls CPU-Schwankungen um mehrere Prozent. Deshalb ist der kleine CPU-Rückgang von Pferdesättel allein kein ausreichender Kausalitätsbeweis.
- Ergebnis: 6.72.375 bleibt funktional freigegeben, aber der behauptete große Live-Performanceeffekt des Meta-/Options-Rootfix ist NICHT bewiesen.
- Kein neues Plugin aus diesem Befund erzeugt.
- Aktueller Prüfpfad: dominierende Objektcache-/Post-/Term-/Inventararbeit im echten Rankingpfad untersuchen; erst mehrere belegte Ursachen bündeln und gemeinsam Alt/Neu simulieren.
- Messdatei im Büro: /pferdeatelier/PERFORMANCE_BUERO/MESSUNGEN/pferdeatelier-performance-gesamtanalyse-20261124-104853.json


## 2026-11-24 – 6.72.376 gebündelter Testkandidat freigegeben

- Live bleibt bis Installation 6.72.375.
- Nachweisbarer Restpfad: Sattel und Pferdesättel haben beide 1.010 Rohkandidaten; Sattel verarbeitet in der besten Relevanzstufe 171, Pferdesättel 1.010. Die fachliche Kandidatenprüfung wird NICHT verkürzt.
- Vier zunächst erwogene nur bedingt wirksame Änderungen (Meta/Control/Incident/eBay-Checkpoint) wurden wegen fehlendem Live-Ursachenbeweis aus dem Paket entfernt.
- 6.72.376 bündelt nur zwei direkt aktive Wiederholungen:
  - Portal/Home: Ausrüstung 3.024 -> 3; Sattel 513 -> 3; Pferdesättel 3.030 -> 3.
  - Idealo-Rohoption: auf allen drei Referenzseiten 11 -> 3.
- final ausgewählte Produkte Alt=Neu.
- 2.721 Normalisierungen identisch; Shared Pool 1.010 identisch.
- 30/30 Provider-/Link-/Amazon-Kombinationen identisch.
- 10/10 finale Drei-Slot-Auswahlen identisch.
- Dynamik-/Fallbacktests: externer Objektcache, home_url, Idealo-Optionsfilter, pre_option und echte Option-Mutationen PASS.
- Dateien 66 -> 66; entfernt 0; geändert nur Hauptdatei + Idealo-Trait + readme.
- Funktionen/Methoden 1.581 -> 1.585; entfernt 0; 1.576 bestehende unverändert.
- kritische Auswahl-/Ranking-/Provider-/Fallback-/Health-/Bild-/Tracking-/Renderfunktionen unverändert.
- Produktions-Schreibwege unverändert.
- Actions 176 -> 179 ausschließlich wegen drei Invalidierungs-Hooks für echte Option-Änderungen; Filter 30, Shortcodes 6 unverändert.
- PHP 23/23 PASS; finales ZIP 66/66, 0 Hashabweichungen nach Re-Extract.
- Paket: PFERDEATELIER_AFFILIATE_6.72.376_GEBUENDELT_CONTEXT_READ_ROOTFIX.zip
- SHA-256: ec15beafe4944eddcffc8401081c31f7d330546497fab9dd3e3f4661e0245b45
- Prüfnachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.376.md
- Büro: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.376_GEBUENDELT_CONTEXT_READ_ROOTFIX.zip
- Nächster Schritt: nur 6.72.376 installieren und genau einen PASSIV-Gesamtlauf ausführen; Livewirkung erst danach bewerten.


## 2026-11-24 – 6.72.376 LIVE ausgewertet

Messung: pferdeatelier-performance-gesamtanalyse-20261124-142623.json
- Affiliate-Zentrale 6.72.376 live aktiv.
- Hauptdatei-Fingerprint live: 4ecb3b07e74c61f81dabbcd358bc4b60daceefd215367cbbc644697706ee5614; stimmt exakt mit dem freigegebenen 6.72.376-ZIP überein.
- Pferdesättel: 5.332,37 ms Wall / 1.493,98 ms CPU / 121.246 Cache-Hits / 310 Queries.
- Vergleich 6.72.375: 2.583,26 / 1.214,68 / 135.828 / 310.
- Cache-Hits: 135.828 -> 121.246 = -14.582 bzw. ca. -10,7 %; Queries unverändert.
- Sattel-Elternseite: 81.301 -> 78.476 Cache-Hits = -2.825 bzw. ca. -3,5 %; Queries 288 -> 288.
- Lokaler Ursachenbeweis passt zur Live-Signatur: Pferdesättel Portal/Home 3.030 -> 3, Sattel 513 -> 3; damit entfernt der Fix auf Pferdesättel 3.027 und auf Sattel 510 wiederholte Portal/Home-Lesungen. Die live verschwundenen Cache-Hits skalieren in derselben Größenordnung mit dieser Differenz.
- Daher ist die Reduktion der internen Cache-Wiederholung durch 6.72.376 ursächlich belegt.
- Ein Live-Speedup ist NICHT belegt: Wall +106 % und CPU +23 % auf Pferdesättel; gleichzeitig höhere Serverlast ca. 65/66/65 statt 51/52/57 und gemeinsame Vergleichsrouten im neuen Lauf im Mittel rund +9 % CPU. Der Lauf ist für Gesamtgeschwindigkeit ungünstiger.
- OPcache-Messung erneut nahe Restart (104 s), alle Frontendrequests eingeloggt.
- Ergebnis: 6.72.376 funktional und für Cache-Reduktion live bestätigt; keine Aussage eines Speedups.
- Messdatei im Büro: /pferdeatelier/PERFORMANCE_BUERO/MESSUNGEN/pferdeatelier-performance-gesamtanalyse-20261124-142623.json
- Nächster Prüfblock: verbleibende 121.246 Cache-Hits und der weiterhin große 1.010er Vollblock in mehreren belegten Ursachen zerlegen; kein neues Paket bis mehrere sichere Punkte gemeinsam simuliert sind.


## 2026-11-24 – 6.72.377 als gebündelter Testkandidat freigegeben

- Live bleibt bis Installation 6.72.376.
- Kein Einzel-Fix: 6.72.377 bündelt mehrere bereits im echten 1.010er-Pferdesättel-Pool gemessene Wiederholungsblöcke.
- Metadaten-Hotpath 8.080 -> 1.010 Aufrufe (-87,5 %), identischer Ergebnis-Hash.
- Control: Meta 2.020 -> 1.010; Optionen 9.316 -> 11; Portal/Home 3.030 -> 3; 1.010/1.010 Entscheidungen identisch.
- Incident: 648 -> 8 Optionslesungen, identischer Hash.
- eBay Public Checkpoint: 393 -> 1 Optionslesung, 393/393 Entscheidungen identisch.
- Shared Pool: 1.010 Kandidaten Alt=Neu; Meta 3.812 -> 2.721; Optionen 648 -> 0; identische Reihenfolge.
- Relevante Filter / externer Objektcache erzwingen weiterhin historischen Einzelpfad.
- Echte Meta-/Provider-/Notstopp-/Checkpoint-Änderungen mitten im Ablauf werden sofort gesehen.
- Dateien 66 -> 66; entfernt 0; Funktionen 1.585 -> 1.591; entfernt 0; 1.575 bestehende unverändert.
- Auswahl, Ranking, Provider-Mix, Fallback, Health, Bilder, Tracking und Rendering unverändert.
- Produktions-Schreibwege unverändert.
- PHP 23/23 PASS; finales ZIP nach Re-Extract 66/66, 0 Hashabweichungen, PHP erneut 23/23 PASS.
- Paket: PFERDEATELIER_AFFILIATE_6.72.377_GEBUENDELT_EXACT_READ_ROOTFIX.zip
- SHA-256: df04630d846b0417dd0ddb1341cd2321a308ca189e0ade4c7e6adb11b2fce844
- Büro: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.377_GEBUENDELT_EXACT_READ_ROOTFIX.zip
- Prüfnachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.377.md
- Nächster Schritt: 6.72.377 installieren und genau einen PASSIV-Gesamtlauf ausführen. Live-Speedup erst danach bewerten.


## 2026-11-24 – 6.72.377 LIVE ausgewertet; 6.72.378 gebündelt freigegeben

Messung: pferdeatelier-performance-gesamtanalyse-20261124-151323(1).json
- 6.72.377 live aktiv.
- Pferdesättel: 4.859,09 ms Wall / 1.601,79 ms CPU / 89.392 Cache-Hits / 310 Queries.
- Gegen 6.72.376: Cache-Hits 121.246 -> 89.392 = -31.854 / -26,3 %; Queries 310 -> 310.
- Der große Restblock liegt im Produkt-/Inhaltsweg zwischen loop_start und Erreichen von wp_footer: 3.628,90 ms.
- Kein Einzel-Fix: 6.72.378 bündelt vier dort nachgewiesene Wiederholungen gemeinsam: redundante innere eBay-Kohorten-Schlüsselarbeit unter vorhandenem äußeren Postprocess-Plan, wiederholte Home-Host-Lesung der Bildprüfung, wiederholte vollständige Kandidaten-Fingerprints für Slot 2/3 und wiederholte GTIN-Normalisierung.
- Echter WXR-Bestand, Pferdesättel 1.010 Kandidaten (393 eBay + 617 idealo), 20 Alt/Neu-Durchläufe: Median 216,71 -> 187,71 ms (-13,38 %).
- Slot 2: 16,91 -> 6,96 ms; Slot 3: 13,23 -> 5,10 ms.
- get_post_meta 3.731 -> 3.114; get_option 324 -> 15.
- 2.721/2.721 Kampagnennormalisierungen identisch; kombinierter Hash Alt=Neu.
- 25/25 reale Seiten-/Providerkombinationen Alt=Neu: Pferdesättel, Satteldecken, Reitplatzpflege, Zeitschalt-Futterautomaten, Stall Organisation; jeweils automatic/hybrid, automatic/products, combined/products, ebay_only/hybrid, idealo_only/comparison.
- Produktplatz 1/2/3: Post-ID, Kampagnen-ID, Provider, Titel, URL, Bild, CTA, Preis, Währung, Verfügbarkeit und vollständige Kandidatenhashes identisch.
- Pferdesättel Produkt 1/2/3 bis zum echten render_banner() ausgeführt: HTML Alt=Neu.
- Dynamiktests get_post_metadata, home_url, pre_option und externer Objektcache: Alt/Neu identische Ausgaben und identische Meta-/Options-Aufrufzahlen; historischer Einzelweg bleibt erhalten.
- Echte Home-/Postmeta-/idealo-Optionsänderungen im Ablauf werden nach Invalidierung sofort gesehen.
- Dateien 66 -> 66; entfernt 0; geändert nur Hauptdatei, eBay-Trait, Idealo-Trait, readme.
- Funktionen/Methoden 1.591 -> 1.594; entfernt 0; 1.582 bestehende unverändert; 3 interne Performance-Helfer neu.
- Actions 183, Filter 30, Shortcodes 6 und Produktions-Schreibprimitive Alt=Neu.
- PHP 23/23 PASS; finales ZIP 66/66, fehlend 0, zusätzlich 0, Hashabweichungen 0; Re-Extract PHP 23/23 PASS.
- Paket: PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_POSTPROCESS_ROOTFIX.zip
- SHA-256: 9283dd3b4237717db084708f981b2b4ef3b5b7c67568794a66f47c522f265bd7
- Büro: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_POSTPROCESS_ROOTFIX.zip
- Prüfnachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.378.md
- Nächster Schritt: 6.72.378 installieren und genau einen PASSIV-Gesamtlauf ausführen; Live-Speedup erst danach bewerten.


## 2026-11-24 – KORREKTUR 6.72.378: Erstkandidat verworfen, nur kausal belegte A+C freigegeben

- Der zuvor dokumentierte 6.72.378-POSTPROCESS_ROOTFIX mit vier Maßnahmen und SHA 9283dd3b4237717db084708f981b2b4ef3b5b7c67568794a66f47c522f265bd7 ist VERWORFEN und darf NICHT installiert werden.
- Verschärfte Einzel-Kausalitätsprüfung gegen denselben echten 1.010er-Pferdesättel-Bestand.
- Maßnahme A direkt im betroffenen eBay-Kohortenabschnitt: Median 78,83 -> 62,34 ms (-20,9 %); Meta 1.010 -> 393; 315 -> 315 Ergebnisse; geordneter Output-Hash identisch.
- Maßnahme C direkt für die wiederholte Schlüsselarbeit von Produktplatz 2+3: 17,08 -> 1,67 ms (-90,2 %).
- Gesamt A+C, 10 alternierende Realbestandsläufe: 220,75 -> 188,04 ms (-14,82 %); Meta 3.731 -> 3.114; Optionen unverändert 324 -> 324; Produkte 1/2/3 identisch.
- Verworfen wegen fehlendem/negativem Zeitbeweis: Home-Host-Cache (ca. +1,3 %), GTIN-Cache (17,19 -> 20,25 ms, langsamer), Deferred-Titelsignatur (242,72 -> 259,33 ms, langsamer), Seller-Key-Cache (kein stabiler Gewinn).
- Funktionsbeweis ist inhaltlich, nicht Bytevergleich: 2.721/2.721 reale Normalisierungen identisch; 25/25 reale Seiten-/Providerkombinationen identisch; 75/75 tatsächlich gerenderte Produktkarten inkl. HTML identisch.
- Sechs explizit aktivierte dynamische Sonderfälle (Metadata-, sanitize_key-, pre_option-, idealo-pre_option-, home_url-Filter, externer Objektcache): Fachausgabe UND Aufrufzahlen Alt=Neu; historischer Einzelweg bleibt erhalten.
- Echte Meta-/Provider-/Strategieänderungen während des Ablaufs werden Alt=Neu erkannt.
- Struktur nur Zusatzbeweis: 66 Dateien, 23 PHP-Dateien, 1.591 -> 1.593 Funktionen/Methoden, entfernt 0; Produktions-Schreibprimitive unverändert.
- Finale Paketprüfung: PHP 23/23 PASS; Re-Extract 66/66; fehlend 0; zusätzlich 0; Hashabweichungen 0; Re-Extract PHP erneut 23/23 PASS.
- Einziger freigegebener Kandidat: PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_CAUSAL_ROOTFIX.zip
- SHA-256: af39e106c595be83210d2c4a164c1274c723d25c2a2599b77f86488e4eda9839
- Büro: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_CAUSAL_ROOTFIX.zip
- Prüfnachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.378.md
- Nächster Schritt: ausschließlich diese korrigierte 6.72.378 installieren und genau einen PASSIV-Gesamtlauf ausführen.


## 2026-11-24 – 6.72.378 LIVE bestätigt

Messung: pferdeatelier-performance-gesamtanalyse-20261124-173614.json
- LIVE-Version 6.72.378 bestätigt; Source-Fingerprints stimmen exakt mit dem freigegebenen korrigierten CAUSAL_ROOTFIX.
- Pferdesättel: 2.222,09 ms Wall / 1.092,40 ms CPU / 89.461 Cache-Hits / 310 Queries.
- Gegen 6.72.377: Wall -54,27 %, CPU -31,80 %, Cache +69, Queries unverändert.
- Inhalts-/Produktausgabeblock loop_start -> wp_footer: 3.628,90 -> 1.492,57 ms (-58,87 %).
- Host-/Laufbedingungen sind ebenfalls günstiger; daher wird der volle Wall-Gewinn nicht dem Plugin zugerechnet.
- Vergleichsrouten verbessern sich CPU-seitig im Median um ca. -15,22 %. Pferdesättel liegt bei -31,80 %, also ca. 16,6 Prozentpunkte zusätzlicher Rückgang.
- Dieser Zusatz liegt nahe am lokal isolierten A+C-Gewinn von -14,82 %. Damit stimmt der Live-Effekt in Richtung und Größenordnung mit dem Kausaltest überein.
- Kein neues Plugin aus dem Live-Lauf erzeugt.
- Messdatei im Büro: /pferdeatelier/PERFORMANCE_BUERO/MESSUNGEN/pferdeatelier-performance-gesamtanalyse-20261124-173614.json
- Nächster Prüfblock: gemeinsamer Kandidatenaufbau (~81 ms / 2.721 Kampagnendaten-Lesungen) plus verbliebenes Produkt-1-Postprocessing (~100 ms) weiter zerlegen und mehrere belegte Ursachen bündeln.


## 2026-11-24 – 6.72.379 gebündelter Testkandidat H+I freigegeben

- LIVE bleibt 6.72.378.
- Kein Einzel-Fix: 6.72.379 bündelt zwei getrennt kausal belegte Wiederholungen im exakten Zielzuordnungspfad.
- H: 2.363 Prüfungen / nur 156 eindeutige Zielschlüssel-Sätze; direkter Abschnitt 6,676 -> 1,649 ms (-75,30 %), Ergebnis identisch.
- I: bereits kanonische Zielschlüssel; direkter Abschnitt 12,769 -> 3,618 ms (-71,66 %), Ergebnis identisch.
- Whole-Path-Inkrementalbeweis: H zusätzlich zu I -2,36 %; I zusätzlich zu H -5,67 %.
- H+I 24 Realbestandsläufe: 198,743 -> 183,221 ms (-7,81 %).
- finales Re-Extract-ZIP 20 Alternierungen: 201,865 -> 187,102 ms (-7,31 %).
- Verworfene Ansätze: E +4,84 %, F betroffener Abschnitt +3,45 %, G +8,87 %, J +0,13 % / kein stabiler Gewinn.
- Funktionsbeweis: 2.721/2.721 Normalisierungen, 25/25 reale Seiten-/Providerfälle, 75/75 gerenderte Karten inkl. HTML Alt=Neu.
- Dynamische Filter-/Object-Cache-Fälle: Ausgabe UND Meta-/Options-Aufrufzahlen Alt=Neu.
- echte Meta- und Provider-/Strategiemutation im selben Ablauf Alt=Neu.
- Funktionen 1.593 -> 1.593; entfernt 0; hinzugefügt 0; geändert nur category_product_shared_rank_base() und ranked_campaign_raw_target_keys().
- Schreibwege, Actions, Filter und Shortcodes unverändert.
- Paket 66/66, PHP 23/23 PASS, Re-Extract 0 Abweichungen.
- Paket: PFERDEATELIER_AFFILIATE_6.72.379_GEBUENDELT_EXACT_TARGET_ROOTFIX.zip
- SHA-256: 264b872aae3238027b38304282ddc6fcca868cb8a0b46629ad85f67b813ecc67
- Büro: /pferdeatelier/PERFORMANCE_BUERO/AKTUELLES_PLUGIN/PFERDEATELIER_AFFILIATE_6.72.379_GEBUENDELT_EXACT_TARGET_ROOTFIX.zip
- Prüfnachweis: protocol/PFERDEATELIER_PERFORMANCE_BUERO/PRUEFNACHWEIS_6.72.379.md
- Nächster Schritt: ausschließlich 6.72.379 installieren und genau einen PASSIV-Gesamtlauf ausführen.


## 2026-11-25 – 6.72.379 LIVE ausgewertet

Messung: pferdeatelier-performance-gesamtanalyse-20261125-091933.json
- LIVE-Version 6.72.379 bestätigt; Hauptdatei-Fingerprint 0501805a4aaaa03e7c48cd930de0c27b92a21ab343cb8b3a9f5af7bd54da99a8 entspricht exakt dem freigegebenen Paket.
- Pferdesättel: 2.435,59 ms Wall / 1.127,46 ms CPU / 89.460 Cache-Hits / 316 Queries.
- Gegen 6.72.378: Wall +9,61 %, CPU +3,21 %, Cache praktisch unverändert, Queries +6.
- loop_start -> wp_footer: 1.492,57 -> 1.601,48 ms (+7,30 %).
- Kontrollrouten CPU-Median ca. -0,06 %; Serverlast nicht höher, OPcache-Neustartnähe ähnlich.
- Zwischen den Läufen wurden weitere Plugins geändert (Relevanssi, Texterstellung, WPForms) und der Pferdesättel-Request hat 6 zusätzliche Queries. Deshalb kein kausaler Rückschritt von H+I beweisbar.
- Der einzelne Live-Gesamtlauf bestätigt den erwarteten kleinen H+I-Gewinn nicht. Der direkte lokale Kausaltest bleibt gültig: finaler Realpfad -7,31 % bei identischer Fachausgabe.
- Kein neues Plugin aus diesem Bericht erzeugt; 6.72.379 bleibt installiert, da kein bewiesener Funktions- oder Performance-Rückschritt durch H+I vorliegt.
- Messdatei im Büro: /pferdeatelier/PERFORMANCE_BUERO/MESSUNGEN/pferdeatelier-performance-gesamtanalyse-20261125-091933.json
- Nächster Schritt: Restpfade weiter isolieren und mehrere neue, direkt messbare Ursachen sammeln, bevor ein nächstes Paket gebaut wird.


## 2026-11-25 – Freigabestandard verschärft

- Nutzeranforderung verbindlich präzisiert: keine Plugin-Ausgabe mehr auf Basis von Teilpfad- oder Mikrobenchmark-Gewinnen.
- Fehler bei 6.72.379: lokal waren H+I kausal und der isolierte Realpfad schneller, aber der vollständige lokale Seitenpfad war vor Ausgabe nicht als klarer Gesamtgewinn nachgewiesen. Nach neuem Standard wäre 6.72.379 nicht ausgegeben worden.
- Ab sofort Pflicht vor jeder Ausgabe: vollständige lokale Alt/Neu-Seitensimulation mit echten Daten, mehrere alternierende Läufe, jede Einzelmaßnahme separat kausal schneller, Bündelung erneut schneller, komplettes Rendering und inhaltlicher Funktionsvergleich.
- Bytevergleich/Dateigrößenvergleich zählt nur als Zusatzbeweis.
- Funktionsschutz muss Kandidaten, Reihenfolge, Ranking, Provider, Links/Tracking, Bilder, Preise, Fallbacks, dynamische Änderungen, Filter, Objektcache und tatsächlich gerendertes HTML abdecken.
- Live-Messung dient nur noch als Bestätigung des vorher vollständig lokal bewiesenen Gesamtgewinns.
- Kein neues Plugin, solange diese Hürde nicht vollständig bestanden ist.


## 2026-11-25 – 6.72.380 vor Ausgabe vollständig lokal freigegeben

- Freigabestandard eingehalten: nicht Teilpfad, sondern finales neu entpacktes ZIP als vollständiger Seitenpfad gemessen.
- 20 alternierende Vollpfad-Läufe: 465,55 -> 248,58 ms = -46,61 %.
- fünf weitere Seitenpfade alle schneller: -41,80 %, -46,51 %, -31,04 %, -17,37 %, -11,10 %.
- Inhaltlicher Funktionsbeweis: 2.721/2.721 Kampagnennormalisierungen, 25/25 Provider-/Strategiefälle, 75/75 gerenderte Karten und 2.955/2.955 Sicherheits-/Policyfälle Alt=Neu.
- dynamische Sicherheitsfälle inkl. Notabschaltung, Providerpause, Filter, externer Cache, Locale, REST und Cron Alt=Neu.
- kein bestehender Funktionsname entfernt; Schreibwege unverändert.
- Paket 66/66; PHP 23/23; Re-Extract 0 Abweichungen.
- Paket: PFERDEATELIER_AFFILIATE_6.72.380_GEBUENDELT_PERFORMANCE_ROOTFIX.zip
- SHA-256: 00da8aa7bf6ff560563433abeb643eb0352b72ef5a97c1314a6a40c365223348
- Büro und Prüfnachweis gespeichert.
- Nächster Schritt: nur 6.72.380 installieren und danach ein PASSIV-Live-Lauf.


## 2026-11-25 – 6.72.380 LIVE: lokaler Freigabebeweis als WordPress-Gesamtbeweis verworfen

- PASSIV-Datei: pferdeatelier-performance-gesamtanalyse-20261125-102437.json
- Paketidentität live exakt bestätigt.
- Pferdesättel: 3.102,79 ms Wall / 1.135,25 ms CPU / 310 Queries.
- gegen 6.72.379: CPU +0,69 %; kein messbarer Live-Speedup.
- Kontrollrouten CPU-Median ca. -3,36 %, also kein Hinweis, dass 6.72.380 im Hotpath relativ besser wurde.
- Wall nicht kausal: Server-Load im neuen Lauf 45/72/132 statt vorher 44/48/52.
- Ursachenprüfung des lokalen Harness: er führte vollständig die drei Affiliate-Slots mit echten WXR-Kampagnendaten aus, aber keinen vollständigen WordPress-Seitenrequest.
- außerdem fehlte die reale Live-Tabelle slfo_ppar_ebay_items (aktuell 8.114 Zeilen); Source-Zeilen waren im Harness deterministisch erzeugt.
- daher ist -46,61 % nur ein interner Affiliate-Harnesswert, kein belastbarer WordPress-Gesamtreleasebeweis.
- ab sofort Performance-Release-Sperre für WXR+Stub-Harness; er bleibt ausschließlich für Fachregression/Hotpath-Vergleich.
- inhaltlicher Funktionsschutz von 6.72.380 bleibt für die tatsächlich geprüften Fachfälle bestehen.
- kein neues Plugin und kein Rückbau allein aus diesem Lauf.
