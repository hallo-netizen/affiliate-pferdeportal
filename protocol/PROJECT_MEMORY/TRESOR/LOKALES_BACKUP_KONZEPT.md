# LOKALES CAMPUS-BACKUP – 1:1-WIEDERAUFBAU

STAND: 2026-09-05
STATUS: KONZEPT + GETESTETE WERKZEUGE V1

## Ziel

Ein lokaler, versionierter Sicherungsstand soll einen funktionalen 1:1-Wiederaufbau des gesicherten Campus-/Repositoryzustands ermöglichen.

Der lokale Tresor ist **keine Arbeitsquelle**.
Er ist ausschließlich:
**BACKUP / VERIFY / RESTORE**.

## Drei unabhängige Ebenen

1. **GitHub**
   - aktive Git-/Arbeitsquelle;
   - main, Branches, Tags, Issues, PRs, Releases, Rulesets usw.

2. **ChatGPT Campus-Archiv**
   - persistentes Roharchiv der Master-/Plugin-/Belegdateien;
   - aktuell 38 Dateien / 985.708.251 Bytes.

3. **Lokaler Tresor**
   - zweite unabhängige Rohkopie auf dem Nutzergerät bzw. bevorzugt verschlüsselter externer SSD;
   - versionierte Snapshots;
   - frühere PASS-Stände niemals überschreiben.

## Inhalt jedes lokalen Snapshots

### A. Git
- kompletter `git clone --mirror`;
- Git-Bundle aller Refs;
- echter Restore aus Bundle;
- Ref-für-Ref-Vergleich Quelle gegen Restore.

### B. GitHub-Metadaten
Mindestens:
- Repository;
- Branches;
- Tags;
- Issues;
- Pull Requests;
- Releases;
- Rulesets;
- Workflows;
- Labels.

Wenn ein notwendiger Export – insbesondere Rulesets – nicht möglich ist:
**LOCAL_BACKUP_BLOCKED**.

### C. Campus-Archiv
- komplette lokale Kopie des aktuellen `/Campus-Archiv`;
- Dateianzahl;
- Bytezahl;
- SHA-256 jeder Datei;
- Quell-/Zielvergleich nach Kopie.

### D. Recovery
Nicht exportierbare Abhängigkeiten werden **niemals** in GitHub/PROJECT_MEMORY geschrieben.

Es gibt lokal ein separates Recovery-Verzeichnis mit:
- vollständigem Recovery-Inventar;
- sicherem Wiederherstellungsort oder Verfahren;
- praktisch geprüftem Recovery-Status.

Aktuell hart belegt:
- GitHub Actions Secret `ENDSTEMPEL_PRIVATE_KEY`.

Der Secret-Wert kann aus GitHub nicht zurückgelesen werden.
Ohne unabhängige Recovery-Quelle:
**kein TRESOR_PASS**.

### E. Manifest
Jeder Snapshot enthält:
- Zeit;
- Hashes;
- Git-Restore-Ergebnis;
- Archivkopie-Ergebnis;
- Recovery-Status;
- Gesamtstatus.

## Statusbegriffe

### LOCAL_BACKUP_PASS
Der lokale Snapshot selbst wurde technisch vollständig erzeugt und geprüft.

### TRESOR_PASS
Strenger.

Zusätzlich zu LOCAL_BACKUP_PASS müssen:
- alle für die Rekonstruktion notwendigen Originalartefakte überhaupt vorhanden sein;
- alle bekannten Recovery-Abhängigkeiten vollständig und praktisch wiederherstellbar sein;
- der Campus-Prüfvertrag PASS liefern.

**LOCAL_BACKUP_PASS ist deshalb nicht automatisch TRESOR_PASS.**

## Aktuell erzeugter Roharchiv-Export

Quelle:
ChatGPT Library `/Campus-Archiv`

Bestand:
- 38 Dateien;
- 985.708.251 Bytes;
- SHA-256-Manifest erzeugt;
- vollständiger Restore des Exports 38/38 geprüft.

Für praktikablen lokalen Download wurde der Export in fünf unveränderte Teile gesplittet.

Wichtig:
Erst nachdem diese Teile auf einem unabhängigen lokalen Speicher liegen und dort erneut Hash-PASS liefern, zählt der lokale Speicher als zweite Archivablage.

## Lokales Ein-Klick-Werkzeug

`CAMPUS_LOCAL_TRESOR.command`

Ablauf:
1. Git-Mirror;
2. Bundle;
3. echter Restore-/Refvergleich;
4. GitHub-Metadaten;
5. Campus-Archiv bytegenau kopieren;
6. Recovery prüfen;
7. versionierten Snapshot + Manifest erzeugen.

Positiv-/Negativtest V1:
- korrekter Git-/Archiv-/Recovery-Stand → `LOCAL_BACKUP_PASS`;
- fehlendes Campus-Archiv → BLOCK;
- Recovery nicht vollständig bestätigt → `LOCAL_BACKUP_BLOCKED:RECOVERY_NOT_CONFIRMED`;
- manipuliertes Roharchivteil → Hashprüfung FAIL.

## Lokale Speicherempfehlung

KISS:
- verschlüsselte externe SSD, APFS verschlüsselt;
- Ordner `Campus-Tresor/SNAPSHOTS/`;
- jeder Lauf neuer Zeitstempel;
- niemals alten PASS überschreiben.

Für höhere lokale Ausfallsicherheit:
zweite externe Platte oder Time Machine zusätzlich.

## Aktuell bekannte verbleibende TRESOR-PASS-Blocker

1. Die heutige Library-Rohablage besitzt noch keine **bestätigte** zweite unabhängige lokale Kopie.
2. Pferde-Design: exakte finale 1.50.472-Plugin-/Master-Rohartefakte fehlen weiterhin.
3. Recovery von `ENDSTEMPEL_PRIVATE_KEY` ist noch nicht praktisch als unabhängig wiederherstellbar bestätigt.
4. Weitere externe Recovery-Abhängigkeiten müssen vollständig inventarisiert oder ausdrücklich als nicht notwendig ausgeschlossen werden.

## Alte PREPASS-Stände

Der vorhandene V4-Git-/GitHub-PREPASS beweist, dass:
- Mirror-Erzeugung funktioniert;
- Git-Bundle funktioniert;
- echter Git-Restore funktioniert;
- Metadatenexport funktioniert.

Er ist **kein aktueller Backupstand mehr**, sobald Campus/Branches danach weiterentwickelt wurden.

Regel:
**Restore-Beweis darf alt sein. Ein 1:1-Backupstand muss frisch sein.**
