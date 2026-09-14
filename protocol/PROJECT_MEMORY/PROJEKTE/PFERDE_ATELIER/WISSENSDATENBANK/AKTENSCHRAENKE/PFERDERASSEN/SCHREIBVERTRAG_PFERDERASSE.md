# SCHREIBVERTRAG PFERDERASSE

STAND: 2026-09-14
STATUS: VERBINDLICH FÜR CHAT-ERSTELLUNG / EIGENSTÄNDIGE BEITRAGSART

## HARTE SYSTEMGRENZE
Dieser Vertrag ist die einzige Textautorität für Pferderassen-Artikel.

Es gilt ausschließlich:
`freigegebener Rassendatensatz -> dieser Schreibvertrag -> Artikel -> Pferderassen-Manager-JSON`

**TABU:** Regeln, Prompts, Keywordsysteme, Prüfungen oder Abläufe aus TEXT/Textmaschine, ACM, PPM, LT oder anderen Artikel-Workflows dürfen weder gelesen noch übernommen noch sinngemäß angewendet werden.

## ZWECK
Der Schreiber darf formulieren, aber nicht entscheiden.

**Kernsatz 1:** Was nicht im freigegebenen Rassendatensatz steht, existiert für den Schreiber nicht.

**Kernsatz 2:** Textfreiheit besteht ausschließlich in Satzbau, Rhythmus und Wortwahl. Fakten, Struktur, Reihenfolge und Abschnittszweck sind nicht frei.

## 1. EINZIGE FAKTENQUELLE
- einzige Faktenquelle ist der freigegebene Datensatz unter `DATEN/breed-*.json`;
- keine eigene Webrecherche während des Schreibens;
- kein Weltwissen, keine Erinnerung, keine Ergänzung aus Plausibilität;
- `nicht_recherchiert`, `nicht_belegt`, `nicht_anwendbar`, `quellenkonflikt` dürfen nicht aufgefüllt oder umgedeutet werden;
- keine Ableitung aus Körperbau, Herkunft, Nutzung oder Typ, wenn die abgeleitete Aussage nicht selbst belegt ist.

## 2. H1-/TITEL-REGEL
Schema:
`[Rassename] – [kurze belegte Zuordnung mit Pferd oder Pferderasse]`

Harte Grenzen:
- Rassename muss unverändert enthalten sein;
- `Pferd` oder `Pferderasse` muss in der Überschrift vorkommen; enthält der kanonische Rassename selbst bereits `Pferd`, erfüllt dies die Zuordnung und muss nicht künstlich wiederholt werden;
- zweite Hälfte nur aus belegter Herkunft, Region, Typ, Nutzung oder besonderem Merkmal;
- keine Werbung, Wertung oder Superlative;
- keine freien Adjektive wie faszinierend, edel, außergewöhnlich, perfekt oder beliebt;
- möglichst kurz und natürlich.

Im JSON steht diese H1 ausschließlich im Feld `titel`. `artikeltext` beginnt direkt mit `Herkunft und Geschichte`; dadurch entsteht in WordPress keine doppelte H1.

## 3. PFERD-/PFERDERASSE-REGEL
- im Fließtext muss mindestens einmal `Pferderasse` innerhalb der ersten 150 Wörter vorkommen;
- danach keine Pflichtwiederholung;
- `Rasse` nicht als automatisches Ersatzwort wiederholen;
- Wiederholungen aktiv vermeiden; bevorzugt Rassename, `das Pferd` oder fachlich passende konkrete Bezeichnung;
- `Population`, `Zucht`, `Bestand` nur verwenden, wenn fachlich exakt gemeint.

## 4. VERBINDLICHE ARTIKELSTRUKTUR
Reihenfolge darf nicht verändert werden:

1. `Herkunft und Geschichte`
2. `Erscheinungsbild`
   - `Größe und Gewicht`
   - `Körperbau`
   - `Farben und Abzeichen`
3. `Charakter und Verhalten`
4. `Bewegung und Gangarten`
5. `Einsatzmöglichkeiten`
   - `Ursprüngliche Nutzung`
   - `Heutige Nutzung`
6. `Haltung und Gesundheit`
   - `Haltung`
   - `Gesundheit und mögliche rassetypische Risiken`
7. `Zucht und Verbreitung`
8. `Status der Population`
9. `Besonderheiten der Rasse`
10. `[Rassename] auf einen Blick`
11. `Abgrenzung zu ähnlichen Rassen`
12. `Zusammenfassung`

Im JSON-`artikeltext` werden die Hauptabschnitte als `<h2>` und Unterabschnitte als `<h3>` ausgegeben. Keine zusätzliche H2. Keine H2 darf entfallen.

## 5. ABSCHNITTSBINDUNG
Jedes Datenfeld besitzt einen fachlich passenden Hauptabschnitt. Fakten dürfen nicht beliebig verschoben werden.

- Herkunft/Entstehung -> Herkunft und Geschichte;
- ursprüngliche Nutzung -> Ursprüngliche Nutzung;
- Stockmaß/Gewicht -> Größe und Gewicht;
- Exterieur -> Körperbau;
- Farben/Abzeichen -> Farben und Abzeichen;
- Charakter -> Charakter und Verhalten;
- Gangarten/Bewegung -> Bewegung und Gangarten;
- Haltung/Fütterung -> Haltung;
- Gesundheit/Genetik -> Gesundheit und mögliche rassetypische Risiken;
- Zucht/Verbreitung/Gefährdung -> Zucht und Verbreitung;
- formal domestiziert/feral/Wildform -> Status der Population.

Doppelung ist nur in `Auf einen Blick` und in der abschließenden `Zusammenfassung` zulässig.

## 6. VERBOTENE FREIHEITEN
Der Schreiber darf nicht:
- neue Fakten hinzufügen;
- unbelegte Eigenschaften verallgemeinern;
- Zielgruppen behaupten;
- `Anfängerpferd`, `Familienpferd`, `kinderlieb`, `pflegeleicht`, `gesund`, `unkompliziert` o. ä. verwenden, wenn nicht explizit belegt;
- aus Anatomie sportliche Eignung ableiten;
- aus Herkunft Robustheit, Trittsicherheit oder Genügsamkeit ableiten, sofern nicht belegt;
- fehlende Gesundheitsdaten als Gesundheitsfreiheit darstellen;
- aus fehlenden Risiken `keine Risiken bekannt` machen;
- klassische Fazit-, Kaufberatungs-, Vor-/Nachteils- oder Werbesprache einbauen.

## 7. BESONDERHEITEN
- 3–6 Punkte;
- nur belegte Besonderheiten;
- keine Auffüllung auf sechs Punkte;
- nicht bloß vorherige Sätze wortgleich wiederholen;
- jeder Punkt muss auf ein Datenfeld zurückführbar sein.

## 8. AUF EINEN BLICK
Feste Reihenfolge:
- Herkunft
- Region
- Typ
- Status
- Stockmaß
- Gewicht; wenn nicht belegt: `nicht belastbar dokumentiert`
- Typische Farben
- Besondere Gangarten
- Ursprüngliche Nutzung
- Heutige Einsatzgebiete
- Charakteristische Merkmale
- Zuchtstatus / Verband
- Gefährdungsstatus nur wenn belastbar

Keine subjektiven Scores.

## 9. ABGRENZUNG
- konkrete Vergleichsrasse nur nennen, wenn Datensatz oder gebundene Fachbasis die Abgrenzung trägt;
- keine künstlichen Vergleiche;
- wenn keine belastbare Vergleichsrasse vorliegt: knapp sagen, dass keine belastbare konkrete Abgrenzung dokumentiert ist.

## 10. ZUSAMMENFASSUNG
- letzter Hauptabschnitt lautet immer exakt `Zusammenfassung`;
- ca. 70–120 Wörter;
- nur bereits im Artikel belegte Kernpunkte;
- keine neuen Fakten;
- kein Fazitston, keine Wertung, keine Kaufempfehlung;
- Rassename muss enthalten sein.

## 11. INTERNE LINKS – NUR GEBUNDEN
Interne Links sind optional und nie Voraussetzung für das Schreiben.

Wenn ein freigegebenes Linkpaket vorliegt:
- nur diese Ziele verwenden;
- keine Ziel-URL selbst recherchieren oder erfinden;
- Glossarlink nur an der ersten natürlichen Nennung;
- maximal 3 interne Links pro Artikel;
- wenn kein Linkpaket vorliegt, wird der Artikel ohne interne Links geschrieben.

## 12. VERBINDLICHER MANAGER-0.2.0-JSON-VERTRAG
Die Produktionsausgabe eines Test- oder Serienbatches ist zwingend eine echte maschinenlesbare `.json`-Datei. Chattext, Markdown-Datei, WordPress-XML oder ein nacktes JSON-Array sind keine gültige Übergabe.

Top-Level muss exakt die technische Form des Pferderassen-Managers 0.2.0 erfüllen:

```json
{
  "contract": "PA_BREED_BATCH_V1",
  "batch_id": "nichtleere-eindeutige-id",
  "articles": []
}
```

Pflichtfelder jedes Objekts in `articles`:
- `source_id`
- `rassename`
- `slug`
- `rassengruppe_slug`
- `titel`
- `artikeltext`
- `kurztext`
- `meta_title`
- `meta_description`

Keines dieser Felder darf leer oder `null` sein.

### source_id
- muss exakt die stabile `breed-*`-ID aus dem gebundenen WDB-Katalog des Managers sein;
- unbekannte ID = BLOCK;
- doppelte ID im selben Batch = BLOCK;
- bereits importierte ID = BLOCK im realen Import.

### slug
- muss nichtleer und eindeutig im Batch sein;
- doppelter Slug = BLOCK;
- bereits vorhandener Pferderassen-Slug = BLOCK im realen Import.

### rassengruppe_slug
Zulässig sind ausschließlich die sechs im Manager 0.2.0 fest definierten Werte:
- `warmblueter` = Warmblüter
- `vollblueter` = Vollblüter
- `kaltblueter` = Kaltblüter
- `ponys-kleinpferde` = Ponys & Kleinpferde
- `gangpferde` = Gangpferde
- `robust-landrassen` = Robust- & Landrassen

Die Zuordnung darf nur erfolgen, wenn der freigegebene Rassendatensatz sie über `typ`/`rassegruppen` eindeutig trägt. Bei Mehrdeutigkeit wird nicht geraten; für einen Testbatch ist stattdessen eine eindeutig zuordenbare Rasse zu wählen.

### artikeltext / HTML
- `artikeltext` wird als WordPress-Inhalt importiert und muss deshalb als zulässiges WordPress-HTML geliefert werden;
- keine Markdown-Überschriften im Importfeld;
- technische Mindestlänge nach Entfernen aller HTML-Tags: 300 Zeichen;
- HTML, das durch `wp_kses_post` verändert würde, ist unzulässig;
- verwendet werden nur einfache, sichere Inhalts-Tags wie `<h2>`, `<h3>`, `<p>`, `<ul>`, `<li>`, `<strong>` und gebundene sichere `<a>`-Links.

### Batchgrenze
- mindestens 1 Artikel;
- maximal 25 Artikel pro Batch;
- Testbatch: exakt 5 Artikel.

## 13. ABSCHLUSSPRÜFUNG VOR DATEIAUSGABE
Vor Ausgabe muss der komplette Batch einmal gegen den gesamten Vertrag geprüft werden. Keine schrittweise Fehlerbehebung nach Importer-Rückmeldungen.

Textprüfung je Artikel:
- Titelregel erfüllt;
- `Pferderasse` mindestens einmal in den ersten 150 Fließtextwörtern;
- alle 12 H2 vorhanden und in korrekter Reihenfolge;
- vorgeschriebene H3 vollständig;
- keine zusätzliche H2;
- kein unbelegter Fakt;
- kein geschlossen dargestelltes offenes Feld;
- Besonderheiten 3–6 und belegt;
- Auf-einen-Blick-Reihenfolge korrekt;
- Zusammenfassung ohne neue Fakten;
- nur gebundene Links verwendet, falls Linkpaket vorhanden;
- keine unnötige Wiederholung von `Rasse`/`Pferderasse`.

Technische Prüfung des gesamten JSON:
- echte `.json`-Datei;
- Top-Level Objekt;
- `contract` exakt `PA_BREED_BATCH_V1`;
- `batch_id` nichtleer;
- `articles` Array;
- Testbatch exakt 5 Artikel;
- maximal 25 Artikel;
- alle neun Pflichtfelder je Artikel nichtleer;
- jede `source_id` im gebundenen Manager-WDB-Katalog vorhanden;
- keine doppelte `source_id`;
- keine doppelten Slugs;
- jeder `rassengruppe_slug` exakt einer der sechs erlaubten Werte;
- Gruppenzuordnung durch den jeweiligen WDB-Datensatz eindeutig getragen;
- jeder `artikeltext` nach Tag-Entfernung mindestens 300 Zeichen;
- nur zulässiges WordPress-HTML.

Erst nach dieser Gesamtprüfung darf die Datei ausgegeben werden.

## 14. PASS-REGEL
Der Autor darf sich nicht selbst fachlich freigeben.

Autorenausgabe = `ENTWURF`.

Ein separater Prüfschritt muss Datensatz + Schreibvertrag + fertigen Artikel vergleichen und liefert nur:
- `PASS`
oder
- konkrete Reparaturpunkte.

Ohne Prüfschritt kein fachlicher Produktions-PASS.

## 15. TESTBATCH
Erste Produktionsprüfung: exakt 5 Rassen.

Für den Testbatch sind bevorzugt fünf Rassen zu wählen, die zugleich:
- im gebundenen Manager-WDB-Katalog vorhanden sind;
- aus den freigegebenen WDB-Datensätzen geschrieben werden;
- eindeutig einer der sechs Manager-Rassengruppen zugeordnet werden können.

Ziel:
- Textqualität prüfen;
- Regelbindung prüfen;
- vollständigen JSON-Vertrag in einem Zug prüfen;
- anschließend erst Serienproduktion freigeben.
