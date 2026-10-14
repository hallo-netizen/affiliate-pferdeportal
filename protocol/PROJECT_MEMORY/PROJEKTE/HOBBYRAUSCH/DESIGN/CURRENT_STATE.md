# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **SEITE WIEDER ERREICHBAR / ARCHITEKTUR- UND RUNTIME-ÄNDERUNGEN GESPERRT / HERO-ONLY-PATCH 1.50.659 LOKAL PASS / LIVE-PRÜFUNG OFFEN**

## Harte Sperre
Ab jetzt keine Änderungen an:
- PHP des Template-Kits;
- Routing;
- Templates;
- CSS;
- Seitenstruktur;
- Kartenmapping;
- Architektur/System.

## Aktueller Kandidat
`HOBBY_DEPOT_HERO_IMAGES_ONLY_1.50.659.zip`

SHA-256:
`85618e481f35833f1ae2a1b54efe1fdaa573675916a06a53995d1fbd554820a4`

## Was der Patch exakt ändert
- fügt **65 neue Hero-WebP-Dateien** hinzu, alle **600×220**;
- ändert genau **eine bestehende Datei**:
  `assets/hobby-depot-v150650/hub2-image-map.json`
- darin wird ausschließlich der `heroes`-Block auf die neuen `*-v150659.webp`-Dateien umgestellt;
- `cards` und `meta` bleiben ab dem `"cards"`-Marker bytegenau unverändert.

## Lokale Prüfung
Auf originalem 1.50.650-Runtime-Baum:
- **55/55 PHP-Dateien byte-identisch**;
- Templates unverändert;
- Routing unverändert;
- CSS unverändert;
- Karten unverändert;
- nur 65 neue Hero-Dateien + Hero-Mapping;
- **65/65 Hero-Dateien 600×220**;
- vollständiger Render `Druck & Fotografie` PASS;
- gerenderte Hero-URL zeigt auf `druck-foto-v150659.webp`;
- ZIP-Integrität PASS.

## EXAKT EINE NEXT ACTION
**Nur `HOBBY_DEPOT_HERO_IMAGES_ONLY_1.50.659.zip` als separates Plugin installieren und aktivieren; danach eine Hub2-Seite prüfen. Keine andere Plugin-/Architekturänderung.**
