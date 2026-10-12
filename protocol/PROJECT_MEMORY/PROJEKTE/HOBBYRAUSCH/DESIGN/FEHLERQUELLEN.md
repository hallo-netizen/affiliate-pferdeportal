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

## Arbeitsfehlerprotokoll 2026-10-12
Die vollständige interne Fehler-/Lernakte dieses Designlaufs liegt dauerhaft hier:

`protocol/PROJECT_MEMORY/PROJEKTE/HOBBYRAUSCH/DESIGN/ARBEITSFEHLERPROTOKOLL_20261012.md`

Dort dokumentiert sind insbesondere:
- falscher Repo-Kontext beim ersten Check;
- 1.50.629 als Bildfix ausgegeben, obwohl die sichtbare Wirkung nicht ausreichend bewiesen war;
- Regression einer bereits akzeptierten Navigation;
- 1.50.630 mit fälschlich reaktiviertem v150623-Bildsatz und wiederkehrenden Szenen/Doppelbildern;
- Verwechslung von SHA-Eindeutigkeit und visueller Eindeutigkeit;
- zu frühe ZIP-Freigabe vor vollständiger Simulation;
- nicht mittiger Claim durch `scaleX(1.06)`;
- fehlender geometrischer Nachweis der gemeinsamen Logo-/Claim-/Navigationslinie;
- unzureichendes Einfrieren bereits live akzeptierter Bereiche;
- zeitweise zu starke Dokumentationsaussagen gegenüber dem tatsächlich bewiesenen Stand.

Diese Akte ist Historie/Fehlerprävention. Aktueller Fehlerstatus bleibt ausschließlich in dieser `FEHLERQUELLEN.md`, aktueller Gesamtstatus/NEXT ACTION ausschließlich in `CURRENT_STATE.md`.

