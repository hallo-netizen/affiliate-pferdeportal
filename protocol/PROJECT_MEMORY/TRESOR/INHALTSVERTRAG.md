# NOTFALL-TRESOR – INHALTSVERTRAG

STAND: 2026-09-07

Ein Tresorstand darf nur `TRESOR_PASS` heißen, wenn alle zum Sicherungszeitpunkt bekannten Wiederherstellungsbestandteile erfasst sind.

## A. Git vollständig

Pflicht:
- Repository-Mirror;
- komplette Commit-Historie;
- main;
- alle Branches;
- alle Tags;
- alle erreichbaren Git-Objekte, die zur Wiederherstellung benötigt werden.

Paul-Branches zählen ausdrücklich dazu.

## B. Projektgedächtnis vollständig

Pflicht:
- Hauptpförtner;
- alle Projektgebäude;
- alle Büros;
- alle CURRENT_STATE;
- alle Hobbyräume;
- Handlungsverzeichnis;
- Fehlerregister;
- Änderungs-/Erklärungsregister;
- Baucontainer;
- Paul-Regeln und Paul-Aufträge;
- SAFE_POINTS / Wiederherstellungspunkte, sobald eingeführt.

## C. Projektdateien vollständig

Pflicht:
- Quellcode;
- Workflows;
- Regeln;
- Protokolle;
- Konzepte;
- Ideen und Entscheidungen, soweit sie im Projekt abgelegt sind;
- Test- und Regressionsevidenz;
- Release-/Runtime-/Governance-Dateien;
- relevante Artefakte, soweit sie zur Rekonstruktion benötigt werden.

## D. GitHub-Zustand

Soweit über die GitHub-Schnittstellen auslesbar und für Wiederaufbau relevant:
- Issues;
- Pull Requests;
- Releases;
- Rulesets;
- erforderliche Repository-/Schutzinformationen;
- Zuordnung aktiver Arbeitsbranches und offener Baustellen.

## E. Nicht automatisch exportierbare Abhängigkeiten

Beispiele:
- geheime Schlüssel/Secrets;
- externe Zugangsdaten;
- externe Autorisierungen oder Verbindungen, deren Originalwert nicht aus GitHub ausgelesen werden kann.

Regel:
Solche Bestandteile dürfen **nicht stillschweigend fehlen**.

Für jeden muss entweder:
1. eine sichere wiederherstellbare Quelle vorhanden sein, oder
2. eine eindeutige Wiederherstellungsprozedur dokumentiert sein.

Fehlt beides:
`TRESOR_FAIL_NONRECOVERABLE_DEPENDENCY`

## F. Manifest

Jeder Tresorstand benötigt ein maschinenlesbares Manifest mit mindestens:
- Erstellungszeitpunkt;
- Repository;
- main-SHA;
- Anzahl/IDs der Branches und Tags;
- Projektgebäude;
- Dateien/Artefakte mit Hashes;
- GitHub-Metadaten-Snapshot;
- bekannte nicht automatisch exportierbare Abhängigkeiten;
- Prüfergebnis;
- Tresorstatus.

## Harte Regel

`UNGEKLÄRT` ist kein PASS.

Was für den Wiederaufbau relevant sein könnte, aber nicht eindeutig gesichert oder ausgeschlossen ist, blockiert den vollständigen Tresor-PASS.


## G. Lokale unabhängige Wiederherstellungskopie

Für einen vollständigen Tresor-PASS reicht die ChatGPT-Library allein nicht.

Pflicht:
- relevante Library-Roharchive zusätzlich auf einem unabhängigen lokalen Speicher;
- Hashgleichheit belegt;
- lokale Kopie Bestandteil eines versionierten Tresorsnapshots.

## H. Recovery-Geheimnisse

Aktuell technisch konkret belegt:
- `ENDSTEMPEL_PRIVATE_KEY` als GitHub Actions Secret.

Der Originalwert ist über GitHub nicht exportierbar.
Der Tresor darf deshalb nur PASS liefern, wenn dafür außerhalb GitHub eine sichere und praktisch getestete Recovery-Quelle existiert.

Keine Secret-Werte in PROJECT_MEMORY, GitHub oder Chat protokollieren.


## I. Geschlossene Ein-Datei-Kapsel

Für den neuen Zielzustand gilt zusätzlich:

Ein `TRESOR_PASS` darf nur vergeben werden, wenn **eine einzige verschlüsselte Recovery-Datei** alle Wiederherstellungsbestandteile enthält.

Keine Pflichtdatei darf nur:
- in der ChatGPT-Library;
- auf einem alten lokalen Datenträger;
- in einem zweiten GitHub-Repository;
- auf dem WordPress-Server;
- in einem separaten Downloadpaket

liegen und trotzdem für den Restore benötigt werden.

Externe Quellen dürfen beim Erzeugen der Kapsel verwendet werden.
Nach Abschluss muss die Kapsel selbst geschlossen sein.

## J. Campus-Referenzschluss

Jede Campusreferenz auf Rohartefakte wird gegen die Kapsel geprüft.

Regel:
**Campus verweist auf Datei → Datei muss in der Kapsel enthalten oder nachweislich als nicht wiederherstellungsrelevant klassifiziert sein.**

`UNGEKLÄRT` blockiert weiterhin `TRESOR_PASS`.

## K. GitHub-Kollaborationshistorie

Zur Informationsvollständigkeit werden soweit über GitHub exportierbar zusätzlich archiviert:
- Issue-Kommentare;
- PR-Reviews;
- PR-Review-Kommentare;
- Milestones;
- Release-Artefakte;
- ursprüngliche IDs, Nummern und Zeitstempel.

Beim Restore können providerinterne IDs neu entstehen.
Der Originaldatensatz bleibt dennoch vollständig im Tresor erhalten.

## L. WordPress-Vollstand

Für den Gesamt-`TRESOR_PASS` reicht ein WordPress-Export-XML nicht.

Pflicht:
- Datenbankdump;
- komplette WordPress-Dateien einschließlich Uploads;
- Plugins/Themes;
- relevante Laufzeit-/Serverkonfiguration;
- benötigte Recovery-/Zugangsinformationen.
