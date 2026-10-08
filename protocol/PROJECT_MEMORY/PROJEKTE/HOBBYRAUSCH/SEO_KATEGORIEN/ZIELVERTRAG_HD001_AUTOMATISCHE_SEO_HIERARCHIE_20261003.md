# ZV-HOBBYRAUSCH-HD001-001 – INTEGRIERTE HOBBY-ARCHITEKTUR BIS FRONTEND

STAND: 2026-10-07
STATUS: AKTIV
FASSUNG: 2.6
ERSETZT: Fassung 2.5 vom 2026-10-07; davor Fassung 2.4 / 2.3 / 2.2 / 2.1 / 2.0 vom 2026-10-07 und Fassung 1.0 vom 2026-10-03

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

Leaf-Kategorie:
- unter 4 tragfähige Beitragsintentionen: zusammenlegen / keine eigene Kategorie;
- 4: Grenzfall, nur begründete Ausnahme;
- 5–12: idealer Zielbereich;
- 13–14: oberhalb des Idealbereichs; keine automatische Teilung;
- ab etwa 15: prüfen, ob zwei echte Themenbereiche entstehen; nur dann teilen.

Hobby-Hub:
- <3 tragfähige Leafs: Hub kritisch prüfen;
- 3–6: typischer Zielbereich;
- 7–9: oberhalb des typischen Bereichs; prüfen, aber nicht automatisch zerlegen;
- ab etwa 10 eigenständigen Unterbereichen: Macro-/Split-Prüfung.

Die Zahlen sind Prüfgrenzen, keine Aufforderung zu künstlicher Symmetrie.

## Verbindliche Leaf-Kapazität und Zusammenfassung

Die Content-Capacity wird NICHT nur für ein Hobby insgesamt geprüft.

Jede unterste Kategorie muss separat tragfähig sein:
- unter 4 eigenständige Beitragsintentionen: zusammenlegen / keine eigene Leaf-Kategorie;
- 4: Grenzfall;
- 5–12: idealer Zielbereich;
- 13–14: oberhalb des Idealbereichs; keine automatische Teilung;
- ab etwa 15: Teilung prüfen; nur bei echter fachlicher Trennlinie teilen.

Ein Beitrag zählt nur bei eigenständigem Nutzer-/Suchintent.
Synonyme und bloße Formulierungsvarianten zählen nicht mehrfach.

Kleine valide Hobbys bleiben als eigene kanonische Identitäten erhalten.
Wenn sie allein keine tragfähige Struktur besitzen, dürfen sie über fachlich passende:
- Übersichts-/Parentseiten;
- gemeinsame Leaf-Kategorien;
- redaktionelle Cluster

zusammen sichtbar gemacht werden.

Diese Zusammenfassung darf die Hobby-Identitäten nicht verschmelzen.
Neue strukturelle Gruppen werden erst im späteren Gesamt-Zielbaum-Delta erzeugt, wenn der bewertete Gesamtbestand sie belegt.

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
- Parent;
- structural_role;
- neue Zwischenkategorie;
- Promotion eines Themas in CORE.

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

### PRAKTISCHE FINALISIERUNG – Baseline statt 841 Einzelprüfungen

Der 841er Hobby-Master ist **Inventar**, nicht eine Liste von 841 zwingend anzulegenden CORE-Kategorien.

Verbindliche Produktionsregel:
- bestehende V1.12-Zielbasis bleibt Ausgangspunkt: 95 Strukturknoten + 329 explizite CORE-Hobby-Zuordnungen;
- nicht explizit freigegebene Master-Identitäten bleiben durch `retain_editorial` im Finder/Editorial erhalten;
- ein **HOBBY_HUB** besitzt vor regulärer Artikelproduktion eine sichtbare Content-Kategorieebene;
- Zielbereich eines HOBBY_HUBs sind **3–6 tragfähige Content-Kategorien**; 7–9 = Review, ab etwa 10 = Macro-/Split-Review;
- jede Content-Kategorie muss selbst den Leaf-Vertrag erfüllen: ideal **5–12 eigenständige Beitragsintentionen**; 0–3 = keine eigene Kategorie, 4 = Grenzfall, 13–14 = Review, ab etwa 15 = Split-Prüfung;
- Beiträge eines HOBBY_HUBs werden regulär **nicht direkt unter dem Hobby** abgelegt, sondern genau einer sichtbaren Content-Kategorie zugeordnet;
- direkte Beiträge ohne Content-Kategorie sind nur für ausdrücklich dafür vorgesehene Rollen/Einzelfälle zulässig, insbesondere ARTICLE_ONLY/EDITORIAL, nicht als Normalmodell eines HOBBY_HUBs;
- DataForSEO wird nur noch bei echten Promotions-/Demotions-/Ownership-Grenzfällen eingesetzt;
- die 16er-Batchschleife endet mit Batch 003 und ist kein Produktionsmodell;
- Abschlussweg: globaler Baseline-/Alias-/Override-Audit → genau ein Zielbaum-Delta → ein kontrollierter WordPress-Sync → Frontend-Readback → Plugin kann entfernt werden.

Damit gilt die Qualitätsregel für unterste Kategorien wieder als Bestandteil eines HOBBY_HUBs. Die frühere KISS-Ausnahme "CORE-Hobby darf regulär Beiträge direkt enthalten" ist für HOBBY_HUBs aufgehoben.

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

Für direkte Zwischenbereiche unter einer Welt gibt es **keine starre künstliche Maximalzahl**.
Bis zu etwa **10–11 fachlich klare Punkte** auf dieser Ebene sind ausdrücklich zulässig, wenn der reale Bestand sie trägt.

Verbindlich:
- nicht künstlich zusammenziehen, nur um die Navigation dünn zu halten;
- nicht künstlich auffüllen, nur um Symmetrie zu erzeugen;
- deutlich dünne oder deutlich überbreite Welten werden fachlich auf Ausgewogenheit geprüft;
- echte fachliche Trennlinien haben Vorrang vor einer möglichst kleinen Anzahl von Menüpunkten;
- leere Zwischenbereiche bleiben verboten.

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
