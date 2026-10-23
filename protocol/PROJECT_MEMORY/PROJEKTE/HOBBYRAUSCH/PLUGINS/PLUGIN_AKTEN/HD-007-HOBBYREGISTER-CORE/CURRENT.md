# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.1.1 HOBBYREGISTER-KORREKTUR LOCAL HARD PASS / LIVE-INSTALLATION OFFEN**

Plugin-ID:
HD-007-HOBBYREGISTER-CORE

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.1.1_FULL_KORREKTUR.zip`

SHA-256:
`f963a0c07a4e5f9275992db8eea82f92721a4c12b62a3a7f0e78ed9b7a094d7c`

Hauptordner:
`hd-hobbyregister-core/`

Fachautorität:
`../../../WISSENSDATENBANK/CURRENT_STATE.md`

Textvertrag:
`../../../WISSENSDATENBANK/HOBBYREGISTER_TEXTREGELN_V1.md`

Referenztransfer:
`../../../WISSENSDATENBANK/HOBBYREGISTER_REFERENZTRANSFER_V1.md`

## Korrektur 1.1.1

Startseite:
- Breadcrumb-Höhe/Abstände an Hobby-Depot-Standard angepasst;
- Suche + A–Z;
- acht Hobbygruppen als reine Icon-Navigation nach dem bewährten Pferderassen-Prinzip;
- 16 Hobbykarten je Seite + Pagination.

Detailseiten:
- kein 4-Zeilen-Kurzprofil-Fallback mehr;
- alle 862 Profile liefern acht Fließtextabschnitte nach dem verbindlichen Schema;
- linke „Auf einen Blick“-Leiste cremefarben, petrolfarbene Oberkante, größere Schrift und kleine Icons;
- Hobbygruppe + drei Einträge aus derselben Hobbygruppe links;
- ähnliche Hobbys nur einmal am Seitenende.

## Datenbasis

Unverändert:
- 862 kanonische Hobbys;
- 54 hashgebundene Basistraits in der aktuellen physischen Runtime-Projektion;
- 4/4 Kurzprofilfelder;
- Basis-SHA `4deb4be2b235db450d58f02485ec40e780fc2671f9dfc6edf8cbbba0f738af78`.

Fachautorität bleibt Schema 1.2 mit 57/57 Traits.
1.1.1 rät keine fehlenden drei Zusatzwerte; sie werden nur dort verwendet, wo sie bereits explizit gebunden sind.

## QA

- Core-ready 862/862 PASS;
- 862/862 Detailprofile: 8 nichtleere Fließtextabschnitte PASS;
- kürzester generierter Text 486 Wörter;
- Buchbinden / Slacklining / Geocaching / Aquaristik / Münzen / 3D-Druck Vollrender PASS;
- 8 Icon-Gruppen PASS;
- Compact-Fallback entfernt PASS;
- Sidebar-Icons / größere Typografie PASS;
- „Ähnliche Hobbys“ nur einmal PASS;
- PHP-Lint / Fresh-Unpack PASS;
- keine DB-Writes / Cron / Netzwerkänderung.

Evidence:
`EVIDENCE_1.1.1.md`

## EXAKT EINE NEXT ACTION

**1.1.1 als vollständigen Ordner `hd-hobbyregister-core` per Cyberduck über den bestehenden Ordner in `wp-content/plugins/` zusammenführen und Register-Startseite plus mindestens eine bisherige Nicht-Test-Detailseite live prüfen.**
