# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.2.6 KOMPILIERTE DATENREPARATUR / LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.6_FULL_REPARIERT_KOMPILIERT.zip`

SHA-256:
`875b498b2437697c96c35fb7d6899cbb5c7f9af4c66b7c79a4e56d3c92fd9a0c`

## Reparatur

Der wiederkehrende Fehler „Hobby nicht gefunden / Artikel weg“ wird am Datenladepfad beseitigt.

1.2.6 lädt primär kompiliert:
- 862 Registerdatensätze;
- 862 Artikel;
- 862 Bildzuordnungen;
- Traitschema.

Die großen JSON-Dateien sind nur noch Fallback.

## Weiterhin enthalten

- 862/862 Hobbys;
- 57/57 Traits;
- 862 statische Texte mit je 8 Abschnitten;
- aktuelle Register-/Profiloberfläche;
- `Selbe Hobbygruppe`;
- kein Detail-Banner unten.

## QA

Fresh-Unpack:
- genau eine Pluginwurzel `hd-hobbyregister-core/`;
- ready PASS;
- count 862;
- 862/862 Profile gerendert;
- Registerindex PASS;
- PHP-Lint PASS.

Harter Failover:
- gesamter JSON-`data/`-Ordner entfernt;
- ready PASS;
- count 862;
- 862/862 Profile gerendert;
- Registerindex PASS.

Evidence:
`EVIDENCE_1.2.6.md`

## EXAKT EINE NEXT ACTION

**1.2.6 über den bestehenden aktiven Ordner `hd-hobbyregister-core` kopieren/überschreiben und Registerstart plus ein Detailprofil live prüfen.**
