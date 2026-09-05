# NOTFALL-TRESOR – PRÜFVERTRAG

STAND: 2026-09-05

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
