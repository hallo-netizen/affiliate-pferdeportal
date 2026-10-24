# HD-003 – EVIDENCE 1.50.730 BODY 1200

STAND: 2026-10-24
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HD003_CYBERDUCK_1.50.730_BODY_1200_HEADER_FOOTER_UNBERUEHRT_HARDPASS.zip`

SHA-256:
`b31c2528ad049d9974104cd8de35b39cf69bf701efe429104c8c4218bd798279`

## Änderung
- zentrale Hobby-Depot-Body-Achse maximal 1200 px;
- Header und Footer behalten 1440-px-Basis;
- native ListingHive-/WordPress-`.site-content`-Seiten ebenfalls max. 1200 px;
- Glossar-Single-Altbreite 1240 px zentral auf 1200 px gekappt;
- Hobbyregister übernimmt die vorhandenen HD-003-Containerklassen.

## Browservergleich gegen 1.50.729
Viewports: 1600 / 1366 / 1024 / 760 / 390 px.

- Header: 0 px Breiten-/Positionsänderung.
- Footer: 0 px Breiten-/Positionsänderung.
- 1600 px: Body 1440 → 1200 px.
- 1366 px: Body 1294 → 1200 px.
- 1024 px und kleiner: responsive Außenabstände bleiben bestehen.
- Glossar Übersicht / Single, Hobbyregister, Portalabschnitt und native site-content: gemeinsame Außenachse PASS.

## Paket-QA
- exakt ein Root: `affiliate-portal-template-kit/`;
- 935 Dateien;
- PHP 10/10 PASS;
- ZIP-Integrität PASS;
- nach erneutem Entpacken Source/ZIP bytegleich;
- Browser-Hardpass direkt aus dem erneut entpackten finalen ZIP.
