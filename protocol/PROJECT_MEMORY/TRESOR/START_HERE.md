# NOTFALL-TRESOR – START_HERE

STAND: 2026-09-07
STATUS: EIN-DATEI-ZIEL V3 DEFINIERT / LOKALE AKTIVIERUNG + WORDPRESS-VOLLSTAND OFFEN / TRESOR_PASS BLOCKED

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Die Katastrophen-Wiederherstellung des gesamten Campus und Repositorys.

**HIER BIST DU RICHTIG, WENN …**  
der aktive Campus/GitHub-Stand verloren, beschädigt oder unzuverlässig ist oder ein neuer Backupstand erstellt werden soll.

**DU DARFST …**  
Konzept, Inhaltsvertrag, Prüfvertrag, aktuellen Tresorstatus und Wiederaufbauanleitung lesen.

**DU DARFST NICHT …**  
einen unvollständigen Backupstand als PASS bezeichnen oder einen älteren gültigen PASS überschreiben.

**ALS NÄCHSTES …**  
`STATUS.md`.

Danach:
- Backup erstellen → `KONZEPT.md` + `INHALTSVERTRAG.md` + `PRUEFVERTRAG.md` + `LOKALES_BACKUP_KONZEPT.md`
- Wiederaufbau → `NOTFALL_WIEDERAUFBAU.md`

## Aktueller Stand

Git-Mirror + GitHub-Metadaten + Git-Restore-Test:
PASS als externer PREPASS.

Vollständiger Tresor:
BLOCKED zuerst an noch nicht redundant gesicherten relevanten Roharchiven.

Danach verbleibt die Prüfung nicht exportierbarer Recovery-Abhängigkeiten.

## Harte Regel

Nur ein real geprüfter, externer, vollständiger Stand darf:
`TRESOR_PASS`
heißen.


## TRESOR IST NIE WERKBANK

Der Tresor und sein Git-Mirror sind ausschließlich Sicherungs-/Restorequellen.

Verboten:
- Runner/Tests/Reparaturen/Produktion direkt aus `/Campus-Tresor/`;
- Mirror als aktuellen Arbeitsstand verwenden;
- Worktree direkt an Tresor-Git-Metadaten hängen und darin arbeiten;
- Tresor als Ausweichroute bei BLOCKED benutzen.

Wiederherstellung endet erst nach Aufbau eines **frischen Arbeits-Worktrees außerhalb des Tresors** und erneutem normalen Eingangstest.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**

Autorität:
`protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md` → **Backup-/Tresor-/Archiv-Sperre**.



## Lokaler 1:1-Wiederaufbau

Verbindlicher lokaler Sicherungsweg:
`LOKALES_BACKUP_KONZEPT.md`

Der alte PREPASS ist Restore-Beweis, aber nach späteren Campusänderungen kein aktueller 1:1-Snapshot mehr.


## Aktuelles Download-Kit 2026-09-07

Aktuelles Mac-Kit:
`CAMPUS_LOCAL_TRESOR_KIT_20260907.zip`

Library:
`/Campus-Archiv/TRESOR_TOOLS/2026-09-07/`

SHA-256:
`74ebe867ddcb3920fe333f3d2bb31a9d7332bc03e0cd6c7a72a99f0a1bf033c6`

Das Kit enthält:
- Ein-Klick-Backupwerkzeug;
- Restorewerkzeug für die fünf Roharchivteile;
- Recovery-Vorlage;
- Mac-Startanleitung;
- Download-Checkliste;
- Testbeleg.

Nächster echter Schritt:
Kit + fünf Archivteile auf einen unabhängigen lokalen Datenträger herunterladen und dort Restore-/Hashprüfung ausführen.


## Ein-Klick-Automatisierung V2

Aktuelles Kit:
`CAMPUS_LOCAL_TRESOR_KIT_20260907_V2.zip`

Dauerhafte Library-Ablage:
`/Campus-Archiv/TRESOR_TOOLS/2026-09-07/`

SHA-256:
`bb5f28d26885fd8b58fd86bea3548375c97782f58581277daddd651b2151ca54`

Bevorzugter Start:
`START_CAMPUS_TRESOR.command`

Der Starter prüft/restauriert das Campus-Archiv bei Bedarf und startet danach automatisch die vollständige GitHub-/Campus-/Recovery-Sicherung.

Optional:
`AUTOMATIK_EINRICHTEN.command` richtet auf dem Mac eine tägliche oder wöchentliche Sicherung ein; Rhythmus und Stunde wählt der Nutzer selbst.


## Ein-Datei-Einstieg V3

Bevorzugter zukünftiger Nutzerweg:
- einmalig V3-Kit auf dem Mac einrichten;
- automatischer lokaler Campus-Snapshot;
- automatische verschlüsselte Ein-Datei-Kapsel;
- Upload als Release in privaten GitHub-Tresor;
- lokale Kopie behalten.

Kein alter Mehrdatei-Stand darf dadurch rückwirkend als `TRESOR_PASS` gelten.
