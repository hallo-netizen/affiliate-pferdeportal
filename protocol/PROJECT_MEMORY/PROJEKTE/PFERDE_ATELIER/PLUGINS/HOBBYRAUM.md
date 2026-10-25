# PFERDE-ATELIER – PLUGINS – HOBBYRAUM

<!-- DERIVED_EXECUTION_SURFACE_V1 -->

> **NICHT CURRENT-AUTORITATIV.** Diese Datei ist nur die abgeleitete Ausführungsfläche für eine bereits von der zuständigen Current-Autorität freigegebene Arbeit.  
> Aktuellen Stand, Blocker und NEXT ACTION ausschließlich über `protocol/PROJECT_MEMORY/AUTORITAETSPLAN.json` aus der dort benannten Current-Autorität lesen.  
> Widerspruch oder stale Bindung = **BLOCKED**, niemals Hobbyraum gegen Current durchsetzen.



## Technischer Einzel-Arbeitsstand

Einzige aktuelle Kandidatenbindung: `PLUGINS/CURRENT_STATE.md`, Abschnitt `PFERDEATELIER_PLUGIN_WORKBENCH_LOCK`. Keine weiteren Arbeitsstände als aktuelle Version verwenden.

Die Datei `tests/guard_active_workbench.py` prüft Dateiname, SHA-256, Quell-ZIPs, Quelländerungen und die tatsächlich ausführbaren Original-PHP-Gegenläufe. Alte, manipulierte oder nicht gebundene Dateien werden abgewiesen. Release bleibt ohne echten Original-Endlauf bis WordPress-Draft gesperrt.

Aufruf aus dem Repository-Hauptverzeichnis: `python3 protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/tests/guard_active_workbench.py --current protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/PLUGINS/CURRENT_STATE.md --artifact <aktuelle-qa-zip>`.

Bei jeder Änderung zuerst mit der einen im Current benannten Arbeitsfassung weiterarbeiten, denselben Gesamtprüflauf wiederholen, diese eine QA-Datei aktualisieren und ihre neue SHA ausschließlich im Current nachführen. Der Originalcode ist Vergleichsmaterial, kein zweiter aktiver Arbeitsstand. Keine alten Fehler erneut als neu entdecken. Keine Einzelkeyword-Reparatur.

## ABGELEITETER AUSFÜHRUNGSWEG

Nur den von `PLUGINS/CURRENT_STATE.md` freigegebenen Auftrag an dessen technischer Fachquelle bearbeiten. Vor Beginn die tatsächliche aktive Arbeitsbindung prüfen; fehlt sie oder widerspricht sie Current, **BLOCKED** statt aus früheren Hobbyraum-Zwischenständen zu raten.

Nach Abschluss Fachnachweise im bestehenden `UPDATEPROTOKOLL.md` dokumentieren und nur nach Freigabe den isolierten Ausgabestand synchronisieren. Diese Ausführungsfläche führt **keinen** eigenen dynamischen Status, Blocker oder NEXT ACTION.

## NICHT ANFASSEN

- keine zweite Plugin-ID für ein bereits registriertes Plugin;
- keine lokale Kandidatenversion als CURRENT ohne Fach-/Testbindung;
- keine Fach-/LIVE-Wahrheit in dieses Inventarbüro kopieren;
- PPA-013 nicht reaktivieren; kanonisches Pferde-Design ist PPA-002.

## RÜCKGABEWEG

Neue Entwicklung immer aus der zuständigen Fachquelle starten und erst nach PASS hier synchronisieren.
