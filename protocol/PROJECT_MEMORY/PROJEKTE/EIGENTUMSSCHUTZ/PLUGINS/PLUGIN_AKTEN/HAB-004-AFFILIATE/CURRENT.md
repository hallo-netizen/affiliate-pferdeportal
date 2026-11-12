## 12.11.2026 – HAB-004 RC20 0.1.17-rc20: IDEALO AKTIVIERUNGSFEHLER BEHOBEN

**Neues offizielles vollständiges Pluginpaket:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, zusätzliche benannte `HAB_AFFILIATE_RC20_0.1.17-rc20.zip`, SHA256 `532d3ef2552c44cc9652881e1ff943ad7bcd8ddd93fb779f5dab1d55a08b8d97`, 36 Dateien. Das bisherige RC19 sperrte pauschal die Idealo-Feed-ID **2901**, obwohl diese in Hab & Bewahr bei eigener Adspace **568944** angeboten wird. RC20 sperrt ausschließlich die fremde Adspace **568313**; der freigegebene eigene Feed wird nicht mehr abgeschaltet. GitHub-Lauf 43240486920: fünf ausgeführte PHP-Funktionstests PASS, alle 25 PHP-Dateien syntaxfehlerfrei, ZIP 36/36 CRC PASS. Sonstige RC19-Funktionen, Versicherungsregeln, Design und andere Portale unverändert. **Noch keine WordPress-Liveabnahme.** Nach Installation Hab-Backend: Haken aktivieren, „Speichern & API prüfen“ und echte Freigabe kontrollieren.

---

## 12.11.2026 – IDEALO HAB & BEWAHR: FREIGABE GEMELDET, KONFIGURATION NUTZT RC19

Betreiber meldet neu freigegebenen iPN-Produktdatenfeed für **Hab & Bewahr, Werbefläche 568944**. Tatsächliches HAB-004 `CURRENT.zip` erneut geprüft: **RC19 0.1.16-rc19 unverändert** (36 Einträge, SHA256 `6d72fcd41a8b365e84815770014098946774bab7f2425c3546e48da66cd262f0`), integrierter iPN-Adapter und Versicherungs-Sperre vorhanden. **Kein neues Plugin nötig**. Exakte eigenständige Feed-ID, privater iPN-API-Key und Download-URL sind im WordPress-Backend noch nicht verifiziert; kein Live-Import oder öffentliches PASS behaupten. Ablauf: `Affiliate-Zentrale → idealo`, Hab-Adspace und reale Feed-ID eingeben, `Speichern & API prüfen`, nach echtem API-PASS privater Feed-Import, abschließender Ausgabetest. **Keine Idealo-, Amazon- oder eBay-Produktwerbung im Versicherungsbereich.** `CURRENT.zip` unverändert. Gemeinsame verbindliche Anleitung: `../../../AFFILIATE/IDEALO_FREIGABE_EINRICHTUNG_20261112.md`. GitHub-Action-Checks 43233587036 / 43233830615.

---

## 11.11.2026 – HAB-004 AFFILIATE RC19 (0.1.16-rc19) – VERSICHERUNGSBEREICH EXKLUSIV, LÜCKENLOS EIGENBANNER

**Vollständige CURRENT.zip als RC19-Kandidat im HAB-Pluginbüro gebaut:** 2.336.726 Bytes, 36 Dateien, SHA256 6d72fcd41a8b365e84815770014098946774bab7f2425c3546e48da66cd262f0 (nach bestandenem GitHub-Merge gültiger offizieller Current). Direkter, reproduzierbarer Build ausschließlich aus HAB-004 RC18 (0.1.15-rc18, verifizierte SHA256 a98063820d1564bf7cc7312c4c232369ac198bbaa49fbb6b173f76cd5096da89). **Nur vier bestehende Dateien im vollständigen Plugin verändert**: affiliate-portal-router.php, includes/trait-ppar-hb-amazon.php, assets/frontend.css, readme.txt. Keine neue Plugin-Identität, keine neue Tabelle, keine Änderung der sechs anderen Themenwelten oder des Designplugins HAB-001 RC19.

**Nutzer-Zielvertrag umgesetzt (offline):** Alle vorhandenen, aktiven Bannerplätze im Versicherungszweig von der R1-Hauptwelt über 5 R2, 46 R3, 323 Kategorien bis zu den eindeutig verknüpften Artikeln zeigen – wenn kein freigegebener Partnerbanner existiert – einen eigenen internen Hab-&-Bewahr-Versicherungs-Themenbanner. Der eigene Hinweis enthält einen aus dem aktiven Kategorie-Snapshot ermittelten internen R1/R2-Link, ist kein angebliches Tarifcheck-Angebot und hat keine erfundene Provision. Produktkarten-/Amazon-/Shop-Fallbacks werden im Versicherungszweig unterbunden; vorhandene 300×250- und 125×125-Originalbanner sind für passende Artikel/Glossar-Slots unverzerrt zulässig; 728×90 und 468×60 für entsprechende Versicherungs-Querbanner. Direktpartner Tarifcheck, Awin und ADCELL verwenden weiterhin die vorhandene zentral verwaltete Kampagnenauswahl. Ein echtes, freigegebenes allgemeines Versicherungsprogramm kann unterhalb exakt passender Programme als Fallback erscheinen; sonst eigener interner Themenbanner. Kein externes Frontend-HTTP und keine neue Werbe-Engine.

**Harter Runner-Test PASS:** 1.421 ausgeführte PHP-Funktionsprüfungen gegen 1 R1 + 5 R2 + 46 R3 + 323 Kategorien plus Beiträge / Gegenfälle, einschließlich Amazon/Finanzen-Sperre, Partner-Verbot, Freigabe allgemeiner Versicherungsvergleiche, internem Fallback in jedem geplanten Bannerplatz, 728×90 / 468×60 / 300×250 / 125×125 und Gegenproben auf eine fremde Welt. Alle 25 PHP-Dateien ohne Syntaxfehler, 36/36 ZIP-Inhalte mit CRC geprüft. GitHub-Actions-Run 43014867482; reproduzierbarer Build und echte PHP-Testquelle in AFFILIATE/IMPLEMENTIERUNG_RC19_INSURANCE.

**WICHTIGE GRENZE:** Die Tarifcheck-Partner-Bannercodes, echten Direktlinks, Rechnercodes und providerseitigen Freigaben wurden nicht übergeben. Die neue Version **erstellt keine erfundenen oder provisionsfähigen Tarifcheck-Anzeigen** und führt noch keinen Live-Test durch. Vor echtem Tarifcheck-Banner müssen Original-Werbemittel in der zentralen Affiliate-Zentrale freigegeben/zugeordnet werden. Die internen Themenbanner garantieren vorerst die optische Belegung. Vollständiger Vertrag: AFFILIATE/VERSICHERUNGEN_TARIFCHECK_KONZEPT_20261111.md Abschnitt 9. **WordPress-Installation/Liveabnahme OFFEN.**

---

## 09.11.2026 – LIVE-PASS: HAB-004 AFFILIATE RC18 (0.1.15-rc18), AMAZON-KACHELDARSTELLUNG

Nutzer bestätigt ausdrücklich die Amazon-Kacheldarstellung unter RC18 als bestanden. **Scope: visuelle Live-Abnahme**, nicht automatisch Tracking/Provider- oder Bestellfunktionsprüfung. **CURRENT.zip bleibt die bereits im Pluginbüro vorhandene RC18-Datei** (36 Einträge; Git-Blob `9d415e7dcae70ec1ff23a466ed6b1186134564ec`); keine erneute Erstellung oder Änderung. Gemeinsames Live-Abnahmeprotokoll: `../../ABNAHMEN/2026-11-09_WORDPRESS_DESIGN_RC19_AFFILIATE_RC18.md`. Ältere „Live offen“-Vermerke für die Amazon-Kacheldarstellung sind historisch.

---

## 08.11.2026 – HAB-004 Affiliate RC18 0.1.15-rc18 – weltweite Amazon-Kachel-Ursache behoben (geprüfte Current-ZIP)

**Physisch im eigenen Pluginbüro:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, 2.332.375 Bytes, 36 Dateien, Git-Blob `9d415e7dcae70ec1ff23a466ed6b1186134564ec`; GitHub-Runner-SHA256 `a98063820d1564bf7cc7312c4c232369ac198bbaa49fbb6b173f76cd5096da89`. **Partnerplugin HAB-001 Design bleibt RC18 0.1.191 unverändert** (84.538.023 Bytes). Vorheriges HAB-004 RC17 ist historischer Stand, nicht länger Current.

**Reproduzierte Ursache, nicht nur Symptom:** Amazon-Weltbild wurde aus `sanitize_title($world['name'])` bestimmt. Deutsches WordPress formt dabei Umlaute zu `oe/ae`; die handgeschriebenen Bildzuordnungen erwarteten `o/a`. So fehlten sämtliche Banner in den Welten *Vandalismus & Zerstörung* und *Technik & Ausfälle* einschließlich ihrer Unterebenen. Zusätzlich wurde bei Seiten die bereits vorhandene feste Knotenkennung nicht bis zum Banneranbieter weitergereicht.

**KISS-Fix:** Nur vier vorhandene Dateien im vollständigen HAB-004 geändert: Pluginheader, Original-Hab-Brücke, ursprüngliche Amazon-Fallback-Funktion und Readme. Die sechs Schutzwelten nutzen nun ausschließlich ihre **festen aktiven Knoten-IDs**. Das Design übergibt seine reale ID, die Affiliate-Brücke verifiziert sie zusätzlich gegen Seiten-ID und aktuellen Snapshot; alle vorhandenen Kampagnen, Produkte, Bilder, Amazon-Tracking, eBay/Idealo, Speicherregeln und andere Portale bleiben unverändert. Keine neue Tabelle/Engine, keine neue kostenpflichtige Suche.

**Ursachenbeweis mit echtem HAB-001-Designbaum und deutscher Umlautbehandlung:** vor Änderung nur **282/415** Bannerkontexte mit Ausgabe (4/6 Welten, 21/31 R2, 63/93 R3, 194/285 Blattkategorien); danach **415/415** (6/6, 31/31, 93/93, 285/285). Zusätzlich 25/25 PHP-Syntax, 36/36 ZIP-CRC, alle 32 unbetroffenen Einträge inhaltsgleich. Build des tatsächlichen GitHub-CURRENT aus unabhängig abgezogener offizieller RC17-Datei mit 36/36 identischen Datei-Inhalten; GitHub-Actions-Run `42505319754` erfolgreich. Der Dateisatz ist für die vier geänderten Dateien per SHA256 abgesichert und der Build reproduzierbar dokumentiert: `AFFILIATE/RC18_BUILD_FROM_RC17.py`.

**Noch nicht behaupten:** Eine WordPress-Live-Abnahme dieser neuen RC18 fehlt. Nutzer-Screenshots hatten Wasser & Leckage für RC17 bestanden, Vandalismus RC17 NICHT. **Nach Installation nur HAB-004 Affiliate RC18 zusätzlich zum installierten Design RC18 prüfen:** Vandalismus und Technik plus je eine Unterseite und Blattkategorie; bereits bestätigte Wasser-Kacheln dürfen nicht verschlechtern.

---

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

## HAB-004 – RC9: Sieben Hauptwelten ohne Gesamtsperre

**07.11.2026 – HAB-004 0.1.6-rc9 (einzige aktuelle Voll-ZIP):** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **618.212 Bytes, 28 Dateien**, SHA256 `04de5f4492887686c5a224640ffa5e4d64175927186dc3fe7f19d546e0ea4120`, Git-Blob `500d70b04607373a133966859de02b03ec7f62cb`.

**Harte Ursache:** Kategorienstruktur kennt sechs bestehende Welten plus `core:world:insurance` (siebte Welt), aber RC8 verlangte exakt sechs. Original-RC8 mit sieben Hauptwelten reproduzierbar `hb_worlds_unexpected`. Die 2.720 Knoten/2.714 Bindungen sind Live-Screenshot-Werte, kein heruntergeladener WP-Datenbankabzug.

**KISS-Korrektur:** Es wird nur verlangt, dass mindestens eine gültige gemappte Hauptwelt existiert; Welt- und Bereichszahlen folgen dem tatsächlich aktiven Bestand. Eine zusätzliche oder nicht gemappte einzelne Welt blockiert die restlichen Welten nicht. Bei vollständig fehlendem/ungültigem Snapshot werden weiterhin sicher keine kostenpflichtigen Aufträge gestartet. Der Affiliate-Hauptschalter `ppar_enabled` bleibt unverändert und muss bei Bedarf in WordPress (`Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv`) ausdrücklich aktiviert werden.

**Echte lokale Prüfungen:** 116 vollständige Original-Plugin-/Design-WP-Simulationen (6/7/8 Welten, 2.720 Knoten/2.714 Mapping, Klick→DataForSEO-Mock→ASIN→Speicherung→R3-/Kategorie-Ausgabe, 1 Welt ohne Mapping, falsche Revision, Altwerbe-Vorrang, global AUS); 104 DataForSEO-Worker-/Kosten-/Fehler-/Beitragstests mit sieben Welten; 96 Regressionstests; **316 PASS, 0 FAIL, keine PHP-Warnungen**, **25/25 PHP-Lints**, **ZIP 28/28 CRC**. 25/28 Plugindateien gegenüber RC8 identisch. Kein echter WordPress-Produktivlauf oder bezahlter DataForSEO-API-Auftrag. Dokument: `AFFILIATE/IMPLEMENTIERUNG_RC9/PRUEFBERICHT.md`, minimaler Patch `RC8_TO_RC9_SOURCE_DIFF.patch`.

**Nächster Schritt:** RC9 in WordPress als Update des bestehenden Plugins einspielen. Wenn die oben sichtbare Meldung „Affiliate-Zentrale insgesamt ausgeschaltet“ besteht, über `Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv → Einstellung speichern` einschalten. Erst dann unter `Amazon-Automatik` einmal `Jetzt einen Suchlauf starten`; der Status muss zeigen, ob ein Auftrag erzeugt wird, ein Fehler vorliegt oder bereits geprüft ist. Max. fünf neue kostenpflichtige DataForSEO-Aufträge/UTC-Tag. Die Live-Wirkung erst danach bestätigen.

---

## 07.11.2026 – HAB-004 RC8 – einziges Current

**07.11.2026 – HAB-004 Affiliate-Zentrale 0.1.5-rc8 ist einzige aktuelle Voll-ZIP:** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **620242 Bytes**, 28 ZIP-Dateien, SHA256 `f2d09e649fbb6a69a54e64b01df239013975999e46921f08b722adff139ccd30`, Git-Blob `35d32677fb7232a8c0891cc0e730b4b02851b945` (bei GitHub binär geprüft).

**Vollständige lokale Workflow-Simulation: 234 bestandene Prüfungen, 25/25 PHP-Syntax, ZIP-CRC 28/28; nur 3/28 Originaldateien verändert** (`affiliate-portal-router.php`, `includes/trait-ppar-hb-amazon.php`, `readme.txt`). RC7 hatte beim echten Screenshot nach manuellem Run null Kandidaten, aber irreführend bloß „Keine neuen passenden Produkte“. Nachstellung mit den originalen aktiven Hab-Quelladapter-Klassen beweist: bei fehlendem/falschem/inhaltlich nicht freigegebenem WP-Kategoriebaum wurde dessen WP_Error als leere Kandidatenliste verschluckt. Zudem vorherige RC7-Simulation des Frontends hatte einen falschen Kategorie-Slot und ignorierte leere Kategorien/Produktseiten. RC8 zeigt direkt nach Klick oben den echten Workflow- und Kategoriebaum-/Provider-Status und lässt DataForSEO bei ungültiger Quelle gesperrt; echte DataForSEO-API-Taskfehler werden erkannt, statt als unendliches „noch in Bearbeitung“ zu gelten. Wiederverwendung des bestehenden Workers, API-Kostenlimits und Slots, plus die vorhandenen Hab-Design-/Kategorie-Hooks für Amazon-Affiliate-Links auf relevanten Produktseiten selbst ohne redaktionelle Beiträge. Bereits vorhandene Werbung hat Vorrang. Keine zweite DB, kein zweiter Cron, keine Fremdportale/K0 verändert.

**Ehrliche Testgrenze:** Die originalen vollständigen Hab-Plugin-Dateien inkl. originalem Portal-Quelladapter und originalem Design-Plugin-Hook wurden offline mit nachgestellten WordPress-Optionen und DataForSEO-API-Antworten ausgeführt; **keine echte WordPress-Produktivabnahme, keine kostenpflichtige Provider-Abfrage, kein Einblick in Live-Kategoriebaum-Optionen**. RC8 zeigt die genaue Quelle des noch offenen Live-Blockers erst nach Installation.

**Nächster Schritt:** Auf Hab-&-Bewahr-WordPress das bestehende HAB-004-Affiliate-Plugin durch diese RC8-Voll-ZIP ersetzen, `Affiliate-Zentrale → Amazon-Automatik → Jetzt einen Suchlauf starten` **einmal** drücken, dann die **oben sichtbare Statusbox** prüfen. Kein wiederholtes blindes Klicken; bis zu 5 neu bezahlte DataForSEO-Aufträge je UTC-Tag. Falls Quelle blockiert, dort die genaue Ursache lesen statt neue Suche zu behaupten.

---

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
