# NOTFALL-TRESOR – STATUS

STAND: 2026-09-08

## GESAMTSTATUS

Tresor-Automatik:
**AKTIV + REAL GETESTET**

Lokales Ein-Klick-Backup:
**WERKZEUG V2 HART GETESTET / REALER MAC-LAUF NOCH AUSSTEHEND**

## TRESOR – AUTOMATISCH

Zeitplan:
**sonntags 03:17 Europe/Berlin**

Unabhängig vom Nutzer-Mac:
**JA**

Auslöser:
Scheduler aktualisiert
`control/tresor/AUTO_TRIGGER.txt`
auf
`tresor/build-20260905`.

Dadurch startet:
`Campus GitHub Complete Backup`.

Externer Speicher:
`/Campus-Tresor/`

Aktueller Pointer:
`/Campus-Tresor/LATEST_GITHUB_BACKUP.txt`

## REALER AUTOMATIK-TEST 2026-09-08

Trigger-Commit:
`25e4c462b2a93447a8ca3be68e6ae2942b4dd4b6`

Workflow Run:
`34198674940`

Ergebnis:
`SUCCESS`

Artifact:
`10044960646`

Exakte heruntergeladene Datei:
`GITHUB_TRESOR_AUTO_2026-09-08_072023Z.zip`

SHA-256:
`0d8a7e06813e363784c46289ea92e2e43bab48251e1e892d08a39a6971e43b38`

Zusätzlich extern unter
`/Campus-Tresor/GITHUB_TRESOR_AUTO_2026-09-08_072023Z.zip`
abgelegt.

Exakter Nachtest:
- äußere Hashprüfung PASS;
- innere Hashprüfung PASS;
- Git-Bundle verify PASS;
- Mirror-Clone PASS;
- `git fsck --full --strict` PASS;
- Campus-Dateien auf aktuellem Campus-Branch: 133.

Ergebnis:
`TRESOR_AUTO_BACKUP_REALTEST_PASS`

## LOKALES BACKUP

Werkzeug:
`GITHUB_BACKUP_STARTEN.command`

Feste aktuelle Datei:
`Schreibtisch/GitHub-Backup/GITHUB_BACKUP_AKTUELL.zip`

V2-Test:
- Bash-Syntax PASS;
- exakte finale ZIP erneut geöffnet PASS;
- Restore aus finaler ZIP PASS;
- Campus byteidentisch PASS;
- Negativtest Änderung während Lauf korrekt BLOCK.

Nächster realer Schritt:
Mac-Lauf mit Doppelklick.

## PROVIDERGRENZE

Nicht 1:1 aus GitHub exportierbar:
- Secret-Werte;
- einzelne interne Admininformationen;
- identische GitHub-interne IDs/Zeitstempel bei Neuaufbau.
