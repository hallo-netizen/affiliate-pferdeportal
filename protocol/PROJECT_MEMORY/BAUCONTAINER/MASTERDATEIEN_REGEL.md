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


## Keine zweite CURRENT-Wahrheit

Masterdateien-Inventare sind **Inventare, keine laufenden Statusspeicher**.

Sie dürfen historische Versionen, Heads, Hashes, Live-Belege und damalige Statusdateien inventarisieren, aber niemals so formulieren, dass daraus eine zweite aktuelle Fach-/Release-Wahrheit entsteht.

Verboten in einem Inventar als eigene aktuelle Aussage:
- „aktueller Statusbeleg“ für eine datierte Altakte;
- aktueller Branch-Head;
- aktuelles Manifest;
- aktueller Blocker/NEXT ACTION;
- aktueller Releasekandidat.

Stattdessen nur Verweis auf:
- zuständiges `CURRENT_STATE.md`;
- zuständiges `HOBBYRAUM.md`;
- technische Originalautorität/Governance.

Negativprüfung bei jeder Inventar-Aktualisierung:
**Kann ein neuer Chat aus dem Inventar einen anderen aktuellen Stand ableiten als aus CURRENT_STATE/Governance?**
Wenn ja: BLOCKED und Inventar bereinigen.
