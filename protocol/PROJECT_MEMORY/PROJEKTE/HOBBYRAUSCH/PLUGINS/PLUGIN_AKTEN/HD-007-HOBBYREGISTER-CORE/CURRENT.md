# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.1.0 HOBBYREGISTER-FRONTEND PROTOTYP LOCAL HARD PASS / LIVE-INSTALLATION OFFEN**

Plugin-ID:
HD-007-HOBBYREGISTER-CORE

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.0_FULL_PROTOTYP.zip`

SHA-256:
`85c267e999bbb34b56c31003473b0f33fd8589a87dfa4d4fede98d2bca3e1ff0`

Hauptordner:
`hd-hobbyregister-core/`

Fachautorität:
`../../../WISSENSDATENBANK/CURRENT_STATE.md`

Textvertrag:
`../../../WISSENSDATENBANK/HOBBYREGISTER_TEXTREGELN_V1.md`

Referenztransfer:
`../../../WISSENSDATENBANK/HOBBYREGISTER_REFERENZTRANSFER_V1.md`

## Rolle

HD-007 bleibt die einzige read-only WordPress-Laufzeitprojektion des zentralen Hobbyregisters.
Kein Parallelplugin und keine zweite Hobby-Datenbank.

## Datenbasis

Hashgebundene Basisprojektion:
- 862 kanonische Hobbys;
- 54 unveränderte Basistraits je Hobby;
- 4/4 Kurzprofilfelder;
- Basis-SHA `4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`.

Die zentrale Fachautorität ist bereits Schema 1.2 mit 57/57 Traits.
Für die zwei Volltextproben sind die drei neuen Werte exakt aus der geprüften Schema-1.2-Evidence eingebunden.
Die vollständige 57er Laufzeitprojektion wird erst vor dem 862er Volltextrollout gebunden; die 54er Basis wurde nicht verändert.

## Frontend 1.1.0

Virtuelle read-only Routen:
- `/hobbyregister/`;
- `/hobbyregister/<hobby-slug>/`.

Übersicht:
- Hero;
- Suche;
- A–Z;
- acht Hobbygruppen;
- 4-spaltige Hobbykarten;
- 16 Karten je Seite;
- Pagination.

Gruppen:
**Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln.**

Sie werden als Views aus bestehenden Daten abgeleitet, nicht persistent als zweite Taxonomie gespeichert.

Detail:
- Hero;
- „Auf einen Blick“;
- Hobbygruppe;
- gleiche Hobbygruppe;
- ähnliche Hobbys;
- Schema-F-Fließtext;
- Register-/Magazin-Navigation.

Volltextproben:
- Buchbinden: 8 Abschnitte / 657 Wörter;
- Slacklining: 8 Abschnitte / 670 Wörter.

Andere Profile bleiben bis zur Abnahme bewusst kompakt.

## SEO-Schutz im Prototyp

Detailprofile sind vorläufig `noindex,follow`, bis die CORE-vs-REGISTER-Owner-Matrix je Hobby vorliegt.
Das ist kein finaler Voll-noindex-Vertrag.

## Harte Grenzen

- keine WordPress-DB-Writes;
- keine eigenen Tabellen;
- keine Cronjobs;
- keine Netzwerkaufrufe;
- keine zweite Hobby-Taxonomie;
- keine Auto-Massenproduktion vor Text-/Designabnahme.

## QA

- PHP-Lint 4/4 PASS;
- Core-ready 862/862 PASS;
- Register-Basis-SHA unverändert PASS;
- 862 eindeutige Profilslugs PASS;
- Gruppenabdeckung 862/862 / unzugeordnet 0;
- Overview 16 Karten + Pagination PASS;
- Buchbinden E2E PASS;
- Slacklining E2E PASS;
- Pferde-/Rassenbegriffe im ausgelieferten Plugin: 0;
- Write-/Cron-/Network-Audit PASS.

Evidence:
`EVIDENCE_1.1.0.md`

## EXAKT EINE NEXT ACTION

**1.1.0 als vollständigen Ordner `hd-hobbyregister-core` nach `wp-content/plugins/` hochladen, aktivieren und anschließend Register-Startseite sowie Buchbinden/Slacklining visuell und sprachlich abnehmen.**
