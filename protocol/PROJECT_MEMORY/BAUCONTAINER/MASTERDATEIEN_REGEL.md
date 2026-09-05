# BAUCONTAINER – MASTERDATEIEN-REGEL

STAND: 2026-09-05

## Harte Regel

**Alles aus einer Masterdatei wird verwertet und zugeordnet. Nichts darf still verloren gehen.**

Masterdatei bedeutet nicht „nur die neueste Version“.

Auch Archive, Altversionen, Protokolle, Fehlerlisten, Statusdateien, Tests, Hashes, Exporte, Produktionsdaten, Migrationen, Zwischenstände und Nebenmaterial werden inventarisiert.

## Zwei getrennte Entscheidungen

### A. Artefaktklassifizierung
Für jeden Bestandteil:
- ALLGEMEINER CODE/KERN
- PROJEKTKONFIGURATION
- PROJEKTDATEN
- HISTORIE
- FEHLERBELEG
- TESTBELEG
- PROTOKOLL/ERKLÄRUNG
- DUBLETTE
- UNGEKLÄRT

Eine einzelne Masterdatei kann dadurch GEMISCHT sein.

### B. Modulklassifizierung
Der erkannte Modul-Kern wird separat im Modulregister klassifiziert:
- ALLGEMEINGÜLTIG
- PROJEKTBEZOGEN
- UNGEKLÄRT

**GEMISCHT ist keine Modulklasse.**

## Default

Wenn die Modulklasse nicht sicher belegt ist:
**UNGEKLÄRT.**

Nicht automatisch als projektbezogen ablegen.
Nicht automatisch als allgemeingültig wiederverwenden.

## Pflichtzuordnung je Bestandteil

Mindestens:
- Quelle
- Dateiname/Pfad
- Hash, wenn verfügbar
- Inhaltstyp
- Zweck/Bedeutung
- Artefaktklasse
- Projekt/Büro/Modul
- Status
- offene Fragen
- Ziel-/Referenzort

## Dubletten

Byte-identische Dateien werden als DUBLETTE markiert.
Ihre Herkunft bleibt erhalten.

## Sensible technische Werte

Secrets werden nicht in ein öffentliches Repository kopiert.
Existenz, Funktion und Herkunft bleiben inventarisiert.

## Löschen

Erst nach vollständiger Zuordnung und Referenzprüfung.

UNGEKLÄRT = NICHT ANFASSEN.
