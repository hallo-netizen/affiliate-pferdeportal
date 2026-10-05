# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-10-05
STATUS: V1.9.9 LIVE CONTENT-PASS / V1.10.0 ENGINE-TESTS PASS / REALER GESAMTPORTAL-E2E BLOCKED / KEIN RELEASE

## Plugin

ID:
`HD-001-KATEGORIE-WORKFLOW`

Name:
`Affiliate-Portal Kategorie-Workflow`

Art:
Eigenentwicklung / Hobby-Depot-Linie.

Fachbüro:
`SEO_KATEGORIEN`

## Live

V1.9.9:
Buchbinden + vier Content-Kategorien + zugeordneter Testartikel real im Frontend bestätigt.

## V1.10.0 Arbeitskopie

Pfad:
`/mnt/data/hd001-v1100-work`

Plugin-Header:
`1.10.0`

Funktion:
- portalweite Rohkandidaten-Discovery;
- bounded DataForSEO Overview-Batches;
- Synonym/Core-Keyword-Dedupe;
- canonical Seeds;
- per-Hobby DataForSEO-Suggestions für Weltzuordnung;
- exakt 8 Konzeptwelten;
- variable Content-Hierarchie;
- getrennte Magazin-/HivePress-Stränge;
- Resume ohne erneute abgeschlossene Overview-Batches;
- kein Publish während Discovery.

Frisch ausgeführt:
- 270/270 Legacy Regression PASS;
- Portal Discovery PASS;
- World Routing PASS;
- Concept Auto World PASS;
- Eight Worlds E2E PASS;
- Portal Scale PASS;
- Portal Negative PASS;
- Admin Portal PASS;
- Portal Resume PASS.

Diese Tests beweisen die Engine, nicht den realen Gesamtbestand-Endlauf.

## ERSTER BLOCKER

`HD001_V1100_REAL_HD002_INVENTORY_INPUT_NOT_BOUND`

HD-002 meldet autoritativ `Gesamtbestand: erfasst`, aber dieser Bestand ist für HD-001 aktuell nicht als belastbare read-only `hobby_candidates`-Quelle gebunden.

## NEXT ACTION

Echten HD-002-Gesamtbestand read-only exportieren/übernehmen und unverändert an V1.10.0 Portal Discovery binden.

Danach kompletter realer DataForSEO→Gesamtbaum→WordPress/Frontend Positiv-/Negativ-E2E.

## Release-/Artefaktgrenze

Kein V1.10.0 Release und kein isoliertes `CURRENT.zip` ersetzen, solange der reale Gesamt-E2E blockiert ist.

Lokale Packaging-Metadaten sind noch nicht releasefertig:
`README.txt` nennt weiterhin Version 1.9.6.
