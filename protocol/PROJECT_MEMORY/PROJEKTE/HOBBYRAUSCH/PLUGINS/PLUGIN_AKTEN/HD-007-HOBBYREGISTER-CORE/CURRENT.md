# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.2.1 LAYOUT/BILD/ÜBERSCHRIFT-FIX LOCAL HARD PASS / LIVE-INSTALLATION OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.1_FULL_LAYOUT_IMAGE_HEADING_FIX.zip`

SHA-256:
`050e7f4a0611cd96adc8cdc4607f6be22a14b848d1f3e97653311231440978f3`

Größe:
1,722,789 Bytes.

Hauptordner:
`hd-hobbyregister-core/`

## Datenvertrag

- 862/862 Hobbys;
- 57/57 Traits;
- 2.586 neue Schema-1.2-Werte gebunden;
- 46.548 alte Traitwerte unverändert;
- Runtime-Register-SHA `d0d424485e6dbcf65a8332da732d2e342b279f0a1311919149ba8dfcdb93604a`.

## Textvertrag

- 862/862 statische Texte;
- je 8 Schema-F-Abschnitte;
- 656–761 Wörter;
- alle 57 Merkmale im Produktionsgenerator berücksichtigt;
- keine 4-Zeilen-Kurzprofil-Fallbacks.

## Design

- Body/Breadcrumb max. 1180px;
- Profil-Hero ohne wiederholenden Kurzprofil-Untertext;
- kurzer gruppenspezifischer Claim;
- grüne Schreibschrift + gelber Brush-Unterstrich.

## Bilder

Aktuelle Darstellungsabdeckung 862/862:
- 328 exakt kuratierte bestehende Hobbyfotos;
- 534 fachlich zugeordnete bestehende Themen-Masterbilder.

Die 534 Themenbilder werden nicht als neu erzeugte individuelle Portraitmaster ausgegeben.
Der zentrale Portrait-Bildplan bleibt dafür maßgeblich.

## QA

- ready() PASS;
- 862 × 57 Traits PASS;
- alte 54 unverändert PASS;
- 862 × 8 Textabschnitte PASS;
- 862 Bildzuordnungen PASS;
- 7 heterogene E2E-Profile PASS;
- PHP-Lint/Fresh-Unpack PASS.

Evidence:
`EVIDENCE_1.2.0.md`

## 1.2.1 Korrektur

- Register/Breadcrumb auf 1050px Portalbreite;
- Überschrift „Zur gleichen Hobbygruppe“ gekürzt auf „Gleiche Hobbygruppe“;
- beanstandete Geocaching-Hero-Zuordnung von Kletter-/Seilmotiv auf Outdoor-Master korrigiert;
- 57-Trait- und 862-Text-Stand aus 1.2.0 unverändert erhalten.

## EXAKT EINE NEXT ACTION

**Den vollständigen Ordner `hd-hobbyregister-core` aus 1.2.1 über den bestehenden aktiven Pluginordner kopieren/überschreiben, ohne ihn vorher zu löschen. Danach Registerbreite, Geocaching-Hero und Sidebar-Überschrift live prüfen.**
