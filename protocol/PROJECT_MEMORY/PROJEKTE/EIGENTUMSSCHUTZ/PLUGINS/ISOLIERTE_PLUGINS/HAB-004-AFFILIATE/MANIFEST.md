## 13.11.2026 – RC31 NEUESTE GEPRÜFTE TESTVERSION, NOCH NICHT LIVE

`HAB_Bewahr_Affiliate_RC31_TEST.zip` (2.349.072 Bytes, SHA256 `fa72cf9519ccaf92c672581eff35a8e4908a3f15511a1ef5f272448a36c99d56`), Plugin **0.1.28-rc31**, GitHub-Release `hab-affiliate-rc31-insurance-branch-cascade-20261113`, QA GitHub Actions **43439019366 SUCCESS**. Spezialversicherungsbanner ausschließlich in eigenem nachgewiesenen Versicherungszweig mit echter Verteilung zu den Unterkategorien; echte allgemeine Versicherungen innerhalb des gesamten Versicherungsbaums, andere Welten und Kredit sauber ausgeschlossen. Automatisches Neu-Zuordnen der schon gespeicherten Tarifcheck-Originale im Affiliate-Backend, max. 60 pro Aufruf; kein Reimport. Idealo-Bericht nennt jetzt ausdrücklich nur *Idealo*-Feedabdeckung, andere Anbieter weiter wie bisher. Testvollbeleg `../../../AFFILIATE/RC31_INSURANCE_CASCADE/ABNAHME_RC31_20261113.md`.

**Archiv- und Livewarnung:** `CURRENT.zip` hier ist weiterhin historische RC22-Baubasis, nicht RC31 und keine Aussage zur Liveinstallation. RC31 vollständige ZIP liegt ausschließlich als explizites Testrelease. WordPress-Liveabnahme offen. Keine anderen Portale, keine Kategorie- oder Designänderung.

---

## 13.11.2026 – RC30 (0.1.27-rc30), neueste vollständig getestete HAB-004-Test-ZIP

**Release:** `hab-affiliate-rc30-one-ad-label-real-bullets-20261113`, komplette Datei `HAB_Bewahr_Affiliate_RC30_TEST.zip` (2.346.028 Bytes; SHA256 `baa8e87cbab1f1bbbbce4f482bd73a706985f583c847f543eb93fbf7c644f34f`). Test `43419366272` vollständig PASS, echte PHP-Gruppen- und Produktkartenausgabe geprüft. Doppelte Anzeige aus dem **Produkt-Slot selbst** entfernt; Gruppentitel-Anzeige bleibt; echte Produktdaten in kurze Stichpunkte getrennt. Nur PHP-Hauptdatei/CSS/Readme geändert. Design RC19, Kategoriebaum, Affiliate-Provider, andere Portale und bestehende Importe unangetastet. **Liveinstallation noch offen. Kein Reimport zur Überprüfung erforderlich.** Prüfakte `../../../AFFILIATE/RC30_ONE_LABEL_BULLETS/ABNAHME_RC30_20261113.md`.

**Historische Ablage:** `CURRENT.zip` im Archiv bleibt weiterhin die reproduzierbare ältere RC22-Basis; installierbare RC30 ist die oben genannte vollständige Test-ZIP aus dem GitHub-Release. Nicht diese beiden Versionen verwechseln.

---

## 13.11.2026 – RC28 (0.1.25-rc28) NEUESTE GEPRÜFTE TEST-VERSION – LIVEABNAHME OFFEN

**Vollständiger GitHub-Release:** `hab-affiliate-rc28-kiss-topic-category-recognition-20261113`; Datei `HAB_Bewahr_Affiliate_RC28_TEST.zip` (2.344.644 Bytes; SHA256 `e474e25ec0f63440dfb5d69c993d0b0884431ee10cd009b589b3b6b50cc66f32`). Prüfung `43410070887` SUCCESS; 25/25 PHP-Lint, Regressionen ursprünglicher Affiliate-Funktionen, echte PHP-Kategorietests und alle 36 ZIP-Einträge bestanden. KISS-Ursache: Warenname nur aus redaktioneller Endkategorie statt bereits zugeordneter physischer Themenseite; eindeutige deutsche Schreib-/Pluralformen bislang übersehen. Korrigiert ausschließlich vier bestehende Dateien. Ausführlicher Bericht `../../../AFFILIATE/RC28_CATALOG_KISS/ABNAHME_RC28_20261113.md`.

**Wichtig:** `CURRENT.zip` dieser historischen Pluginbüro-Akte bleibt die verifizierte RC22-Ausgangsbasis für den vollständigen reproduzierbaren Testaufbau, **nicht** die neue RC28-ZIP und **kein Beweis über die Liveinstallation**. RC28 als vollständige Download-ZIP im GitHub-Release. Vorherige echte WordPress-Werte bleiben 14/35 Produktgruppen und 1.949 letzte importierte Produkte; Verbesserung bis WordPress-Prüfung unbekannt. Andere Portale unverändert.

---

## 12.11.2026 – RC22 0.1.19-rc22: BROWSER-CSS-CACHE-ROOTFIX (ECHTER LIVE-CHROME-GEGENTEST)

**Offizielle Voll-ZIPs:** `CURRENT.zip` + `HAB_AFFILIATE_RC22_0.1.19-rc22.zip`, 2.337.621 Bytes, 36 Dateien, SHA256 `c9d501396d5500e699eb6dd8d867318c41e8ea8efc43c8fe00ad9ee4ab4e32d1`. Gegenüber RC21 **nur Hauptdatei/Readme** geändert; RC21-Karten, CSS, Idealo, Amazon, Versicherungen, GTIN, Designplugin bytegleich. Ursache: Browser erhielt weiterhin unveränderte CSS-Version `6.72.211-hb-rc16-20261108`, sodass vor RC21 gespeicherte CSS-Fassung die neuen 3 Kacheln weiter untereinander anzeigen konnte. Neue CSS-Version wird über nativen WordPress-Plugin-Header abgeleitet: `6.72.211-hb-plugin-0.1.19-rc22`, künftig mit Pluginversion aktualisiert. **Live-Ursachenreproduktion im echten Chrome PASS:** Live-RC21-CSS 3 Karten nebeneinander, testweise altes RC20-CSS → exakt 3 große Karten untereinander, RC21-CSS zurück → wieder 3 nebeneinander (GitHub-Run 43247959556). 25 PHP Lints, 11 ursprüngliche Bridge/Design-Funktionstests, 36+432 ZIP-CRC PASS. **RC22 WordPress-Liveinstallation/Abnahme OFFEN**, keine echten Produktbilder (0), noch keine Idealo-Zusatzbuttons (3 Amazon-Links). Gesamtbeleg: `../../../AFFILIATE/RC22_CSS_CACHE_LIVE_20261112.md`.

---

## 12.11.2026 – OFFIZIELLE RC21 (0.1.18-rc21): KATEGORIE-PRODUKTKACHELN KOMPAKT, 3/2/1

**Vollständige Installations-ZIP und CURRENT:** `HAB_AFFILIATE_RC21_0.1.18-rc21.zip` bzw. `CURRENT.zip`, beide 2.337.596 Bytes, 36 Dateien, SHA256 `0f40eddb4526434c03acdd370d2763ac5a01eaea862a40cb9ae25bb8754363bf`. Aus dem echten RC20-CURRENT exakt und ohne Datenbank-/Frontend-Änderung gebaut. 4 Dateien im ZIP berührt: Hauptdatei (Version und Kartenhöhen), bestehende Hab-Bridge (Kategorie-Grid), bestehende CSS (responsive) und Readme (Version). Alle übrigen 32 unverändert.

**Ursache behoben:** Die drei bestehenden Produktkarten auf Kategorieebene wurden zuvor nur aneinandergehängt; zusätzlich hohe starre Mindesthöhen. Neues einziges Grid **Desktop 3 / Tablet 2 / Mobil 1**, keine doppelten Karten-Engines, kein Designplugin-Update. Vorhandene Multi-Provider-Ausgabe unverändert: zusätzliche Amazon/eBay/Idealo-Buttons nur bei GTIN-Exaktmatch und aktivem Feed, kein erfundenes Foto für Amazon-ASIN. Eigene Versicherungs-Sperre und andere Portalwelten unverändert. **RC21 Offline-PASS**: GitHub-Actions 43244276656, 11 echte PHP-Bridge-/Design-Tests, alle 25 PHP-Dateien lintfrei, 36/36 Affiliate-CRC und 432/432 Design-CRC. **WordPress-Installation/Liveabnahme OFFEN**. Verbindlicher Nachweis: `../../../../AFFILIATE/RC21_KATEGORIE_PRODUKTKACHELN_20261112.md`.

---

## 12.11.2026 – RC20 (0.1.17-rc20): IDEALO-FEED 2901 AUCH FÜR HAB FREIGEBEN

**Ursache eindeutig im echten HAB-004 RC19 nachgewiesen:** `idealo_settings()` hat `enabled=false` gesetzt, sobald **feed_id=2901** gespeichert war, auch bei korrekter Hab-&-Bewahr-Werbefläche `568944`. Der Idealo-Publisher zeigt Feed 2901 jedoch für 568944 an. Diese zusätzliche Sperre gegen vermeintlich fremde Pferde-Atelier-Werte war sachlich falsch.

**Korrektur im bestehenden HAB-004:** Sperre gilt jetzt nur für die wirklich fremde **Adspace 568313**, nicht für Feed 2901. Vollständige neue `CURRENT.zip` und benannte `HAB_AFFILIATE_RC20_0.1.17-rc20.zip`, 2.336.717 Bytes, 36 Einträge, SHA256 `532d3ef2552c44cc9652881e1ff943ad7bcd8ddd93fb779f5dab1d55a08b8d97`. Nur 3 Dateien geändert: Hauptdatei/Readme für Versionsnummer und `includes/trait-ppar-idealo.php` für Ursache. Alle 25 PHP-Dateien lintfrei, 36 ZIP-CRC OK; 5 echte PHP-Testfälle PASS, darunter Hab 568944/2901 erlaubt und fremde Adspace 568313 weiter gesperrt (GitHub-Actions 43240486920). Bestehende RC19-Versicherungsregeln bleiben unverändert.

**Noch offen:** WordPress-Installation und Live-API-Test. Nach Einbau den Haken „idealo-Verbindung verwenden“ bei Hab 568944/2901 setzen, „Speichern & API prüfen“. Öffentliche Idealo-Ausgabe zunächst aus; Auto-Refresh aus. Kein neuer API-Key erforderlich.

---

## 11.11.2026 – HAB-004 AFFILIATE RC19 (0.1.16-rc19) – VERSICHERUNGSBEREICH EXKLUSIV, LÜCKENLOS EIGENBANNER

**Vollständige CURRENT.zip als RC19-Kandidat im HAB-Pluginbüro gebaut:** 2.336.726 Bytes, 36 Dateien, SHA256 6d72fcd41a8b365e84815770014098946774bab7f2425c3546e48da66cd262f0 (nach bestandenem GitHub-Merge gültiger offizieller Current). Direkter, reproduzierbarer Build ausschließlich aus HAB-004 RC18 (0.1.15-rc18, verifizierte SHA256 a98063820d1564bf7cc7312c4c232369ac198bbaa49fbb6b173f76cd5096da89). **Nur vier bestehende Dateien im vollständigen Plugin verändert**: affiliate-portal-router.php, includes/trait-ppar-hb-amazon.php, assets/frontend.css, readme.txt. Keine neue Plugin-Identität, keine neue Tabelle, keine Änderung der sechs anderen Themenwelten oder des Designplugins HAB-001 RC19.

**Nutzer-Zielvertrag umgesetzt (offline):** Alle vorhandenen, aktiven Bannerplätze im Versicherungszweig von der R1-Hauptwelt über 5 R2, 46 R3, 323 Kategorien bis zu den eindeutig verknüpften Artikeln zeigen – wenn kein freigegebener Partnerbanner existiert – einen eigenen internen Hab-&-Bewahr-Versicherungs-Themenbanner. Der eigene Hinweis enthält einen aus dem aktiven Kategorie-Snapshot ermittelten internen R1/R2-Link, ist kein angebliches Tarifcheck-Angebot und hat keine erfundene Provision. Produktkarten-/Amazon-/Shop-Fallbacks werden im Versicherungszweig unterbunden; vorhandene 300×250- und 125×125-Originalbanner sind für passende Artikel/Glossar-Slots unverzerrt zulässig; 728×90 und 468×60 für entsprechende Versicherungs-Querbanner. Direktpartner Tarifcheck, Awin und ADCELL verwenden weiterhin die vorhandene zentral verwaltete Kampagnenauswahl. Ein echtes, freigegebenes allgemeines Versicherungsprogramm kann unterhalb exakt passender Programme als Fallback erscheinen; sonst eigener interner Themenbanner. Kein externes Frontend-HTTP und keine neue Werbe-Engine.

**Harter Runner-Test PASS:** 1.421 ausgeführte PHP-Funktionsprüfungen gegen 1 R1 + 5 R2 + 46 R3 + 323 Kategorien plus Beiträge / Gegenfälle, einschließlich Amazon/Finanzen-Sperre, Partner-Verbot, Freigabe allgemeiner Versicherungsvergleiche, internem Fallback in jedem geplanten Bannerplatz, 728×90 / 468×60 / 300×250 / 125×125 und Gegenproben auf eine fremde Welt. Alle 25 PHP-Dateien ohne Syntaxfehler, 36/36 ZIP-Inhalte mit CRC geprüft. GitHub-Actions-Run 43014867482; reproduzierbarer Build und echte PHP-Testquelle in AFFILIATE/IMPLEMENTIERUNG_RC19_INSURANCE.

**WICHTIGE GRENZE:** Die Tarifcheck-Partner-Bannercodes, echten Direktlinks, Rechnercodes und providerseitigen Freigaben wurden nicht übergeben. Die neue Version **erstellt keine erfundenen oder provisionsfähigen Tarifcheck-Anzeigen** und führt noch keinen Live-Test durch. Vor echtem Tarifcheck-Banner müssen Original-Werbemittel in der zentralen Affiliate-Zentrale freigegeben/zugeordnet werden. Die internen Themenbanner garantieren vorerst die optische Belegung. Vollständiger Vertrag: AFFILIATE/VERSICHERUNGEN_TARIFCHECK_KONZEPT_20261111.md Abschnitt 9. **WordPress-Installation/Liveabnahme OFFEN.**

---

## 09.11.2026 – WORDPRESS-SICHTABNAHME RC18: AMAZON-KACHELN PASS

Nutzer bestätigt die **Amazon-Kacheldarstellung** des Affiliate-Plugins RC18 als bestanden. Original-`CURRENT.zip` **unverändert**. Keine pauschale Funktionsabnahme von Tracking/Providern. Gemeinsames Protokoll: `../../ABNAHMEN/2026-11-09_WORDPRESS_DESIGN_RC19_AFFILIATE_RC18.md`. Ältere Vermerke über offene Live-Darstellung sind für diesen Punkt historisch.

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

# HAB-004 – Affiliate-Zentrale – CURRENT

## HAB-004 – RC9: Sieben Hauptwelten ohne Gesamtsperre

**07.11.2026 – HAB-004 0.1.6-rc9 (einzige aktuelle Voll-ZIP):** `PLUGINS/ISOLIERTE_PLUGINS/HAB-004-AFFILIATE/CURRENT.zip`, **618.212 Bytes, 28 Dateien**, SHA256 `04de5f4492887686c5a224640ffa5e4d64175927186dc3fe7f19d546e0ea4120`, Git-Blob `500d70b04607373a133966859de02b03ec7f62cb`.

**Harte Ursache:** Kategorienstruktur kennt sechs bestehende Welten plus `core:world:insurance` (siebte Welt), aber RC8 verlangte exakt sechs. Original-RC8 mit sieben Hauptwelten reproduzierbar `hb_worlds_unexpected`. Die 2.720 Knoten/2.714 Bindungen sind Live-Screenshot-Werte, kein heruntergeladener WP-Datenbankabzug.

**KISS-Korrektur:** Es wird nur verlangt, dass mindestens eine gültige gemappte Hauptwelt existiert; Welt- und Bereichszahlen folgen dem tatsächlich aktiven Bestand. Eine zusätzliche oder nicht gemappte einzelne Welt blockiert die restlichen Welten nicht. Bei vollständig fehlendem/ungültigem Snapshot werden weiterhin sicher keine kostenpflichtigen Aufträge gestartet. Der Affiliate-Hauptschalter `ppar_enabled` bleibt unverändert und muss bei Bedarf in WordPress (`Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv`) ausdrücklich aktiviert werden.

**Echte lokale Prüfungen:** 116 vollständige Original-Plugin-/Design-WP-Simulationen (6/7/8 Welten, 2.720 Knoten/2.714 Mapping, Klick→DataForSEO-Mock→ASIN→Speicherung→R3-/Kategorie-Ausgabe, 1 Welt ohne Mapping, falsche Revision, Altwerbe-Vorrang, global AUS); 104 DataForSEO-Worker-/Kosten-/Fehler-/Beitragstests mit sieben Welten; 96 Regressionstests; **316 PASS, 0 FAIL, keine PHP-Warnungen**, **25/25 PHP-Lints**, **ZIP 28/28 CRC**. 25/28 Plugindateien gegenüber RC8 identisch. Kein echter WordPress-Produktivlauf oder bezahlter DataForSEO-API-Auftrag. Dokument: `AFFILIATE/IMPLEMENTIERUNG_RC9/PRUEFBERICHT.md`, minimaler Patch `RC8_TO_RC9_SOURCE_DIFF.patch`.

**Nächster Schritt:** RC9 in WordPress als Update des bestehenden Plugins einspielen. Wenn die oben sichtbare Meldung „Affiliate-Zentrale insgesamt ausgeschaltet“ besteht, über `Affiliate-Zentrale → Übersicht → Hauptschalter → Affiliate-Automatik aktiv → Einstellung speichern` einschalten. Erst dann unter `Amazon-Automatik` einmal `Jetzt einen Suchlauf starten`; der Status muss zeigen, ob ein Auftrag erzeugt wird, ein Fehler vorliegt oder bereits geprüft ist. Max. fünf neue kostenpflichtige DataForSEO-Aufträge/UTC-Tag. Die Live-Wirkung erst danach bestätigen.

---



Letzte Version ist einzig die genannte RC9-Voll-ZIP; ältere RC8/RC7/RC6 nur in Git-Historie. Das Kategorieplugin, Designplugin, Bildzentrale, Pferdeatelier und Hobbydepot bleiben unverändert.
