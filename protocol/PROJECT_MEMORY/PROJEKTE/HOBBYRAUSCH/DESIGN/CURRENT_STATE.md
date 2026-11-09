# Hobbydepot DESIGN – Ergänzung 09.11.2026

**Designplugin HD003 1.50.809 ist aktueller geprüfter Installationskandidat.** Mobile Kategorieeinleitungen und Ausklapptexte auf 14 px vereinheitlicht; geprüft an Typen Hub2, Leaf, Sonderfall Schuhmacherei und Kettenhemd-FAQ, Desktop unverändert. Echte Live-Kategorie-Vorprüfung hatte 15 px sichtbar vs. 14 px ausgeklappt bestätigt. Neue mobile Playwright-Simulation bestanden; Live-Installation 1.50.809 noch nicht nachgewiesen.

Hobbyfinder-Resultatfotos: ursprüngliche Bildzuordnung und Bildausgabe unverändert, mobil nicht per CSS versteckt; Testfoto im 360/390/620/760-px-Rendering sichtbar. Keine Live-Resultatprüfung möglich: bekannte Hobbyfinder-URLs geben zur Prüfzeit 404. Kein generisches Fremdbild, keine Änderung am Register. Siehe Pluginakte `PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`.

---

# HOBBYRAUSCH – DESIGN – CURRENT_STATE

**Sichtabnahme des Nutzers, 08.11.2026:** HD003 **1.50.806** für das Hobbydepot-Beitragsdesign **„erst einmal okay, bis auf Kleinigkeiten“**. Dies ist eine **vorläufige Freigabe des erreichten Testartikel-Designs**, keine Detail-Vollabnahme und insbesondere **keine Freigabe einer produktiven Amazon-Artikelbox**. Gesicherter aktueller Vollinstaller `HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip` plus byteidentisches `CURRENT.zip` (Git-Blob `e3496adbc4524da0c6375d198d9010e2cc30d9f4`, SHA-256 `665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358`). Nichts am Plugin geändert, **keine Versionsänderung**. Ein Hero, kein wiederholtes Hero-Foto, kein bildloser Amazon-Suchbanner im Artikel, keine zweite Bildkachel rechts. Hab-&-Bewahr-inspirierter Lesestil bleibt zunächst **nur auf dem markierten Testartikel**; Detailkleinigkeiten bleiben offen, aber keine neue Designrunde ohne Anlass. **Nächster Arbeitsbereich ist die echte Amazon-Produktbox auf Artikelebene in der HD009 Affiliate-Zentrale**, einschließlich DataForSEO-Recherche, Freigabe, korrekter Zuordnung und erlaubtem Produktbild. HD003, HD006 (Bildzentrale), HD007 und die bestehende HD009 0.1.28 bleiben durch diese Dokumentation unangetastet.



**08.11.2026 – HD003 1.50.806 ist der aktuelle geprüfte Stand für das Hobbydepot-Beitragslayout.** Letzter Fehler bei 1.50.805: doppelte Hero-Fotografie im Artikeltext, bildloser Amazon-Suchbanner im Artikel, weitere Drachenfotografie in der rechten Kategorie-Kachel. **Ursache:** Alte CSS/JS-Deduplizierung zielte auf `.entry-content` statt ListingHive-`.post__text`; Amazon-Standardkachel ohne Bild lief durch; Bild der rechten Karte war fest auf Sportdrachen codiert. **Fix:** Gleiche Foto-URL im regulären Beitrag serverseitig aus dem Lesetext entfernen, generischen `post_inline_banner` auf Beitragsseiten unterdrücken, rechte Spalte nur mit echten internen Textlinks ohne Foto ausgeben. Alte falsch zielende JS/CSS-Workarounds entfernt. Hab-inspirierte Zweispalten-/Schriftvorlage vorerst nur am gekennzeichneten Design-Testpost; andere Beiträge bleiben in ihrer bisherigen Layoutform. ZIP `HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip` und `CURRENT.zip` byteidentisch, SHA-256 `665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358`. ZIP 1290/1290, PHP 13/13 und Funktionstests + reale HTML-Browsersimulation fünf Bildschirmbreiten PASS (Action 42489458324). **Produktivinstallation/Sicht-PASS weiter offen.** HD009 0.1.28 bleibt eigenes Affiliate-Plugin, HD006 bleibt **Bildzentrale** und unverändert.



**08.11.2026 – HD003 1.50.805 ist die aktuelle Design-Testversion.** Vorherige 1.50.804 hatte die großen Schriften und Hab-&-Bewahr-Zweispaltenansicht nur im Zweileiner-/Vierleiner-Design-Test korrigiert, **aber die drei alten, statischen, bildlosen Produktkacheln und eine redundante Verweiskachel übersehen**. Das ist jetzt behoben: ungeprüfte Produktbeispielkacheln und provisorischer Partnerbanner des Testartikels werden nicht mehr öffentlich ausgegeben, stattdessen erscheint eine echte, bildgestützte „Mehr zum Thema“-Kategorieverlinkung im Sidebar-Stil. Foto: eigenes existierendes Sportdrachen-Kategoriefoto, nicht als vermeintliches Produktbild. Produktbild-Automatik/DataForSEO bleibt separat in HD009 offen. Einzige gültige HD003-ZIP `HOBBY_DEPOT_DESIGN_HD003_1.50.805.zip` und byteidentisches `CURRENT.zip`, SHA-256 `e90b7e220fca7226b75da8ec7adabb80407e18576350744b1dd37346b37c7a72`. PHP 13/13, ZIP 1290/1290 und tatsächlicher PHP-Ausgabetest/Browser bei 1440/960/768/390/360px PASS. **WP-Installation und echte Sichtabnahme offen. Andere Beiträge und Seiten unverändert.**



**08.11.2026 – HAB-&-BEWAHR-BEITRAGSDESIGN INS HOBBYDEPOT ÜBERTRAGEN, TESTSTUFE.** Das neue HD003 **1.50.804** (Download `HOBBY_DEPOT_DESIGN_HD003_1.50.804.zip`, SHA-256 `ea85bde0f9bc48d679112df2dac5a6b9d53f63379f9a4633979b7be126b04a52`) verändert absichtlich ausschließlich den bestehenden Zweileiner/Vierleiner-**Design-Testbeitrag**: Hab-Leseraster übersetzt auf Hobbydepot-Farben/Montserrat, kleinere H1/H2/H3, Einleitung 36→18px Desktop bzw. 17px Mobil, rechts nur reale Kategorie-/Artikelverweise, mobil eine Spalte. „Fachartikel“ und unnötige fünfteilige Inhaltsliste verschwinden, „Auf einen Blick“ sowie Hero erhalten. Für normale Beiträge läuft weiterhin das vorherige Design – erst nach Test-PASS ausrollen. Affiliate-Produktboxen bis zu geprüftem DataForSEO-/Amazon-Produktbetrieb nicht vortäuschen. **Technische Tests PHP 13/13, ZIP 1290/1290, realer Browser sechs Breiten PASS; echte Installation offen.** HD009 0.1.28 und HD007 1.2.21 bleiben unverändert.



Stand: 02.11.2026. Dies ist die einzelne Fach-Current-Autorität für das Portaldesign. Der genaue Pluginstand und seine ZIP-Abrufwege stehen ausschließlich unter ../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md.

## Belastbarer Stand

- Globaler Header und Footer sind laut aktueller Betreiberprüfung bereits in Ordnung; nicht verändern.
- Anzeigenmarkt-Startseite nutzt das freigegebene Hobby-Depot-Design.
- Seit dem am 02.11. geprüften Designupdate erhalten die echten HivePress-Anzeigenkategorien auf allen Ebenen die vorhandene Anzeigenmarkt-Darstellung; Seitenleiste entfällt, Kategorien/Anzeigen/Filter bleiben bei HivePress. Der Betreiber hat das neue Erscheinungsbild mit „passt“ bestätigt.
- Die WordPress-Funktion wurde nicht durch neue Anzeigenlogik ersetzt; keine weiteren Kategorien wurden angelegt oder gelöscht.
- Design-Außenachse 1.200 px, Header/Footer-Achse 1.440 px beibehalten.
- Weitere Arbeiten am einzelnen Beitrags-Hero sind **nicht** durch das Anzeigenmarkt-PASS freigegeben. Früherer, bereits erarbeiteter Anspruch: Artikelüberschrift oberhalb des Bilds, Motiv rechts, Claim links als HTML-Text, kein Text ins Bild eingebrannt, ein Bild je Thema, keine Collage.
- Vollständige aktuelle Plugin-ZIP und Tests sowie Rollback siehe alleinige HD-003-CURRENT.md. Ein eigener authentifizierter Server-Bytevergleich ist noch nicht erfolgt.

## Nicht verändern

Keine Seitenstruktur, SEO, Bildzentrale, Hobbyregister, WordPress-Inhalte oder fremde Projekte allein durch diese Abschlussprüfung verändern. Keine zweite Design-Architektur und keine zusätzlichen Plugins.

## Erster offener Punkt / genau eine NEXT ACTION

Die tatsächlich auf WordPress laufende HD-003-Dateiversion unabhängig read-only mit dem aktuellen vollständigen GitHub-Paket abgleichen; bis dahin nur den vom Betreiber beobachteten Frontend-PASS, nicht einen vollständigen Live-Code-PASS behaupten.

Historische Zwischenstände und Detailabnahmen bleiben im Git-Verlauf dieser Datei und im vorhandenen PLUGINS/UPDATEPROTOKOLL.md nachvollziehbar.
