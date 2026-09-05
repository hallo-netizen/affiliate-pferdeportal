# NOTFALL-TRESOR – KONZEPT

STAND: 2026-09-05
STATUS: KONZEPT V1

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
