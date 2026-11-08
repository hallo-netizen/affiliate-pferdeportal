# HOBBY DEPOT – AFFILIATE – EINZIGE AKTUELLE FACH-AUTORITÄT

**Verbindliche Übergabe 08.11.2026:** Die separat gesicherte aktuelle Plugin-/Amazon-DataForSEO-Übergabeakte ist `PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/UEBERGABE_AMAZON_DATAFORSEO_0.1.31_20261108.md`. HD009 **0.1.31** bleibt unverändert CURRENT; volle ZIP und `CURRENT.zip` wurden als byteidentisch geprüft. Kein neues Installerpaket nötig. Noch offen: zulässige Amazon-Produktbilder, eBay-/Idealo-Provider-Vorrang, WordPress-Livetest. Kostenpflichtige Auto-Recherche weiterhin standardmäßig **AUS**.



**08.11.2026 – HD009 0.1.31: DataForSEO-Automatik nach tatsächlichem Hab-RC11-Quellabgleich.** Das alte Hobbydepot-HD009 0.1.29 war nur manuelle bezahlte `products/live/advanced`-Suche + einzelner ASIN-Freigabe. **Neu** im selben Plugin: standardmäßig ausgeschaltener, ausdrücklich kostenpflichtig freizugebender Worker; zunächst kostenfreier Kandidatencheck im vorhandenen Amazon-Backend; sichere `task_post`-Anlage/gesonderter `task_get/advanced`-Abruf, fünf neue automatische Anfragen pro UTC-Tag, kein Doppelaufruf, automatische Abschaltung bei Fehlern. HD007 862 Registereinträge + HD003 381 aktive Hobbys ergeben 235 vorsichtige Keyword-Kandidaten; reale Artikel-Zuordnung nur nach Kategorie-/Titelbeleg. Ergebnisse nur echte Amazon.de-ASIN/Titel, max. drei je Artikel, in bestehendem Produktspeicher, keine Drittbilder/Preise. **Keine vollautomatischen Amazon-Fotos – Produktkacheln ohne zulässiges Bild weiterhin absichtlich unsichtbar.** Offizielle Amazon-Produktbildanbindung und eBay-/Idealo-Provider-Vorrang bleiben offen. Voll-ZIP `HOBBY_DEPOT_AFFILIATE_HD009_0.1.31.zip` = `CURRENT.zip`, SHA-256 `3b3d65bd534a249c6ac645a20eac3da9aae68c7e82e52ad7e121639399b46e87`, 41/41 ZIP, 24/24 PHP, kostenfreie reale PHP-Fixturetests PASS (GitHub Action 42496624037). **Keine echte DataForSEO-API-Suche/Kosten, keine Live-Installation/Abnahme behauptet.** Isolierter nicht bestandener 0.1.30-Testzweig wurde nicht kopiert. HD003 1.50.806 und HD006 Bildzentrale unverändert.



**08.11.2026 – HD009 Affiliate-Zentrale 0.1.29 ist der neue geprüfte Pluginstand für Amazon-Artikelproduktkarten.** Erhält dieselbe Daten-/ASIN-Freigabe und exakte WordPress-Zuordnung wie 0.1.28, ermöglicht im vorhandenen Backend das Zuordnen eines eigenen/lizenzierten WordPress-Produktbilds, und zeigt auf Beiträgen nur bei erfülltem Bildrechte-Nachweis echte Amazon-Werbekarten. Im bestehenden Hab-inspirierten Beitragslayout in der rechten Spalte, mobil darunter, ohne Design-/Hero-Modifikation. Fehlt ein Bild, keine leere oder textlose Fake-Karte; vorhandene Provider-Produktbereiche haben Vorrang. Full ZIP `HOBBY_DEPOT_AFFILIATE_HD009_0.1.29.zip` mit byteidentischem `CURRENT.zip`; 1.557.483 Bytes, SHA-256 `56aa1338e27bf0582a24e82f20184bccca782555028d9104efee96d0d2059dce`. PHP 24/24, ZIP 41/41, Funktions- und Browsertests fünf Breiten PASS (Action 42492560262). **DataForSEO automatische Recherche und offizieller Amazon-Produktbildabruf weiterhin offen; keine bezahlte Anfrage ausgelöst.** Dieser Schritt ist die geprüfte Ausgabe-/Bildrechtevorstufe, nicht der fertige automatische 381-Hobby-Befüllungsworkflow. Nutzerabnahme der produktiven WordPress-Installation offen. HD003 1.50.806 bleibt unangetastet und vorläufig freigegeben.



**Sichtabnahme des Nutzers, 08.11.2026:** HD003 **1.50.806** für das Hobbydepot-Beitragsdesign **„erst einmal okay, bis auf Kleinigkeiten“**. Dies ist eine **vorläufige Freigabe des erreichten Testartikel-Designs**, keine Detail-Vollabnahme und insbesondere **keine Freigabe einer produktiven Amazon-Artikelbox**. Gesicherter aktueller Vollinstaller `HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip` plus byteidentisches `CURRENT.zip` (Git-Blob `e3496adbc4524da0c6375d198d9010e2cc30d9f4`, SHA-256 `665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358`). Nichts am Plugin geändert, **keine Versionsänderung**. Ein Hero, kein wiederholtes Hero-Foto, kein bildloser Amazon-Suchbanner im Artikel, keine zweite Bildkachel rechts. Hab-&-Bewahr-inspirierter Lesestil bleibt zunächst **nur auf dem markierten Testartikel**; Detailkleinigkeiten bleiben offen, aber keine neue Designrunde ohne Anlass. **Nächster Arbeitsbereich ist die echte Amazon-Produktbox auf Artikelebene in der HD009 Affiliate-Zentrale**, einschließlich DataForSEO-Recherche, Freigabe, korrekter Zuordnung und erlaubtem Produktbild. HD003, HD006 (Bildzentrale), HD007 und die bestehende HD009 0.1.28 bleiben durch diese Dokumentation unangetastet.



**08.11.2026 – HD003 1.50.806 ist der aktuelle geprüfte Stand für das Hobbydepot-Beitragslayout.** Letzter Fehler bei 1.50.805: doppelte Hero-Fotografie im Artikeltext, bildloser Amazon-Suchbanner im Artikel, weitere Drachenfotografie in der rechten Kategorie-Kachel. **Ursache:** Alte CSS/JS-Deduplizierung zielte auf `.entry-content` statt ListingHive-`.post__text`; Amazon-Standardkachel ohne Bild lief durch; Bild der rechten Karte war fest auf Sportdrachen codiert. **Fix:** Gleiche Foto-URL im regulären Beitrag serverseitig aus dem Lesetext entfernen, generischen `post_inline_banner` auf Beitragsseiten unterdrücken, rechte Spalte nur mit echten internen Textlinks ohne Foto ausgeben. Alte falsch zielende JS/CSS-Workarounds entfernt. Hab-inspirierte Zweispalten-/Schriftvorlage vorerst nur am gekennzeichneten Design-Testpost; andere Beiträge bleiben in ihrer bisherigen Layoutform. ZIP `HOBBY_DEPOT_DESIGN_HD003_1.50.806.zip` und `CURRENT.zip` byteidentisch, SHA-256 `665a71d705ae80891ca43d56aca851c006608fcfcb61185381e3f96033635358`. ZIP 1290/1290, PHP 13/13 und Funktionstests + reale HTML-Browsersimulation fünf Bildschirmbreiten PASS (Action 42489458324). **Produktivinstallation/Sicht-PASS weiter offen.** HD009 0.1.28 bleibt eigenes Affiliate-Plugin, HD006 bleibt **Bildzentrale** und unverändert.



**Amazon-/DataForSEO-Produktboxen – überprüfter Arbeitsstand 08.11.2026, NOCH OFFEN.** Aktuelles HD009 bleibt **0.1.28**, unverändert. Die Produktbefüllung wird nicht automatisch durchgeführt: Hobbydepot fragt kostenpflichtig nur auf manuellen Klick DataForSEO ab und muss die Produkt-ASIN anschließend pro WP-Ziel einzeln freigeben; gespeicherte Anzeigen erscheinen nur mit genau passendem Ziel und aktivem Launch/Tracking. Hab-&-Bewahr-HAB-004 (amtliches GitHub-CURRENT RC11) hat einen offline geprüften automatischen ASIN-Sucher mit Limit fünf neue Aufträge pro UTC-Tag, Wiederabfrage statt Doppelzahlung und echten Fehlermeldungen, aber **keine bestandene vollständige Produktbild-/Live-Abnahme**. Der Hab-Code ist nicht 1:1 auf die Hobby-Kategorien übertragbar. **Neue harte, kostenfreie Datenprüfung:** 381/381 aktive Hobbyziele sind exakt mit HD007-Registerdatensätzen verbunden; 246 vorsichtige erste Ausrüstungssuchwörter, 135 noch unklare Fälle; 10 positive/negative Produkt-ASIN-/Host-/Titelprüfungen erfolgreich. **Keine API-Kosten, keine Live-Daten, keine Pluginänderungen oder behauptete Produktbefüllung.** Voller Bericht: `DATAFORSEO_KOSTENFREIE_VORPRUEFUNG_20261108.md`. Nächstes Ziel: den vorhandenen HD009-Worker nach Hab-Muster erweitern (eine Engine, Kostenlimit, klare Fehlerrückmeldung, eindeutige Produktzuordnung). Produktfotos benötigen eine zulässige Amazon-Quelle (Creators API/PA API); DataForSEO-Fotos nicht einfach übernehmen. Eigene HD009-ZIPs, K0 und Hab-Plugins bleiben unangetastet.



**Neuer gültiger Stand 08.11.2026: HD009 0.1.28** (`HOBBY_DEPOT_AFFILIATE_HD009_0.1.28.zip`, SHA-256 `ad4685633516cde1f22af21a2d8ecc92965bab658f7a9411f287c58f85bb39cd`). Die zuvor bei `/bewegen/wind-drachen/` und anderen übergeordneten Seiten auftretende fachfremde Bildauswahl wurde durch den gemeinsamen bestehenden HD003-Kategoriebaum für 8 Welt-, 69 Gruppen-, 381 Hobby- und 3.376 unterste Kategorieziele ersetzt. „Wind & Drachen“ erhält ein anderes vorhandenes Lenkdrachenbild statt Outdoorausrüstung; richtige Welt-/Gruppenbilder auf allen Ebenen. ZIP CRC, PHP und Browser-Tests vier Breiten bestanden. **Liveinstallation und Abnahme offen.** HD003 1.50.803 (Vorschaubilder ohne Featured Image) und HD007 1.2.21 unverändert. Ältere HD009-Versionen in folgenden Abschnitten sind historisch.



**Aktuell am 08.11.2026: gemeinsamer Bildfix HD009 0.1.27 + HD003 1.50.803.** HD009 nutzt auf echten WordPress-Kategoriearchiven die vorhandene 3.376er-Leaf-Zuordnung aus HD003, selbst wenn WordPress keine Elternkategorie setzt. Der Banner zeigt das thematisch passende genehmigte Foto der Hobbygruppe; Sportdrachen → Wind-&-Drachen-Foto statt bildlosem bzw. fachfremdem Banner. Als Rückfall bleiben die acht Weltbilder. HD003 zeigt in seinen drei vorhandenen Beitragskachel-Varianten bei fehlendem Beitragsbild ein passendes, vorhandenes Hobbyfoto; vorhandene Beitragsbilder haben Vorrang. Sportdrachen-Vorschaubild: separates Delta-Drachen-Foto. **Keine neuen Bilder generiert, keine neuen Bannerplätze, keine Änderung an Partner-/Produktlogik.** Beide vollständigen ZIPs gebaut, ZIP/PHP 24+13 PASS, echte PHP-Funktionstests PASS, Zuordnung 3.376/3.376 PASS, Browser-Simulation bei 1440/900/390/360 PASS. Die beiden neuen ZIPs sind gültige Downloads; **Installation und echte Sichtabnahme noch offen**. Bisherige Angaben zu 0.1.26 bzw. 1.50.798 darunter historisch.



**Aktueller Stand 08.11.2026: HD009 Affiliate-Zentrale 0.1.26**, Download `HOBBY_DEPOT_AFFILIATE_HD009_0.1.26.zip`, 1.553.271 Bytes, SHA-256 `a627e35a9e8d20f34616c1ead4bc1b7d180e40a8f74abb985c7311b60dcfcd8f`. Einzige Abweichung von 0.1.25: zu großer Abstand **oberhalb des im Hobbyregister-Text eingebauten Querbanners** auf Desktop und Mobil korrigiert (47→17 bzw. 57→11px gerundet). Acht Themenfotos, Kategoriebanner-Höhe, Amazon-Button und alle Ausspielregeln unverändert. Voll-ZIP 41/41, PHP 24/24 und Browser-Test zwei Registerprofile / vier Breiten PASS (Action 42461816837). Live-Installation und optische Abnahme 0.1.26 offen; Beitragsbannerdesign später separat entscheiden. Frühere HD009-Stände unten sind historisch.



**Aktuell 07.11.2026: HD009 Affiliate-Zentrale Version 0.1.25** (Download `HOBBY_DEPOT_AFFILIATE_HD009_0.1.25.zip`, Größe 1.553.090 Bytes, SHA-256 `c82b75f9f485eec43f6b8626ff4a6748f3610c0093e61616d4bdd8d4d62204d0`). Auf allen Kategorieebenen verwenden eigene Amazon-Kreativs acht feste, textfreie Weltbilder statt des Seiten-Heros; „Tiere“ zeigt Terraristik/Insektenumfeld statt Haustiere. Desktop-Kategorie-Werbebanner 6:1, mobil 4,2:1; Original-Amazon-Button, Verlauf, Titel und vorhandene Ausspielplätze bleiben unverändert. Hobbyregister-Quadrat hat wieder echte Bildquelle (bei Bedarf das HD007-Herobild mit anderem Zuschnitt). Eigene Beiträge und Produkt-/Kampagnenlogik unverändert. Voll-ZIP CRC, PHP 24/24, fünf Original-PHP-Fälle, reale Frontend-Simulationen bei 1440/960/390/360 alle bestanden; Live-Installation/Abnahme noch offen. Angaben zu früheren HD009-Versionen darunter historisch.



**Aktueller Stand 07.11.2026: HD009 Affiliate-Zentrale 0.1.24** (Download `HOBBY_DEPOT_AFFILIATE_HD009_0.1.24.zip`, SHA-256 `e1bc7cc4d7ab69bc711c424c3d1a612c4710f66155eba7a401552329a800f3a6`). Belegte Bannerplätze auf Kategorieebenen, im Hobbyregister und auf regulären Artikeln bekommen bei fehlendem genehmigtem Fotomotiv einen Bild-freien, thematischen Amazon-Suchbanner. Für Registerprofile bleibt nur **ein** Affiliate-Foto im Querbanner; Quadrat als gestalteter Themenbanner ohne Bildwiederholung. Bestehende Partner-/Produktzuordnung unverändert. Tests PHP 24/24, CRC, sechs Funktionsfälle und Browser 4 Layouts/4 Breiten PASS; produktive Installation und Vollabnahme noch offen. Ältere HD009-Standangaben unten sind Historie.



**Aktueller Downloadstand 07.11.2026: HD009 Affiliate-Zentrale 0.1.22 (`HOBBY_DEPOT_AFFILIATE_HD009_0.1.22.zip`) und HD007 Hobbyregister 1.2.20 (`HOBBY_DEPOT_HOBBYREGISTER_HD007_1.2.20.zip`).** Beide vollwertigen Installations-ZIPs liegen zusätzlich byteidentisch als jeweilige `CURRENT.zip` im zugehörigen Büro. 0.1.21 und 1.2.18 sowie alle weiteren früheren Versionen in älteren Abschnitten sind **historisch**. PHP/ZIP-Prüfung bestanden, echte WordPress-Live-Versionen nicht authentifiziert ausgelesen.



**Neueste aktive Download-Wahrheit (07.11.2026): HD009 0.1.21-dev**, 1.067.588 Bytes, SHA-256 `f6dd1cb301dbe661b63a9dd6b7890d0363c3317f025ee8617a94348b6001a002`. Hero-Farbwelt und Verlaufsbanner sind neu. Bestehende Werbeplätze, Link- und Providerlogik sowie DataForSEO bleiben unverändert; Browser-Prüfung PASS, Live-Installation noch offen. Alle 0.1.20-Angaben in den folgenden älteren Abschnitten sind historisch.

**Neu zur Design- und Produktstrategie 0.1.20:** Siehe `BANNER_ZIELREGELN_20261107.md`. Banner-Design ist in der neuen aktuellen Voll-ZIP, DataForSEO-Recherche weiterhin manuell; kein automatischer Produktlinkwechsel. Sonstige ältere Prüfabschnitte unten beschreiben den 0.1.18/0.1.19-Vorläufer.

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

**Stand 07.11.2026 · Affiliate-Zentrale HD009 0.1.20-dev.**

## Einziger aktueller Download

- `../PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/CURRENT.zip`
- **1.066.589 Bytes · SHA-256 `cd6cb75f3ef0f393f94f3f93b974f3663ffa1f449c579886ae9520bc3d920cbb`**.
- WordPress-Originalordner `affiliate-portal-router/` bleibt erhalten. **Keine parallele Plugininstallation.**
- Details und Nachweise im `../PLUGINS/ISOLIERTE_PLUGINS/HD-009-AFFILIATE-ZENTRALE/MANIFEST.md`.

## Hobbyregister – verbindliche neue Anzeigenplätze (0.1.19)

Die HD007-Hobbyregister-Inhalte und das HD003-Design bleiben unverändert. Nur das **vorhandene HD009-Affiliate-Plugin** steuert die Position der beiden Banner auf den Register-Einzelprofilen:

- **Desktop:** `Auf einen Blick` → quadratischer Amazon-Partnerbanner → `Hobbygruppe` → übrige Seitenleistenblöcke.
- **Zusätzlich im Haupttext:** ein responsiver Querbanner **unmittelbar nach `Kosten und Ausrüstung`**.
- **Mobil:** zuerst der Hauptartikel (mit einer Inlineanzeige nach `Kosten und Ausrüstung`), **anschließend** die quadratische Seitenleistenanzeige **als erster Block vor der Hobbygruppe**. Nicht direkt ganz oben.
- **In 0.1.20 optisch verfeinert:** wärmerer Verlauf, 2px-Rundungen, kleinerer Amazon-Button, Foto dezent zurückgenommen.
- Derselbe native Pferdeatelier-/Hobby-Partner-, Kategorie- und Werbemittelweg bleibt zuständig. Keine zusätzliche Quelle, neuer Import oder neues Plugin.

**Nachweis:** Original-Plugins HD003+HD007+HD009 in realem WordPress mit MariaDB und Browser getestet. Öffentliche Test-Registerseite HTTP 200, Desktop- und Mobil-Anzeigenordnung sowie vollständige Gestaltung, eine Sidebar- und eine Inline-Anzeige pro Profil **PASS**. Einzelwerte und Testbericht in der HD009-`EVIDENCE`.

**Grenze:** Die 0.1.19-Positionen hat der Betreiber live bestätigt; die neue 0.1.20-Gestaltung ist noch nicht live geprüft.

## Verbindlicher Amazon-Eigenbanner nach Auswahl Variante 4

- **Eigenes Hobby-Depot-Logo im Werbebanner entfernt.** Kein zusätzliches „Entdecke deine Ausrüstung“.
- Oben nur der Hobby-Titel, z. B. „Airbrush-Modellbau“, auf **schmalem warmem Verlauf**.
- Darunter ein **großes, nachweislich passendes Hobbyfoto** aus dem bestehenden HD003/HD007-Bestand, keine Collagen.
- **Im Foto:** gelb-oranger Button mit Pfeil und dem *originalen, unveränderten, von Amazon für Werbung zugelassenen deutschen* Logo **„Erhältlich bei Amazon“**. Das gewöhnliche Amazon-Logo ist ohne Sondergenehmigung **nicht** zulässig. Bei extrem schmalen Werbeplätzen wird auf einen Textlink umgestellt.
- **Quadrat 1:1**: vorhandene Hobbyregister- und Glossar-Einzelbanner, Desktop und Mobil.
- **Querformat**: vorhandene Kategorien-/Hubbanner, volle verfügbare Breite und flexible Mindesthöhe. Original-HD003-Problem (76px feste Höhe einschließlich der Bilder) für **diesen einen eigenen Banner-Typ** gezielt aufgehoben.
- **Nur einmal „Anzeige“**: vorhandene Kategorien-Kennzeichnung „Anzeige · Partner“ bleibt, das zweite Label des Eigenbanners dort unsichtbar.
- Richtige Ziel-URL: hinterlegte Amazon-Tracking-ID, aus dem echten Hobbyteil abgeleiteter Suchlink. WordPress-HTML-Entities in Titeln werden vor Generierung korrigiert. **Keine Produkt-/Preisbehauptungen ohne echte Daten.**

## Vorhandene Technik bleibt zuständig

Pferdeatelier-basierte Kampagnenauswahl, Relevanz, Kategorien/Elternpfad, Bildformat, Freigaben/Veto und bestehende HD004-/HD007-Kontakte bleiben unverändert. Amazon/idealo/DataForSEO-Funktion nicht neu entwickelt; weder neuer Bannerverteiler noch Tabelle oder zusätzliches Plugin. Mietwerbung `Hier könnte Ihre Werbung stehen` gehört allein zum unveränderten HD003-Design.

## Nachweis und noch offener Livepunkt

- 24/24 PHP geprüft, ZIP CRC PASS; PHP-Amazon/Partner-Regressionschecks PASS.
- Vier echte Chromium-Browserfälle bestanden – **700px Quadrat, 186px Register-Quadrat, 770px Querformat, 355px schmales Querformat**. Alter fester 76px-Streifen in der Simulation beseitigt; Amazon-Logo dort mindestens 140px, ohne Verzerrung.
- Screenshots plus Prüfnachweis in der einzigen HD009-Plugin-Akte.
- **Produktivinstallation 0.1.18 noch nicht durchgeführt/bestätigt.** Kein behauptetes Live-PASS.

## Einmaliger WordPress-Test nach Installation

1. `https://hobby-depot.de/gestalten/malen-zeichnen/` – Querbanner unter „Weiter in Malen & Zeichnen“.
2. `https://hobby-depot.de/hobbyregister/airbrush-modellbau/` – Quadratbanner in der Register-Seitenleiste.
3. Es muss in beiden Fällen genau ein deutlich sichtbarer Banner mit Titelstreifen, großem Hobbyfoto und orangefarbenem Amazon-Button erscheinen. Keine doppelte Anzeigenkennung auf der Querseite.
