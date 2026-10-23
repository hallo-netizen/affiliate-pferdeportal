# HD-007 – HOBBYREGISTER CORE – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.1.5 FULL REPLACEMENT LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
`HD-007-HOBBYREGISTER-CORE`

Artefakt:
`HOBBY_DEPOT_VOLLERSATZ_20261023_HD003_1.50.729_HD007_1.1.5.zip`

SHA-256:
`f735f41fa1740904e13428350bef04cb89c34664fbb6e8ff1014b8581b6de046`

HD-007 liegt darin vollständig unter:
`hd-hobbyregister-core/`

## Ursache/Fix

1.1.4 nutzte fälschlich `astra_content_before`; Hobby Depot läuft auf ListingHive.

1.1.5:
- falschen Astra-Hook entfernt;
- Breadcrumb inline in exakt der Hobby-Depot-Standardgeometrie;
- Startseite › Magazin › Hobbyregister › Hobby;
- Auf einen Blick nur Icon + Wert;
- gleiche Hobbygruppe / ähnliche Hobbys garantiert disjunkt;
- beide Sidebar-Buttons gleiches helles Petrol;
- Gruppenüberschrift zweizeilig.

QA:
- 4 E2E-Profile PASS;
- Relationsaudit 862/862 PASS, 0 Überschneidungen;
- PHP-Lint PASS;
- Full-Unpack PASS.

Evidence:
`../../EVIDENCE_FULL_REPLACEMENT_20261023.md`

## EXAKT EINE NEXT ACTION

**Den bestehenden Ordner `hd-hobbyregister-core` vollständig durch den Ordner aus dem Vollersatz ersetzen und danach Live-Readback durchführen.**
