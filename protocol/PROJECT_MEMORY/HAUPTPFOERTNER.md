# HAUPTPFÖRTNER – Campus-Eingang

STAND: 2026-09-05
STATUS: V1 / Organisations-Hobbyraum
BASIS-MAIN: 54c68a0242da568a0c542f3a73250283b3bce63c

## Zweck

Zentraler organisatorischer Einstieg und Resetpunkt für Menschen und Chats.

Der Hauptpförtner ersetzt NICHT die technische Codex-Eingangstür in `AGENTS.md`.
Maschinenraum, Gates, Runtime, Release-Governance und bestehende technische Regeln bleiben autoritativ.

## Wenn der Nutzer sagt: „Hauptpförtner.“

Der Chat MUSS:

1. diesen Hauptpförtner lesen;
2. das richtige Projektgebäude bestimmen;
3. dessen `START_HERE.md` lesen;
4. das zuständige Büro bestimmen;
5. dessen `CURRENT_STATE.md` lesen;
6. dessen `HOBBYRAUM.md` lesen;
7. im `HANDLUNGSVERZEICHNIS.md` den vorhandenen Arbeitsweg nachsehen;
8. relevante Einträge im `FEHLERREGISTER.md` und `AENDERUNGSREGISTER.md` lesen;
9. relevanten aktiven Zielvertrag im `ZIELVERTRAEGE/REGISTER.md` prüfen;
10. bei Modul-/Plugin-/Masterdatei-Fragen zusätzlich `ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md` lesen;
11. erst danach weiterarbeiten.

## Pflicht-Rückmeldung nach Reset

- PROJEKT:
- BÜRO:
- AKTUELLER AUFTRAG:
- AKTIVER ZIELVERTRAG:
- LETZTER SICHERER STAND:
- NÄCHSTER SCHRITT:
- VERBINDLICHER ARBEITSWEG:
- RELEVANTE SPERREN:

Wenn ein Punkt nicht eindeutig gefunden wird:
**STOPP – NICHT RATEN. Keine Ersatzroute erfinden.**

## Campus

Aktuelles Projektgebäude:
- `PROJEKTE/PFERDE_ATELIER/`

Projektübergreifendes Gebäude:
- `ALLGEMEINGUELTIGE_BAUSTEINE/`

Zentrales Modulgedächtnis:
- `ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md`

Zielverträge:
- `ZIELVERTRAEGE/`

Historische Akten:
- `ARCHIV/`

Der Campus ist organisch und jederzeit erweiterbar/umbaubar.

## Neues Projekt – automatische Modulprüfung

Der Projektstart-Ablauf („Oberwachtmeister“) MUSS:
1. Hauptpförtner lesen;
2. Anforderungen/Zielvertrag bestimmen;
3. MODULREGISTER prüfen;
4. passende ALLGEMEINGÜLTIGE Module verwenden;
5. bei UNGEKLÄRT nicht raten;
6. nur fehlende Funktionen neu bauen.

Der Nutzer muss nicht erinnern, welche Module existieren.

## Neue Masterdatei / neues Plugin

Immer automatisch:
vollständig inventarisieren → Artefakte trennen → Modulklasse prüfen → Modulregister aktualisieren → Hauptort/Archivzuordnung bestimmen.

## Zugriffsschutz

Aktueller Campus-Prototyp liegt noch im öffentlichen Pferde-Atelier-Repository.

Offene Architekturentscheidung:
**Soll der Campus in ein eigenes privates GitHub-Repository umziehen?**

Empfehlung:
JA, sobald das Campusmodell als V1 bestätigt ist.

Grund:
mehrere Projektgebäude gehören logisch nicht einem einzelnen Projekt-Repository; zentrale Projektakten und Roharchive lassen sich dort sauber geschützt verwalten.

Bis zur Entscheidung:
keine Secrets oder ungeschützten Zugangsdaten in den öffentlichen Campus-Prototyp schreiben.

## Katastrophenfall

Einstieg:
`protocol/PROJECT_MEMORY/TRESOR/NOTFALL_WIEDERAUFBAU.md`

Nur einen geprüften `TRESOR_PASS`-Stand verwenden.
