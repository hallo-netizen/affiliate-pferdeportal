# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-051
Historie bleibt bestehen.

## HRD-052 – 1.50.625 verursacht WordPress Critical Error
STATUS: ROOT CAUSE GEFUNDEN / LOCAL CLOSED 1.50.626 / LIVE OFFEN

ROOT CAUSE:
Die neu benannten v150625 Front-/Contenttemplates enthielten noch harte Aufrufe auf die nicht mehr vorhandene Klasse:
`Hobby_Depot_Profile_V150624`.

Dadurch fataler Klassenfehler beim Templateaufruf.

FIX 1.50.626:
Main, aktive Klasse, Router und beide Templates vollständig auf
`Hobby_Depot_Profile_V150626`
gebunden.

NEGATIVCHECK:
Keine V150624/V150625-Klassenreferenz mehr im aktiven PHP.

## Aktuell erster Blocker

**Live prüfen, ob 1.50.626 den Critical Error vollständig beseitigt.**
