# NOTFALL-TRESOR – INHALTSVERTRAG

STAND: 2026-09-05

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
