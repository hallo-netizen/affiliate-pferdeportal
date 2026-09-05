# HANDLUNGSVERZEICHNIS

STAND: 2026-09-05

Zweck: „Ich will X tun – welcher vorhandene Weg ist verbindlich?“

HARD RULE:
**Bekannte Aktion niemals erraten. Existiert ein definierter Workflow, darf kein Ersatzweg erfunden werden.**

## Neues Projekt beginnen

Aktion: eigenständiges neues Projekt aufsetzen

Verbindlicher Weg:
1. `HAUPTPFOERTNER.md`
2. Anforderungen/Ziel des Projekts bestimmen
3. `ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md`
4. passende vorhandene Module auswählen
5. nur relevante Modulakten lesen
6. minimales Projektgebäude nach `BAUCONTAINER/NEUES_PROJEKT_VORLAGE.md` anlegen
7. projektbezogene Nutzung/Config dokumentieren

Nicht erlaubt:
- Pferde-Atelier blind kopieren
- bekannte Grundmodule neu erfinden
- alle Campusakten ungefiltert in ein neues Projekt kopieren

## Neue Masterdatei aufnehmen

Aktion: Masterdatei/Archiv/Pluginpaket übernehmen

Verbindlicher Weg:
1. `BAUCONTAINER/MASTERDATEIEN_REGEL.md`
2. vollständig inventarisieren
3. nichts still verwerfen
4. Bestandteile klassifizieren
5. Modul-Kern bestimmen
6. `ALLGEMEINGUELTIGE_BAUSTEINE/MODULREGISTER.md` prüfen/aktualisieren
7. genau einen Hauptort festlegen
8. Projektanwendung nur referenzieren

## Codex / technische Projekteingangstür

Aktion: Codex-Arbeit im Repository beginnen
Autorität: Root-`AGENTS.md`
Verbindlicher Start:
`python3 control/cloud-entry-gate/cloud_entry.py start`

Bei BLOCKED: stoppen. Keine Alternativroute.

## Textmaschine / Artikelproduktion

Autorität:
- Root-`AGENTS.md`
- aktueller technischer State unter `control/startmaster0107/`
- gebundene Capsule/Instruction

Keine manuelle freie Artikelproduktion als Ersatz.
Während paralleler TEXT-Arbeit zuerst TEXT-`CURRENT_STATE.md` neu synchronisieren.

## Text-Regression

Matrix:
`control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`

Runner:
`control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`

Keine theoretischen Zusatzprüfungen anstelle des Matrixprozesses.

## Affiliate-Release

Autorität:
`control/release-governance/CURRENT_RELEASE.json`

Prüfer:
`control/release-governance/release_guard.py`

Zusatzregeln:
`release/affiliate-zentrale/AGENTS.md`

Keine Rekonstruktion oder Ersatzroute bei Governance-Blockade.

## Unbekannte Aktion

Wenn kein eindeutiger Eintrag existiert:
**STOPP – nicht raten.**
Erst Zuständigkeit und vorhandenen Arbeitsweg klären.
