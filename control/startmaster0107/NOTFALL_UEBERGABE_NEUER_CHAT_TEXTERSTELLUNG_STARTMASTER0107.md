# STARTMASTER0107 — WIEDEREINSTIEG NÄCHSTER CHAT

Diese Datei ist **nur Wegweiser**. Sie ist keine CURRENT-, Fehler-, Ziel- oder NEXT-ACTION-Wahrheit.

## Pflichtweg

1. `control/CURRENT_STARTMASTER.json` lesen.
2. Dessen `root_ref` folgen:
   `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`.
3. Dort ausschließlich `navigation_authority` folgen:
   `control/startmaster0107/CURRENT_STATE.json`.
4. Den dort gebundenen Frischecheck durchführen:
   - den dort genannten aktiven Arbeitsbranch/Head prüfen;
   - die dort genannten letzten relevanten Test-/Workflowbelege prüfen;
   - nur feststellen, ob seit dem gebundenen Stand ein relevantes Delta vorliegt.
5. Kein relevantes Delta:
   **keine Vollrekonstruktion**; direkt die eine `next_action` aus CURRENT_STATE ausführen.
6. Relevantes Delta:
   ausschließlich dieses Delta prüfen und CURRENT_STATE zuerst nachziehen.
7. Nicht belastbar bestimmbar:
   **BLOCKED – NICHT RATEN**.

## Rollen

- `PFERDE_ATELIER_START_HERE.json`: Navigation + technisch notwendige Integritätsbindung; keine eigenständige Fachentscheidung.
- `CURRENT_STATE.json`: einzige dynamische Current-/Status-/Blocker-/NEXT-ACTION-Autorität.
- Protokolle/Evidence: Nachweis und Historie.
- Branches/Worker/Workflow-Runs: Ausführung/Evidence, niemals CURRENT.
- Übergabe: nur dieser Wegweiser.

## Nicht als Current verwenden

- diese Übergabe;
- Chat-Erinnerung;
- Protokolle;
- Hobbyraum;
- Archiv;
- alte Konzeptbranches;
- Testartefakte;
- Worker-/Workflow-Ausgaben;
- historische Runtime-Inbox-/Recovery-Zustände.

## Harte Produktionsregeln

Nach Auflösung der Current-Autorität gilt ausschließlich deren gebundener Arbeitsweg.
Keine freie Stufenwahl, kein alternativer Abschlussweg, keine historischen Artikel als Produktionsquelle, keine Qualitätsabschwächung und kein Publish.

Die konkrete aktuelle NEXT ACTION steht **nur** in:
`control/startmaster0107/CURRENT_STATE.json`.
