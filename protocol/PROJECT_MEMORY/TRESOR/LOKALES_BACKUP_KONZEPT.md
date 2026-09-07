# LOKALES CAMPUS-BACKUP – 1:1-WIEDERAUFBAU

STAND: 2026-09-07
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


## Downloadpaket 2026-09-07

Mac-Kit:
`CAMPUS_LOCAL_TRESOR_KIT_20260907.zip`

SHA-256:
`74ebe867ddcb3920fe333f3d2bb31a9d7332bc03e0cd6c7a72a99f0a1bf033c6`

Dauerhafte Library-Ablage:
`/Campus-Archiv/TRESOR_TOOLS/2026-09-07/`

Zusätzlich lokal zu speichern:
- `CAMPUS_ARCHIV_20260905.part-00`
- `CAMPUS_ARCHIV_20260905.part-01`
- `CAMPUS_ARCHIV_20260905.part-02`
- `CAMPUS_ARCHIV_20260905.part-03`
- `CAMPUS_ARCHIV_20260905.part-04`

Die fünf Teile enthalten den bereits 38/38 restore-geprüften Roharchivexport.

Ablauf auf dem Mac:
1. Kit entpacken.
2. fünf Teile in denselben Ordner legen.
3. `RESTORE_CAMPUS_ARCHIV.command` ausführen.
4. Ergebnis `CAMPUS_ARCHIV_RESTORE_PASS` verlangen.
5. Recovery-Verzeichnis separat/sicher einrichten.
6. `CAMPUS_LOCAL_TRESOR.command` ausführen.
7. Nur `LOCAL_BACKUP_PASS` akzeptieren.

Erst der reale Lauf auf dem unabhängigen Nutzer-Datenträger schließt die Redundanzlücke.


## Automatisierung V2

Bevorzugter Einstieg:
`START_CAMPUS_TRESOR.command`

Ein Start erledigt automatisch:
1. lokales Campus-Archiv verifizieren;
2. falls nötig aus den fünf Exportteilen wiederherstellen;
3. Recovery-Vorlage bei Bedarf anlegen;
4. GitHub/Git vollständig sichern;
5. Metadaten exportieren;
6. Archiv bytegenau kopieren;
7. Recovery prüfen;
8. Snapshot mit Manifest und Hashes erzeugen.

`AUTOMATIK_EINRICHTEN.command` richtet optional einen macOS-LaunchAgent ein.
Der Nutzer wählt selbst täglich oder wöchentlich und die gewünschte Stunde.

Grenze:
GitHub wird bei jedem Lauf frisch gesichert.
ChatGPT-Library-Roharchive können vom lokalen Mac nicht still automatisch synchronisiert werden; ein neuer Roharchivstand benötigt einen neuen Export.


## Ein-Datei-Automatik V3

V3 baut auf V2 auf; keine zweite Backup-Engine.

Ablauf:
1. V2 erzeugt/verifiziert den aktuellen Git-/GitHub-/Campus-/Recovery-Snapshot.
2. V3 prüft den Snapshot fail-closed.
3. WordPress-Vollstand wird als zusätzlicher Pflichtbaustein geprüft.
4. Restore-Werkzeuge + Ein-Datei-Manifest werden eingebettet.
5. genau eine verschlüsselte 7z-Kapsel wird erzeugt und sofort mit dem Masterpasswort getestet.
6. SHA-256 wird berechnet.
7. optional wird genau diese verschlüsselte Datei als versioniertes Release in den privaten GitHub-Tresor hochgeladen.
8. lokale Datei bleibt erhalten.

Sicherheitsentscheidung:
Das Masterpasswort wird für automatische lokale Läufe im macOS-Schlüsselbund gehalten.
Es wird weder in PROJECT_MEMORY noch in GitHub im Klartext gespeichert.

Katastrophenregel:
Nach Totalverlust benötigt der Nutzer neben der Recovery-Datei nur das Masterpasswort und frei neu installierbare Standardwerkzeuge.

Aktuelle Grenze:
Die vollständige WordPress-Quelle ist noch nicht technisch angebunden.
Daher kann V3 aktuell den Campus kapseln, aber noch keinen echten Gesamt-`TRESOR_PASS` erzeugen.


## Testautomatik V4

V4 ersetzt die Automatik nicht durch eine neue Backup-Engine.

Die bestehende Kette wird lediglich geschlossen:

`V2 Snapshot`
→ `V3/V4 Ein-Datei-Kapsel`
→ `isolierter Restore-Test`
→ **nur bei PASS**
→ `GitHub-Tresor-Release`.

Damit gilt:
Ein automatischer Upload darf nicht erfolgen, wenn der isolierte Restore-Test fehlschlägt.

Zusätzlicher GitHub-Informationsumfang:
- Issue-Kommentare;
- PR-Review-Kommentare;
- PR-Reviews;
- Milestones;
- Release-Artefakte;
- Deployments soweit verfügbar.

WordPress-Vertrag:
Ein beliebiger Ordner mit Flag reicht nicht mehr.
`WORDPRESS_BACKUP_PRUEFEN.command` verlangt Datenbank, vollständiges Dateiarchiv, Manifest und passende Hashes.

Testkit:
`CAMPUS_LOCAL_TRESOR_ONEFILE_TESTKIT_20260907_V4.zip`
SHA-256:
`83b80a7108c13d17af9d88b03c6da942e8191432106e786bc06af247cd5bae1d`.


## Nutzerweg – ab ARCH-081

Dieses Dokument beschreibt nur die interne Technik.

**Nicht mehr Nutzerweg:**
- V1/V2/V3/V4-Kits bedienen;
- `.command`-Dateien starten;
- fünf Archivteile zusammensetzen;
- manuell Hashes prüfen.

**Einziger Nutzerweg:**
GitHub Releases → neueste `TRESOR_PASS`-Datei herunterladen → lokal speichern.

Die bestehende lokale Technik bleibt nur als Entwicklungs-/Restore-Baustein erhalten, bis die automatische serverseitige Kette vollständig aktiviert und real abgenommen ist.
