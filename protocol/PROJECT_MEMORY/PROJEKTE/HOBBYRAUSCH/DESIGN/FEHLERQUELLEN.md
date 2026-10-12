# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-052
Historie bleibt bestehen.

## HRD-053 – Hauptnavigation: Sammeln fällt weiterhin aus der Linie
STATUS: LOCAL CLOSED 1.50.627 / LIVE OFFEN

FIX:
Ab 761 px feste 8-spaltige Grid-Navigation mit exakt einer 26-px-Zeile.
Linklabel und Pfeil besitzen getrennte Gridspalten; der Pfeil kann die Label-Baseline nicht mehr verschieben.

TEST:
1600/1200/1024/900/800/761 px: alle 8 Labels exakt gleiche Y-/Bottom-Koordinate, Overflow 0.

## HRD-054 – Hubmotive zu kleinteilig / zu voll
STATUS: LOCAL CLOSED 1.50.627 / LIVE OFFEN

FIX:
Alle 65 kontrollierten Motive enger gezoomt und neu als 600×320 ausgegeben.
Ziel: Hauptmotiv größer, weniger Umgebung, ruhiger lesbar.

TEST:
65/65 eindeutige SHA-256; perceptual dHash Mindestabstand 92.

## HRD-055 – Hero-Texte schablonenhaft und unnatürlich
STATUS: LOCAL CLOSED 1.50.627 / LIVE OFFEN

FIX:
Für alle 8 Hauptwelten eigene, direkte, natürliche Kurztexte statt Auto-Schablone.

## HRD-056 – `Mehr über … erfahren` auf Hauptwelten unerwünscht
STATUS: LOCAL CLOSED 1.50.627 / LIVE OFFEN

FIX:
Accordion vollständig aus dem Hub1-Ausgabepfad und aus dem aktiven Code entfernt.
Dafür pro Hauptwelt eigener Langtext am Seitenende mit Zwischenüberschriften und validierten semantischen Links.

## Aktuell erster Blocker
**Live-Abnahme 1.50.627: Technik, Pflanzen, Sammeln.**
