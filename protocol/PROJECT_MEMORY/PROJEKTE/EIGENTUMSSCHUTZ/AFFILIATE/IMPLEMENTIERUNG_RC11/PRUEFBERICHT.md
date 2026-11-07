# HAB-004 RC11 – abgeschlossene Ursachenprüfung und gesicherte Installations-ZIP

- Version 0.1.8-rc11, 624020 Bytes, SHA-256 `cf8cf7946aa7605dadecda1f041cfc6fb150c7971f7c9feb9dbb6dd1ac8eabda`.
- Verifiziertes Ausgangs-ZIP RC10: SHA-256 `f3b6b0ac4fd05310fa32ce68e2715b29d022003ac68f32ceb051443832364ced`.
- Keine neuen Plugins, Hooks, Datenbanken, Imports, Worker oder bezahlten Provider-Aufträge. Nur bestehendes HAB-004.
- Vollständige aktuellen Original-ZIPs von Pferdeatelier, Hobbydepot HD009 0.1.19, HAB-004 RC10 und HAB-001-Design vor Korrektur untersucht.
- Verbindlich festgestellte Ursache: HAB-001 filtert mit Kategorie-Knoten, HAB-004s `area()` akzeptierte nur `page`; RC10 R3-Amazon-Fallback verkettete ASINs mit ` · `.
- In RC11: bestehender `provide_leaf_category_affiliate_slot_html` leitet die verifizierte WP-Term-ID zu `render_affiliate_slot_for_context` weiter; bestehende Kampagnenvorwahl unverändert. Nur bei leerer Werbekampagne zeigen drei originale Produktplätze je EINEN verifizierten Amazon-Treffer über den bisherigen `render_banner`.
- R3: bisherige `hb_amazon_area_product_fallback` befüllt bis zu drei vorhandene `category_product_[1-3]`-Plätze mit jeweils einem einzelnen tatsächlich gespeicherten ASIN-Titel/Trackinglink, keine gekoppelten Textzeilen. Fehlende ASIN: kein Produktkartenersatz.
- Baseline mit tatsächlichem RC10-Code und HAB-001-Hook reproduziert: Wassermelder leer, R3-Treffer als Textzeile.
- RC11 in vollständigem ursprünglichem Plugin/HAB-001-Design-Filterlauf geprüft: zwei getrennte `data-ppar-category-product-card`-Karten auf Kategorie und R3, echte gespeicherte ASINs, `habundbewahr-21`, keine gefälschten Bilder/Preise.
- Vorrang einer eingebuchten Anzeige, zentrale Abschaltung, fremde unbekannte Kategorie, keine ASIN und kostenfreies Rendern: PASS.
- Bestehende RC10-Szenarien (inklusive Cron/Provider/Beitragsfreigabe) und die RC5-/RC6-/RC7-/Amazon-Regressionsskripte: **18 getrennte PHP-Prozesse PASS**; **34 PHP-Syntaxprüfungen PASS**; **28/28 ZIP-Dateien CRC PASS**.
- ÄNDERUNGEN: `includes/class-ppar-hab-bewahr-bridge.php` (Kategorie anschließen), `includes/trait-ppar-hb-amazon.php` (ASIN-Karten über Originalrenderer), `affiliate-portal-router.php` und `readme.txt` (nur Versionsnummer). Übrige 24 Plugindateien bytegleich.
- RELEASE: nur `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` aktualisiert; alle vier aktuellen Plugin-Akten konsistent aktualisiert. Ursprüngliches ZIP in der Git-Historie.
- Sicherer offener Livepunkt: WordPress-Pluginupdate und öffentliche Sichtprüfung; kein echter IONOS-WordPress-/DataForSEO-Livetest und keine serverseitige Cron-Reparatur behauptet. **Kein neuer DataForSEO-POST für die bereits gespeicherten Produktdaten nötig.**
