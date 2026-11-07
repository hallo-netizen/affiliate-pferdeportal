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

## 07.11.2026 – HAB Affiliate AMAZON RC8: geprüfter kompletter Workflow, echte Diagnose und Ausgabe

**07.11.2026 – HAB-004 Affiliate-Zentrale 0.1.5-rc8 ist einzige aktuelle Voll-ZIP:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **620242 Bytes**, 28 ZIP-Dateien, SHA256 `f2d09e649fbb6a69a54e64b01df239013975999e46921f08b722adff139ccd30`, Git-Blob `35d32677fb7232a8c0891cc0e730b4b02851b945` (bei GitHub binär geprüft).

**Vollständige lokale Workflow-Simulation: 234 bestandene Prüfungen, 25/25 PHP-Syntax, ZIP-CRC 28/28; nur 3/28 Originaldateien verändert** (`affiliate-portal-router.php`, `includes/trait-ppar-hb-amazon.php`, `readme.txt`). RC7 hatte beim echten Screenshot nach manuellem Run null Kandidaten, aber irreführend bloß „Keine neuen passenden Produkte“. Nachstellung mit den originalen aktiven Hab-Quelladapter-Klassen beweist: bei fehlendem/falschem/inhaltlich nicht freigegebenem WP-Kategoriebaum wurde dessen WP_Error als leere Kandidatenliste verschluckt. Zudem vorherige RC7-Simulation des Frontends hatte einen falschen Kategorie-Slot und ignorierte leere Kategorien/Produktseiten. RC8 zeigt direkt nach Klick oben den echten Workflow- und Kategoriebaum-/Provider-Status und lässt DataForSEO bei ungültiger Quelle gesperrt; echte DataForSEO-API-Taskfehler werden erkannt, statt als unendliches „noch in Bearbeitung“ zu gelten. Wiederverwendung des bestehenden Workers, API-Kostenlimits und Slots, plus die vorhandenen Hab-Design-/Kategorie-Hooks für Amazon-Affiliate-Links auf relevanten Produktseiten selbst ohne redaktionelle Beiträge. Bereits vorhandene Werbung hat Vorrang. Keine zweite DB, kein zweiter Cron, keine Fremdportale/K0 verändert.

**Ehrliche Testgrenze:** Die originalen vollständigen Hab-Plugin-Dateien inkl. originalem Portal-Quelladapter und originalem Design-Plugin-Hook wurden offline mit nachgestellten WordPress-Optionen und DataForSEO-API-Antworten ausgeführt; **keine echte WordPress-Produktivabnahme, keine kostenpflichtige Provider-Abfrage, kein Einblick in Live-Kategoriebaum-Optionen**. RC8 zeigt die genaue Quelle des noch offenen Live-Blockers erst nach Installation.

**Nächster Schritt:** Auf Hab-&-Bewahr-WordPress das bestehende HAB-004-Affiliate-Plugin durch diese RC8-Voll-ZIP ersetzen, `Affiliate-Zentrale → Amazon-Automatik → Jetzt einen Suchlauf starten` **einmal** drücken, dann die **oben sichtbare Statusbox** prüfen. Kein wiederholtes blindes Klicken; bis zu 5 neu bezahlte DataForSEO-Aufträge je UTC-Tag. Falls Quelle blockiert, dort die genaue Ursache lesen statt neue Suche zu behaupten.

Details und Reproduktionsnachweis: `RC8_WORKFLOW_SIMULATION_20261107.md`. Vorherige RC7-Nennungen darunter nur Historie.

---

## 07.11.2026 – HAB-004 RC7: automatische Amazon-Recherche für neue Beiträge

**HAB-004 Affiliate-Zentrale 0.1.4-rc7**, vollständige einzige `CURRENT.zip`: **616209 Bytes, 28 Dateien**, ZIP-SHA256 `08725e5cf9d18654345b4b18b9f3c63ade54ce7a6da932d9768bc2b9867b1d6e`, GitHub-Binär-Blob `3df1bd941aa051f6706a66fd857a8745d0209420`. Gegen RC6 25/28 Dateien byteidentisch; nur die vorhandene Amazon-Datei, der bisherige Hab-Router und `readme.txt` geändert. Keine Fremdportale.

**Nach Prüfung des wirklichen RC6-Codes:** Die vorhandene Artikelerkennung und Werbeplan-Neuberechnung bei Speicherung blieb unangetastet. Neu nutzt **derselbe DataForSEO-Worker** künftig auch veröffentlichte Artikel, wenn die direkte Hab-Produktkategorie wirklich passt und der Artikel-Titel die konkrete Produktfamilie nennt. Bewusste Ausschlüsse: Entwürfe, allgemeine Ratgeber ohne explizites Produkt, Werbesperren, falsche Produktfamilien. Änderungen an Titel/Kategorie machen alte Treffer sofort ungültig. Alle aktuellen Produkt-/Bannerkampagnen behalten Vorrang; bei fehlenden passenden Produkten nur klar gekennzeichneter Amazon-Suchlink, nach verifiziertem API-Ergebnis reale Amazon-Textlinks. Kein zweiter Worker, keine neue API-Suche beim Beitragsspeichern und keine zusätzliche Datenbank; fünf bezahlte DataForSEO-Aufträge/UTC-Tag bleiben.

**Tests:** Alle 25 PHP-Dateien ohne Syntaxfehler, ZIP-CRC PASS, 23+16+23+34 lokale Assertions PASS (96 nicht notwendigerweise unabhängige Fälle). Echte Artikel-Produktslot-Funktion aus Original-Hauptdatei mit globaler Sperre, bestehender Werbung und Hybrid-/Legacy-Modus geprüft. **Kein** WordPress-/DataForSEO-/echter Produktiv-End-to-End-Test; Portal enthält derzeit noch keine echten Beiträge. RC7 bleibt ein geprüftes Upgrade-Paket, nicht produktiv abgenommen.

Arbeits- und Testnachweise ausschließlich im eigenen Hab-Affiliatebüro: `IMPLEMENTIERUNG_RC7/`. RC6 und ältere Angaben sind historisch.

**Nächster Schritt:** Auf ausschließlich `hab-und-bewahr.de` das bereits vorhandene HAB-004 mit der RC7-ZIP kontrolliert aktualisieren. Amazon-Partner-ID und gespeicherte Zugangsdaten bleiben über dieselben bestehenden WordPress-Optionen erhalten, deren tatsächliches Fortbestehen nach dem Upgrade zu prüfen ist. Beim nächsten real veröffentlichten, korrekt kategorisierten Produktbeitrag erfolgt die themenbezogene Suche über den bestehenden WP-Cron. Keine manuellen Amazon-Einzelkampagnen, keine neuen Plugins. HAB-001/002/003, Pferdeatelier, Hobbydepot und K0 unverändert.

---

## 07.11.2026 – HAB AMAZON RC6: STARTKNOPF UND EIGENSTÄNDIGE KATEGORIERECHERCHE

**Stand 07.11.2026 – einzige aktuelle HAB-004-Voll-ZIP 0.1.3-rc6:** `CURRENT.zip` 618.152 Bytes, 28 Dateien, SHA-256 `ef51d931d0c104e8cbb1ed0b27d33e0b6855c1202e605fe06440afc50d0574b9`, Git-Blob `c9026cbcfaa44a03a69820d9d35207f8b6ce5c27` (Größe und Hash aus echtem GitHub-Binärarchiv geprüft).

**Nachgewiesene Ursache aus dem RC5-Quellcode:** kein manueller Start; erster WP-Cron-Lauf erst nach mindestens 5 Minuten plus Website-Aufruf; DataForSEO-Kandidatensuche ausschließlich bei bereits aktiven eBay-/idealo-Produktkampagnen, obwohl Hab diese Anbieter noch nicht eingerichtet hat. Dass der WP-Cron eingetragen ist, beweist keinen tatsächlichen Suchlauf. **RC6:** im selben vorhandenen Hab-Amazon-Modul ein authentifizierter Admin-Button `Jetzt einen Suchlauf starten` an **denselben** vorhandenen Worker angebunden; stündlicher WP-Cron unverändert. Bei fehlenden eBay-/idealo-Kandidaten werden ausschließlich nachweislich im aktiven Hab-Zielkatalog vorhandene konkrete Produktfamilien recherchiert. DataForSEO-Ergebnisse werden nur bei organischen Amazon.de-Produktlinks, gültiger ASIN und im Titel tatsächlich genannter Produktfamilie als maximal 3 schlichte Textlinks pro Kategorie in **bereits vorhandenem Banner-Slot** zugelassen. Keine erfundenen Produktkarten, keine Bilder/Preise/Bewertungen oder Lagerbehauptungen. Bestehende Kampagne hat Vorrang. Ungültige/fremde Treffer bleiben gesperrt. Keine zweite Produktdatenbank, kein neues Plugin.

**Belege/Grenzen:** 25/25 PHP-Syntaxprüfungen, vollständiger ZIP-CRC, 62 lokale Positiv-/Negativprüfungen in drei Testdateien, 25/28 RC5-Dateien byteidentisch (neu geschrieben nur `affiliate-portal-router.php` Version, `includes/trait-ppar-hb-amazon.php`, `readme.txt`). Kein echter WordPress-/DataForSEO-/Amazon-Produktivtest und keine Ausführung kostenpflichtiger API-Abfragen durch den Build. Bestehende Einstellungen beim WordPress-Update sollen erhalten bleiben; unverändert bleiben auch HAB-001/002/003, Pferdeatelier, Hobbydepot, K0. In der WordPress-Sitzung müssen tatsächliche DataForSEO-Zugangsdaten gespeichert und die Amazon-Automatik aktiv sein. Maximal 5 neue kostenpflichtige POST-Suchaufträge pro UTC-Tag auch beim manuellen Start; offener Auftrag wird lediglich per kostenlosem GET abgefragt.

Arbeitsbelege im eigenen Büro: `IMPLEMENTIERUNG_RC6/RC5_TO_RC6.patch` und `IMPLEMENTIERUNG_RC6/test_hab_rc6.php`; RC5/RC4 nur historische Belege.

**NÄCHSTER SCHRITT:** Bestehende Hab-&-Bewahr-Affiliate-Zentrale in WordPress durch die neue RC6-ZIP ersetzen. `Affiliate-Zentrale → Amazon-Automatik → Jetzt einen Suchlauf starten` einmal klicken. Danach zeigt dieselbe Seite **Letzter tatsächlicher Lauf**, **Letzte Meldung**, **Offener Auftrag**, **gefundene Einzelproduktlinks** und **bezahlte Suchaufträge heute**. Kein zweites Plugin. Ein neuer Suchauftrag kostet DataForSEO-Guthaben. Ein Ergebnis kann erst bei einem späteren Worker-Durchlauf eintreffen. Nach echten Daten prüfen, ob die globale Affiliate-Ausspielung und die Kategorie-Slots aktiviert sind; keine Live-Ausgabe vorher behaupten.

---

## 07.11.2026 – HAB-004 RC5: AMAZON-DATENFELD + AUTOMATISCHE SUCHLINKS KORRIGIERT

**Version 0.1.2-rc5 (07.11.2026), allein HAB-004:** Voll-ZIP `CURRENT.zip` 616.662 Bytes, 28 Dateien, SHA-256 `84b4c071f69c6da3e6a3a92dac519ced45a9ba331b09f9d395914a96baa3a7c7`, Git-Blob `13ecb1aa84e1050f4c7fc53a06c32e6c9369a2d6` (GitHub-Ordner: Größe/Blob unabhängig abgeglichen). RC4 aus PR #664 bleibt über Git-Historie wiederherstellbar.

**Gezielte RC4-Korrektur:** Der DataForSEO-Merchant-Amazon-Products-Endpunkt liefert die Kennung als `data_asin`; RC4 las nur `asin`. RC5 liest das tatsächliche `data_asin` und prüft zusätzlich Amazon-Domain, exakten Titel, eindeutige Kennung, Packungsvarianten und keine bezahlten Treffer. Wenn noch kein eBay-/idealo-Produktkatalog existiert, wird **nur für reale Produktfamilien-Kategorien aus dem eigenen Hab-Workflow**, und nur im vorhandenen Banner-Slot `product_after_category_tiles`, ein einfacher automatischer Amazon-Suchlink erzeugt (mit `habundbewahr-21`, Anzeige-/Werbelinkkennzeichnung). Keine erfundene Amazon-Produktkarte, kein zweiter Bannermotor, keine Bilder/Preise/Bewertungen aus DataForSEO. Vorhandene Werbekampagne hat Vorrang. Für echte Einzelprodukt-Direktkarten benötigt der bestehende DataForSEO-Worker weiterhin ein vorhandenes freigegebenes eBay-/idealo-Ausgangsprodukt.

**Tests:** 25/25 PHP-Syntaxprüfungen, ZIP-CRC 28/28, 40 lokale Positiv-/Negativtests (darunter 16 neue RC5-Fälle), 25 originale RC3-Dateien unverändert. Keine authentifizierte WordPress-/Provider-Liveprüfung; DataForSEO kostet bei eingeschalteter Recherche, max. fünf neue Tasks je UTC-Tag. Die gesamte Automatik ist standardmäßig aus. Keine Änderungen an HAB-001/002/003, Pferdeatelier, Hobbydepot, K0 oder externen Zugangsdaten.

**Nächster Schritt:** Nur die bestehende Hab-Affiliate-Zentrale in WordPress kontrolliert mit RC5 aktualisieren. `Affiliate-Zentrale → Amazon-Automatik`: Tag `habundbewahr-21` speichern, Amazon-Produktbuttons aktivieren; DataForSEO noch aus lassen. Erst echten Kategorien-Suchlink mit eigener Tracking-ID prüfen, danach die kostenpflichtige DataForSEO-Suche getrennt freigeben und Datenbasis für konkrete Produktkarten prüfen.

Quellpatch/Test der gezielten RC5-Korrektur: `IMPLEMENTIERUNG_RC5/`.

---

## 07.11.2026 – AMAZON-AUTOMATIK RC4 IM EIGENEN HAB-PLUGIN IMPLEMENTIERT

HAB-004 0.1.1-rc4: vollständige CURRENT.zip, 616072 Bytes, 28 Einträge, SHA256 c601c1f540fccdd18dde59b7c15fc55cfe53b68a59459d45182a2cf1bcd55017, Git-Blob f3a77efff2cb16de34c91eb0c4ec3b072a3999db (remote Größe und Blob bytegleich geprüft).

Original: Hab-RC3, 27 Dateien. Von deren Dateien 25 byteidentisch, geändert Haupt-PHP und includes/trait-ppar-idealo.php, hinzugefügt includes/trait-ppar-hb-amazon.php. Existing Banner-, Frontend-, Produktkarten-, Ausgabe- und Artikelplandateien unberührt. DataForSEO: Opt-in, stündliche WP-Cron-Verarbeitung, max. 5 kostenpflichtige POSTs/UTC-Tag, gespeicherte offene task-ID, eindeutiger Variantenabgleich. Amazon: eigene Tracking-ID habundbewahr-21 ausschließlich nach Speicherung/Aktivierung; direkte Links nur für belegte einzelne ASIN aus idealo oder streng geprüfte DataForSEO-Treffer. Kein eigener manueller Amazon-Kampagnenweg. Alte fremde idealo-Defaults (Adspace 568313, Feed 2901) aus Hab entfernt/gesperrt. Keine Fremd-Provider-Zugangsdaten übertragen.

Lokal geprüft: PHP Syntax 25/25, 24 Assertions (Positiv/Negativ, Variantenabweichung, falsche Portal-ID, bezahlter POST vs kostenloser GET, Tagesgrenze, keine doppelten Buttons), ZIP CRC, installierbare Original-Pluginwurzel, 25/27 originale Dateien bytegleich. Keine authentifizierte WordPress-Installation oder echte Provider-Verbindung und keine Google-/Frontend-Liveprüfung; nur ein Upgrade-Testkandidat. Die Standardautomatik bleibt deaktiviert.

Arbeitsquelle, exakter Zwei-Dateien-Patch und ausführbarer Regressionstest: IMPLEMENTIERUNG_RC4/. Original-Pferdeatelier und Hobbydepot wurden ausschließlich als Recherchevorbild betrachtet, nicht modifiziert.

Nächster Schritt: nur das bestehende Hab-004-WordPress-Plugin mit CURRENT.zip aktualisieren; Affiliate-Zentrale → Amazon-Automatik öffnen; habundbewahr-21 speichern, Amazon-Produktbuttons einschalten; eigene DataForSEO-Zugangsdaten erst nach Kostenfreigabe eingeben; an einer echten passenden Produktkarte Ziel/Tracking und Slot prüfen. Pferdeatelier und Hobbydepot/K0 unverändert.

---

## 07.11.2026 – HARTER AMAZON-/DATAFORSEO-RC3-ABGLEICH (NACH ORIGINAL-ZIP)

**Prüfbeleg:** [AMAZON_AUTOMATIK_ABGLEICH_20261107.md](AMAZON_AUTOMATIK_ABGLEICH_20261107.md).

**Ergebnis:** Die amtliche Hab-004-RC3-ZIP (605.196 B, SHA `2e5f6790...`) hat die generischen idealo-/Banner-/Output-Wege, aber **kein** DataForSEO-Modul und keine aktive Amazon-Produktrecherche. Die vorhandene Amazon-Providerkarte ist `prepared`, nicht `active`. Die Anwenderforderung bleibt ausdrücklich **vollautomatisch**, **keine** manuellen Einzelkampagnen. PartnerNet-Website und separate Hab-Tracking-ID sind vorhanden. Die ältere Pferdeatelier-Referenz weist eine spätere DataForSEO-/Amazon-Automatik nach; ihre vollständigen Originalbytes waren in diesem Durchlauf trotz Bibliotheksnachweis nicht exportierbar. **Kein ungeprüftes Wiederprogrammieren oder RC4 auf Vermutung.**

**NEXT ACTION:** Vollständiges zugängliches originales Pferdeatelier-Affiliate-ZIP mit Amazon-Automatik gegen eigenständige Hab-RC3-Quelle vergleichen, nur fehlende allgemein wiederverwendbare Funktionen isoliert portieren und vollständig samt WP-/Negativ-/Tracking-Gates testen. Bis dahin keine Pluginaktualisierung und keine Aktivierung von Amazon-Produktanzeigen. eBay/Pferdeatelier/Hobbydepot unverändert.

---

## 07.11.2026 – AMAZON-/EBAY-EINRICHTUNGSSTAND (AKTUELLE OPERATIVE FORTSETZUNG)

**Verbindlicher Gesprächs-/Kontostand:** [SETUP_EBAY_AMAZON_BANNER_20261107.md](SETUP_EBAY_AMAZON_BANNER_20261107.md). Amazon-Tracking-ID für Hab & Bewahr laut Nutzer **bereits angelegt**; Website-Liste und Anbindung im WP-Plugin noch zu prüfen. Amazon im Plugin „Adapter vorbereitet“, nicht live verbunden. Eigene breite/quadratische Banner sind Designentwürfe, noch keine Produktions-/Amazon-Freigabe. eBay: eigene Hab-EPN-Kampagne im Plugin gespeichert; Zusatz-Keysets für Hobby Depot und Hab & Bewahr beantragt, Ticket 261106-000039, eBay-Rückfrage zur Begründung, Antwortversand noch unbestätigt. **Pferdeatelier-/Hobbydepot-Developer-Einstellungen und Plugins nicht verändern.**

**NEXT ACTION:** Amazon PartnerNet → Kontoeinstellungen → Website-Liste bearbeiten: `hab-und-bewahr.de` auf Vorhandensein prüfen. Tracking-ID nicht noch einmal erstellen; danach einen Testlink ausschließlich mit Hab-Tracking-ID erzeugen. Keine automatische Auslieferung einschalten. Der folgende RC3-Stand bleibt die autoritative Plugin-Basis.

---

## 06.11.2026 – RC3 BEREINIGUNG / OFFIZIELLE HAB-004-PLUGINABLAGE

**Neue gültige Version:** 0.1.0-rc3, vollständige ZIP im ursprünglichen `../PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip` (605.196 Bytes; SHA-256 `2e5f6790ab3a64b446e34d132037684ad8fa637f76f43974e2816a1f75bc11eb`). RC2 unten ist nur Historie.

**Ursache und Korrektur:** Die RC2-Produktlistenprüfung bezog sich ausschließlich auf Produktbegriffe in Seitenüberschriften. Der tatsächliche Design-Kategoriebaum liegt in der bestehenden WordPress-Zielrevision mit 6 Schutzwelten. In RC3 werden 285 Artikelkategorien und 13 klar benannte Produktprofile aus dem offiziellen Design-Nodes-Stand erkannt; nicht pauschal jedes Sicherheitsthema als Produkt deklariert. Die Werbung nutzt die echten gemappten WP-Zielseiten, nie die Pferde- oder Hobby-Quellkataloge. Welt-/Unterbereich-/Magazin-/Anzeigenmarkt- und Artikel-Brücken nach tatsächlichen Designfiltern, 92 reale Boot-Hooks, 24/27 Dateien gegenüber RC2 unverändert, keine Funktionen aus neutraler Engine gelöscht.

**Performance mit Beleg:** Einmaliger, pro Seitenaufruf zwischengespeicherter WP-Seitenindex ersetzt wiederholtes Durchsuchen des gesamten Zielbaums. Keine unbelegte globale Laufzeitverbesserung behauptet. ZIP-Bau zweimal identisch, alle PHP/JS-Tests, 546 Design-Knoten als Testkorpus, negative und positive Tests, SHA + unabhängiger GitHub-Readback PASS (GitHub Run 42252394077).

**Restgrenzen:** noch kein echter WordPress-/Provider-Livetest; eBay-Quellstand 6.72.306 als 66-Datei-Referenz nicht physisch im Hab-Büro, daher keine zugesagte vollständige Parität; Glossar-Einzelseiten ohne echte CPT-Zielbindung bleiben sicher leer statt erfundene Werbung zu zeigen. Automatische Affiliate-Ausgabe standardmäßig inaktiv.

---

## 06.11.2026 – HAB-004 AFFILIATE – ISOLIERTER WORDPRESS-RELEASE 0.1.0-rc2
<!-- HAB_AFFILIATE_RC2_20261106 -->
**Neue Ausgabe im zuständigen eigenen Pluginbüro:** `../PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, 27 Dateien, 603.323 Bytes, SHA-256 `014e42b9657eed74b4d2e1f29ea51c6c6bf5c276ec30402011289b3821cbe153`. Build und Prüfquellen ausschließlich auf isoliertem Zweig `hbd-affiliate-port-20261106` in `AFFILIATE/HAB_BAU`; unveränderter fachlicher Originalstamm `NEUTRAL_STAMM` bleibt erhalten.

**Belegt:** Vollständiger neutraler 26-Dateien-Grundstock mit eBay, idealo, Awin, ADCELL, Digistore24, Tarifen, Werbebannern, manuellen Kampagnen, Affiliate-Automatisierung, Chefsteuerung, Ausgabeobjekten, Produktkarte und Artikelplanung erhalten. PHP-Signaturen der 26 Originaldateien nicht entfernt. Fünf vorhandene Zusatzmodule (Produkt-Source-Plan, Admin KISS, Deal-Radar, Partneranalytik, DS24-Nachverarbeitung) waren in neutraler Quelle nicht am Bootstrap angebunden; im neuen Paket geprüft gestartet. Alle Horse-/Hobby-Designreferenzen aus Installationscode entfernt; Hab-Adapter liest nur aktive, passende WordPress-Revision aus Kategorie-Workflow. Anbindung an HBDP-Artikel-/Bereichsfilter (Design 0.1.189) und fail-closed ohne Kategorievertrag. 27/27 ZIP CRC, alle PHP-Lints, JS Syntax, echte Start-Hooks (90), Positiv-/Negativkatalogtests sowie unabhängig über frischen GitHub-Klon erneut gelesene ZIP: **LOCAL PASS** (GitHub-Run 42246580133).

**Harte Grenzen:** Vollständiges Pferdeatelier 6.72.306 Paket mit 66 Files / 5.343.938 Bytes ist lediglich als Referenz beschrieben und befindet sich nicht als Vollarchiv im Hab-Büro. Deshalb **keine behauptete volle Versions-/Featuregleichheit zu 6.72.306**; belegt ist die neutrale Stammfunktions-Erhaltung. Kein realer WordPress-/Provider-/eBay-API-/HivePress-Livetest und keine Lastmessung im Live-Hosting. Kein belegter genereller Performancefehler, daher keine blind gelöschten Alt- oder Sicherungsfunktionen. Standardeinstellung Auslieferung deaktiviert. Der neue Hab-Katalog benötigt aktive WP-Kategorien, echte veröffentlichte Produktziele und kann andernfalls leer bleiben.

**NEXT ACTION (einziger freigegebener operativer Schritt):** Hab-Plugin als neue, bereits separat benannte Instanz unter `affiliate-portal-router` auf Hab-&-Bewahr-WordPress kontrolliert installieren, aktivieren, im Backend Ist-Zustand/Partner-Sperre prüfen. Erst nach klarem WordPress-Readback Providerdaten neu für Hab & Bewahr hinterlegen und Tests durchführen. K0 und alle anderen Projekte unverändert.

---

# HAB & BEWAHR – AFFILIATE CURRENT

STAND: 2026-10-26
STATUS: NEUTRALER STAMM GESICHERT / NO LIVE PASS / HAB-&-BEWAHR-ANPASSUNG NOCH OFFEN

## Verbindlicher Stand

Für Hab & Bewahr wurde ein eigenes Affiliate-Büro angelegt.

Gesicherte technische Ausgangsbasis:
`NEUTRAL_STAMM/affiliate-portal-router/`

Der Stamm basiert auf der bereits pferdeatelier-bereinigten HD-009-Engine, wurde aber vor Ablage hier zusätzlich von Hobby-Depot-spezifischer Bindung getrennt.

Entfernt bzw. neutralisiert wurden insbesondere:
- Hobby-Depot-Pluginidentität und Routerklassenbindung
- HD-004-Kategorie-/Zielquellenbindung
- HD-003/Hobby-Depot-Designprofilbindung
- fest verdrahtete Hobby-Depot-Slotmatrix
- Hobby-Depot-spezifische eBay-/idealo-Zieltexte, Defaults und Zielquellenklassen
- Hobby-Depot-spezifische Provider-/Deal-Radar-Bezeichnungen

Erhalten wurden:
- allgemeine Affiliate-Engine
- eBay- und idealo-Providerlogik
- Awin / ADCELL / Digistore24 / Direktpartner-Basis
- Kontroll-, Veto-, Output- und Automationslogik
- bestehende Credential-/Konfigurationsschnittstellen

Zugangsdaten sind nicht im Campus gespeichert.

## Wichtig

Der neutrale Stamm ist **keine installierbare Hab-&-Bewahr-Livefreigabe**.
Die Portal-Zielquelle ist absichtlich ungebunden und fail-closed.

## Herkunft

Hobby-Depot-Arbeitsquelle:
`hobbyrausch/hd009-affiliate-port-20261026`
Head bei Ableitung:
`56b91b171cb68129369b67e411da5345957af4f2`

Die Hobby-Depot-Entwicklung bleibt davon getrennt und wird nicht zurückgesetzt.

## NEXT ACTION

Für den späteren Hab-&-Bewahr-Chat:

1. Hab-&-Bewahr-Zielquelle aus dem zuständigen Kategorie-/Portal-Current anbinden.
2. Hab-&-Bewahr-Design-/Slotvertrag separat anbinden.
3. Portalnamen und projektspezifische Defaults setzen.
4. Positiv-, Negativ-, Regression-, Installations- und Runtimeprüfung durchführen.
5. Erst danach einen Hab-&-Bewahr-Installationskandidaten bauen.

Nicht HD-004 übernehmen. Nicht Hobby-Depot-Slotmatrix übernehmen. Nicht wieder aus Pferdeatelier kopieren.
