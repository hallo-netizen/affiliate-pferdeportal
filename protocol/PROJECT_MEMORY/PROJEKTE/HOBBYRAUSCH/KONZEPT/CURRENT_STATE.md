# HOBBYRAUSCH – KONZEPT – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-09
STATUS: FACHKONZEPT 2.7 AKTIV / STARTFÄHIGE CONTENT-EBENE + FLEXIBLES MAGAZIN / HD-001-TECHNIK BIS ZUM NEUEN FACH-SOLL EINGEFROREN

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_KONZEPT`.

## Aktueller belastbarer Stand

Marke:
**Hobby Depot**

Drei Säulen:
- CORE = Hauptportal;
- EDITORIAL = Magazin;
- DIRECTORY = HivePress / Anbieter.

Acht geschützte Hauptwelten:
**Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln**

### Harte Ebenenregel

Die acht Hauptwelten sind die oberste fachliche CORE-Ebene.

`Hobbywelten` ist nur Übersichts-/Einstiegsseite bzw. View und NICHT Parent der acht Hauptwelten.

Beliebte Hobbys, ungewöhnlich, zuhause, günstig usw. sind ebenfalls Views/Filter/kuratierte Einstiege, keine zweite Taxonomie.

## Portfolioziel

Hobby Depot soll wirtschaftlich breiter werden, ohne zum beliebigen Massenportal zu explodieren.

Integrierte Mischung:
- große bekannte Hobbys = wirtschaftliche Anker;
- mittlere Hobbys = stabiles Rückgrat;
- Nischen-/ungewöhnliche Hobbys = SEO-Longtail + Differenzierung.

Diese Klassen verändern nicht die kanonische Identität und erzeugen keine Parallelstruktur.

Großer interner Hobbybestand ist erlaubt.
Die sichtbare Navigation bleibt klein und selektiv.

## Portalgrenze

Ein Thema wird regulär aufgenommen, wenn es:
- aktive/wiederholbare Freizeitpraxis ist;
- erlern-/vertiefbaren Tätigkeitsschwerpunkt besitzt;
- natürlich in eine der acht Welten passt;
- nicht nur durch erzwungene Zuordnung integrierbar ist.

Ein echtes Hobby außerhalb dieser natürlichen Passung erzeugt nicht automatisch eine neunte Welt.

## Rollen- und Größenlogik

Mögliche Rollen:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

Leaf-Kategorie:
- unter 4 zusammenlegen / keine eigene Leaf-Kategorie;
- 4 Grenzfall;
- ideal etwa 5–12 Beiträge;
- 13–14 oberhalb des Idealbereichs / prüfen;
- ab etwa 15 Teilung prüfen.

Hobby-Hub:
- typischer Zielbereich 3–6 tragfähige Leaf-Kategorien;
- 7–9 oberhalb des typischen Bereichs / prüfen;
- ab etwa 10 Macro-/Split-Prüfung.

Monetarisierung entscheidet nicht über Behalten/Löschen.
Nicht monetarisierbare gültige Themen bleiben für Magazin/SEO/Finder erhalten.

## Zentrale Hobby-Sammelstelle

Rohliste bleibt unveränderte Provenienzquelle.

Aktive Bewertungsbasis:
`/hobby rausch/HOBBY_DEPOT_HOBBY_MASTER_V2_20261007.json`

Current-Zeiger:
`KONZEPT/VORARBEITEN_HOBBYFINDER/HOBBY_MASTER_V2_CURRENT.md`

Bestand:
- 908 Rohzeilen;
- 844 exakte Namen;
- 841 kanonische Identitäten nach aktuellen Alias-Merges;
- 329 bestehende V1.12-Monetarisierungs-/CORE-Regeln übernommen;
- 286 DIRECT;
- 43 ASSISTED;
- 512 UNKNOWN, aber weiterhin erhalten;
- zusätzlich 19 Research-Queue-Kandidaten außerhalb der 841 aktuellen Identitäten;
- 0 Namens-/Alias-Kollisionen im aktuellen Intake-Check;
- Fotografie ist durch den Pilotbefund für eine provisorische Master-Aufnahme vorbereitet.

## Neue bekannte Hobby-Kandidaten

Research Queue:
Fotografie, Malen, Zeichnen, Nähen, Stricken, Häkeln, Holzwerken, Heimwerken, Wandern, Radfahren, Camping, Schwimmen, Klettern, Bouldern, Gärtnern, Gemüseanbau, Briefmarken sammeln, Angeln, Plane Spotting.

Nicht automatisch publizieren.
Sie durchlaufen dieselben Scope-/Größen-/Rollen-Gates wie die bisherigen Nischen.

## Maschinenlesbare Umsetzung

Gebunden:
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_ASSESSMENT_RULES_20261007.json`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_RESULTS_20261007.json`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_RESEARCH_INTAKE_20261007.json`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_INTAKE_DELTA_001_20261007.json`

Damit ist die frühere Lücke zwischen Konzeptregel und tatsächlicher maschinenlesbarer Entscheidung geschlossen.

Wichtig:
Fehlende Evidenz führt zu `EVIDENCE_REQUIRED`, nicht zu einer geratenen Rollen- oder Weltzuordnung.

Batch 001 ist autoritativ final:
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_FINAL_ASSESSMENT_20261007.json`;
- 16/16 geschlossen;
- 7 HOBBY_HUB;
- 3 ORIENTATION_UNIVERSE;
- 6 EDITORIAL_TOPIC;
- 0 unresolved;
- 0 Strukturwrites.

## Nachprüfung gegen das vollständige Konzept

Nachgezogen:
- nicht die Gesamtzahl eines Hobbys zählt, sondern jede unterste Kategorie einzeln;
- Ziel pro unterster Kategorie: 5–12 eigenständige Artikelintents;
- kleine valide Hobbys dürfen in stärkeren Übersichts-/Leaf-/Magazinstrukturen zusammengefasst werden, ohne ihre Hobby-Identität zu verlieren;
- neue Zwischenkategorien werden erst im späteren Gesamt-Delta gebaut;
- Fachlogik definiert und zählt die eigenständigen Artikelintents; DataForSEO validiert Nachfrage, Synonyme, Core-Keywords und Intent-Überschneidung, kann Dubletten zusammenführen, erzeugt aber weder Struktur noch zusätzliche Artikelintents und löscht keinen fachlich eigenständigen Intent nur wegen einer fehlenden exakten Longtail-Zeile.

Konzeptaudit:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_CONCEPT_AUDIT_20261007.md`

## Reales Batch-001-Ergebnis – historische Evidence

Der echte WordPress-/DataForSEO-Lauf wurde ausgeführt und bleibt als Evidence erhalten:
- 263 fachlich vorgeschlagene Artikelintents;
- 106 exakte Keyword-Overview-Zeilen im ersten Aufruf;
- anschließend historische Depth-Aufrufe;
- insgesamt 39 Provider-Aufrufe;
- ca. 0.9738 USD historische Kosten;
- 0 Strukturwrites.

Wichtig:
Die damaligen Zwischenbewertungen aus V1.12.1–V1.12.4 sind durch die KISS-Regel 1.4 für Content Capacity fachlich überholt.
Sie bleiben nur Fehler-/Evidence-Historie und dürfen nicht als aktueller Rollenbefund verwendet werden.

## KISS-Korrektur nach vollständiger Fehlerkettenprüfung

Die reale DataForSEO-Evidence ist vollständig vorhanden.

Die wiederholte technische Schleife hatte drei aufeinanderfolgende Fehlinterpretationen:
- fehlende exakte DataForSEO-Zeile wurde zu stark als fehlender Content behandelt;
- danach wurden Keyword-Ideas-Rohzeilen fälschlich als zusätzliche Artikel gezählt;
- anschließend wurden fachlich definierte Artikel noch zu stark von einem lexikalischen Provider-Match abhängig gemacht.

Verbindlich ab Regelvertrag 1.4:

1. **Fachlogik bestimmt die Content Capacity.**
   Gezählt werden fachlich eigenständige Nutzer-/Suchintents pro unterster Kategorie.

2. **DataForSEO ist der Abgleich.**
   Es liefert Nachfrage, Primärkeyword, Synonyme, Core Keyword und Intent-Überschneidung.

3. **DataForSEO darf deduplizieren.**
   Wenn zwei fachliche Seeds nach echter Core-Keyword-/Synonym-Evidence dasselbe meinen, zählen sie einmal.

4. **Fehlende exakte Longtail-Zeile löscht keinen Artikelintent.**
   Nur dessen SEO-Metriken bleiben offen.

5. **Provider-Rohzeilen erzeugen keine Artikel.**
   Keyword Ideas/Suggestions sind im Normalweg keine automatische Content-Capacity-Stufe.

Damit entspricht der Ablauf wieder dem Grundprinzip:
**fachlich prüfen, wie viele Einzelbeiträge die unterste Kategorie trägt → DataForSEO abgleichen → danach Rolle/Größe entscheiden.**

Der vollständige reale Batch wurde mit V1.12.5 lokal neu gerechnet:
- 34 ideale Leafs;
- Buchbinden = vollständiger HOBBY_HUB_CANDIDATE;
- sechs weitere Hobbys liegen kapazitätsseitig im typischen Hubbereich, benötigen aber noch Scope-/Identitätsfreigabe;
- drei Macro-Reviews;
- ein Editorial-Thema;
- fünf Aggregation-Reviews;
- 0 Strukturwrites.

## Pilotbefund – historisch eingeordnet

Frühere Pilot-/Zwischenbefunde sind durch die finale Batch-001-Datei ersetzt, soweit sie Batch-001-Rollen betreffen.
Fotografie/Garten/Musizieren bleiben nur als separate frühere Konzeptbeispiele bestehen und sind nicht Teil von Batch 001.

## Autoritative Konzeptdateien

- `HOBBY_GROESSEN_ROLLENMODELL_20261007.md`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_INTEGRATION_20261007.md`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_PILOT_20261007.md`

## Technische Abgrenzung

Pluginversionen, technische Release-/Teststände und Live-Status ausschließlich aus:
- `PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`;
- `SEO_KATEGORIEN/CURRENT_STATE.md`.

## Batch 001 – fachlicher Abschluss

Einzige autoritative Abschlussdatei:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_001_FINAL_ASSESSMENT_20261007.json`

Ergebnis:
- 7 HOBBY_HUB;
- 3 ORIENTATION_UNIVERSE;
- 6 EDITORIAL_TOPIC;
- 0 unresolved.

## Batch 002 – vorbereitet

Deterministische erste 16 noch nicht final bewerteten Master-Identitäten sind gebunden.

Fachvorbereitung:
- 51 Leafs;
- 304 eigenständige Artikelintents;
- 304 DataForSEO-Seeds;
- ein einziger Overview-Abgleich;
- keine automatische Tiefenrecherche.

Plan:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_BATCH_002_PREPARED_20261008.json`


## Praktische Produktionsentscheidung – finalisiert

Der 841er Master ist Inventar, nicht 841 Pflichtseiten.

Historischer Produktionsstand vor Regelkorrektur 2.6/1.6:
- 340 CORE-Hobbyidentitäten;
- 501 Finder/Editorial-Identitäten.

Dieser frühere Stand ist für die Ebenenlogik ÜBERHOLT.

Aktuell verbindlich:
- HOBBY_HUB besitzt eine sichtbare Content-Kategorieebene;
- typischer Zielbereich 3–6 tragfähige Content-Kategorien;
- jede Leaf-Kategorie ideal 5–12 eigenständige Beitragsintentionen;
- reguläre HOBBY_HUB-Beiträge liegen nicht direkt unter der Hobbyseite;
- keine künstlichen oder leeren Leafs.

### Endgültige Weltenstruktur

Die acht Welten:
Gestalten / Fertigen / Technik / Forschen / Pflanzen / Tiere / Bewegen / Sammeln

sind echte physische CORE-Rootseiten.

`Hobbywelten` bleibt eine Übersichts-/View-Seite und besitzt 8 Relation-Verweise auf diese Welten.
Es ist ausdrücklich kein struktureller Parent.

Finaler Zielbaum:
- 103 Basis-Logikknoten;
- 440 aufgelöste Logikknoten;
- 431 physische Zielobjekte;
- davon 404 Pages.

Kalibriertes CORE-Delta:
- 12 Promotionen;
- 1 Demotion;
- netto +11 CORE-Identitäten.

Batch 001–003 waren Kalibrierung.
Batch 004+ ist gestrichen.

## Sichtbarkeits- und Kategorienregel – verbindlich ab 2026-10-08

- Acht Welten bleiben die oberste fachliche CORE-Ebene.
- Alle tatsächlich vorhandenen kanonischen Ebenen werden im normalen Drill-down angezeigt.
- Globaler Header klein; lokale Kindnavigation vollständig.
- Zwischenbereiche nicht künstlich zusammenziehen, nur um die Navigation dünn zu halten.
- Bis etwa 10–11 fachlich klare Zwischenbereiche unter einer Welt sind zulässig.
- HOBBY_HUB: 3–6 tragfähige Content-Kategorien als sichtbare Ebene.
- Leaf: ideal 5–12 eigenständige Beitragsintentionen.
- Keine leeren Symmetrie-Kategorien.
- FAQ bleibt Prüfbereich; keine pauschale Pflichtkategorie ohne ausreichende eigenständige Intents.
- Ein Beitrag besitzt genau einen Intent-/Kategorie-Owner.

Aktueller Master:
- 860 kanonische Identitäten;
- 359 CORE;
- 501 Finder/Editorial.

Audit:
`../SEO_KATEGORIEN/HD001_BALANCED_VISIBLE_LEVELS_AUDIT_20261008.json`

## Fachlicher Endstand Kategorienstruktur

Abschluss:
- 359/359 damalige Current-CORE-Identitäten nach Regeln 1.6 entschieden;
- 279 HOBBY_HUB;
- 53 ORIENTATION_UNIVERSE;
- 22 EDITORIAL_TOPIC;
- 5 ALIAS_ONLY;
- 65 fachlich geprüfte Zwischenbereiche;
- 1.292 sichtbare Content-Kategorien;
- alle HOBBY_HUBs besitzen ihre sichtbare Content-Ebene;
- keine künstlichen Symmetrieäste;
- kein Capacity-Verstoß.

Autoritativ:
`../SEO_KATEGORIEN/HD001_FINAL_VISIBLE_FACH_SOLLPROFIL_20261008.json`

## Operative Abgrenzung

Das Konzeptbüro enthält keine eigene dynamische HD-001-Live-/Plugin-/Sync-Wahrheit.

Für die operative Fortsetzung gilt ausschließlich:
`../SEO_KATEGORIEN/CURRENT_STATE.md`

Dort stehen aktueller Live-Status, erster Blocker und exakt eine NEXT ACTION.

## EXAKT EINE NEXT ACTION

Keine weitere Konzeptänderung.
Für HD-001 direkt der zuständigen SEO-Kategorien-Current folgen.



## NEUAUSRICHTUNG 2026-10-09 – STARTFÄHIGE CONTENT-EBENE

### Ausgangspunkt

Die technische Zielbaum-Arbeit hat bewiesen, dass sich ein großer WordPress-Zielbaum deterministisch schreiben, lesen, zurückrollen und idempotent halten lässt.

Die sichtbare Fachstruktur war trotzdem nicht ausreichend nutzerorientiert:
- viele Hobby-Hubs hatten nur individuell abgeleitete Fach-Leafs;
- universelle Nutzerbedürfnisse wie Einstieg, FAQ und Ausrüstung/Kosten waren nicht systematisch abgedeckt;
- ein interner Frontend-Readback konnte PASS melden, obwohl der sichtbare reale Seitenpfad teilweise nicht das erwartete Ergebnis zeigte;
- die bisherige 3–6-Leaf-Zielgröße förderte unnötiges Zusammenfassen.

Neue Grundentscheidung:
**Nicht die perfekte Endtaxonomie vorab bauen. Einen fachlich sauberen Startzustand bauen, sichtbar prüfen und später normal weiterentwickeln.**

### Harte Designregel – zweite CORE-Ebene

Direkte sichtbare Kinder einer Hauptwelt im Mega-Menü:
**maximal 10**.

Aktueller sichtbarer Mega-Menü-Prüfstand des Live-Readbacks:
- Gestalten 7;
- Fertigen 10;
- Technik 11;
- Forschen 5;
- Pflanzen 9;
- Tiere 7;
- Bewegen 8;
- Sammeln 8.

Strukturelle Direktknoten wie Heimwerken oder Gärtnern können zusätzlich auf der Welt-Landingpage existieren; sie zählen nicht als zusätzliche Mega-Menü-Zwischenkategorie.

Folge:
Nur Technik muss vor dem nächsten Zielbaum fachlich von 11 auf höchstens 10 sichtbare Mega-Menü-Kinder gebracht werden.

Keine Zusammenlegung nur aus Symmetriegründen. Aber die optische 10er-Grenze ist verbindlich.

### Unterste Content-Ebene – neue Startlogik

Bestehende fachlich sinnvolle Leafs bleiben bestehen.

Zusätzlich wird jeder HOBBY_HUB auf vier universelle Nutzerbedürfnisse geprüft:

1. **Einstieg & Grundlagen – Pflicht als eigene sichtbare Kategorie.**
2. **FAQ / Häufige Fragen – Pflicht als eigene sichtbare Kategorie.**
3. **Ausrüstung & Kosten – Standardkategorie, sobald mindestens 3 eigenständige Beiträge möglich sind; sonst sinnvoll mit Einstieg zusammenführen.**
4. **Praxis & Vertiefung – Pflicht als Nutzerabdeckung.** Keine künstliche Doppelung, wenn vorhandene Fach-Leafs wie Training, Tricks, Techniken, Projekte oder Spezialmethoden erfahrene Nutzer bereits bedienen.

Danach kommen hobbiespezifische Leafs hinzu, z. B.:
Training, Übungen, Tricks, Techniken, Sicherheit/Gefahren, Regeln, Herausforderungen, Pflege, Fehler/Lösungen, Projekte, Materialien, Orte/Touren, Wettbewerbe, Bestimmen/Echtheit/Wert.

Neue Mindestschwelle:
**3 eigenständige sinnvolle Beitragsintentionen reichen für einen startfähigen Leaf.**
4+ = klar tragfähig.
Keine Synonymzählung.

Es gibt auf dieser letzten Ebene keine künstliche Gesamtobergrenze mehr. 7, 8, 9 oder mehr sinnvolle Leafs sind zulässig.

### Abgrenzung Einstieg vs. FAQ

Einstieg & Grundlagen:
- zusammenhängende Erklärartikel;
- Voraussetzungen;
- erste Schritte;
- Grundbegriffe;
- Einstiegshürden;
- typische Anfängerfehler.

FAQ:
- konkrete Frageintents;
- bevorzugt aus DataForSEO/PAA/Longtails;
- jede Frage nur dann eigener Artikel, wenn sie einen eigenständigen Such-/Nutzerintent besitzt;
- kein Doppelowner: eine große Grundlagenfrage lebt als Hauptartikel in Einstieg und wird aus FAQ verlinkt.

### Rolle von DataForSEO

DataForSEO wird vereinfacht genutzt.

Es darf auf der letzten Ebene:
- echte Frageintents sammeln;
- Leaf-Kandidaten unter einem feststehenden Hobby vorschlagen;
- Keywords/Longtails clustern;
- Bezeichnungen und Nachfrage prüfen;
- Überschneidungen/Dubletten sichtbar machen.

Es darf weiterhin nicht:
- Hauptwelt oder oberen Parent bestimmen;
- ein Hobby eigenmächtig in CORE promoten;
- eine zweite konkurrierende Taxonomie erzeugen.

### Start statt Endlosmodell

Vor Massenausrollung werden 10 repräsentative HOBBY_HUBs vollständig nach der neuen Regel aufgebaut und **im echten Browser/Theme** geprüft.

Erst wenn dort:
- alle Leaf-Kacheln sichtbar sind;
- Einstieg/FAQ/Ausrüstung/Vertiefung logisch getrennt sind;
- bestehende Fachkategorien erhalten sind;
- keine Doppelungen entstehen,

wird auf die restlichen Hubs skaliert.

## MAGAZIN – NEUES PARALLELKONZEPT

Das Magazin ist frei von der Mega-Menü-10er-Grenze. Es wird über Kacheln, organische Suche und interne Einstiege erschlossen.

Startfähige Kachelstruktur:
1. Hobby finden
2. Hobby-Ideen & Inspiration
3. Ungewöhnliche & skurrile Hobbys
4. Neue Hobbys & Trends
5. Hobby-Porträts
6. Menschen & Geschichten
7. Geschichte & Herkunft
8. Wissen & Glossar
9. Vergleiche & Alternativen
10. Zeit, Budget & Platz
11. Alter & Lebensphasen
12. Saison, drinnen & draußen

Die Anzahl darf später wachsen.

Valide schräge/Nischenthemen wie Treibholz sammeln werden nicht gelöscht:
- kanonische Identität bleibt erhalten;
- kein erzwungener CORE-Platz;
- redaktionelle Nutzung im Magazin/Hobbyfinder;
- ein primärer SEO-Owner, zusätzliche Einstiege nur als View/Relation.

Das Magazin darf sowohl Inspiration als auch echte Informationssuche bedienen:
Skurriles, Alter/Lebensphasen, Geschichten, Glossar, neue Trends, Vergleiche, Situationen, Saison, Budget, Platz, Finder-Inhalte und Hobby-Porträts.

## RETROSPEKTIVE HD-001 – FEHLER, IRRWEGE UND VERBINDLICHE LEHREN

### Was funktioniert hat
- stabile Hobby-/Node-Identitäten;
- Dry-Run vor Writes;
- Rollback;
- Idempotenz;
- Schutz vor Fremdobjekten;
- Alias-/Legacy-Migration;
- Trennung CORE / EDITORIAL / DIRECTORY;
- vollständiger Soll/Ist-Readback als technische Kontrolle.

### Was unnötig Zeit gekostet hat

1. **Technik vor sichtbarem Nutzerziel.**
   Der Zielbaum wurde technisch immer genauer, bevor die Frage abschließend beantwortet war: Was soll ein Mensch auf einer Hobbyseite tatsächlich sehen?

2. **Zu abstrakte Content-Capacity-Regeln.**
   5–12 Intents und 3–6 Leafs wurden zu stark als Strukturziel verwendet. Dadurch wurden offensichtliche universelle Bereiche nicht konsequent angelegt.

3. **DataForSEO als zu strenges Gate.**
   Provider-Evidence wurde zeitweise mit fachlicher Content-Existenz verwechselt. Künftig dient DataForSEO auf der Leaf-Ebene als Recherche-/Clustering-/Validierungswerkzeug, nicht als alleinige Existenzberechtigung.

4. **Interner Renderer mit realem Frontend verwechselt.**
   Ein interner 279/279-PASS beweist nicht automatisch die tatsächliche sichtbare Ausgabe durch Theme/Template. Künftig gehört ein echter Browser-/Theme-Pilot vor jeder Massenausrollung zur Fachabnahme.

5. **Zu viele Versionsschritte vor einem visuellen Pilot.**
   Mehrere technische Korrekturen wurden nacheinander gebaut, obwohl 10 vollständig fertig geprüfte reale Hobbyseiten früher gezeigt hätten, ob das Fachmodell überhaupt überzeugt.

6. **Migration und Fachkonzept gleichzeitig verändert.**
   Legacy-/Alias-/Rollback-Probleme und die eigentliche Kategorienlogik wurden zu eng miteinander gekoppelt. Künftig: erst Fach-Soll festlegen, dann Migration exakt darauf anwenden.

7. **Die Mega-Menü-Grenze war nicht früh genug harte Anforderung.**
   Für die zweite CORE-Ebene gilt künftig von Anfang an max. 10 sichtbare Kinder.

8. **Magazin zu stark als Restablage gedacht.**
   EDITORIAL ist eine eigenständige organische Informations-/Inspirationssäule und wird künftig parallel konzipiert, nicht erst nach CORE als Auffangbecken.

### Verbindliche Vorgehensweise für kommende Portale

1. sichtbares Nutzerziel zuerst;
2. feste Designgrenzen sofort dokumentieren;
3. vorhandenen Bestand erhalten;
4. universelle Nutzerbedürfnisse definieren;
5. fachliche individuelle Kategorien ergänzen;
6. Mindestbestand 3 echte Beiträge pro Leaf;
7. DataForSEO zur Recherche/Validierung;
8. 10 reale Seiten komplett als Pilot;
9. echter Browser-/Theme-Check;
10. erst danach Automatisierung und Massensync;
11. keine neue Plugin-Version für jeden Einzelfehler, sondern gebündelte Ursachenbehebung;
12. Technik gilt erst dann als fertig, wenn das sichtbare Ergebnis fachlich stimmt.

## NÄCHSTE FACHLICHE AKTION

Kein weiterer HD-001-Code-Fix.

Zuerst:
1. Technik von 11 auf maximal 10 sichtbare Mega-Menü-Zwischenkategorien neu ordnen;
2. 10 repräsentative Hobby-Hubs für den neuen Leaf-Standard auswählen;
3. bestehende Leafs unverändert übernehmen;
4. fehlende universelle Leafs ergänzen;
5. DataForSEO-Fragen und zusätzliche hobbiespezifische Leaf-Kandidaten prüfen;
6. Magazin-Kachelstruktur parallel als Startbestand ausarbeiten;
7. erst danach neues Sollprofil und technische Umsetzung.


## KONKRETER STARTPILOT 2.7 – 10 HOBBY_HUBS

Der Pilot deckt unterschiedliche Hobbytypen/Welten ab und verwendet den realen aktuellen Bestandsbaum:

1. Buchbinden
2. Balance Board
3. Glasmalerei
4. Lasergravieren
5. Fledermausbeobachtung
6. Hydrokultur
7. Riffaquaristik
8. Briefmarken sammeln
9. Geocaching
10. Imkerei

### Pilotregel

Für jeden der 10:
- vorhandene Content-Kategorien unverändert als Ausgangspunkt übernehmen;
- semantisch prüfen, welche universellen Nutzerbedürfnisse bereits erfüllt sind;
- niemals einen vorhandenen guten Leaf nur für ein Standardschema ersetzen;
- fehlendes Einstieg & Grundlagen ergänzen;
- fehlendes FAQ ergänzen;
- Ausrüstung & Kosten ergänzen, wenn nach Abzug bestehender Leafs mindestens 3 eigenständige Beiträge übrig bleiben;
- erfahrene Nutzer müssen über bestehende Fach-Leafs oder einen zusätzlichen Vertiefungs-Leaf bedient werden;
- weitere hobbyspezifische Leafs nur ab mindestens 3 eigenständigen Beitragsintentionen;
- DataForSEO liefert konkrete Fragen, Keywords, Clustering und mögliche zusätzliche Leaf-Kandidaten;
- abschließend echter Browser-/Theme-Check, nicht nur interner Renderer.

### Erwartete Lücken im Pilot – vor DataForSEO

Buchbinden:
- Bestand deckt Einstieg, Ausrüstung, Material, Techniken/Praxis bereits ab;
- sicher fehlend: FAQ;
- Kosten innerhalb Ausrüstung prüfen;
- Vertiefung durch Techniken & Praxis bereits grundsätzlich abgedeckt.

Balance Board:
- Bestand: Board & Rolle, Grundbalance, Training & Sicherheit, Tricks & Übungen;
- ergänzen: Einstieg & Grundlagen, FAQ;
- Ausrüstung & Kosten separat prüfen;
- Vertiefung bereits durch Training/Tricks abgedeckt.

Glasmalerei:
- Bestand ist stark fachtechnisch;
- ergänzen: Einstieg & Grundlagen, FAQ;
- Ausrüstung & Kosten separat prüfen;
- Vertiefung durch Farben/Finish/Fixieren/Vorbereitung/Linien & Flächen abgedeckt.

Lasergravieren:
- Einstieg & Geräte ist vorhanden;
- ergänzen: FAQ;
- Kosten/Betrieb als separaten Bereich prüfen;
- Vertiefung durch Leistungs-/Qualitäts-/Material-Leafs vorhanden.

Fledermausbeobachtung:
- Einstieg & Arten vorhanden;
- ergänzen: FAQ;
- Ausrüstung & Kosten gegen Bat-Detector/Dokumentation abgrenzen;
- Orte & Saison bleibt eigener Fachbereich.

Hydrokultur:
- Einstieg & Systeme vorhanden;
- ergänzen: FAQ;
- Ausrüstung & Kosten gegen Blähton/Gefäße/Systeme abgrenzen;
- Vertiefung über Nährlösung, Pflege, Probleme vorhanden.

Riffaquaristik:
- Einstieg & System vorhanden;
- ergänzen: FAQ;
- Ausrüstung & Kosten als starker separater Kandidat;
- Vertiefung über Korallen, Licht/Strömung, Nährstoffe, Wasserwerte vorhanden.

Briefmarken sammeln:
- Einstieg & Sammelgebiete vorhanden;
- ergänzen: FAQ;
- Ausrüstung & Kosten gegen Aufbewahrung/Kaufen/Katalogisieren abgrenzen;
- Vertiefung über Bestimmen, Zustand, Echtheit, Wert vorhanden.

Geocaching:
- Einstieg & Cachetypen vorhanden;
- ergänzen: FAQ;
- Ausrüstung & Kosten gegen GPS & Apps abgrenzen;
- Vertiefung über Rätsel, Multis, eigene Caches/Regeln vorhanden.

Imkerei:
- Einstieg & Standort sowie Ausrüstung & Beute vorhanden;
- ergänzen: FAQ;
- Kosten/laufender Aufwand innerhalb oder neben Ausrüstung prüfen;
- Vertiefung über Völkerführung, Schwarm/Königin, Gesundheit/Winter, Ernte vorhanden.

## ZWEITE CORE-EBENE – KONKRETE 10ER-LÖSUNG ALS NÄCHSTES SOLL

### Fertigen

Aktuell bereits **10 sichtbare Mega-Menü-Zwischenkategorien**. Kein Merge nötig.

Der strukturelle Direktknoten Heimwerken bleibt als eigener World-Landingpage-/Hobbyknoten erhalten und ist kein zusätzlicher Mega-Menü-Zwischenbereich.

Die zuvor erwogene Zusammenlegung Metall + Schmuck wird deshalb **nicht** als Soll verfolgt.

### Technik

Aktuell 11 direkte Zielkinder.

Bevorzugte Korrektur:
- RC-Boote, RC-Flug & Drohnen, RC-Fahrzeuge zu **RC & Modelltechnik** als gemeinsame zweite Ebene bündeln;
- die heutigen RC-Hobby-Hubs direkt unter diesem gemeinsamen Ast behalten;
- keine zusätzliche Zwischenebene nur für die drei alten Gruppen;
- Ergebnis: Technik fällt von 11 auf 9 und besitzt noch einen freien Slot für spätere fachlich sinnvolle Erweiterung.

Diese beiden Änderungen sind das fachliche Soll für die nächste Simulation, noch kein Live-Write.
