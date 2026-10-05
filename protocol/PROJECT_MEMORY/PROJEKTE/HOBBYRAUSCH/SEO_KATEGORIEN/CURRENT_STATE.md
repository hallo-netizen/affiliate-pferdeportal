# HOBBYRAUSCH – SEO_KATEGORIEN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-05
STATUS: V1.10.0 GESAMTPORTAL-ENGINE LOKAL HARD PASS / REALER GESAMTBESTAND-EINGANG AUS HD-002 OFFEN / KEIN RELEASE

## Ziel

Konzept + echte Hobbykandidaten + DataForSEO → vollständiger Portalbaum:
- 8 Hauptwelten;
- variable Seitenhierarchie;
- Content-Kategorien;
- Magazin;
- HivePress;
- WordPress-Publish;
- sichtbares Frontend;
- Readback;
- spätere Delta-Erweiterung ohne Gesamtumbau.

## V1.9.9

Taxonomie-/Frontend-Pilot live bestätigt:
- Buchbinden sichtbar;
- Einstieg / Ausrüstung / Material / Techniken & Praxis sichtbar;
- ein veröffentlichter Testartikel ist über alle vier Kategorien im Frontend sichtbar.

Damit ist die technische WordPress-/Frontend-Abbildung für den Content-Strang real belegt.

## V1.10.0 – Gesamtportal-Engine

Lokale Arbeitskopie vorhanden:
`/mnt/data/hd001-v1100-work`

Version:
`1.10.0`

Neu vorhanden:
- `class-apkw-portal-discovery.php`;
- Portalprofil mit exakt 8 Konzeptwelten;
- DataForSEO Overview-Dedupe/Synonymgruppierung;
- automatische Weltzuordnung erst nach pro-Hobby DataForSEO-Suggestions;
- variable Concept-Batches;
- getrennte `journal_cat`-/`hp_listing_category`-Stränge;
- Admin-Portalprofil-Import und Resume;
- kein Publish während der Discovery.

## Konzept/DataForSEO-Vertrag

Konzept gibt nur Leitplanken:
- 8 Welten;
- Geschäftsmodell;
- erlaubte Stränge;
- bekannte bereits bestätigte Parent-Pfade;
- Kandidaten-/Leaf-Regeln.

DataForSEO entscheidet:
- ob ein Rohkandidat echte Nachfrage hat;
- Synonym-/Core-Keyword-Gruppierung;
- welche Kandidaten canonical weiterlaufen;
- pro Hobby die evidenzbasierte Weltzuordnung;
- welche Leaf-Gruppen genügend echte Keyword-Unterstützung haben;
- Marketplace-/Magazin-Evidenz.

Rohliste ist ausdrücklich **keine Taxonomie**.

## Harte lokale Tests

Frisch geprüft:
- Altregression: 270/270 PASS;
- V1.10.0 Portal Discovery PASS;
- Auto-World-Routing PASS;
- Concept Auto World PASS;
- Eight Worlds E2E PASS;
- Portal Scale PASS;
- Portal Negative PASS;
- Admin Portal PASS;
- Portal Resume PASS.

Skalierungstest:
- 844 Rohkandidaten;
- exakt 2 DataForSEO Overview-Batches;
- 844 positive Fixture-Kandidaten;
- 34 Concept-Batches bei Batchgröße 25.

8-Welten-E2E:
- Gestalten;
- Fertigen;
- Technik;
- Forschen;
- Pflanzen;
- Tiere;
- Bewegen;
- Sammeln;
alle korrekt geroutet.

Ambige Weltzuordnung bleibt fail-closed und wird nicht als Hobbyseite promotet.

## Wichtige Beleggrenze

Die 844er Prüfung ist **Skalierungs-/Maschinenbeweis**, nicht der reale Hobby-Depot-Bestand.

Der autoritative HD-002-Stand sagt:
`Gesamtbestand: erfasst`.

Dieser echte Bestand liegt jedoch im HD-002-Live-Speicher. Im aktuell verfügbaren Library-/Containerbestand wurde weder:
- ein vollständiger HD-002-Gesamtbestandsexport,
- noch die HD-002-V0.1.4-Source
gefunden.

Deshalb wird die reale Kandidatenliste **nicht aus Erinnerung rekonstruiert** und nicht durch synthetische Hobbys ersetzt.

## ERSTER OFFENER BLOCKER

`HD001_V1100_REAL_HD002_INVENTORY_INPUT_NOT_BOUND`

## NEXT ACTION

Den bereits erfassten echten HD-002-Gesamtbestand read-only als Kandidatenquelle binden.

Kein neuer Gesamtbestand.
Keine manuelle erfundene Hobbyliste.
Keine neuen Kategorien aus dem Kopf.

Nach Bindung:
echter Gesamtbestand → DataForSEO Overview → Synonym-/Demand-Filter → pro-Hobby Suggestions → 8-Welten-Routing → vollständiger Content-/Magazin-/HivePress-Baum → komplette Positiv-/Negativ-E2E-Simulation → erst dann Release/Live-Publish.
