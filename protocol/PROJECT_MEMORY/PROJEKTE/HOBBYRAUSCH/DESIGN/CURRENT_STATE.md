# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **HD-003 1.50.724 FOOTER LOCAL HARD PASS / HD-007 1.1.0 HOBBYREGISTER PROTOTYP LOCAL HARD PASS / LIVE-ABNAHME OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Magazin

Der aktuelle Magazinstand bleibt als Arbeitsstand bestehen.
Das endgültige Magazin-Finishing wird bewusst erst nach realistischen Dummy-/Testbeiträgen vorgenommen.

## Footer – HD-003 1.50.724

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.724_UPDATE_FOOTER_MARKENLEISTE.zip`

SHA-256:
`8f45a2541b537db15cd16eea509021857568ddf9bc234fd605ad48c7e6b37e44`

Neu:
- kleine Markenleiste oberhalb der vier Spalten;
- Hobby-Depot-Logo ca. 132 px;
- Claim „Hobbys. Ideen. Möglichkeiten.“;
- vier Footer-Spalten bleiben unverändert;
- KI-/Copyrightbereich bleibt separat.

## Hobbyregister – HD-007 1.1.0

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.0_FULL_PROTOTYP.zip`

SHA-256:
`85c267e999bbb34b56c31003473b0f33fd8589a87dfa4d4fede98d2bca3e1ff0`

Designprinzip:
- Register-Hero;
- Suche + A–Z;
- acht Hobbygruppen;
- 4-spaltiges Kartenraster;
- 16 Hobbys je Seite;
- Detailseite mit Hero, „Auf einen Blick“, Sidebar und Fließtext;
- gleiche Hobbygruppe;
- ähnliche Hobbys;
- keine Pferde-/Rassenbezeichnungen oder -bilder.

Text-/Designproben:
- Buchbinden;
- Slacklining.

Die übrigen Profile bleiben vor dem Massenrollout bewusst kompakt.

Verträge:
- `../WISSENSDATENBANK/HOBBYREGISTER_TEXTREGELN_V1.md`;
- `../WISSENSDATENBANK/HOBBYREGISTER_REFERENZTRANSFER_V1.md`.

## Lokale QA

HD-003:
- PHP-Lint/Fresh-Unpack PASS;
- Logo/Claim/4 Spalten/PB-one PASS.

HD-007:
- PHP-Lint 4/4 PASS;
- 862/862 Datensätze;
- 862 eindeutige Profilslugs;
- Gruppenabdeckung 862/862;
- 16 Karten + Pagination;
- Buchbinden/Slacklining E2E PASS;
- Write-/Cron-/Network-Audit PASS.

## EXAKT EINE NEXT ACTION

**Footer-Update und HD-007-Prototyp live einspielen; anschließend Footer, Register-Startseite sowie Buchbinden und Slacklining visuell/sprachlich abnehmen.**
