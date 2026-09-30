# HOBBY DEPOT – KONZEPT-ZWISCHENSTAND KATEGORIEN & INTERNE SUCHE

STAND: 2026-09-30
STATUS: BRAINSTORMING KONSOLIDIERT / HAUPTKATEGORIEN NOCH OFFEN / KEINE TECHNISCHE FREIGABE

## 1. Zweck dieses Dokuments

Dieses Dokument hält den aktuellen konzeptionellen Zwischenstand fest, damit die im Brainstorming erarbeiteten Ideen nicht verloren gehen.

Es ist **keine finale Taxonomie** und **kein technischer Umsetzungsvertrag**.

Die historischen Vorarbeiten in `VORARBEITEN_HOBBYFINDER/` bleiben erhalten. Dieses Dokument konsolidiert die neueren Überlegungen für den aktuellen Markenstand **Hobby Depot**.

---

## 2. Portal-Grundidee bleibt unverändert

Hobby Depot soll zwei Nutzergruppen gleichzeitig bedienen:

### A. Menschen, die ihr Hobby bereits kennen
Sie suchen typischerweise:
- das konkrete Hobby;
- Fachbegriffe;
- Techniken;
- Zubehör;
- Ausrüstung;
- Produkte;
- Probleme und konkrete Fragen.

Beispiele:
- `Buchbinden`
- `Bonsai drahten`
- `RC Crawler Reifen`
- `Aquascaping Beleuchtung`

Diese Nutzer sollen primär über:
- konkrete Hobbyseiten;
- Kategorien;
- Beiträge / Magazinbeiträge;
- Anzeigen;
- normale interne Suche

abgeholt werden.

### B. Menschen, die noch kein konkretes Hobby kennen
Sie suchen eher nach einer Tätigkeit, Stimmung, Situation oder groben Wunschrichtung.

Beispiele:
- „Ich möchte etwas mit den Händen machen.“
- „Ich will etwas Ruhiges.“
- „Ich möchte draußen etwas entdecken.“
- „Ich möchte tüfteln.“
- „Ich suche etwas, das ich alleine machen kann.“

Für diese Nutzer soll zusätzlich eine **interne semantische Hobby-Finder-Funktion** entstehen.

Wichtig:
Diese Funktion ist **nur interne Benutzerführung**.
Sie soll **keine zusätzliche SEO-Taxonomie** und **keine externe Google-SEO-Strategie** ersetzen.

---

## 3. SEO nach außen bleibt getrennt

Externe Suchintentionen werden weiterhin durch echte Inhalte abgedeckt:

- Haupt-/Hobbyseiten;
- Kategorien;
- Beiträge;
- Magazin;
- Longtail-Beiträge;
- ggf. SEO-Landingpages.

Beispiel:
Wenn `Bonsai drahten` ein relevanter Suchbegriff ist, wird dafür ein echter Beitrag oder geeigneter Inhalt produziert.

Die interne semantische Suche soll **nicht dieselben Themen künstlich doppelt abbilden**.

Grundregel:

> Gibt es für eine Anfrage bereits einen starken direkten Treffer aus Seite, Kategorie, Beitrag oder Anzeige, gewinnt der normale Suchtreffer.

Die semantische Hobby-Finder-Ebene springt nur dort ein, wo die Anfrage **unscharf, bedürfnisorientiert oder nicht durch konkrete Inhalte abgedeckt** ist.

---

## 4. Semantische Hobby-Finder-Ebene

### Ziel

Nicht unendlich viele einzelne Suchphrasen pflegen, sondern wenige **Themen-/Bedeutungsfamilien**.

Beispielhafte Familie:

### Themenfamilie: „mit den Händen arbeiten / etwas herstellen“

Mögliche sprachliche Ausprägungen:
- mit den Händen arbeiten
- etwas selber machen
- etwas herstellen
- etwas bauen
- etwas erschaffen
- handwerklich
- werkeln
- machen

Diese Familie kann mit passenden Hobbys verknüpft werden, z. B.:
- Buchbinden
- Schnitzen
- Lederarbeiten
- Töpfern
- Korbflechten

Der Nutzer muss nicht exakt einen hinterlegten Satz treffen.
Die Suchlogik soll die Aussage möglichst einer Themenfamilie zuordnen.

### Weitere mögliche Familien
Noch **nicht final**, nur Beispiele:
- ruhig / entspannend / konzentriert
- draußen / Natur
- beobachten / erforschen
- Technik / tüfteln
- Bewegung / körperlich
- sammeln / ordnen / finden
- allein / zu zweit / Gruppe
- wenig Platz / zuhause
- etwas erschaffen / herstellen

---

## 5. Direkttreffer verdrängen semantische Fallbacks

Es soll **keine sichtbare Doppelung** entstehen.

Beispiel:

Heute existiert kein eigener Inhalt zu:
`Hobbys mit den Händen`

Dann darf die semantische Hobby-Finder-Ebene passende Hobbys vorschlagen.

Später entsteht ein echter Beitrag:
`Hobbys, bei denen man mit den Händen arbeitet`

Dann soll dieser echte Inhalt bei passender Suche Vorrang haben.

Die semantische Zuordnung muss dafür nicht gelöscht werden.
Sie kann intern erhalten bleiben und wird für diese Anfrage **automatisch stummgeschaltet / verdrängt**, solange ein hinreichend starker direkter Inhalt existiert.

Vorteil:
Wird der direkte Inhalt später entfernt oder umbenannt, kann der semantische Fallback wieder greifen, ohne dass Zuordnungen neu aufgebaut werden müssen.

---

## 6. Denkbare Datenstruktur im Hintergrund

Noch **kein finaler Technikentscheid**.

Für jede relevante Hobbyseite / Kategorie könnte eine interne Zuordnung existieren, etwa:

- kanonischer Hobbybegriff;
- starke Synonyme;
- Themenfamilien;
- grobe Eigenschaften;
- semantische Begriffe;
- optionale SEO-Recherche-Hinweise.

Beispiel `Buchbinden`:
- kanonisch: Buchbinden
- Synonyme: Bücher binden
- Themenfamilien: mit Händen arbeiten / herstellen / Papier
- Eigenschaften: ruhig / drinnen / allein möglich

Diese Daten sollen nicht automatisch neue öffentliche Kategorien oder indexierbare Seiten erzeugen.

---

## 7. Rolle von DataForSEO

DataForSEO kann bei der Kategorien-/Keyword-Recherche zusätzliche sprachliche Varianten oder Suchmuster hochspülen.

Diese sollen **nicht automatisch als Tausende einzelne interne Suchbegriffe** übernommen werden.

Stattdessen:
1. prüfen, ob der Begriff durch echten Inhalt abgedeckt wird;
2. falls nein, prüfen, ob er in eine bestehende Themenfamilie passt;
3. nur bei wirklich neuer Bedeutung ggf. neue Familie anlegen;
4. Zuordnung später jederzeit ergänzbar oder korrigierbar halten.

Damit bleibt die interne Suche flexibel und wächst mit dem Portal.

---

## 8. Denkbare Einbindung in die bestehende Suche

Die aktuelle Pferde-Atelier-Suche dient als Funktionsvorbild:
- ANZEIGEN
- KATEGORIEN
- BEITRÄGE

Für Hobby Depot könnte später zusätzlich eine Gruppe wie:

- PASSENDE HOBBYS
- HOBBY-IDEEN
- PASSENDE THEMEN

eingeblendet werden.

Wichtig:
Diese zusätzliche Gruppe soll nur dann erscheinen, wenn sie einen echten Mehrwert liefert, insbesondere bei unscharfen oder bedürfnisorientierten Anfragen.

Bei einem klaren Suchbegriff wie `Buchbinden` soll nicht künstlich eine Hobbyberatung vor den direkten Treffern erscheinen.

---

## 9. Technische Rollen – aktueller Denkstand

Noch nicht final beschlossen.

Aktuell sinnvoll erscheint folgende Trennung:

### Kategorie-Workflow
Kann beim Aufbau der Portalstruktur:
- SEO-/Themenbegriffe sammeln;
- potenzielle Themenfamilien erkennen;
- Hobbyseiten/Kategorien mit semantischen Hinweisen vorbereiten.

### WordPress / persistente Metadaten
Die semantischen Zuordnungen sollten dauerhaft an den realen Seiten/Kategorien bzw. in einer stabilen zentralen Struktur gespeichert werden.

Sie dürfen nicht verschwinden, wenn das schwere Aufbau-/Kategorie-Plugin später deaktiviert wird.

### Suche
Die Suchfunktion wertet die gespeicherten Zuordnungen aus und entscheidet:
- direkter Treffer vorhanden → direkter Treffer hat Vorrang;
- echte Suchlücke / unscharfe Anfrage → semantische Hobby-Vorschläge ergänzen.

### Design
Das Design entscheidet nur über Darstellung und Gruppierung der Ergebnisse.
Es soll nicht die fachliche Zuordnung von Begriffen zu Hobbys bestimmen.

Ein eigenes neues Groß-Plugin ist **nicht automatisch erforderlich**.
Die genaue technische Heimat wird erst entschieden, wenn die fachliche Logik feststeht.

---

## 10. Hauptkategorien – aktueller Denkstand

Die Hauptnavigation hat ungefähr **6–8 verfügbare Slots**.

Anforderungen:
- sehr kurze Begriffe;
- optisch möglichst ausgewogen;
- sofort verständlich;
- klare Abgrenzung;
- möglichst geringe Schnittmengen auf der obersten Ebene;
- ausreichend breite Unterstruktur;
- nach unten langfristig erweiterbar;
- Begriffe sollen Charakter haben und nicht wie eine trockene Verwaltungs-Taxonomie wirken.

### Wichtig: Magazin zählt nicht zu diesen Slots
Das Magazin ist ein eigener SEO-/Inspirationskanal.

Dort kann ausdrücklich eine Rubrik für:
- exotische Hobbys;
- ungewöhnliche Hobbys;
- neue / schräge Hobby-Ideen

geführt werden.

Die gespeicherte Hobby-Rohliste mit besonders ungewöhnlichen Kandidaten bleibt dafür wertvoll.

---

## 11. Bisher diskutierte Begriffe / Bewertung

### Begriffe mit Potenzial

**Machen**
- sympathisch;
- breit;
- passt zu „mit Händen etwas tun / herstellen“;
- Problem: semantisch sehr breit;
- kann möglicherweise `Gestalten` als Unterwelt aufnehmen.

**Tüfteln**
- charaktervoll;
- verständlich für Technik-/Bau-/Optimierungs-Hobbys;
- Problem: möglicherweise kein starker externer SEO-Begriff;
- externe SEO-Bezeichnung der Zielseite muss nicht identisch mit Menübezeichnung sein.

**Forschen**
- besser und präziser als `Entdecken` für Astronomie, Mikroskopie, Wetter, Beobachtung, Analyse usw.;
- klare Erkenntnisorientierung;
- Abgrenzung zu `Suchen` muss im finalen Modell noch geprüft werden.

**Bewegen**
- verständlich als Tätigkeit;
- Abgrenzung zu `Sport` noch nicht endgültig bewertet;
- soll nicht automatisch alle Outdoor-/Abenteuerhobbys schlucken.

**Sammeln**
- stark und verständlich;
- relativ klare Hobbyfamilie.

**Gestalten**
- charaktervoll;
- aber enger als zunächst angenommen;
- passt stark zu Design, Form, Farbe, Ausdruck;
- Buchbinden, Schmieden, Lederarbeiten usw. fühlen sich darunter nicht selbstverständlich an.

### Begriffe mit deutlichen Problemen

**Handwerk**
- bewusst problematisch;
- zu stark mit klassischen Gewerken/Berufen wie Tischler, Dachdecker, Maurer usw. assoziiert;
- soll voraussichtlich **nicht** als sichtbare Hauptkategorie verwendet werden;
- kann aber intern als semantischer Suchbegriff wertvoll sein.

**Werken**
- wirkt schnell wie Schulfach, Holzwerken oder Heimwerken;
- aktuell kein Favorit.

**Pflegen**
- zu mehrdeutig;
- Assoziationen zu Körper-/Menschen-/Haushaltspflege;
- für Bonsai/Aquaristik/Terraristik nicht eindeutig genug.

**Entdecken**
- charmant, aber zu offen;
- kann Reisen, Abenteuer, Orte oder „neue Hobbys entdecken“ bedeuten;
- als harte Hauptkategorie derzeit eher zu unpräzise.

**Spiele**
- echte Hobbywelt, aber als knapper Hauptslot wahrscheinlich zu eng bzw. strukturell wenig variantenreich;
- Gefahr, in ein eigenes Brett-/Kartenspielportal abzudriften;
- aktuell kein Favorit für die oberste Navigation.

**Hobbys**
- als Hauptslot neben anderen Welten zu allgemein;
- wirkt wie zweite Startseite / Obermenge aller übrigen Kategorien.

**Außergewöhnlich / Exotisch**
- stark für Magazin/SEO/Startseiten-Inspiration;
- als Hauptkategorie ungeeignet, weil es eine Eigenschaft quer zu allen Hobbyfamilien ist.

---

## 12. Zentrale Erkenntnis zur Kategorienlogik

Die sichtbare Hauptnavigation muss **nicht alle denkbaren Begriffe und Nutzerformulierungen abbilden**.

Die semantische Hobby-Finder-Schicht kann Begriffe auffangen, die nicht sinnvoll als Hauptkategorie taugen.

Beispiel:
`Handwerk` muss nicht oben sichtbar sein.
Wer intern nach `Handwerk`, `mit den Händen arbeiten` oder `etwas herstellen` sucht, kann trotzdem passende Hobbys bekommen.

Dadurch wird die Hauptnavigation von dem Zwang entlastet, jede menschliche Formulierung als sichtbare Kategorie abzubilden.

---

## 13. Noch offene Hauptfrage

Die endgültigen **6–8 Hauptkategorien** sind weiterhin offen.

Noch zu klären:
- einheitliches sprachliches Prinzip: Verben, Substantive oder bewusst gemischt;
- klare Grenze zwischen `Machen` und möglichen kreativen/gestalterischen Unterwelten;
- Begriff für Hobbys rund um Tiere, Pflanzen, Aquaristik, Terraristik, Zucht, lebende Systeme;
- genaue Rolle von `Forschen`;
- genaue Rolle von `Bewegen`;
- ob eine weitere eigenständige Hobbyfamilie fehlt;
- ob 6, 7 oder 8 Slots tatsächlich gebraucht werden.

Keine Kategorie soll nur deshalb ergänzt werden, um einen freien Menüslot zu füllen.

---

## 14. Nächster konzeptioneller Arbeitsschritt

Weiter ausschließlich an der **Begrifflichkeit und Abgrenzung der Hauptkategorien** arbeiten.

Noch keine technische Umsetzung der semantischen Suche.
Noch keine finale Kategorie-Taxonomie.
Noch keine automatische Übernahme von Rohliste-Zwischenüberschriften.

Ziel des nächsten Schritts:
Eine kleine Zahl sehr klarer, charaktervoller und gegeneinander belastbar abgegrenzter Hauptwelten finden, bevor die gespeicherte Hobby-Rohliste systematisch dagegen getestet wird.
