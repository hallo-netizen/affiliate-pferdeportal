# Pferde Atelier – Konzept 9

**Rolle dieser Datei:** Navigation, keine CURRENT-Wahrheit.

## Einstieg

1. Bürotür: `K9:pferdeatelier` im Repo `hallo-netizen/text-start`.
2. Einzige Current-Autorität: `CURRENT_STATE.json` auf Branch `konzept9/greenfield-20260929`.
3. Wenn Current `operational_mode = EXECUTE_RUNTIME_CHAT_ENTRY_ONLY` meldet und `runtime/CHAT_ENTRY.json` existiert, ist der Chat ab diesem Moment ausschließlich Worker:
   - `CHAT_ENTRY` lesen;
   - exakt den offenen Job ausführen;
   - vor der Ausführung keinen Statusbericht, keine Diagnose, keine Fixdiskussion und keine Workflow-Erklärung;
   - keine Vorgängerstation neu bewerten;
   - nicht routen.
4. Nur ohne gültigen offenen Chat-Job darf Current eine Supervisor-NEXT-ACTION vorgeben.

## Invariantes K9-Prinzip

Recherche, Schreiben, Prüfung und Reparatur erzeugen vollständige, dauerhaft gespeicherte Produkte. Routing entscheidet die feste K9-Zustandslogik, nicht der Chat. Qualitätsgates bleiben LT 6.8, PPM 6.7.9, PSERC, ENDSTEMPEL und WordPress-Endformatprüfung. `publish_allowed=false`.
