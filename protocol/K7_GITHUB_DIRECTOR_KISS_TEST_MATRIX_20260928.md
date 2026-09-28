# K7 GitHub Director KISS — Entwicklung/Testmatrix — 2026-09-28

Status: Entwicklungsnachweis, keine zweite CURRENT-/NEXT-ACTION-Autorität.

## Unveränderbar
- bestehender Fachworkflow;
- bestehende Worker-Aufgaben;
- Research/Faktenbindung;
- LanguageTool 6.8;
- PPM 6.7.9;
- PSERC;
- ENDSTEMPEL;
- Publish=false;
- bestehende Recovery-/Checkpoint-Logik.

## Einzige Ergänzung
Ein domain-blinder äußerer Regisseur liest ausschließlich den gültigen gespeicherten Checkpoint, erzeugt exakt ein hashgebundenes Ticket für die bereits festgelegte allowed_action, nimmt ausschließlich das dazu passende Worker-Ergebnis an, persistiert den daraus durch die bestehenden Guards erzeugten neuen Checkpoint und leitet daraus die nächste allowed_action ab. Nur STOP ist terminal.

## Positivmatrix
- Start/Resume aus exakt gespeichertem Checkpoint;
- identisches Resume vor Worker-Rückgabe;
- WRITE_DRAFT -> LT68 -> PPM679;
- PPM679 REPAIR_REQUIRED -> derselbe Artikel -> Repair -> LT68 -> PPM679;
- nächster Artikel erst nach PASS;
- PSERC -> ENDSTEMPEL -> STOP;
- Neustart mitten im Artikel;
- Neustart in REPAIR_REQUIRED;
- Neustart nach gespeichertem Schritt;
- Reasoning-Default medium aus unverändertem Zielvertrag.

## Negativmatrix
Muss fail-closed blockieren:
- manipuliertes Ticket;
- andere allowed_action;
- falscher Checkpoint;
- stale/replayed alter Checkpoint;
- falscher Worker-Rückgabebeleg;
- Worker versucht next_action vorzugeben;
- Worker verlangt Workflowänderung;
- publish_allowed=true;
- Artefakt außerhalb des gebundenen Workroots;
- falscher Artefakt-Hash;
- unbekannte Aktion/Checker;
- fehlender gespeicherter Checkpoint;
- veränderter Zielvertrag;
- Veränderung einer bestehenden Kern-/Qualitäts-/Recovery-Datei.

## Testprinzip
Die bestehenden Kern-Dateien werden bytegenau über Git-Blob-Fingerprints festgehalten. Die Testmatrix enthält sowohl den zulässigen kompletten Weg als auch absichtliche Regelverletzungen. Ein Negativfall, der nicht blockiert, ist Gesamt-FAIL.

Interne Entwicklungssimulation des neuen Director-Adapters: PASS.

## GitHub-Realtest
- Run: `36420006811`
- Ergebnis: **PASS**
- Director-Matrix: **11/11 PASS**
- Full16-Simulation: **16 Artikel / 5 Repairs / Unterbrechung vor und nach jedem akzeptierten Schritt / Replay alter Tickets BLOCKED / ENDSTEMPEL -> STOP**
- Bestehende Deterministic-Gate-Regression: PASS
- Bestehende Production-Continuity-Regression: PASS
- Testworkflow war ausschließlich Wegwerf-Testhülle in PR #470 und wird nicht in Produktion übernommen.
