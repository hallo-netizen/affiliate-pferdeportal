# NOTFALL-TRESOR – WIEDERAUFBAU OHNE VORWISSEN

STAND: 2026-09-07

Diese Datei ist der Einstieg, wenn der aktive Campus ganz oder teilweise verloren oder unzuverlässig ist.

## 0. Ein-Datei-Regel

Bevorzugter Katastrophenfall:
Es existiert nur noch die zuletzt lokal gespeicherte verschlüsselte Tresordatei.

Zulässige Ausgangsmittel:
- genau diese eine Recovery-Datei;
- das bekannte Masterpasswort;
- ein leerer Rechner/Server bzw. neue leere Providerkonten;
- frei neu installierbare Standardwerkzeuge.

Nicht zulässig:
- weitere Projekt-ZIPs;
- alte Masterdateien;
- ChatGPT-Library als Pflichtquelle;
- ein zweites Backup;
- ein noch funktionierendes WordPress als Quelle;
- ein noch funktionierendes GitHub-Repository als Quelle.

Der Wiederaufbau gilt nur dann als vollständig, wenn aus dieser Ausgangslage der Campus und die gebundenen Systeme rekonstruiert werden können.

## 1. Tresorstand wählen

Nur einen Stand mit `TRESOR_PASS` verwenden.

Wenn mehrere vorhanden sind:
- jüngsten belastbaren PASS wählen;
- bei Verdacht auf bereits enthaltenen Fehler einen älteren SAFE/PASS-Stand wählen.

## 2. Manifest prüfen

Vor Wiederaufbau:
- Manifest vorhanden;
- Hashprüfung PASS;
- main/Branches/Tags vollständig;
- keine ungeklärte Wiederherstellungsabhängigkeit.

## 3. Git wiederherstellen

Aus dem Git-Mirror:
- Repository;
- Historie;
- main;
- Branches;
- Tags.

**Nicht im Mirror arbeiten und dort nichts ausführen.**

Der Mirror ist nur Quelle. Wiederherstellung erfolgt in ein reguläres Repository / einen frischen Arbeits-Worktree **außerhalb** von `Campus-Tresor` und `Campus-Archiv`.

Keine einzelnen Dateien manuell zusammensuchen, wenn der vollständige Mirror vorhanden ist.

## 4. GitHub-Struktur wiederherstellen

Anhand des Metadaten-Snapshots:
- Repository-Zustand;
- Rulesets/Schutzregeln;
- relevante Releases;
- Issues/PRs soweit vorgesehen und technisch wiederherstellbar;
- aktive Arbeitsbranch-Zuordnungen.

## 4a. Original-GitHub-Informationen

Providerseitig neu vergebene IDs sind zulässig, wenn GitHub sie technisch nicht identisch wiederherstellen lässt.

Pflicht:
Die ursprünglichen IDs, Nummern, Inhalte, Beziehungen und Zeitstempel bleiben im Metadatenarchiv der Recovery-Datei erhalten.

Dadurch geht keine ursprüngliche Information verloren, auch wenn GitHub beim Neuaufbau neue interne Objekte erzeugt.

## 5. Nicht exportierbare Abhängigkeiten

Alle im Manifest aufgeführten Schlüssel/Autorisierungen/externen Abhängigkeiten nach der dokumentierten Recovery-Prozedur wiederherstellen.

Fehlt ein notwendiger Wert:
STOPP. Nicht improvisieren.

## 6. Arbeitsquelle neu legitimieren

Vor Fach-/Runnerarbeit:
- wiederhergestelltes offizielles GitHub-Repository vorhanden;
- frischer Arbeits-Worktree außerhalb Tresor/Archiv;
- `origin` zeigt auf das offizielle GitHub-Repository;
- normale technische Eingangstür PASS.

Ein Worktree, der noch am Tresor-/Archiv-Gitdir hängt, ist **nicht** arbeitsfähig.

## 7. Hauptpförtner

Danach:
`protocol/PROJECT_MEMORY/HAUPTPFOERTNER.md`

lesen und den normalen Campus-Reset durchführen.

## 8. Baucontainer

Bauplan und Änderungen prüfen:
- welche Projektgebäude existieren;
- welche Büros existieren;
- welche Architekturentscheidungen gelten.

## 9. Fachstände

Je aktivem Büro:
- START_HERE;
- CURRENT_STATE;
- HOBBYRAUM;
- relevante Fehler;
- relevante Änderungen;
- verbindlichen Arbeitsweg.

## 10. Maschinenraum prüfen

Bestehende technische Gates/Tests ausführen.
Keine neue Architektur als Ersatz bauen.

## 11. Wiederaufbau-Abnahme

Erst wenn:
- Struktur vollständig;
- Git/Metadaten vollständig;
- Schutzregeln hergestellt;
- Projektgedächtnis vollständig;
- technische Pflichtprüfungen PASS;

gilt der Campus als wiederhergestellt.

Endstatus:
`CAMPUS_RESTORE_PASS`

Andernfalls:
`CAMPUS_RESTORE_BLOCKED:<ERSTER_FEHLER>`
