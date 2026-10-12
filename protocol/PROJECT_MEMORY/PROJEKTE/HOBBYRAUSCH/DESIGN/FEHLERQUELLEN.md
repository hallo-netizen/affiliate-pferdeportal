# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-056
Historie bleibt bestehen.

## HRD-057 – Navigation 1.50.627 gleichmäßig, aber insgesamt zu tief
STATUS: **GRUNDLINIE LIVE BESTÄTIGT / HEADERPOSITION IN HRD-062**

## HRD-058 – Hub-Kartenbilder zu klein
STATUS: **LAYOUT LIVE CLOSED 1.50.628**

## HRD-059 – Zu viele interne Links in Seitenendtexten
STATUS: **LIVE CLOSED 1.50.628**

## HRD-060 – Kategorie-/Link-Bilder zu eng / Lupeneindruck
STATUS: **1.50.629 LIVE FAIL / 1.50.631 LOCAL CLOSED / LIVE OFFEN**

Befund:
- 1.50.629 brachte live keine ausreichende sichtbare Änderung.
- gewünschte Richtung: Motiv weiter heraus, klarer Gesamtgegenstand, weniger Detaildruck.

Fix 1.50.631:
- 65 eindeutige v150629-Quellmotive;
- daraus 65 neue v150631-Dateien mit echtem 80%-Zoom-out und ruhiger Bildumfelderweiterung;
- alle 600×320 / SHA-eindeutig.

## HRD-061 – 1.50.630 brachte Doppelbilder zurück
STATUS: **ROOT CAUSE CLOSED / 1.50.630 VERWORFEN**

Root Cause:
- 1.50.630 bevorzugte den alten v150623-Satz;
- dieser Satz enthält mehrfach dieselben Szenenfamilien für unterschiedliche Kategorien.

Fix 1.50.631:
- v150623 aus aktivem Hub1-Bildpfad entfernt;
- Hub1 kein Fallback auf wiederholte WordPress Featured Images.

## HRD-062 – Claim nicht mittig / Logo-Unterkante nicht auf Navigationslinie
STATUS: **LOCAL CLOSED 1.50.631 / LIVE OFFEN**

Root Cause:
- Claim wurde per `scaleX(1.06)` nach rechts verbreitert;
- Geometrieabweichung vor Fix: Desktop 7 px, 761–1000 px 38 px.

Fix:
- Claim-Skalierung entfernt;
- Logo nach unten versetzt;
- lokale Simulation 1600/1440/1200/1024/900/800/761: Claim-Unterkante = Navigations-Unterkante, Delta 0 px.

## Aktuell erster Blocker
**Live-Abnahme 1.50.631: Vorschaubilder + Logo/Claim/Navigationslinie.**
