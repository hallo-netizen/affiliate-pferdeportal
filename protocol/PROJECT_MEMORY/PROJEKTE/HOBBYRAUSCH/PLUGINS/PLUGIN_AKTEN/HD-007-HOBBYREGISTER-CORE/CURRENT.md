# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.2.3 PORTALBREITE EXAKT + BILDBATCH 01 DEFINIERT / LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.3_FULL_BREITE_BILDBATCH01.zip`

SHA-256:
`f92acb8f2b4e0b338bd2f7baad326fa4c5174eb82c3f6ee0b80b95794543cd65`

## Breite

Register übernimmt jetzt exakt die bestehende Portalbreitenkette:
- äußerer Template-Container: 100%, max-width none;
- Register/Breadcrumb: width 100%;
- max-width 1200px;
- Innenabstand 20px;
- Mobil 10px.

Damit wird nicht mehr mit 1050/1180 geraten, sondern die vorhandene Portalregel 1:1 verwendet.

## Bildproduktion

Zentraler Bildbestand weiterhin 862/862 sichtbar gebunden.

Neu in 1.2.3:
`data/image-production-batch-01.json`

Batch 01:
- 25 Hobbys;
- konkrete individuelle Fotomotive;
- Zielpfad je Hobby;
- Masterformat 3:2;
- Mindestgenerierung 1536×1024;
- finales WebP 1500×1000;
- center-safe für Hero + Vorschaukarten;
- keine Markenlogos/Wasserzeichen;
- bestehende sichtbare Quelle bleibt aktiv, bis der neue Master wirklich vorhanden ist.

Batch 01 beginnt mit Air-Dry Clay und endet mit Axtwurf als Sport.

## Weiterhin erhalten

- 862/862 Hobbys;
- 57/57 Traits;
- 862 statische 8-Abschnitt-Texte;
- „Selbe Hobbygruppe“;
- kein Detail-Banner unten;
- Registerübersichts-Banner unverändert.

## QA

- PHP-Lint 4/4 PASS;
- Fresh-Unpack PASS;
- Portalbreite 1200/20 PASS;
- 25/25 Bilddefinitionen PASS.

## EXAKT EINE NEXT ACTION

**1.2.3 über den bestehenden aktiven Ordner kopieren/überschreiben und die Breite live gegen eine normale Portalseite prüfen. Parallel Bildbatch 01 als erste 25 individuellen Masterbilder produzieren.**
