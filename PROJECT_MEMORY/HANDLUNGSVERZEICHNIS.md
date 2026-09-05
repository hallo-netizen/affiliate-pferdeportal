# HANDLUNGSVERZEICHNIS

STAND: 2026-09-05

Zweck: „Ich will X tun – welcher vorhandene Weg ist verbindlich?“

HARD RULE:
**Bekannte Aktion niemals erraten. Existiert ein definierter Workflow, darf kein Ersatzweg erfunden werden.**

## Codex / technische Projekteingangstür

Aktion: Codex-Arbeit im Repository beginnen
Autorität: Root-`AGENTS.md`
Verbindlicher Start:
`python3 control/cloud-entry-gate/cloud_entry.py start`

Bei BLOCKED: stoppen. Keine Alternativroute.

## Textmaschine / Artikelproduktion

Aktion: vorhandenen gebundenen Text-/Produktionsprozess ausführen
Autorität:
- Root-`AGENTS.md`
- aktueller technischer State unter `control/startmaster0107/`
- aktuell gebundene Capsule/Instruction

Keine manuelle freie Artikelproduktion als Ersatz für einen gebundenen Workflow.
Da aktuell parallel an TEXT gearbeitet wird: vor jeder neuen Textaktion zuerst TEXT-`CURRENT_STATE.md` neu synchronisieren.

## Text-Regression

Autoritative historische Matrix:
`control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`

Ausführbarer Runner:
`control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`

Keine theoretischen Zusatzprüfungen anstelle des gebundenen Matrixprozesses.

## Affiliate-Release

Autorität:
`control/release-governance/CURRENT_RELEASE.json`

Prüfer:
`control/release-governance/release_guard.py`

Zusätzliche Fachregeln:
`release/affiliate-zentrale/AGENTS.md`

Keine Rekonstruktion oder Ersatzroute, wenn die Governance blockiert.

## Unbekannte Aktion

Wenn kein eindeutiger Eintrag existiert:
**STOPP – nicht raten.**
Erst Zuständigkeit und vorhandenen Arbeitsweg klären.
