# CAMPUS-ARCHIV

STAND: 2026-09-05
STATUS: AKTIV

## 1-KLICK-ÜBERSICHT

**WAS IST DAS?**  
Der historische Aktenraum des Campus.

**HIER BIST DU RICHTIG, WENN …**  
du alte Masterstände, Übergaben, Pluginstände, Protokolle, Exporte oder andere historische Belege suchst.

**DU DARFST …**  
historische Akten lesen, über Register finden und ihre Archiv-/Hash-Angaben prüfen.

**DU DARFST NICHT …**  
ARCHIVIERT mit „falsch“ oder „löschbar“ gleichsetzen, UNGEKLÄRT wegarchivieren oder Fachinhalte umschreiben.

**ALS NÄCHSTES …**  
`REGISTER.md` für vorhandene Bestände; `DATEIEINGANG.md` für neue Akten.

## Harte Regel

ARCHIVIERT bedeutet:
**historisch, nicht aktuelle Hauptwahrheit.**

Es bedeutet NICHT:
- unwichtig;
- falsch;
- automatisch löschbar.

## Archiv-Ampel

ROT / GELB / GRÜN steht in `REGISTER.md`.

Nur GRÜN darf bedeuten:
`LOKALE_KOPIE_ENTBEHRLICH: JA`.


## EINE WAHRHEIT – ARCHIV IST NIE CURRENT

Das Archiv ist ausschließlich historische Ablage und Belegraum.

Für den **aktuellen** Stand immer zurück zum zuständigen:
- Büro-`CURRENT_STATE.md`, oder
- Modul-`CURRENT_STATE.md`.

`ARCHIV/REGISTER.md` darf keine aktuelle Fachwahrheit ersetzen.
Ein historischer Stand wird niemals allein durch „neuere Dateigröße/Version“ wieder aktuell.


## ARCHIV IST NIE WERKBANK

Archivierte Dateien dürfen untersucht, verglichen und als historische Belege genutzt werden.

Sie dürfen **nicht direkt ausgeführt** werden:
kein Runner, Test, Release, Reparatur- oder Produktionslauf aus `Campus-Archiv`.

Soll ein historischer Stand Wiederherstellungsbasis sein:
erst über den Tresor-/Restoreweg in einen frischen offiziellen Arbeits-Worktree überführen und dort neu verifizieren.

## Globale Arbeitsort-Sperre

**Tresor, Archiv, Backup und Git-Mirror sind niemals Werkbank oder Runner-Quelle.**

Autorität:
`protocol/PROJECT_MEMORY/BAUCONTAINER/EINGANGSSTANDARD.md` → **Backup-/Tresor-/Archiv-Sperre**.

