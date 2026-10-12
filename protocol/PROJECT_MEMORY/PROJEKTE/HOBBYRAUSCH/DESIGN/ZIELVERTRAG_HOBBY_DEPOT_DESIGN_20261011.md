# ZV-HOBBYRAUSCH-DESIGN-001 – HOBBY DEPOT PORTALDESIGN

STATUS: AKTIV
FASSUNG: 2.3 / 2026-10-12

## Header / Navigation
- Logo unverändert und linksbündig. Die Bilddatei bleibt byteidentisch; Halbkreis/dein, HOBBY DEPOT und Claim werden aus demselben Asset getrennt dargestellt und vertikal entzerrt.
- Header als 2-Spalten-System: links Logo; rechts Suchfeld + Navigation.
- Suchfeld liegt auf der HOBBY-DEPOT-Wortmarkenlinie.
- Navigation liegt rechts **direkt an der unteren Headerkante**.
- Ab 761 px: alle 8 Welten **in exakt einer horizontalen Zeile und auf derselben Baseline**, einschließlich Sammeln.
- <761 px: Mobilmenü.
- Navigationsicons entfallen; Text + Pfeil bleiben.
- Flyouts per Hover/Fokus/Klick und viewport-sicher.

## Hub-/Unterkategorie-Karten
- alle bildtragenden Hub-Karten folgen demselben Bildprinzip:
  - **ein klares Hauptmotiv / eine klare Tätigkeit**;
  - ruhiger Ausschnitt;
  - deutlich weniger Nebenmotive;
  - einheitliches Querformat 600×320;
  - keine visuell doppelten/nahezu identischen Bilder innerhalb des aktiven Hub-Bildbestands.
- Für die acht ersten Welt-Hubs sind alle 65 direkten Unterkategorien mit kontrollierten Motiven belegt.
- Bei diesen 65 Karten hat das kontrollierte Designasset **Vorrang vor WordPress Featured Images**, damit alte Live-Featured-Images keine Wiederholungen mehr erzwingen.
- Bei tieferen Ebenen darf ein echtes eigenes Featured Image verwendet werden, sofern kein kontrolliertes Designasset existiert.
- Kein Parent-/Hero-Bild als mehrfacher Universalersatz.
- natürliche Überschrift: `Weiter in <Welt>` / `Weitere Kategorien`.
- Kartentitel 15 px; Untertitel 12 px nur mit echtem Orientierungswert; kein Fülltext.

## Monetarisierung im Kategorienraster
- Affiliate-Produkte stehen **nicht** zwischen Unterkategorie-Reihen.
- Nur ein Affiliate-Banner darf die letzte unvollständige 3er-Reihe ergänzen:
  - Rest 1 Kategorie → Banner 2 Kartenbreiten;
  - Rest 2 Kategorien → Banner 1 Kartenbreite;
  - Rest 0 → Banner als volle eigene Zeile.
- Produkte bleiben außerhalb des Kategorie-Rasters als natives Empfehlungsmodul.
- öffentlich leer unsichtbar; eingeloggt leer sichtbar.

## Bestehende Bindungen
- Hero/Fold ohne Textdoppelung.
- Direktwerbung: maximal ein Platz, ein Foto, Brush-Headline, heller CTA.
- keine Taxonomie-/Workflow-/Provideränderung durch Design.
- HD-001/HD-004 bleiben Kategorie-/Runtime-Autorität; Affiliate-Zentrale bleibt Monetarisierungsautorität.

## PASS
Kein Live-PASS ohne echten WordPress-Readback.

Lokaler Pflichtcheck:
- PHP/ZIP;
- 65/65 Bildpfade;
- 65/65 unterschiedliche Datei-Hashes;
- zusätzlich Perceptual-Hash-Prüfung gegen visuelle Duplikate;
- Featured-Image-Override-Test;
- Navigation 1600/1200/1024/900/800/761: 8 Items eine Baseline, Sammeln eingeschlossen, kein horizontaler Overflow;
- 760: Mobilepfad;
- Flyout Sammeln viewport-sicher.
