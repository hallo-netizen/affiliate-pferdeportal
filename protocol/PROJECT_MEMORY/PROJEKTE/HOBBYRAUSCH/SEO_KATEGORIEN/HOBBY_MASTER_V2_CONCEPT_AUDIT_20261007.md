# HOBBY DEPOT – V2 KONZEPTAUDIT GEGEN AKTUELLEN ARBEITSSTAND

STAND: 2026-10-07
STATUS: PASS MIT NACHGEZOGENEN KORREKTUREN

## Geprüfte verbindliche Grundregeln

Bestätigt:
- drei Säulen CORE / EDITORIAL / DIRECTORY bleiben;
- acht Welten bleiben oberste fachliche CORE-Ebene;
- `Hobbywelten` bleibt View, nicht Parent;
- großer interner Hobbybestand + kleine sichtbare Navigation;
- große bekannte Hobbys = wirtschaftliche Anker;
- mittlere Hobbys = Rückgrat;
- Nischen bleiben SEO-/Longtail- und Inspirationsbestand;
- nicht monetarisierbare valide Hobbys werden nicht gelöscht;
- Bekanntheit/Beliebtheit erzeugt keine zweite Taxonomie;
- pro primärem Intent genau ein SEO-Owner;
- DataForSEO ist SEO-/Nachfrage-/Intent-Evidenz, keine Strukturautorität.

## Wichtigste Größenregel

Ein Hobby-Hub wird nicht anhand einer Gesamtzahl von Artikeln freigegeben.

Jede unterste Kategorie wird einzeln geprüft:
- unter 4 eigenständige Beiträge: zusammenlegen / keine eigene Leaf-Kategorie;
- 4: Grenzfall;
- 5–12: idealer Zielbereich;
- 13–14: oberhalb des Idealbereichs; keine automatische Teilung;
- ab etwa 15: Teilung prüfen, nicht automatisch erzwingen.

Ein Hobby-Hub benötigt typischerweise 3–6 tragfähige Leafs; ab etwa 10 eigenständigen Unterbereichen folgt eine Macro-/Split-Prüfung.

Ein Beitrag zählt nur einmal pro echtem Nutzer-/Suchintent.
Synonyme und bloße Formulierungsvarianten werden zusammengeführt.

## Zusammenfassung kleiner Themen

Kleine valide Hobbys bleiben als kanonische Hobby-Identitäten erhalten.

Wenn sie allein keine tragfähige Struktur ergeben, dürfen sie gemeinsam über:
- bestehende Parent-/Übersichtsseiten,
- gemeinsame Leaf-Kategorien,
- redaktionelle Cluster

sichtbar gemacht werden.

Wichtig:
Zusammenfassung bedeutet NICHT Identitäten verschmelzen.

Neue Zwischenkategorien werden während der Einzelbewertung noch nicht gebaut.
Zunächst wird nur `AGGREGATION_CANDIDATE` festgehalten.
Strukturänderungen kommen erst im späteren Gesamt-Delta.

## DataForSEO-Vertrag

Verbindlicher KISS-Weg nach vollständiger Realprüfung:

1. Fachlogik schlägt mögliche Leaf-Bereiche und echte eigenständige Artikelintents vor.
2. Diese fachlich unterschiedlichen Intents bilden die Content Capacity.
3. DataForSEO prüft Nachfrage, Primärkeyword, Synonyme, Core Keyword und Intent-Überschneidung.
4. Exaktes DataForSEO-Evidence darf zwei fachliche Intents als Dublette zusammenführen.
5. Wenn DataForSEO für einen fachlich eigenständigen Longtail keine exakte Zeile liefert, bleiben nur dessen SEO-Metriken offen; der Artikelintent bleibt bestehen.
6. Keyword-Ideas-/Suggestions-Rohzeilen erzeugen keine zusätzlichen Artikelintents.
7. Danach wird jede Leaf-Kategorie nach den Konzeptgrenzen bewertet.

DataForSEO darf NICHT bestimmen:
- Hauptwelt;
- Parent;
- neue Zwischenkategorie;
- Strukturrolle;
- CORE-Promotion;
- Löschung.

Automatische Keyword-Ideas-Tiefenrecherche ist im Normalweg nicht erforderlich.

## Vollständige Fehlerkettenprüfung Batch 001

Realer Ausgang:
- 16 Hobbys;
- 34 vorgeschlagene Leafs;
- 263 fachlich vorgeschlagene Artikelintents;
- 39 historische DataForSEO-Aufrufe;
- ca. 0.9738 USD historische Kosten;
- 0 Strukturwrites.

Gefundene Fehlerkette:
- V1.12.1: fehlende exakte Provider-Zeile wurde zu stark als fehlender Content interpretiert;
- V1.12.2/V1.12.3: Keyword-Ideas-Rohzeilen wurden fälschlich zur Content Capacity addiert;
- V1.12.4: Rohzeilen addierten keine Artikel mehr, aber ein fachlicher Intent blieb noch zu stark von lexikalischem Provider-Match abhängig.

Root Cause:
**Content Capacity und SEO-Evidenz wurden vermischt.**

Korrektur:
Regelvertrag 1.4 + HD-001 V1.12.5.

## V1.12.5 – Real-Result-Replay

Die echte gespeicherte V1.12.3-Datei wurde lokal mit V1.12.5 ohne neue Provider-Aufrufe neu ausgewertet.

Ergebnis:
- 34 ideale Leafs;
- 1 HOBBY_HUB_CANDIDATE;
- 1 EDITORIAL_TOPIC_CANDIDATE;
- 5 AGGREGATION_REVIEW;
- 3 MACRO_REVIEW;
- 6 EVIDENCE_REQUIRED;
- 0 Zielbaum-Writes.

Kapazitätsseitig typischer Hubbereich:
- Airbrush: 5 Leafs;
- Bean-to-Bar-Schokolade: 6;
- Aeroponik: 4;
- Ameisenhaltung: 6;
- 3D-Bogenschießen: 5;
- Wabikusa: 4.

Diese sechs sind noch nicht final publizierbar, weil Scope/Identität/Ownership getrennt geprüft werden müssen.

Buchbinden:
- 4 ideale Leafs;
- 5 / 6 / 6 / 6 eigenständige Artikelintents;
- HOBBY_HUB_CANDIDATE.

Macro:
- 3D-Druck;
- Amateurastronomie;
- Filzen.

Editorial:
- Treibholz sammeln.

Aggregation:
- alte Brettspiele;
- Air-Dry Clay;
- Airbrush-Modellbau;
- Alabasterschnitzen;
- Algenkultur.

Beleg:
`HOBBY_MASTER_V2_BATCH_001_V125_KISS_REPLAY_20261007.md`

## Hardtest

V1.12.5:
- PHP Source 68/68 PASS;
- Legacy 270/270 PASS;
- V1.12 POS/NEG PASS;
- realer 908/844/841-Lauf PASS;
- V1.12.1 Assessment Regression PASS;
- echter V1.12.3-Result-Replay PASS;
- Missing-Provider-Row-Negativtest PASS;
- Exact-Core-Keyword-Dedupe PASS;
- automatische Depth-Recherche = 0 Calls PASS;
- 0 neue Kosten PASS;
- 0 Strukturwrites PASS;
- Recalc idempotent PASS;
- Fresh Release PHP 31/31 PASS.

## Ergebnis

Konzept: konsistent.

Root Cause der wiederholten DataForSEO-Schleife: geschlossen.

Noch offen:
nur ein realer WordPress-Readback des exakt getesteten V1.12.5-Recalc-Ergebnisses.

Noch kein Zielbaum-Delta.
Noch kein WordPress-Sync.
