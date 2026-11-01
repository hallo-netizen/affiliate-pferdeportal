# HOBBYREGISTER – TEXTREGELN V1

STAND: 2026-10-23
STATUS: BINDING FÜR SCHEMA-F-PRODUKTION

## Verbindliche Korrektur 01.11.2026 – KEIN blindes Einsetzen von Hobbynamen

**Fachlicher Fehlernachweis:** Die ältere Schablone `Passt [Hobby] zu dir?` bzw. `Wo und wann kannst du [Hobby] ausüben?` ist für **Gegenstände** wie „Münzen“ oder „Spielkarten“ semantisch falsch. Eine solche mechanische Verwendung ist ab sofort untersagt.

**Hobbyidentität vs. Tätigkeit:** Der kanonische Hobbyname bleibt unverändert (z. B. **Münzen**). Für fließende Fragen wird dagegen die **aus Name und vorhandenem Kurzprofil begründete Tätigkeit** verwendet (z. B. **Münzen sammeln**). Beispiele:
- Münzen → „Münzen sammeln – passt das zu dir?“ / „Wo und wann kannst du Münzen sammeln?“
- Spielkarten → „Spielkarten sammeln – passt das zu dir?“ / „Wo und wann kannst du Spielkarten sammeln?“
- Sportdrachen → „Lenkdrachen fliegen – passt das zu dir?“ / „Wo und wann kannst du Lenkdrachen fliegen?“
- Wandern → „Wandern – passt das zu dir?“ / „Wo und wann kannst du wandern?“
- Bonsai → „Bonsai gestalten und pflegen – passt das zu dir?“ / „Wo und wann kannst du Bonsai gestalten und pflegen?“

**Eine zentrale Sprachentscheidung pro Hobby statt mehrfacher Sonderprüfungen:** Die eindeutigen Zuordnungen stehen für alle **862/862** Registry-IDs in `HOBBYREGISTER_862_UEBERSCHRIFTEN_KORREKTUR_20261101.csv`. Sie sind ein **redaktioneller Korrekturkandidat** und ersetzen nicht die ursprüngliche Hobby-Datenwahrheit. Unterzeichnete Live-Freigabe und wortgetreue Übernahme in die Original-Version HD-007 1.2.16 stehen **noch aus**. Keine stillschweigende Umbenennung, keine neue WordPress-Kategorie, keine zusätzliche Plugin-Engine, keine Änderung des Artikeltexts.

**Abnahme der späteren Pluginübernahme:** dieselben 862 Registry-IDs und Hobby-Label (862/862, 0 Umbenennungen), neue F2/F3 aus der zentralen Zuordnung, alle 8 Überschriften sprachlich kontrolliert, Positiv-/Negativbeispiele, Bild-/Trait-/Bodybestand bytegleich, PHP-Syntax und ZIP-Test, danach tatsächliche WordPress-Frontend-Prüfung. *Ohne diese Prüfungen kein PASS.*

---

## Zweck

Alle Hobbyregister-Detailtexte folgen demselben fachlichen Aufbau, ohne wie ein Formular oder eine 57-Felder-Liste zu wirken.

Datenbasis:
- genau eine kanonische Hobbyidentität;
- zentrale Kurzprofile;
- zentrale 57 Traits nach Schema 1.2;
- Schema F V1.

## HARD RULES

1. Nichts erfinden. Nur Aussagen, die Kurzprofil oder Traits tragen.
2. UNKNOWN erzeugt keine Behauptung.
3. Keine stereotype Eignung nach Geschlecht, Alter oder Lebensstil.
4. Direkte natürliche Du-Ansprache.
5. Fließtext statt Merkmalsliste.
6. Keine generischen Füllabsätze und kein künstliches Fazit.
7. Traitwerte werden in verständliche Alltagssprache übersetzt, nicht als interne IDs ausgegeben.
8. Widersprüche zwischen Kurzprofil und Traits blockieren Produktion.
9. F9 ist der kompakte Vergleichsblock; derselbe Inhalt wird im Fließtext nicht mechanisch wiederholt.
10. F10 „ähnliche Hobbys“ wird aus dem zentralen Traitbestand abgeleitet, nicht manuell als zweite Taxonomie gepflegt.

## Verbindlicher Aufbau der Detailseite

### 1. Worum geht es bei [Hobby]?
F1: Was ist das? Was macht man? Was ist der Reiz? Einordnung klassisch/Nische/ungewöhnlich nur, wenn belegt.

### 2. [Tätigkeit] – passt das zu dir?
F2: Motivation, Sozialform, Abhängigkeit von anderen, Tempo, Abwechslung, Öffentlichkeit, Natur, Wettbewerb.

### 3. Wo und wann kannst du [Tätigkeit]?
F3: Ort, Infrastruktur, Reise, Wetter, Tageslicht, Saison, typische Dauer, Planbarkeit, Häufigkeit, Pausierbarkeit, Projekthorizont.

### 4. Platz, Alltag und Pflege
F4: aktiver Platz, Lagerplatz, Transport, Lärm, Schmutz, Geruch/Dämpfe, Anschlüsse, Auf-/Abbau, Ausrüstungspflege.

### 5. Kosten und Ausrüstung
F5: Kurzprofil „Was braucht man?“, Einstiegskosten, laufende Kosten, Verbrauchsmaterial, Umfang der Ausrüstung, Leihen/Mieten, Wartung.

### 6. Was musst du können?
F6: körperliche Intensität, Kraft, Ausdauer, Koordination/Balance, Feinmotorik, Konzentration, Präzision, Lernkurve, Anfängerfreundlichkeit, Anleitung, Meisterungstiefe.

### 7. Was entsteht daraus?
F7: Tätigkeitsarten, Ergebnis, analog/digital, Bildschirmanteil, Struktur, Abwechslung.

### 8. Grenzen, Sicherheit und Regeln
F8: Sicherheitsrisiko, Regeln/Genehmigungen, Pflegepflichten, Zugang, Anpassbarkeit.

Daneben bzw. davor:
- F9 „Auf einen Blick“ als knapper Vergleichsblock;
- F10 gleiche Hobbygruppe + ähnliche Hobbys.

## Länge

Richtwert für einen vollständigen Registertext:
**ca. 650–1.100 Wörter**.

Nicht künstlich auf Länge schreiben. Ein Hobby mit wenigen belastbaren Aussagen darf kürzer sein; ein komplexes Hobby darf länger werden.

Je Abschnitt normalerweise 1–2 natürliche Absätze. Überschriften bleiben funktional gleich, dürfen sprachlich leicht an das Hobby angepasst werden.

## Stil

- einfache, klare Sätze;
- konkrete Wörter;
- „du“ statt unpersönlichem Behördenstil;
- keine Werbesprache wie „perfekt“, „ideal für jeden“, „unvergleichlich“;
- keine pseudo-psychologischen Aussagen;
- keine Wiederholung desselben Merkmals in drei Abschnitten;
- Kosten/Zeit/Platz möglichst konkret, wenn die zentrale Klassifikation konkrete Klassen liefert;
- Risiken sachlich nennen, nicht dramatisieren.

## Textproben V1

Verbindliche Prototypen:
- Buchbinden – 8 Abschnitte, ruhiges/fertigendes Hobby;
- Slacklining – 8 Abschnitte, bewegungs-/koordinationsintensives Hobby.

Sie dienen der visuellen und sprachlichen Abnahme vor dem 862er-Rollout.
