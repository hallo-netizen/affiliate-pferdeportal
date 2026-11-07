# Abschluss der bisherigen Prüfung: RC11 seit 07.11.2026 im Pluginbüro als CURRENT; Tests bestanden. Die folgende Prüfung dokumentiert den **vorherigen RC10-Ausgangszustand**. Die RC11-Liveabnahme in WordPress ist weiterhin offen.

---

# HAB-004 – Verbindlicher Dreifachabgleich vor jeder Änderung an der Affiliate-Ausgabe
**Datum:** 07.11.2026. **Status:** LESENDE CODEPRÜFUNG, KEIN PLUGIN-BUILD, KEINE Änderung an HAB-001/002/003/004 und keinen Fremdprojekten.

## Anlass – echter Betreiber-Frontend-Readback
1. WordPress-Seite 169 „Leckwarnung & Absperrung“: Im Abschnitt „Empfehlungen“ erscheinen drei echte von DataForSEO gespeicherte Amazon-ASIN-Links in EINER textbasierten Anzeige; darunter weiterer Suchlink. Das beweist, dass die Recherche und Grundausgabe laufen, nicht aber die gewünschte Produktdarstellung.
2. WordPress-Kategorie 210 „Wassermelder“: Design zeigt „Empfehlungen“, darunter im Administrator-Modus „Nur Admin · vorhandener Produktslot; noch keine fachlich passenden Affiliate-Produkte geliefert.“ Die Seite ist keine Shop-/Produktseite; es sind WP-Seiten und WP-Kategorien.

## Wirklicher Codeabgleich
### Pferdeatelier: vorhandene funktionale Grundlage
Quellstand in GitHub, Branch `affiliate-release-current`, `release/affiliate-zentrale/current/affiliate-portal-router/pferdeportal-affiliate-router.php` gelesen (nicht verändert). Funktionen `render_affiliate_slot_for_context`, `render_banner` und `category_product_shared_rank_base` vorhanden. Vorhandene Produktplätze `category_product_1..3` verwenden bestehende Kampagnenauswahl/-prüfung und gegebenenfalls Multianbieter-Ausgabe. Dieses Prinzip nicht durch zweite Textkarten-Engine ersetzen. Der genannte Pferdeatelier-Releasezweig ist kein Live-Erfolgsnachweis; die Quelldateien sind nachweisbar.

### Hobbydepot: übernommener Weg und Bannerregeln
Aktuelle HD009-Quelle laut offizieller Plugin-Akte `HOBBYRAUSCH/PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/MANIFEST.md` und `HOBBYRAUSCH/AFFILIATE/CURRENT_STATE.md`: 0.1.18-dev, alte Pferdeatelier-Kampagnenauswahl/-Slots beibehalten; Amazon-Eigenbanner im bestehenden HD003-Platz, korrektes Format und genau ein Anzeigenlabel. Bestehende Kategorie-/Elternpfad- und Freigabelogik bleibt. Die vollständige Hobby-ZIP ist in GitHub nachgewiesen, aber in dieser Prüfung nicht entpackt und nicht zeilenweise verglichen; vor einer Codeübernahme MUSS die reale ZIP selbst diff-geprüft werden. Lokal getestete Hobby-0.1.18 ist kein bestätigter Live-Stand.

### Hab & Bewahr: beide Originalplugins tatsächlich geprüft
Aktuelles HAB-004 0.1.7-rc10 Voll-ZIP und HAB-001 Design 0.1.189 aus vorhandenen Archiven lokal gelesen. Kein Plugin geändert.

A) HAB-001 `includes/detail-categories.php`: `hbdp_render_detail_category_page($node)` ruft für JEDE Kategorie `hbdp_area_product_markup($node)` auf; dieser ruft in `includes/area-design-prototype.php` den EXISTIERENDEN Filter `hbdp_area_product_cards_html` mit dem **Kategorie-Knoten** auf.

B) HAB-004 `includes/class-ppar-hab-bewahr-bridge.php`: derselbe Filter ist auf `PPAR_HB_Integration::area_products` gelegt, aber `area()` hat `if (($node['type'] ?? '') !== 'page') return '';`. Er verwirft jeden Kategorie-Knoten. **Dies erklärt den leeren vorhandenen Produktslot auf der Wassermelder-Kategorie konkret und direkt.**

C) HAB-004 `affiliate-portal-router.php`: Die ursprünglichen Produkt- und Kampagnenfunktionen `render_affiliate_slot_for_context`, `render_banner`, `provide_leaf_category_affiliate_slot_html` sowie `category_product_1..3` sind bereits enthalten. Die Leaf-Kategoriefunktion ist im HAB-004-Quellstand auffindbar, aber dieser neue Design-Filterpfad ruft sie nicht auf.

D) HAB-004 `includes/trait-ppar-hb-amazon.php`: `hb_amazon_area_product_fallback` erzeugt am Seite3-Hub einzelne `hb_amazon_product_family_markup`-Blöcke mit mehreren ASIN-Links, verbunden durch ` · `. Auf dem Frontend entsteht eine Textanzeige statt der normalen vorhandenen Produktkarten. Dieser Fallback wird erst verwendet, wenn die ursprünglichen drei Kampagnenplätze leer sind. Er ist KEIN Ersatz für deren gemeinsame Kampagnenausgabe.

## Harte KISS-Regel für jede spätere Änderung – vorher / nachher
1. ZUERST jeweilige echte aktuelle **Pferdeatelier-Quelle** und **Hobbydepot-Pluginquelle** lesen; ihre Werbe-/Produkt-Slots, Provider-/Bild-/Freigaberegeln, echte Nutzung und geprüfte Grenzen dokumentieren.
2. DANACH im echten HAB-004-Quellstand und im tatsächlichen HAB-001-Design nach identischen bereits implementierten Funktionen suchen. Keine Vermutung auf Basis von Plugin-Namen.
3. Bestehende Kanäle an den tatsächlichen Hab-Knoten (WP-**Seiten**, **Kategorien**, später **Beiträge**) korrekt anbinden. **Keine neue Engine, Datenbank, Zweitplugin, eigene Werbeplätze oder neue Planungsarchitektur**.
4. Kein „ein Fix nach dem anderen“. Immer EINE geschlossene Ende-zu-Ende-Simulation mit realem HAB-001/HAB-004-Hook-Weg: gültige Kategorie → gespeicherte DataForSEO-ASIN → bestehender Kategorieprodukt-Slot → tatsächliches HTML → eindeutige Anzeige/korrekte Amazon-Tracking-ID. Derselbe Test für R3-Seite, Beiträge, gebuchte Kampagnen mit Vorrang sowie keine Daten.
5. Tests müssen den vorigen sichtbaren Fehler reproduzieren (Kategorieknoten verworfen + ASIN-Links als lange Textzeile) und das korrigierte Verhalten belegen, einschließlich Negativ-/Grenzfällen; nur anschließend eine Installations-ZIP für HAB-004 erstellen und an echte Live-Prüfung anschließen. Keine anderen Projekte verändern.
6. Keine Fake-Bilder, Preise, Bewertungen oder Amazon-Produktdaten: DataForSEO-ASIN/Titel reichen **nicht** für echte Produktfotos/Preise. Wenn das Bild aus einer genehmigten lokalen Bildquelle stammt, Werbemittel und Produktangebot nicht irreführend vermischen. Hobbydepot-Eigenbanner sind nicht automatisch Hab-Banner.

## Nächste Handlung (kein Build durchgeführt)
Vollständige HD009-Source-ZIP vor Änderung selbst diff-prüfen. Danach NUR den vorhandenen Hab-Kategorie-Filter korrekt mit der bereits vorhandenen Produktausgabe verbinden und den alten nichtstandardmäßigen Fallback vermeiden, soweit bestehende Anzeigen-/Provider-Priorität nicht verletzt wird. Ende-zu-Ende-Tests mit dem aktuellen HAB-001-Design sind Freigabegate. Neue Amazon-Kostenaufträge sind für den bekannten 3-ASIN-Test nicht notwendig.

**Wichtige Grenze:** Keiner dieser Offline-Quellabgleiche ist ein Beweis, dass Pferdeatelier/Hobbydepot im Moment produktiv dieselbe Version haben. Screenshot/Live-Readback ist nur von Hab & Bewahr belegt.
