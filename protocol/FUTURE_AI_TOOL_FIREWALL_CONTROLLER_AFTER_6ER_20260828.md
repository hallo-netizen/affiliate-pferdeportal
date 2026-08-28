# FUTURE AI TOOL FIREWALL CONTROLLER – NACH 6ER-ARTIKELTEST

Stand: 28.08.2026

## Zweck
Die vorhandene MASTER-/CURRENT_STATE-/NEXT_ALLOWED_STEP-Logik bleibt unverändert. Ergänzt werden soll ausschließlich eine äußere technische Zwangsschicht, damit das Modell keine eigenen Workflow-Schritte, Wiederholungsprüfungen oder Nebenpfade starten kann.

## Harte Zielregel
- GitHub/MASTER bleibt alleinige Workflow-Autorität.
- Controller liest ausschließlich aktuellen `CURRENT_STATE` und `NEXT_ALLOWED_STEP`.
- Modell erhält nur den konkret freigegebenen Schritt sowie die dafür nötigen Dateien/Funktionen.
- Nicht erlaubte Tools/Aktionen werden dem Modell technisch nicht angeboten.
- Ergebnis außerhalb des erlaubten Schemas/Schritts wird verworfen; Workflowzustand bleibt unverändert.
- Nur ein erfolgreich validierter vorhandener Gate-/Runner-Schritt darf den Zustand fortschreiben.
- Neuer Chat/Neustart beginnt immer aus dem aktuellen GitHub-Zustand, nicht aus Erinnerung oder Chat-Historie.

## Schutz des bestehenden Systems
- Keine Änderung an Fachworkflow, Textqualität, Recherche, LanguageTool, PSTE, PSERC, PPM, Design, Dubletten-/Kannibalisierungsregeln oder Publish-Logik.
- Keine WordPress-Pluginänderung für diese Absicherung.
- Kein neuer Qualitätsgate; nur technische Durchsetzung der bereits vorhandenen Navigation.
- Umsetzung ausdrücklich erst NACH Abschluss des laufenden 6er-Artikeltests.

## Zielarchitektur
`GitHub/MASTER -> externer zustandsbasierter API-Controller mit Tool-Firewall -> Modell -> vorhandene Gates -> CURRENT_STATE`

Ziel: Dem Modell die Workflow-Navigation vollständig entziehen; es darf nur den bereits festgelegten Schritt ausführen.
