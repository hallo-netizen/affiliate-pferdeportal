# NOTFALL-TRESOR – PRÜFVERTRAG GITHUB

STAND: 2026-09-08
STATUS: VERBINDLICH

## GEMEINSAME HARD RULE

Kein Backup erhält PASS nur weil es erzeugt wurde.

PASS nur nach realer Prüfung des tatsächlich erzeugten Sicherungsstands.

## A. AUTOMATISCHER TRESOR

Pflicht je Lauf:
1. GitHub-Refs frisch abrufen.
2. Git-Bundle erzeugen und verifizieren.
3. Bundle isoliert als Mirror klonen.
4. `git fsck --full --strict`.
5. Quellrefs gegen Restore vergleichen.
6. Pflicht-Metadaten sichern, soweit GitHub sie exportierbar liefert.
7. Release-Artefakte sichern, soweit vorhanden/lesbar.
8. Endarchiv erzeugen und wieder lesen.
9. SHA-256 prüfen.
10. Erst nach erfolgreichem Lauf die neue datierte Datei extern unter `/Campus-Tresor/` speichern.
11. `LATEST_GITHUB_BACKUP.txt` erst danach auf den neuen PASS-Stand umstellen.
12. Bei FAIL alten gültigen Tresorstand unangetastet lassen.

## B. LOKALES BACKUP

Pflicht je Lauf:
1. aktuelle GitHub-Refs am Anfang binden;
2. Mirror + Bundle erzeugen;
3. `git fsck --full --strict`;
4. final erzeugte ZIP erneut öffnen;
5. innere Hashes prüfen;
6. aus genau dieser finalen ZIP in ein leeres Mirror-Repository restoren;
7. alle gesicherten Refs vergleichen;
8. Campus `protocol/PROJECT_MEMORY/**` per Pfad + Git-Blob-Hash vergleichen;
9. GitHub-Refs am Ende erneut lesen;
10. nur bei unverändertem Quellstand `GITHUB_BACKUP_AKTUELL.zip` ersetzen.

Änderung während des Laufs:
`BACKUP_FAIL:GITHUB_WAEHREND_BACKUP_GEAENDERT`.

## C. UNABHÄNGIGER LOKALER NOTFALLTEST

Die vorhandene `GITHUB_BACKUP_AKTUELL.zip` wird unabhängig vom Erzeugungslauf geprüft:

`ZIP-Hash → ZIP lesen → innere Hashes → Bundle verify → Mirror-Restore → git fsck → Refvergleich → Campus-Blobvergleich → Aktualitätsbindung`.

Realer Nutzer-Mac-Test 2026-09-08:
`NOTFALL_WIEDERAUFBAU_PASS`.

## STATUSBEGRIFFE

`GITHUB_REPOSITORY_RESTORE_PASS`:
Git und die gesicherten Refs sind real wiederherstellbar geprüft.

`GITHUB_DATEIEN_CAMPUS_1ZU1_RESTORE_PASS`:
Git-Dateien/Refs/Campus wurden aus der finalen lokalen ZIP real wiederhergestellt und verglichen.

`TRESOR_AUTO_BACKUP_REALTEST_PASS`:
automatischer Lauf + realer Restore + externe Ablage wurden erfolgreich geprüft.

`GITHUB_KOMPLETT_PASS`:
zusätzlich wäre ein vollständiger Neuaufbau aller erforderlichen exportierbaren GitHub-Metadaten/Einstellungen in einem leeren GitHub-Zielsystem real end-to-end nachzuweisen.

Dieser vollständige GitHub-Metadaten-Neuaufbau ist derzeit **nicht** als PASS belegt.

## PROVIDERGRENZE

GitHub-Secret-Werte sind nicht exportierbar.
Providerinterne IDs/Zeitstempel sind nicht garantiert identisch reproduzierbar.
Nicht lesbare Admin-Endpunkte müssen ausdrücklich als `UNAVAILABLE` dokumentiert bleiben.

## NEGATIVREGEL

Kein WordPress-Test.
Kein Website-Test.
Kein Projektarchiv-Test.
Kein PASS aufgrund eines alten Backups.
Kein `GITHUB_KOMPLETT_PASS` nur aufgrund eines erfolgreichen Git-/Campus-Restores.
