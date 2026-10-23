# HD-007 – EVIDENCE 1.2.6 KOMPILIERTE DATENREPARATUR

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`HOBBY_DEPOT_HOBBYREGISTER_CORE_HD007_V1.2.6_FULL_REPARIERT_KOMPILIERT.zip`

SHA-256:
`875b498b2437697c96c35fb7d6899cbb5c7f9af4c66b7c79a4e56d3c92fd9a0c`

## Reparatur
Runtime-Daten nicht mehr primär aus großen JSON-Dateien:
- 862 Registerdatensätze als kompiliertes PHP;
- 862 Artikel als kompiliertes PHP;
- 862 Bildzuordnungen als kompiliertes PHP;
- Traitschema als kompiliertes PHP.

JSON bleibt nur Fallback.

Damit ist der Fehlerpfad
`JSON nicht lesbar/decodierbar -> Register leer -> Hobby nicht gefunden`
ausgeschaltet.

## QA
Fresh-Unpack:
- genau eine Pluginwurzel `hd-hobbyregister-core/`;
- PHP-Lint PASS;
- ready PASS;
- count 862;
- 862/862 Profile gerendert;
- Registerindex PASS.

Harter Failover-Test:
- kompletter `data/`-Ordner temporär entfernt;
- ready PASS;
- count 862;
- 862/862 Profile gerendert;
- Registerindex PASS.

Kein Live-PASS behaupten.
