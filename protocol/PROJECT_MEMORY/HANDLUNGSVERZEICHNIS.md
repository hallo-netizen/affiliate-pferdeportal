# HANDLUNGSVERZEICHNIS

STAND: 2026-09-09

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

Status-/Bürowahrheit liest Paul dagegen frisch vom offiziellen Campus-Ref; sein eigener Branch ist dafür keine Autorität. Vor Start und vor Rückgabe erneut prüfen.

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


## Tresor / Archiv / Git-Mirror

Verbindlicher Weg:
- Historie/Beleg → `ARCHIV/START_HERE.md`;
- Backup/Restore → `TRESOR/START_HERE.md` → `TRESOR/NOTFALL_WIEDERAUFBAU.md`.

Harte Grenze:
**Nie Runner, Tests, Produktion oder Reparatur direkt aus Archiv/Tresor/Mirror ausführen.**
Auch nicht als Ersatzroute bei BLOCKED.

Nach Restore erst frischen offiziellen Arbeits-Worktree herstellen und dann den normalen definierten Arbeitsweg neu starten.


## Produktvergleich planen / entwickeln

Aktion:
Produktwissen/Produktrecherche, konkrete Produktvergleiche, Vergleichsmerkmale, SEO-Nachfrageabgleich, harte Fakten/Quellen, Dossiers oder den eigenständigen V1-Produktvergleichsweg bearbeiten.

Verbindlicher Weg:
`PROJEKTE/PFERDE_ATELIER/PRODUKTVERGLEICH/START_HERE.md`
→ `CURRENT_STATE.md`
→ `HOBBYRAUM.md`
→ gebundene Originalquellen.

Fachgrenzen:
- PRODUKTWISSEN bleibt Produktwahrheit;
- SEO/PSTE liefert nur Nachfrage-/Planning-/Kannibalisierungssignale und schreibt keine Produktfakten;
- AFFILIATE bleibt nachgelagerter Exact-Match-Commerce-Layer;
- STARTMASTER/TEXT wird aus diesem Büro nicht umgebaut;
- V1 besitzt aktuell keine STARTMASTER/TEXT-Laufzeitabhängigkeit;
- eine spätere ACM-/TEXT-Anbindung ist nur nach eigener isolierter Machbarkeits-/Vertragsentscheidung zulässig und niemals automatische Ersatzroute.

Keinen parallelen STARTMASTER-/TEXT-Umbau aus dem Produktvergleichsbüro beginnen.


## Externe READ-ONLY-Zweitprüfung

Aktion:
Ein externer Prüfer (z. B. Claude) soll zu **einem beliebigen Campus-/Projekt-/Fachthema** eine unabhängige Zweitmeinung geben, besitzt aber keine Git-/Repo-Werkzeuge.

Verbindlicher Weg:
`PAUL/READ_ONLY_REVIEW.md`

Regel:
- eine einzige allgemeingültige Außentür in der Paul-Etage;
- Prüfgegenstand = exakt das vom Nutzer genannte Thema;
- Standard = FACH-/INHALTSPRÜFUNG;
- Paul-/Campus-/Branch-/Routingarchitektur nur bei ausdrücklich verlangter SYSTEM-/ARCHITEKTURPRÜFUNG;
- externe Prüfung = READ/REVIEW ONLY;
- keine Kopie aktueller Fachwahrheit;
- Claude wird nicht zu Paul;
- Paul kann Claudes Befund anschließend verwenden.

Wenn die externe Umgebung auch öffentliche HTTPS-Links nicht öffnen kann:
STOPP → genau eine automatisch erzeugte Prüfkapsel für den genannten Prüfgegenstand; keine manuelle Mehrdatei-Übergabe.


## PB ONE – Präsentation / Werbung / Angebot / Flyer erstellen

Aktion:
Präsentation, Pitch, Werbung, Flyer, Angebotsunterlage, Leistungsdarstellung oder Vertriebsmaterial entwickeln.

Weg:
`PB_ONE/ANGEBOTE_FLYER/START_HERE.md`
→ `CURRENT_STATE.md`
→ `HOBBYRAUM.md`
→ Quellen
→ Entwurf
→ Freigabe
→ Unterlagenregister.

Keine Programmierung.

## PB ONE – gemeinsame Agenturarbeit

Aktion:
Ideen sammeln, mit Paul entwickeln, Konzepte ausarbeiten oder Unterlagen erstellen.

Weg:
- Überblick → `PB_ONE/ZENTRALREGISTER.md`
- Rohidee → `PB_ONE/IDEENWERKSTATT/START_HERE.md`
- Entwicklung → `PB_ONE/ENTWICKLUNGSRAUM/START_HERE.md`
- Arbeitsdokument/Präsentationsentwurf → `PB_ONE/ARBEITSDOKUMENTE/START_HERE.md`
- Preise/Pakete/Baukasten → `PB_ONE/AKTENSCHRANK/PREISE/START_HERE.md`
- Vertriebsabläufe/Lead-Management → `PB_ONE/AKTENSCHRANK/VERTRIEB/START_HERE.md`
- Präsentation/Werbung/Angebot/Flyer → `PB_ONE/ANGEBOTE_FLYER/START_HERE.md`

Nutzer und Paul haben in PB ONE dieselben redaktionellen Rechte.

Keine Programmierung in PB ONE.
Technische Umsetzung erst nach bewusster Übergabe an ein Projekt-/Fachbüro.


## PB ONE – Arbeitsdokument anlegen

Aktion:
Für eine Präsentation, einen Flyer, ein Konzeptpapier oder eine andere laufende Unterlage Punkte und Entwürfe sammeln.

Weg:
`PB_ONE/ARBEITSDOKUMENTE/START_HERE.md`
→ neue Akte nach Vorlage
→ Punkte/Entscheidungen/Entwürfe fortlaufend dort pflegen
→ nach Freigabe finales Ergebnis im zuständigen Register referenzieren.

Regel:
Eine laufende Unterlage = eine eigene Akte.
Register enthalten nur Verweise, nicht den vollständigen Inhalt.
Keine Programmierung.


## GitHub-Komplettsicherung / Backup

Aktion:
GitHub-Repository `hallo-netizen/affiliate-pferdeportal` regelmäßig vollständig sichern oder Wiederherstellbarkeit prüfen.

Verbindlicher Weg:
`TRESOR/START_HERE.md` → `TRESOR/KONZEPT.md` → `TRESOR/STATUS.md`.

HARD RULE:
**GitHub-Backup = GitHub only.**

Verboten ohne neuen ausdrücklichen Nutzerauftrag:
- WordPress dazunehmen;
- Projektarchiv dazunehmen;
- WP-Plugin als Backupweg bauen;
- eine dritte parallele Backup-Architektur erzeugen.

Verbindliche Sicherungsarchitektur:
- **Tresor automatisch:** wöchentlich sonntags 03:17 Europe/Berlin; technischer Branch `tresor/build-20260905`; bestehender Workflow `.github/workflows/campus-tresor-snapshot.yml`; externe PASS-Ablage unter `/Campus-Tresor/`.
- **Lokales Backup:** manuell per `GITHUB_BACKUP_STARTEN.command`; aktueller PASS-Stand `Schreibtisch/GitHub-Backup/GITHUB_BACKUP_AKTUELL.zip`.

Beide Wege sichern denselben GitHub-Projektbestand, sind aber unabhängig voneinander.

Prüfung/Wiederaufbau:
`TRESOR/PRUEFVERTRAG.md` + `TRESOR/NOTFALL_WIEDERAUFBAU.md`.

Backup/Mirror ist niemals Arbeitsquelle.

## PB ONE – selbstentwickelte Plugins finden

Aktion:
Geschäftlichen Überblick über bestätigte PB-ONE-Eigenentwicklungen/Plugins erhalten.

Weg:
`PB_ONE/AKTENSCHRANK/PLUGINS/START_HERE.md`
→ `REGISTER.md`
→ technische Hauptquelle.

Regel:
Kein zweiter Versions-/Release-/LIVE-Stand im PB-ONE-Pluginfach.


## PB ONE – Preise / Pakete / Baukasten

Aktion:
Website-Pakete, Zusatzmodule, Zahlungsmodell, Vorkasse oder Preislogik entwickeln bzw. nachschlagen.

Weg:
`PB_ONE/AKTENSCHRANK/PREISE/START_HERE.md`

Regel:
Entwurfswerte sind nicht automatisch verbindliche Kundenpreise.


## PB ONE – Vertriebsabläufe / Lead-Management

Aktion:
Kundendaten-Schnittstellen, Angebotsablauf, Sonderfälle, Onboarding, Lead-Zugänge oder Interessentenstatus klären bzw. nachschlagen.

Weg:
`PB_ONE/AKTENSCHRANK/VERTRIEB/START_HERE.md`

Offene Punkte:
`PB_ONE/AKTENSCHRANK/TODO/VERTRIEB_STARTKLAR_20260907.md`

Grenze:
LeadScout als Produkt/Plugin bleibt im Plugin-Fach; Preislogik im Preis-Fach; Verkaufsunterlagen im Präsentations-/Werbebereich.


## DESIGN – lokale Miniänderung / Elementtausch

Aktion:
Im Pferde-Atelier-DESIGN soll ein vorhandenes Element lokal verschoben oder mit einem direkt benachbarten Element getauscht werden.

Verbindlicher Weg:
`PROJEKTE/PFERDE_ATELIER/DESIGN/HOBBYRAUM.md`
→ `MINIMAL_PATCH_JOB_CURRENT.json`
→ `MINIMAL_PATCH_RUNNER.py`.

HARD RULE:
**Kein manueller Patchweg.**

Der Runner ist fail-closed und darf nur den im Job definierten minimalen Tausch auf der exakt hashgebundenen Baseline durchführen.

Kein neuer Plugin-Versionszähler pro Versuch.
Im Hobbyraum existiert nur `DESIGN_HOBBYRAUM_CANDIDATE.zip`.
Neue Releaseversion erst nach echtem LIVE-PASS.
