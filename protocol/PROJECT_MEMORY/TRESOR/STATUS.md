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
