# Hab & Bewahr – HAB-004 RC14, Kategorie- und Beitragsbanner – 08.11.2026

**WICHTIG ZUM STAND**: vollständige Installations-ZIP `Hab-und-Bewahr-Affiliate-RC14-Kategorien-und-Beitraege.zip` ist **im Chat als erzeugter Dateianhang verfügbar**, Version `0.1.11-rc14`, 2.092.433 Bytes, SHA256 `b524b5fbd06b15bbe8425c0d7da2b5c28b2eb2b1896dee9a7e8fd84443e8a7e4`. WordPress-Pluginordner `affiliate-portal-router/` unverändert. **Nicht behaupten, dass RC14 im GitHub-`CURRENT.zip` liegt**: GitHub-HAB-004/CURRENT ist weiterhin RC11; RC14 benötigt WordPress-Liveabnahme. RC13 ist vollständig in RC14 enthalten; keine separat zu installierende Zwischenversion.

## Vorher hart geprüft (KISS)
- Echte unveränderte **Hobbydepot-HD009 0.1.25**-Original-ZIP auf Prüfsumme `c82b75f9f485eec43f6b8626ff4a6748f3610c0093e61616d4bdd8d4d62204d0` geprüft und Quellcode der `hdar_ci_amazon_banner`-Weltbild-Vererbung, der Originalgrafik `hdar-amazon-available-at-amazon-de-official.png` und des 6:1-/4,2:1-/1:1-CSS untersucht.
- Echte originale HAB-001 Design-ZIP und ihre 333 bereits vorhandenen WebP-Motive; Bilder auf Motiv und Bild-Identitätsmapping geprüft. **Kein Hero-Duplikat**: `scene-flood.webp` als Duplikat von `hero-wasser-feuchtigkeit.webp` ausgeschlossen, stattdessen eigenständiges `focus-keller-rueckstau.webp`.
- Im Hab Affiliate RC13 sind die regulären Kampagnenprioritäten, Kategoriebaum, Parent-Pfade, Newsletter-/eBay-/Idealo-Produktengine, Glossar-Filter `hbdp_glossary_ad_markup`, Artikel-Filter `hbdp_article_auto_banner_html`, Seitenleiste und Amazon-House-Fallback bereits vorhanden; lediglich vorhandene Bildbindung/Formate/Artikel-Fallback zu Ende verbunden. Keine neue DB, Plugininstanz, Cron, externe Foto-API oder kostenpflichtige neue Suche.
- Die 28 RC13-Originaldateien erhalten; **nur vier** vorhandene Dateien bearbeitet: `affiliate-portal-router.php`, `includes/trait-ppar-hb-amazon.php`, `assets/frontend.css`, `readme.txt`. **Sieben** Assetdateien hinzugefügt (sechs WebP-Bilder aus HAB-001 und exakt die originale erlaubte Amazon-Button-Grafik aus HD009). Gesamt 35 ZIP-Dateien, Plugin-Einstiegsordner unverändert. Alle anderen Web-/Plugin-/Datenquellen unverändert.

## Bild pro Schutzwelt, alle Unterkategorien erben
Ausschließlich aktiver `apkw_target_tree_active_snapshot_v1` Kategoriebaum und explizite Parent-Pfade. Nur ein korrektes Motiv je Hauptwelt (NICHT je hundert Endkategorien). Titel und Amazon-Suche stammen weiterhin aus dem **konkreten** Ziel, nur die Motivdatei aus dem Elternbereich.
- **Einbruch & Diebstahl**: `scene-security.webp` (Eingang/Sicherheit) → `hb-amazon-world-einbruch.webp`.
- **Vandalismus & Zerstörung**: `scene-graffiti.webp` (beschädigte Fassade) → `hb-amazon-world-vandalismus.webp`.
- **Wasser & Feuchtigkeit**: `focus-keller-rueckstau.webp` (Keller/Rückstau) → `hb-amazon-world-wasser.webp`.
- **Feuer & Gase**: `area-brandschutz-loeschmittel.webp` (Feuerlöscher) → `hb-amazon-world-feuer.webp`.
- **Wetter & Naturgefahren**: `scene-weather.webp` (Haus/Unwetter) → `hb-amazon-world-wetter.webp`.
- **Technik & Ausfälle**: `scene-tech.webp` (Haustechnik) → `hb-amazon-world-technik.webp`.
- **Versicherungen**: kein automatischer Amazon-Banner. Keine entsprechende sachlich passende physische Amazon-Produktkategorie; bestehende echte Kampagnen bleiben nutzbar. Amazon-Literatur o.ä. nicht als Versicherung vorspiegeln.

## Original-Button und HTML
- Amazon-Originalgrafik `Erhältlich bei Amazon` **einmal** im einzigen **orangenen** Button + Pfeil, keine zweite Textzeile `Bei Amazon entdecken`, kein Portal-Logo, keine Werbefloskel/Eyebrow.
- Nur eine vorhandene Anzeige-Kennzeichnung auf dem Designrahmen, keine zusätzlichen verschachtelten Rahmen. Querformat 6:1 Desktop, 4,2:1 mobil. Quadrat 1:1 für native Glossar-/Beitrags-Sidebar. Smartphone und Desktop geprüft.
- Gebuchte Banner haben stets Vorrang: Standard `render_affiliate_slot_for_context` entscheidet vor `hb_amazon_category_search_fallback`; World-Banner wird nur bei freiem, thematisch geprüftem Slot erzeugt. Weiterhin `habundbewahr-21`, `rel=sponsored nofollow noopener noreferrer`, global AUS, Amazon AUS, fehlender echter World-Parent => leer. Keine erfundenen Produktfotos, Preise oder Empfehlungen.

## Beitragsebene
- **Native HAB-001-Artikelseitenleiste**, gleicher Quadratbanner wie bei Glossar; vorhandener Slot `hbdp_article_auto_banner_html` → `hab_bw_article_slot($post_id,'banner')` → `post_inline_banner`.
- Echte `wp_get_post_categories` an aktivem Baum geprüft. Bei mehreren Kategorien muss eine eindeutige Hauptwelt vorliegen. Bei mehreren Kategorien einer Welt gewinnt ausschließlich die tiefste eindeutige; sonst leer, statt willkürliches Bild/Keyword. Amazon-Suche verwendet **Kategoriebezeichnung**, nicht geratenen Titel/Produkt. Gebuchte Artikelkampagne gewinnt, keine Einbettung in `the_content`.
- Auch wenn neuer Artikel noch keinen aktuellen Hybridplan hat, wird der **vorhandene** leere Standard-Bannerslot geprüft; unveränderte Artikelproduktslots bleiben unberührt.

## QA
- Echte Quell- und Bilddateien 6 Welten geprüft (WebP-Maße >=1400x700).
- 63 eigenständige PHP-Tests am echten RC14-House-Renderer: sechs Welten, Hauptwelt/Kategorie/Unterkategorie, WordPress-Beitrag, Glossar, eindeutige Eltern, fehlende Zuordnung, Mehrwelt-Konflikt, falsche Reihenfolge, Amazon an/aus und Tracking sowie CSS-Formate.
- Alle 25 PHP-Dateien: `php -l` PASS. Vollständige 35-Dateien-ZIP: CRC PASS, 28 Originalpfade erhalten. Nur vier Altdateien verändert, sieben freigegebene Assets ergänzt.
- Browser Chromium 1250px und 390px (echte Bilder, Original-Button, echte HTML-/CSS-Renderer): 4/4 Bilder geladen, kein horizontaler Überlauf, 1100x183px Querbanner und 300x300px Quadrat Desktop, 338x120px Querbanner und 300x300px Quadrat Mobil, nur ein Label.
- **Noch keine echte WordPress-Abnahme**, nicht behaupten, dass Website/Server aktualisiert sind. Einzelprodukte bleiben weiterhin ohne Amazon-Einzelproduktfotos bis zu eBay-/Idealo- oder anderer zulässiger Bildquelle. Kein neuer bezahlter DataForSEO-Auftrag.

## Nächster Schritt
1. Benutzer installiert **nur vollständige RC14** als Update des vorhandenen HAB-004 Affiliate-Plugins (kein RC12/RC13 als Zwischenschritt).
2. Prüft Wassermelder-Kategorie (Water-World-Motiv), Einbruch-Kategorie (anderes Motiv), Glossar-Einzelseite mit freigegebenem Target und veröffentlichten Beitrag mit eindeutig zugeordneter Kategorie; Desktop/Mobil und Amazon-Kategoriesuche.
3. Meldet echte Screenshots; dann nur nach nachgewiesenen Ursachen nachbessern. Anschließend RC14-ZIP als GitHub-`CURRENT.zip` synchronisieren; dieses Dokument behauptet nicht, dass dies bereits geschehen sei.
