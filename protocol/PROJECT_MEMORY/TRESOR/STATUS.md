# NOTFALL-TRESOR – STATUS

STAND: 2026-09-08

## GESAMTSTATUS

Tresor-Automatik:
**AKTIV + REAL GETESTET**

Lokales Ein-Klick-Backup:
**REALER MAC-BACKUPSTAND + UNABHÄNGIGER NOTFALL-RESTORE PASS**

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

## PROVIDERGRENZE

Nicht 1:1 aus GitHub exportierbar:
- Secret-Werte;
- einzelne interne Admininformationen;
- identische GitHub-interne IDs/Zeitstempel bei Neuaufbau.


## REALER LOKALER MAC-TEST 2026-09-08

Erzeugter Stand:
`2026-09-08_09-33-26`

Belegt:
- äußerer ZIP-Hash gegen `.sha256` + Info PASS;
- ZIP vollständig lesbar PASS;
- innere Hashes PASS;
- Backup-Info meldet 294 Branches, 1 Tag, 176 Pull-Refs, 4 Campus-Branches, 474 Campus-Dateieinträge;
- Aktualitätsbindung meldet `PASS_GITHUB_REFS_AM_ENDE_UNVERAENDERT`.

Der erste unabhängige Prüfer V2 scheiterte danach fälschlich bei `BUNDLE_VERIFY`, weil `git bundle verify` ohne Git-Repository-Kontext aufgerufen wurde.

Korrektur:
Prüfer V3 erzeugt dafür ein separates leeres Test-Repository; dieser Fix ist lokal positiv getestet.

## UNABHÄNGIGER NOTFALL-ENDTEST V3 – REALER MAC-LAUF PASS

Exakt derselbe vorhandene lokale Backupstand wurde mit Prüfer V3 unabhängig geprüft.

Realer Nutzerlauf:
- äußerer ZIP-Hash gegen `.sha256` + Info PASS;
- ZIP vollständig lesbar PASS;
- innere Hashes PASS;
- Git-Bundle im separaten Test-Repository verify PASS;
- echter Mirror-Restore PASS;
- `git fsck --full --strict` PASS;
- alle gesicherten Refs identisch PASS;
- Campus bytegenau identisch PASS;
- Aktualitätsbindung über SHA256 PASS.

Endergebnis:
`NOTFALL_WIEDERAUFBAU_PASS`

Damit ist für den lokalen Stand 2026-09-08_09-33-26 der Wiederaufbau der gesicherten Git-Dateien, Historie, Refs und Campus-Dateien real auf dem Nutzer-Mac nachgewiesen.

Providergrenze bleibt unverändert:
GitHub-Secret-Werte und einzelne providerinterne Informationen sind nicht 1:1 exportierbar.

NEXT ACTION:
Kein weiterer Test dieses identischen lokalen Backupstands erforderlich. Nächster lokaler Lauf erst bei gewünschter Aktualisierung per Doppelklick.


## GESAMT-GITHUB-RESTOREGRENZE

Real bewiesen:
- Git-Dateien;
- komplette Git-Historie;
- gesicherte Branch-/Tag-/Pull-Refs;
- Campus-Dateien im Repository.

Exportiert, aber noch **nicht** als vollständiger Neuaufbau in ein leeres GitHub-Zielrepository end-to-end eingespielt:
- Issues/Kommentare/Events;
- Pull-Request-Metadaten/Reviews;
- Releases/Labels/Milestones;
- Rulesets/Workflows/Deployments und weitere exportierbare GitHub-Metadaten.

Darum bleibt für einen vollständigen GitHub-Neuaufbau:
`GITHUB_KOMPLETT_PASS` **OFFEN**.

Das reale lokale Ergebnis
`NOTFALL_WIEDERAUFBAU_PASS`
bezieht sich auf den tatsächlich ausgeführten Git-/Ref-/Campus-Wiederaufbau, nicht auf eine erfundene 1:1-Reproduktion providerinterner GitHub-Objekte.
