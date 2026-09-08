# NOTFALL-TRESOR – STATUS

STAND: 2026-09-08

## AUFTRAG

**GITHUB ONLY**

Repository:
`hallo-netizen/affiliate-pferdeportal`

Ziel:
regelmäßig per Doppelklick einen frischen, restore-geprüften GitHub-Backupstand erzeugen.

## AKTUELLER NUTZERWEG

Ein Werkzeug:
`GITHUB_BACKUP_STARTEN.command`

Nutzeraktion:
**doppelklicken.**

Ergebnis auf dem Mac:
`Schreibtisch/GitHub-Backup/GITHUB_BACKUP_AKTUELL.zip`

Zusätzlich bleibt jeder datierte PASS-Stand erhalten.

## AKTUALITÄT – HARD GATE

Vor dem Backup werden die aktuellen GitHub-Refs gebunden.

Nach Erstellung und Restore-Test werden die GitHub-Refs erneut gelesen.

Wenn sich GitHub während des Laufs verändert hat:
`BACKUP_FAIL:GITHUB_WAEHREND_BACKUP_GEAENDERT`

Dann:
- kein PASS;
- `GITHUB_BACKUP_AKTUELL.zip` wird nicht ersetzt;
- alter letzter gültiger Stand bleibt bestehen.

Nur wenn Anfangs- und Endrefs identisch sind:
`AKTUELLITAET_PASS`.

## RESTORE – HARD GATE

Vor PASS wird aus der **finalen ZIP-Datei selbst** wiederhergestellt und geprüft:

- Git-Bundle verify;
- Mirror-Clone;
- `git fsck --full --strict`;
- alle gesicherten Heads/Tags/Pull-Refs identisch;
- Campus `protocol/PROJECT_MEMORY/**` per Pfad + Git-Blob-Hash identisch.

PASS:
`GITHUB_DATEIEN_CAMPUS_1ZU1_RESTORE_PASS`

## REALER GITHUB-TEST 2026-09-08

GitHub Actions Run:
`34160894135`
Attempt:
`3`
Ergebnis:
`SUCCESS`

Frischer Snapshot:
- Branches: 293;
- main SHA: `36d1ecb52cf80c91e2f30f5a1eb7ecc1f14782c9`;
- Campus-Branch SHA: `abd5f78d71eae6f277714beb4569b12eee36a115`;
- Campus-Dateien auf diesem Branch: 133.

Direkter GitHub-Abgleich nach dem Lauf:
- Branchanzahl: 293 → identisch;
- main SHA → identisch;
- Campus SHA → identisch.

Restore aus dem erzeugten Bundle:
- Hashprüfung PASS;
- Bundle verify PASS;
- Mirror-Clone PASS;
- `git fsck --full --strict` PASS.

## EXAKTER WERKZEUGTEST V2

- Bash-Syntax PASS;
- exakte finale ZIP erzeugt und wieder eingelesen PASS;
- Git-Restore aus genau dieser ZIP PASS;
- Campus byteidentisch PASS;
- Negativtest: GitHub-Änderung während Backup → korrekt BLOCK;
- bei Negativtest wurde keine `GITHUB_BACKUP_AKTUELL.zip` erzeugt/ersetzt.

## GRENZE

Für Git-Dateien, Historie, Branches, Tags, Pull-Refs und den im Repository liegenden Campus gilt der oben geprüfte 1:1-Restore.

Nicht 1:1 aus GitHub exportierbar:
- Secret-Werte;
- einzelne providerinterne Admininformationen;
- identische GitHub-interne IDs/Zeitstempel bei Neuaufbau.

Diese Grenze darf nicht als Datei-/Campus-Restore-PASS ausgegeben werden.

## AUTOMATIK

Keine separate ChatGPT-/WordPress-Automatik aktiv.

Der aktuelle KISS-Weg ist bewusst:
**Doppelklick → frisches Backup → harte Aktualitäts- und Restore-Prüfung.**
