# System 4 — Codex-Lauf: Protokoll für Optimierungspotenzial — 2026-09-18

## Zweck

Nur Beobachtungs-/Optimierungsprotokoll. Keine Produktionslogik, keine Fachregeln, kein Publish und kein Eingriff in den laufenden Codex-Auftrag.

## Aktuelle Referenz

- geprüfter main vor Codex-Start: `df30a8cf7a157ee4eba979e272ad3d1eb76a5544`
- aktueller Batch: `7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a`
- Runtime-Generation: `1`
- aktueller Codex-Startkommentar: PR #83, Comment `5734493708`
- vollständige System-4-Abnahme auf exakt diesem main: Run `35380544689` = SUCCESS
- Auto-Publish: `false`

## Beobachtete Reibungsverluste / Fehlerquellen

1. Trigger-Branch konnte veralten. PR #83 zeigte vor der letzten Freigabe noch auf einen älteren Commit.
2. Codex-spezifische Startanweisung konnte vom aktuellen Maschinenweg abweichen. `AGENTS.override.md` enthielt noch den alten direkten Root-Start. Der aktuelle Produktionsweg verlangt `python3 isolated_system4/parent_start.py start-current-bound`.
3. Historischer Startfehler: `ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO`.
4. Historischer Startfehler: `PARENT_SOURCE_REQUEST_MISSING`, verursacht durch einen manuell vorgegebenen Pfad ohne maschinell erzeugte gebundene Source-Requests.
5. Zu viele getrennte Vorprüfungen erhöhen Drift- und Wiederholungsrisiko.
6. CURRENT_STATE kann fachlich korrekt sein, während eingebettete Beweis-SHAs älter als der tatsächliche main sind.
7. Codex-Laufstatus ist während der Ausführung über PR-Kommentare nur begrenzt sichtbar.
8. Parent-Chat-Dateirückgabe muss ein eigenes hartes Abschlusskriterium bleiben. `/tmp`, Codex-Sandbox, Log oder kurzlebiges Actions-Artefakt sind kein gültiger Abschluss.
9. NEW-Regel muss direkt im Worker-Start gebunden bleiben: alte Recovery-Artikel, alte Drafts, frühere Codex-Texte, historische Handoffs und `.pferde-release/**` dürfen nie Schreibquelle sein.

## Konkretes Optimierungspotenzial

### A. Ein einziger maschinenfester PRE-CODEX-CHECK

Vor Codex genau einen Checker, der in einem Ergebnis prüft:

- current main SHA
- PR #83 head == current main
- aktueller 107007-Step-Hash
- Current-State-Hash
- Source-Requests-Hash
- Source-Snapshot-Hash
- Production-Package-Hash
- Batch-SHA / Generation / Artikelanzahl
- `AGENTS.override.md` verlangt exakt `start-current-bound`
- keine manuellen Workspace-/Source-Request-Pfade
- NEW-Regeln aktiv
- kein vorhandener Generation-Replay/Endstempel
- Durable-Release-/Parent-Chat-Strecke vorhanden
- `publish_allowed=false`

Nur ein Ergebnis: `PRECODEX_READY_PASS` oder erster exakter Blocker.

### B. Trigger-Head automatisch prüfen

Start blockiert, wenn `PR83_HEAD != MAIN_HEAD`.

### C. Startanweisung gegen Step automatisch binden

Start blockiert, wenn die Codex-Anweisung nicht exakt dem aktuell autorisierten Produktionseinstieg entspricht.

### D. Keine manuellen externen Pfade mehr

Run-Root, Source-Requests-Kopie, Point-0, Batch-Root und Workspaces nur durch die Maschine erzeugen.

### E. CURRENT_STATE-Frische explizit prüfen

Eigener Hinweis/Blocker `CURRENT_STATE_EVIDENCE_STALE`, wenn aktuelle Beweise nicht zum neuesten main gehören.

### F. Testmenge reduzieren, Aussagekraft erhöhen

Nach Reparatur:
1. gezielter Test der Fehlerklasse,
2. genau eine vollständige System-4-Abnahme auf endgültigem main,
3. keine redundanten Wiederholungsläufe vor Codex.

### G. Codex-Fortschritt maschinenlesbar machen

Persistenter read-only Status mit Item 0..N, Phase, Revision und letztem PASS/Blocker — ohne Artikelbytes.

### H. Abschluss immer mit Durable-Asset-Beweis

Terminaler PASS nur mit Endstempel-PASS, finalem Dateinamen, finalem SHA-256, Release-Tag, dauerhaftem Release-Asset und Parent-Chat-Bytevergleich PASS.

## Wichtig für spätere Auswertung

Priorität:
1. manuelle Startschritte eliminieren,
2. mehrere Vorprüfungen zu einem einzigen Checker zusammenziehen,
3. eindeutige Frische-/SHA-Wahrheit,
4. Fortschritt sichtbar machen,
5. finalen Parent-Chat-Dateitransport als harten Abschluss beibehalten.

## Laufender Produktionslauf

Während dieses Protokolls wurde kein weiterer Codex-Start ausgelöst und `main` nicht verändert. Der bereits freigegebene Lauf aus PR #83 / Comment `5734493708` bleibt der einzige laufende Produktionsauftrag.
