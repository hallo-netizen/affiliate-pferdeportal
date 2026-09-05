# NOTFALL-TRESOR – START_HERE

STAND: 2026-09-05
STATUS: EXTERNER GIT-/METADATEN-PREPASS VORHANDEN / ROHARCHIV-REDUNDANZ BLOCKIERT TRESOR_PASS

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
