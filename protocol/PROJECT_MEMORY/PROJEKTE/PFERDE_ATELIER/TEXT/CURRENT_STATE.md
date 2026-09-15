# PFERDE ATELIER – TEXT – CURRENT STATE

STAND: 2026-09-11
STATUS: BLOCKED / ONE-FRESH-ARTICLE REALTEST NEXT

## EINE AKTUELLE WAHRHEIT

Current technical main:
`f1d1605f18bd23d9189f89ad173598958718d08a`

Letzter belastbarer Live-/Recovery-Baseline-Stand vor M37:
`bb005a5324a0a6270aacb52b5927613bde1ab4bc`

Aktuelle autoritative Fehlerquelle:
`QUELLEN_AKTUELL/04_FEHLERLISTE_KOMPLETT_AKTUELL_20260911.md`

## M37 – ABGESCHLOSSEN UND INTEGRIERT

History-Phase:
- PR248;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS.

Produktfix:
- PR247;
- Kandidat `59ad44da3d89769c05f0725f9929135b0262f4dd`;
- `HOBBYROOM_HISTORY_MACHINE_PROOF_PASS:M37`;
- hardlock PASS;
- hardlock-base PASS;
- neuer Main `f1d1605f18bd23d9189f89ad173598958718d08a`.

M01–M37 sind damit die integrierte bekannte Regression.

## AKTUELLER REALBLOCKER

Der letzte frische Lauf vor M37 erreichte realen PPM/PSERC und endete äußerlich bei:
`PPM679_REAL_EXECUTION_BLOCKED`.

Der damalige innere Grund ist nicht mehr rekonstruierbar.
**Produktions-Rootcause bleibt UNKNOWN.**

## NEXT ACTION

Genau einen frischen ersten Artikel über den offiziellen aktuellen 107007-Weg bis zum realen LanguageTool-/PPM-/PSERC-Handoff ausführen.

Bei erstem BLOCKED/REPAIR_REQUIRED:
- exakt stoppen;
- nur den ersten konkreten neuen Grund übernehmen;
- keine Reparatur im laufenden Test.

Bei Ein-Artikel-PASS:
- erst danach Restbatch fortsetzen.

## HARTE GRENZEN

- kein neuer Runner/Gate/Controller/Sidecar;
- keine Regeländerung;
- kein Rootcause raten;
- kein zweiter Artikel vor Auswertung des ersten;
- kein 7/7-Diagnoselauf vor Ein-Artikel-Beweis;
- kein WordPress-Write;
- Kein Publish.
