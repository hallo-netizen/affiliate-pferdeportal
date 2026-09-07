# NOTFALL-TRESOR – PRÜFVERTRAG

STAND: 2026-09-07

## Ziel

Nicht „Backup erstellt“, sondern:
**Backup nachweislich vollständig genug für den Wiederaufbau.**

## Vor jedem lokalen Backup

Der Tresorprozess muss zuerst den aktuellen Projektstand neu erfassen.

Kein alter Inventarstand darf ungeprüft als aktuell übernommen werden.

## Pflichtprüfungen

Mindestens:

- aktueller main-SHA gebunden;
- vollständige Branchliste erfasst;
- vollständige Tagliste erfasst;
- Paul-Branches erfasst;
- Git-Mirror vorhanden;
- PROJECT_MEMORY vollständig;
- alle registrierten Projektgebäude vorhanden;
- alle registrierten Büros vorhanden;
- CURRENT_STATE/Hobbyraum je aktivem Büro erfasst;
- Fehlerregister vorhanden;
- Änderungs-/Erklärungsregister vorhanden;
- Baucontainer vorhanden;
- Handlungsverzeichnis vorhanden;
- relevante GitHub-Metadaten exportiert;
- Ruleset-/Schutzinformationen erfasst;
- Manifest-Hashes stimmen;
- keine bekannte Wiederherstellungsabhängigkeit ungeklärt.

## Ergebnis

Nur zwei gültige Endzustände:

`TRESOR_PASS`
oder
`TRESOR_FAIL:<ERSTER_FEHLER>`

Kein Teil-PASS wird als vollständige Sicherung bezeichnet.

## Wiederherstellungstest

Ein Tresor ist erst wirklich vertrauenswürdig, wenn die Wiederherstellung praktisch geprüft wurde.

KISS-Regel:
- jeder Backup-Lauf: vollständiger Inhalts-/Hash-/Inventarcheck;
- regelmäßig und nach wesentlichen Architekturänderungen: echter Wiederherstellungstest in isolierter Umgebung.

Der letzte erfolgreich getestete Wiederaufbau wird im Tresormanifest referenziert.

## Versionierung

Jeder PASS-Stand bekommt einen neuen unveränderlichen Ordner/Container.

Beispiel:
`TRESOR/2026-09-05_1130/`

Nie einen früheren PASS-Stand überschreiben.


## Lokaler Snapshot – Pflichtprüfung

Jeder lokale Snapshot muss zusätzlich beweisen:
- Git-Mirror erzeugt;
- Bundle erzeugt und verifiziert;
- Restore aus Bundle real durchgeführt;
- alle Git-Refs Quelle/Restore identisch;
- GitHub-Metadatenexport vollständig oder fail-closed;
- lokale Campus-Archivkopie Hash-für-Hash identisch;
- Recovery-Inventar vollständig;
- gesamte Recovery praktisch getestet;
- Snapshot unveränderlich/versioniert abgelegt.

Negativ:
- fehlendes Archiv → BLOCK;
- Hashabweichung → BLOCK;
- fehlende Ruleset-/Schutzmetadaten → BLOCK;
- nicht bestätigte Recovery → BLOCK.

Ein alter PREPASS darf nicht als aktueller Snapshot wiederverwendet werden.


## Ein-Datei-Abnahme

Der neue Zielzustand verschärft die Abnahme:

### Positiv

Ein isolierter Wiederaufbau wird ausschließlich aus:
1. genau **einer** verschlüsselten Recovery-Datei und
2. dem Masterpasswort

durchgeführt.

Der Test muss mindestens beweisen:
- Git-Historie/Branches/Tags vollständig;
- Campusdateibaum vollständig;
- alle als recovery-relevant registrierten Rohakten vorhanden;
- GitHub-Metadatenarchiv vollständig;
- WordPress-Dateien + Datenbank vorhanden und technisch restorefähig;
- Recovery-Sektion vorhanden und entschlüsselbar;
- Manifest/Hashes PASS.

### Negativ

Jeder dieser Fälle blockiert:
- benötigte Datei nur extern referenziert;
- ein Roharchiv fehlt;
- Git-Ref fehlt;
- Release-Artefakt fehlt, obwohl recovery-relevant;
- WordPress-Datenbank oder wp-content fehlt;
- benötigtes Secret nur als GitHub-Secret-Name bekannt;
- Kapsel kann nicht entschlüsselt/verifiziert werden.

### Endregel

**Kein simulierter Teiltest darf `TRESOR_PASS` erzeugen.**

Erst ein echter isolierter Wiederaufbau ausschließlich aus der einen Recovery-Datei darf:
`TRESOR_PASS`
setzen.


## V4-Testmatrix

Vor jedem echten End-to-End-Test muss:
`TEST_VORBEREITUNG_PRUEFEN.command`
exakt `TRESOR_TEST_READY` liefern.

### Sicherer lokaler Test

`TEST_ALLES.command` muss:
- frischen Git-/GitHub-/Campus-Snapshot erzeugen;
- vollständige Ein-Datei-Kapsel erzeugen;
- dieselbe Kapsel in ein leeres temporäres Verzeichnis entschlüsseln;
- Payload-Hashes prüfen;
- Git aus Bundle neu aufbauen;
- Git-FSCK durchführen;
- alle gespeicherten Source-Refs vergleichen;
- Hauptpförtner im wiederhergestellten Gitbestand nachweisen;
- Campus-Archivmanifest nachweisen;
- Pflichtklassen der GitHub-Metadaten nachweisen;
- Recovery-Bestätigung nachweisen;
- WordPress-Backupvertrag und Hashes prüfen.

Ergebnis:
`TRESOR_LOCAL_ONEFILE_TEST_PASS`.

### Echter GitHub-Neuaufbau

`TEST_GITHUB_NEUAUFBAU.command` darf ausschließlich ein separates privates Test-Repository verwenden.

Pflicht:
- produktives Repository unangetastet;
- neues Test-Repository vorher nicht vorhanden;
- Push aus der Recovery-Kapsel;
- erneuter Clone aus GitHub;
- Vergleich aller Heads und Tags mit dem gesicherten Original.

Ergebnis:
`GITHUB_RESTORE_TEST_PASS`.

### GitHub-Informationsarchiv V4

Pflichtklassen umfassen zusätzlich:
- Issue-Kommentare;
- PR-Review-Kommentare;
- PR-Reviews;
- Milestones;
- Release-Artefakte;
- Deployments soweit exportierbar.

### WordPress

Ein vollständiger WordPress-Teststand muss mindestens enthalten:
- `database.sql.gz`;
- `wordpress-files.tar.gz`;
- `WORDPRESS_MANIFEST.json`;
- `WORDPRESS_COMPLETE.flag`.

`WORDPRESS_BACKUP_PRUEFEN.command` muss PASS liefern.

Ein XML-Export allein reicht weiterhin nicht.

### Kryptografie

Der echte Mac-Test muss zusätzlich beweisen:
- 7-Zip AES-256/Header-Verschlüsselung erzeugt die Kapsel;
- falsches Passwort blockiert;
- beschädigte Kapsel blockiert;
- korrektes Masterpasswort entschlüsselt und verifiziert.

Ohne diesen realen Kryptotest kein End-to-End-`TRESOR_PASS`.
