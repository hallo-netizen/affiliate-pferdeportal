# PFERDE-ATELIER DESIGN – FEHLERQUELLEN

Keine zweite Fehlerwahrheit.

## DESIGN-LIVE-20260915-001

STATUS: **AKTIV / BLOCKED**

SYMPTOM:
Nach der in diesem Chat erzeugten Design-Pluginfolge meldet der Nutzer real LIVE:
- Pferderassen-Seite nicht mehr auffindbar / zerschossen;
- Glossar nicht mehr auffindbar.

BETROFFENE KANDIDATEN:
- Pferde Atelier Design 1.50.529: vom Nutzer real als fehlerhaft gemeldet;
- Pferde Atelier Design 1.50.530: nur als nachträglicher lokaler Fixkandidat erzeugt, **keine Abnahme, kein LIVE-PASS**;
- Universal Portal Design Suite 2.2.42: im selben Änderungszug erzeugt; Rolle im realen Fehler **UNGEKLÄRT**.

FEHLER IN DIESEM CHAT:
- Pluginänderungen wurden zu früh als lokal ausreichend geprüft dargestellt;
- die Interaktion des allgemeinen und des Pferde-Designplugins war vor Ausgabe nicht belastbar reproduzierbar belegt;
- ein realer LIVE-Ausfall widerlegt die vorherige Abnahmebehauptung;
- danach wurden erneut Downloadpakete angeboten, bevor die tatsächlich installierte Plugin-Kombination frisch bestimmt war.

HARTE REGEL:
Kein Designplugin-PASS mehr aus isolierter Prüfung. Bei Änderungen an gemeinsam wirksamen Designregeln muss die reale Plugin-Kombination positiv **und** negativ geprüft werden. Ein Kandidat darf bei ungeklärtem LIVE-Ausfall weder als CURRENT synchronisiert noch als abgenommen ausgegeben werden.

ERFORDERLICHE REPARATUR:
1. installierte Versionen beider Designplugins frisch feststellen;
2. Fehler exakt reproduzieren;
3. Ursache zwischen allgemeinem Plugin, Pferde-Plugin oder Interaktion isolieren;
4. Pferderassen + Glossar gemeinsam als Pflichtregression testen;
5. erst dann minimaler Fix und WordPress-LIVE-Readback.

## HISTORISCHE FEHLERKETTEN

### V104 Tabellenabstand
GitHub-Autorität: `design-baseline/2026-08-22/v101` bis `v104`.
V104 bleibt der historisch belegte nicht kollabierende Tabellenabstand-Fix.

### Kategorie-Reihenfolge 2026-09-07
STATUS: CLOSED / LIVE PASS.
Finaler Job: `DESIGN-ORDER-SWAP-002`.
Belege: `LIVE_PASS_DESIGN_ORDER_SWAP_002.md`, `MINIMAL_PATCH_LAST_RECEIPT.json`.
