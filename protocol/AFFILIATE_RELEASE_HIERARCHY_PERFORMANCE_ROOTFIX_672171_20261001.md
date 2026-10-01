# Affiliate-Zentrale 6.72.171 – Hierarchie-Performance Rootfix

Datum: 2026-10-01

## Reales Fehlerbild

Live mit Performance Diagnose Safe 2.3.0:
- /ausruestung/ ca. 1.65 s
- /ausruestung/ausruestung-sattel/ ca. 8.85 s
- /ausruestung/ausruestung-sattel/pferdesaettel/ ca. 9.09 s
- /ausruestung/ausruestung-trensen-und-gebisse/ ca. 8.91 s
- /ausruestung/ausruestung-trensen-und-gebisse/trensen/ ca. 8.62 s

Die Query-Zahl steigt dabei nur moderat. Der Unterschied entsteht im PHP-Rankingpfad für Produktplätze auf hierarchischen Unterseiten.

## Ziel

Die Hierarchie-Regeln bleiben fachlich identisch:
exakte Seite > Vorfahr/Themenkreis > allgemeiner Fallback.

Aber der reine Zielkanten-Test für tausende Kampagnen darf nicht pro Kandidat serialize/hash/array_unique/array_intersect ausführen.

## Fix

Für normale page/category_archive-Kontexte wird der bestehende automation_target_keys-Rank semantisch identisch über einen request-lokalen, vor-normalisierten Kontext-Set geprüft:
- page:<current>
- page:<ancestor>
- journal:<current>
- category:<current>
- category:<ancestor>
- bestehende Produktfamilienkante

Alle anderen Kontexte und Sonderfälle bleiben auf dem bisherigen Pfad.

## Pflichtsimulation vor Installer

Gleiche lokale WordPress-7.1.2/MariaDB-Instanz, gleicher synthetischer Bestand und gleiche drei Seitenebenen werden zweimal gefahren:
1. released 6.72.170
2. candidate 6.72.171

Gemessen werden dieselben öffentlichen Slot-Aufrufe für:
- Top-Ebene
- zweite Ebene
- dritte Ebene

Positiv: gleiche ausgewählten Kampagnen / gleiche Reihenfolge.
Negativ: fremder Ast und falsche Zielkante bleiben gesperrt.
Performance: 6.72.171 muss auf Ebene 2 und 3 klar schneller als 6.72.170 sein; andernfalls kein Installer.
