# AFFILIATE HOBBYRAUM V1

Zweck: Ein strikt isolierter Arbeitsraum ausschließlich für die AFFILIATE_ZENTRALE.

Regeln:
- genau EINE Aufgabe pro Lauf
- nur ausdrücklich freigegebene Eingabedateien
- keine Projekt-Gesamtsuche
- kein GitHub/Web/Netzwerk im Lauf
- kein Zugriff auf STARTMASTER/Textmaschine/andere Workstreams
- Originalprojekt wird nicht direkt verändert
- nur ausdrücklich erlaubte Dateien dürfen geändert werden
- keine Wiederholung alter PASS-Prüfungen
- keine Architekturänderung außerhalb der Aufgabe
- Ergebnis nur PATCH + erlaubte Output-Dateien
- Fehler => BLOCKED, keine Alternativroute

## Verbindliche Fehlermatrix
Datei: `AFFILIATE_HOBBYRAUM/FEHLERMATRIX.md`

- Die Matrix enthält alle bisher bekannten Affiliate-/Codex-/Arbeitsfehler.
- Sie wird automatisch in jeden Lauf als read-only Guard-Datei eingebunden.
- Bekannte technische Umwege werden bereits vor Ausführung BLOCKED.
- Vor jedem Lauf muss gegen die komplette Matrix geprüft werden.
- Jeder neue Fehler bekommt sofort eine neue AF-ID.
- Nach einem neuen Fehler darf kein zweiter Versuch starten, bevor die Matrix ergänzt wurde.

Runner:
python3 AFFILIATE_HOBBYRAUM/affiliate_hobbyraum.py TASK.json
