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

Finaler Trigger nach Campus-Korrektur:
`dd8028b81e21f99f6fcbbbe3832d1501e2ecd450`

Workflow Run:
`34199171706`

Ergebnis:
`SUCCESS`

Artifact:
`10045146430`

Exakte extern gespeicherte Datei:
`/Campus-Tresor/GITHUB_TRESOR_AUTO_2026-09-08_FINAL_072615Z.zip`

SHA-256:
`9356b1eafc3af3c8c3c3630ecdff08787bd2e7c58033abf460370d69bf7a337a`

Exakter Nachtest:
- äußere Hashprüfung PASS;
- innere Hashprüfung PASS;
- Git-Bundle verify PASS;
- Mirror-Clone PASS;
- `git fsck --full --strict` PASS;
- Campus-Dateien auf aktuellem Campus-Branch: 133;
- externer Upload nach `/Campus-Tresor/` PASS;
- Pointer `LATEST_GITHUB_BACKUP.txt` auf diesen Lauf aktualisiert.

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
