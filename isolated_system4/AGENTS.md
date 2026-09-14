# SYSTEM 4 — VERBINDLICHE ARBEITSREGELN

Scope: nur `isolated_system4/**`. Kein Merge, kein Publish. Produktions-Workspaces und Artikeloutput liegen außerhalb des Repositories.

## Eine Produktionsstraße

Es gibt nur diesen Produktionsweg:

`Machine source/prewrite → Point-0 V2 → Root → Supervisor → Worker-Dispatch → Research → Facts → Context → Draft → fullcheck → Same-Article-Repair → Batch → V2-Handoff`.

Keine alternative Route, kein Legacy-Orchestrator, kein STARTMASTER/H7/H8/ACM/System3-Runtimepfad.

## Vor Codex unveränderlich

Die Maschine bindet je Artikel vor Worker-Start:
- Artikelidentität und `plan_slot`;
- Kategorie;
- interne Linkbindungen und `quality_binding`;
- eigenen Research-Pool;
- Git-Head, Root-Manifest und `publish_allowed=false`.

Worker-Dispatch muss `external_web_search_allowed=false` und `machine_prewrite_mutation_allowed=false` enthalten. Codex darf weder fremde Quellen einschleusen noch die gebundenen Schienen neu definieren.

## Codex

Codex ist der einzige fachliche Worker. Er wertet die gebundenen Quellen aus, erzeugt Facts, ergänzt nur erlaubte faktabhängige Context-Felder, schreibt den Artikel und führt verlangte Same-Article-Reparaturen aus. Er besitzt weder Workflow noch Textmaschine noch Design noch PASS.

## Textmaschine / Design unveränderlich

Textmaschine, PPM 6.7.9, LanguageTool 6.8, Authoring-/Content-/Designregeln, WordPress-Plugin, Theme/CSS und bestehende Designselektoren sind READ-ONLY. Keine Ersatzregel, kein CSS, kein Inline-Style, keine nachträgliche HTML-Normalisierung.

`controller.py fullcheck` ist der einzige Produktions-Prüforchestrator. Reparierbare Befunde führen zu `REPAIR_REQUIRED`; danach ausschließlich `controller.py repair` am selben Artikel und erneuter `fullcheck`. Broad rewrite ist verboten und mechanisch zu blockieren.

## Research / Facts

`RESEARCH_REQUIRED` akzeptiert nur den exakt vom Supervisor gebundenen artikelbezogenen Pool. `FACT_CHECK_REQUIRED` akzeptiert nur Claims mit akzeptierter `source_id`, realem `evidence_text` und passendem SHA. Fact-Pack und Article-Fact-Traces müssen dieselben akzeptierten Quellen/Fakten binden.

## 1..N und Batch

Der gebundene Snapshot bestimmt exakt Anzahl und Reihenfolge. Jede endliche Anzahl `1..N` verwendet denselben Pfad. Kein Drop, Duplikat, Austausch oder Reordering. Alle Artikel müssen `OUTPUT_GATE_REQUIRED` mit FULL_PRODUCTION PASS erreichen, bevor `batch_gate.py collect` laufen darf.

## Handoff

Finaler Vertrag: `SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2`. Der Parent-Chat muss nach Canonicalize/Inline-Pack/Inline-Unpack exakt dieselben Bytes rekonstruieren. Kein Repository-/Git-/Codex-Sandbox-Handoff. `publish_allowed=false` bleibt gesetzt. Signing/ENDSTEMPEL bleiben aus, solange der bestehende WordPress-Signature-Switch aus ist.

## Testregel

Die Live-Paritätsstrecke darf keinen vereinfachten Checker-/Root-Pfad besitzen. Im Test darf ausschließlich Codex durch einen deterministischen Testworker ersetzt werden. Echte LT-/PPM-Prüfer, Root, Supervisor, Dispatch, Controller, Repair, Batch und Handoff bleiben identisch. Historische Negativfälle und neue Point-0-V2/Prewrite-Angriffe sind Pflichtregressionen.
