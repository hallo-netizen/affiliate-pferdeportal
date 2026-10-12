# HAB & BEWAHR – DESIGN – CURRENT STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-12
STATUS: **ERSTER ISOLIERTER DESIGNKANDIDAT LOKAL GEPRÜFT / WORDPRESS-LIVE OFFEN**

## Ziel / bindende Nutzerentscheidung
Erst eine **grobe Visualisierung** der bestehenden echten Website-Struktur, keine fertige CI/SEO-Produktion. Grobe Orientierung am Hub-/Kartenaufbau des Hobby-Depot-Design-Plugins; keine Architekturübernahme. Farbwelt warmes Terrakotta, Salbei, Anthrazit, cremefarbener Hintergrund. Wortmarke **Hab & Bewahr** mit Bogen, Claim **„Wissen. Vergleichen. Besser schützen.“**; Hero **„Was dir gehört, soll dir bleiben.“**. Sechs Gefahrenwelten + Magazin + Dienstleister, vorhandenes R2-Profil. Vier echte, eindeutig markierte Testartikel; dieselben Beispiele nur als Kacheln auf anderen Kategorieebenen.

## Aktueller Kandidat (nur Chat-Artefakt)
`HAB_UND_BEWAHR_DESIGN_VORSCHAU_0.1.0.zip`
SHA-256: `c24af5b3a82f88c5c3c902e64fd0a973e8b0d25904a0a045bfe30efa8a76a067`

- Eigener deaktivierbarer Visualisierungsplugin, ohne Eingriff in HD-001.
- Echtgebundene 354 WP-Zielobjekte / 141 CORE-Kategorien aus R2-Readback vom 2026-10-12, Status COMPLETE/PASS.
- Dynamische Seitenhierarchie per vorhandenen Objekt-IDs.
- Vier DEMO-Artikel werden einmalig bei Aktivierung erstellt, je eine vorhandene CORE-Kategorie. `noindex`; bei Deaktivierung in Entwurf. Kein Content-Massenimport.
- Startseite, 6 Weltseiten, Unterhubs, Terminalkategorien, Demo-Artikelseite; Layoutbeispiele für Magazin und Dienstleister.
- Beispielfotos und rasterbasierte Logo-Referenz sind Ausschnitte aus dem bereitgestellten Chat-Mockup vom 8.10.; **Master-Logo nicht separat vorhanden, pixelgenaue Freigabe OFFEN**.
- Arbeitsfarben des Erstwurfs (nicht behauptete finale CI-Farbwerte): Terrakotta `#B35C40`, Salbei `#65745F`, Anthrazit `#252825`, Hintergrund `#FAF8F4`.
- Hobby-Depot-Plugin-Stand 1.50.635 in dessen DESIGN-Current verifiziert, Original-ZIP hier nicht verfügbar; visuelle Orientierung, keine Behauptung einer Codeübernahme.

## Nachweise
`php -l` Hauptplugin und Template PASS. Lokale WordPress-Mock-Startseite PASS: sechs Themenwelten und vier Demokarten. ZIP-Integrität PASS. **Kein echter WordPress-Live-Test oder Screenshot-Audit**; keine Behauptung von Live-PASS.

## Schutzgrenze
Keine Synchronisierung / Mutation des R2-Kategoriebaums. Kein Update des Hobbyrausch-Template-Kits. Keine zusätzlichen Plugins. Kein Test auf Nutzer-WordPress durch GitHub allein.

## EXAKT EINE NEXT ACTION
Design-Vorschau 0.1.0 auf hab-und-bewahr.de installieren/aktivieren; danach echte Startseite sowie Welt-, Hub-, Kategorien- und Demo-Artikelseiten prüfen und anhand des Feedbacks minimal anpassen.
