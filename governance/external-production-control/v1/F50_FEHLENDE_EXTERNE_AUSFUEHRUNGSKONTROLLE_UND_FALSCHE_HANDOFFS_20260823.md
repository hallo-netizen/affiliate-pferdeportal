# F-50 – fehlende externe Ausführungskontrolle / falsche Handoffs

## Root Cause
Der bestehende Fachworkflow war nicht die Ursache der heutigen Fehlerserie. Die Chat-Ausführung hatte außerhalb des Fachworkflows zu viel Freiheit: Zustände konnten aus Historie rekonstruiert, Paketdateien falsch gebaut/benannt, lokale Tests als FINAL überhöht und falsche Dateien an den Nutzer übergeben werden.

## Korrektur
Externe, governance-only Control Plane mit fail-closed State-/Action-/Artifact-/Handoff-/Delivery-Gates. Sie verändert den Fachworkflow nicht und kann keine Fachentscheidung treffen.

## Dauerhafte Sperren
- kein Memory-Fallback
- keine freie Workflow-Navigation
- keine falsche nächste Datei
- keine doppelten aktiven Rollen/Planplätze/Canonical IDs
- kein falsches lokales FINAL
- kein Future-Step-False-Blocker
- kein Chatende ohne verifiziertes Delivery-Manifest
