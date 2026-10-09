# ZV-HOBBYRAUSCH-HD001-001 – INTEGRIERTE HOBBY-ARCHITEKTUR BIS FRONTEND

STAND: 2026-10-09
STATUS: AKTIV / FACHLICHE NEUAUSRICHTUNG DER CONTENT-EBENE
FASSUNG: 2.7
ERSETZT: Fassung 2.6 vom 2026-10-07; davor Fassung 2.5 / 2.4 / 2.3 / 2.2 / 2.1 / 2.0 vom 2026-10-07 und Fassung 1.0 vom 2026-10-03

## Geltungsbereich

HOBBYRAUSCH / SEO_KATEGORIEN / HD-001 Kategorie-Workflow.

## Verbindliches Endziel

Zentraler Hobbybestand
→ HOBBY_MASTER V2
→ Scope-/Identitäts-/Größen-/Rollenprüfung
→ integrierter 3-Säulen-Zielbaum
→ DataForSEO-SEO-Anreicherung
→ globale Intent-/Keyword-Ownership-Prüfung
→ WordPress/HivePress Soll/Ist-Sync
→ sichtbare Frontend-Navigation
→ Readback.

Kein bestehender produktiver Bestand darf dabei ungeprüft verloren gehen.

## Unveränderte Grundarchitektur

Drei Säulen:
- CORE = Hauptportal;
- EDITORIAL = Magazin;
- DIRECTORY = HivePress / Anbieter.

Acht geschützte Hauptwelten:
Gestalten · Fertigen · Technik · Forschen · Pflanzen · Tiere · Bewegen · Sammeln.

### Harte Ebenenregel

Die acht Hauptwelten sind die oberste fachliche CORE-Ebene.

`Hobbywelten` darf als Übersichts-/Einstiegsseite oder kuratierte View existieren, ist aber KEIN fachlicher Parent der acht Hauptwelten.

Falsch:
`Hobbywelten → Gestalten/Fertigen/…`

Richtig:
`Gestalten/Fertigen/…` = oberste CORE-Ebene;
`Hobbywelten` = zusätzliche Ansicht / Einstieg auf dieselben kanonischen Knoten.

Beliebte Hobbys, ungewöhnliche Hobbys, zuhause, günstig usw. sind ebenfalls Views/Filter/kuratierte Einstiege und erzeugen keine zweite Taxonomie.

## Geschäfts- und Portallogik

Hobby Depot ist weder reines Nischenportal noch beliebiges Hobby-Lexikon.

Portfolioziel:
- große bekannte Hobbys = wirtschaftliche Anker;
- mittlere Hobbys = stabiles Rückgrat;
- ungewöhnliche/Nischenhobbys = SEO-Longtail + Differenzierung.

Großer interner Bestand ist erlaubt.
Die globale Header-/Hauptnavigation bleibt bewusst klein. Die vollständigen aktiven Kindebenen innerhalb von Welt-, Zwischenbereich- und Hobbyseiten bleiben davon unberührt und müssen sichtbar sein.

Das Ziel ist NICHT „mehr Kategorien“, sondern für jedes Thema die richtige Ebene und Rolle.

## Portalgrenze und Rollen

Ein Kandidat wird fachlich geprüft auf:
- aktive/wiederholbare Freizeitpraxis;
- erlern-/vertiefbaren Tätigkeitsschwerpunkt;
- natürliche Passung zu einer der acht Welten;
- klare Identität/Aliaslage;
- beherrschbare Größe;
- Content Capacity;
- wirtschaftliche bzw. strategische Rolle.

Mögliche Rollen:
- ORIENTATION_UNIVERSE;
- HOBBY_HUB;
- EDITORIAL_TOPIC;
- ARTICLE_ONLY;
- FINDER_ONLY;
- OUT_OF_SCOPE.

Ein echtes Hobby außerhalb der natürlichen Acht-Welten-Passung wird als SCOPE_REVIEW behandelt. Es erzeugt nicht automatisch eine neue Hauptwelt.

## Größenvertrag

### Zweite CORE-Ebene / Mega-Menü

Aus optischen Gründen gilt für die direkten sichtbaren Kinder einer Hauptwelt eine **harte Obergrenze von 10**.

Verbindlich:
- pro Hauptwelt maximal 10 direkte sichtbare Kinder im Mega-Menü;
- keine künstliche Auffüllung bis 10;
- wenn mehr als 10 reale Kinder vorhanden sind, muss fachlich gruppiert oder ein breiter Knoten sinnvoll neu geordnet werden;
- die Begrenzung betrifft die Mega-Menü-/zweite CORE-Ebene, NICHT die unterste Content-Kategorieebene eines HOBBY_HUBs;
- vorhandene fachlich gute Hobby- und Content-Knoten dürfen nicht nur wegen dieser Grenze gelöscht werden.

Aktueller sichtbarer Mega-Menü-Prüfstand:
- Gestalten 7;
- Fertigen 10;
- Technik 11 → MUSS auf höchstens 10 neu geordnet werden;
- Forschen 5;
- Pflanzen 9;
- Tiere 7;
- Bewegen 8;
- Sammeln 8.

Wichtig:
Strukturelle Direktknoten wie Heimwerken oder Gärtnern können zusätzlich auf der jeweiligen Welt-Landingpage existieren, ohne als zusätzliche Mega-Menü-Zwischenkategorie zu zählen. Die 10er-Grenze ist eine Darstellungsgrenze des Mega-Menüs.

### Unterste Content-Kategorieebene

Für die letzte Ebene unter einem HOBBY_HUB gibt es **keine künstliche Gesamtobergrenze**.

Startregel:
- eine Content-Kategorie darf angelegt bzw. erhalten werden, wenn sie mindestens **3 eigenständige sinnvolle Beitragsintentionen** trägt;
- 3 = ausreichender Startbestand;
- 4+ = klar tragfähig;
- Synonyme/Formulierungsvarianten zählen nicht mehrfach;
- späteres Wachstum ist ausdrücklich erlaubt: Kategorien dürfen ergänzt, umbenannt, zusammengelegt oder geteilt werden;
- bestehende fachlich sinnvolle Kategorien bleiben unangetastet; neue Standardbereiche werden nur ergänzend hinzugefügt;
- nicht die Anzahl der Leafs entscheidet, sondern ihre eigenständige Nutzerfunktion und Content-Tragfähigkeit.

Ein HOBBY_HUB darf deshalb je nach Thema auch 7, 8, 9 oder mehr sinnvolle Content-Kategorien besitzen. Die frühere 3–6-Zielbegrenzung ist für die Produktionspraxis aufgehoben.

## Verbindliche universelle Nutzerbedürfnisse auf Hobby-Ebene

Jeder HOBBY_HUB wird aus zwei Perspektiven geprüft:
1. Mensch hört/kennt das Hobby kaum und braucht Orientierung zum Einstieg;
2. Mensch betreibt das Hobby bereits und sucht fachliche Vertiefung.

Daraus folgen vier universelle Prüffelder:

### 1. Einstieg & Grundlagen – Pflicht
Muss als sichtbare Content-Kategorie vorhanden sein.
Typische Inhalte:
- Was ist das Hobby?;
- Voraussetzungen;
- erste Schritte;
- Grundbegriffe;
- wie anfangen?;
- typische Anfängerfehler;
- Eignung / Schwierigkeitsgrad.

### 2. FAQ / Häufige Fragen – Pflicht
Muss als sichtbare Content-Kategorie vorhanden sein.
Abgrenzung:
- Einstieg enthält zusammenhängende erklärende Grundlagen;
- FAQ enthält konkrete eigenständige Frageintents;
- ein Intent besitzt nur einen primären Owner;
- DataForSEO/PAA/Longtails liefern und priorisieren konkrete Fragen.

### 3. Ausrüstung & Kosten – Standardpflicht
Wird als eigene Kategorie angelegt, sobald mindestens 3 eigenständige Beiträge möglich sind.
Typische Inhalte:
- Was brauche ich?;
- Grundausstattung;
- Kauf-/Auswahlfragen;
- Einsteigerbudget;
- laufende Kosten;
- günstige vs. hochwertige Optionen.
Wenn ein Hobby nachweislich keine drei eigenständigen Themen trägt, wird dieser Bereich mit Einstieg/Grundlagen zusammengeführt statt künstlich leer angelegt.

### 4. Praxis & Vertiefung – Pflicht als Nutzerabdeckung, nicht zwingend als zusätzlicher Leaf
Erfahrene Nutzer müssen einen sichtbaren Vertiefungspfad haben.
Wenn bestehende fachliche Kategorien dies bereits leisten (z. B. Training, Tricks & Übungen, Techniken, Projekte, Spezialmethoden), werden diese NICHT dupliziert.
Nur wenn mindestens 3 eigenständige vertiefende Intents übrig bleiben, entsteht zusätzlich eine eigene Kategorie wie Praxis & Vertiefung / Fachwissen.

## Hobbyspezifische Zusatzkategorien

Zusätzlich werden pro Hobby nur reale, passende Bereiche ergänzt. Mögliche Muster:
- Training;
- Übungen;
- Tricks;
- Techniken/Methoden;
- Sicherheit/Gefahren;
- Regeln;
- Herausforderungen;
- Pflege/Wartung;
- Fehler & Lösungen;
- Projekte/Ideen;
- Materialien;
- Orte/Touren;
- Wettbewerbe/Leistung;
- Sammeln/Bestimmen/Echtheit/Wert.

Regel:
**Sobald ein solcher Bereich mindestens 3 eigenständige sinnvolle Beitragsintentionen trägt und nicht bereits durch eine bestehende Kategorie abgedeckt ist, darf er als eigener Leaf bestehen.**

## Bestehende Kategorien bleiben erhalten

Die neue Regel ist ADDITIV.

Beispiel Balance Board:
bestehende Kategorien wie Board & Rolle, Grundbalance, Training & Sicherheit, Tricks & Übungen bleiben bestehen.
Neu ergänzt werden nur universelle Lücken wie Einstieg & Grundlagen, FAQ und ggf. Ausrüstung & Kosten.

Beispiel Buchbinden:
bestehende Kategorien Einstieg, Ausrüstung, Material, Techniken & Praxis bleiben bestehen.
Sie können universelle Prüffelder bereits erfüllen; fehlende Bereiche wie FAQ werden ergänzt, ohne Bestandskategorien zu ersetzen.

## Monetarisierung

Monetarisierung entscheidet NICHT über Behalten oder Löschen eines gültigen Hobbys.

Sie beeinflusst:
- CORE-Priorität;
- kommerzielle Tiefe;
- Sichtbarkeit;
- HivePress-Verknüpfung.

DIRECT / ASSISTED + ausreichende Contenttiefe
→ starker HOBBY_HUB-Kandidat.

NONE / UNKNOWN + SEO-/Inspirationswert
→ EDITORIAL_TOPIC / ARTICLE_ONLY / FINDER_ONLY.

Nicht monetarisierbare valide Themen bleiben erhalten.

## DataForSEO-Vertrag

DataForSEO ist KEINE Strukturautorität.

DataForSEO darf belegen bzw. auswählen:
- Nachfrageband;
- Primärkeyword;
- Synonyme;
- Longtail-Tiefe;
- Keyword-/Intent-Überschneidung;
- Suchnachfrage innerhalb fachlich bereits definierter Kandidaten.

DataForSEO darf NICHT selbst bestimmen:
- Hauptwelt;
- Parent oberhalb eines bereits feststehenden HOBBY_HUBs;
- structural_role;
- CORE-Promotion.

DataForSEO DARF auf der letzten Content-Ebene:
- konkrete FAQ-/Frageintents liefern;
- zusätzliche Leaf-Kandidaten unter einem bereits feststehenden HOBBY_HUB vorschlagen;
- mehrere Suchanfragen zu einem stabilen Themencluster bündeln;
- Bezeichnung, Primärkeyword, Nachfrage und Überschneidung eines Leaf-Kandidaten belegen.

Die endgültige Leaf-Entscheidung bleibt fachlich: mindestens 3 eigenständige Beitragsintentionen, klare Nutzerfunktion, keine Doppelung mit bestehenden Leafs.

Fachlogik bestimmt WAS ein Thema ist und WO es strukturell lebt.
SEO-Daten zeigen WIE VIEL Nachfrage/Intenttiefe dafür belegt ist.

### KISS-Regel für Content Capacity

Die Anzahl möglicher Artikel wird fachlich bestimmt.

Verbindlich:
- Fachlogik definiert die eigenständigen Nutzer-/Suchintents einer untersten Kategorie;
- diese fachlich unterschiedlichen Intents bilden die Content Capacity;
- DataForSEO reichert sie mit Nachfrage, Primärkeyword, Synonymen, Core Keyword und Intent-Überschneidung an;
- exaktes Core-Keyword-/Synonym-Evidence darf zwei fachlich vorgeschlagene Intents als Dublette zusammenführen;
- wenn DataForSEO für einen fachlich eigenständigen Longtail keine exakte Zeile liefert, bleiben dessen SEO-Metriken offen, aber der Artikelintent wird NICHT gelöscht;
- Keyword-Ideas-/Suggestions-Rohzeilen erzeugen umgekehrt niemals zusätzliche Artikelintents;
- automatische Keyword-Ideas-Tiefenrecherche ist kein Pflichtschritt des Normalwegs.

Kurz:
**Fachlogik zählt den möglichen Content; DataForSEO prüft und dedupliziert SEO-seitig.**

### PRAKTISCHE FINALISIERUNG – STARTFÄHIG STATT PERFEKT

Der Hobby-Master ist Inventar, nicht eine Aufforderung, jede denkbare Struktur vorab perfekt zu modellieren.

Verbindlicher Produktionsweg:
- bestehende fachlich sinnvolle Kategorien bleiben bestehen;
- pro HOBBY_HUB zuerst die universellen Lücken Einstieg & Grundlagen, FAQ, Ausrüstung & Kosten sowie der Vertiefungspfad prüfen;
- fehlende universelle Bereiche mit mindestens 3 eigenständigen Beitragsintentionen ergänzen;
- danach mit Fachlogik + DataForSEO nur die wirklich tragfähigen hobbiespezifischen Zusatzbereiche ergänzen;
- kein künstliches Zusammenpressen auf 3–6 Leafs;
- kein Warten auf einen vermeintlich endgültigen Zustand: Erweiterung/Umbenennung/Zusammenlegung bleibt Teil des Normalbetriebs;
- vor Massenausrollung zunächst ein repräsentativer Pilot aus 10 HOBBY_HUBs vollständig sichtbar im echten Frontend prüfen;
- erst nach diesem visuellen Pilot-PASS die restlichen Hubs in Batches ausrollen.

Beiträge eines HOBBY_HUBs liegen regulär unter genau einer sichtbaren Content-Kategorie.

## Strukturprinzip

Maximale Grundform des Hauptportals:
`WELT-SEITE → ZWISCHENBEREICH-SEITE → HOBBY-SEITE → CONTENT-KATEGORIE → BEITRÄGE`.

### Sichtbarkeitsregel – alle vorhandenen Ebenen sichtbar

Jede **tatsächlich vorhandene kanonische Ebene** muss beim normalen Durchklicken sichtbar und erreichbar sein:
- Weltseite zeigt ihre aktiven Zwischenbereiche vollständig;
- Zwischenbereich zeigt seine aktiven Hobby-Knoten vollständig;
- HOBBY_HUB zeigt seine aktiven Content-Kategorien vollständig;
- Content-Kategorie zeigt die zugeordneten Beiträge.

Es ist unzulässig, eine vorhandene Ebene im Frontend zu überspringen oder unsichtbar zu machen.

Die globale Header-/Hauptnavigation darf weiterhin klein und selektiv bleiben. "Kleine sichtbare Navigation" bedeutet **nicht**, dass untergeordnete Ebenen auf Welt-/Zwischenbereich-/Hobbyseiten verborgen werden dürfen.

### Breite und Ausgewogenheit

Für direkte sichtbare Kinder unter einer Hauptwelt gilt wegen des Mega-Menüs eine **harte Maximalzahl von 10**.

Verbindlich:
- 0–10 ist zulässig, wenn fachlich getragen;
- nicht künstlich auf 10 auffüllen;
- bei 11+ muss vor Ausrollung fachlich neu geordnet werden;
- echte fachliche Trennlinien bleiben wichtig, aber die Darstellung darf das Mega-Menü nicht sprengen;
- leere Zwischenbereiche bleiben verboten;
- diese 10er-Grenze gilt ausschließlich für die zweite CORE-/Mega-Menü-Ebene, nicht für Content-Leafs unter einem Hobby.

Nicht jeder Ast benötigt jede **maximale** Ebene; aber wenn ein Knoten als HOBBY_HUB geführt wird, gehört seine tragfähige Content-Kategorieebene zum sichtbaren Hub-Modell.
Keine Kategorie unter Kategorie.

Die V2-Rollenlogik liegt VOR dem Zielbaum:
`Rohliste → HOBBY_MASTER V2 → Bewertung → Zielbaum-Delta`.

Der vorhandene V1.12-Zielbaum ist Baseline, aber nicht automatisch finaler Installationsbaum.

## Integration der drei Säulen

Alle drei Säulen verwenden dieselbe stabile Themen-/Hobbyidentität.

CORE:
systematischer Hobby-Hub / Orientierung.

EDITORIAL:
Inspiration, kleine Themen, Longtails, Situationen, Vergleiche.

DIRECTORY:
Anbieter-, Kurs-, Vereins-, Werkstatt-, Shop- und Service-Intents.

Ein Thema darf in mehreren Säulen referenziert werden, aber pro primärem Suchintent gibt es genau EINEN SEO-Owner.

Keine Säule baut eine konkurrierende Kopie desselben Hobbys.

## Flexible Änderungen

Stable identity = `hobby_id/node_id`.

Unterstützt werden:
- Add;
- Rename;
- Move;
- Merge/Alias;
- Archive/Demotion;
- spätere Promotion.

Bestehende IDs bleiben bei gleicher Objektidentität erhalten.
Kein Hard-Delete als Normalweg.

## WordPress- und Frontend-Ziel

Erfolg bedeutet:
- korrekte Seiten und Taxonomien;
- korrekte Parent-/Child-Beziehungen;
- veröffentlichter Zielbestand nur nach vollständiger Prüfung;
- sichtbare Frontend-Navigation;
- acht Hauptwelten auf oberster CORE-Ebene;
- keine zweite Hobbywelten-Parentebene;
- korrekte Magazin-/HivePress-Integration;
- Readback des WordPress- und Frontend-Endzustands.

Aktive Revision erst nach vollständigem Write + Readback umschalten.

## Harte Abnahme

Kein Ziel-PASS ohne:
- vollständige lokale POSITIVE UND NEGATIVE E2E-Simulation;
- realen relevanten Request-/Admin-/Resume-Pfad;
- Idempotenz;
- Drift-Erkennung;
- Rollback;
- Add/Move/Rename/Merge/Archive;
- Alias-/Dublettenprüfung;
- Cross-Pillar Keyword-/Intent-Kannibalisierung;
- Schutz nicht monetarisierbarer valider Themen;
- Nachweis, dass DataForSEO keine Struktur erzeugt/verschiebt;
- Nachweis der obersten Acht-Welten-Ebene;
- WordPress-/Frontend-Readback.

Lokaler PASS ist kein Live-PASS.
Live-PASS erst nach echtem produktivem WordPress-/Frontend-Readback.

## Aktuelle Integrationsgrenze

Die acht Welten und die bestehende Zwischenstruktur werden im ersten V2-Integrationslauf geschützt.
Zuerst wird der HOBBY_MASTER bewertet.
Erst danach wird ein begründetes Delta zum V1.12-Zielbaum erzeugt.

Keine direkte WordPress-Synchronisierung aus einem unbewerteten Master.


## Magazin – eigenständige flexible Editorial-Struktur

Das Magazin ist NICHT an die 10er-Grenze des Mega-Menüs gebunden. Der Einstieg erfolgt primär über Kacheln, organische Suche und thematische Einstiege.

Ziel:
- valide Themen erhalten, die nicht in den CORE-Zielbaum gehören;
- Inspiration, Information, Longtails und redaktionelle Suchintentionen abdecken;
- ungewöhnliche/schräge Themen wie Treibholz sammeln nicht löschen, sondern redaktionell verwerten;
- keine konkurrierenden Kopien von CORE-Hobbyseiten erzeugen.

Startfähige Magazin-Kachelstruktur:
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

Diese Struktur ist bewusst erweiterbar und besitzt keine starre Obergrenze.

Hobbyfinder bleibt Werkzeug/Orientierung und kann in mehrere redaktionelle Einstiege verlinkt werden.
Situations-, Saison-, Alters-, Budget- oder Platzmerkmale dürfen zusätzlich als Views/Filter verwendet werden, ohne doppelte SEO-Owner zu erzeugen.

## Startregel ab Fassung 2.7

Nicht mehr auf Vollkommenheit warten.

Reihenfolge:
1. sichtbare Mega-Menü-Zwischenkategorien auf maximal 10 je Welt bringen; aktuell muss nur Technik von 11 reduziert werden;
2. vorhandene Hobby-Leafs einfrieren, nicht ersetzen;
3. 10 repräsentative Hobbys nach der neuen universell+individuell-Regel ergänzen;
4. DataForSEO für konkrete Fragen, Keywords und zusätzliche Leaf-Kandidaten verwenden;
5. echten Browser-/Theme-Ausgabepfad visuell prüfen;
6. Regel ggf. einmal korrigieren;
7. dann restliche HOBBY_HUBs ausrollen;
8. Magazin parallel nach dem flexiblen Kachelmodell aufbauen.

