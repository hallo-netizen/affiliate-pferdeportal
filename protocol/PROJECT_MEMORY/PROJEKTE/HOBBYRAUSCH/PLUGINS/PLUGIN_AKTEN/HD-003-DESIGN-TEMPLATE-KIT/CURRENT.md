# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-24
STATUS: **1.50.731 / MAGAZIN-GLOSSAR-LINK + BODY-1200 REGRESSION PASS / LIVE OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Aktuelles Bundle:
`HOBBY_DEPOT_DESIGN_SEARCH_BUNDLE_20261024_HD003_1.50.731_HD007_1.2.15_HDG_1.0.25_HARDPASS.zip`

SHA-256:
`581736924531499b589a8349fba3b8bf42ef3ffb3755c0043be35a568d1ef4c8`

Pluginroot im Bundle:
`affiliate-portal-template-kit/`

## Aktueller Vertrag
- zentrale Hobby-Depot-Body-Achse max. 1200 px;
- Header und Footer behalten unverändert ihre bisherige 1440-px-Achse;
- Hobbymagazin „Wissen & Glossar“ verlinkt kanonisch auf `/magazin/wissen-glossar/`;
- Footer-Glossarlink verwendet ebenfalls die kanonische Route;
- keine sonstige Header-/Footer-Designänderung.

## QA
- Hobbymagazin-Toolkarte aus echtem Plugin gerendert: kanonischer Glossarlink PASS, alte `/glossar/`-Route dort nicht mehr vorhanden;
- 1200-px-Body-Regeln aus 1.50.730 weiterhin vorhanden;
- Header-/Footer-1440-Override weiterhin vorhanden;
- Gesamtbundle Fresh-Unpack und Source↔ZIP bytegleich;
- PHP im Gesamtbundle 22/22 PASS.

## EXAKT EINE NEXT ACTION
**Bundle serverseitig in die drei bestehenden kanonischen Pluginordner überschreiben; keine zusätzlichen Pluginordner anlegen.**
