# HD-007 – EVIDENCE 1.2.16 SEARCH WIDTH

STAND: 2026-10-24
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.16_SEARCH_WIDTH_HARDPASS.zip`

SHA-256:
`3e5f46b1c2a7183df1b49d987ee8712c7c059eda18507de31de6d2a782cab78a`

## Beanstandung
Live-Screenshot: Register-Suchzeile über volle Breite, aber Such-Input nur in Browser-Standardbreite; sichtbares Label „Hobby suchen“ sollte entfallen.

## Ursache
Die Grid-Spalte war bereits korrekt `1fr + Button`. Dem `input` fehlte `width:100%`.

## Änderung
- `input{width:100%;box-sizing:border-box}`;
- sichtbares Label entfernt;
- Placeholder: „Hobby suchen …“;
- `aria-label="Hobby suchen"` für Zugänglichkeit;
- AJAX-Code funktional unverändert.

## QA
- PHP 4/4 PASS;
- ZIP CRC PASS;
- exakt ein Root `hd-hobbyregister-core/`;
- Source↔Fresh-Unpack bytegleich;
- Daten und Assets gegenüber 1.2.15 byteidentisch;
- Render-Test: Label 0, Placeholder PASS, aria-label PASS;
- Browser-Geometrie:
  - 1600 px: Feld 1030 px + Button 118 px = Zeile 1148 px;
  - 1024 px: Feld 782 px + Button 118 px = Zeile 900 px;
  - 760 px: Feld 566 px + Button 94 px = Zeile 660 px;
  - 390 px: Feld 196 px + Button 94 px = Zeile 290 px.
