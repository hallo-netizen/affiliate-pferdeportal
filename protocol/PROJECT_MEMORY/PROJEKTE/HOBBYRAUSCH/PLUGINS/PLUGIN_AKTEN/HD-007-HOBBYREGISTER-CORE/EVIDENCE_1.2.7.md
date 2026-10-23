# HD-007 – EVIDENCE 1.2.7 STABILE REPARATUR

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.7_FULL_STABIL_REPARIERT.zip`

SHA-256:
`1019a7b0df6f268caba9acdeaa296a2a12817e1264db43024adaec369517dc7c`

## Ursache des kritischen Fehlers

Der 1.2.6-Umbau wird vollständig verworfen.

Zusätzlich reproduziert:
Wenn zwei Hobbyregister-Kopien gleichzeitig geladen werden, konnten die bisherigen Versionen dieselben globalen Funktionen/Klassen erneut deklarieren und damit einen PHP-Fatal auslösen.

## 1.2.7

Basis wieder stabiles JSON-Laufzeitsystem aus 1.2.5.
Kein compiled/-Datenumbau.

Kollisionsschutz:
- neue interne Runtime-Klassen mit eindeutigen Namen;
- globale Kompatibilitätsfunktionen erst nach dem Laden aller Plugin-Mainfiles und nur wenn sie noch nicht existieren;
- eigene Frontend-Hooks mit hoher Priorität, damit der aktuelle Register-Renderer gewinnt.

Erhalten:
- 862 Hobbys;
- 57 Traits;
- 862 statische Artikel;
- 862 Bildzuordnungen;
- Selbe Hobbygruppe;
- kein Detailbanner unten;
- Portalbreite `min(calc(100% - 72px),1440px)`.

## QA

Fresh-Unpack:
- genau eine Pluginwurzel;
- PHP-Lint 4/4 PASS.

Daten:
- 862 Records;
- 57 Traits je Hobby;
- 862 Artikel;
- je 8 Textabschnitte;
- 862 Bildzuordnungen.

Slug-/Artikelprüfung:
- 862/862 PASS.

Vollrender:
- 3D-Druck PASS;
- Geocaching PASS;
- Buchbinden PASS;
- Slacklining PASS;
- Aquaristik PASS;
- Münzen PASS;
- Unterwasserhockey PASS;
- Air-Dry Clay PASS.

Registerindex:
- PASS.

Doppelplugin-Simulation:
- alte Version -> 1.2.7: PASS, kein Fatal;
- 1.2.7 -> alte Version: PASS, kein Fatal.

Kein Live-PASS behaupten.
