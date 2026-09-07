# NOTFALL-TRESOR – KONZEPT

STAND: 2026-09-07
STATUS: KONZEPT V2 – EIN-DATEI-DISASTER-RECOVERY

## Ziel

Der Tresor ist die vollständige Katastrophen-Wiederherstellungskapsel des gesamten Campus.

Aus einem gültigen Tresorstand muss ein neuer Mensch oder Chat **ohne Vorwissen** den gesicherten Projektstand wieder aufbauen können:
- vollständige Git-Historie;
- main, alle Branches und Tags;
- alle Projektgebäude;
- alle Büros, Hobbyräume und Paul-Arbeitsstände;
- Hauptpförtner;
- Handlungsverzeichnis;
- Fehlerregister;
- Änderungs-/Erklärungsregister;
- Baucontainer;
- Konzepte, Ideen, Regeln und Workflows im Projekt;
- relevante GitHub-Metadaten und Schutzregeln;
- aktueller verifizierter Arbeitsstand;
- sichere Wiederherstellungsanleitung.

## Grundsatz

Der Tresor ist **keine zweite lebende Projektwelt** und steuert nichts.

Er wird aus dem aktuellen Projektstand erzeugt, geprüft, abgeschlossen und danach unveränderlich gesichert.

## Backup-Ablauf

1. aktuellen Campus-/Repositoryzustand erfassen;
2. exakte Git- und GitHub-Quellenstände binden;
3. vollständigen Tresorstand neu erzeugen;
4. Inventar und Manifest erzeugen;
5. Vollständigkeit und Hashes prüfen;
6. Wiederherstellbarkeit prüfen;
7. nur bei vollständigem PASS den Stand als `TRESOR_PASS` markieren;
8. neuen versionierten Tresorstand lokal sichern;
9. ältere gültige Tresorstände nicht überschreiben.

## Sicherheitsregel

Ein Fehler im aktiven Gebäude darf einen früheren gültigen Tresorstand niemals automatisch überschreiben.

Darum:
- jeder Tresorstand ist versioniert;
- gültige ältere Stände bleiben erhalten;
- „live spiegeln und überschreiben“ ist verboten.

## Externer Speicherort

Der produktive Tresor soll außerhalb des aktiven Repositorys liegen.

Im Repository liegen nur:
- Tresorkonzept;
- Inhaltsvertrag;
- Prüfvertrag;
- Wiederaufbauanleitung.

Der spätere lokale Backup-Klick sichert den extern erzeugten Tresorstand.


## Verbindlicher Zielzustand – eine Recovery-Datei

Der bevorzugte vollständige Tresorstand ist **eine einzige verschlüsselte Disaster-Recovery-Datei**.

Aus dieser einen Datei muss – zusammen mit dem vom Nutzer bekannten Masterpasswort, aber ohne weitere Projektdateien – der komplette gesicherte Systemstand wieder aufgebaut werden können.

Pflichtinhalt der Kapsel:

1. **Git vollständig**
   - kompletter Repository-Mirror;
   - vollständige Commit-Historie;
   - main;
   - alle Branches;
   - alle Tags;
   - notwendige Git-LFS-Objekte;
   - Submodule nur, wenn sie vollständig eingebunden und gesichert sind.

2. **GitHub-Campus vollständig**
   - gesamtes `protocol/PROJECT_MEMORY/**`;
   - alle Projektgebäude, Büros, Hobbyräume, Register, Zielverträge, Fehlerquellen, Archiveinträge, Baucontainer, Paul-Regeln und Arbeitsstände;
   - alle Repository-Dateien, Workflows, Regeln und technische Projektquellen.

3. **Alle vom Campus benötigten externen Rohakten**
   - komplette Roharchive/Installer/Masterdateien/Belege, auf die der Campus verweist;
   - keine Referenz darf nach Wiederaufbau auf eine verlorene Datei zeigen.

4. **Persistente GitHub-Projektdaten**
   - Repository-Metadaten;
   - Branch-/Tag-Metadaten;
   - Issues und Kommentare;
   - Pull Requests, Reviews und Review-Kommentare;
   - Releases einschließlich Release-Artefakten;
   - Labels/Milestones;
   - Rulesets/Schutzregeln;
   - Actions-/Environment-Konfiguration soweit exportierbar;
   - ursprüngliche GitHub-IDs/Zeitstempel als Archivinformation.

5. **WordPress / Projektlaufzeit**
   - vollständige WordPress-Dateien;
   - vollständige Datenbank;
   - Uploads;
   - Plugins/Themes;
   - relevante Server-/Cron-/PHP-/Webserver-Konfiguration;
   - notwendige Wiederanbindungsinformationen.

6. **Recovery**
   - benötigte Secrets/Schlüssel/Zugänge in einer verschlüsselten Recovery-Sektion;
   - niemals im Klartext im Repository oder in PROJECT_MEMORY.

7. **Restore**
   - Wiederaufbauanleitung und Restore-Werkzeuge;
   - Manifest und Hashes;
   - eindeutiger PASS-/BLOCKED-Status.

## Bedeutung von „1:1“

**Inhaltlich und funktional 1:1** ist Pflicht.

Nach einer vollständigen Löschung darf kein Campusinhalt, keine benötigte Rohakte und keine für den Wiederaufbau notwendige Information fehlen.

Technische Provider-Grenze:
GitHub kann bei neu angelegten Issues/PRs/Releases interne Objekt-IDs oder providerseitige Zeit-/Systemwerte neu vergeben.
Die ursprünglichen Werte werden deshalb im Tresor archiviert und bleiben als Information erhalten, auch wenn GitHub beim Neuaufbau neue interne IDs erzeugt.

## Download-Ort

Ziel ist ein eigener privater GitHub-Tresorbereich mit versionierten Releases.

Jeder veröffentlichte vollständige Stand:
- genau eine verschlüsselte Recovery-Datei;
- klarer Zeitstempel;
- Hash in der Release-Beschreibung;
- nur bei erfolgreicher interner Prüfung freigeben;
- ältere gültige PASS-Stände nicht überschreiben.

Der Nutzer lädt regelmäßig die neueste PASS-Datei lokal auf einen unabhängigen Datenträger.

GitHub-Release = bequemer Download-Ort.
Lokale Kopie = eigentliche unabhängige Katastrophensicherung.
