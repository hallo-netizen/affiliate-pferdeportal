# NOTFALL-TRESOR – STATUS

STAND: 2026-09-05

ERGEBNIS:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`

## Git-/Repository-Sicherung – PASS ALS PREPASS

Ein vollständiger externer Git-/GitHub-Metadaten-PREPASS wurde erzeugt und real restore-getestet.

Externer Speicher:
`/Campus-Tresor/`

Aktuellster Git-/Metadaten-PREPASS:
`/Campus-Tresor/LATEST_PREPASS.txt`

## Erster verbleibender Blocker

Das Campus-Archiv enthält weiterhin mehrere Rohbestände mit Ampel:
- GELB = nur ein unabhängiges Speichersystem;
- ROT = noch nicht vollständig roh gesichert/verifiziert.

Beleg:
`protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`

Nach dem Tresor-Inhaltsvertrag gehören relevante Artefakte zur vollständigen Rekonstruktion.

Solange die erforderlichen Roharchive nicht mindestens in einer zweiten unabhängigen verifizierten Ablage gesichert sind:

**KEIN TRESOR_PASS.**

## Danach bereits bekannter nächster Prüfpunkt

Nicht automatisch exportierbare Wiederherstellungsabhängigkeiten:
- Secrets/Schlüssel;
- externe Zugangsdaten;
- externe Autorisierungen.

Auch diese müssen später entweder sicher wiederherstellbar oder mit eindeutiger Recovery-Prozedur dokumentiert sein.

## Harte Regel

Der Tresor meldet immer den ersten belegten Blocker.

Git-/Metadaten-PREPASS ≠ vollständiger Katastrophen-PASS.


## Lokaler Backup-Befund 2026-09-05

Aktueller Library-Rohbestand:
- 38 Dateien;
- 985.708.251 Bytes;
- vollständig materialisiert;
- SHA-256 je Datei berechnet;
- Export-Restore 38/38 PASS.

Lokaler Export vorbereitet:
fünf Teile + Manifest + Restore-/Hashwerkzeug.

**Noch nicht als zweite unabhängige Ablage gezählt**, solange der Nutzer diese Dateien nicht tatsächlich lokal/external gespeichert und dort geprüft hat.

Der vorhandene Git-/GitHub-PREPASS V4 ist technisch restore-geprüft, bindet aber einen älteren Campus-/Paul-Stand und ist daher heute nur noch **Restore-Beweis**, nicht aktueller 1:1-Backupstand.

Real nachgewiesene nicht exportierbare Abhängigkeit:
`ENDSTEMPEL_PRIVATE_KEY`

GitHub enthält nur das Secret, nicht den auslesbaren Originalwert.
Recovery muss separat vorhanden und praktisch geprüft sein.

Bekannter Rohartefakt-Blocker bleibt außerdem:
Pferde-Design 1.50.472 – finale Plugin-/Master-ZIPs fehlen.

ERGEBNIS BLEIBT:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`
