## 08.11.2026 – VERBINDLICHE HAB CURRENT-RELEASE: DESIGN RC18 + AFFILIATE RC17

**Tatsächlich im offiziellen Pluginbüro als vollständig neu gebaute, geprüfte `CURRENT.zip` auf dem geschützten Releasezweig; Veröffentlichung nach Merge:**
- **HAB-001-DESIGN 0.1.191 (RC18)**: `PLUGINS/ISOLIERTE_PLUGINS/HAB-001-DESIGN/CURRENT.zip`; 84.538.023 Bytes; **SHA256 `def9ceb5a99eb965aa55805038d92e93e53747191786edc9f44fe74bbe560a7e`**, Git-Blob `04f8ef38c649049cebcc12f240471a66d270a465`; **432 Dateien**, 35/35 PHP-Lint und 432/432 ZIP-Inhaltsverifikation.
- **HAB-004 Affiliate-Zentrale 0.1.14-rc17**: `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`; 2.331.918 Bytes; **SHA256 `b22e4d49a56b25e3fc2e46c9bdd0ccbd7c6c16eb7c1f6bb48ae005db0ba50a03`**, Git-Blob `e8f5d5c77459a2e94b77c093f7c58883a2e4386c`; **36 Dateien**, 25/25 PHP-Lint und 36/36 ZIP-Inhaltsverifikation.
- Ausgangs-ZIPs **wort-/bytegenau aus dem offiziellen Pluginbüro erneut geprüft**: Design 0.1.189 SHA256 `947a950273edb6bf47e76ffeef67ff51425db620adc2650c742831e73093134c`; HAB-004 RC11 SHA256 `cf8cf7946aa7605dadecda1f041cfc6fb150c7971f7c9feb9dbb6dd1ac8eabda`. Alle Altdateien übernommen. Nur belegte Quelländerungen von RC18/RC17 zugespielt; sieben bereits in HAB-001 vorhandene Themenfotos für HAB-004 bytegleich kopiert. **Kein neues Plugin, keine neue DB, keine Änderungen an Pferdeatelier/Hobbydepot, kein bezahlter Suchlauf.**

**Nutzer-Liveabnahme der VORGÄNGER RC17 Design + RC16 Affiliate vom 08.11. 15:25–15:36:** Kachelfotos PASS, Raster-Kacheln formatfüllend PASS. **Noch offen / durch neuen RC18-Kandidaten offline korrigiert:** Einteilungslogik auf allen Kategorieebenen, auch bei vollständig gefüllten Zeilen; hoch-nach-unten-Bildverlauf in Amazon-Rasterkacheln, größerer am unteren Rand platzierter offizieller Amazon-Button, Hover auf Beitragsvorschauen, präzise Produktsuche statt „Wasser & Feuchtigkeit“ → Luftbefeuchter. Browser mit echten Originaldateien/CSS: **42 Konstellationen** aus sechs Bildschirm-/Rastertypen, darunter Hauptwelt/R2/R3, 900/390 px, plus 12 gesonderte Screenshots/Prüfungen bei 1250px, keine Überläufe, CTA sichtbar, Originalbutton und Hover. PHP-Funktionstest: **17 konkrete Zielzuordnungen** bestanden. **Echte WordPress-Liveabnahme dieser NEUEN Versionen noch offen**; nicht als schon installiert ausgeben.

**Korrekturregel Amazon:** Nicht die bloße Themenüberschrift „Wasser & Feuchtigkeit“ als Suchwort: gezielt `Wassermelder Leckagesensor Wasserstopp`; für Leckage/Rückstau/Siphon passende physische Schutz-/Reparaturprodukte; feste Themenbäume statt geratenem Amazon-Kategorieausgang; nur bestehender Hausbanner als nachrangiger Fallback. Benutzerwunsch gilt für alle Schutz-/Kategorienebenen, einschließlich voller Reihen. Versicherungsstrang bietet thematisch Dokumentenschutzartikel, **keine als Versicherungsleistung ausgegebenen Amazon-Produkte**.

**Zulässige nächste Aktion:** Die beiden neuen aktuellen `CURRENT.zip` im WordPress-Backend als Updates installieren; dann an mehreren Hauptwelten und R2/R3 inklusive Vandalismus, Wasser und unterster Kategorie testen, volle Reihen, Handyansicht, Amazon-Ziel und Beitrag-Hover. Keine RC16/RC17-Vorinstallation nötig; immer beide aktuellen Zips zusammen. 

---

## 08.11.2026 – HAB-004 RC14 – Kategorie- und Beitragsbanner, CHAT-TESTVERSION

**Aktueller vollständig installierbarer CHAT-KANDIDAT**: `Hab-und-Bewahr-Affiliate-RC14-Kategorien-und-Beitraege.zip`, **0.1.11-rc14, 2.092.433 Bytes, SHA256 b524b5fbd06b15bbe8425c0d7da2b5c28b2eb2b1896dee9a7e8fd84443e8a7e4**, 35 Dateien (28 Originale + sechs freigegebene Hab-Weltmotive + originaler Hobbydepot-Amazon-Badge). RC11/RC12/RC13 als notwendige Zwischeninstallation **NEIN**. `HAB-004/CURRENT.zip` auf GitHub bleibt bis zur gesonderten Synchronisierung weiter RC11, NICHT RC14. **Noch nicht live abgenommen.**

**Harter Quellabgleich:** HAB-001 Original, HAB-004 RC13, Hobbydepot HD009 **0.1.25**. Bereits vorhandene Banner-/Kampagnen-/Glossar-/Artikel-Slots wiederverwendet, keine neue Architektur. 6 eindeutige Hauptwelten mit je eigenem ORIGINAL-Hab-Themenfoto; alle nachgeordneten Themen, WordPress-Kategorien und eindeutig zugeordneten Beiträge/Glossarbegriffe erben das Weltmotiv; Amazon-Suchthema bleibt konkret. Versicherungen: ohne passende physische Amazon-Kategorie KEIN täuschender Amazon-Banner. Breite Banner 6:1 PC, 4,2:1 mobil, Glossar und Beitrags-Seitenleistenquadrat 1:1. Offizieller, einziger Amazon-Button aus HD009 in Orange, kein Portal-Logo/Zusatztext, keine Mehrfachrahmen. Echte Kampagnen haben Vorrang. Keine neuen bezahlten Suchläufe und keine Änderungen an eBay/Idealo-Produkten.

**Prüfung:** 63 PHP-Funktionstests bestanden, 25/25 PHP-Lint, 35/35 ZIP-CRC, alle bisherigen Originaldateien enthalten. In Chromium bei 1250/390 px alle 4 realen Bilder geladen, kein horizontaler Überlauf, korrekte Formate. Detailbericht: `AFFILIATE/RC14_BANNER_KATEGORIEN_BEITRAEGE_20261108.md`.

**Nächster Schritt:** RC14 als reguläres HAB-004-Update in WordPress installieren, echte Screenshots Kategorie Wassermelder + zweite Schutzwelt, Glossar + Beitrag prüfen. Erst dann Live-PASS. Einzelproduktbilder (Amazon ASIN) weiterhin **nicht** behoben.

---

## 07.11.2026 – RC13 BANNER: IM CHAT ALS TEST-ZIP, NOCH NICHT LIVE

**Aktuell erzeugte vollständige HAB-004-Testversion:** `Hab-und-Bewahr-Affiliate-RC13-Banner-Test.zip`, Version `0.1.10-rc13`, 627700 Bytes, SHA256 `4179371267f4d983b095ab846166c9d9dd44eb010c54e18ca3d808585c617f1e`. Im **Chat zum Herunterladen**, **NICHT** im GitHub-`CURRENT.zip`. Es gilt weiterhin: **GitHub-`CURRENT.zip` = RC11, live 16:47 durchgefallen**; RC12 wurde vom Nutzer nie installiert. RC13 enthält RC12 vollständig, also kein vorheriges RC12-Upgrade nötig.

**Was tatsächlich offline bestanden hat:** vorhandene RC12-House-Banner-Ausgabe nach dem HD009-Original für 4.2:1-Quer-/1:1-Quadratbanner mit Original-Hab-Themenfotos und Amazon-Kategoriesuchlinks; echtes HAB-001-Glossar nutzt bisher ungenutzten Original-Filter `hbdp_glossary_ad_markup` für das Quadrat in der Seitenleiste, statt tote `the_content`-Hooks. Gebuchte Werbung/Schalter/keine passenden Bilder beachtet; keine neue Engine und keine Fremdportal-Änderung. 20 Funktionsproben, 25 PHP-Lints, 28 ZIP-CRC, Original-WebP mit 1200/1024/390px-Layout PASS. **WordPress-Live-Abnahme fehlt**, echte Amazon-Einzelproduktfotos weiterhin ungelöst. Details: `AFFILIATE/RC13_BANNER_ABNAHME_20261107.md`. **Keinen neuen kostenpflichtigen DataForSEO-Lauf auslösen.**

---

## 07.11.2026, 16:47 Uhr – RC11 live NICHT BESTANDEN (Screenshotbeweis)

- Wassermelder-Frontend: 3 ASIN-Produkttitel und Amazon-Links, **riesige leere Bildkarten**, nicht die funktionsfähige Pferdeatelier-Produktdarstellung. Das ursprüngliche `hb_amazon_product_family_markup` übergibt bewusst `image_url=''` an unveränderten Karten-Renderer, der eine 150-Pixel-Bildzeile und 360-Pixel-Mindesthöhe erzwingt.
- Bestehender Affiliate-Bannerslot im Design meldet **kein passendes Werbemittel**. In `PPAR_HB_Integration::area` wird bei echten WordPress-Kategorie-Knoten `kind=banner` ausdrücklich verweigert. Für Seiten benötigt die reguläre Bildbanner-Ausgabe eine gültige Bild-URL; Hab-Amazon-Fallback erzeugt nur Textlinks. Damit fehlen Amazon-Übergangsbanner.
- Harter Quellabgleich mit aktuellen Originalen **Pferdeatelier**, **Hobbydepot HD009 0.1.20**, **HAB-001 Design** und **HAB-004 RC11** vom 07.11.2026. Hobbydepot benutzt für freie Bannerplätze bereits einen Amazon-Suchlink **mit thematisch freigegebenem Portalbild** in der bestehenden Ausgabe; Pferdeatelier rendert reale Produktkarten mit echten Quellbildern und Mehranbieter-Buttons. Keine Erweiterungsarchitektur nötig.
- Hab speichert aus DataForSEO bewusst nur ASIN/Titel; **keine rechtlich abgesicherte Amazon-Produktbildquelle**, keine Creators-/PA-API in HAB-004. Drittanbieter-`image_url` nicht ohne geprüfte Nutzungsrechte als Amazon-Foto übernehmen. Amazon-Partnernet-Richtlinien: https://partnernet.amazon.de/help/operating/policies
- **Status: RC11 ist kein live abgenommener Fix; vor weiterem Installer vollständige Produkt-/Bannerquelle und Ausgabe prüfen.** KISS-Ziel: gebuchte Kampagnen zuerst, sonst Themenbanner nach Hobby-Modell im gleichen Slot; Einzelprodukte nur mit echtem zulässigem Produktbild, bei identischem Artikel eBay/idealo im vorhandenen Mehranbieter-Renderer. Keine neue Datenbank, keine andere Portaländerung, keine kostenpflichtige DataForSEO-Suche ohne Bedarf.

---

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

# HAB-004 – Affiliate-Zentrale – CURRENT

## HAB-004 – RC9: Sieben Hauptwelten ohne Gesamtsperre

**07.11.2026 – HAB-004 0.1.6-rc9 (einzige aktuelle Voll-ZIP):** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **618.212 Bytes, 28 Dateien**, SHA256 `04de5f4492887686c5a224640ffa5e4d64175927186dc3fe7f19d546e0ea4120`, Git-Blob `500d70b04607373a133966859de02b03ec7f62cb`.

**Harte Ursache:** Kategorienstruktur kennt sechs bestehende Welten plus `core:world:insurance` (siebte Welt), aber RC8 verlangte exakt sechs. Original-RC8 mit sieben Hauptwelten reproduzierbar `hb_worlds_unexpected`. Die 2.720 Knoten/2.714 Bindungen sind Live-Screenshot-Werte, kein heruntergeladener WP-Datenbankabzug.

**KISS-Korrektur:** Es wird nur verlangt, dass mindestens eine gültige gemappte Hauptwelt existiert; Welt- und Bereichszahlen folgen dem tatsächlich aktiven Bestand. Eine zusätzliche oder nicht gemappte einzelne Welt blockiert die restlichen Welten nicht. Bei vollständig fehlendem/ungültigem Snapshot werden weiterhin sicher keine kostenpflichtigen Aufträge gestartet. Der Affiliate-Hauptschalter `ppar_enabled` bleibt unverändert und muss bei Bedarf in WordPress (`Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv`) ausdrücklich aktiviert werden.

**Echte lokale Prüfungen:** 116 vollständige Original-Plugin-/Design-WP-Simulationen (6/7/8 Welten, 2.720 Knoten/2.714 Mapping, Klick→DataForSEO-Mock→ASIN→Speicherung→R3-/Kategorie-Ausgabe, 1 Welt ohne Mapping, falsche Revision, Altwerbe-Vorrang, global AUS); 104 DataForSEO-Worker-/Kosten-/Fehler-/Beitragstests mit sieben Welten; 96 Regressionstests; **316 PASS, 0 FAIL, keine PHP-Warnungen**, **25/25 PHP-Lints**, **ZIP 28/28 CRC**. 25/28 Plugindateien gegenüber RC8 identisch. Kein echter WordPress-Produktivlauf oder bezahlter DataForSEO-API-Auftrag. Dokument: `AFFILIATE/IMPLEMENTIERUNG_RC9/PRUEFBERICHT.md`, minimaler Patch `RC8_TO_RC9_SOURCE_DIFF.patch`.

**Nächster Schritt:** RC9 in WordPress als Update des bestehenden Plugins einspielen. Wenn die oben sichtbare Meldung „Affiliate-Zentrale insgesamt ausgeschaltet“ besteht, über `Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv → Einstellung speichern` einschalten. Erst dann unter `Amazon-Automatik` einmal `Jetzt einen Suchlauf starten`; der Status muss zeigen, ob ein Auftrag erzeugt wird, ein Fehler vorliegt oder bereits geprüft ist. Max. fünf neue kostenpflichtige DataForSEO-Aufträge/UTC-Tag. Die Live-Wirkung erst danach bestätigen.

---



Letzte Version ist einzig die genannte RC9-Voll-ZIP; ältere RC8/RC7/RC6 nur in Git-Historie. Das Kategorieplugin, Designplugin, Bildzentrale, Pferdeatelier und Hobbydepot bleiben unverändert.
