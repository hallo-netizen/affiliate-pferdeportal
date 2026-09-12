# BÜRO PFERDERASSEN

STAND: 2026-09-12

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Das Fachbüro für die zentrale, strukturierte und quellengebundene Rassenbasis des Pferde-Ateliers – für Pferderassen, Ponyrassen und Kleinpferde in EINER gemeinsamen Datenbasis.

**HIER BIST DU RICHTIG, WENN …**  
du Rassen recherchieren, Rassefakten prüfen, Herkunft/Geschichte/Exterieur/Charakter/Einsatz/Haltung/Gesundheit erfassen, Quellen binden oder später aus diesen Fakten Rassebeiträge vorbereiten willst.

**DU DARFST …**  
Rassenfakten recherchieren, Quellen ergänzen, Datensätze vervollständigen, Synonyme zusammenführen, Klassifikationen korrigieren und das Datenmodell kontrolliert erweitern.

**DU DARFST NICHT …**  
Rassefakten erfinden, Ponys als zweite Parallel-Datenbank führen, unbelegte Charakterklischees als Tatsachen speichern, Gesundheitsbehauptungen ohne belastbare Quelle übernehmen, WordPress-/TEXT-/SEO-/AFFILIATE-Systeme aus diesem Büro ungefragt verändern oder hier eine zweite Produktionswahrheit anlegen.

**ALS NÄCHSTES …**  
`CURRENT_STATE.md` → `HOBBYRAUM.md` → `RASSEN_DATENMODELL.md` → `RASSEN_REGISTER.md` → `DATEN/START_HERE.md`.

## SCHNELLWEGWEISER – EINE WAHRHEIT

- **AKTUELLER BÜROSTAND:** `CURRENT_STATE.md`
- **AKTUELLE ARBEIT / NEXT ACTION:** `HOBBYRAUM.md`
- **DATENMODELL / FELDLOGIK:** `RASSEN_DATENMODELL.md`
- **RASSENINDEX:** `RASSEN_REGISTER.md`
- **EINZELDATENSÄTZE:** `DATEN/`
- **FEHLER:** `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Fehlerquelle
- **ZIELVERTRAG:** `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → Hauptquelle
- **WARUM GEÄNDERT:** `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- **HISTORIE:** `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

**Regel:** Diese Bürotür ist Orientierung. Sie pflegt keine zweite aktuelle Rassen-, Fehler-, Ziel- oder Produktionswahrheit.

## FACHGRENZEN

- PFERDERASSEN verantwortet die quellengebundene Rassen-Faktenbasis.
- Pferde, Ponys und Kleinpferde liegen in derselben Datenstruktur; die Einordnung erfolgt als Feld im Datensatz.
- TEXT verantwortet die spätere eigentliche Artikelproduktion, sofern/solange kein eigener gebundener Produktionsweg beschlossen wird.
- SEO kann später Nachfrage/Priorisierung liefern, schreibt aber keine Rassefakten.
- AFFILIATE ist für Rassefakten nicht zuständig.
- WordPress erhält später nur freigegebene Ausgaben; die Campus-Datenbasis wird nicht bei jedem Seitenaufruf live abgefragt.

## FLEXIBILITÄTSREGEL

Das Datenmodell ist bewusst erweiterbar:
- wenige stabile Kernfelder;
- optionale Fachfelder;
- `schema_version` je Datensatz;
- neue sinnvolle Felder dürfen zentral im Datenmodell ergänzt werden;
- ältere Datensätze bleiben gültig und werden anschließend kontrolliert nachgezogen;
- fehlend ist nicht gleich falsch: `nicht_recherchiert`, `nicht_belegt` und `nicht_anwendbar` werden unterschieden.

Keine starre technische Struktur darf verhindern, dass später ein fachlich sinnvoller Punkt für alle Rassen ergänzt wird.

## QUELLENREGEL

Jede belastbare fachliche Aussage muss auf eine Quelle zurückführbar sein. Priorität:
1. offizieller Zuchtverband / anerkanntes Zuchtbuch / zuständige staatliche oder internationale Stelle;
2. wissenschaftliche oder universitäre Quelle;
3. seriöse Fachquelle ergänzend.

Bei Widersprüchen werden beide Aussagen mit Quellenstatus gespeichert; keine freie Auflösung durch Vermutung.

## Arbeitsfreigabe bei echter Arbeit

Vor jeder technischen Aktion:
1. `CURRENT_STATE.md`;
2. `HOBBYRAUM.md`;
3. `protocol/PROJECT_MEMORY/HANDLUNGSVERZEICHNIS.md`;
4. `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` und relevante Originalquelle;
5. `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`;
6. aktiver Zielvertrag über `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md`.

Treffer auf einen bekannten Fehler/verbotsgleichen Weg = nicht erneut ausprobieren.

## Globale Arbeitsort-Sperre

Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.
