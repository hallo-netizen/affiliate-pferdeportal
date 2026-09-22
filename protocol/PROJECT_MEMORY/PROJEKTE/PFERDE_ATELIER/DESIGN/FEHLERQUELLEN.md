# PFERDE-ATELIER DESIGN – FEHLERQUELLEN

STAND: 2026-09-16

Keine zweite Fehlerwahrheit. Aktueller Stand ausschließlich aus `CURRENT_STATE.md`.

## DESIGN-LIVE-20260915-001

STATUS: **CLOSED / AKTUELLER DESIGNSTAND 1.50.541 WORDPRESS-LIVE PASS**

HISTORISCHER BEFUND:
Nach der damaligen Design-Pluginfolge meldete der Nutzer real LIVE:
- Pferderassen-Seite nicht mehr auffindbar / zerschossen;
- Glossar nicht mehr auffindbar.

BETROFFENE HISTORISCHE KANDIDATEN:
- Pferde Atelier Design 1.50.529: real als fehlerhaft gemeldet;
- 1.50.530: nachträglicher lokaler Fixkandidat ohne damaligen LIVE-PASS;
- Universal Portal Design Suite 2.2.42: Rolle im damaligen Ausfall nicht eindeutig belegt.

DAUERHAFTE LERNREGEL:
Kein Designplugin-PASS aus isolierter Codeprüfung, wenn mehrere Designplugins gemeinsam wirken. Positiv-, Negativ- und relevante Kombinationsregression sowie WordPress-LIVE bleiben erforderlich.

SCHLIESSUNG:
Spätere gebundene Pferde-Designstände wurden lokal geprüft und real in WordPress abgenommen. Aktuell ist **Pferde Atelier Design 1.50.541** LIVE PASS. Der alte Incident blockiert deshalb die aktuelle Arbeit nicht mehr.

WICHTIG:
Eine nachträgliche eindeutige technische Root-Cause-Zuweisung des historischen 1.50.529/1.50.530-Ausfalls wird nicht erfunden. Die Schließung bedeutet: aktueller Fehlerpfad nicht mehr reproduziert / aktueller LIVE-Stand funktionsfähig, nicht nachträgliche Ursachenbehauptung.

## HISTORISCHE FEHLERKETTEN

### V104 Tabellenabstand
GitHub-Autorität: `design-baseline/2026-08-22/v101` bis `v104`.
V104 bleibt der historisch belegte nicht kollabierende Tabellenabstand-Fix.

### Kategorie-Reihenfolge 2026-09-07
STATUS: CLOSED / LIVE PASS.
Finaler Job: `DESIGN-ORDER-SWAP-002`.
Belege: `LIVE_PASS_DESIGN_ORDER_SWAP_002.md`, `MINIMAL_PATCH_LAST_RECEIPT.json`.

### Journal-Startseite 2026-09-16
1.50.540: Hauptkarten-Fettung + weniger Crop/rechter Bildfokus LIVE grundsätzlich PASS; Referenzkacheln `Glossar`/`Pferderassen` noch nicht fett.
1.50.541: ausschließlich diese beiden Referenztitel ergänzt; Nutzerbestätigung `ok pass`.
