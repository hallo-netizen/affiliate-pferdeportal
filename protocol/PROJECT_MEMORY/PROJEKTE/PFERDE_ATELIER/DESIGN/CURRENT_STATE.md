# DESIGN – CURRENT STATE

STAND: 2026-09-14

## AUTORITÄT DIESER DATEI

Diese Datei ist die **einzige aktuelle Campus-Standzusammenfassung dieses Büros**.

- aktuelle Arbeit / NEXT ACTION → `HOBBYRAUM.md`
- Fehler → `protocol/PROJECT_MEMORY/FEHLERREGISTER.md` → autoritative Fehlerquelle
- Zielvertrag → `protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md` → Hauptquelle
- Änderungsgrund → `protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md`
- Historie → `protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

Technische/Fachwahrheit bleibt an den verlinkten Originalquellen. Andere Campus-Dateien dürfen diesen dynamischen Bürostand nicht als zweite Wahrheit fortschreiben.

## Aktueller belastbarer LIVE-Stand

### Allgemeines bestätigtes Design

Historische bestätigte Basis bleibt:
- Pferde Atelier Design 1.50.472 / Contract V104;
- Kategorie-Reihenfolge `DESIGN-ORDER-SWAP-002` LIVE PASS.

Diese bestätigten Bereiche dürfen durch die aktuelle Pferderassen-Arbeit nicht regressieren.

### Pferderassen – aktueller realer Stand

Installierter/getesteter Kandidat:
`PFERDE_ATELIER_DESIGN_V1.50.507_AJAX_PAGINATION_BODYWIDTH_INSTALLIEREN.zip`

SHA-256:
`b27898d26b32e9fe9910a2312b6bfbcec12c738f76290ed89304eca931353ec9`

Lokale exakte ZIP-Prüfung:
- Contract 28/28 PASS;
- Runtime 28/28 PASS;
- PHP-Lint PASS;
- ZIP-/Strukturprüfung PASS;
- 11/11 absichtlich gebrochene Varianten ROT.

Realer Nutzer-Readback 2026-09-14:
- Hauptsuche mit eigener Welt `Pferderassen`: LIVE PASS;
- Pferderassen-Hero: LIVE PASS;
- lokale Pferderassen-AJAX-Suche: LIVE PASS;
- `Alle Rassen` Pagination 24/Seite: LIVE PASS;
- Einzelrassenbreite: **LIVE FAIL** – trotz lokalem Breitenvertrag bleibt die reale Seite zu schmal.

Damit ist **Design 1.50.507 kein Gesamt-LIVE-PASS**.

## Verbindliche Pferderassen-Regeln

Hauptquelle:
`PFERDERASSEN_DESIGN_RULES.md`

Besonders bindend:
- Startseite max. 8 Vorschauen;
- `Alle Rassen` paginiert 24/Seite;
- Hero Übersicht: `PFERDE IM PORTRÄT / Pferderassen / Charakter, Herkunft & Besonderheiten`;
- Einzelrasse: Breadcrumb nach Glossar-Geometrie, kein Autor;
- Beitragsbild = Heroquelle = Vorschaubild;
- links Icon-Steckbrief, Mitte Factsheet-Text, rechts Wissens-/Relationsspalte;
- generischer Kurztext unter dem Rassentitel entfällt;
- normale WordPress-Beiträge bleiben unberührt.

## Aktueller Fehler

Autoritative Detailquelle:
`FEHLERQUELLEN.md` → `DESIGN-RASSEN-20260914`.

Kurz: Der tatsächliche Astra/Kubio-/Body-Container hält `single-pa_breed` weiterhin schmal. Der nächste Fix muss am bewährten Portal-Containerpfad ansetzen; kein weiterer innerer `max-width`-Versuch.

## Quell-/Releasegrenze

Die Pferderassen-Designstände 1.50.500–1.50.507 wurden in diesem Chat als installierbare lokale Pluginpakete erzeugt und geprüft, sind aber **nicht als autoritative Plugin-Source/Releasekette im Repository gebunden**.

Daher darf im PLUGINS-Büro kein isoliertes `CURRENT.zip` aus diesem Stand behauptet werden.

## NEXT ACTION

Siehe ausschließlich `HOBBYRAUM.md`.