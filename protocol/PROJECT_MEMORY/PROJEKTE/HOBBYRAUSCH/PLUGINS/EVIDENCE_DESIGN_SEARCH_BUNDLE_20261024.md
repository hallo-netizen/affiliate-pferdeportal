# HOBBY DEPOT – DESIGN + BEREICHSSUCHE BUNDLE 2026-10-24

STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_DESIGN_SEARCH_BUNDLE_20261024_HD003_1.50.731_HD007_1.2.15_HDG_1.0.25_HARDPASS.zip`

SHA-256:
`581736924531499b589a8349fba3b8bf42ef3ffb3755c0043be35a568d1ef4c8`

Roots:
- `affiliate-portal-template-kit/` – HD-003 1.50.731
- `hd-hobbyregister-core/` – HD-007 1.2.15
- `hobby-depot-glossar/` – HDG 1.0.25

## Änderungen
- Hobbymagazin Glossarlink auf `/magazin/wissen-glossar/`.
- Hobbyregister-Banner zwischen Suche/A–Z und Hobbygruppen.
- Schreibschrift + Brush auf Registerübersicht und Einzelprofil.
- Registerprofil-Hero 238 px Desktop / 190 px mobil.
- Register-AJAX-Suche exklusiv auf 862 Registerdatensätze.
- Glossar-AJAX-Suche exklusiv auf veröffentlichte `hdg_term`.

## Regression
- HD-003 1200-px-Body aus 1.50.730 erhalten; Header/Footer-Override erhalten.
- HD-007: 862 Hobbys, 57 Traits, 862 Artikel × 8 Abschnitte, 24 finale Masterbilder.
- Glossar: 308 Begriffe, 13 Batches, 308 eindeutige IDs/Slugs.
- echte `HDG_Manager::validate_batch()`: 13/13 PASS.

## Paket-QA
- exakt 3 Roots;
- 1048 Dateien;
- ZIP CRC PASS;
- Source↔Fresh-Unpack bytegleich;
- PHP 22/22 PASS;
- Register Render/AJAX PASS;
- Glossar Render/AJAX PASS;
- Magazin→Glossar Link PASS;
- Register- und Glossar-Clientvorschau PASS.
