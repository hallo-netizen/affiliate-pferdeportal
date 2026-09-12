# BAUCONTAINER – BAUAUFNAHME 2026-09-05

STATUS: READ-ONLY SNAPSHOT
ZWECK: Vorarbeit für späteres Aufräumen. Keine dieser Klassifizierungen ist ein Lösch- oder Verschiebefreibrief.

## Repository-Basis bei Aufnahme

- Repository: `hallo-netizen/affiliate-pferdeportal`
- main: `54c68a0242da568a0c542f3a73250283b3bce63c`
- main geschützt: JA
- aktives Ruleset: `Pferde Atelier Main Hardlock`
- Required Checks: `hardlock`, `hardlock-base`
- Bypass: keiner

## Größenbild

Read-only ermittelt:

- 281 Tree-Einträge auf main
- 37 Root-Dateien
- 7 Root-Verzeichnisse
- 17 ZIP-Dateien
- 68 Markdown-Dateien
- 63 JSON-Dateien
- 52 Python-Dateien
- 256 Branches
- 212 unterschiedliche Branch-Head-Commits
- 15 Gruppen mit identischem Head auf mehreren Branches

## Aktive/geschützte Maschinenraum-Pfade

Besonders geschützt bzw. technisch sensibel:

- `.github/workflows/**`
- `AGENTS.md`
- `control/cloud-entry-gate/**`
- `control/deterministic-entrance-gate/**`
- `control/production-continuity/**`
- `control/startmaster0107/ENDSTEMPEL_*`

Diese Bereiche werden durch den Organisationsumbau nicht verändert.

## Aktuelle bekannte Fachautoritäten

TEXT:
- Root-`AGENTS.md`
- `control/CURRENT_STARTMASTER.json`
- `control/startmaster0107/`
- M01–M33-Matrix + ausführbarer Runner

AFFILIATE:
- `release/affiliate-zentrale/AGENTS.md`
- `control/release-governance/CURRENT_RELEASE.json`
- `control/release-governance/release_guard.py`

DESIGN / HIVEPRESS:
- fachlich getrennte Zuständigkeiten;
- technisch können gemeinsame Template-/Plugin-Dateien betroffen sein;
- aktuelle Originalautoritäten vor erster neuer Arbeit noch hart zu verifizieren.

## Laufende TEXT-Baustelle zum Aufnahmezeitpunkt

- PR #132: `Hobbyraum M26 regression-matrix verification`
- Issue #133: `REAL 7-Artikel-Textlauf`

Darum wird TEXT während des Organisationsumbaus nicht repariert und sein finaler CURRENT_STATE erst nach Ende des Nachbarchats frisch übernommen.

## Altbestand – nur Klassifikationskandidaten

Root enthält zahlreiche:
- historische CODEX-ZIPs;
- QUELLCODE-ZIPs;
- PROTOKOLL-Dateien;
- frühere Reparaturstände.

Unter `control/` existieren mehrere STARTMASTER-Generationen.
Unter `protocol/` existieren historische Übergaben/Protokolle.
Es existieren sehr viele alte Reparatur-/Test-/Restore-Branches und offene Alt-PRs.

Aktueller Status dafür:
**ARCHIV-/BEREINIGUNGSKANDIDAT – NICHT ANFASSEN**

Vor jeder echten Verschiebung/Löschung:
1. vollständige Referenzprüfung;
2. Hash-/Workflow-/Pfadabhängigkeiten prüfen;
3. Beweis-/Regressionseignung prüfen;
4. erst danach klassifizieren: AKTIV / HISTORISCH / ARCHIV / UNGEKLÄRT.

UNGEKLÄRT = NICHT ANFASSEN.
