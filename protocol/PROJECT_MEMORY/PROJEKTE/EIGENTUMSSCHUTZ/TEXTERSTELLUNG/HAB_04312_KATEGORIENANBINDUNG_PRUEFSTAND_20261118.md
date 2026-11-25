# Hab & Bewahr – Texterstellung 0.4.31.2 – vorhandene Kategorien zugeordnet

**Stand 18.11.2026. Nur vorhandene Original-Kategorienanbindung korrigiert; kein Umbau oder Neubau.**

## Tatsächlich geändert
- Basis: die vorhandene minimale Hab-Kopie 0.4.31.1 aus dem Original-Pferdeatelier-Plugin 0.4.31. Vorherige Universal-Neuarchitektur 0.5.x wurde NICHT verwendet.
- Die bestehende PSTE_Portal_Category_Map liest bei der leeren Hab-Karte jetzt die schon vorhandenen, nur lesbaren WordPress-Term-/Seitenbindungen des Hab-Kategorie-Workflow-Plugins: _apkw_target_node_id, _apkw_parent_concept_id, _apkw_target_active, _apkw_target_pillar. R1 > R2 > R3 > tatsächliche Fachkategorie bleibt unverändert. Nicht gebundene verwaltete Kategorien führen zu einer Fehlermeldung. Redaktions- und inaktive Kategorien werden nicht in die Fachrecherche aufgenommen. Keine WP-Writes.
- Die bestehende PSTE_Article_Type_Registry bietet einer einzigen realen Fachkategorie die 10 bereits im Original vorhandenen Recherchesuchabsichten an, statt pro Suchabsicht eine künstliche WP-Kategorie zu erzeugen. Dadurch bleibt beispielsweise 'Türen & Fenster' für Beratung, FAQ, Kosten, Pflege und Vergleich dieselbe WP-Kategorie. Der echte K0-Schreibartikeltyp wird wie bisher einmalig und unabhängig im MINI festgelegt.
- Der restliche Original-Rechercheablauf, WordPress-Auftragsregal, MINI, K0 und Entwurfsimport wurden NICHT geändert.

## Dateien und Testbelege
- Exakt 4 von 87 bestehenden Paketdateien geändert: original/pste/includes/class-pste-portal-category-map.php, original/pste/includes/class-pste-article-type-registry.php, texterstellung.php (Versionsangabe), README-TESTINSTALLATION.txt.
- Keine neue oder gelöschte Programmdatei, 83 von 87 Dateien bytegleich zur Hab-0.4.31.1-Kopie.
- 78/78 PHP-Lint, 8/8 JSON, ZIP-CRC PASS (87/87 Einträge).
- Original-WP-Metadaten-Vertrag nachgewiesen im Hab-Kategorie-Workflow; die 285 Kategorie-Namen im bisherigen Original-Readback sind eindeutig.
- WP-Mock: Zwei vorhandene Hab-Termnamen und WP-IDs im selben tatsächlichen R3 zugeordnet, ohne doppelte Quarantäne; Beratung, FAQ, Kosten, Pflege und Vergleich bleiben für dieselbe WP-Kategorie erreichbar; alle 10 Original-Suchabsichten verfügbar.
- WP-Mock: inaktive Kategorie ignoriert, fehlender R3-Besitzer blockiert; 285 synthetische Kategorien unter 93 synthetischen R3-Seiten vollständig erhalten (0 Quarantäne). Wichtig: Mengentest war synthetisch, kein realer Live-WP-Readback.
- Bestehender Original-MINI-Worker separat 7/7 getestet, einschließlich Anleitung und Negativfällen. Kein K0-Quellcode geändert.

## Download-Datei und tatsächlich gespeicherte Büroablage
- Dateiname: Texterstellung_HAB_UND_BEWAHR_0.4.31.2_KATEGORIEN_ZUORDNUNG.zip
- SHA256: 15706a29140b86ceaa4ae88baf3944bb7b1f58e3f0092dc6c71dd48e89d28919
- Lokal WordPress-installationsfähiges Paket; alle verifizierten internen ZIP-, PHP- und strukturellen Tests PASS.
- Tatsächlich im Hab-Library-Büro gespeichert: /hab-und-bewahr/TEXTERSTELLUNG/PLUGIN_FREIGABEKANDIDATEN/04312/ mit Plugin-ZIP, ARBEITSPROTOKOLL_04312.md, QA_04312.json, Bauskript und ausführbaren Regressionstests.

## Echte Prüfgrenze, nicht als abgeschlossen behaupten
- Kein direkter WordPress-Livezugriff aus dieser Sitzung, daher tatsächliches Erkennen der derzeit aktiven Hab-Kategorien noch auf der WP-Testseite zu bestätigen.
- Noch kein kostenpflichtiger DataForSEO-Echtlauf für diese Version und keine bestätigte externe K0-Portalregistrierung. Original-WordPress-Import bleibt auf Entwurf begrenzt.
- Nächster Bedienweg: Hab-WordPress vorzugsweise Staging -> Plugins -> Plugin hinzufügen -> ZIP hochladen -> bestehendes Plugin ersetzen; Texterstellung -> Recherche aufrufen und zunächst erkannte Kategorien prüfen, bevor eine bezahlte Recherche ausgelöst wird.
- Original-Pferdeatelier, Universal-Blanko, K0, übrige Kategorienplugins und WordPress-Livebestand NICHT verändert.