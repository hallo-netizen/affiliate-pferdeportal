# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.2.10 GLEICHER HOBBY-DEPOT-CONTAINER / LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.10_FULL_GLEICHER_HD_CONTAINER.zip`

SHA-256:
`510c6dbec8a654ee6dde9c0233ca00ff69f6918520548dc97db0fb68ff782962`

## Breite

Nicht mehr numerisch nachgebaut.

HD-007 verwendet jetzt dieselben echten Hobby-Depot-Klassen aus HD-003 1.50.729:
- `hd-content-v150616`
- `hd-portal-section`
- `hd-breadcrumb-wrap`

Lokaler Chromium-Pixeltest gegen HD-003-Kategorie:
1600/1440/1366/1180/1024/761/760/390 px Viewport.
Links, rechts und Gesamtbreite jeweils Delta **0 px**.

## Stabilität

- 862/862 Detailseiten PASS
- Registerübersicht PASS
- 57 Traits PASS
- 862 Artikel PASS
- 862 Bildzuordnungen PASS
- Owned shell PASS
- PHP/Fresh-Unpack PASS
- Duplicate-load alt→neu PASS
- Duplicate-load neu→alt PASS

Evidence:
`EVIDENCE_1.2.10.md`

## EXAKT EINE NEXT ACTION

**1.2.10 über den bestehenden aktiven Ordner `hd-hobbyregister-core` kopieren/überschreiben und live nur die Breite gegen eine bestehende Hobby-Depot-Kategorieseite prüfen.**
