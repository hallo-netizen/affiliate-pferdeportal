# HANDLUNGSVERZEICHNIS

STAND: 2026-09-05

HARD RULE:
**Bekannte Aktion niemals erraten. Existiert ein definierter Workflow, darf kein Ersatzweg erfunden werden.**

## Architektur verbessern

Aktion:
Ein Chat erkennt in realer Arbeit einen Optimierungsbedarf am Campus.

Verbindlicher Weg:
1. konkreten Bedarf benennen;
2. kleinste nachhaltige Architekturänderung wählen;
3. nur Architektur-Ebene verändern, keine fremde Facharbeit;
4. `BAUCONTAINER/BAUPROTOKOLL.md`;
5. dauerhaftes WARUM → `AENDERUNGSREGISTER.md`;
6. bei Fehler → `BAUCONTAINER/ARCHITEKTUR_FEHLERKISTE.md`;
7. Hardlocks/Prüfung.

Kein spezieller Architekten-Chat erforderlich.

## Hausmeister-Lauf

Aktion:
Produktive Räume auf Ballast prüfen.

Verbindlicher Weg:
`BAUCONTAINER/HAUSMEISTER.md`

Harte Grenzen:
- AKTIV nicht verschieben;
- UNGEKLÄRT nicht verschieben;
- keine Löschung;
- vor Verschiebung Referenzen/Hash/Ziel prüfen;
- jede Verschiebung im `ARCHIV/HAUSMEISTER_PROTOKOLL.md`.

## Neues Projekt beginnen

1. Hauptpförtner;
2. Ziel/Anforderungen;
3. Modulregister;
4. passende vorhandene Module;
5. minimales Projektgebäude.

## Neue Masterdatei aufnehmen

1. `BAUCONTAINER/MASTERDATEIEN_REGEL.md`;
2. vollständig inventarisieren;
3. Artefakte trennen;
4. Modulklasse prüfen;
5. Modulregister aktualisieren;
6. Hauptort/Archivzuordnung bestimmen.

## Codex / technische Projekteingangstür

Autorität: Root-`AGENTS.md`
Start:
`python3 control/cloud-entry-gate/cloud_entry.py start`

Bei BLOCKED: stoppen. Keine Alternativroute.

## Textmaschine / Artikelproduktion

Autorität:
- Root-`AGENTS.md`
- aktueller technischer State unter `control/startmaster0107/`
- gebundene Capsule/Instruction

Keine manuelle Ersatzproduktion.

## Text-Regression

Matrix:
`control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`

Runner:
`control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`

## Affiliate-Release

Autorität:
`control/release-governance/CURRENT_RELEASE.json`
`release/affiliate-zentrale/AGENTS.md`

## Unbekannte Aktion

**STOPP – nicht raten.**
Erst Zuständigkeit und vorhandenen Arbeitsweg klären.
