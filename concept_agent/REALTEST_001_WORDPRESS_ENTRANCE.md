# REALTEST 001 — WORDPRESS INPUT ENTRANCE

Status: **EXPECTED BLOCK / PASS AS NEGATIVE TEST**

## Reale Quelle
READ-ONLY-Kopie des ersten Artikels aus dem vorhandenen WordPress-Live-Snapshot.

- Titel: Das Wichtigste über Hindernisstangen für Pferde
- Keyword: Hindernisstangen für Pferde
- Typ: Beratung
- Kategorie: hindernisstangen-beratung
- Plan-Slot: 9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56
- publish_allowed: false

## Befund
Der reale WordPress-Snapshot enthält für diesen Auftrag **keine konkreten drei internen Linkbindungen**.

Die bestehende Textmaschinen-/PPM-Anforderung ist aus READ-ONLY-Nachweisen bekannt:
- genau drei interne Links = PASS-Bedingung;
- fehlende/ersetzte gebundene interne Links müssen BLOCK auslösen.

Concept Agent darf diese Links nicht erfinden.

## Erwartetes Ergebnis
Eingang muss stoppen mit:

`EXACT_THREE_INTERNAL_LINKS_REQUIRED`

Kein Research Agent.
Kein Facts Agent.
Kein Writer.
Kein Repair.
Keine finale Datei.

## Bewertung
Das ist kein Systemfehler, sondern korrektes Fail-Closed-Verhalten.

## Nächste Teststufe
Die drei real gebundenen Links ausschließlich aus einer belegten READ-ONLY-Quelle übernehmen. Erst dann REALTEST 002 als vollständigen Lauf starten.
