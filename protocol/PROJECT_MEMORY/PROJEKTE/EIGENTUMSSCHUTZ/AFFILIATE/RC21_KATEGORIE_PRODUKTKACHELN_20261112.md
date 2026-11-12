# HAB-004 Affiliate RC21 – Kompakte Produktkacheln auf Kategorieebene
**Datum:** 12.11.2026 · **Version:** 0.1.18-rc21 · **Stand:** Offline-PASS, WordPress-Liveabnahme offen

## Anlass / nachgewiesene Ursache

Nutzer-Screenshot auf `hab-und-bewahr.de/einbruch-und-diebstahl/einbruch-und-diebstahl-haus-und-wohnung/c22-haustuerschloesser-dd9773fd40/`: Unter „Empfehlungen“ stehen drei große, textbasierte Amazon-Produktblöcke **untereinander**.

**Echte ZIP- und Source-Prüfung (HAB-001 RC19 und HAB-004 RC20):**
- Das Hab-Design `includes/detail-categories.php` gibt `hbdp_area_product_markup($node)` im unveränderten bestehenden Abschnitt `.hbdp-detail-products-feed` aus.
- Das Affiliate-Bridge `PPAR_HB_Integration::area()` erzeugt drei geprüfte echte Produkt-Slots `category_product_1`, `_2`, `_3` und fügte sie bislang **direkt hintereinander ohne Grid-Wrapper** zusammen.
- Die alten produktbezogenen Inline-Stile erzwingen teilweise Mindesthöhen **416/360/152 px**, auch wenn ein rechtlich erlaubtes echtes Produktfoto nicht vorliegt.
- Daraus folgen die übergroßen, untereinander angeordneten Karten. Kein manuelles WordPress-Redigieren erforderlich.

**Geprüfte Pferde-Atelier-Referenz:** Branch `affiliate-release-current`, Source `release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php` und `assets/frontend.css`: Kategorie-Slots `category_product_[123]`, echtes responsives Raster mit **3 Spalten ab 901px**, **2 Spalten 621–900px**, **1 Spalte bis 620px**. Echte Providerbuttons nur für nachweislich identische Produktkennung. Die Pferdeatelier-Quelle wurde ausschließlich gelesen, nicht kopiert oder verändert.

## Umsetzung – bestehendes HAB-004, kein Umbau

- **Bridge**: Der unveränderte bestehende Kategorieprodukt-Filter wird um **einen** `ppar-hb-category-products-grid`-Container erweitert; die drei ausgewählten originalen Affiliate-Slots werden unverändert hineingegeben. Gilt für WP-Endkategorien und passende fachliche R2/R3-Seiten. Nicht für R1-Welten, Artikel, Magazin, HivePress oder Banner-Slots.
- **CSS** in der bereits vorhandenen `assets/frontend.css`: 3/2/1-Spalten, kompakte weiße Karten mit dezentem Rand, gut lesbare vollständige Produktbezeichnung, kleine 150px-Originalbilder bei tatsächlicher Verfügbarkeit; responsive Anbieterbuttons. **„Anzeige“** einmal als Gruppenüberschrift; pro Karte doppelte Anzeige-Label visuell unterdrückt, bereits vorhandene andere Pflichtinformationen bleiben bestehen.
- **Renderhöhe** ausschließlich für die bestehenden `category_product_[123]`-Slots reduziert (keine künstlichen Bildbereiche ohne echte Bilder). Bestehende URL-, Tracking-, Provider- und Produktauswahl bleibt in ihrem einzigen zentralen Renderer.
- **Mehrere Anbieter je Produkt:** Der vorhandene Originalpfad `multiprovider_matching_offers_for_banner` + `multiprovider_render_offer_buttons` bleibt **unverändert**. Amazon, eBay, Idealo können nur bei belegtem **GTIN-Exaktmatch** zusammen in einer Karte erscheinen. Ein **ASIN allein** ist kein GTIN-Nachweis; es darf kein falsch zugeordnetes Idealo-Angebot dazu erfunden werden. Idealo erfordert zuvor eigenes aktives, gültiges Feedmaterial und entsprechende Ausgabefreigabe (bei `ebay_only` noch nicht öffentlich).
- **Keine falschen Produktdaten**: Der sichtbare Amazon-Test besitzt derzeit Titel, ASIN und Original-Anbieterlink, **kein freigegebenes Produktfoto, Preis oder verfügbare zusätzliche Provider-IDs**. Diese Daten werden nicht erfunden. Die Karten werden dennoch kompakt nebeneinander dargestellt.
- **HAB-001 Design RC19** (84,5 MB) bleibt bytegenau unverändert; keine Änderung der WordPress-Kategorien, Beiträge, Design-Templates, Versichertenthemen, Hauptseiten und anderen Portale.
- **Versicherungswelt:** RC19/RC20-Versicherungsausschluss bleibt enthalten; keine Amazon-/Idealo-Produktkarten in Versicherung. Das allgemeine Produktkarten-Raster aktiviert keine zusätzlichen Versicherungs-Produkt-Slots.
- **Keine neue Tabelle, kein zweites Plugin, keine neuen HTTP-Aufrufe im Frontend.**

## Release / Prüfstand

HAB-004: `CURRENT.zip` und benannter Release `HAB_AFFILIATE_RC21_0.1.18-rc21.zip` im offiziellen `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/`.

**Vollständiges ZIP:** 2.337.596 Bytes, 36 Dateien, SHA256 `0f40eddb4526434c03acdd370d2763ac5a01eaea862a40cb9ae25bb8754363bf`.

Nur **vier** Dateien in der vollständigen ZIP im Vergleich zu RC20 verändert: `affiliate-portal-router.php` (Inline-Kartenhöhe/Version), `includes/class-ppar-hab-bewahr-bridge.php` (Grid bei Kategorie), `assets/frontend.css` (scoped responsive Grid) und `readme.txt` (Version). Alle anderen Plugin-Dateien bleiben bytegenau wie RC20.

**GitHub-Actions Run 43244276656 PASS:** tatsächlicher HAB-Design-Filter (aus Original-RC19-ZIP) → tatsächlicher HAB-Affiliate-Bridge-Code → drei unveränderte Produkt-URLs und 3 Kacheln; 11 unabhängige Funktions- und Negativtests (auch bestehende Banner-/World-/Editorial-/Buchungs-/Leerstandswege unverändert), responsive 3/2/1-CSS, **alle 25 PHP-Dateien syntaxfrei**, **36/36** Affiliate-ZIP-CRC, **432/432** Design-ZIP-CRC, Original-Multiprovider-Pfad vorhanden. Testquellen `AFFILIATE/IMPLEMENTIERUNG_RC21_CATEGORY_CARDS/{build_rc21.py,qa_rc21.py}`.

**NICHT behaupten:** Dass RC21 schon in WordPress installiert, live visuell abgenommen oder Idealo-Fotos/Amazon-Idealo-Doppelbuttons bereits tatsächlich verfügbar sind. Diese Punkte bleiben nach Installationsfreigabe zu kontrollieren.

## Nächste Schritte

1. Vollständige RC21-ZIP in Hab-&-Bewahr-WordPress über das vorhandene Plugin aktualisieren; kein zweites Plugin installieren.
2. Auf der genannten **Haustürschlösser-Kategorie** in Desktop/Tablet/Smartphone prüfen: drei kompakte Kacheln nebeneinander auf Desktop, Titel/je vorhandener Anbieterlink, keine falschen Bilder; die andere Bannerwerbung bleibt bestehen.
3. Danach IDEALO-Produktfeed importieren und im separaten Hab-Affiliate-Arbeitsschritt Produkt- und Anbieterzuordnung (GTIN/ASIN) weiter prüfen; erst dann zusätzliche Idealo-Schaltflächen live erwarten.
4. Live-PASS nur nach tatsächlicher Sicht- und Klickprüfung protokollieren.
