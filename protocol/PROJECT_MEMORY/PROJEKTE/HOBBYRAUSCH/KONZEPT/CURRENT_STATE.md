# HOBBYRAUSCH – KONZEPT – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-08
STATUS: REGELN 2.6/1.6 FEST / FACH-SOLLPROFIL PASS / 359 CURRENT-CORE VOLLSTÄNDIG REVALIDIERT / 279 HOBBY_HUB / 1.292 CONTENT-KATEGORIEN / KEIN OFFENER KONZEPT-BLOCKER / OPERATIVE FORTSETZUNG ÜBER SEO_KATEGORIEN-CURRENT

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

## Aktueller Strukturstand nach Gesamtprüfung

Regeln 2.6/1.6 sind bereinigt und widerspruchsfrei.

Welt-/Zwischenstruktur:
`../SEO_KATEGORIEN/HD001_BALANCED_WORLD_INTERMEDIATE_TARGET_20261008.json`

Aktuelle CORE-Rollenabdeckung:
- 359 CORE;
- 60 aktuell produktionsgültig bewertet durch Batch 001–003 + Expansion19;
- 299 benötigen globalen Recheck nach 1.6;
- Batch 004–019 bleiben historische Evidence, nicht Produktionsautorität.

## Aktueller Recheck-Stand

- 359 aktuelle CORE-Identitäten;
- 161 nach Regel 1.6 entschieden;
- 75 historische aktuelle HOBBY_HUBs mit 355 sichtbaren Content-Kategorien nachgezogen;
- 198 aktuelle CORE-Identitäten noch offen.

## Fachlicher Endstand Kategorienstruktur

Abschluss:
- 359/359 aktuelle CORE-Identitäten nach Regeln 1.6 entschieden;
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

## Erster offener Blocker

KEIN OFFENER KONZEPT-BLOCKER.

Die technische/operative Fortsetzung gehört ausschließlich zur zuständigen Fach-Current:
`../SEO_KATEGORIEN/CURRENT_STATE.md`

## EXAKT EINE NEXT ACTION

Für jede weitere Kategorie-/WordPress-Arbeit zu
`../SEO_KATEGORIEN/CURRENT_STATE.md`
wechseln, dort Frischecheck durchführen und ausschließlich deren NEXT ACTION ausführen.

Keine neue Konzept- oder Kategorieregel erfinden.
