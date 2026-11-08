# HOBBY DEPOT – PLUGINBÜRO – AKTUELLER BESTAND

**08.11.2026 – HD003 1.50.806 ist der aktuelle geprüfte Stand für das Hobbydepot-Beitragslayout.** Letzter Fehler bei 1.50.805: doppelte Hero-Fotografie im Artikeltext, bildloser Amazon-Suchbanner im Artikel, weitere Drachenfotografie in der rechten Kategorie-Kachel. **Ursache:** Alte CSS/JS-Deduplizierung zielte auf `.entry-content` statt ListingHive-`.post__text`; Amazon-Standardkachel ohne Bild lief durch; Bild der rechten Karte war fest auf Sportdrachen codiert. **Fix:** Gleiche Foto-URL im regulären Beitrag serverseitig aus dem Lesetext entfernen, generischen `post_inline_banner` auf Beitragsseiten unterdrücken, rechte Spalte nur mit echten internen Textlinks ohne Foto ausgeben. Alte falsch zielende JS/CSS-Workarounds entfernt. Hab-inspirierte Zweispalten-/Schriftvorlage vorerst nur am gekennzeichneten Design-Testpost; andere Beiträge bleiben in ihrer bisherigen Layoutform. ZIP `HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip` und `CURRENT.zip` byteidentisch, SHA-256 `665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358`. ZIP 1290/1290, PHP 13/13 und Funktionstests + reale HTML-Browsersimulation fünf Bildschirmbreiten PASS (Action 42489458324). **Produktivinstallation/Sicht-PASS weiter offen.** HD009 0.1.28 bleibt eigenes Affiliate-Plugin, HD006 bleibt **Bildzentrale** und unverändert.



**08.11.2026 – HD003 1.50.805 ist die aktuelle Design-Testversion.** Vorherige 1.50.804 hatte die großen Schriften und Hab-&-Bewahr-Zweispaltenansicht nur im Zweileiner-/Vierleiner-Design-Test korrigiert, **aber die drei alten, statischen, bildlosen Produktkacheln und eine redundante Verweiskachel übersehen**. Das ist jetzt behoben: ungeprüfte Produktbeispielkacheln und provisorischer Partnerbanner des Testartikels werden nicht mehr öffentlich ausgegeben, stattdessen erscheint eine echte, bildgestützte „Mehr zum Thema“-Kategorieverlinkung im Sidebar-Stil. Foto: eigenes existierendes Sportdrachen-Kategoriefoto, nicht als vermeintliches Produktbild. Produktbild-Automatik/DataForSEO bleibt separat in HD009 offen. Einzige gültige HD003-ZIP `HOBBY_DEPOT_DESIGN_HD003_1.50.805.zip` und byteidentisches `CURRENT.zip`, SHA-256 `e90b7e220fca7226b75da8ec7adabb80407e18576350744b1dd37346b37c7a72`. PHP 13/13, ZIP 1290/1290 und tatsächlicher PHP-Ausgabetest/Browser bei 1440/960/768/390/360px PASS. **WP-Installation und echte Sichtabnahme offen. Andere Beiträge und Seiten unverändert.**



**08.11.2026 – HAB-&-BEWAHR-BEITRAGSDESIGN INS HOBBYDEPOT ÜBERTRAGEN, TESTSTUFE.** Das neue HD003 **1.50.804** (Download `HOBBY_DEPOT_DESIGN_HD003_1.50.804.zip`, SHA-256 `ea85bde0f9bc48d679112df2dac5a6b9d53f63379f9a4633979b7be126b04a52`) verändert absichtlich ausschließlich den bestehenden Zweileiner/Vierleiner-**Design-Testbeitrag**: Hab-Leseraster übersetzt auf Hobbydepot-Farben/Montserrat, kleinere H1/H2/H3, Einleitung 36→18px Desktop bzw. 17px Mobil, rechts nur reale Kategorie-/Artikelverweise, mobil eine Spalte. „Fachartikel“ und unnötige fünfteilige Inhaltsliste verschwinden, „Auf einen Blick“ sowie Hero erhalten. Für normale Beiträge läuft weiterhin das vorherige Design – erst nach Test-PASS ausrollen. Affiliate-Produktboxen bis zu geprüftem DataForSEO-/Amazon-Produktbetrieb nicht vortäuschen. **Technische Tests PHP 13/13, ZIP 1290/1290, realer Browser sechs Breiten PASS; echte Installation offen.** HD009 0.1.28 und HD007 1.2.21 bleiben unverändert.



**Neuer gültiger Stand 08.11.2026: HD009 0.1.28** (`HOBBY_DEPOT_AFFILIATE_HD009_0.1.28.zip`, SHA-256 `ad4685633516cde1f22af21a2d8ecc92965bab658f7a9411f287c58f85bb39cd`). Die zuvor bei `/bewegen/wind-drachen/` und anderen übergeordneten Seiten auftretende fachfremde Bildauswahl wurde durch den gemeinsamen bestehenden HD003-Kategoriebaum für 8 Welt-, 69 Gruppen-, 381 Hobby- und 3.376 unterste Kategorieziele ersetzt. „Wind & Drachen“ erhält ein anderes vorhandenes Lenkdrachenbild statt Outdoorausrüstung; richtige Welt-/Gruppenbilder auf allen Ebenen. ZIP CRC, PHP und Browser-Tests vier Breiten bestanden. **Liveinstallation und Abnahme offen.** HD003 1.50.803 (Vorschaubilder ohne Featured Image) und HD007 1.2.21 unverändert. Ältere HD009-Versionen in folgenden Abschnitten sind historisch.



**Aktuell am 08.11.2026: gemeinsamer Bildfix HD009 0.1.27 + HD003 1.50.803.** HD009 nutzt auf echten WordPress-Kategoriearchiven die vorhandene 3.376er-Leaf-Zuordnung aus HD003, selbst wenn WordPress keine Elternkategorie setzt. Der Banner zeigt das thematisch passende genehmigte Foto der Hobbygruppe; Sportdrachen → Wind-&-Drachen-Foto statt bildlosem bzw. fachfremdem Banner. Als Rückfall bleiben die acht Weltbilder. HD003 zeigt in seinen drei vorhandenen Beitragskachel-Varianten bei fehlendem Beitragsbild ein passendes, vorhandenes Hobbyfoto; vorhandene Beitragsbilder haben Vorrang. Sportdrachen-Vorschaubild: separates Delta-Drachen-Foto. **Keine neuen Bilder generiert, keine neuen Bannerplätze, keine Änderung an Partner-/Produktlogik.** Beide vollständigen ZIPs gebaut, ZIP/PHP 24+13 PASS, echte PHP-Funktionstests PASS, Zuordnung 3.376/3.376 PASS, Browser-Simulation bei 1440/900/390/360 PASS. Die beiden neuen ZIPs sind gültige Downloads; **Installation und echte Sichtabnahme noch offen**. Bisherige Angaben zu 0.1.26 bzw. 1.50.798 darunter historisch.



**Aktueller Stand 08.11.2026: HD009 Affiliate-Zentrale 0.1.26**, Download `HOBBY_DEPOT_AFFILIATE_HD009_0.1.26.zip`, 1.553.271 Bytes, SHA-256 `a627e35a9e8d20f34616c1ead4bc1b7d180e40a8f74abb985c7311b60dcfcd8f`. Einzige Abweichung von 0.1.25: zu großer Abstand **oberhalb des im Hobbyregister-Text eingebauten Querbanners** auf Desktop und Mobil korrigiert (47→17 bzw. 57→11px gerundet). Acht Themenfotos, Kategoriebanner-Höhe, Amazon-Button und alle Ausspielregeln unverändert. Voll-ZIP 41/41, PHP 24/24 und Browser-Test zwei Registerprofile / vier Breiten PASS (Action 42461816837). Live-Installation und optische Abnahme 0.1.26 offen; Beitragsbannerdesign später separat entscheiden. Frühere HD009-Stände unten sind historisch.



**Zwischenstand 08.11.2026 – Nutzerfreigabe erster Eindruck:** HD009 **0.1.25** („auf den ersten Blick pass“) und HD007 **1.2.21** sind weiterhin die einzigen gültigen Downloadstände in ihren getrennten Plugin-Büros. Beide Installations-ZIPs und die jeweiligen CURRENT.zip-Dateien sind unverändert und byteidentisch; keine zusätzliche Pluginversion erzeugt. **Erledigt:** 8 neutrale Hobbywelt-Fotos (Tiere: Terraristik), eigene Kategoriebannerbilder statt Hero-Wiederholung, flaches Kategorie-Format, bebilderte Hobbyregisterbanner, Claim ohne Schlusspunkt. **Offen:** Beitragsbanner-Design ausdrücklich separat festlegen; Sichtprüfung der Ausspielung auf weiteren Seiten und Mobilgeräten, keine pauschale Abnahme aller Seiten. Die HTML-Ausspielungsregeln für Beiträge in HD009 bleiben bislang unverändert; die Designentscheidung dafür ist noch nicht abgeschlossen.


**Aktuell 07.11.2026: HD009 Affiliate-Zentrale Version 0.1.25** (Download `HOBBY_DEPOT_AFFILIATE_HD009_0.1.25.zip`, Größe 1.553.090 Bytes, SHA-256 `c82b75f9f485eec43f6b8626ff4a6748f3610c0093e61616d4bdd8d4d62204d0`). Auf allen Kategorieebenen verwenden eigene Amazon-Kreativs acht feste, textfreie Weltbilder statt des Seiten-Heros; „Tiere“ zeigt Terraristik/Insektenumfeld statt Haustiere. Desktop-Kategorie-Werbebanner 6:1, mobil 4,2:1; Original-Amazon-Button, Verlauf, Titel und vorhandene Ausspielplätze bleiben unverändert. Hobbyregister-Quadrat hat wieder echte Bildquelle (bei Bedarf das HD007-Herobild mit anderem Zuschnitt). Eigene Beiträge und Produkt-/Kampagnenlogik unverändert. Voll-ZIP CRC, PHP 24/24, fünf Original-PHP-Fälle, reale Frontend-Simulationen bei 1440/960/390/360 alle bestanden; Live-Installation/Abnahme noch offen. Angaben zu früheren HD009-Versionen darunter historisch.



**Aktueller Stand 07.11.2026: HD009 Affiliate-Zentrale 0.1.24** (Download `HOBBY_DEPOT_AFFILIATE_HD009_0.1.24.zip`, SHA-256 `e1bc7cc4d7ab69bc711c424c3d1a612c4710f66155eba7a401552329a800f3a6`). Belegte Bannerplätze auf Kategorieebenen, im Hobbyregister und auf regulären Artikeln bekommen bei fehlendem genehmigtem Fotomotiv einen Bild-freien, thematischen Amazon-Suchbanner. Für Registerprofile bleibt nur **ein** Affiliate-Foto im Querbanner; Quadrat als gestalteter Themenbanner ohne Bildwiederholung. Bestehende Partner-/Produktzuordnung unverändert. Tests PHP 24/24, CRC, sechs Funktionsfälle und Browser 4 Layouts/4 Breiten PASS; produktive Installation und Vollabnahme noch offen. Ältere HD009-Standangaben unten sind Historie.



**Aktueller Downloadstand 07.11.2026: HD009 Affiliate-Zentrale 0.1.22 (`HOBBY_DEPOT_AFFILIATE_HD009_0.1.22.zip`) und HD007 Hobbyregister 1.2.20 (`HOBBY_DEPOT_HOBBYREGISTER_HD007_1.2.20.zip`).** Beide vollwertigen Installations-ZIPs liegen zusätzlich byteidentisch als jeweilige `CURRENT.zip` im zugehörigen Büro. 0.1.21 und 1.2.18 sowie alle weiteren früheren Versionen in älteren Abschnitten sind **historisch**. PHP/ZIP-Prüfung bestanden, echte WordPress-Live-Versionen nicht authentifiziert ausgelesen.



**Aktuelle Hauptstände am 07.11.2026 (einzige CURRENT-ZIPs):** HD009 Affiliate-Zentrale **0.1.21-dev** (1.067.588 Bytes, SHA-256 `f6dd1cb301dbe661b63a9dd6b7890d0363c3317f025ee8617a94348b6001a002`) und HD007 Hobbyregister Core **1.2.18** (14.834.693 Bytes, SHA-256 `1908ff82d348993bb5012fad9357e67a4580170fa40d9710fc03084f26d64935`). Beide vollständig im isolierten Plugin-Büro abgelegt. HD009: neue Hero-Verläufe für Quadrat/Quer, dynamische Titellänge. HD007: kurze mobile Startseiten-Hero-Beschreibung. Beide technisch und im isolierten Browser geprüft. **Liveinstallation beider neuen Versionen offen.**

**Historische Erläuterungen darunter (0.1.20 / 1.2.17 und älter) sind nicht mehr die Download-Wahrheit.**

**Hinweis:** Alle weiteren 0.1.10–0.1.19-Vermerke weiter unten sind Historie und nicht der aktuelle Download.

**Aktualisierung 07.11.2026 – HD009 (einzige CURRENT-Version):** `ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip` = **0.1.20-dev**, 1.066.589 Bytes, SHA-256 `cd6cb75f3ef0f393f94f3f93b974f3663ffa1f449c579886ae9520bc3d920cbb`, Git-Blob `9d9ac298c9e32bfc54f81d80e39f1a3560200d8c`. Die existierende Pferdeatelier-/Hobby-Automatik bleibt erhalten; Variante-4-Banner wie abgenommen. **Neu:** Desktop-Registeranzeige nach `Auf einen Blick` vor `Hobbygruppe`, ein Querbanner im Haupttext nach `Kosten und Ausrüstung`, mobil Quadratbanner nach Haupttext als erster Seitenleistenblock. **WordPress-/Browser-E2E in 0.1.19 PASS, Positionen vom Betreiber live bestätigt; 0.1.20 CSS-Update ZIP/24 PHP PASS, Liveprüfung noch offen.** Fachliche Statusautorität `../AFFILIATE/CURRENT_STATE.md`, technische `PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/CURRENT.md`. Alle weiteren alten HD009-Einträge sind Historie.

Stand: 07.11.2026 (HD-009 aktualisiert; die übrigen Pluginstände behalten ihre zuletzt dokumentierten Prüfdaten). **Nur selbst entwickelte Hobby-Depot-Plugins und eigene Projektwerkzeuge. Keine Fremdplugins.**

Die technische Einzelwahrheit liegt weiterhin ausschließlich in der jeweiligen Plugin-Akte unter `PLUGIN_AKTEN/<Plugin-ID>/CURRENT.md`. Die WordPress-Pluginliste ist ein älterer Betreiberstand vom 01.11.2026; aktuelle Serverdateien wurden nicht selbst ausgelesen.

## Eigene Plugins / Projektwerkzeuge – laut letzter WordPress-Liste aktiv

| Eigenplugin | Belegter Versionsstand | Stand der ORIGINAL-Sicherung im Pluginbüro |
|---|---|---|
| HD-001 – Kategorie-Workflow | 1.14.17 (WordPress-Liste) | Aktuelle Voll-ZIP noch nicht im Büro; ältere 1.14.16 in der Projektkonversation vorhanden |
| HD-003 – Design / Template Kit | 1.50.798, vom Betreiber im Frontend abgenommen | **Voll-ZIP gesichert, unabhängig geöffnet** |
| HD-004 – Kategorie-Kern | 1.0.0 | **Original-Voll-ZIP gesichert, unabhängig geprüft** |
| HD-005 – Glossar Core | 1.0.25 | Aktuelle Voll-ZIP noch nicht im Büro |
| HD-006 – Bildzentrale | 2.7.8 | Aktuelle Voll-ZIP noch nicht im Büro |
| HD-007 – Hobbyregister Core | 1.2.16 in WordPress-Liste, 1.2.17 als neuer Stand freigegeben | **Voll-ZIP 1.2.17 gesichert, unabhängig geöffnet; Serverstand nicht separat geprüft** |
| HD-009 – Affiliate-Zentrale | **0.1.19-dev GitHub CURRENT.zip**, isolierter WordPress-E2E bestanden, Live-Update offen | **Einzige Voll-ZIP 1.066.241 Bytes, Prüfberichte in technischer HD009-Akte** |
| Footer-Umzug – Portale | 1.1.1 | **Original-Voll-ZIP im Pluginbüro gesichert und unabhängig wieder geöffnet** |
| Hobby Depot – FAQ Frontend Fix | 1.0.2 | **Original-Voll-ZIP gesichert, unabhängig geprüft** |
| Hobby Depot – Performance Diagnose | 1.1.0 | Aktuelle Voll-ZIP noch nicht im Büro |

Zusätzlich existieren eigenentwickelte, **nicht als aktiv belegte Kandidaten**: HD-002 Text/SEO, HD-008 SEO-Metadaten und HD-008 Anzeigenfüller. Ihre bestehenden Akten bleiben erhalten; die doppelte Kennung HD-008 wird ohne gesicherte Zuordnung nicht geändert.

## Was jetzt tatsächlich gesichert ist

- **HD-003 / 1.50.798:** vollständiges Original-Paket `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip`, unabhängig überprüft.
- **HD-007 / 1.2.17:** vollständiges Original-Paket `ISOLIERTE_PLUGINS/HD-007-HOBBYREGISTER-CORE/CURRENT.zip`, unabhängig überprüft.
- **HD-004 / 1.0.0:** exakte aktuelle Original-ZIP, 3.736 Bytes, vollständiger Bytevergleich erfolgreich.
- **FAQ Frontend Fix / 1.0.2:** exakte aktuelle Original-ZIP, 6.193 Bytes, vollständiger Bytevergleich erfolgreich.
- **HD-009 / 0.1.10-dev:** aus tatsächlicher 0.1.7-Serverquelle aktualisiert; 26-Dateien-ZIP auf GitHub physisch gesichert, 607784 Bytes, SHA-256 `e8613f742a0c3a9e93b3c335b82b6594e95d61c89fd70f5a33981c73871427f4`, Readback PASS. Das Original bleibt als Nachweis der bisherigen WordPress-Installation 0.1.7 erhalten. Fachliche Statusautorität ausschließlich `../AFFILIATE/CURRENT_STATE.md`.
- **Neu gefunden:** vollständige früher ausgelieferte Originalpakete HD-001 1.14.17 (529.810 Bytes) und HD-006 Bildzentrale 2.7.8 (66.404 Bytes) lokal bytegenau geprüft. Sie sind noch nicht als neue GitHub-ZIP abgelegt, dürfen also nicht als dort gesichert bezeichnet werden.
- **Weitere ältere Downloads nachgewiesen:** HD-009 0.1.7-dev (Original nun vom Betreiber als WordPress-ZIP verfügbar), Performance-Diagnose 1.1.0 und Design-Such-Bundle mit Glossar 1.0.25. Der frühere Fehlzugriff auf die HD-009-Library-Datei ist für die neue GitHub-Update-ZIP nicht mehr relevant.

**Ausschließlich aktuelle Eigenplugin-Versionen im aktiven Pluginbüro:** Die fünf Fremdplugin-Pakete und die veraltete HD-009 0.1.2-dev-CURRENT.zip samt Manifest sind entfernt. Die Entfernung betrifft ausschließlich GitHub. Weder auf WordPress noch an installierten Fremdplugins wurde etwas geändert. Eine historische Git-Versionsspur bleibt erhalten.

## Einziger nächster Schritt

**Die bereits gefundenen Original-ZIPs der zuletzt bestätigten eigenen Pluginversionen aus den vorhandenen Downloads unverändert in den Campus übertragen; ausschließlich nach Originalhash-/Versions- und ZIP-Prüfung als CURRENT führen.** Fehlende Rohdaten nicht aus älteren Versionen rekonstruieren.


## HD-009 – aktueller Nachtrag 07.11.2026

**Fertig als GitHub-Installationsdatei:** `ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip` Version **0.1.10-dev**; ZIP-Größe 607784 Bytes; SHA-256 `e8613f742a0c3a9e93b3c335b82b6594e95d61c89fd70f5a33981c73871427f4`; GitHub-Blob `8b6732f2b3ec88e390662021ec7e0760da8f6fba`. Das tatsächliche 0.1.7-Original aus WordPress und der jüngere Pferdeatelier-Ursachenpatch 6.72.308 wurden geprüft; passende allgemeine eBay-/Amazon-Hobby-Korrekturen sind integriert.

**Echte Paketdatei:** [CURRENT.zip](ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip). [Manifest](ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/MANIFEST.md). [Prüfnachweis](PLUGIN_AKTEN/HD-009-AFFILIATE-ZENTRALE/EVIDENCE/HD009_0.1.10_HARMONISIERUNG_20261107.md).

**Bürovertrag:** Nur ein fachliches Affiliate-Büro `../AFFILIATE/`, genau ein aktuelles HD009-Plugin im bestehenden technischen Pluginbüro. WordPress-Upgrade und echte Provider-Liveabnahme wurden noch nicht durchgeführt. Alte 0.1.2/0.1.9-Protokolle sind Historie, keine zweite Current-ZIP.
