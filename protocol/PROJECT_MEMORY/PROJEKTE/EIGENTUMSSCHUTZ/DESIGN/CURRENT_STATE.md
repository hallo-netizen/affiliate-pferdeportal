# HAB & BEWAHR – DESIGN – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **0.1.2 VOLLSTÄNDIGE KATEGORIENNAVIGATION LOKAL GEPRÜFT / WORDPRESS-LIVE OFFEN**

## Ziel / bindende Nutzerentscheidung
Erst eine **grobe Visualisierung** der bestehenden echten Website-Struktur, keine fertige CI/SEO-Produktion. Grobe Orientierung am Hub-/Kartenaufbau des Hobby-Depot-Design-Plugins; keine Architekturübernahme. Farbwelt warmes Terrakotta, Salbei, Anthrazit, cremefarbener Hintergrund. Wortmarke **Hab & Bewahr** mit Bogen, Claim **„Wissen. Vergleichen. Besser schützen.“**; Hero **„Was dir gehört, soll dir bleiben.“**. Sechs Gefahrenwelten + Magazin + Dienstleister, vorhandenes R2-Profil. Vier echte, eindeutig markierte Testartikel; dieselben Beispiele nur als Kacheln auf anderen Kategorieebenen.

## Aktueller Kandidat (nur Chat-Artefakt)
`HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.2_ALLE_KATEGORIEN_SICHTBAR.zip`
SHA-256: `3217e899e1a2eeb70a4a68e6d04d55ece20bcc437099780beb44a7a4dae7eb0f`

- Eigener deaktivierbarer Visualisierungsplugin, ohne Eingriff in HD-001.
- Echtgebundene 354 WP-Zielobjekte / 141 CORE-Kategorien aus R2-Readback vom 2026-10-12, Status COMPLETE/PASS.
- Dynamische Seitenhierarchie per vorhandenen Objekt-IDs.
- Vier DEMO-Artikel werden einmalig bei Aktivierung erstellt, je eine vorhandene CORE-Kategorie. `noindex`; bei Deaktivierung in Entwurf. Kein Content-Massenimport.
- Startseite, 6 Weltseiten, Unterhubs, Terminalkategorien, Demo-Artikelseite; Layoutbeispiele für Magazin und Dienstleister.
- **0.1.2 – Vollständiges Megamenü:** sechs Welten als Hauptnavigation. Pro geöffnetem Menü werden **alle zugehörigen Bereiche, Unterbereiche und die 141 Blattkategorien als direkte Links ohne zweite Klickstufe** ausgegeben. Umfangreiche Menüs scrollen innerhalb des Panels; Desktop auch per Hover, mobil per Klick. Keine Änderung des R2-Profils.
- Beispielfotos und rasterbasierte Logo-Referenz sind Ausschnitte aus dem bereitgestellten Chat-Mockup vom 8.10.; **Master-Logo nicht separat vorhanden, pixelgenaue Freigabe OFFEN**.
- Arbeitsfarben des Erstwurfs (nicht behauptete finale CI-Farbwerte): Terrakotta `#B35C40`, Salbei `#65745F`, Anthrazit `#252825`, Hintergrund `#FAF8F4`.
- Hobby-Depot-Plugin-Stand 1.50.635 in dessen DESIGN-Current verifiziert, Original-ZIP hier nicht verfügbar; visuelle Orientierung, keine Behauptung einer Codeübernahme.

## Nachweise
`php -l` Hauptplugin und Template PASS. PHP-Hauptplugin und Template Syntax PASS; vollständige lokale WordPress-Mock-Startseite PASS; alle Menüebenen (6/31/45/141) und konkrete Linkziele PASS; kein verschachteltes DETAILS im Megamenü; JS Syntax PASS; ZIP-Integrität PASS; Vergleich 0.1.1 zeigt ausschließlich Änderungen in PHP/JS/CSS/README, Assets und nodes.json byteidentisch. **Automatisierter Chromium-Browser-Test durch Umgebung (ERR_BLOCKED_BY_ADMINISTRATOR) verhindert; echte WordPress-Darstellung OFFEN.** Keine Behauptung von Live-PASS.

## Schutzgrenze
Keine Synchronisierung / Mutation des R2-Kategoriebaums. Kein Update des Hobbyrausch-Template-Kits. Keine zusätzlichen Plugins. Kein Test auf Nutzer-WordPress durch GitHub allein.

## EXAKT EINE NEXT ACTION
Bestehendes Design-Vorschau-Plugin auf **0.1.2** aktualisieren; live eine Themenwelt im Megamenü aufklappen und prüfen, dass alle unteren Kategorien ohne zusätzlichen Klick sichtbar und direkt erreichbar sind. Danach nur nötige optische Korrekturen, Kategoriebaum und Demoartikel unverändert.
