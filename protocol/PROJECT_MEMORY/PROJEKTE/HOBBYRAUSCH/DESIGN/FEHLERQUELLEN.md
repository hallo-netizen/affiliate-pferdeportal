# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-035
Historie bleibt bestehen; lokale Fixstände gelten erst nach Live-Readback als endgültig geschlossen.

## HRD-036 – Navigation weiterhin zu hoch
STATUS: LOCAL CLOSED 1.50.619 / LIVE OFFEN

Fix:
größere vertikale Trennung von Logo/Search/Navigation; eigene tiefere Nav-Zeile.

## HRD-037 – Flyout nach 1.50.618 faktisch weg
STATUS: LOCAL CLOSED 1.50.619 / LIVE OFFEN

Ursache:
eine ältere Mid-Breakpoint-Regel unterdrückte Hover-Flyouts weiterhin mit `!important`.

Fix:
späteste 1.50.619-Regel aktiviert Hover/Fokus/Klick explizit wieder und verankert Flyouts am jeweiligen Weltpunkt.

## HRD-038 – Kategorie-Vorschaubilder zu klein
STATUS: LOCAL CLOSED 1.50.619 / LIVE OFFEN

Fix:
Bild füllt die komplette vorgesehene Querformatfläche; kein Innenrand/Inset.

## HRD-039 – Untertitel generisch und wiederholend
STATUS: LOCAL CLOSED 1.50.619 / LIVE OFFEN

Fix:
Gestalten erhält 7 kurze individuelle Kurzzeilen. Ohne echte Kurzinfo kein generischer Füllsatz.

## Aktuell erster Blocker
**Live-Abnahme 1.50.619.**
