# STARTMASTER0107 — WIEDEREINSTIEG NÄCHSTER CHAT

Diese Datei ist **nur Wegweiser**. Sie ist keine CURRENT-, Fehler- oder NEXT-ACTION-Wahrheit.

## Exakter Einstieg

1. `control/CURRENT_STARTMASTER.json` lesen.
2. Dessen `root_ref` folgen: `control/startmaster0107/PFERDE_ATELIER_START_HERE.json`.
3. Dort ausschließlich `navigation_authority` folgen: `control/startmaster0107/CURRENT_STATE.json`.
4. Frischecheck durchführen:
   - aktuellen `main` prüfen;
   - aktuellen Dispatcher PR #107 / `codex-chat-launcher` prüfen;
   - gegen die in CURRENT_STATE gebundene aktuelle Evidence vergleichen.
5. Bindung unverändert: **keine Vollrekonstruktion**, keine historischen Protokolle zusammensetzen; direkt die **eine `next_action` aus CURRENT_STATE** ausführen.
6. Relevante Änderung: nur das Delta seit CURRENT_STATE prüfen und CURRENT_STATE zuerst nachziehen.

## Nicht als Einstieg verwenden

- keinen alten `project_single_door_entry_v2.py status`-Chatbefehl aus dieser Übergabe ableiten;
- keinen `cloud_entry.py`-Start erraten;
- keine manuelle Point-0-/SOURCE_REQUESTS-/Workspace-Konstruktion;
- keine Übergabe, kein Protokoll, kein Hobbyraum und keine Chat-Erinnerung als zweite Standwahrheit verwenden.

Der produktive Befehl ergibt sich ausschließlich aus der frisch geprüften CURRENT_STATE plus der aktuell bindenden Repository-Instruktion.
