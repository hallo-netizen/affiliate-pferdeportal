## 07.11.2026 – HAB-004 RC7 (neue einzige technische Current)

**HAB-004 Affiliate-Zentrale 0.1.4-rc7**, vollständige einzige `CURRENT.zip`: **616209 Bytes, 28 Dateien**, ZIP-SHA256 `08725e5cf9d18654345b4b18b9f3c63ade54ce7a6da932d9768bc2b9867b1d6e`, GitHub-Binär-Blob `3df1bd941aa051f6706a66fd857a8745d0209420`. Gegen RC6 25/28 Dateien byteidentisch; nur die vorhandene Amazon-Datei, der bisherige Hab-Router und `readme.txt` geändert. Keine Fremdportale.

**Nach Prüfung des wirklichen RC6-Codes:** Die vorhandene Artikelerkennung und Werbeplan-Neuberechnung bei Speicherung blieb unangetastet. Neu nutzt **derselbe DataForSEO-Worker** künftig auch veröffentlichte Artikel, wenn die direkte Hab-Produktkategorie wirklich passt und der Artikel-Titel die konkrete Produktfamilie nennt. Bewusste Ausschlüsse: Entwürfe, allgemeine Ratgeber ohne explizites Produkt, Werbesperren, falsche Produktfamilien. Änderungen an Titel/Kategorie machen alte Treffer sofort ungültig. Alle aktuellen Produkt-/Bannerkampagnen behalten Vorrang; bei fehlenden passenden Produkten nur klar gekennzeichneter Amazon-Suchlink, nach verifiziertem API-Ergebnis reale Amazon-Textlinks. Kein zweiter Worker, keine neue API-Suche beim Beitragsspeichern und keine zusätzliche Datenbank; fünf bezahlte DataForSEO-Aufträge/UTC-Tag bleiben.

**Tests:** Alle 25 PHP-Dateien ohne Syntaxfehler, ZIP-CRC PASS, 23+16+23+34 lokale Assertions PASS (96 nicht notwendigerweise unabhängige Fälle). Echte Artikel-Produktslot-Funktion aus Original-Hauptdatei mit globaler Sperre, bestehender Werbung und Hybrid-/Legacy-Modus geprüft. **Kein** WordPress-/DataForSEO-/echter Produktiv-End-to-End-Test; Portal enthält derzeit noch keine echten Beiträge. RC7 bleibt ein geprüftes Upgrade-Paket, nicht produktiv abgenommen.

**Nächster Schritt:** Auf ausschließlich `hab-und-bewahr.de` das bereits vorhandene HAB-004 mit der RC7-ZIP kontrolliert aktualisieren. Amazon-Partner-ID und gespeicherte Zugangsdaten bleiben über dieselben bestehenden WordPress-Optionen erhalten, deren tatsächliches Fortbestehen nach dem Upgrade zu prüfen ist. Beim nächsten real veröffentlichten, korrekt kategorisierten Produktbeitrag erfolgt die themenbezogene Suche über den bestehenden WP-Cron. Keine manuellen Amazon-Einzelkampagnen, keine neuen Plugins. HAB-001/002/003, Pferdeatelier, Hobbydepot und K0 unverändert.

Quellvergleich, reproduzierbarer PHP-Gegentest und ausführliche Prüfung: `../../../AFFILIATE/IMPLEMENTIERUNG_RC7/RC6_TO_RC7.patch`, `test_hab_rc7.php`, `TESTRESULTS.md`. Vorgängerversion RC6 bleibt in der Git-Historie zur Verfügung.

---

## 07.11.2026 – RC6: Ersten Amazon-Suchlauf starten, ohne eBay/idealo

**Stand 07.11.2026 – einzige aktuelle HAB-004-Voll-ZIP 0.1.3-rc6:** `CURRENT.zip` 618.152 Bytes, 28 Dateien, SHA-256 `ef51d931d0c104e8cbb1ed0b27d33e0b6855c1202e605fe06440afc50d0574b9`, Git-Blob `c9026cbcfaa44a03a69820d9d35207f8b6ce5c27` (Größe und Hash aus echtem GitHub-Binärarchiv geprüft).

**Nachgewiesene Ursache aus dem RC5-Quellcode:** kein manueller Start; erster WP-Cron-Lauf erst nach mindestens 5 Minuten plus Website-Aufruf; DataForSEO-Kandidatensuche ausschließlich bei bereits aktiven eBay-/idealo-Produktkampagnen, obwohl Hab diese Anbieter noch nicht eingerichtet hat. Dass der WP-Cron eingetragen ist, beweist keinen tatsächlichen Suchlauf. **RC6:** im selben vorhandenen Hab-Amazon-Modul ein authentifizierter Admin-Button `Jetzt einen Suchlauf starten` an **denselben** vorhandenen Worker angebunden; stündlicher WP-Cron unverändert. Bei fehlenden eBay-/idealo-Kandidaten werden ausschließlich nachweislich im aktiven Hab-Zielkatalog vorhandene konkrete Produktfamilien recherchiert. DataForSEO-Ergebnisse werden nur bei organischen Amazon.de-Produktlinks, gültiger ASIN und im Titel tatsächlich genannter Produktfamilie als maximal 3 schlichte Textlinks pro Kategorie in **bereits vorhandenem Banner-Slot** zugelassen. Keine erfundenen Produktkarten, keine Bilder/Preise/Bewertungen oder Lagerbehauptungen. Bestehende Kampagne hat Vorrang. Ungültige/fremde Treffer bleiben gesperrt. Keine zweite Produktdatenbank, kein neues Plugin.

**Belege/Grenzen:** 25/25 PHP-Syntaxprüfungen, vollständiger ZIP-CRC, 62 lokale Positiv-/Negativprüfungen in drei Testdateien, 25/28 RC5-Dateien byteidentisch (neu geschrieben nur `affiliate-portal-router.php` Version, `includes/trait-ppar-hb-amazon.php`, `readme.txt`). Kein echter WordPress-/DataForSEO-/Amazon-Produktivtest und keine Ausführung kostenpflichtiger API-Abfragen durch den Build. Bestehende Einstellungen beim WordPress-Update sollen erhalten bleiben; unverändert bleiben auch HAB-001/002/003, Pferdeatelier, Hobbydepot, K0. In der WordPress-Sitzung müssen tatsächliche DataForSEO-Zugangsdaten gespeichert und die Amazon-Automatik aktiv sein. Maximal 5 neue kostenpflichtige POST-Suchaufträge pro UTC-Tag auch beim manuellen Start; offener Auftrag wird lediglich per kostenlosem GET abgefragt.

**NÄCHSTER SCHRITT:** Bestehende Hab-&-Bewahr-Affiliate-Zentrale in WordPress durch die neue RC6-ZIP ersetzen. `Affiliate-Zentrale → Amazon-Automatik → Jetzt einen Suchlauf starten` einmal klicken. Danach zeigt dieselbe Seite **Letzter tatsächlicher Lauf**, **Letzte Meldung**, **Offener Auftrag**, **gefundene Einzelproduktlinks** und **bezahlte Suchaufträge heute**. Kein zweites Plugin. Ein neuer Suchauftrag kostet DataForSEO-Guthaben. Ein Ergebnis kann erst bei einem späteren Worker-Durchlauf eintreffen. Nach echten Daten prüfen, ob die globale Affiliate-Ausspielung und die Kategorie-Slots aktiviert sind; keine Live-Ausgabe vorher behaupten.

---

## 07.11.2026 – HAB-004 RC5 (einzige aktuelle technische Version)

**Version 0.1.2-rc5 (07.11.2026), allein HAB-004:** Voll-ZIP `CURRENT.zip` 616.662 Bytes, 28 Dateien, SHA-256 `84b4c071f69c6da3e6a3a92dac519ced45a9ba331b09f9d395914a96baa3a7c7`, Git-Blob `13ecb1aa84e1050f4c7fc53a06c32e6c9369a2d6` (GitHub-Ordner: Größe/Blob unabhängig abgeglichen). RC4 aus PR #664 bleibt über Git-Historie wiederherstellbar.

**Gezielte RC4-Korrektur:** Der DataForSEO-Merchant-Amazon-Products-Endpunkt liefert die Kennung als `data_asin`; RC4 las nur `asin`. RC5 liest das tatsächliche `data_asin` und prüft zusätzlich Amazon-Domain, exakten Titel, eindeutige Kennung, Packungsvarianten und keine bezahlten Treffer. Wenn noch kein eBay-/idealo-Produktkatalog existiert, wird **nur für reale Produktfamilien-Kategorien aus dem eigenen Hab-Workflow**, und nur im vorhandenen Banner-Slot `product_after_category_tiles`, ein einfacher automatischer Amazon-Suchlink erzeugt (mit `habundbewahr-21`, Anzeige-/Werbelinkkennzeichnung). Keine erfundene Amazon-Produktkarte, kein zweiter Bannermotor, keine Bilder/Preise/Bewertungen aus DataForSEO. Vorhandene Werbekampagne hat Vorrang. Für echte Einzelprodukt-Direktkarten benötigt der bestehende DataForSEO-Worker weiterhin ein vorhandenes freigegebenes eBay-/idealo-Ausgangsprodukt.

**Tests:** 25/25 PHP-Syntaxprüfungen, ZIP-CRC 28/28, 40 lokale Positiv-/Negativtests (darunter 16 neue RC5-Fälle), 25 originale RC3-Dateien unverändert. Keine authentifizierte WordPress-/Provider-Liveprüfung; DataForSEO kostet bei eingeschalteter Recherche, max. fünf neue Tasks je UTC-Tag. Die gesamte Automatik ist standardmäßig aus. Keine Änderungen an HAB-001/002/003, Pferdeatelier, Hobbydepot, K0 oder externen Zugangsdaten.

**Nächster Schritt:** Nur die bestehende Hab-Affiliate-Zentrale in WordPress kontrolliert mit RC5 aktualisieren. `Affiliate-Zentrale → Amazon-Automatik`: Tag `habundbewahr-21` speichern, Amazon-Produktbuttons aktivieren; DataForSEO noch aus lassen. Erst echten Kategorien-Suchlink mit eigener Tracking-ID prüfen, danach die kostenpflichtige DataForSEO-Suche getrennt freigeben und Datenbasis für konkrete Produktkarten prüfen.

---

## 07.11.2026 – aktueller technischer HAB-004-Stand RC4

HAB-004 0.1.1-rc4: vollständige CURRENT.zip, 616072 Bytes, 28 Einträge, SHA256 c601c1f540fccdd18dde59b7c15fc55cfe53b68a59459d45182a2cf1bcd55017, Git-Blob f3a77efff2cb16de34c91eb0c4ec3b072a3999db (remote Größe und Blob bytegleich geprüft).

Original: Hab-RC3, 27 Dateien. Von deren Dateien 25 byteidentisch, geändert Haupt-PHP und includes/trait-ppar-idealo.php, hinzugefügt includes/trait-ppar-hb-amazon.php. Existing Banner-, Frontend-, Produktkarten-, Ausgabe- und Artikelplandateien unberührt. DataForSEO: Opt-in, stündliche WP-Cron-Verarbeitung, max. 5 kostenpflichtige POSTs/UTC-Tag, gespeicherte offene task-ID, eindeutiger Variantenabgleich. Amazon: eigene Tracking-ID habundbewahr-21 ausschließlich nach Speicherung/Aktivierung; direkte Links nur für belegte einzelne ASIN aus idealo oder streng geprüfte DataForSEO-Treffer. Kein eigener manueller Amazon-Kampagnenweg. Alte fremde idealo-Defaults (Adspace 568313, Feed 2901) aus Hab entfernt/gesperrt. Keine Fremd-Provider-Zugangsdaten übertragen.

Lokal geprüft: PHP Syntax 25/25, 24 Assertions (Positiv/Negativ, Variantenabweichung, falsche Portal-ID, bezahlter POST vs kostenloser GET, Tagesgrenze, keine doppelten Buttons), ZIP CRC, installierbare Original-Pluginwurzel, 25/27 originale Dateien bytegleich. Keine authentifizierte WordPress-Installation oder echte Provider-Verbindung und keine Google-/Frontend-Liveprüfung; nur ein Upgrade-Testkandidat. Die Standardautomatik bleibt deaktiviert.

Nächster Schritt: nur das bestehende Hab-004-WordPress-Plugin mit CURRENT.zip aktualisieren; Affiliate-Zentrale → Amazon-Automatik öffnen; habundbewahr-21 speichern, Amazon-Produktbuttons einschalten; eigene DataForSEO-Zugangsdaten erst nach Kostenfreigabe eingeben; an einer echten passenden Produktkarte Ziel/Tracking und Slot prüfen. Pferdeatelier und Hobbydepot/K0 unverändert.

---

# HAB-004 – Hab & Bewahr Affiliate-Zentrale

## Aktuelle Version 0.1.0-rc3 – 06.11.2026

**Status:** Vollständiger isolierter **Installationskandidat**, nicht auf WordPress live freigegeben.
**Offizieller Voll-ZIP-Pfad:** `ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`.
**ZIP:** 605.196 Bytes, 27 Dateien, WordPress-Pluginordner `affiliate-portal-router/`.
**SHA-256:** `2e5f6790ab3a64b446e34d132037684ad8fa637f76f43974e2816a1f75bc11eb`.
**Git-Blob:** `b6b19e7a739b70a813c5e9de2e290d98c898156f`.
**Nachweis:** GitHub-Workflow `42252394077` PASS; unabhängiger vollständiger GitHub-Readback, identischer SHA. Im offiziellen Design-ZIP 0.1.189 waren 546 Knoten; der neue Hab-Adapter ermittelt daraus sechs Schutzwelten, 285 zugeordnete Artikelkategorien und 13 konkretere Produktkategorien. **Dies ist der im Design hinterlegte Kategorienstand, keine Aussage zum Live-WordPress-Inhalt.**

### Was geprüft und verändert ist
- 26 Originaldateien aus dem neutralen Affiliate-Stamm **unverkürzt erhalten** und 1 eigener Hab-Adapter: keine bestehende PHP-Funktion entfernt.
- Gegen vorige RC2-ZIP **24 von 27 Dateien bytegleich**, Änderungen nur an Plugin-Hauptdatei, eigenem Hab-Adapter und Readme. Unveränderte Engine der Provider, eBay, idealo, Awin, ADCELL, Digistore24, Produktplanung, Kampagnen, Werbemittel, Chefentscheidungen, Nachverarbeitung bleibt erhalten.
- Fünf vorher nur beiliegende Zusatzmodule für Produktquellen, Admin-KISS, Deal-Radar, Partnerstatistik und Digistore24-Weitergabe beim tatsächlichen WordPress-Hook-Start aktiviert. **92** registrierte Hook-Typen im isolierten CLI-Test.
- Fehler aus RC2 behoben: harte Positivliste suchte Produkte nur in Seitenüberschriften und traf den Designbestand nicht. RC3 bindet tatsächliche Kategorie-Namen an echte gemappte, veröffentlichte WordPress-Parent-Seiten (nicht an erfundene Produktseiten); enge Fachproduktprüfung, Verwechslungs-/Zubehörsperre, sechs echte Schutzwelten, alle 285 belegten Kategorien.
- Bestehende Hab-&-Bewahr-Design-Filter für Artikel, Bereichsseiten, Schutzwelten und Magazin-/Anzeigenmarkt-Werbeplätze angebunden; kein automatisches doppeltes Artikeldesign-Rendering.
- Seitenklassifizierung verwendet einmaligen, pro Request zwischengespeicherten Index statt mehrfach vollständigen Kategorien-Scan. Alle 27 PHP-Quellen lint-geprüft, Frontend-JS syntaktisch geprüft, ZIP CRC PASS.
- Voll-ZIP wurde zweimal unabhängig gebaut: beide bytegleich, erneuter kompletter GitHub-Download bytegleich.
- Fremde Pferdeatelier-/Hobbydepot-Designbindungen und Portaldaten werden nicht aktiviert; vorhandene allgemeine Affiliate-Engine bleibt in den Originalfunktionen erhalten.

### Grenzen / keine erfundenen Freigaben
- **Keine Live-Abnahme im echten WordPress** und keine realen API-/Provider-Konto-Tests. Automatische Affiliate-Auslieferung standardmäßig aus.
- Die vollständige Pferdeatelier-Referenz **6.72.306** (66 Dateien) liegt im Hab-Affiliate-Büro nicht als installierbares Gesamtarchiv; Gleichheit aller jüngsten Pferdeatelier-Funktionen ist **nicht belegt**. Nachweis betrifft die 26-Dateien-Quelle.
- Keine Messung der Website-Gesamtperformance im Hosting. Gemessen/qualifiziert ist lediglich die schnellere Lookup-Logik und das Vermeiden unnötiger wiederholter Options-/Baumzugriffe im selben Request.
- Historische fachliche Vergleichsbeispiele können als harmlose Kommentare der unverändert gehaltenen neutralen eBay-Engine vorkommen. Das ist kein aktiver Pferdeatelier-Zielkatalog; die reale fachliche Produktzuordnung nutzt allein den Hab-Kategorie-Workflow. Keine blinde Löschung notwendiger Recovery-/Sicherheitslogik.
- Glossar-Einzelbanner: Die Design-Glossarfunktion hat keine allgemein gültige echte WordPress-CPT-Zielkennung. Daher wird keine erfundene Zielzuordnung behauptet. Andere echte Bannerplätze sind angebunden.

**Nächster Schritt:** RC3 auf gesichertem Hab-&-Bewahr-WordPress installieren, **nicht** auf Pferdeatelier. Zuerst Backend-Seiten, Kategorie-Readback, echten Artikel und echte Werbeplätze prüfen. Erst nach eindeutiger Liveprüfung Provider für Hab & Bewahr separat anbinden und Automatik aktivieren.
