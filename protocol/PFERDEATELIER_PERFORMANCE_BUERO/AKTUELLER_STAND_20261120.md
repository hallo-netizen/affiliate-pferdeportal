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
