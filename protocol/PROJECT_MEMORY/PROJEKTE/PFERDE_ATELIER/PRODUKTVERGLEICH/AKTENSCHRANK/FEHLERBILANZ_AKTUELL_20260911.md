# PRODUKTVERGLEICH – OPERATIVE FEHLERBILANZ

STAND: 2026-09-11
STATUS: AKTUELL

## AUTORITÄT

Diese Datei ist die einzige operative Fehlerwahrheit des Büros Produktvergleich.
`../FEHLERQUELLEN.md` bleibt ausschließlich Wegweiser und dupliziert keine Fehlerdetails.

## AKTIVE TECHNISCHE / FACHLICHE OFFENHEIT

### F-TECH-01 – UPC 0.8.6 WORDPRESS-LIVE NOCH OFFEN

Status: **OFFEN**

- UPC 0.8.6 ist lokal hart, Fresh-ZIP und read-only architektonisch geprüft.
- Ein WordPress-Live-Test von UPC 0.8.6 wurde nicht ausgeführt.
- Deshalb darf für UPC 0.8.6 kein WordPress-Live-PASS behauptet werden.
- Letzter tatsächlich belegter WordPress-Live-Stand bleibt UPC 0.8.5.

### F-TECH-02 – TECHNISCHE PROFILMATERIALISIERUNG NOCH OFFEN

Status: **OFFEN / READINESS-GAP**

- 150 Registry-Gruppen sind V1-fähig fachlich disponiert.
- UPC 0.8.6 enthält weiterhin nur 7 maschinenfeste Vergleichsprofile/Decision-Policies.
- 143/150 V1-fähige Gruppen sind technisch noch nicht materialisiert.
- Source-bound Profilspezifikationen ändern diesen technischen Bestand nicht automatisch.

## IN DER ABSCHLUSS-/NACHHOLPRÜFUNG GEFUNDEN UND REPARIERT

### F-GOV-01 – FEHLERQUELLEN ZEIGTE AUF NICHT VORHANDENE AKTE 24

Status: **REPARIERT 2026-09-11**

Befund:
- `FEHLERQUELLEN.md` verwies auf `AKTENSCHRANK/24_FEHLERBILANZ_NACH_V084_20260910.md`.
- Diese Datei ist am geprüften Produktvergleich-Branch nicht vorhanden.

Reparatur:
- operative Fehlerautorität auf diese Datei gelegt;
- `FEHLERQUELLEN.md` bleibt danach reiner Wegweiser.

Warum:
- Ein Fehlerweg darf nicht auf eine nicht vorhandene Quelle zeigen.
- Es darf genau eine operative Fehlerwahrheit geben.

### F-GOV-02 – CURRENT_STATE HINKTE HINTER BRANCH-HEAD HER

Status: **REPARIERT 2026-09-11**

Befund:
- Branch-HEAD `8f00f65254a63d21e9cf02f37df8839338d9684c` enthält Akte 84.
- `CURRENT_STATE.md` war nur bis Akte 82 / 61 source-bound Gruppen nachgezogen.

Reparatur:
- CURRENT_STATE auf Akten 62–84 / 67 source-bound Gruppen nachgezogen;
- nächster Registry-Block auf `hindernisstangen -> sprungstaender -> cavaletti` gesetzt.

### F-GOV-03 – HOBBYRAUM / NEXT ACTION HINKTE HINTER BRANCH-HEAD HER

Status: **REPARIERT 2026-09-11**

Befund:
- HOBBYRAUM band noch `schubkarren -> mistcontainer -> paddockzaeune`, obwohl Akten 83 und 84 bereits am Head vorhanden waren.

Reparatur:
- HOBBYRAUM auf Akte 84 / 67 source-bound Gruppen und den nächsten exakten Registry-Block nachgezogen.

### F-GOV-04 – TAGESPROTOKOLL WAR NUR BIS AKTE 65 NACHGEZOGEN

Status: **REPARIERT 2026-09-11**

Befund:
- `PROTOKOLL_20260911.md` enthält den chronologischen Stand nur bis Akte 65.
- Akten 66–84 waren dort noch nicht nachgetragen.

Reparatur:
- vollständige Nachhol-/Abschlussfortsetzung in `../PROTOKOLL_NACHHOLUNG_20260911.md` angelegt.
- Das alte Tagesprotokoll wird nicht rückwirkend umgeschrieben; die Fortsetzung ist ausdrücklich als Anschlussprotokoll gebunden und keine zweite CURRENT_STATE-Wahrheit.

### F-GOV-05 – COMMIT-SHA UND TREE-SHA IM CHAT KURZ VERWECHSELT

Status: **KORRIGIERT / KEIN REPO-FEHLER**

- aktueller geprüfter Commit-HEAD vor der Nachholung: `8f00f65254a63d21e9cf02f37df8839338d9684c`;
- dessen Tree-SHA: `70917470d9d8b85d5d33cf8004712b45dbf79acc`.
- Die Verwechslung war nur eine Zwischenangabe im Chat; Repository-Dateien wurden dadurch nicht überschrieben.

## NICHT ALS FEHLER UMINTERPRETIEREN

- Die 25 `PRODUCT_COMPARISON_V1_NOT_APPLICABLE`-Gruppen sind finale V1-Disposition und kein Coverage-Fehler.
- 67 source-bound Profilspezifikationen sind fachliche Vorbereitung, kein technischer Materialisierungs-PASS.
- Ein Profil mit 0 zulässigen Cross-Brand-Paaren kann korrekt fail-closed sein.

## REGEL

Neue operative Fehler, Statusänderungen, Reparaturen und Retests werden ausschließlich hier gepflegt oder – falls diese Datei ausdrücklich abgelöst wird – in genau einer klar benannten Nachfolgerquelle. Der zentrale `FEHLERREGISTER.md` und `FEHLERQUELLEN.md` bleiben Wegweiser.
