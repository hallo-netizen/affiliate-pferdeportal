# HAB & BEWAHR – DESIGN – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-13
STATUS: **0.1.3 SCHLICHTES TEXTMENÜ UND VERSTÄNDLICHE THEMEN LOKAL GEPRÜFT / WORDPRESS-LIVE OFFEN**

## Ziel / bindende Nutzerentscheidung
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

## EXAKT EINE NEXT ACTION
Bestehendes Design-Vorschau-Plugin auf **0.1.3** aktualisieren und auf echter WordPress-Seite schlichtes Textmenü (alle Ebenen) sowie bessere Erkennbarkeit von Thema und Nutzen auf Start- und Weltseiten prüfen. Nur nach Live-Feedback weiter anpassen; keinerlei Kategoriebaum-Änderungen.
