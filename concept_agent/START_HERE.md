# Pferde Atelier — Concept Agent

Diese Datei ist ausschließlich die **Bürotür**. Sie enthält keine eigene CURRENT-, Fehler- oder NEXT-ACTION-Wahrheit.

## Einzige Current-Autorität

`control/startmaster0107/CURRENT_STATE.json` auf dem geschützten `main`.

Pflichtweg:
1. `concept_agent/CONTROL_ENTRY_POINTER.json` nur als technische Bindungs-/Kompatibilitätsdatei lesen.
2. Dessen `current_authority_ref` folgen.
3. Genau die dort genannte Current-Autorität lesen.
4. Frischecheck nur auf Delta durchführen.
5. Ausschließlich die eine dort gespeicherte `next_action` ausführen.

**Wichtig:** Der historische Workflow-Bezeichner `PFERDE_ATELIER_KONZEPT_5_CONCEPT_AGENT` in technischen Bindungspointern ist ein bestehender Maschinenvertragsname und keine Aussage darüber, welches Optimierungskonzept aktuell bearbeitet wird. Aktueller Konzept-/Branch-/Run-/Blockerstatus kommt nur aus CURRENT_STATE.

## Produktionsanschluss

Bei einem realen Produktionslauf bestimmt ausschließlich die frisch gelesene Current-Autorität den erlaubten Einstieg. Bereits gültig gebundene Research-/Checkpoint-/Artikelzustände werden wiederverwendet; ein erneuter Start darf keinen parallelen zweiten Wahrheitsweg eröffnen.

**HARD RULE – text-start ist kein Antwortpunkt:** Sobald ein realer `text-start` ein gültiges `CONCEPT_AGENT_INTAKE_READY` mit `continuation_required=true` an den bereits gebundenen `BOUND_CHAT_WORKER` übergibt, darf dieser weder antworten noch erneut prüfen/suchen. Er muss ohne Nutzer-Zwischenmeldung die exakt gebundene `process_trigger`-Aktion unmittelbar ausführen, deren Rückgabe in den bestehenden Guard zurückführen und jede weitere nicht-terminale gebundene Aktion unmittelbar fortsetzen. Erst der ausdrücklich gebundene terminale `STOP` beendet den Lauf.

Nicht-terminale Übergaben sind kein Chat-Stop. Schreiben, LanguageTool 6.8, PPM 6.7.9, Same-Article-Repair, PSERC und ENDSTEMPEL laufen nur in der von Current gebundenen Reihenfolge. Ein echter Fehler blockiert fail-closed am ersten gebrochenen Punkt.

**HARD RULE – Unterbrechung/Wiedereinstieg:** Nach jedem akzeptierten Produktionsresultat muss der vollständige aktuelle Produktionsstand dauerhaft gespeichert sein. Bei Unterbrechung zwischen Schritten, mitten in einem Artikel, mitten in einer Reparatur, Shutdown oder neuem Chat gilt ausschließlich der letzte gültige Checkpoint mit Artikelbytes, Prüf-/Reparaturstand und NEXT ACTION. Kein Zusammensuchen aus Chat-Historie, keine Rekonstruktion und kein alternativer Wiedereinstieg.

## Nicht als Current verwenden

- `CONTROL_ENTRY_POINTER.json` selbst;
- alte Runtime-Inbox-/Recovery-Dateien;
- historische Produktionsbranches;
- Protokolle;
- Übergaben;
- Hobbyräume;
- Workflow-/Worker-Evidence;
- Chat-Erinnerung.

## Unveränderliche Qualitätsgrenzen

LanguageTool 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL und `publish_allowed=false` dürfen nicht durch Navigation, Optimierung oder Wiedereinstieg abgeschwächt werden.

Die konkrete aktuelle Aktion steht ausschließlich in:
`control/startmaster0107/CURRENT_STATE.json`.

## Aktuelle Ausführungsgrenze

Für Produktion gilt ausschließlich der in der Current-Autorität gebundene Concept-Agent-Weg. Historische, archivierte oder frühere externe Ausführungswege besitzen **keine** aktuelle Start-, Worker-, Routing-, Diagnose- oder Fallback-Autorität und dürfen nicht als Lösung reaktiviert oder vorgeschlagen werden.
