# HD-007 – EVIDENCE 1.2.10 GLEICHER HOBBY-DEPOT-CONTAINER

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.10_FULL_GLEICHER_HD_CONTAINER.zip`

SHA-256:
`510c6dbec8a654ee6dde9c0233ca00ff69f6918520548dc97db0fb68ff782962`

## Breitenursache

Frühere Stände kopierten die numerische Breitenformel in HD-007. Das war nicht ausreichend.

1.2.10 verwendet jetzt dieselben echten Layoutklassen wie die Hobby-Depot-Kategorieseiten aus HD-003 1.50.729:
- Root: `hd-content-v150616`
- Breitencontainer: `hd-portal-section`
- Breadcrumb: `hd-breadcrumb-wrap`

HD-007 enthält für den Register-Hauptcontainer keine eigene Breitenformel mehr.

## Lokaler Browser-Beweis

Chromium, echtes HD-003-CSS plus tatsächlich gerendertes Geocaching-Profil aus HD-007 1.2.10.

Verglichen:
- HD-003 `.hd-portal-section`
- HD-003 `.hd-catlevel-intro`
- HD-007 `.hd-portal-section.hdr-wrap`

Pixelmessung:
- 1600: 1440 / 1440 / 1440
- 1440: 1368 / 1368 / 1368
- 1366: 1294 / 1294 / 1294
- 1180: 1108 / 1108 / 1108
- 1024: 952 / 952 / 952
- 761: 689 / 689 / 689
- 760: 736 / 736 / 736
- 390: 366 / 366 / 366

Links/rechts/Breite jeweils Delta 0 px.

## Regression/Fatal-QA

Fresh-Unpack:
- exakt ein Root `hd-hobbyregister-core`
- PHP-Lint PASS
- 862/862 Detailseiten PASS
- Registerübersicht PASS
- Owned-shell PASS
- Duplicate-load alt→neu PASS
- Duplicate-load neu→alt PASS
- 862 Registerdatensätze
- 57 Traits je Hobby
- 862 Artikel
- 862 Bildzuordnungen

Kein Live-PASS behaupten.
