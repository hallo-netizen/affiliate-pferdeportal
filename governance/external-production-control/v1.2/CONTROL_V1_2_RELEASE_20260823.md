# External Production Control V1.2

## Ziel
Externe Governance-/Kontrollschicht. Der bestehende fachliche Workflow bleibt unverändert.

## Neue harte Regel
Jede konkrete Workflow-Anweisung benötigt eine maschinell erzeugte Authorization des aktuellen Zustands. Ohne gültige Authorization ist die Anweisung nicht ausführbar.

## Autoritätsreihenfolge
1. aktuelles autoritatives Live-Artefakt / Live-Zustand
2. CURRENT_STATE
3. hashgebundene aktuelle Artefakte
4. bindende MASTER-Regeln
5. Historie nur als Beleg
6. Erinnerung niemals als Navigationsquelle

## Auto-Correct-to-Workflow
- Resume vor Restart
- Reuse vor Recheck
- kein neuer Recherchelauf zur Auflösung bloßer Chat-Unsicherheit
- keine parallele äquivalente Aktion
- falsche oder redundante Aktion wird auf `NEXT_ALLOWED_STEP` zurückgeführt
- bereits bestandene Schritte werden ohne echten Delta-Trigger nicht erneut geöffnet

## Maintenance Lane
Technische Reparaturen laufen isoliert außerhalb des fachlichen Produktionspfads. Ein Maintenance-Fix darf den Primary Workflow nicht zurücksetzen. Nach PASS wird exakt am gespeicherten Primary Checkpoint fortgesetzt.

## Delivery Gate
Vor Chatende werden MASTER, CURRENT_STATE, Handoff, exakt nächste Eingabedatei sowie Instruction Authorization gegeneinander geprüft. Nur die mechanisch freigegebenen Dateien dürfen als aktuelle Übergabe ausgegeben werden.

## Aktueller Zustand
- Primary checkpoint: `SEO_BREADTH_RESEARCH_TERMINAL_RESULT_OBSERVED_CLIENT_GUARD_ERROR`
- Maintenance: PSTE 0.56.10 Final-Readback-Rootfix bereit
- Next allowed step: `INSTALL_PSTE_0_56_10_BREADTH_FINAL_READBACK_ROOTFIX`
- danach Resume: `POST_BREADTH_USE_CURRENT_SERVER_STATE_NO_RESEARCH_RERUN`

## QA
PASS: State verification, Auto-Correction, gültige Instruction Authorization, manipulierte Authorization BLOCKED, Input-Hash, Maintenance-Isolation, No-Restart-on-Uncertainty, Reuse/Resume-Regeln.
