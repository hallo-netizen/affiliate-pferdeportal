# NOTFALL-TRESOR – START_HERE

STAND: 2026-09-07
STATUS: EIN-DATEI-ZIEL / AUTOMATISCHE ERZEUGUNG NOCH NICHT PRODUKTIV / TRESOR_PASS BLOCKED

## FÜR DEN NUTZER

Der Nutzerweg ist absichtlich nur:

**GitHub → Releases → neueste Datei mit `TRESOR_PASS` herunterladen → lokal speichern.**

Mehr nicht.

Der Nutzer:
- startet keine Backup-Skripte;
- führt keine Terminal-Kommandos aus;
- setzt keine Einzelarchive zusammen;
- prüft keine Hashlisten manuell;
- baut keine Testumgebung selbst.

Alle technischen Werkzeuge, Tests und alten Mac-Kits sind **interne Tresor-Technik** und kein Nutzerweg.

## ZIEL

Regelmäßig wird automatisch genau **eine verschlüsselte Komplettsicherung** erzeugt.

Beispiel:
`PB_ONE_KOMPLETTSICHERUNG_2026-09-07-0317.tar.gz.gpg`

Sie darf nur als `TRESOR_PASS` bereitgestellt werden, wenn sie nachweislich für den vollständigen Wiederaufbau ausreicht.

Pflichtinhalt:
- kompletter GitHub-Campus;
- vollständige Git-Historie, Branches und Tags;
- alle benötigten Roh-/Masterdateien;
- relevante GitHub-Metadaten;
- vollständiger WordPress-Stand;
- notwendige Recovery-Daten;
- Wiederaufbauwerkzeuge und Manifest.

## FESTER DOWNLOAD-ORT

Bevorzugt wird der bestehende GitHub-**Releases**-Bereich genutzt.

Warum:
- kein zweites Repository nötig;
- versionierte Sicherungen;
- eine Datei pro Sicherungsstand;
- ältere PASS-Stände bleiben erhalten;
- für den Nutzer ein klarer Download-Ort.

Release-Schema:
`tresor-YYYY-MM-DD-HHMM`

Asset:
`PB_ONE_KOMPLETTSICHERUNG_YYYY-MM-DD-HHMM.tar.gz.gpg`

## HARTE REGEL

Eine Datei ohne realen vollständigen Restore-Beweis darf **nicht** `TRESOR_PASS` heißen und wird dem Nutzer nicht als gültige Komplettsicherung angeboten.

## INTERN

Technische Hauptquellen:
- `KONZEPT.md`
- `INHALTSVERTRAG.md`
- `PRUEFVERTRAG.md`
- `LOKALES_BACKUP_KONZEPT.md`
- `NOTFALL_WIEDERAUFBAU.md`
- `STATUS.md`

Tresor/Archiv/Backup bleiben READ/VERIFY/RESTORE ONLY und niemals Werkbank.
