# Affiliate-Zentrale 6.72.171 – Category-Product Performance Rootfix

Datum: 2026-10-01
Status: PASS / INSTALLER LOCAL BYTE-IDENTISCH GEBAUT / LIVE-READBACK OFFEN

## Anlass

Die reale Performance-Diagnose nach 6.72.170 zeigte weiterhin einen klaren Hierarchie-/Product-Slot-Unterschied:
- Top-Kategorie `/ausruestung/`: ca. 1.65 s Serverzeit.
- zweite/dritte Kategorieebene mit Produktkarten: z. B. Trensen-Unterzweig ca. 8.91 s, Trensen ca. 8.62 s, Pferdesättel ca. 9.09 s.
- DB-Query-Zahl blieb in derselben Größenordnung; der Restaufwand lag im wiederholten PHP-Ranking-/Gate-/Providerpfad der drei `category_product_1..3`-Slots.

## Rootfix 6.72.171

Nur normale öffentliche Frontend-Requests:
- slot-unabhängiges Kategorieprodukt-Kontextranking wird pro Seite einmal gebaut und für `category_product_1..3` wiederverwendet;
- exakte Target-Ranks identischer Target-Key-Sets werden request-lokal memoisiert;
- unveränderte Control-/Health-/Image-Gates werden request-lokal wiederverwendet;
- Slot-Veto bleibt pro Slot separat;
- eBay-Source-/Duplicate-/Provider-Cohort-Arbeit wird nur bei identischem Input request-lokal wiederverwendet;
- Placement, Control/Veto, Provider-Mix, finale Slot-Auswahl, PRIVATE/BUSINESS, Coverage, Quality, Health, Tracking und Design bleiben fachlich unverändert;
- Admin/Worker-Pfade verwenden weiterhin den bisherigen uncached Weg.

Geänderte Runtime-Dateien gegenüber exakt freigegebenem 6.72.170:
1. `pferdeportal-affiliate-router.php`
2. `includes/trait-ppar-automation-suite.php`
3. `includes/trait-ppar-ebay.php`

Getesteter Source-Head:
`ad4db0c34552667a9d398d4b74cb7d8b7130f03a`

## 1:1 Positiv-/Negativ-A-B

Run `36839006440` – Affiliate 6.72.171 Exact Local A-B – SUCCESS.

Basis und Kandidat:
- 6.72.170 gegen 6.72.171;
- WordPress 7.1.2;
- MariaDB 10.11;
- identische DB und identische Frontend-Fixture;
- Hub-Banner plus drei Kategorieprodukt-Slots.

Positiv/Negativ:
- identische ausgewählte Kampagnen;
- identische HTML-Hashes und HTML-Längen;
- identische Kandidatenreihenfolge/-anzahl;
- Slot-1/2/3-Bindung bleibt strikt slotbezogen;
- falsches Target ausgeschlossen;
- inaktive Kampagne ausgeschlossen;
- falscher Creative-Typ ausgeschlossen;
- direkte Seitenbindung vorhanden;
- Parent/Descendant-Bindung vorhanden;
- alle drei Produktkarten vorhanden;
- WP-CLI/Admin bleibt außerhalb des Frontend-Caches.

Messung:
- 6.72.170 Median: 393.694 ms
- 6.72.171 Median: 365.895 ms
- Verbesserung: 7.06 %
- Ergebnis: `EXACT_LOCAL_AB_POSITIVE_NEGATIVE_NO_REGRESSION_PASS`

## Realitätsnähere 2012er Snapshot-A-B

Run `36839006513` – Affiliate 6.72.171 Snapshot Exact Local A-B – SUCCESS.

Fixture:
- historischer 2012-Zeilen-Produktbestand aus dem vorhandenen read-only Snapshot;
- 1518 aktive Produkte;
- 922 eBay;
- 1090 idealo;
- 118 reale Hub-Target-Hits;
- 43 reale Leaf-Target-Hits;
- drei explizite positive Anker nur zur Sicherung sichtbarer Produktkarten; die 2012er Topologie bleibt die Timinglast.

Funktionsgleichheit:
- ausgewählte Kampagnen 1:1 identisch;
- HTML-Hashes 1:1 identisch;
- geordnete Kandidatenzahlen 1:1 identisch;
- Hub und Leaf haben in allen drei Produkt-Slots sichtbare Ausgabe;
- shared rank base exakt einmal pro Kontext.

Performance:
- Gesamt: 1248.595 ms -> 249.597 ms = 80.01 % schneller.
- Hub-Kontext: 658.457 ms -> 189.623 ms = 71.20 % schneller.
- Leaf-/Unterkategorie-Kontext: 587.812 ms -> 59.572 ms = 89.87 % schneller.
- Kandidatenzahl blieb unverändert: je Kontext 710 Kandidaten in category_product_1, 2 und 3.
- Ergebnis: `SNAPSHOT_EXACT_LOCAL_AB_POSITIVE_NEGATIVE_PERFORMANCE_PASS`.

## Fresh Installer-Verifikation

Der Installationsbaum wurde bytegenau gegen den getesteten GitHub-Source-Head geprüft:
- 27/27 Dateien vorhanden;
- Git-Blob-SHA 27/27 identisch mit dem aktuellen Source-Baum;
- PHP-Lint 21/21 PASS;
- Pluginheader und Runtime-Konstante: 6.72.171;
- Fresh-Unpack erneut: 27 Dateien, PHP 21/21 PASS;
- drei geänderte Runtime-Dateien nach Fresh-Unpack erneut blob-identisch.

Lokaler finaler Installer:
`AFFILIATE_ZENTRALE_6.72.171.zip`

SHA-256:
`769bcf21e7b89da68bc97cd32a284124174ad1e712575a16c4b55d5db8298714`

Source-Manifest SHA-256:
`5094f6df73c172b01819294d3dd455002fa244aa9676da0ebbbb4b058530dda4`

## Reuse der bestehenden 6.72.170 Full-Gates

Die 6.72.170-Provider-/Recovery-/Storage-/Fresh-Unpack-Gates bleiben gültige Baseline-Evidence. 6.72.171 ändert ausschließlich die oben genannten request-lokalen Frontend-Performancepfade. Die A-B-Gates prüfen die betroffene Semantik direkt gegen exakt 6.72.170 und verlangen byte-/outputgleiche Ergebnisse. Es wurde kein fachlicher Gate gelockert.

## Offen

Genau eine reale Anschlussprüfung bleibt:
6.72.171 installieren/readbacken und danach dieselbe Performance-Diagnose auf dem realen Pferde-Atelier wiederholen.

Der isolierte Campus-`CURRENT.zip`-Sync wird separat im Pluginmanifest geführt. Keine Binärkopie wird behauptet, solange kein bytegenauer Repository-Transfer nachgewiesen ist.
