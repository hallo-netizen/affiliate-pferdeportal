# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **1.50.664–1.50.667 VERWORFEN / 1.50.668 FULL LOCAL HARD PASS / LIVE READBACK OFFEN**

## Basis

Affiliate Portal Template Kit **1.50.650** bleibt Ausgangsbasis.

Nicht verwenden:
1.50.664 / 1.50.665 / 1.50.666 / 1.50.667.

## Kandidat 1.50.668

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.668_HOBBY_DEPOT_REGISTRY_NAV_TEXT_HEROPREVIEW_HARDPASS.zip`

Library:
`/hobby rausch/releases/AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.668_HOBBY_DEPOT_REGISTRY_NAV_TEXT_HEROPREVIEW_HARDPASS.zip`

SHA-256:
`ee521c5f8b360c16d641e77507b94b64b93432da701e4760e7c4daa67d9440b6`

QA:
- `/hobby rausch/releases/HOBBY_DEPOT_1.50.668_BROWSER_ACCEPTANCE.json`
- `/hobby rausch/releases/HOBBY_DEPOT_1.50.668_FINAL_DIFF.json`

## Enthalten

- Hab-&-Bewahr-Prinzip: Registry als einzige Strukturwahrheit, fail-closed;
- keine rohen WP-Kinder/Geschwister als Ersatz;
- Page- und Category-Ebene korrekt;
- terminale Inhaltskategorien sichtbar;
- zufälliger Weltbild-Fallback aus aktivem Renderer entfernt;
- Mega-Menü aus Registry;
- `Mehr Kategorien` erweitert im selben Flyout;
- eine zusätzliche Orientierungsebene, kein Vollbaum;
- Hub2-Text nach Vertrag;
- 65 bestehende Hero→Preview-Paare synchronisiert.

## Local Hard QA

- Baseline 330 terminale Hobbyseiten: 0 Renderer-Abweichungen;
- V3 370 terminale Hobbyseiten / 2160 Leafs: 0 Renderer-Abweichungen;
- Trainspotting-Negativfall PASS;
- Ameisenhaltung 7/7 terminale Kategorien PASS;
- Headless-Browser: 1920 / 1440 / 1101 / 1100 / 1024 / 768 / 761 / 760 / 390 PASS;
- alle 8 Mega-Menüs PASS;
- `Mehr Kategorien` PASS;
- Text-Accordion: Hero-Höhenänderung 0 px;
- horizontaler Overflow 0;
- PHP 58/58 PASS;
- ZIP 984/984 Roundtrip PASS;
- 0 Dateien entfernt;
- 0 Hero-Dateien verändert.

## Abhängigkeit

HD-004 muss als Runtime-Registry vorhanden sein. Bei vorhandener zentraler Revision gibt es bewusst keinen stillen Rückfall auf rohe WordPress-Struktur.

## V3-Grenze

Die fünf neuen direkten V3-Hub2 brauchen vor Live-Freigabe jeweils eigenes Hero + daraus abgeleitete Preview:
Spotting & Verkehr, Citizen Science, Natur bestimmen, Suchen & Finden, Modellbau.

## EXAKT EINE NEXT ACTION

**HD-004 live bereitstellen; danach 1.50.668 gegen die aktuelle 330er Baseline installieren und ausschließlich Registry/Navi/Mega-Menü/Hub2-Text/terminale Ebene live prüfen. V3 noch nicht synchronisieren.**
