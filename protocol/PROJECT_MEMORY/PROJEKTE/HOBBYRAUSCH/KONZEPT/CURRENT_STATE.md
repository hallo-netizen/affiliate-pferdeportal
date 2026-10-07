# HOBBYRAUSCH – KONZEPT – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-07
STATUS: 3-SÄULEN-GRUNDKONZEPT FEST / V2-REGELN 1.4 KISS / ECHTE DATAFORSEO-EVIDENCE VORHANDEN / V1.12.5 GESAMTPFAD LOKAL HARD PASS / EINMALIGER LIVE-READBACK OFFEN

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

Batch 001 bestätigt:
- ID-Eindeutigkeit funktioniert;
- vier aktuelle Alias-/Kanonikbindungen bleiben stabil;
- zwölf Kandidaten benötigen noch semantische Identitäts-/Unterformprüfung;
- Monetarisierung erzeugt keine automatische CORE-Promotion;
- der Hauptengpass ist jetzt der echte DataForSEO-Abgleich der vorgeschlagenen Artikelintents plus Ownership; die Regeldefinition ist nachgezogen.

## Nachprüfung gegen das vollständige Konzept

Nachgezogen:
- nicht die Gesamtzahl eines Hobbys zählt, sondern jede unterste Kategorie einzeln;
- Ziel pro unterster Kategorie: 5–12 eigenständige Artikelintents;
- kleine valide Hobbys dürfen in stärkeren Übersichts-/Leaf-/Magazinstrukturen zusammengefasst werden, ohne ihre Hobby-Identität zu verlieren;
- neue Zwischenkategorien werden erst im späteren Gesamt-Delta gebaut;
- Fachlogik definiert und zählt die eigenständigen Artikelintents; DataForSEO validiert Nachfrage, Synonyme, Core-Keywords und Intent-Überschneidung, kann Dubletten zusammenführen, erzeugt aber weder Struktur noch zusätzliche Artikelintents und löscht keinen fachlich eigenständigen Intent nur wegen einer fehlenden exakten Longtail-Zeile.

Konzeptaudit:
`../SEO_KATEGORIEN/HOBBY_MASTER_V2_CONCEPT_AUDIT_20261007.md`

## Reales Batch-001-Ergebnis

Der erste echte WordPress-/DataForSEO-Lauf ist erfolgt.

Ergebnis:
- 263 fachlich vorgeschlagene Artikelintents;
- 106 exakte Keyword-Overview-Zeilen von DataForSEO;
- 157 exakte Seeds ohne Overview-Zeile;
- 0 Strukturwrites.

Wichtig:
Die 157 fehlenden Zeilen sind KEIN Beweis, dass diese Inhalte nicht existieren.
Nach Regelvertrag 1.2 ist der exakte Overview nur eine Evidenzstufe.
Die noch offenen, bereits fachlich definierten Leaf-/Themenräume müssen anschließend mit Keyword Ideas/Suggestions auf echte Intenttiefe geprüft werden.

Daraus folgt:
Das Zwischenresultat `0 Hub-Kandidaten` darf nicht als endgültige Portalentscheidung verwendet werden.

HD-001 V1.12.3 setzt genau diese fehlende zweite Evidenzstufe timeout-sicher um:
37 offene Cluster → 37 Keyword-Ideas-Aufrufe → 1 abschließender gebündelter Overview → erneute Zählung/Dedupe/Ownership.

Keine Struktur wird dabei erzeugt.

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

## Pilotbefund

- Buchbinden → bestehender Live-/Technikpilot bleibt stabil; endgültiger V2-HOBBY_HUB-PASS ist wegen der strengeren 5–12-pro-Leaf-Regel wieder offen;
- Fotografie → Macro-/Orientation-Prüfung statt Riesenhub;
- Garten → kein einzelner Vollhub;
- Treibholz sammeln → EDITORIAL erhalten, kein unbelegter CORE-Hub;
- Musizieren → Scope-Review statt erzwungener Weltzuordnung.

## Autoritative Konzeptdateien

- `HOBBY_GROESSEN_ROLLENMODELL_20261007.md`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_INTEGRATION_20261007.md`
- `../SEO_KATEGORIEN/HOBBY_MASTER_V2_PILOT_20261007.md`

## Technische Abgrenzung

Pluginversionen, technische Release-/Teststände und Live-Status ausschließlich aus:
- `PLUGINS/PLUGIN_AKTEN/HD-001-KATEGORIE-WORKFLOW/CURRENT.md`;
- `SEO_KATEGORIEN/CURRENT_STATE.md`.

## Erster offener Blocker

`HD001_V2_BATCH001_V125_SINGLE_LIVE_READBACK_PENDING`

Kein weiterer Research-/DataForSEO-Schritt ist offen.

Der komplette Batch-001-Pfad ist gegen das Konzept lokal bis zum Endergebnis geprüft.

## EXAKT EINE NEXT ACTION

Einmal HD-001 V1.12.5 in Hobby Depot installieren und `Kategorien → V2-Hobbybewertung` öffnen.

Das vorhandene Ergebnis wird ohne Provider-Aufruf nach Regelvertrag 1.4 neu berechnet.

Danach das Ergebnis-JSON einmal readback-prüfen.

Noch NICHT:
- Zielbaum synchronisieren;
- Kategorien schreiben;
- neue Keyword-Ideas-Recherche starten.
