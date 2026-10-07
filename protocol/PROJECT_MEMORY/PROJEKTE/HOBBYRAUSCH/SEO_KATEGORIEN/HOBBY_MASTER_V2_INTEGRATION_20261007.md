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
- 13–15 zwingende Split-Prüfung;
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

## 10. Nächster Arbeitsblock

Nicht sofort alle 841 Kandidaten vollredaktionell manuell bewerten.

Stattdessen:

1. Master technisch validieren;
2. Bewertungsregeln maschinenlesbar machen;
3. Pilot-Sample aus fünf Typen:
   - starker bestehender Hub: Buchbinden;
   - große bekannte Erweiterung: Fotografie;
   - Macro-Grenze: Garten;
   - kleine Nische: Treibholz sammeln;
   - Scope-Grenzfall: Musizieren;
4. Pilot durch Scope + Größe + Content Capacity + Monetarisierung + 3-Säulen-Routing laufen lassen;
5. Regeln korrigieren;
6. danach Batch-Bewertung des Gesamtbestands;
7. erst dann V1.12-Zielbaum als Delta aktualisieren.

Damit wird nicht erneut ein kompletter Baum auf Verdacht gebaut.
