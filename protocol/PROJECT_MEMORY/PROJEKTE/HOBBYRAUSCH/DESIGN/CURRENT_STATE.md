# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: **HD-003 1.50.789 ARTIKEL-HERO UND 5ER-SUCHERGEBNISSE LOKAL PASS / LIVE-VORSCHAU/ABNAHME OFFEN**

Zielvertrag:
`ZIELVERTRAG_HOBBY_DEPOT_DESIGN_20261011.md`  
**ZV-HOBBYRAUSCH-DESIGN-001 / Fassung 5.5 / 2026-10-19**

Plugin-Current:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/CURRENT.md`

Fehlerautorität:
`FEHLERQUELLEN.md` → `HRD-078`

Historie / WAS+WARUM:
`../PLUGINS/UPDATEPROTOKOLL.md` → `PU-20261024-001`

## AKTUELLER BELASTBARER STAND
- ältere Campus-Deklaration vom 24.10.: **1.50.744**; neuer aufgespürter Dateieintrag 1.50.785, echter Byte-Readback noch nicht möglich;
- Anzeigenmarkt-Startseite ist als **Root-only**-Ausbaustand dokumentiert;
- Zielreihenfolge: Breadcrumb → Banner → eigener Anzeigenmarkt-Hero → reine Anzeigen-Suche → 8 Fotokacheln → „Aktuelle Anzeigen“ → nativer HivePress-Anzeigenbestand;
- doppelte native HivePress-Root-Oberfläche soll auf Root nicht erscheinen;
- zweite/Kategorieebene bleibt vorerst nativ und ist noch nicht gestaltet;
- Live-PASS für 1.50.744 ist **nicht** belegt.

## ERSTER OFFENER BLOCKER
Der aufgefundene 1.50.785-Kandidat ist weiterhin nicht als echte ZIP unabhängig wiedergeöffnet und nicht in der isolierten Campus-Ablage gesichert. WordPress meldet 1.50.783 als aktiv; ihr realer Dateibestand ist noch nicht mit 1.50.785 verglichen.

## NICHT ANFASSEN
- zentrale Hobby-Depot-Body-Achse: 1200 px;
- Header/Footer-Achse: 1440 px;
- Hobbyregister-Layout HD-007 nicht nebenbei verändern;
- Glossar- und Register-Core nicht löschen; beide bleiben Runtime-Komponenten;
- keine neue Service-Template-/Kubio-Runtime-Architektur.


## WordPress-Version und Favicon / Nachholcheck 01.11.2026

- Die Betreiber-Pluginliste beweist als übermittelte Admin-Ansicht: **Affiliate Portal Template Kit 1.50.783 aktiv**. 1.50.785 steht nicht in dieser Liste und darf nicht als installiert behauptet werden. Ein eigener authentifizierter Server-Readback wurde nicht ausgeführt.

- 1.50.785-Vollplugin-Dateieintrag vorhanden, in `/hobby rausch/`, nicht im autoritativen Campus-`ISOLIERTE_PLUGINS`-Zielordner.
- Die Originalbogen-/H-D-Vorschau ist als vorhandenes Bild lesbar; keine Neugenerierung und kein fremder Schrift-Ersatz.
- Prüfbericht 1.50.785 spricht von 11 PHP-Syntax-PASS und ZIP-Integrität, **nicht** von nachgeprüfter Liveinstallation.
- Aktueller Rohdateizugriff gescheitert; kein neues unabhängiges Unzip/Hash und kein Campus-CURRENT.zip. Details stehen ausschließlich in der HD-003-Plugin-Current und deren MANIFEST.
- Anzeigenmarkt-/Kategoriearbeit bleibt bis zum Plugin-Wiederöffnen unverändert; keine Rücksetzung auf eine alte 1.50.744-Datei.

## 01.11.2026 – neue 1.50.786

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
