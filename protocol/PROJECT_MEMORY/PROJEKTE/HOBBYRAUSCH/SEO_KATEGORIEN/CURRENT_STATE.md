# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-05
STATUS: V1.9.9 CONTENT-PILOT LIVE PASS / V1.10.0 ENGINE-TESTS PASS / REALER GESAMTPORTAL-E2E BLOCKED / KEIN RELEASE

## Zielautorität

`ZIELVERTRAG_HD001_AUTOMATISCHE_SEO_HIERARCHIE_20261003.md`

Ziel unverändert:
Konzept + echter Hobbybestand + DataForSEO → 8 Hauptwelten → variable Seitenhierarchie + Content-Kategorien + Magazin + HivePress → WordPress Publish → sichtbares Frontend → Readback → spätere Delta-Erweiterung.

## Belastbarer Live-Stand

V1.9.9 Content-Pilot real bestätigt:
- Buchbinden sichtbar;
- Einstieg / Ausrüstung / Material / Techniken & Praxis sichtbar;
- ein veröffentlichter Testartikel ist über die vier Kategorien im Frontend sichtbar.

Livebestand nicht zurückrollen.

## V1.10.0 Arbeitsstand

Lokale Arbeitskopie:
`/mnt/data/hd001-v1100-work`

Plugin-Header:
`1.10.0`

Frisch am 2026-10-05 erneut ausgeführt:
- Legacy Regression: 270/270 PASS;
- Portal Discovery PASS;
- World Routing PASS;
- Concept Auto World PASS;
- Eight Worlds E2E PASS;
- Portal Scale PASS;
- Portal Negative PASS;
- Admin Portal PASS;
- Portal Resume PASS.

Bewiesen ist damit die Maschine, nicht der reale Gesamtportal-Endlauf.

Skalierungsfixture:
844 synthetische Rohkandidaten, 2 Overview-Batches, 34 Concept-Batches bei Batchgröße 25.

Acht getestete Konzeptwelten:
Gestalten / Fertigen / Technik / Forschen / Pflanzen / Tiere / Bewegen / Sammeln.

## Konzept/DataForSEO-Vertrag

Konzept setzt Leitplanken.
DataForSEO entscheidet innerhalb dieser Leitplanken:
- Nachfrage;
- Synonyme/Core-Keyword-Gruppen;
- canonical Hobby-Seeds;
- evidenzbasierte Weltzuordnung;
- tragfähige Unterintentionen/Leafs;
- Marketplace-/Magazin-Evidenz.

Rohliste ist keine Taxonomie.
Ambige Evidenz bleibt fail-closed.

## ERSTER OFFENER BLOCKER

`HD001_V1100_REAL_HD002_INVENTORY_INPUT_NOT_BOUND`

Der autoritative HD-002-Stand sagt:
`Gesamtbestand: erfasst`.

Für HD-001 liegt dieser reale Bestand aktuell jedoch nicht als belastbar gebundene read-only Kandidatenquelle vor.
Weder manuelle Rekonstruktion noch synthetische Ersatzliste ist zulässig.

## EXAKT EINE NEXT ACTION

Den bereits erfassten echten HD-002-Gesamtbestand **read-only** exportieren/übernehmen und unverändert als `hobby_candidates`-Eingang an V1.10.0 Portal Discovery binden.

Danach in einem vollständigen realen lokalen Lauf:
echter Gesamtbestand → DataForSEO Overview → Synonym-/Demand-Filter → per-Hobby Suggestions → 8-Welten-Routing → Content + Magazin + HivePress → WordPress/Frontend-Simulation → Positiv-/Negativ-E2E.

Erst bei diesem Gesamt-PASS darf ein V1.10.x Release-/Uploadkandidat entstehen.

## NICHT ANFASSEN

- keinen neuen Gesamtbestand erfassen;
- keine Hobbyliste aus Chatgedächtnis bauen;
- V1.9.9-Livebestand nicht zurückrollen;
- keinen Live-Publish aus V1.10.0 vor vollständigem realem E2E.

## Packaging-Hinweis

Arbeitskopie ist noch kein Release.
`README.txt` nennt noch Version 1.9.6 und muss erst im späteren Release-/Packaging-Schritt bereinigt werden.
