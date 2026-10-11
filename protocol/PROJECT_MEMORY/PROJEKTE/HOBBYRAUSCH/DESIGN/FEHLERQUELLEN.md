# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Autoritative Fehlerhistorie dieses Design-Scopes.  
Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 – Startseite im WordPress-Blogloop
STATUS: CLOSED

## HRD-002 – Startseite wich vom freigegebenen Entwurf ab
STATUS: CLOSED FÜR CODEPFAD / LIVE-REGRESSIONSSCHUTZ AKTIV

## HRD-003 – Hero-CTAs/Bildschriftzug bei Zwischenbreiten abgeschnitten
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

Korrektur:
responsiver Hero, Desktop-/Mobile-Safe-Crop, Bildschriftzug bleibt.

## HRD-004 – Mega-Menü verschwindet beim Mausweg
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

Korrektur:
0-px-Hoverweg / Hoverbrücke.

## HRD-005 – Weltbilder unscharf / fachlich unpassend
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

Korrektur:
8 kontrollierte native Weltassets, je 1400×620; fachlich abgeglichen; Tiere rahmenlos und ohne Hund-/Haustierclaim.

## HRD-006 – Startseite unvollständig / TEST-Fallback
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

Korrektur:
vollständige reale Editorial-/Magazinstruktur, kein TEST-Fallback.

## HRD-007 – Affiliate-Leerzustand / Direktwerbung
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

Korrektur:
Affiliate-Banner/Produkte öffentlich leer unsichtbar, eingeloggt leer sichtbar; Direktwerbung maximal einmal und öffentlich auch unverkauft sichtbar.

## HRD-008 – Header/Body zu einheitlich / Logo-Readback
STATUS: LOCAL CLOSED / LIVE REGRESSIONSSCHUTZ

Korrektur:
weißer Body, warm-off-white Header, unverändertes Logo mit cache-sicherem Pfad.

## HRD-009 – 1.50.611 sichtbar wirkungslos
STATUS: CLOSED DURCH 1.50.612 / LIVE REGRESSIONSSCHUTZ

Ursache:
wiederverwendete Renderer-/Assetpfade plus Featured-Image-Priorität.

Korrektur:
neue Renderer-/Assetpfade, kontrollierte Weltbilder bindend.

## HRD-010 – Navigation weiterhin zu hoch

STATUS: LOCAL CLOSED IN 1.50.613 / LIVE OFFEN

Befund:
Live 1.50.612: Navigation noch nicht bündig mit der untersten Logo-/Claim-Textlinie.

Korrektur:
Desktopnavigation 1.50.613 real um 14 px nach unten verschoben; Tablet/Mobile nicht künstlich verschoben.

## HRD-011 – Hobbyfinder-Karte anderer Schatten/Farbton

STATUS: LOCAL CLOSED IN 1.50.613 / LIVE OFFEN

Befund:
Hobbyfinder, Magazin und Wissen wirkten als zusammengehörige Dreiergruppe farblich uneinheitlich.

Korrektur:
alle drei Kartenflächen verwenden einheitlich `#f5f1e9`, keine unterschiedlichen Verlaufs-/Schattierungsfarben.

## HRD-012 – Verkaufbarer Werbeplatz auf Startseite faktisch nicht sichtbar

STATUS: LOCAL CLOSED IN 1.50.613 / LIVE OFFEN

Befund:
Der Direktwerbeplatz war im bisherigen Startseitenfluss nicht als klar sichtbares Verkaufsangebot wahrnehmbar.

Korrektur:
- öffentlich unverkauft immer sichtbar;
- Text: **„Hier könnte Ihre Werbung stehen.“**;
- maximal einmal;
- im Startseitenfluss unmittelbar nach Hobbyfinder/Magazin/Wissen.

## HRD-013 – Noch keine verbindliche Hub-/Breadcrumb-Darstellung

STATUS: LOCAL CLOSED IN 1.50.613 / LIVE OFFEN

Korrektur:
- eigenes Contenttemplate für CORE-Seiten/Kategorien;
- Breadcrumb überall außer Start;
- erste Welt-Hubs mit exakt dem Startseiten-Weltbild;
- nächste Ebene, Banner, Beitragsvorschau, Produkte und genau ein Direktwerbeplatz.

## Aktuell erster Fehler-/Abnahmeblocker

**Live-Abnahme 1.50.613 auf Startseite + einer ersten Welt-Hubseite.**
