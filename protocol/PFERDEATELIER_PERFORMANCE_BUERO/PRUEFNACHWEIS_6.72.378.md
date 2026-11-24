# Pferdeatelier Affiliate-Zentrale 6.72.378 – gebündelter Postprocess-Rootfix

Stand: 24.11.2026
Basis: live gemessene 6.72.377
Paket: PFERDEATELIER_AFFILIATE_6.72.378_GEBUENDELT_POSTPROCESS_ROOTFIX.zip
SHA-256: 9283dd3b4237717db084708f981b2b4ef3b5b7c67568794a66f47c522f265bd7

## Live-Ausgangspunkt
- 6.72.377 Pferdesättel: 4.859,09 ms Wall / 1.601,79 ms CPU / 89.392 Cache-Hits / 310 Queries.
- Gegen 6.72.376: Cache-Hits 121.246 -> 89.392 (-26,3 %), Queries 310 -> 310.
- Verbleibender großer Produkt-/Inhaltsblock loop_start -> wp_footer: 3.628,90 ms.

## Vier gebündelte Ursachen
1. Redundante innere eBay-Kohorten-Schlüsselarbeit entfällt, wenn der bereits vollständig abgesicherte äußere Postprocess-Plan autoritativ ist. Die Fachverarbeitung selbst bleibt erhalten.
2. Der Home-Host der Bildprüfung wird im stabilen Request einmal gelesen statt für jeden Bildkandidaten erneut; echte Optionsänderungen invalidieren ihn.
3. Vollständige Kandidaten-Fingerprints des privaten Shared-Ranking-Pfads werden einmal gebildet und für Produktplatz 2/3 wiederverwendet; direkte/generische Aufrufer behalten den vollständigen historischen Kandidatenhash.
4. Finale GTIN-Ergebnisse unveränderter Kampagnen werden request-lokal wiederverwendet; Kampagnensignatur und Postmeta-Mutationsinvalidierung schützen die Semantik.

## Performancebeweis mit echtem Bestand
WXR: pferdeatelier.WordPress.2026-11-22.xml
Pferdesättel: 1.010 reale Kandidaten = 393 eBay + 617 idealo.

20 vollständige Alt/Neu-Durchläufe:
- 6.72.377 Median 216,71 ms
- 6.72.378 Median 187,71 ms
- -13,38 %

Slots:
- Produkt 1: 186,84 -> 174,91 ms
- Produkt 2: 16,91 -> 6,96 ms
- Produkt 3: 13,23 -> 5,10 ms

Leseaufwand:
- get_post_meta 3.731 -> 3.114 (-16,54 %)
- get_option 324 -> 15 (-95,37 %)

GTIN-Mikrotest, 10.000 identische Aufrufe, Median aus 10 Läufen:
- 23,12 -> 13,10 ms bei identischem Ergebnis.

## Inhaltlicher Funktionsbeweis
Kein reiner Bytevergleich.

### 2.721 reale Kampagnen
- 2.721/2.721 vollständige Normalisierungen Alt=Neu.
- 0 Fehlnormalisierungen.
- kombinierter Ergebnis-Hash Alt=Neu:
  b3ebc847bbf5bfb8927988a96f4c391384ba731e7b798835e418243e6312ba17

### 25 reale Seiten-/Providerkombinationen
Seiten:
- Pferdesättel
- Satteldecken
- Reitplatzpflege
- Zeitschalt-Futterautomaten
- Stall Organisation

Modi je Seite:
- automatic + hybrid
- automatic + products
- combined + products
- ebay_only + hybrid
- idealo_only + comparison

Ergebnis 25/25 Alt=Neu:
- Shared-Ranking-Basis
- Kandidatenanzahl
- Produktplatz 1/2/3 vollständige Kandidatenhashes
- Post-ID, Kampagnen-ID, Provider, Titel, URL, Bild, CTA, Preis, Währung, Verfügbarkeit, Providerzahl

### Gerenderte Produktkarten
Pferdesättel Produkt 1/2/3 bis render_banner():
- Produkt 1 HTML-Hash 96d6b966e58fa43f56e3e8e90cda1a4e2d961ba77816116a2a46d8f39cb5b77b
- Produkt 2 HTML-Hash 73695c3aed20046638927d97df3a9ad630248e54ad3359bd91f8a58a4b2efd6e
- Produkt 3 HTML-Hash 63462077064236244807d4b1d6ecf80adf388f02aef3516d533ba66224af8da9
- HTML Alt=Neu; Kampagnen-, Gruppen- und Bannerstrukturen ebenfalls identisch.

### Dynamik-/Fallback-Schutz
Alt=Neu unter:
- get_post_metadata-Filter
- home_url-Filter
- globalem pre_option-Filter
- externem Objektcache

In allen vier Fällen:
- gleiche Shared-Ranking-Basis
- gleiche drei Produktauswahlen
- gleiche Slot-Kandidatenhashes
- exakt gleiche Meta-/Options-Aufrufzahlen
- historischer Einzelweg bleibt aktiv.

Zusätzlich:
- direkte In-Memory-Kandidatenänderung ändert weiterhin den vollständigen generischen Plan-Key.
- echte Home-Optionsänderung wird nach Invalidierung neu gelesen.
- echte Postmeta-Änderung wird nach Mutation-Hook neu gelesen.
- idealo-Modusänderung zwischen Slots liefert Alt/Neu dieselbe nachfolgende Auswahl.

## Bestandsschutz
- Dateien 66 -> 66; entfernt 0; hinzugefügt 0.
- geändert nur Hauptdatei, eBay-Trait, Idealo-Trait, readme.
- Funktionen/Methoden 1.591 -> 1.594.
- entfernt 0.
- 1.582 bestehende Funktionen token-inhaltlich unverändert.
- 9 bestehende Funktionen nur im gemessenen Lese-/Postprocess-/Invalidierungspfad geändert.
- 3 interne Performance-Helfer neu.
- Actions 183 -> 183.
- Filter 30 -> 30.
- Shortcodes 6 -> 6.
- update_option 290 -> 290; delete_option 37 -> 37.
- update_post_meta 85 -> 85; delete_post_meta 10 -> 10.
- wp_insert_post 3 -> 3; wp_update_post 12 -> 12.
- $wpdb->insert 13 -> 13; $wpdb->update 76 -> 76; $wpdb->delete 2 -> 2; $wpdb->query 16 -> 16.
- Produktions-Schreibwege damit nicht entfernt oder verkürzt.

## Paketprüfung
- PHP 23/23 PASS.
- ZIP 66/66.
- fehlend 0, zusätzlich 0.
- Arbeitsstand vs. Re-Extract: 0 Hashabweichungen.
- Re-Extract PHP 23/23 PASS.
- ZIP-Wurzel ausschließlich affiliate-portal-router/.
- Header/Klassenkonstante/Stable Tag 6.72.378.

## Grenze
6.72.378 ist lokal als gebündelter Testkandidat freigegeben. Live-Speedup erst nach Installation und PASSIV-Gesamtlauf bewerten.
