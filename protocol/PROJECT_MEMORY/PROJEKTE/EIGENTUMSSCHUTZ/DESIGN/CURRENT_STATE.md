# HAB & BEWAHR – DESIGN – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **ZWEI UNGEWOLLT GETRENNTE DESIGN-PLUGINS GEMELDET – KONSOLIDIERUNG IN DAS BEREITS EXISTIERENDE DESIGN-PLUGIN VERBINDLICH; WORDPRESS-LIVE-VERSION/BASENAME/AKTIVIERUNG UNBESTÄTIGT; KEINE WEITEREN PLUGINS INSTALLIEREN**

## NEUE VERBINDLICHE ENTSCHEIDUNG – 14.10.2026 (Vorrang vor älteren Abschnitten)

**Genau EIN Plugin für das GESAMTE Hab-&-Bewahr-Design.** Zielname in WordPress: **„Hab & Bewahr – Design“**. Startseite = erster Baustein, später dieselbe Pluginbasis für Header, Welten, Bereiche, Kategorien, Magazin, HivePress-Dienstleister und Beitragsseiten. **KEINE eigenständigen Zusatzplugins pro Seitentyp.**

**Konsolidierungsfehler:** Nach vorherigem Design-Vorschau-Plugin `HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.3_TEXTMENUE_KLARE_THEMEN.zip` wurde separat `HAB_UND_BEWAHR_STARTSEITE_0.1.0.zip` mit eigener Plugin-Identität/Ordnerstruktur erzeugt und dem Nutzer zum Installieren gegeben. Nutzer zeigt zwei unterschiedliche Plugins im WordPress-Backend. Dies ist unerwünscht. Die Startseite darf **NICHT** dauerhaft eine zweite Plugin-Identität bilden. Der neue Startseiten-Entwurf ist **kein** freigegebener vollständiger Ersatz für die ältere breitere Pluginfunktion; es fehlen dessen Originalquelldateien hier. Kein drittes Plugin bauen, keine Neuinstallation als „Design v0.2“, kein Blind-Deaktivieren, keine Aktivierungs-/Live-Behauptung.

**Richtiger technischer Pfad:** Bestehende umfassende Design-Vorschau als **einzigen** Weiterentwicklungsträger übernehmen und **dieselbe installierte Plugin-Identität / dasselbe Plugin-Verzeichnis / denselben Updatepfad** behalten; nur den Anzeigenamen zu „Hab & Bewahr – Design“ ändern. Das Startseitenmodul dort integrieren, nicht separat betreiben. **Erst** nach In-Place-Update, Funktions-/Performanceprüfung und Kontrolle, dass keine Seite auf den separaten Shortcode `[habundbewahr_startseite]` angewiesen ist, das zusätzliche Startseitenplugin deaktivieren und anschließend optional löschen. Kein Verlust bestehender Templates oder URLs.

**Design-C-Lock:** Header-Variante C gewählt, Schutzbogen schlank, mittelhoch und etwas flacher als vorher, spitz auslaufend, Terrakotta. Claim **„Schütze dein Eigentum“ ohne Punkt**, optisch deutlich von der Wortmarke abgesetzt, schmale gesperrte Großbuchstaben; zentriert. Zusatz über Navigation: **„Dein Ratgeber für Schutz & Sicherheit“**, auf Mobil sichtbar. Sichtbare dünne Linie unter der Navigation, breiteres Suchfeld, größere Nav-Begriffe. Die ursprünglichen **ersten Kacheln** sollen erhalten bleiben: **nicht** behaupten, dass das eigenständige Startseitenplugin sie bereits korrekt übernommen habe; Originallayout erst aus Originaldatei verifizieren. Terrakotta `#B35C40`, Salbei ergänzend `#65745F`, Hintergrund `#FAF8F4`.

**Höchste technische Priorität: PERFORMANCE-SCHONEND** für JEDES Designplugin und künftige Pluginanbindung:
- Kein mit jeder Anfrage durchlaufender Kategorie-Workflow oder Struktur-Scan; Kategorie-Daten über zentrale bestehende Live-Bindung/Registry lesen.
- Keine Backgroundjobs, SEO-/Providerabfragen, Massen-WP-Abfragen, unnötige Aktivierungswrites oder Site-Wide-Hooks für reine Darstellung.
- CSS/JS nur für benötigte Seiten/Ansichten laden; klein und möglichst ohne Dritt-Abhängigkeiten; keine zweite Template-Engine, kein Parallel-Rendering.
- WordPress-/DB-Cache nutzen, nur echte Revision-/Inhaltswechsel invalidieren; keine DB-Massenabfragen in Menüs, Kacheln oder Header pro Aufruf.
- Lokale Messung von Abfragen, Ladezeit, Speicherbedarf vor Freigabe gegenüber vorhandener Pluginversion; positiver/negativer Regressionstest.
- Keine Architektur-/WordPress-Kategoriewrites und keine Änderungen an anderen Plugins als Nebenwirkung.

**Aktuelle gesicherte Struktur:** R3/V8 WordPress-Readback 546/546 PASS (6 Welten, 31 Bereiche, 93 Unterbereiche, 285 CORE-Blätter); keine Neu-Synchronisierung. Operative Kategorie-Autorität: `../KATEGORIEN/CURRENT_STATE.md`.

## Ziel / bindende Nutzerentscheidung **(historische Vorschau-Entscheidung vom 13.10.2026, durch aktuellen Design-C-Lock ersetzt)**
Erst eine **grobe Visualisierung** der bestehenden echten Website-Struktur, keine fertige CI/SEO-Produktion. Grobe Orientierung am Hub-/Kartenaufbau des Hobby-Depot-Design-Plugins; keine Architekturübernahme. Farbwelt warmes Terrakotta, Salbei, Anthrazit, cremefarbener Hintergrund. Wortmarke **Hab & Bewahr** mit Bogen, Claim **„Wissen. Vergleichen. Besser schützen.“**; Hero **„Was dir gehört, soll dir bleiben.“**. Sechs Gefahrenwelten + Magazin + Dienstleister, vorhandenes R2-Profil. Vier echte, eindeutig markierte Testartikel; dieselben Beispiele nur als Kacheln auf anderen Kategorieebenen.

## Aktueller Kandidat (nur Chat-Artefakt)
`HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.3_TEXTMENUE_KLARE_THEMEN.zip`
SHA-256: `f7cd98459fba15fb0d2ec61cb0c837a6d4e77708ae22f910aba8efa7b0d894b8`

- Eigener deaktivierbarer Visualisierungsplugin, ohne Eingriff in HD-001.
- Echtgebundene 354 WP-Zielobjekte / 141 CORE-Kategorien aus R2-Readback vom 2026-10-12, Status COMPLETE/PASS.
- Dynamische Seitenhierarchie per vorhandenen Objekt-IDs.
- Vier DEMO-Artikel werden einmalig bei Aktivierung erstellt, je eine vorhandene CORE-Kategorie. `noindex`; bei Deaktivierung in Entwurf. Kein Content-Massenimport.
- Startseite, 6 Weltseiten, Unterhubs, Terminalkategorien, Demo-Artikelseite; Layoutbeispiele für Magazin und Dienstleister.
- **0.1.2 – Vollständiges Megamenü:** sechs Welten als Hauptnavigation. Pro geöffnetem Menü werden **alle zugehörigen Bereiche, Unterbereiche und die 141 Blattkategorien als direkte Links ohne zweite Klickstufe** ausgegeben. Umfangreiche Menüs scrollen innerhalb des Panels; Desktop auch per Hover, mobil per Klick. Keine Änderung des R2-Profils.
- **0.1.3 – Vereinfachung:** komplette Navigation in vier schlichten Textspalten **ohne Karten/Rahmen/Symbole** und ohne zweite Aufklappstufe; echte 6/31/45/141 Links. Für Start- und Weltseiten konkrete verständliche Gefahren- und Schutzbeispiele; auf Kategorieebenen nur passende der bestehenden vier Testbeiträge, ansonsten sichtbarer Layoutplatzhalter. Keine Taxonomie- oder Beitragserzeugungsänderung.
- Beispielfotos und rasterbasierte Logo-Referenz sind Ausschnitte aus dem bereitgestellten Chat-Mockup vom 8.10.; **Master-Logo nicht separat vorhanden, pixelgenaue Freigabe OFFEN**.
- Arbeitsfarben des Erstwurfs (nicht behauptete finale CI-Farbwerte): Terrakotta `#B35C40`, Salbei `#65745F`, Anthrazit `#252825`, Hintergrund `#FAF8F4`.
- Hobby-Depot-Plugin-Stand 1.50.635 in dessen DESIGN-Current verifiziert, Original-ZIP hier nicht verfügbar; visuelle Orientierung, keine Behauptung einer Codeübernahme.

## Nachweise
`php -l` Hauptplugin und Template PASS. PHP-Hauptplugin und Template Syntax PASS; drei lokale WordPress-Mock-Ansichten (Start, Welt, Blattkategorie) PASS, 6/31/45/141 Link-Hierarchie PASS; Startseite vier DEMO-Karten, Welt/Blatt nur fachlich passende DEMO-Karte PASS; ZIP-Integrität PASS. Gegenüber 0.1.2 ausschließlich Template, CSS, Hauptplugin-Versionszeile und README geändert; JSON-Daten, vier DEMO-Spezifikationen, Bilder, Logo und JS byteidentisch. Browser-Screenshot lokal nicht verfügbar (Chromium hängt bei Environment-Start). Live weiterhin offen. **Automatisierter Chromium-Browser-Test durch Umgebung (ERR_BLOCKED_BY_ADMINISTRATOR) verhindert; echte WordPress-Darstellung OFFEN.** Keine Behauptung von Live-PASS.

## Schutzgrenze
Keine Synchronisierung / Mutation des R2-Kategoriebaums. Kein Update des Hobbyrausch-Template-Kits. Keine zusätzlichen Plugins. Kein Test auf Nutzer-WordPress durch GitHub allein.


## QUELLENLAGE / WEITERARBEIT 14.10.2026
- Im aktiven Arbeitscontainer liegt das komplette **separate** Startseiten-Plugin `HAB_UND_BEWAHR_STARTSEITE_0.1.0.zip`, bestehend aus einer ca. 13-KB-PHP-Datei. Sein WordPress-Basename beginnt im Ordner `hab-und-bewahr-startseite/`; eigenes Plugin-Headerlabel; **es ist kein sicheres Update** für das alte Design-Vorschau-Plugin.
- Aus der persönlichen Library konnte `/Eigentumsschutz/Design/HAB_UND_BEWAHR_DESIGN_PREVIEWS_V1.zip` als Datei real zurückgewonnen werden (802.970 Byte, SHA-256 `18c16e2761af101cde107c313f44ebae8388ce10e98f94784f2225e5ca23bdf0`). Inhalt: `previews/startseite.html`, `preview.css`, andere HTML-Layouts und 17 konkrete WebP-Assets. Das ist eine **ältere statische Design-/Kachelreferenz**, aber **nicht** der PHP-Quellstand von `Design-Vorschau 0.1.3`.
- Sichtbarer WordPress-Backend-Screenshot des Nutzers vom 14.10.2026 zeigt **beide Plugins aktiv**: `Hab & Bewahr – Design-Vorschau` Version 0.1.3 und `Hab & Bewahr – Startseite` Version 0.1.0; eindeutige interne PHP-Pluginpfade/Originalquellen sind damit nicht sichtbar. Eine echte WordPress-Dateiabfrage hat nicht stattgefunden.
- In den tatsächlich erreichbaren lokalen und Library-Quellen wurde die **Original-PHP-ZIP `HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.3_TEXTMENUE_KLARE_THEMEN.zip` bisher nicht gefunden**. Sie ist laut bisheriger Current nur Chat-Artefakt. **Kein Ersatzbau aus einem älteren 1.50.579-Template-Kit**.
- Performance-Vorbefund am separaten 0.1.0-Plugin: Registrierung/Enqueue des Inline-CSS erfolgt in `wp_enqueue_scripts` **global**, auch ohne gerenderten Shortcode; dies widerspricht dem neuen performance-first Ziel. Bei der Integration CSS ausschließlich auf wirklich genutzten Designansichten ausgeben. Keine WordPress-Live-Messung behaupten.
- **Aktueller Blocker für lieferfähiges In-Place-Update:** Ohne reale PHP-Original-ZIP und Original-Plugin-Basename kann kein verlustfreies und updatekompatibles Gesamt-Designplugin gebaut oder geprüft werden. Original-ZIP von WordPress/Downloads als Quelle benötigt; nur dann zusammenführen.

## EXAKT EINE NEXT ACTION
**Die bisher nicht verfügbare echte Original-Installations-ZIP des bestehenden WordPress-Plugins „Hab & Bewahr – Design-Vorschau“ 0.1.3 beschaffen (als Nutzer-Upload oder belegbar gleiche Autoritätsquelle); daraus internen Plugin-Basename lesen und das Startseitenmodul einschließlich referenzierter ursprünglicher Kacheln, Header-C-Lock und lokaler Performanceprüfung verlustfrei als Update DIESER bestehenden Plugin-Identität integrieren.** Bis dahin keine weitere Installation, Deaktivierung oder Löschung. Keine WordPress-Writes in diesem Dokumentationsschritt.
