# Hab & Bewahr – Verbindlicher Design-/Textstandard Ebene 2 (36 Bereiche)
Stand: 18.10.2026 · Fassung 0.1.37

## Verbindlich für jede Ebene-2-Seite
- Gilt für **alle 36 Bereichsseiten** in sechs Welten: Einbruch 6, Vandalismus 5, Wasser 5, Feuer/Gase 5, Wetter/Natur 8, Technik/Ausfälle 7.
- **H1 und individuell formulierter kurzer Schutzsatz** als getrennte HTML-Texte im Hero; kein Bildtext, kein standardisierter Kategorietext.
- **Hero in Inhaltsbreite** (kein Full-Bleed), Breadcrumbs unmittelbar davor. **Identische Bilddatei** wie in der verlinkenden Bereichskachel der Elternwelt, berechnet aus genau derselben aktuellen Bildallokation – keine parallele Hero-Auswahl.
- Unterkategorien als **scharfe rechteckige (ca. 1,7:1) Fotokacheln**, echte Seitenziele aus aktivem zentralem Snapshot, keine erfundenen Links, kein zusammenhangloses Nahmotiv und keine visuell identischen Fotos innerhalb derselben Kachelgruppe. Abweichende Dateinamen zählen **nicht** als verschiedene Bilder, wenn die Bilddaten gleich sind.
- Oben Schutzthemen, danach thematisch passende Produkte/Anzeigen, bebilderte Ratgeber und optional echter Magazinverweis; darunter ausführlicher Fachtext.
- Produktanzeige, automatische Affiliate-Banner und unabhängig vermietbare Werbefläche sind getrennte Ausgabebereiche. Ohne verfügbare reale Inhalte bleiben diese im **öffentlichen Frontend unsichtbar**, während Admins einen eindeutig markierten Layoutplatz sehen. Bestehende Provider können Produkt-HTML über den Filter `hbdp_area_product_cards_html` und Banner-HTML über `hbdp_area_auto_banner_html` bereitstellen; **der Release enthält noch keinen Affiliate-Provider**. Vermietbare 36 Bereichsplätze im bestehenden WordPress-Menü **Werkzeuge → Hab & Bewahr Design**, ohne neue Tabelle.
- Nur **echte veröffentlichte Beiträge** öffentlich anzeigen; niemals Dummy-Beiträge veröffentlichen. Als Administrator ohne passende Posts vier rein visuelle Demoartikel je Seite mit Bild, Titel und klarem Demo-Status.
- Fachtext unten: **mindestens vier gegliederte Abschnitte** mit spezifischer Risikobeurteilung, Auswahlberatung, Praxis-/Wartungshinweisen und richtigem Verhalten bei Schaden; zudem mind. drei **echte interne Kindlinks**, 1–2 klare thematische Fotografien und eine kurze Checkliste. Keine Keyword-Füller; keine identischen Einleitungen/Claims über Seiten hinweg. Redaktionelle Tatsachen und Rechtsfragen vor Publikation fachlich und örtlich prüfen.
- Manuelle gesonderte Ebene-2-Bottom-Textvorgabe via `_hbdp_area_bottom_text` gewinnt, falls vorhanden; sonst datengestützter individueller Text.
- Alt-Leiste „Magazin / Dienstleister“/Trennlinie nicht ausgeben. Der reguläre echte Magazinverweis ist zulässig.

## Abgrenzung
**Bestehendes Designplugin** WordPress-Core unangetastet, kein neues CMS, kein neues Kategorie-Plugin, keine Kategorie- oder Post-Writes, keine Frontend-Netzwerkanfragen und keine neuen DB-Tabellen. Bestehende Hero- und Redaktion von Ebene 1 und spezifische Darstellung von Ebene 3 unverändert. Die fünf C2.2-Nachzügler müssen bei Liveprüfung hinsichtlich ihrer tatsächlichen display_names und Subtopics am autoritativen Snapshot abgeglichen werden; **keine Live-WP-Prüfung behaupten**.

## Realisierter Release
0.1.37 aus 0.1.36: 36 individuell verfasste Claims/Intros/4-Abschnittstexte in `data/area-editorial-v1.json`, strukturierte thematische Fotozuordnung inkl. Erkennung gleicher Bildmotive in `data/area-photo-identities.json`, 20 neue komprimierte und scharfe Szene-WebP-Dateien, aktualisierter Shared Renderer `includes/area-design-prototype.php`, CSS nur Ebene 2 und minimale Dispatcher-/Asset-Hooks. Die fünf späteren Bereichsseiten werden namensbezogen innerhalb ihrer exakten Elternwelt erkannt, nicht anhand erfundener Live-IDs.
- 36/36 PHP-Ausgabeseiten in kontrollierter WordPress-Mocksimulation positiv und als Gast/Admin geprüft; je Seite 36 verschiedene Claims, 4 Abschnitte und >=3 echte Links, 4 verschiedene Demoartikel-Fotos für Admin, keine Gäste-Demos.
- 48 Chromium-Browseransichten (36 × 980px, sechs davon zusätzlich bei 390px und 1440px) PASS: Fotos laden bei >=900px Quellbreite, keine Kachel-Doppelmotive nach visuellem dHash, Kacheln rechteckig, kein seitlicher Überlauf, Breadcrumbs über innerhalb des Bodys liegendem Hero.
- 9/9 PHP-Lint PASS und ZIP-Integrität PASS. **Live-WordPress-Abnahme ausstehend**.
- Download-Library: `/Eigentumsschutz/Design/HAB_UND_BEWAHR_DESIGN_0.1.37_EBENE_2_ALLE_36.zip`; ZIP SHA256 `608b262c8b1d825172377bb1357f9160914d8fed8a92c6d1f4294ad2abc0af1b`.

## NEXT ACTION
**Bestehendes Designplugin normal auf 0.1.37 aktualisieren** und aus jedem der sechs Bereiche zuerst eine tatsächliche WordPress-Liveseite öffnen; fünf neue C2.2-Seiten auf korrekte thematische Bildzuordnung/Labels überprüfen. Auffälligkeiten konkreter Seiten lokal reproduzieren und anschließend gezielt korrigieren. Keine Kategorie-Importaktion.
