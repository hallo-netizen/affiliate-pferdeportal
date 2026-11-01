# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: **HD-003 1.50.791 EXAKT FREIGEGEBENE BANNERPIXEL IM VOLLPLUGIN / LOKAL ZIP+PHP+CHROMIUM PASS / WORDPRESS-LIVE OFFEN / LIBRARY-SPEICHERLIMIT**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

Fehlerautorität:
`../../../DESIGN/FEHLERQUELLEN.md` → `HRD-078`

Historie / WAS+WARUM:
`../../UPDATEPROTOKOLL.md` → `PU-20261024-001`

## AKTUELLER BELASTBARER STAND
- letzte ältere Campus-Deklaration vom 24.10.: **1.50.744**, nicht als neue aktuelle Installationsbasis zu verwenden;
- Root-only-Ziel der Anzeigenmarkt-Startseite ist dokumentiert: Breadcrumb → Banner → eigener Anzeigenmarkt-Hero → reine Anzeigen-Suche → 8 Fotokacheln → „Aktuelle Anzeigen“ → nativer HivePress-Anzeigenbestand;
- Kategorie-/zweite Ebene bleibt vorerst nativ;
- Live-PASS für 1.50.744 liegt nicht vor.

Dokumentiertes 1.50.744-Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.744_ANZEIGENMARKT_STARTSEITE_HARDPASS.zip`

Dokumentierter SHA-256:
`72b048db7516640e19f4432aaf98f5d4fa6ca9cc2fd26964a421e2ac1eece6b8`

## ERSTER OFFENER BLOCKER
Die exakten 1.50.744-ZIP-Bytes sind im Abschluss-Frischecheck nicht materialisierbar. Dadurch können SHA/Fresh-Unpack nicht erneut geprüft und `ISOLIERTE_PLUGINS/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.zip` nicht synchronisiert werden.

## ARBEITSBINDUNG
- keine neue HD-003-Designänderung oder Deploymentausgabe aus 1.50.744, solange das exakte Artefakt nicht wiederhergestellt ist;
- 1.50.743 ist nur letzter aktuell materialisierter ZIP-Stand, **nicht** neue Current-Autorität;
- keine Rekonstruktion auf Verdacht;
- Header/Footer-1440 und zentrale Body-Achse 1200 nicht nebenbei verändern.


## NEUER FUND / FRISCHECHECK 01.11.2026

In der vorhandenen Projekt-Dateiablage ist der tatsächliche **Dateieintrag** `/hobby rausch/HOBBY_DEPOT_HD003_1.50.785_ORIGINALLOGO_VERIFIZIERT_VOLLPLUGIN.zip` mit **63.407.568 Bytes** vorhanden. Ebenso vorhanden: die Vorversion 1.50.784 und `HOBBY_DEPOT_HD003_1.50.785_LOGO_PRUEFBERICHT.txt`. Der Bericht dokumentiert ein Favicon aus dem Originalpinselbogen und ausgeschnittenem H/D, 11/11 PHP-Lints und ZIP-Integritätsprüfung im Vorlauf, aber **keinen WordPress-Live-PASS**.

**Harte Prüfgrenze:** Die Datei wurde diesmal nicht als echte ZIP gelesen. Die Rohdatei-Bereitstellung verweigerte mit `This Project file does not have an authorized raw-byte materialization path.`; Textleseversuch meldete `No readable content was found in this file for the requested mode.`. Daher **kein neuer SHA-/ZIP-/Dateibestand-/Funktionsvergleich, keine vollständige neue Simulation**. Auch 1.50.782 wurde lediglich als GitHub-Prüfbeleg vorgefunden; dort steht ausdrücklich „Campus-ZIP noch nicht eingespielt“.

**Keine Herabstufung auf 1.50.744 oder 1.50.782, kein unechtes CURRENT.zip.** Der neueste aufgefundene Kandidat 1.50.785 bleibt bis zum echten Wiederöffnungs-/Prüf-PASS lediglich **Dateifund, nicht freigegebene Campus-Binärversion**.

## WordPress-Inventarabgleich 01.11.2026

Die vom Betreiber gelieferte vollständige WordPress-Pluginliste zeigt **Version 1.50.783 als aktiv**. Der zuvor dokumentierte Entwicklungs-/Teststand 1.50.785 ist nicht mit der aktiven WordPress-Version gleichzusetzen. Ein unabhängiger Server-Quellcode-/ZIP-Readback und ein Live-Funktionstest wurden in diesem Abgleich nicht ausgeführt. Keine Plugininstallation oder Campus-CURRENT.zip-Synchronisierung. Beleg: `../../EVIDENCE_WP_PLUGINLISTE_20261101.md`; operative WordPress-Current: `../../../WORDPRESS_TECHNIK/CURRENT_STATE.md`.

## NEUE VERSION – EXAKTER FREIGABE-/PRÜFNACHWEIS

## 01.11.2026 – HD-003 1.50.786: Favicon + Anzeigenmarkt-Banner

**Version in WordPress laut Betreiberliste: 1.50.783 – unverändert.** Neue freigabefähige Installations-ZIP: **1.50.786**, noch nicht auf WordPress installiert; kein Live-Funktions-PASS.

Die neue Voll-ZIP wurde **direkt aus der vollständigen 1.50.785** gebaut. Zusätzlich wurde die vom Betreiber gemeldete 1.50.783 als Rückfallbasis unabhängig geöffnet und mit 1.50.785 abgeglichen. Das freigegebene Original-Favicon wurde aus `hobby_depot_favicon_original_korrigiert_transparent.png` übernommen – **keine Neuzeichnung**. Aus der Originalkomposition wurden PNG-Größen 16/32/48/64/180/192/512 sowie ICO für die vorhandenen Favicon-Dateipfade generiert. Das Headerlogo-Bild ist byte-identisch zur 1.50.785.

**Anzeigenmarkt-Startseite:** bestehende Banner-Ausgabe direkt nach Breadcrumb entfernt und in der ursprünglichen Reihenfolge **Suche → Banner → 8 Kategorie-Kacheln** zwischen Suche und Kategorie-Kacheln verschoben. Gleicher Slot `anzeigenmarkt_top_banner`, keine zweite Engine, keine neue Kategorie- oder Providerlogik. Unterseiten werden weiterhin durch die vorhandene Market-Root-Bedingung ausgeschlossen.

**QA real ausgeführt:** Ausgangs-ZIPs 1.50.783/1.50.785 vollständig geöffnet und ZIP-CRC gelesen; 1.50.783→1.50.785: 8 neue Favicon-Bilddateien und 2 geänderte PHP-Dateien. Ausgabe 1.50.786 vollständig erneut geöffnet: **1.281/1.281** ZIP-Einträge korrekt; **1.271** Einträge gegen 1.50.785 byte-identisch, **10** gezielte Änderungen (8 Favicon-Assets + 2 PHP-Dateien); **11/11 PHP-Syntax PASS**. Markt-Seiten-Positiv/Negativ-Simulation mit der wirklichen Renderfunktion: Hero→Suche→Banner→Kacheln→Anzeigen PASS; Banner genau einmal PASS; 8 Karten PASS; leere Anzeige für Besucher versteckt PASS; eingeloggte Vorschau PASS; Nicht-Markt-Seite PASS; Taxonomie-Unterseite PASS; keine Kategorien PASS. **Kein echter WordPress-Live-Test**.

**Dauerhafte Original-/Sicherungsablage (vollständige Binär-ZIPs):**
- Original 1.50.783: Library `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HD003_1.50.783_ORIGINAL_RUECKFALLKOPIE.zip`.
- Original 1.50.785: Library `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HD003_1.50.785_ORIGINALLOGO_VERIFIZIERT_VOLLPLUGIN.zip`.
- Neue 1.50.786: Library `/Hobby Depot/Plugin-Büro/HOBBY_DEPOT_HD003_1.50.786_FAVICON_UND_ANZEIGENMARKT_VOLLPLUGIN.zip`.
- Unabhängige Rückfallkopie 1.50.786: Library `/hobby rausch/HOBBY_DEPOT_HD003_1.50.786_FAVICON_UND_ANZEIGENMARKT_RUECKFALLKOPIE.zip`.

**Unabhängige Rückleseprüfung:** Nach dem Upload wurden beide 1.50.786-Library-Kopien über ihren jeweils eigenen neuen File-Eintrag neu materialisiert, als vollständige ZIP geöffnet, 1.281/1.281 Dateien geprüft, Größe, Pluginroot, Hauptdatei und Version geprüft. Beide **63.369.310 Bytes** und SHA-256 `25d8b1ea701139a2cd9b4e4f1cbdcabaa12548f7b2fc2407da8ac44fe58abc3a`. Die beiden gespeicherten Dateien sind byte-identisch zur lokal gebauten ZIP. **Library-Abnahme PASS, GitHub-ISOLIERTE_PLUGINS/CURRENT.zip noch nicht synchronisiert.** Metadaten im GitHub-Campus ersetzen keine ZIP-Bytes.

**NEXT ACTION:** Die fertig geprüfte **1.50.786 Voll-ZIP** in WordPress über die Plugin-Installation mit Ersetzen der installierten **1.50.783** einspielen, danach das Favicon im echten Browser und die Anzeigenmarkt-Seite (Suche→Banner→Kacheln, leere Banner/Unterseiten) prüfen. Keine zweite Installation, keine Änderung an anderen Portalen. Ein tatsächlicher Live-PASS erst nach WordPress-Readback.


## 01.11.2026 – HD-003 1.50.789: Suchergebnisse kompakt + Artikel-Hero

**NEUER INSTALLATIONSKANDIDAT: Version 1.50.789.** Vollständiges Plugin im aktuellen Chat unter `HOBBY_DEPOT_HD003_1.50.789_SUCHERGEBNISSE_ARTIKELHERO_VOLLPLUGIN.zip`, lokaler ZIP-Readback 1285/1285 PASS; 13/13 PHP-Lint PASS; vorheriger 1.50.788-Voll-ZIP-Vergleich: **1280 Einträge unverändert, 3 geänderte PHP-Dateien, 2 zusätzliche PHP/Text-Dateien**, Original-Headerlogo und Originalfavicon byte-identisch. SHA-256 **b89784c8ba9296e5f8faf771f2a258565839da7896d5a55f4b4b03019b460b79**; 63.815.168 Bytes.

**Kritische UI-Korrektur 1: Suchergebnisseite.** Einzige bestehende Hauptsuche bleibt zuständig; kein neuer Index, kein zweiter AJAX-Endpunkt. Pro Bereich zunächst fünf Treffer. Jeder Klick auf „Mehr anzeigen“ legt fünf weitere der maximal 50 bestehenden Treffer frei; Button verschwindet nach letztem Treffer. Ruhige zweispaltige Karteikartenansicht mit Trefferzahl; fünf Bereiche Hobbys, Fachwissen, Magazin, Glossar, Anzeigen erhalten. Detail: `includes/class-hobby-depot-profile-v150709.php`, bestehendes `templates/hobby-depot-search-v150732.php`.

**Kritische UI-Korrektur 2: Artikel oben.** Breadcrumb → genau ein H1-Titel oberhalb → breitflächiges Foto-Hero → Artikeltext. Das Hero wird aus dem vorhandenen WordPress-Beitragsbild (Priorität) oder erstem echten Inhaltsbild gespeist und vermiedene Bildduplikate verborgen. Text ist *niemals* ins Foto eingebrannt: links heller automatischer Farbverlauf, links grüner, kurzer Claim plus weicher verwischter Bogen, Fotomotiv möglichst rechts. Kein Pseudofoto bei fehlendem Bild. Textlieferung kann das EINZIGE Beitragsmetafeld `_hd_article_hero_claim` setzen; ohne Feld wird ein kurzer Auszug verwendet. Regeln für spätere Bildzentrale/Texterstellung stehen **im Plugin** unter `ARTIKELBILD_REGELN_150789.txt`: Motiv rechts, links ruhiger Hintergrund, kein Text im Bild. Die Datei ist eine Regelvorgabe und **keine bereits technisch implementierte Änderung am separaten Bildzentrale-Generator**. Nur der Hobby-Depot-Zweig verwendet die neue Hero-Vorlage, nicht Pferdeatelier oder andere Designprofile. Gespeicherter veröffentlichter Artikel wird nicht verändert, seine Tabellen, Werbebanner, Listen und Produktbereiche bleiben erhalten. Der Legacy-Pferde-Artikelheader-Umordner wird für Hobby Depot übersprungen.

**Positiv-/Negativprüfung lokal:** realer Suchgruppen-Code vom Vorrelease gegen Fachartikel, Fachkategorien, CORE-Seiten, Entwurf, Magazin-Dopplung und Nulltreffer erneut PASS. Neue Suchergebnisse: 12 Treffer → nur 5 sichtbar, 7 verborgen, exakt ein aktivierbarer Mehr-Button; 3 Treffer → kein Button; Nulltreffer; Freigabelogik PASS. Header: erstes Inhaltsfoto, neues Beitragsbild, Claim aus Meta, generischer Fallback ohne Foto, genau ein H1 und ein Hero, Überschrift oberhalb, sonst keine Änderung des bestehenden Inhalts PASS. Alle 13 PHP-Dateien fehlerfrei. **Kein WordPress-Livebrowser-Readback für 1.50.789.**

**Speicherung:** Die ChatGPT-Library hat zuletzt beim Versuch, 1.50.788 als Voll-ZIP zu speichern, das Speicherlimit gemeldet. Für 1.50.789 liegt deshalb **keine neu bestätigte dauerhafte Library-/GitHub-Original-ZIP vor**. Das tatsächlich erzeugte und überprüfte vollständige ZIP ist nur als downloadbarer Anhang im aktuellen Chat gesichert; ältere 1.50.787-Rückfallkopie bleibt erhalten. Diese GitHub-Metadaten ersetzen nie ZIP-Bytes.

**NEXT ACTION:** Vollständiges HD-003 1.50.789 im WordPress-Backend über die vorhandene Designplugin-Installation aktualisieren, danach Suchseite „Zweileiner“ und veröffentlichten Testbeitrag am Desktop/Mobil visuell abnehmen. Erst danach Betreiber-Live-PASS.

## 2026-11-01 – HD-003 Vollplugin 1.50.790: Eigenwerbung auf direkt vermietbaren Bannerplätzen

**Quelle:** echte 1.50.789-Voll-ZIP aus dem aktuellen Pluginstand. Daraus **1.50.790 Voll-ZIP** erstellt, Pluginroot `affiliate-portal-template-kit/` unverändert. Ausgabe im aktuellen Chat: `HOBBY_DEPOT_HD003_1.50.790_EIGENWERBEBANNER_ORIGINALLOGO_VOLLPLUGIN.zip`.

**Genau der beauftragte Umfang:** nur der bestehende `rental_slot($placement)`-Pfad des Designprofils Hobby Depot für *noch nicht gebuchte* direkt vermietbare Werbeflächen, inklusive responsive CSS. Freier Platz zeigt neues Eigenwerbemotiv Modellflugzeug/Werkstatt mit beigem Übergang, originalem aus dem aktiven Plugin geschnittenen Logo ohne Unterzeile, Überschrift „Hier könnte Ihre Werbung stehen“, exakt zwei voneinander unabhängigen HTML-Links „Werbebedingungen“ und „Preise“. Keine weitere Unterzeile, kein grelles Grün. Kein nachgezeichnetes Logo. Die Links werden nur mittels `get_page_by_path` und `get_permalink` aus echten veröffentlichten WP-Seiten aufgelöst: Bedingungen bevorzugt `werbebedingungen`/`werb-anzeigebedingungen` inkl. bekannter Varianten; Preise `preise`. Fehlt eine Zielseite, zeigt der Button seinen deaktivierten Zustand ohne erfundenes Linkziel; der echte WordPress-Pages-Readback ist noch offen.

**Harte Abgrenzung:** Bei aktiv gebuchtem Mietslot mit echter Kundenbild-URL/Ziel-URL bleibt das bisherige Kundenbanner völlig unverändert, ebenso der Provider-Filter `pftk_hobby_rental_slot_html`. Die bereits vorhandene zentrale Einmal-Regel `render_rental_for` bleibt erhalten (maximal ein Mietbanner pro Seite). Kein zweiter Werbebanner-Worker, keine Änderung der Affiliate/Partner-Slots, keine Änderung des Pferdeatelier-Zweiges, von Kategorien, Hero oder Suchfunktion.

**Veränderte Dateien im Vollplugin:** exakt zwei PHP-Dateien (Hauptplugin nur Version, Hobby-Profil Version + Austausch der freien Mietbanner-HTML und Ergänzung ausschließlich dazugehöriger CSS) und zwei neue Assets unter `assets/hobby-depot-v150617/eigenwerbung-v150790/`: `logo-original-ohne-unterzeile.png` als unveränderte Original-Pixel des 640×372-Logos, nur auf 640×315 beschnitten; `modellflugzeug-werkstatt.webp` als Ausschnitt aus dem vom Betreiber freigegebenen Modellflugzeug-Banner, ohne eingebrannte Buttons/Schrift. **1283/1285 alte Originaldateien byteidentisch**, neue ZIP enthält **1287/1287** korrekt lesbare Einträge.

**Simulation/QA:** PHP 13/13 Syntax PASS, ZIP CRC 1287/1287 PASS; Privatmethode `rental_slot` anhand des echten Codes mit WordPress-Stub ausgeführt: freie Fläche hat zwei voneinander verschiedene richtige Links, reservierter Platz verwendet Kundenwerbung statt Eigenbanner, Provider-Override unverändert, fehlende Werbebedingungsseite erzeugt keinen falschen Link, doppelte Mietbannerdarstellung wird blockiert – alles PASS. Visualisierung mittels tatsächlichem gerendertem PHP-/CSS-HTML in Chromium bei Desktop 1200px und Mobil 390px; beide Links vorhanden, kein Überlauf. Vorschauen im aktuellen Chat: `HOBBY_DEPOT_WERBEBANNER_1.50.790_VORSCHAU_1200px.png` und `..._390px.png`.

**ZIP-Readback:** SHA-256 `39953565ba8e9d81e5630255f54cee04fe150c54b68b78ad9c5a8ef639dbe9db`; 64.035.283 Bytes. **Kein echter WordPress-Live-PASS**. Die zuletzt bekannte ChatGPT-Library hat Speicherlimit signalisiert; dort ist 1.50.790 nicht als gespeichert verifiziert. Das dokumentierte GitHub-Campus-Protokoll ist **nicht** das Binär-ZIP. Frühere 1.50.789-ZIP und 1.50.787-Library-Backup bleiben erhalten.

**EXAKT NÄCHSTER SCHRITT:** 1.50.790 als *Update des vorhandenen HD-003* installieren; auf einer noch freien mietbaren Werbefläche beide Buttons im echten WordPress-Frontend überprüfen (Ziel-URL, Erreichbarkeit) und eine gebuchte Fläche auf unveränderte Kundenwerbung prüfen. Keine weiteren Pluginänderungen vorher.

## 2026-11-01 – HD-003 1.50.791: freigegebenes Eigenwerbebanner pixelgenau ohne Zoom/Beschnitt

**Grund der Nachbesserung:** 1.50.790 nahm aus der zuvor abgenommenen Gesamtgrafik rechts einen Bildausschnitt und dehnte ihn per `object-fit:cover` zum Hintergrund. Dadurch entstand ein gezoomtes, von der Freigabe abweichendes Bild. Der Betreiber hat dies ausdrücklich beanstandet. **1.50.790 soll daher durch 1.50.791 ersetzt werden.**

**Exakte Originaldatei:** `/mnt/data/werbebanner_mit_modellflugzeug_und_logo.png` (vom Betreiber abgenommener Entwurf ohne Logo-Untertitel), 2170×725 Pixel, SHA-256 `3cc834d9f67305ce752574b794d834b4b20304ada93eb1518bbae6fd2eb8e579`. Dieses **identische Original-PNG** liegt in 1.50.791 unter `affiliate-portal-template-kit/assets/hobby-depot-v150617/eigenwerbung-v150791/banner-freigabe-originalbild-2170x725.png`. Der ZIP-Inhalt wurde unabhängig und bitgleich zur Freigabedatei geprüft. **Kein Crop, Zoom, Farbwechsel, Logo-Neuzeichnen oder neue Beschriftung.**

**Darstellung:** Freigegebenes Gesamtbild komplett in originalem Seitenverhältnis (2170:725), responsive nur proportional skaliert, `object-fit:contain`. Die beiden bereits ins Bild integrierten Buttons sind über **unsichtbare**, exakt passend positionierte Klickflächen verlinkt. Die URLs stammen nur aus real veröffentlichten WordPress-Seiten (`werbebedingungen` bzw. `preise`, mit bekannter vorhandener Pfadauflösung). Bei fehlender Seite wird der entsprechende Hotspot deaktiviert – niemals erfundener Link. Keine erneute sichtbare Button-/Logo-/Textauflage. Kundenbuchungen und `pftk_hobby_rental_slot_html`-Provider-Hook behalten Vorrang; Einmalregel unverändert.

**Unverändert:** 1.285/1.287 ursprüngliche ZIP-Einträge byteidentisch; genau zwei geänderte PHP-Dateien (Version / Mietslot-Eigenwerbung und CSS); genau eine neue **bitidentische** Original-PNG (die zwei alten Assets bleiben unangetastet, werden nicht mehr verwendet). 13/13 PHP-Syntax PASS; 1.288/1.288 ZIP CRC PASS. Mit echter PHP-Klassenmethode Positiv/Negativ getestet: zwei verschiedene korrekte Links, fehlende Bedingungen ohne Link, gebuchte Werbefläche weiterhin Kundenanzeige, Provider-Override weiterhin Vorrang. Chromium-Layoutprüfung 1200px und 390px: gesamtes Bild im Originalverhältnis, kein abgeschnittener Bildbereich, beide Klickzonen über den gezeigten Buttons.

**Downloadbares vollständiges WordPress-Designplugin im aktuellen Chat:** `/mnt/data/HOBBY_DEPOT_HD003_1.50.791_FREIGEGEBENES_BANNER_EXAKT_VOLLPLUGIN.zip` (65.646.341 Bytes, SHA-256 `1266ed354811eec85263a431b15a206904cd2bf148934908bb79a2675a2ccde7`). **Keine erneute Library-Speicherung behaupten:** Der Library-Plugindateispeicher meldete zuletzt sein Speicherlimit. Github-Textprotokoll ist keine Binär-ZIP-Synchronisierung. Kein echter WordPress-Live-PASS für 1.50.791.

**Nächster Schritt:** 1.50.791 als Full-ZIP-Update des vorhandenen HD-003-Plugins installieren. Die frei mietbare Bannerfläche mit der freigegebenen Gesamtgrafik 1:1 abgleichen und beide echten Buttons im WordPress-Frontend prüfen; Kundenwerbung nicht verändern. Keine anderen Bereiche anfassen.
