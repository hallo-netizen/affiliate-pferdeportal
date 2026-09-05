# NOTFALL-TRESOR – STATUS

STAND: 2026-09-05

ERGEBNIS:
`TRESOR_FAIL:RECOVERY_DEPENDENCIES_UNVERIFIED`

## Git-/Repository-Sicherung – PASS ALS PREPASS

Ein vollständiger externer Git-/GitHub-Metadaten-PREPASS wurde erzeugt und real restore-getestet.

Externer Speicher:
`/Campus-Tresor/`

Der jeweils aktuellste belastbare PREPASS wird **außerhalb des aktiven Repositorys** über:
`/Campus-Tresor/LATEST_PREPASS.txt`
gebunden.

Warum extern:
Ein im Campus selbst hart eingetragener „neuester Snapshot-Hash“ würde bei jeder Aktualisierung einen neuen Campus-Commit erzeugen und damit den Snapshot sofort wieder veralten lassen.

## Was ein gültiger Git-/Metadaten-PREPASS enthalten muss

- vollständigen Git-Bundle-Mirror;
- alle Branches;
- alle Tags;
- vollständige Commit-Historie;
- Campus-Branch;
- Paul-Branches;
- GitHub-Metadaten;
- Ruleset-/Schutzinformationen;
- Manifest + Hashes;
- realen Git-Bundle-Restore-Test.

Die konkreten SHAs, Counts und Hashes stehen im externen PREPASS-Manifest.

## Erster verbleibender Blocker

Noch NICHT hart verifiziert:
alle nicht automatisch exportierbaren Wiederherstellungsabhängigkeiten, insbesondere Secrets/Schlüssel/externe Autorisierungen.

Der Inhaltsvertrag verlangt für jede solche Abhängigkeit entweder:
1. sichere wiederherstellbare Quelle oder
2. eindeutige Wiederherstellungsprozedur.

Bis diese Prüfung abgeschlossen ist:

**KEIN TRESOR_PASS.**

## Harte Regel

Ein Git-/Metadaten-PASS allein ist noch kein vollständiger Katastrophen-PASS.

Nur der externe, manifestgebundene PREPASS plus vollständig geprüfte Recovery-Abhängigkeiten und abschließende Tresor-Abnahme dürfen später zu einem versionierten `TRESOR_PASS` werden.
