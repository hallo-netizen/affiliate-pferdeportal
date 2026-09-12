# MOD-008 / PFERDE-ATELIER – SEITENKONZEPT V1

STAND: 2026-09-12
STATUS: KORRIGIERT / VERBINDLICHE FRONTEND-RICHTUNG

## Grundprinzip

Das Glossar wird wie ein eigener Inhaltsbereich des Pferde-Ateliers aufgebaut – nicht wie eine lange Einzelseite.

Die bereits vorhandene WordPress-Seite `Glossar` bleibt die öffentliche Startseite.

Keine HTML-Anker-Navigation zwischen Kategorien.
Keine Ausgabe aller Glossarbegriffe auf der Startseite.
Keine doppelte Kategorienavigation auf der Startseite.

## Feste Glossar-Navigation

Oben auf jeder Glossarseite steht dieselbe waagerechte Glossar-Navigation.

Beispiel:
`Glossar | Gesundheit | Fütterung | Haltung & Stall | Ausrüstung | Anatomie | ...`

Jeder Kategoriepunkt ist ein echter Link auf eine eigene Glossar-Kategorieseite.

Die Navigation erscheint auf:
- Glossar-Startseite;
- jeder Glossar-Kategorieseite;
- jeder Glossar-Begriffsseite.

## Glossar-Startseite

Die Startseite ist ein Einstieg, kein Gesamtverzeichnis.

Reihenfolge:
1. zum Pferde-Atelier passender Bild-/Hero-Bereich analog der vorhandenen Designlogik;
2. Titel `Glossar` + kurze Einleitung;
3. feste waagerechte Glossar-Navigation;
4. optional kompakte Suche;
5. Bereich `Aus dem Glossar` mit einer begrenzten wechselnden Auswahl einzelner Glossarbegriffe – analog zur Beitragsvorschau auf der normalen Startseite;
6. keine vollständigen Kategorienlisten und keine vollständige Begriffsliste.

Die wechselnde Auswahl bleibt bewusst klein. Die Startseite darf unabhängig von der späteren Gesamtmenge des Glossars nicht mit tausenden Begriffen wachsen.

## Glossar-Kategorieseite

Jede Kategorie erhält eine eigene öffentliche Seite / URL.

Beispiel:
`/glossar/gesundheit/`

Reihenfolge:
1. normale Pferde-Atelier-Kopf-/Bildlogik soweit im Design vorgesehen;
2. feste waagerechte Glossar-Navigation;
3. Kategoriename + kurzer Einleitungstext;
4. Begriffe dieser Kategorie;
5. bei größerer Menge Seitenaufteilung/Paginierung statt Alles-auf-einer-Seite;
6. optional Suche/A–Z innerhalb der Kategorie, sofern später fachlich sinnvoll.

## Glossar-Begriffsseite

Jeder Begriff besitzt eine eigene Zieladresse, z. B.:
`/glossar/gesundheit/kolik/`

Reihenfolge:
1. feste waagerechte Glossar-Navigation;
2. Begriffstitel;
3. Kurzdefinition;
4. Erklärung;
5. verwandte Begriffe / interne Links.

Kein eigenes Beitragsbild pro Begriff erforderlich.

## Designbindung

Kein eigenes Glossar-Sonderdesign erfinden.

Die konkrete Gestaltung wird am aktuellen Pferde-Atelier-Designplugin ausgerichtet. Farben allein reichen dafür nicht; maßgeblich sind auch vorhandene Hero-/Bildlogik, Typografie, Abstände, Karten-/Beitragsvorschau und responsive Verhalten.

Aktueller autoritativer Designstand laut DESIGN/CURRENT_STATE:
`Pferde Atelier Design 1.50.472 / Contract V104 + DESIGN-ORDER-SWAP-002`.

Das Glossar darf optisch wie ein zusätzlicher Bereich des bestehenden Pferde-Ateliers wirken, nicht wie ein separates Fremdplugin.

## Technische Konsequenz

Der bisherige Prototypansatz `eine Startseite + Kategorien als HTML-Anker + alle Begriffe auf einmal` ist verworfen.

Neue technische Zielrichtung:
- Startseite bleibt begrenzt;
- Kategorien sind echte eigene Routen/Seiten;
- Begriffe werden nur im passenden Kontext geladen;
- keine `numberposts = -1`-Gesamtausgabe auf der Glossar-Startseite;
- keine `#anker` als Kategorienavigation;
- gemeinsame waagerechte Navigation wird zentral erzeugt.

Vor Umsetzung muss der Frontend-Prototyp entsprechend umgebaut und danach erneut positiv/negativ getestet werden.