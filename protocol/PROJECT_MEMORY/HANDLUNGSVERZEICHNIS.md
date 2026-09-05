# HANDLUNGSVERZEICHNIS

STAND: 2026-09-05

HARD RULE:
**Bekannte Aktion niemals erraten. Existiert ein definierter Workflow, darf kein Ersatzweg erfunden werden.**

## Architektur verbessern

Aktion:
Ein Chat erkennt in realer Arbeit einen Optimierungsbedarf am Campus.

Verbindlicher Weg:
1. konkreten Bedarf benennen;
2. kleinste nachhaltige Architekturänderung wählen;
3. nur Architektur-Ebene verändern, keine fremde Facharbeit;
4. `BAUCONTAINER/BAUPROTOKOLL.md`;
5. dauerhaftes WARUM → `AENDERUNGSREGISTER.md`;
6. bei Fehler → `BAUCONTAINER/ARCHITEKTUR_FEHLERKISTE.md`;
7. Hardlocks/Prüfung.

Kein spezieller Architekten-Chat erforderlich.

## Hausmeister-Lauf

Aktion:
Produktive Räume auf Ballast prüfen.

Verbindlicher Weg:
`BAUCONTAINER/HAUSMEISTER.md`

Harte Grenzen:
- AKTIV nicht verschieben;
- UNGEKLÄRT nicht verschieben;
- keine Löschung;
- vor Verschiebung Referenzen/Hash/Ziel prüfen;
- jede Verschiebung im `ARCHIV/HAUSMEISTER_PROTOKOLL.md`.

## WordPress-Plugin finden

Aktion:
Prüfen, ob ein WordPress-Plugin/Installer bereits vorhanden ist.

Verbindlicher Weg:
1. `WORDPRESS_REGISTER.md`;
2. bei Allgemeingültigkeit → Modulregister;
3. bei Projektstatus → zuständiges Fachbüro;
4. bei Installation/Release → dortige technische Originalquelle.

Nie aus einem Dateinamen einen LIVE-/Release-Status ableiten.

## Neues Projekt beginnen

1. Hauptpförtner;
2. Ziel/Anforderungen;
3. Modulregister;
4. passende vorhandene Module;
5. minimales Projektgebäude.

## Neue Masterdatei aufnehmen

1. `BAUCONTAINER/MASTERDATEIEN_REGEL.md`;
2. vollständig inventarisieren;
3. Artefakte trennen;
4. Modulklasse prüfen;
5. Modulregister aktualisieren;
6. Hauptort/Archivzuordnung bestimmen.

## Codex / technische Projekteingangstür

Autorität: Root-`AGENTS.md`
Start:
`python3 control/cloud-entry-gate/cloud_entry.py start`

Bei BLOCKED: stoppen. Keine Alternativroute.

## Textmaschine / Artikelproduktion

Autorität:
- Root-`AGENTS.md`
- aktueller technischer State unter `control/startmaster0107/`
- gebundene Capsule/Instruction

Keine manuelle Ersatzproduktion.

## Text-Regression

Matrix:
`control/startmaster0107/HOBBYRAUM_KNOWN_ERROR_REGRESSION_MATRIX_M01_M33_20260904.md`

Runner:
`control/startmaster0107/HOBBYRAUM_M01_M33_REGRESSION.py`

## Affiliate-Release

Autorität:
`control/release-governance/CURRENT_RELEASE.json`
`release/affiliate-zentrale/AGENTS.md`

## Unbekannte Aktion

**STOPP – nicht raten.**
Erst Zuständigkeit und vorhandenen Arbeitsweg klären.


## Natürlicher Campus-Einstieg

Aktion:
Der Nutzer beschreibt in Alltagssprache Campus, Projekt oder Büro.

Verbindlicher Weg:
`START_HERE.md` → `HAUPTPFOERTNER.md` → genanntes Projekt → genanntes Büro.

Kein exaktes Schlüsselwort erforderlich.

## Paul – TEXT/SEO

Aktion:
**Der Nutzer beauftragt ausdrücklich Paul** mit einem klar abgegrenzten TEXT/SEO-Problem.

Ein normaler TEXT-Arbeitschat wird niemals automatisch zu Paul geroutet.

Verbindlicher Einstieg:
`PAUL/TEXT_SEO/START_HERE.md`

Dort liegen/verweisen:
- aktueller Status quo;
- vollständiges Protokoll;
- aktiver Zielvertrag;
- komplette aktuelle Fehlerliste;
- Test-vs-Live-Befund;
- Hard Rules;
- aktuelle technische GitHub-Originalquellen.

Paul arbeitet nur auf dem gebundenen Paul-Branch und nur im ausdrücklich benannten technischen Schreibbereich.

Harte Grenze:
- `protocol/PROJECT_MEMORY/**` für Paul = READ ONLY;
- keine Büro-/Status-/Register-/Archivänderungen durch Paul;
- kein Merge / keine Integration durch Paul;
- Rückgabe als Lösungspaket an den zuständigen Arbeitschat;
- derselbe technische Schreibbereich wird nicht parallel von Paul und Arbeitschat verändert.


## Hobbyraum betreten

Aktion:
Der Nutzer nennt ein Projektbüro und „Hobbyraum“.

Verbindlicher Weg:
Projektgebäude → Büro-`START_HERE.md` → `CURRENT_STATE.md` → `HOBBYRAUM.md`.

Routing-Kennwort:
`Hobbyraum`

Wichtig:
Kein Passwort und keine Schreibberechtigung.
Befugnisse kommen ausschließlich aus Rolle + gebundenem Auftrag + Branch/Fachregeln.
