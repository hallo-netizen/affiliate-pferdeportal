# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-029
Historie bleibt erhalten; frühere lokale Fixbehauptungen gelten nicht als Live-PASS.

## HRD-030 – Logo verzerrt/gequetscht
STATUS: LOCAL CLOSED 1.50.618 / LIVE OFFEN

Ursache:
Breite und zu kleine `max-height` wurden gleichzeitig erzwungen.

Fix:
natürliches Seitenverhältnis, `height:auto`, keine begrenzende Max-Höhe; linksbündig.

## HRD-031 – Navigation zu hoch / Flyout versetzt
STATUS: LOCAL CLOSED 1.50.618 / LIVE OFFEN

Fix:
eigene untere Navigationszeile; Flyout wieder relativ zum jeweiligen Weltpunkt statt statisch über der Gesamtzeile.

## HRD-032 – Hero und Aufklapptext doppeln sich
STATUS: LOCAL CLOSED 1.50.618 / LIVE OFFEN

Fix:
Hero erhält Lead; Fold ausschließlich den verbleibenden Text.

## HRD-033 – Unterkategorie-Bilder viel zu groß
STATUS: LOCAL CLOSED 1.50.618 / LIVE OFFEN

Fix:
einheitliche kompakte Querformat-Thumbnails 132×70 statt großflächiger Kartenbilder.

## HRD-034 – Affiliate trotz Integration optisch unten angeklebt
STATUS: LOCAL CLOSED 1.50.618 / LIVE OFFEN

Fix:
Banner und Produkte sind jetzt direkte Elemente des Next-Level-Kartenrasters; Banner nach erster Reihe, Produkte füllen ungerade letzte Reihen.

## HRD-035 – Verkaufbarer Werbeplatz visuell unverändert/schwach
STATUS: LOCAL CLOSED 1.50.618 / LIVE OFFEN

Fix:
neues Einzelfoto, dunkler Overlayverlauf, farbiger Brushstroke, heller CTA.

## Aktuell erster Blocker
**Live-Abnahme 1.50.618.**
