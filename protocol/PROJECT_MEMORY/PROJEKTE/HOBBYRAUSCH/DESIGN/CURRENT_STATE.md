# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: **HD-003 1.50.786 FAVICON UND MARKT BETREIBER-PASS / 1.50.787 ARTIKELDESIGNTEST VOLL-ZIP GEPRÜFT / FRONTEND-TEST DES ARTIKELS OFFEN**

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

