# HOBBY DEPOT – VOLLERSATZ 2026-10-23

STAND: 2026-10-23
STATUS: FULL REPLACEMENT LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_VOLLERSATZ_20261023_HD003_1.50.729_HD007_1.1.5.zip`

SHA-256:
`f735f41fa1740904e13428350bef04cb89c34664fbb6e8ff1014b8581b6de046`

Größe:
28,936,964 Bytes.

## Ursache des gescheiterten Delta-Laufs

Der Breadcrumb-Fix 1.1.4 hing an `astra_content_before`.
Hobby Depot läuft jedoch auf ListingHive. Dieser Hook ist für diesen Laufweg nicht belastbar.

Zusätzlich waren die letzten Pakete reine Delta-Pakete. Damit war nach einem Merge nicht eindeutig beweisbar, dass der aktive Serverbestand wirklich ersetzt wurde.

## Konsequenz

Kein weiterer Delta-Stand.

Das Artefakt enthält die zwei vollständigen bestehenden Pluginordner:
- `affiliate-portal-template-kit/` – HD-003 1.50.729;
- `hd-hobbyregister-core/` – HD-007 1.1.5.

## HD-003 1.50.729

- vollständiger Pluginordner;
- Footer-Logo nicht mehr per CSS abgeschnitten;
- eigenes physisch zugeschnittenes Footer-Logoasset ohne Unterzeile;
- Runtime-Marker `HD-003 RUNTIME 1.50.729`;
- bestehende Magazin-/Footer-Navigation erhalten.

## HD-007 1.1.5

- vollständiger Pluginordner;
- falscher Astra-Hook entfernt;
- Breadcrumb wieder im Register-Output, aber exakt in Hobby-Depot-Standardgeometrie:
  - Breite `min(calc(100% - 72px),1180px)`;
  - Margin oben 18px;
  - Schrift 12px / 1.4;
  - Hero-Abstand 5px;
- Hierarchie: Startseite › Magazin › Hobbyregister › Hobby;
- Auf einen Blick nur Icon + Wert;
- gleiche Hobbygruppe / ähnliche Hobbys disjunkt;
- beide Buttons gleiches helles Petrol;
- Überschrift Zur gleichen / Hobbygruppe zweizeilig.

## Simulation / QA

Fresh-Unpack:
- 954 Dateien;
- exakt zwei Pluginwurzeln;
- 14 PHP-Dateien, 14/14 Lint PASS.

HD-007 E2E:
- 3D-Druck PASS;
- Geocaching PASS;
- Buchbinden PASS;
- Slacklining PASS.

Je Profil geprüft:
- Version 1.1.5;
- Breadcrumb-Markierung und Hierarchie;
- Standardgeometrie;
- keine sichtbaren Faktenlabels;
- 3 Gruppen-Hobbys;
- 4 ähnliche Hobbys;
- keine Überschneidung;
- zweizeilige Gruppenüberschrift;
- identische Button-CSS.

Relationsaudit:
- 862/862 Hobbys;
- 0 Überschneidungen;
- ähnliche Hobbys liegen außerhalb der primären Hobbygruppe.

HD-003 Footer-Render:
- Runtime-Marker 1.50.729 PASS;
- neues Footer-Logoasset PASS;
- Hobbyfinder/Register/Glossar PASS;
- FAQ im Service PASS.

Kein Live-PASS behaupten.
