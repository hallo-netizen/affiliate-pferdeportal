# P32 – KLARE ROLLEN OHNE DOPPELAUTORITÄT

Datum: 2026-09-08
Status: GO

## Ergebnis

Die Zielarchitektur braucht keine neuen Fachkomponenten.

### Zentralmaschine
Darf nur:
- feste Reihenfolge
- einen kanonischen Jobzustand
- PASS/BLOCKED-Fortschaltung

Darf nicht:
- Inhalt entscheiden
- Design entscheiden
- Reparaturweg frei wählen

### Gebundener Codex-Worker
Darf nur:
- den gebundenen Mikroschritt ausführen
- gebundene Recherche/fact_pack und Artefakte erzeugen

Darf nicht:
- nächsten Schritt wählen
- Regeln wählen
- eigenen PASS attestieren
- publishen

### PSTE
Nur:
- Research-/Planungskontext
- Planning Readiness
- Pre-Title Keyword Ownership

Kein:
- Artikelinhalt
- Design
- Workflownavigation

### PSERC
Nur:
- Editorial-Plan-Metadaten
- Workflow-Supervisionsmetadaten
- feste Bridge zu PPM

Explizit verboten:
- Content-/Format-Autorität
- Design-Autorität
- Publish

### PPM Normal Draft
Nur der exakt gebundene Zielmodus:
- Artikelgenerierung
- Content Validation
- Plan Runtime Gate
- prepare-Payload
- Draft Write
- Readback
- Rendered-DOM-Prüfung

Verboten:
- Publish
- freier externer Reviewer im Zielmodus
- freie Workflownavigation

## KISS

Eine Steuerung, vorhandene Fachbausteine.

Keine zweite Fachlogik.
Keine Doppelprüfung durch neu erfundene Worker.
Keine freie Kommunikation zwischen Komponenten.

Komplette Laborregression P0–P32: PASS.
