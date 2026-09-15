# DESIGN – HOBBYRAUM

STAND: 2026-09-15
STATUS: BLOCKED

## AKTUELLE ARBEIT
Reparatur des realen LIVE-Ausfalls nach der in diesem Chat erzeugten Design-Pluginfolge.

Symptome laut Nutzer:
- Pferderassen-Seite nicht mehr auffindbar / zerschossen;
- Glossar nicht mehr auffindbar.

## HARTE SPERRE
Keine weitere Plugin-Ausgabe und keine Abnahme aus isolierter Codeansicht.
Kein Raten über die Ursache.

## NEXT ACTION
1. real installierte Version des **Pferde Atelier Designplugins** frisch bestimmen;
2. real installierte Version des **Universal Portal Design Suite** frisch bestimmen;
3. exakt diese Kombination als lokale Ausgangsbasis reproduzieren;
4. Pferderassen-Route/Template und Glossar-Route/Template jeweils positiv prüfen;
5. Negativtests erzwingen, die einen Ausfall einer der beiden Welten erkennen;
6. Plugin-Interaktion gemeinsam prüfen;
7. Ursache isolieren;
8. nur minimalen Fix auf exakter Basis bauen;
9. ZIP/Version/Install-over-old/Positiv/Negativ/Regression hart prüfen;
10. erst nach realem WordPress-Readback Freigabe/CURRENT-Sync.

## VERBINDLICHER ARBEITSWEG
Branch: `hobbyroom/project-memory-campus-v1-20260905`

Fehlerautorität: `FEHLERQUELLEN.md` → `DESIGN-LIVE-20260915-001`.
Bürostand: `CURRENT_STATE.md`.
Plugin-Sync erst nach Fach-PASS über `../PLUGINS/`.

## NICHT ANFASSEN
- keinen alten Stand allein aufgrund einer Versionsnummer als aktuell installiert annehmen;
- 1.50.529/1.50.530 nicht als freigegeben behandeln;
- Universal 2.2.42 nicht als unschuldig oder schuldig behaupten, bevor die reale Kombination geprüft ist;
- keine neue Versionsserie vor reproduzierter Ursache.
