# HOBBY DEPOT – INTEGRATION HOBBY_MASTER V2 IN DEN BESTEHENDEN 3-SÄULEN-ZIELBAUM

STAND: 2026-10-07
STATUS: VERBINDLICHER INTEGRATIONSPLAN

## 1. Ziel

Das bestehende Drei-Säulen-Konzept bleibt bestehen.

Die neue Größen-/Rollenlogik wird als Bewertungsschicht ZWISCHEN Rohbestand und Zielbaum eingefügt.

Alt:
Rohliste → Zielbaum.

Neu:
Rohliste → HOBBY_MASTER V2 → Rollen-/Größenprüfung → 3-Säulen-Zielbaum → WordPress/HivePress.

Der HOBBY_MASTER ist damit die zentrale Hobby-Sammelstelle.
Die Rohliste bleibt unveränderte Provenienzquelle.

## 2. Aktueller Master-Bestand

Quelle:
- 908 Rohzeilen;
- 844 exakte unterschiedliche Namen;
- nach bereits gebundenen Alias-Zusammenführungen aktuell 841 kanonische Identitäten.

Bestehende V1.12-Evidenz wird übernommen:
- 329 bisherige Monetarisierungs-/CORE-Regeln;
- 286 DIRECT;
- 43 ASSISTED;
- übrige Kandidaten bleiben UNKNOWN, aber werden NICHT gelöscht.

Bekannte Aliasfälle werden zusammengeführt, z. B.:
- Treibholz → Treibholz sammeln;
- historische Buchbinderei → Buchbinden;
- Wabi-Kusa → Wabikusa;
- Tierhaarfilzen → Filzen.

## 3. Keine Vorab-Löschung

Der Master dient nicht dazu, die Rohliste früh auszudünnen.

Regel:
- fachlich gültige Kandidaten bleiben erhalten;
- noch nicht bewertete Kandidaten = UNASSESSED;
- nicht monetarisierbar = weiterhin EDITORIAL-/FINDER-Kandidat;
- erst OUT_OF_SCOPE darf aus der publizierenden Architektur ausgeschlossen werden;
- auch OUT_OF_SCOPE bleibt als bewertete Historie im Master erhalten.

Damit gibt es keinen Informationsverlust.

## 4. Geschützte Architektur im ersten Lauf

Nicht neu erfinden:
- acht Hauptwelten;
- Drei-Säulen-Modell;
- bestehende V1.12-Zwischenstruktur.

Harte Korrektur zur Ebenenlage:
- die acht Hauptwelten sind oberste fachliche CORE-Ebene;
- `Hobbywelten` ist Übersicht/View und KEIN Parent dieser acht Welten;
- das spätere V2-Zielbaum-Delta muss die V1.12-Baselinebeziehung `core:hub → core:world:...` korrigieren, ohne die acht Welten selbst neu zu erfinden.

Diese Knoten sind im ersten Durchlauf BASELINE_PROTECTED.

Geändert wird zuerst nur:
- Rolle einzelner Hobby-Kandidaten;
- Promotion/Demotion;
- Zusammenführung von Dubletten/Aliasen;
- Zuordnung zu CORE / EDITORIAL / FINDER_ONLY;
- Darstellung/Prominenz.

Zwischenkategorien werden erst verändert, wenn der fertig bewertete Bestand zeigt:
- Ast deutlich überlastet;
- Ast fachlich inkohärent;
- Ast praktisch leer;
- klare neue gemeinsame Hobby-Familie vorhanden.

Keine künstliche Symmetrie.

## 5. Bewertungsreihenfolge pro Kandidat

### Gate A – Portal-Scope
Fragen:
- aktive/wiederholbare Freizeitpraxis?
- erlern-/vertiefbarer Tätigkeitsschwerpunkt?
- natürliche Zuordnung zu einer der acht Welten?

Ergebnis:
- IN_SCOPE;
- SCOPE_REVIEW;
- OUT_OF_SCOPE.

Wenn eine Zuordnung nur erzwungen möglich wäre:
SCOPE_REVIEW statt neuer Hauptwelt.

### Gate B – Identität
Prüfen:
- exakte Dublette;
- Alias/Synonym;
- gleiche reale Tätigkeit mit anderem Namen;
- Varianten, die nur eine Unterform sind.

Ergebnis:
eine stabile hobby_id + Aliase.

### Gate C – Größenklasse
Mit Fachlogik + vorhandener SEO-/Intent-Evidenz prüfen:

MICRO:
zu klein für einen eigenen Hub.

FIT:
beherrschbare Hobby-Einheit.

MACRO:
zu groß; würde wie ein eigenes Portal funktionieren.

### Gate D – Content Capacity

Leaf-Kategorie:
- 5–12 Beiträge Ziel;
- 4 nur Ausnahme;
- 13–14 oberhalb des Idealbereichs; keine automatische Teilung;
- ab etwa 15 Teilung fachlich prüfen.

Hobby-Hub:
- 3–6 tragfähige Leafs Ziel;
- 7–9 oberhalb des typischen Hubbereichs; prüfen, aber nicht automatisch zerlegen;
- ab etwa 10 eigenständigen Unterbereichen Macro-/Split-Prüfung.

### Gate E – wirtschaftliche Rolle

DIRECT / ASSISTED:
starker CORE-Kandidat, sofern Größe passt.

NONE / UNKNOWN:
nicht löschen;
EDITORIAL / ARTICLE_ONLY / FINDER_ONLY prüfen.

### Gate F – Drei-Säulen-Ownership

Pro primärem Intent genau ein SEO-Owner.

CORE:
bekanntes Hobby / systematische Vertiefung.

EDITORIAL:
Inspiration / kleine Themen / Longtails / Situationen / Vergleiche.

DIRECTORY:
Anbieter-/Kurs-/Service-Intent.

Andere Säulen dürfen Relation/Filter/Verweis sein, aber keine konkurrierende SEO-Zielseite.

## 6. Veröffentlichungsrollen

Mögliche Endrollen:

- ORIENTATION_UNIVERSE
- HOBBY_HUB
- EDITORIAL_TOPIC
- ARTICLE_ONLY
- FINDER_ONLY
- OUT_OF_SCOPE

Diese Rollen sind veränderbar.
Keine Rolle löscht die hobby_id.

## 7. Umgang mit großen bekannten Hobbys

Große bekannte Hobbys werden NICHT blind in den Baum geschoben.

Sie kommen zuerst in eine RESEARCH_QUEUE.

Erste Kandidaten:
- Fotografie
- Malen
- Zeichnen
- Nähen
- Stricken
- Häkeln
- Holzwerken
- Heimwerken
- Wandern
- Radfahren
- Camping
- Schwimmen
- Klettern
- Bouldern
- Gärtnern
- Gemüseanbau
- Briefmarken sammeln
- Angeln
- Plane Spotting

Das sind ausdrücklich KEINE automatisch freigegebenen Hubs.

Jeder Kandidat durchläuft dieselben Gates wie die bestehenden Nischen.

Beispiel:
"Garten" kann als ORIENTATION_UNIVERSE enden.
"Gemüseanbau" kann darunter eine beherrschbare Hobby-Einheit sein.

## 8. Benutzerführung

Der große Master wird NICHT als komplette Navigation ausgespielt.

Sichtbare Einstiege bleiben klein:
- 8 Hobbywelten;
- Suche;
- Hobbyfinder;
- Magazin;
- Anbieter;
- kuratierte Views wie "Beliebte Hobbys".

Views erzeugen keine neuen SEO-Owner.

So kann der Backend-Bestand groß sein, während die Oberfläche übersichtlich bleibt.

## 9. Technische Umsetzung im Plugin

Der bestehende V1.12-Zielbaum bleibt die Zielbaum-Schicht.

Neu vorgeschaltete Daten:
HOBBY_MASTER V2.

Plugin-/Engine-Aufgaben:
1. Master lesen;
2. nur ASSESSED/APPROVED Rollen in Zielbaum übersetzen;
3. stabile hobby_id verwenden;
4. Alias-Merges berücksichtigen;
5. CORE/EDITORIAL/DIRECTORY-Rollen erzeugen;
6. Ownership validieren;
7. Soll/Ist-Diff;
8. Readback;
9. atomare Aktivierung.

DataForSEO darf dabei Felder anreichern:
- primary_keyword;
- demand_band;
- longtail_depth;
- synonyms.

Es darf structural_role und parent nicht selbst ändern.

## 10. Maschinenlesbarer Bewertungsvertrag

Verbindliche Regeldatei:
`HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json`

Sie trennt jetzt eindeutig:
- Portal-Scope;
- Identität/Alias;
- Content Capacity;
- Größenklasse;
- Portalrolle;
- wirtschaftliche Priorität;
- säulenübergreifende Ownership.

Fail-closed-Regel:
Fehlende Evidenz erzeugt `EVIDENCE_REQUIRED`.
Monetarisierung oder SEO-Nachfrage allein dürfen niemals eine Strukturrolle erzeugen.

Die sechs Portalrollen bleiben:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

## 11. Kontrollierter Batch 001

Der erste Master-Batch ist nicht mehr frei wählbar, sondern reproduzierbar definiert:

1. je geschützter Welt die lexikographisch erste bereits `IN_SCOPE_PROVISIONAL` gebundene hobby_id;
2. alle Master-Einträge mit Alias;
3. die ersten vier `UNASSESSED`-hobby_id lexikographisch;
4. danach Deduplizierung bei stabiler Reihenfolge.

Ergebnis:
16 Kandidaten.

Ausführung/Evidence:
`HOBBY_MASTER_V2_BATCH_001_RESULTS_20261007.json`

Aktueller Befund nach Regeln 1.4 und V1.12.5-Real-Result-Replay:
- 16/16 hobby_id-Werte eindeutig;
- 4 aktuelle Alias-/Kanonikbindungen stabil;
- fachliche Content Capacity ist nicht mehr an das Vorhandensein jeder einzelnen exakten DataForSEO-Longtail-Zeile gebunden;
- 34 vorgeschlagene Leafs liegen nach fachlicher Intent-Zählung im Idealbereich;
- Buchbinden = vollständiger HOBBY_HUB_CANDIDATE;
- Airbrush, Bean-to-Bar-Schokolade, Aeroponik, Ameisenhaltung, 3D-Bogenschießen und Wabikusa liegen kapazitätsseitig im typischen Hubbereich, bleiben aber wegen Scope-/Identitätsprüfung EVIDENCE_REQUIRED;
- Treibholz sammeln = EDITORIAL_TOPIC_CANDIDATE;
- 3D-Druck, Amateurastronomie und Filzen = MACRO_REVIEW;
- fünf kleine/spezielle Themen = AGGREGATION_REVIEW.

Kein Zielbaum-Write aus Batch 001.

## 12. Research-Queue-Intake

Die 19 wirtschaftlich/bekanntheitsseitig wichtigen Ergänzungen sind ausdrücklich NICHT Bestandteil der bisherigen 841 Master-Identitäten.

Maschinenlesbarer Intake:
`HOBBY_MASTER_V2_RESEARCH_INTAKE_20261007.json`

Aktueller Check:
- 19 Kandidaten geprüft;
- 0 exakte/current-Alias-Kollisionen gegen die 841 Identitäten;
- 17 bleiben bis Scope-Evidenz in der Research Queue;
- Angeln bleibt bewusster Scope-Review;
- Fotografie ist durch den vorhandenen Pilotbefund als IN_SCOPE / Welt Gestalten belegt und für eine provisorische Master-Identität bereit.

Vorbereitetes Intake-Delta:
`HOBBY_MASTER_V2_INTAKE_DELTA_001_20261007.json`

Dieses Delta ist ausschließlich Master-Intake.
Es ist KEIN Zielbaum-Delta und erzeugt keinen WordPress-/HivePress-/Frontend-Knoten.

## 13. Nächster Arbeitsblock

1. Genau einen realen V1.12.5-Readback des bereits vollständig lokal geprüften Batch-001-Endstands erzeugen.
2. Danach offene Scope-/Identitäts-/Ownership-Fälle klären; Content Capacity selbst ist für die fachlich vorgeschlagenen Intents nach Regeln 1.4 berechnet.
3. Nur belastbar bewertete Fälle dürfen in die Gesamtbewertung einfließen.
4. Danach Master batchweise mit derselben stabilen KISS-Logik fortsetzen.
5. Erst nach belastbarer Gesamtbewertung den Zielbaum als Delta aktualisieren.

Damit wird weder aus Monetarisierung noch aus DataForSEO-Rohzeilen eine Taxonomie erfunden.


## 14. Nachgeholte Leaf-Kapazitätsregel

Das vollständige Konzept verlangt ausdrücklich:
Nicht die Gesamtzahl möglicher Hobbyartikel entscheidet über einen Hub.

Jede unterste Kategorie wird einzeln geprüft:
- 0–3 distinct Artikelintents → keine eigene Leaf-Kategorie;
- 4 → Ausnahmeprüfung;
- 5–12 → Zielbereich;
- 13–14 → oberhalb des Idealbereichs, keine automatische Teilung;
- ab etwa 15 → Teilung prüfen.

Nur echte verschiedene Nutzer-/Suchintents zählen.
Synonyme und Formulierungsvarianten zählen nicht mehrfach.

Ein Hobby-Hub benötigt typischerweise 3–6 tragfähige Leafs.

Maschinenlesbar gebunden in:
`HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json` Version 1.4.

## 15. Zusammenfassung kleiner valider Hobbys

Ein kleines Hobby wird nicht gelöscht und seine hobby_id wird nicht mit anderen Identitäten verschmolzen.

Wenn es allein keine tragfähige SEO-Struktur ergibt, darf es zusammen mit fachlich verwandten kleinen Hobbys über:
- bestehende Übersichts-/Parentseiten;
- gemeinsame unterste Kategorien;
- redaktionelle Cluster

sichtbar gemacht werden.

Die gemeinsame unterste Kategorie muss selbst wieder die 5–12-Regel erfüllen.

Im Kandidatenlauf wird nur `AGGREGATION_CANDIDATE` markiert.
Eine neue Zwischenkategorie darf erst im späteren Gesamt-Zielbaum-Delta entstehen, wenn der vollständig bewertete Bestand sie belegt.

## 16. Batch 001 – Fachvorprüfung und DataForSEO-Abgleich

Fachvorprüfung:
`HOBBY_MASTER_V2_BATCH_001_SUBJECT_PREFLIGHT_20261007.json`

Sie definiert die fachlichen Leaf-/Artikelkandidaten.

Reale DataForSEO-Evidence ist inzwischen vorhanden:
- 39 historische Provider-Aufrufe;
- ca. 0.9738 USD historische Kosten;
- 0 Strukturwrites.

Die Tiefenläufe haben gezeigt, warum DataForSEO-Rohzeilen NICHT als Artikel gezählt werden dürfen.

Verbindliche KISS-Korrektur Regeln 1.4:
- Fachlogik zählt eigenständige Artikelintents;
- DataForSEO reichert an und dedupliziert;
- fehlende exakte Longtail-Zeilen löschen keinen fachlich eigenständigen Artikelintent;
- Keyword-Ideas-/Suggestions-Rohzeilen erzeugen keine Artikel;
- automatische Depth-Recherche ist kein Normalweg.

Lokaler Endreplay:
`HOBBY_MASTER_V2_BATCH_001_V125_KISS_REPLAY_20261007.md`

## 17. Batch 001 – fachlich geschlossen

Finale Bewertung:
`HOBBY_MASTER_V2_BATCH_001_FINAL_ASSESSMENT_20261007.json`

Ergebnis:
- 7 HOBBY_HUB;
- 3 ORIENTATION_UNIVERSE;
- 6 EDITORIAL_TOPIC;
- 0 unresolved;
- 0 Strukturwrites.

Wesentliche Ownership-Grenzen sind pro Kandidat gebunden.

## 18. Aktueller Arbeitsweg

1. Batch 002 deterministisch als erste 16 noch nicht final bewerteten Master-Identitäten in stabiler Master-Reihenfolge ziehen.
2. Fachlogik definiert Scope, Identität, Größenklasse, mögliche Leafs und Artikelintents.
3. DataForSEO im Normalweg nur als gebündelter Overview-Abgleich, keine automatische Keyword-Ideas-Tiefenrecherche.
4. Batch fachlich schließen.
5. Master batchweise vollständig fortsetzen.
6. Erst nach vollständiger 841er Bewertung Zielbaum-Delta erzeugen.
7. Danach WordPress/HivePress-Sync und Frontend-Readback.

Keine Strukturänderung aus einem Zwischenbatch.
