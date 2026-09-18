# STARTMASTER0107 – AKTUELLE FEHLERQUELLE

STAND: 2026-09-18
ROLLE: AUTORITATIVE FEHLERQUELLE FÜR PFERDE_ATELIER / TEXT / STARTMASTER0107

## AKTUELLER FEHLERSTATUS

**Kein offener technischer Projektfehler vor dem realen Codex-Lauf.**

Die einzige aktuelle Sperre ist **keine Fehlerklasse**, sondern eine Freigabesperre:
`EXPLICIT_CODEX_APPROVAL_MISSING`.

Aktuellen operativen Status, Blocker und NEXT ACTION ausschließlich aus:
`control/startmaster0107/CURRENT_STATE.json`

## REGRESSION

M01–M39 bleiben als bekannte Fehler-/Regressionklassen verbindlich erhalten.

Autoritative technische Regressionsquelle:
`control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`

Bestehender Regressionrunner:
`control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`

## LETZTE RELEVANTE FEHLERSTATUSÄNDERUNGEN

- M37: integriert / Regression.
- M38 `PSERC_BRIDGE_PPM_PLAN_VERSION_MISMATCH`: Produktfix integriert; Regression PASS.
- M39 `CURRENT_7ER_BATCH_ALREADY_HAS_DURABLE_RELEASE_IDENTITY_COLLISION`: durch getrennte technische Release-Identität gelöst und integriert.
- Historische Recovery-/Altartikel bleiben als Produktionsquelle verboten.
- Fehlende Point-0-Datei bleibt fail-closed.
- Artikelidentität vor Batch-`advance` bleibt maschinell gebunden.
- Kein Publish ohne separate Nutzerfreigabe.

## AKTUELLER BELEG

Technischer Produktions-CURRENT:
`control/startmaster0107/CURRENT_STATE.json`

Dort gebunden:
- `current_work_status = PRECODEX_READY_AWAITING_EXPLICIT_CODEX_APPROVAL`
- `current_execution_blocker.code = EXPLICIT_CODEX_APPROVAL_MISSING`
- `publish_allowed = false`

Aktueller Repository-`main` beim Abschlusscheck:
`bc50759e5ce50cc3058c220bbdff6650a35fd06f`

Exakt auf diesem Main:
- System-4A Acceptance Run `35367822404`: **40/40 PASS**
- Deterministic Entrance Run `35364997364`: **PASS**

PR #325, der ausschließlich den finalen Pre-Codex-Status synchronisierte:
- Hardlock Run `35364953617`: **PASS**
- Deterministic Entrance Run `35364953439`: **PASS**

## REGEL

Neue reale Fehler werden hier mit eindeutiger Fehlerklasse aufgenommen. Ein Freigabeschritt, der absichtlich auf Nutzerentscheidung wartet, ist kein Projektfehler.
