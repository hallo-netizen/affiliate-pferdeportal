# HAB-004 RC12 – 07.11.2026 – NUR GEPRÜFTE TESTVERSION, NICHT CURRENT

**WICHTIG:** GitHub-CURRENT.zip bleibt 0.1.8-rc11 (vorher live durchgefallen). RC12 ist eine im Chat erstellte **lokale Test-ZIP**, NICHT als GitHub Release oder Live-PASS freigegeben. Keine Behauptung, sie wäre bereits installiert. Originalcode der anderen Portale nicht verändert.

## Realer Fehler / Ursachen
Nutzer-Screenshots 07.11. 16:46/16:47 Uhr, Wassermelder: Amazon-ASIN-/Titel aus DataForSEO erfolgreich; echte Produkbilder fehlen, originale Pferdeatelier-Kartengeometrie erzwingt große Leerflächen. Separat: vorhandener Hab Kategorie-Banner-Anschluss verwirft `kind=banner`, und Amazon-Fallback ist ein bloßer Textlink.

## Harte Vergleichsprüfung
Vollständige Original-ZIPs Hab Affiliate RC11, HAB-001 Design, Hobbydepot HD009 0.1.20 und Pferdeatelier original Affiliate-Current überprüft. In Hab sind die originalen Produktbild-/Mehr-Anbieter-Funktionen bereits vorhanden. Originale eBay-/Idealo-/Kampagnen-Sortierung bleiben unverändert. Aus DataForSEO Amazon Products API ist technisch `image_url` abrufbar, aber eine Amazon-PartnerNet-freigegebene Quelle für produktgenaue Werbebilder ist **NICHT** in den gespeicherten Hab-Suchergebnissen/Plugins nachgewiesen. Keine Rechtebehauptung, keine Bildkopie. Amazon verlangt produktgenaue Bildinhalte über zugelassene Programmschnittstellen (Creators API).

**Originäre Designfotos:** Aus echtem HAB-001 CURRENT.zip Mapping und Assets überprüft: `Wasser & Feuchtigkeit :: Leckage & Rohrbruch :: Wassermelder` -> `topic-62-wassermelder.webp` EXISTIERT, `... :: Leckwarnung & Absperrung` -> `new-boiler.webp` EXISTIERT; freigegeben als Themenbild, nicht als exaktes ASIN-Produktbild.

## RC12 lokale Test-ZIP – genau 5 geänderte Dateien von 28
- `includes/class-ppar-hab-bewahr-bridge.php`: echter Kategorie-Banner-Aufruf über den ALTBESTEHENDEN `provide_leaf_category_affiliate_slot_html`, keine zweite DB.
- `includes/trait-ppar-hb-amazon.php`: nur nach erfolgloser vorhandener Kampagnenauswahl das bereits vom Design verifizierte Themenbild auf dem nativen Amazon-Übergangs-Banner, Suchlink mit `habundbewahr-21`; keine erfundenen Produkbilder; keine weiteren DataForSEO-Anfragen.
- `affiliate-portal-router.php` plus `assets/frontend.css`: nur tatsächlich bildlose Amazon-Einzelkarten kompakt, ohne die originale 416/360/210-pixel-Produkthöhe. Original-Renderer mit Bildern und Mehranbieter-Funktion für eBay/Idealo unverändert.
- `readme.txt`: Version 0.1.9-rc12.

**Harte Offline-Ergebnisse:** 23/28 Originaldateien byteidentisch; 25/25 PHP-Lints; 28/28 ZIP CRC; 10 gezielte PHP-Positiv-/Negativproben bestanden; echter Chrome-Layout-Test 1024px/390px: Produktkarte 111px/155px (statt >360), Themenbanner 217px/207px, kein Horizontal-Overflow. Achtung: Browser nur Mock-WordPress-DOM, kein echtes Live-WordPress. Kein Online-End-to-End-Test. Vor endgültiger Installation zuerst echte Amazon-Produktfotorechte und -quelle klären; sonst ist der gesamte Zielvertrag nicht erfüllt.

## Abschlusskriterien für finale Pluginversion
1. Echter verifizierter Amazon-ASIN-Artikel + passendes freigegebenes **exaktes Produktfoto** im bereits vorhandenen PPAR-Renderer, ohne eBay/Idealo-Abhängigkeit; eBay-/Idealo-Buttons erst bei IDENTISCHER Produktkennung.
2. Ansonsten keine unbeschrifteten Leerbildkarten.
3. Vorhandene freie Bannerflächen: Hobbydepot-Muster mit **eigenem Hab-Themenbild**, Amazon-Suchlink, bestehende Anzeige-Slots, gebuchte Kampagnen zuerst.
4. Volle Original-Pferdeatelier-/Hobbydepot-/HAB-001-Kompatibilität, global OFF, kein weiterer bezahlter DataForSEO-POST, WordPress-Live-Screenshots nach Installation.
5. GitHub-CURRENT erst nach vollständiger Abnahme ersetzen; keine RC12-Test-ZIP ungeprüft als freigegebenen Installer ausgeben.

Quelle Amazon-Richtlinien: https://partnernet.amazon.de/help/operating/policies
