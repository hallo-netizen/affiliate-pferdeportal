# DESIGN – PFERDERASSEN – ENTSCHEIDUNGEN / WARUM – 2026-09-14

ROLLE: dauerhafte WAS/WARUM-Entscheidungen; keine zweite CURRENT-/Fehlerwahrheit.

## RASSEN-DES-001 – Übersicht nach Glossar-Prinzip

**WAS:** Pferderassen-Übersicht übernimmt die bewährte Glossar-Geometrie für Breadcrumb-Abstand, Hero-Übergang, Suche/A–Z und ruhige vertikale Abstände.

**WARUM:** bereits bestätigte, konsistente Wissensbereich-Gestaltung wiederverwenden statt parallele Sondergeometrie zu erfinden.

## RASSEN-DES-002 – Ein Bild pro Rasse

**WAS:** WordPress Featured Image ist dieselbe Quelle für Einzelrassen-Hero und Vorschaubilder in Übersicht/Navigation/Suche.

**WARUM:** rund 200 Rassen bleiben mit einem reproduzierbaren Bild je Rasse beherrschbar; keine doppelte Bildpflege.

## RASSEN-DES-003 – Factsheet bestimmt Einzelrassenlayout

**WAS:** Desktop: linker visueller Icon-Steckbrief | redaktioneller Factsheet-Text | rechte Wissens-/Relationsspalte. Mobil kontrolliert gestapelt.

**WARUM:** die zentrale Rassen-WDB/Factsheet-Struktur ist bei jeder Rasse gleich gegliedert. Das Design soll diese vorhandene Struktur sichtbar machen, nicht Inhalte aus Fließtext erraten.

## RASSEN-DES-004 – Ähnliche Rassen nur strukturiert

**WAS:** ähnliche Rassen werden über stabile Rassen-/WDB-IDs gebunden und daraus als echte Rassenlinks gerendert; kein freies KI-Raten beim Seitenaufruf.

**WARUM:** Beziehungen müssen reproduzierbar, prüfbar und für alle Rassen gleich behandelbar sein.

**OFFEN:** Manager-/Importvertrag muss ein solches Relationsfeld erst verbindlich aufnehmen, sobald die WDB-Relation autoritativ vorliegt.

## RASSEN-DES-005 – Keine generische Datensatz-Floskel im Hero

**WAS:** Sätze wie `Burguete stammt aus Spanien. Der Datensatz dokumentiert Herkunft, Nutzung, Zucht und zentrale Merkmale dieser Pferderasse.` werden im Hero nicht gezeigt.

**WARUM:** diese Sätze sind technische Zusammenfassungsfloskeln ohne zusätzlichen Nutzerwert und schwächen die hochwertige Hero-Gestaltung.

## RASSEN-DES-006 – Breite am realen Theme-Container beweisen

**WAS:** Die Einzelrassenbreite wird am echten Body-/Astra-/Kubio-Containerpfad gebunden und im real gerenderten Browser geprüft. Ein inneres `max-width` allein gilt nicht als Beweis.

**WARUM:** 1.50.507 war lokal gegen die beabsichtigten CSS-Regeln grün, blieb live aber sichtbar zu schmal. Der Test bildete den realen Containerpfad unzureichend ab.

Aktueller LIVE-/Fehlerstatus ausschließlich aus `CURRENT_STATE.md` und `FEHLERQUELLEN.md` lesen.
