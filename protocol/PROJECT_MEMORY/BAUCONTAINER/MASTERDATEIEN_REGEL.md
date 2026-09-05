# BAUCONTAINER – MASTERDATEIEN-REGEL

STAND: 2026-09-05

## Harte Regel

**Alles aus einer Masterdatei wird verwertet und zugeordnet. Nichts darf still verloren gehen.**

Masterdatei bedeutet nicht „nur die neueste Version“.

Auch enthaltene:
- Archive
- alte Versionen
- Protokolle
- Fehlerlisten
- Statusdateien
- Tests
- Hashes
- Exporte
- Produktionsdaten
- Migrationsreste
- Zwischenstände
- Nebenmaterial

werden inventarisiert.

## Pflichtzuordnung je Bestandteil

Mindestens:
- eindeutige Quelle
- Dateiname/Pfad
- Hash, wenn verfügbar
- Inhaltstyp
- Zweck/Bedeutung
- zugehöriges Projekt/Büro/Baustein
- Status:
  - AKTIV
  - LIVE-BELEG
  - HISTORISCH
  - FEHLERBELEG
  - TESTBELEG
  - DATENBELEG
  - ARCHIVKANDIDAT
  - DUBLETTE
  - UNGEKLÄRT
- offene Fragen
- Ziel-/Referenzort

## Dubletten

Byte-identische Dateien werden als DUBLETTE erkannt, aber ihre Herkunft bleibt dokumentiert.

## Sensible technische Werte

Zugangsdaten/Secrets werden nicht in ein öffentliches Repository kopiert.
Ihre Existenz und Funktion werden trotzdem inventarisiert.

Das ist kein „Verlust“, sondern sichere Zuordnung ohne Offenlegung.

## Löschen

Erst nach vollständiger Zuordnung und Referenzprüfung darf über Verschieben/Löschen entschieden werden.

UNGEKLÄRT = NICHT ANFASSEN.
