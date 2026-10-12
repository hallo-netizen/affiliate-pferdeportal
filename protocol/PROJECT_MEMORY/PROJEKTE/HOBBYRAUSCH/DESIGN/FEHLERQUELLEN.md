# HOBBYRAUSCH – DESIGN – FEHLERQUELLEN

ROLLE: Fehlerhistorie. Aktueller Status/NEXT ACTION ausschließlich aus `CURRENT_STATE.md`.

## HRD-001 bis HRD-048
Historie bleibt bestehen. Frühere lokale Fixbehauptungen sind kein Ersatz für Live-Readback.

## HRD-049 – 65 eindeutige Dateien, live trotzdem gleiche Bilder
STATUS: LOCAL CLOSED 1.50.625 / LIVE OFFEN

ROOT CAUSE:
`next_level_card_photo()` priorisierte WordPress Featured Images vor den kontrollierten lokalen Hubmotiven. Mehrfach gepflegte alte Featured Images konnten dadurch auf mehreren Karten gleich erscheinen.

FIX:
Für die 65 direkten ersten Welt-Unterkategorien hat das kontrollierte v150625-Asset Vorrang. Featured Image ist nur noch Fallback, wenn kein kontrolliertes Motiv existiert.

TEST:
Simuliertes identisches Featured Image wird nicht ausgegeben; lokales Technikmotiv gewinnt.

## HRD-050 – Kategorie-Motive visuell zu voll / zu ähnlich
STATUS: LOCAL CLOSED 1.50.625 / LIVE OFFEN

FIX:
65 Motive auf klarere, engere Einzelmotive neu aufgebaut. 600×320. 65 eindeutige SHA-256 und zusätzlicher Perceptual-dHash-Test; Mindestabstand 96.

## HRD-051 – Sammeln nicht exakt auf einer Linie
STATUS: LOCAL CLOSED 1.50.625 / LIVE OFFEN

ROOT CAUSE:
Pfeilbutton und frühere Grid-/Flex-Regeln konnten die optische Item-Baseline beeinflussen.

FIX:
Ab 761 px eine einzige Flex-Zeile. Alle Labels feste 20-px-Zeilenbox; Pfeilbutton absolut und außerhalb des Textflusses.

TEST:
1600/1200/1024/900/800/761 px: alle acht Labels exakt gleiche Y-/Bottom-Koordinate, horizontaler Overflow 0.

## Aktuell erster Blocker

**Live-Abnahme 1.50.625: Technik/Pflanzen-Bilder und Sammeln-Baseline.**
