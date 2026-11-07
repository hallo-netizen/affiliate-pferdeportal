# HAB-004 RC7 – gezielter Originalvergleich und Regression (07.11.2026)

**Basis**: HAB-004 RC6 (WordPress-Original-ZIP 618152 Bytes, Git-Blob c9026cbcfaa44a03a69820d9d35207f8b6ce5c27). **Neu**: HAB-004 RC7 (WordPress-Original-ZIP 616209 Bytes, ZIP-SHA256 08725e5cf9d18654345b4b18b9f3c63ade54ce7a6da932d9768bc2b9867b1d6e, Git-Blob 3df1bd941aa051f6706a66fd857a8745d0209420). Im GitHub-Releasezweig binär-blobgleich verifiziert.

**Harte Ursachenprüfung vor jeder Änderung**:
- `save_post_post → handle_article_plan_post_save` existiert bereits und berechnet Artikelwerbepläne bei Änderungen anhand Titel, Inhalt und Kategorien neu.
- `PPAR_HB_Design_Contract::article_products` gibt den vorhandenen Artikel-Produktslot an `hab_bw_article_slot` weiter; bestehende Anzeigen haben Vorrang.
- `hb_amazon_dfs_candidate` sucht bisher nur vorhandene eBay/idealo-Produktkampagnen; `hb_amazon_category_candidate` nur echte Hab-Produktkategorien. Beitragsbezogene DataForSEO-Themensuche war in RC6 nicht vorhanden.
- Es gibt einen vorhandenen Admin-Startknopf, denselben stündlichen WP-Cron, denselben DataForSEO-Worker, eine bestehende Statusoption und eine Budgetgrenze von fünf neuen kostenpflichtigen Aufträgen pro UTC-Tag. **Kein zweiter Worker oder zusätzlicher WP-Cron erforderlich.**

**Minimaler Eingriff**: exakt 3/28 alte Dateien geändert: WordPress-Hauptdatei (geprüfte Artikel-Slot-Fallback-Anbindung + Version), vorhandenes `includes/trait-ppar-hb-amazon.php` (Artikelthema, nachlaufende Beitragskandidaten, Resultatprüfung, 7-Tage-Recherche-Abstand, 14-Tage-Ergebnisfrische und reine Textlinkausgabe) und `readme.txt` (Version). **25/28 Dateien byteidentisch**; Design, Bannerengine, Artikelplanmodul, Quellenarchitektur, Datenbanktabellen und andere Portale nicht geändert.

**Konkretes Verhalten**:
- Nur veröffentlichte, werbefreigegebene WordPress-Beiträge mit **direkt zugewiesener, realer Hab-Produktkategorie**; im Titel muss die konkrete Produktfamilie ausdrücklich vorkommen. Allgemeine Ratgeber, Entwürfe, falsche Kategorie, werbefreie oder dringliche Beiträge werden nicht gesondert recherchiert.
- Automatische Prüfung durch denselben Cron, **keine kostenpflichtige Suche beim Beitragsspeichern**. Bei neuer/änderter Artikelüberschrift oder Kategorie wird der Themen-Fingerabdruck neu berechnet; alte Artikelangebote erscheinen bei Änderung sofort nicht mehr.
- Product-Werbeplatz: wenn eine valide eigene Produktkampagne existiert, bleibt sie erhalten. Sonst nur ein klar als „Anzeige“ markierter Amazon-Suchlink mit `habundbewahr-21`; bei hinreichend bestätigtem DataForSEO-Ergebnis bis drei geprüfte textuelle Amazon-Direktlinks. Keine fremden Bilder/Preise/Verfügbarkeitsbehauptungen.
- Kein Überspringen der globalen Affiliate-Sperre, der bestehenden Planaktualität, der individuellen Werbesperre oder der Tageskostengrenze.
- Neue Beiträge erscheinen später automatisch in den Kandidaten, ohne manuelle einzelne Amazon-Kampagnen.

**Lokal ausgeführte Tests gegen unveränderte ZIP-Quellen und echten Artikel-Slot**:
- 25/25 PHP-Syntaxprüfungen PASS, ZIP-CRC und 28-Dateien-Verzeichnisstruktur PASS.
- `test_hab_amazon.php`: 23 Prüfassertions PASS.
- `test_hab_rc5.php`: 16 Prüfassertions PASS.
- `test_hab_rc6.php`: 23 Prüfassertions PASS.
- `test_hab_rc7.php`: 34 Prüfassertions PASS. Darin: Veröffentlichung/Entwurf, richtige/falsche Kategorie, Werbesperre, Themenwechsel, veraltete Treffer, Varianten, eigene Tracking-ID, POST/GET mit täglicher Kostenbegrenzung, automatische Erkennung neuer Beiträge; zusätzlich echter `hab_bw_article_slot` aus WordPress-Hauptdatei dynamisch geladen und mit altem Anbieter-Vorrang, Hybrid/Legacy-Modus und Global-Sperre getestet.
- 96 PASS-Assertions insgesamt, **keine Behauptung 96 unabhängiger End-to-End-Fälle**.

**Offen, nicht als PASS behauptet**: keine echten WordPress-Beiträge im Portal, keine echte neue DataForSEO-Suche, kein bezahlter API-Auftrag in diesem Test, kein authentifizierter Frontend- oder WordPress-LIVE-End-to-End-Test. RC7 ist ein lokal getesteter Upgrade-Kandidat, bis er auf Hab & Bewahr installiert und an einem später realen Fachbeitrag geprüft ist.

**Einzige operative nächste Aktion:** Bereits vorhandenes HAB-004 auf Hab & Bewahr mit RC7 aktualisieren, Amazon/DataForSEO-Konfiguration erhalten, dann erst auf echtem WordPress den Status und später die Ausgabe eines realen passenden Beitrags prüfen. Keine neuen Plugins, keine zweite Suche, keine neue Architektur.
