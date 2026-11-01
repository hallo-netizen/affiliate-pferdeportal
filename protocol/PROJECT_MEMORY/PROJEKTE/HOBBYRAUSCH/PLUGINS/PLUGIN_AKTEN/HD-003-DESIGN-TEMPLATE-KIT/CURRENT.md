# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-11-01
STATUS: **1.50.783 laut Betreiber installiert / 1.50.786 Vollplugin lokal PASS und dauerhaft wiedergeöffnet / LIVE-INSTALLATION OFFEN / GITHUB-CURRENT.ZIP OFFEN**

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

