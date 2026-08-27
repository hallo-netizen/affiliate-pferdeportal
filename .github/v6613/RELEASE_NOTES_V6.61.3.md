# Affiliate-Zentrale V6.61.3 – PRODUCT-CARD / IMAGE ROOTFIX

Datum: 27.08.2026

## Reproduzierte Livefehler
- Kategorie-Produktkarten waren unterschiedlich hoch.
- eBay-BUSINESS-Karten konnten mit nicht mehr ladbarem Browserbild erscheinen.
- idealo-Hybridkarten waren bildlos und dadurch geometrisch abweichend.
- iPN-Bild-URLs enthalten wie Klick-URLs `!!TIME_STAMP!!`; Bildtoken wurde bisher nicht explizit zur Laufzeit ersetzt.

## Rootfix
- Öffentliche Produktkarten benötigen Titel + Bild.
- V6.18 bleibt erhalten: pending eBay-BUSINESS darf intern materialisiert werden; öffentlich erst nach realer Bildverifikation.
- eBay-Ausgabe wird an kanonischen Creative-Library-Datensatz, Bildstatus, Maße und SHA-256 gebunden. Stale/kaputte Kandidaten werden übersprungen; nächster gültiger Kandidat rückt auf.
- Verifiziertes eBay-Bild wird hashidentisch serverseitig geprüft und als lokale Browserquelle gecacht; Fehlversuche sind gedrosselt.
- idealo-Hybrid-Familienkarte erhält ein repräsentatives Bild ausschließlich aus derselben sicher gemappten Produktfamilie, ohne Preis-/GTIN-/Produktidentitätsübernahme.
- iPN-Timestamp wird auch in Bild-URLs zur Laufzeit ersetzt.
- `category_product_1..3`: gemeinsamer 150×150-`contain`-Bildvertrag und gleiche Kartenhöhe im echten Affiliate-Renderer. Kein `cover`, kein Designplugin-Eingriff.

## Scope
Gegen V6.61.2 geändert: exakt 5 Dateien: `assets/frontend.css`, `includes/trait-ppar-article-plans.php`, `includes/trait-ppar-idealo.php`, `pferdeportal-affiliate-router.php`, `readme.txt`.

Byteidentisch: eBay-Providerkern, eBay-Run/Safe-Gap/Heartbeat, Network-Sync, Output-Objects, Creative-Library, Frontend-JS, eBay-Katalog, Portalstruktur.

## Prüfergebnis
- Produktbild-/Fallback-/eBay-Hashcache-Tests: PASS
- Idealo/Multi-Provider/Hybrid/GTIN/Negativfälle: PASS
- eBay-Parität: 2.000/2.000 PASS
- Async-Worker/Self-Heal/kein Doppelworker: PASS
- Browser-Geometrie: 326/326/326 px, Medien 150×150, `contain`: PASS
- PHP: 14/14 PASS
- Fresh-Unpack: 19/19 byteidentisch PASS
- ZIP-Integrität: PASS
- Fullfeed 2901 Struktur: 2.041.826 Zeilen, 2.041.826 HTTPS-Bildlinks, Timestamp in allen Bild- und Klicklinks; 2747 vollständig in 2901 enthalten.

LOCAL RELEASE GATE: PASS. Live-Sichtprüfung nach Installation bleibt extern offen.