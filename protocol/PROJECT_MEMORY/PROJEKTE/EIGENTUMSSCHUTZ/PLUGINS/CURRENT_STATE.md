## 07.11.2026 – HAB-004 0.1.8-rc11 – EINZIGER AKTUELLER STAND

**Installations-ZIP:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`; **624,020 Bytes**, **SHA-256:** `cf8cf7946aa7605dadecda1f041cfc6fb150c7971f7c9feb9dbb6dd1ac8eabda`; 28 ursprüngliche Dateien, davon **24 gegenüber RC10 unverändert**. WordPress-Pluginordner bleibt `affiliate-portal-router/`. Vorgänger RC10 ist nur noch über Git-Historie, kein zweites CURRENT.

**Ursache beseitigt (Quell- und offline simulierte Frontend-Ausgabe):** HAB-001 reicht echte WordPress-Kategorien an den bestehenden Filter weiter; HAB-004 wies bislang alle Kategorien ab. RC11 verbindet **nur den vorhandenen Kategorie-Anschluss** mit `provide_leaf_category_affiliate_slot_html`, priorisiert die unveränderte Kampagnenauswahl und zeigt bereits gespeicherte, fachlich passende DataForSEO-Amazon-ASINs als **einzelne Produktkarten** mit dem ursprünglichen `render_banner`. R3-Themenseiten erhalten ebenfalls einzelne Karten statt zusammengeklebter Textlinks. **Ohne gespeicherte gültige ASIN kein leeres/erfundenes Produktangebot.** Keine falschen Bilder, Preise oder Verfügbarkeit.

**Abnahme:** Original-RC10-Fehler reproduziert; vollständiges HAB-004-RC11 samt tatsächlichem HAB-001-Designaufruf offline getestet. Kategorie „Wassermelder“ und R3 „Leckwarnung & Absperrung“ jeweils zwei getrennte geprüfte Amazon-Testlinks mit Hab-Tracking-ID, gebuchte Anzeigen haben Vorrang, Hauptschalter AUS respektiert, unbekannte/produktlose Kategorien bleiben leer. **18 getrennte PHP-Regressionstests, 34 PHP-Syntaxprüfungen (einschließlich Prüfscripten), 28/28 ZIP-CRC, alle erfolgreich.** Testnachweis `AFFILIATE/IMPLEMENTIERUNG_RC11/PRUEFBERICHT.md`. Pferdeatelier 6.72, Hobbydepot HD009 0.1.19 und HAB-001/002/003 nicht geändert. Kein weiterer bezahlter DataForSEO-Auftrag.

**Noch nicht live abgenommen:** RC11 muss als **Update des bestehenden HAB-004** in WordPress installiert werden; dann die vorhandene Kategorie „Wassermelder“ und R3 „Leckwarnung & Absperrung“ im Frontend prüfen. Hauptschalter der Affiliate-Zentrale muss eingeschaltet sein. Die separate serverseitige WP-Cron-Ursache ist nicht hiermit repariert. **Keinen neuen kostenpflichtigen Suchlauf anstoßen**; gespeicherte ASINs genügen zum Test.

---

## 07.11.2026 – HAB-004 RC10, einziger aktueller ZIP-Stand
**ZIP:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **623469 Bytes**, SHA-256 `f3b6b0ac4fd05310fa32ce68e2715b29d022003ac68f32ceb051443832364ced`, Git-Blob `03a79f162ab37b7913b67106988ea9edd4d3ca30`. Version `0.1.7-rc10`; 28 Dateien, 25 davon gegenüber RC9 byteidentisch. Ausschließlich bestehendes HAB-004 geändert; HAB-001/002/003 und andere Portale nicht angerührt.

**Produktiv gemeldete Ursache:** 07.11.2026 13:51 wurde ein kostenpflichtiger DataForSEO-Task für `Wassermelder` angelegt; am Screenshot 15:10 war immer noch nur `geplant` zu sehen und kein weiterer Lauf. RC9 bewies mit `wp_next_scheduled()` bloß einen Zeitplan, aber keine tatsächliche Ausführung. Weshalb der Server den Cron nicht ausführt, ist noch ungeklärt. **Nicht so tun, als sei serverseitiger Cron bereits repariert.**

**RC10 KISS:** Bei offenem, bereits bezahltem DataForSEO-Task führt das Öffnen der bestehenden WordPress-Seite `Affiliate-Zentrale → Amazon-Automatik` höchstens alle 120 Sekunden einen **kostenlosen GET-Ergebnisabruf** durch; kein neuer bezahlter POST. Sichtbar: Uhrzeit letzter realer automatischer Lauf, letzter API-Ergebnisabruf, Status/Error, tatsächlicher geplanter Termin mit ÜBERFÄLLIG statt irreführendem `geplant`. Bei offenem Task nur Knopf `Offenen Auftrag jetzt prüfen (keine neue Suche)` mit eigener garantiert poll-only Behandlung, selbst wenn Auftrag zwischenzeitlich verschwindet; separater eindeutig kostenpflichtiger Startknopf erst nach Abschluss. Ungültige/abgelaufene Task-ID löst nie unbemerkt neue bezahlte Suche aus. Kostenbudget 5/Tag, regulärer WP-Cron, Kategorien- und Ausspielungslogik unverändert.

**Echte lokale Belege:** vollständiges HAB-004 geladen mit WordPress- und DataForSEO-Simulation, 2720 Knoten/2714 Zuordnungen, 6/7/8 Hauptwelten. Vom bezahlten Erstauftrag über bewusst ausbleibenden WP-Cron, kostenlose GET-Anfrage per Admin-Ansicht, später fertiges Ergebnis und Speicherung bis zur Ausgabe im vorhandenen Hab-Designslot. Auch pending, API-Fehler, ungültiger/veralteter Auftrag, Doppelklick, funktionierender Cron, bestehende Regressionen getestet. **400 bestandene Funktionen in 52 Testläufen, 25/25 PHP-Lint, ZIP-CRC 28/28.** Anbieterantworten sind nachgestellt; noch **kein** echter produktiver DataForSEO-Abfragetest, keine serverseitige Cron-Abnahme.

**Direkte nächste Live-Prüfung (keinen neuen bezahlten Auftrag beauftragen!):** RC10 in WordPress als Update installieren; `Affiliate-Zentrale → Amazon-Automatik` öffnen. Die Seite fragt den bisher offenen Task sofort kostenlos ab und zeigt tatsächlichen Ergebnisstatus. Wenn `Letzter automatischer Lauf` nicht weiterläuft und Termin überfällig ist, ist die serverseitige WP-Cron-Ausführung getrennt zu untersuchen. Keine neue Architektur oder weitere App installieren.

---

## HAB-004 – RC9: Sieben Hauptwelten ohne Gesamtsperre

**07.11.2026 – HAB-004 0.1.6-rc9 (einzige aktuelle Voll-ZIP):** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **618.212 Bytes, 28 Dateien**, SHA256 `04de5f4492887686c5a224640ffa5e4d64175927186dc3fe7f19d546e0ea4120`, Git-Blob `500d70b04607373a133966859de02b03ec7f62cb`.

**Harte Ursache:** Kategorienstruktur kennt sechs bestehende Welten plus `core:world:insurance` (siebte Welt), aber RC8 verlangte exakt sechs. Original-RC8 mit sieben Hauptwelten reproduzierbar `hb_worlds_unexpected`. Die 2.720 Knoten/2.714 Bindungen sind Live-Screenshot-Werte, kein heruntergeladener WP-Datenbankabzug.

**KISS-Korrektur:** Es wird nur verlangt, dass mindestens eine gültige gemappte Hauptwelt existiert; Welt- und Bereichszahlen folgen dem tatsächlich aktiven Bestand. Eine zusätzliche oder nicht gemappte einzelne Welt blockiert die restlichen Welten nicht. Bei vollständig fehlendem/ungültigem Snapshot werden weiterhin sicher keine kostenpflichtigen Aufträge gestartet. Der Affiliate-Hauptschalter `ppar_enabled` bleibt unverändert und muss bei Bedarf in WordPress (`Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv`) ausdrücklich aktiviert werden.

**Echte lokale Prüfungen:** 116 vollständige Original-Plugin-/Design-WP-Simulationen (6/7/8 Welten, 2.720 Knoten/2.714 Mapping, Klick→DataForSEO-Mock→ASIN→Speicherung→R3-/Kategorie-Ausgabe, 1 Welt ohne Mapping, falsche Revision, Altwerbe-Vorrang, global AUS); 104 DataForSEO-Worker-/Kosten-/Fehler-/Beitragstests mit sieben Welten; 96 Regressionstests; **316 PASS, 0 FAIL, keine PHP-Warnungen**, **25/25 PHP-Lints**, **ZIP 28/28 CRC**. 25/28 Plugindateien gegenüber RC8 identisch. Kein echter WordPress-Produktivlauf oder bezahlter DataForSEO-API-Auftrag. Dokument: `AFFILIATE/IMPLEMENTIERUNG_RC9/PRUEFBERICHT.md`, minimaler Patch `RC8_TO_RC9_SOURCE_DIFF.patch`.

**Nächster Schritt:** RC9 in WordPress als Update des bestehenden Plugins einspielen. Wenn die oben sichtbare Meldung „Affiliate-Zentrale insgesamt ausgeschaltet“ besteht, über `Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv → Einstellung speichern` einschalten. Erst dann unter `Amazon-Automatik` einmal `Jetzt einen Suchlauf starten`; der Status muss zeigen, ob ein Auftrag erzeugt wird, ein Fehler vorliegt oder bereits geprüft ist. Max. fünf neue kostenpflichtige DataForSEO-Aufträge/UTC-Tag. Die Live-Wirkung erst danach bestätigen.

---

## 07.11.2026 – HAB-004 RC8 – einzige gültige Pluginversion

**07.11.2026 – HAB-004 Affiliate-Zentrale 0.1.5-rc8 ist einzige aktuelle Voll-ZIP:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **620242 Bytes**, 28 ZIP-Dateien, SHA256 `f2d09e649fbb6a69a54e64b01df239013975999e46921f08b722adff139ccd30`, Git-Blob `35d32677fb7232a8c0891cc0e730b4b02851b945` (bei GitHub binär geprüft).

**Vollständige lokale Workflow-Simulation: 234 bestandene Prüfungen, 25/25 PHP-Syntax, ZIP-CRC 28/28; nur 3/28 Originaldateien verändert** (`affiliate-portal-router.php`, `includes/trait-ppar-hb-amazon.php`, `readme.txt`). RC7 hatte beim echten Screenshot nach manuellem Run null Kandidaten, aber irreführend bloß „Keine neuen passenden Produkte“. Nachstellung mit den originalen aktiven Hab-Quelladapter-Klassen beweist: bei fehlendem/falschem/inhaltlich nicht freigegebenem WP-Kategoriebaum wurde dessen WP_Error als leere Kandidatenliste verschluckt. Zudem vorherige RC7-Simulation des Frontends hatte einen falschen Kategorie-Slot und ignorierte leere Kategorien/Produktseiten. RC8 zeigt direkt nach Klick oben den echten Workflow- und Kategoriebaum-/Provider-Status und lässt DataForSEO bei ungültiger Quelle gesperrt; echte DataForSEO-API-Taskfehler werden erkannt, statt als unendliches „noch in Bearbeitung“ zu gelten. Wiederverwendung des bestehenden Workers, API-Kostenlimits und Slots, plus die vorhandenen Hab-Design-/Kategorie-Hooks für Amazon-Affiliate-Links auf relevanten Produktseiten selbst ohne redaktionelle Beiträge. Bereits vorhandene Werbung hat Vorrang. Keine zweite DB, kein zweiter Cron, keine Fremdportale/K0 verändert.

**Ehrliche Testgrenze:** Die originalen vollständigen Hab-Plugin-Dateien inkl. originalem Portal-Quelladapter und originalem Design-Plugin-Hook wurden offline mit nachgestellten WordPress-Optionen und DataForSEO-API-Antworten ausgeführt; **keine echte WordPress-Produktivabnahme, keine kostenpflichtige Provider-Abfrage, kein Einblick in Live-Kategoriebaum-Optionen**. RC8 zeigt die genaue Quelle des noch offenen Live-Blockers erst nach Installation.

**Nächster Schritt:** Auf Hab-&-Bewahr-WordPress das bestehende HAB-004-Affiliate-Plugin durch diese RC8-Voll-ZIP ersetzen, `Affiliate-Zentrale → Amazon-Automatik → Jetzt einen Suchlauf starten` **einmal** drücken, dann die **oben sichtbare Statusbox** prüfen. Kein wiederholtes blindes Klicken; bis zu 5 neu bezahlte DataForSEO-Aufträge je UTC-Tag. Falls Quelle blockiert, dort die genaue Ursache lesen statt neue Suche zu behaupten.

Die anderen drei Hab-Plugins bleiben unverändert. Frühere RC7/RC6-Nennungen darunter sind nur Historie.

---

## 07.11.2026 – HAB-004 RC7: einzige aktuelle Affiliate-ZIP

**HAB-004 Affiliate-Zentrale 0.1.4-rc7**, vollständige einzige `CURRENT.zip`: **616209 Bytes, 28 Dateien**, ZIP-SHA256 `08725e5cf9d18654345b4b18b9f3c63ade54ce7a6da932d9768bc2b9867b1d6e`, GitHub-Binär-Blob `3df1bd941aa051f6706a66fd857a8745d0209420`. Gegen RC6 25/28 Dateien byteidentisch; nur die vorhandene Amazon-Datei, der bisherige Hab-Router und `readme.txt` geändert. Keine Fremdportale.

**Nach Prüfung des wirklichen RC6-Codes:** Die vorhandene Artikelerkennung und Werbeplan-Neuberechnung bei Speicherung blieb unangetastet. Neu nutzt **derselbe DataForSEO-Worker** künftig auch veröffentlichte Artikel, wenn die direkte Hab-Produktkategorie wirklich passt und der Artikel-Titel die konkrete Produktfamilie nennt. Bewusste Ausschlüsse: Entwürfe, allgemeine Ratgeber ohne explizites Produkt, Werbesperren, falsche Produktfamilien. Änderungen an Titel/Kategorie machen alte Treffer sofort ungültig. Alle aktuellen Produkt-/Bannerkampagnen behalten Vorrang; bei fehlenden passenden Produkten nur klar gekennzeichneter Amazon-Suchlink, nach verifiziertem API-Ergebnis reale Amazon-Textlinks. Kein zweiter Worker, keine neue API-Suche beim Beitragsspeichern und keine zusätzliche Datenbank; fünf bezahlte DataForSEO-Aufträge/UTC-Tag bleiben.

**Tests:** Alle 25 PHP-Dateien ohne Syntaxfehler, ZIP-CRC PASS, 23+16+23+34 lokale Assertions PASS (96 nicht notwendigerweise unabhängige Fälle). Echte Artikel-Produktslot-Funktion aus Original-Hauptdatei mit globaler Sperre, bestehender Werbung und Hybrid-/Legacy-Modus geprüft. **Kein** WordPress-/DataForSEO-/echter Produktiv-End-to-End-Test; Portal enthält derzeit noch keine echten Beiträge. RC7 bleibt ein geprüftes Upgrade-Paket, nicht produktiv abgenommen.

Die drei übrigen Hab-Plugins sind unverändert. RC6 und ältere Angaben unterhalb sind historische Belege; maßgeblich bleibt `PLUGIN_AKTEN/HAB-004-AFFILIATE/CURRENT.md`.

**Nächster Schritt:** Auf ausschließlich `hab-und-bewahr.de` das bereits vorhandene HAB-004 mit der RC7-ZIP kontrolliert aktualisieren. Amazon-Partner-ID und gespeicherte Zugangsdaten bleiben über dieselben bestehenden WordPress-Optionen erhalten, deren tatsächliches Fortbestehen nach dem Upgrade zu prüfen ist. Beim nächsten real veröffentlichten, korrekt kategorisierten Produktbeitrag erfolgt die themenbezogene Suche über den bestehenden WP-Cron. Keine manuellen Amazon-Einzelkampagnen, keine neuen Plugins. HAB-001/002/003, Pferdeatelier, Hobbydepot und K0 unverändert.

---

## 07.11.2026 – HAB-004 RC6 – einzige gültige Plugin-Current

**Stand 07.11.2026 – einzige aktuelle HAB-004-Voll-ZIP 0.1.3-rc6:** `CURRENT.zip` 618.152 Bytes, 28 Dateien, SHA-256 `ef51d931d0c104e8cbb1ed0b27d33e0b6855c1202e605fe06440afc50d0574b9`, Git-Blob `c9026cbcfaa44a03a69820d9d35207f8b6ce5c27` (Größe und Hash aus echtem GitHub-Binärarchiv geprüft).

**Nachgewiesene Ursache aus dem RC5-Quellcode:** kein manueller Start; erster WP-Cron-Lauf erst nach mindestens 5 Minuten plus Website-Aufruf; DataForSEO-Kandidatensuche ausschließlich bei bereits aktiven eBay-/idealo-Produktkampagnen, obwohl Hab diese Anbieter noch nicht eingerichtet hat. Dass der WP-Cron eingetragen ist, beweist keinen tatsächlichen Suchlauf. **RC6:** im selben vorhandenen Hab-Amazon-Modul ein authentifizierter Admin-Button `Jetzt einen Suchlauf starten` an **denselben** vorhandenen Worker angebunden; stündlicher WP-Cron unverändert. Bei fehlenden eBay-/idealo-Kandidaten werden ausschließlich nachweislich im aktiven Hab-Zielkatalog vorhandene konkrete Produktfamilien recherchiert. DataForSEO-Ergebnisse werden nur bei organischen Amazon.de-Produktlinks, gültiger ASIN und im Titel tatsächlich genannter Produktfamilie als maximal 3 schlichte Textlinks pro Kategorie in **bereits vorhandenem Banner-Slot** zugelassen. Keine erfundenen Produktkarten, keine Bilder/Preise/Bewertungen oder Lagerbehauptungen. Bestehende Kampagne hat Vorrang. Ungültige/fremde Treffer bleiben gesperrt. Keine zweite Produktdatenbank, kein neues Plugin.

**Belege/Grenzen:** 25/25 PHP-Syntaxprüfungen, vollständiger ZIP-CRC, 62 lokale Positiv-/Negativprüfungen in drei Testdateien, 25/28 RC5-Dateien byteidentisch (neu geschrieben nur `affiliate-portal-router.php` Version, `includes/trait-ppar-hb-amazon.php`, `readme.txt`). Kein echter WordPress-/DataForSEO-/Amazon-Produktivtest und keine Ausführung kostenpflichtiger API-Abfragen durch den Build. Bestehende Einstellungen beim WordPress-Update sollen erhalten bleiben; unverändert bleiben auch HAB-001/002/003, Pferdeatelier, Hobbydepot, K0. In der WordPress-Sitzung müssen tatsächliche DataForSEO-Zugangsdaten gespeichert und die Amazon-Automatik aktiv sein. Maximal 5 neue kostenpflichtige POST-Suchaufträge pro UTC-Tag auch beim manuellen Start; offener Auftrag wird lediglich per kostenlosem GET abgefragt. Alle früheren RC5/RC4-Einträge darunter nur historische Protokolle. Drei anderen Hab-Plugins unverändert.

**NÄCHSTER SCHRITT:** Bestehende Hab-&-Bewahr-Affiliate-Zentrale in WordPress durch die neue RC6-ZIP ersetzen. `Affiliate-Zentrale → Amazon-Automatik → Jetzt einen Suchlauf starten` einmal klicken. Danach zeigt dieselbe Seite **Letzter tatsächlicher Lauf**, **Letzte Meldung**, **Offener Auftrag**, **gefundene Einzelproduktlinks** und **bezahlte Suchaufträge heute**. Kein zweites Plugin. Ein neuer Suchauftrag kostet DataForSEO-Guthaben. Ein Ergebnis kann erst bei einem späteren Worker-Durchlauf eintreffen. Nach echten Daten prüfen, ob die globale Affiliate-Ausspielung und die Kategorie-Slots aktiviert sind; keine Live-Ausgabe vorher behaupten.

---

## 07.11.2026 – HAB-004 RC5: neue einzig gültige Plugin-Current

**Version 0.1.2-rc5 (07.11.2026), allein HAB-004:** Voll-ZIP `CURRENT.zip` 616.662 Bytes, 28 Dateien, SHA-256 `84b4c071f69c6da3e6a3a92dac519ced45a9ba331b09f9d395914a96baa3a7c7`, Git-Blob `13ecb1aa84e1050f4c7fc53a06c32e6c9369a2d6` (GitHub-Ordner: Größe/Blob unabhängig abgeglichen). RC4 aus PR #664 bleibt über Git-Historie wiederherstellbar.

**Gezielte RC4-Korrektur:** Der DataForSEO-Merchant-Amazon-Products-Endpunkt liefert die Kennung als `data_asin`; RC4 las nur `asin`. RC5 liest das tatsächliche `data_asin` und prüft zusätzlich Amazon-Domain, exakten Titel, eindeutige Kennung, Packungsvarianten und keine bezahlten Treffer. Wenn noch kein eBay-/idealo-Produktkatalog existiert, wird **nur für reale Produktfamilien-Kategorien aus dem eigenen Hab-Workflow**, und nur im vorhandenen Banner-Slot `product_after_category_tiles`, ein einfacher automatischer Amazon-Suchlink erzeugt (mit `habundbewahr-21`, Anzeige-/Werbelinkkennzeichnung). Keine erfundene Amazon-Produktkarte, kein zweiter Bannermotor, keine Bilder/Preise/Bewertungen aus DataForSEO. Vorhandene Werbekampagne hat Vorrang. Für echte Einzelprodukt-Direktkarten benötigt der bestehende DataForSEO-Worker weiterhin ein vorhandenes freigegebenes eBay-/idealo-Ausgangsprodukt.

**Tests:** 25/25 PHP-Syntaxprüfungen, ZIP-CRC 28/28, 40 lokale Positiv-/Negativtests (darunter 16 neue RC5-Fälle), 25 originale RC3-Dateien unverändert. Keine authentifizierte WordPress-/Provider-Liveprüfung; DataForSEO kostet bei eingeschalteter Recherche, max. fünf neue Tasks je UTC-Tag. Die gesamte Automatik ist standardmäßig aus. Keine Änderungen an HAB-001/002/003, Pferdeatelier, Hobbydepot, K0 oder externen Zugangsdaten.

Die übrigen drei Hab-Plugins bleiben unverändert. Alte RC4-/RC3-Einträge weiter unten sind historisch. Siehe `PLUGIN_AKTEN/HAB-004-AFFILIATE/CURRENT.md`.

**Nächster Schritt:** Nur die bestehende Hab-Affiliate-Zentrale in WordPress kontrolliert mit RC5 aktualisieren. `Affiliate-Zentrale → Amazon-Automatik`: Tag `habundbewahr-21` speichern, Amazon-Produktbuttons aktivieren; DataForSEO noch aus lassen. Erst echten Kategorien-Suchlink mit eigener Tracking-ID prüfen, danach die kostenpflichtige DataForSEO-Suche getrennt freigeben und Datenbasis für konkrete Produktkarten prüfen.

---

## 07.11.2026 – HAB-004 RC4 (NEUE EINZIGE CURRENT-VERSION)

HAB-004 0.1.1-rc4: vollständige CURRENT.zip, 616072 Bytes, 28 Einträge, SHA256 c601c1f540fccdd18dde59b7c15fc55cfe53b68a59459d45182a2cf1bcd55017, Git-Blob f3a77efff2cb16de34c91eb0c4ec3b072a3999db (remote Größe und Blob bytegleich geprüft).

Lokal geprüft: PHP Syntax 25/25, 24 Assertions (Positiv/Negativ, Variantenabweichung, falsche Portal-ID, bezahlter POST vs kostenloser GET, Tagesgrenze, keine doppelten Buttons), ZIP CRC, installierbare Original-Pluginwurzel, 25/27 originale Dateien bytegleich. Keine authentifizierte WordPress-Installation oder echte Provider-Verbindung und keine Google-/Frontend-Liveprüfung; nur ein Upgrade-Testkandidat. Die Standardautomatik bleibt deaktiviert. Die anderen drei Hab-Plugins bleiben bytegleich unverändert. Die Versionsangaben zur RC3 weiter unten sind historisch.

Technische Details ausschließlich unter PLUGIN_AKTEN/HAB-004-AFFILIATE/CURRENT.md.

Nächster Schritt: nur das bestehende Hab-004-WordPress-Plugin mit CURRENT.zip aktualisieren; Affiliate-Zentrale → Amazon-Automatik öffnen; habundbewahr-21 speichern, Amazon-Produktbuttons einschalten; eigene DataForSEO-Zugangsdaten erst nach Kostenfreigabe eingeben; an einer echten passenden Produktkarte Ziel/Tracking und Slot prüfen. Pferdeatelier und Hobbydepot/K0 unverändert.

---

## 06.11.2026 – HAB-004 Affiliate RC3: OFFIZIELLER NEUER STAND

Neu ist **nur HAB-004-AFFILIATE**: Version **0.1.0-rc3**, komplette `ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` (605.196 Bytes, 27 Dateien), SHA-256 `2e5f6790ab3a64b446e34d132037684ad8fa637f76f43974e2816a1f75bc11eb`, Git-Blob `b6b19e7a739b70a813c5e9de2e290d98c898156f`. Die vorangegangene RC2 ist **historisch** und nicht mehr „CURRENT“. Die drei bestehenden Plugins HAB-001-DESIGN 0.1.189, HAB-002-KATEGORIE-WORKFLOW 1.14.8.37 und HAB-003-BILDZENTRALE 1.0.0 bleiben bytegleich unverändert. Weiterhin **vier vollständige originale WordPress-ZIPs** im bestehenden Pluginbüro.

Verifiziert: GitHub-Run **42252394077** (Dateien/Funktionen der neutralen Engine erhalten, 24/27 Dateien gegenüber RC2 unverändert, 92 Hooks im Starttest, 6 Welten / 285 Kategorien / 13 belegte Produktkategorien aus dem offiziellen HBDP-Designpaket, Positiv- und Negativtests, zweifach bytegleicher Neubau, ZIP-CRC, frischer vollständiger GitHub-ZIP-Readback). **Kein echter WP-Live-PASS**, keine 6.72.306-Gesamtparität, keine Provider-Echtverbindung, keine reale Hosting-Lastmessung. Details und verbindliche Grenzen ausschließlich in `PLUGIN_AKTEN/HAB-004-AFFILIATE/CURRENT.md`.

**Nächster operativer Schritt:** RC3 auf Hab & Bewahr kontrolliert installieren und tatsächliche WordPress-Kategorien und Frontend-Ausgabe prüfen; Affiliate-Automatik bleibt bis dahin AUS. Pferdeatelier K0 und andere Portale unangetastet.

---

## 06.11.2026 – HAB-004-AFFILIATE – neues viertes vollständiges Eigenplugin
<!-- HAB004_20261106_RELEASENOTE -->
Im **bestehenden** Hab-&-Bewahr-Pluginbüro ist die ganze installierbare `ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` (0.1.0-rc2, 603.323 Bytes, 27 Dateien, SHA-256 `014e42b9657eed74b4d2e1f29ea51c6c6bf5c276ec30402011289b3821cbe153`, Git-Blob `077a35ccb3d2f9fc75c646629f183a28acbf342c`) hinzugekommen. Nachweis: GitHub-Run 42246580133 einschließlich vollem unabhängigen GitHub-Wiederabruf, CRC, PHP/JS-Syntax, 26 originalen Source-Files, unveränderten ursprünglichen Funktionen, fünf zuvor fehlenden Modul-Starts sowie Positiv/Negativprüfungen der Hab-Kategoriebindung. Installationskandidat, **WordPress-Liveprüfung und Prüfung gegen das vollständige Pferdeatelier 6.72.306 Archiv sind NICHT abgeschlossen**. Automatik bleibt in Standardeinstellungen AUS. Nur die eigene Projekt-Binärdatei; kein fremdes Portal, keine Provider-Zugänge importiert.

**Neuer Bestand: 4/4 echte vollständige Eigenplugin-ZIPs**. Die vorhandenen Design 0.1.189, Kategorie-Workflow 1.14.8.37 und Bildzentrale 1.0.0 wurden nicht geändert. Dies ist die einzige aktuelle Pluginbüro-Statusautorität, technische Einzelheiten in `PLUGIN_AKTEN/HAB-004-AFFILIATE/CURRENT.md`. **NEXT ACTION:** Kandidat in einer gesicherten Hab-&-Bewahr-WordPress-Installation aktivieren und zunächst ohne Provideraktivierung die Adminseiten, den aktiven zentralen Katalog, die Hub-/Artikel-/Glossar-/HivePress-Brücken, die Performance und die unveränderte Ausgangslage der bestehenden Plugins prüfen.

---

# HAB & BEWAHR – PLUGINS / AKTUELLER CAMPUS-RELEASE-STAND
<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->
## Stand 06.11.2026 – DIE DREI EIGENPLUGINS / VERSION 0.1.189

**Versionsautorität:** die drei bestehenden `PLUGIN_AKTEN/<ID>/CURRENT.md`. Physische echte Voll-ZIPs in `ISOLIERTE_PLUGINS/<ID>/CURRENT.zip`; keine zweite Autorität und keine Bibliothek.

1. `HAB-001-DESIGN` **0.1.189**: 84.349.647 Bytes, 430 ZIP-Einträge, SHA-256 `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`, Git-Blob `504fccb82f4e9a3b10bb6405b468e1dbd03c62e1`. Voll-ZIP im bestehenden Pfad. GitHub-Run **42223947280**: neuer unabhängiger Abruf direkt vom GitHub-Releasezweig `hbd-design-0189-release-20261106`, ZIP vollständig neu geöffnet, CRC/Hash/Version PASS. Das ist ein GitHub-Artefakt-/Quelltest, **keine WP-Live-Freigabe**. Vorherige 0.1.184 als Rollback unverändert in Git-Historie, PR #625.
2. `HAB-002-KATEGORIE-WORKFLOW` **1.14.8.37**: 368.530 Bytes, SHA-256 `ec39080e5350b9f7b3924239376e11580ce7de195a60bb89feafae6152533f98`, Blob `35651f44ac70ed51e663d5dfaf45094bc9f1e3b2`, bestehende Voll-ZIP unverändert.
3. `HAB-003-BILDZENTRALE` **1.0.0**: 70.397 Bytes, SHA-256 `58af0d394752e767b5f0c7d6d9901eeaec921331ab6245144859e3e6626e4559`, Blob `8b8b3b84b494eb2784181d5bfd6acfb2efceafde`, bestehende Voll-ZIP unverändert.

**Status für die drei echten Projekt-Plugins:** ZIP-Archiv/Paket lokal geprüft; separate WordPress-Liveinstallation unbestätigt. **NEXT ACTION:** Design-0.1.189 im bestehenden WordPress-Plugin installieren und je einen normalen Beitrag mobil/desktop und eine Schutzbereichsseite auf tatsächliche Darstellung prüfen. Niemals ein neues Plugin hinzufügen oder K0/andere Portale anfassen.

**Wichtig vor Merge:** Dieser Nachtrag ist auf dem geprüften Releasezweig vorbereitet; er wird erst nach erfolgreicher geschützter Übernahme in den Campus-Hauptzweig zur offiziellen Current-Wahrheit. Kein PR ersetzt den Merge.

---

## Verbindlicher Ablageablauf für jedes künftige Plugin-Update (06.11.2026)

**Dieser vorhandene Weg hat mit PR #634 tatsächlich funktioniert; kein neues Plugin, kein zusätzliches Büro und keine Bibliothek.**

1. **Nur das betroffene Plugin aktualisieren:** von seiner originalen `CURRENT.zip` ausgehen; identischen Pluginordner behalten; ganze neue ZIP auf ZIP-CRC, PHP/JS-Syntax, Version, Hash, Dateibestand und unveränderte Fremddateien prüfen.
2. **Voll-ZIP am vorhandenen Ort aktualisieren:** in einem regulären Freigabezweig vom offiziellen Campus genau `ISOLIERTE_PLUGINS/<ID>/CURRENT.zip` als echte Binärdatei ablegen, technische `PLUGIN_AKTEN/<ID>/CURRENT.md` und Manifest mit Nachweisen aktualisieren. Die anderen zwei Original-ZIPs nicht anfassen.
3. **Normalen GitHub-PR statt Sonderwege:** `single-current-lock` bestehen lassen, geschützten PR in den offiziellen Campus mergen. Nicht auf reine Chat-Datei, kurzlebiges Actions-Artefakt oder offene PR als Ablageersatz ausweichen.
4. **Frischer unabhängiger Wiederabruf:** nach dem Merge alle drei aktuellen `CURRENT.zip` aus dem offiziellen Campus separat abrufen und Größe, SHA-256, ZIP-CRC, Pluginversion prüfen; `PLUGINS/CURRENT_STATE.md` als einzige aktuelle Büro-Autorität pflegen. Ohne Readback kein PASS.
5. **Rollback:** Vorgänger-ZIP bleibt über den vorherigen freigegebenen Git-Commit/PR zugänglich; ein Live-PASS wird nie aus lokalen Tests abgeleitet.

**Nachgewiesene Referenz:** PR #634 enthält echte vollständige Design-ZIP 0.1.189 im bestehenden Büro; GitHub-Actions-Run **42224724306**: unabhängiger frischer Download **aus dem offiziellen Campus** und dreimal `OFFICIAL_CAMPUS_ZIP_READBACK_PASS`:
Design 0.1.189 (84.349.647 B/430 Einträge), Kategorie-Workflow 1.14.8.37 (368.530 B/49), Bildzentrale 1.0.0 (70.397 B/3). Alle drei SHA-256 und CRC stimmen mit ihren technischen Akten überein.

**Verbleibender fachlicher Schritt:** Der neue Plugin-Code ist noch nicht unabhängig auf der tatsächlichen WordPress-Webseite live geprüft; das ist keine Ablagesperre, sondern gesonderte Abnahme.

---

## Historische Ablageakte vom 03.11.2026 (durch obere Fassung für Designversion abgelöst)


## Stand 03.11.2026 – ABLAGE ABGESCHLOSSEN: 3/3 ORIGINAL-ZIPS IM OFFIZIELLEN PLUGINBÜRO

**Geltungsbereich:** ausschließlich die drei belegten eigenen Hab-&-Bewahr-WordPress-Plugins. Keine Fremdplugins und keine Dateien anderer Portale.

**Offizieller Campus-Branch:** `hobbyroom/project-memory-campus-v1-20260905`.
**Speicherort:** `protocol/PROJECT_MEMORY/PROJEKTE/EIGENTUMSSCHUTZ/PLUGINS/ISOLIERTE_PLUGINS/<ID>/CURRENT.zip`.

- **HAB-001-DESIGN:** Version **0.1.184**. Originale vollständige `CURRENT.zip`, **84.339.643 Bytes**, Git-Blob `e153339c967cabcc4953ed6fb0882d9792b622fe`, SHA-256 `76043e5c093058a4d8aff8fd6642307cade951c8267641dc710b8ed70cd323e3`. 426 ZIP-Einträge und CRC PASS. GitHub-Actions-Run **41687120534** erfolgreich; **PR #625** am 03.11.2026 gemergt. Das offizielle GitHub-Verzeichnis bestätigt Größe und Blob-SHA.
- **HAB-002-KATEGORIE-WORKFLOW:** Version **1.14.8.37**. Originale vollständige `CURRENT.zip`, **368.530 Bytes**, Git-Blob `35651f44ac70ed51e663d5dfaf45094bc9f1e3b2`, SHA-256 `ec39080e5350b9f7b3924239376e11580ce7de195a60bb89feafae6152533f98`. 49 ZIP-Einträge und CRC PASS; **PR #622** gemergt. GitHub-Größe und Blob-SHA bestätigt.
- **HAB-003-BILDZENTRALE:** Version **1.0.0**. Originale vollständige `CURRENT.zip`, **70.397 Bytes**, Git-Blob `8b8b3b84b494eb2784181d5bfd6acfb2efceafde`, SHA-256 `58af0d394752e767b5f0c7d6d9901eeaec921331ab6245144859e3e6626e4559`. 3 ZIP-Einträge und CRC PASS; **PR #622** gemergt. GitHub-Größe und Blob-SHA bestätigt.

**Belege:** https://github.com/hallo-netizen/affiliate-pferdeportal/pull/622 · https://github.com/hallo-netizen/affiliate-pferdeportal/pull/625 · https://github.com/hallo-netizen/affiliate-pferdeportal/actions/runs/41687120534

**Versionsautorität:** `PLUGIN_AKTEN/<ID>/CURRENT.md` für jedes Plugin. Vollständiges Original unter `ISOLIERTE_PLUGINS/<ID>/CURRENT.zip`. Manifestdateien sind nur Prüfnachweise. Die 71 Design-Übertragungsteile gehören zum separaten Staging, nicht zum offiziellen Pluginbüro; die vollständige Original-ZIP wurde inzwischen erfolgreich übernommen. Deshalb **keine weiteren Design-Teile zur Vervollständigung nötig**.

**Status: PLUGINABLAGE ABGESCHLOSSEN (3/3).** Die WordPress-Liveinstallation ist dadurch **nicht** geprüft oder freigegeben. Keine Änderungen an WordPress, K0 oder anderen Portalen.

**NEXT ACTION:** Keine weiteren Archivübertragungen erforderlich. Eine spätere WordPress-Liveprüfung ist ein gesonderter Auftrag.
