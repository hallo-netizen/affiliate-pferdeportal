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
- 13–14 zwingende Split-Prüfung;
- >15 nur mit expliziter Ausnahme.

Hobby-Hub:
- 3–6 tragfähige Leafs Ziel;
- 7–8 Split-/Macro-Prüfung;
- >8 grundsätzlich Macro/Split.

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

Befund:
- 16/16 hobby_id-Werte eindeutig;
- 4 aktuelle Alias-/Kanonikbindungen bestätigt;
- 12 semantische Identitäts-/Unterformprüfungen bleiben offen;
- 2 Scope-Fälle durch Pilot fachlich bestätigt;
- 9 weitere nur provisional gebunden;
- 5 benötigen Scope-Evidenz;
- nur Buchbinden besitzt bereits genug Größen-/Pilot-Evidenz für FIT + HOBBY_HUB;
- Treibholz sammeln bleibt sicher EDITORIAL, aber ARTICLE_ONLY vs. EDITORIAL_TOPIC bleibt offen;
- übrige Kandidaten bleiben wegen fehlender Content-Capacity-Evidenz fail-closed.

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

1. Fehlende Scope-/Content-Capacity-/Ownership-Evidenz für Batch 001 erzeugen.
2. Batch 001 erneut durch die gebundenen Regeln laufen lassen.
3. Nur `ASSESSED`-Fälle dürfen anschließend in die Gesamtbewertung einfließen.
4. Parallel die Research Queue kontrolliert durch Gate A/B führen; keine Blind-Promotion.
5. Danach Master batchweise fortsetzen.
6. Erst nach belastbarer Gesamtbewertung V1.12-Zielbaum als Delta aktualisieren.

Damit wird weder aus Monetarisierung noch aus Bekanntheit eine Taxonomie erfunden.


## 14. Nachgeholte Leaf-Kapazitätsregel

Das vollständige Konzept verlangt ausdrücklich:
Nicht die Gesamtzahl möglicher Hobbyartikel entscheidet über einen Hub.

Jede unterste Kategorie wird einzeln geprüft:
- 0–3 distinct Artikelintents → keine eigene Leaf-Kategorie;
- 4 → Ausnahmeprüfung;
- 5–12 → Zielbereich;
- 13–14 → Split-Prüfung;
- ab etwa 15 → Split erforderlich.

Nur echte verschiedene Nutzer-/Suchintents zählen.
Synonyme und Formulierungsvarianten zählen nicht mehrfach.

Ein Hobby-Hub benötigt typischerweise 3–6 tragfähige Leafs.

Maschinenlesbar gebunden in:
`HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json` Version 1.1.

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

Sie enthält:
- mögliche Leaf-/Artikelintents;
- Macro-/Split-Kandidaten;
- mögliche Zusammenfassungen kleiner Themen;
- keine erfundenen SEO-Zahlen.

DataForSEO-Request:
`HOBBY_MASTER_V2_BATCH_001_DATAFORSEO_REQUEST_20261007.json`

Realer vorhandener Buchbinden-Befund:
- Einstieg = 4 distinct Gruppen;
- Ausrüstung = 5;
- Material = 3;
- Techniken/Praxis = 4;
- Fragen/Probleme = 0;
- FAQ = 0.

Damit bleibt der bestehende Pilot erhalten, ist nach der neuen V2-Regel aber noch kein endgültiger HOBBY_HUB-PASS.

Für die übrigen Batch-001-Kandidaten fehlen im geprüften Bestand reale passende DataForSEO-Ergebnisse.
Keine Schätzung.

## 17. Aktueller Arbeitsweg

1. vorbereiteten Batch-001-Request real über DataForSEO ausführen;
2. Synonyme/Varianten deduplizieren;
3. Ownership über CORE / EDITORIAL / DIRECTORY prüfen;
4. jede Leaf-Kategorie separat zählen;
5. bei dünnen validen Hobbys Aggregation prüfen;
6. Batch 001 erneut bewerten;
7. erst bei stabilem Regelverhalten die Gesamtbewertung fortsetzen;
8. erst danach Zielbaum-Delta.
