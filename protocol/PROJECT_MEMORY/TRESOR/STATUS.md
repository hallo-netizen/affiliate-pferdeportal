# NOTFALL-TRESOR – STATUS

STAND: 2026-09-07

ERGEBNIS:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_INCOMPLETE`

## Git-/Repository-Sicherung – PASS ALS PREPASS

Ein vollständiger externer Git-/GitHub-Metadaten-PREPASS wurde erzeugt und real restore-getestet.

Externer Speicher:
`/Campus-Tresor/`

Aktuellster Git-/Metadaten-PREPASS:
`/Campus-Tresor/LATEST_PREPASS.txt`

## Erster verbleibender Blocker

Das Archivregister belegt weiterhin einen **ROT**-Befund:

`ARC-PFERDE-DESIGN-20260905` → exakte finale **1.50.472 Plugin-/Master-Rohartefakte fehlen**.

Das ist strenger als fehlende Redundanz:
Ein nicht vorhandenes Original kann weder serverseitig noch lokal in eine vollständige Recovery-Kapsel aufgenommen werden.

Darum aktuell:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_INCOMPLETE`

Autoritative Belegquelle:
`protocol/PROJECT_MEMORY/ARCHIV/REGISTER.md`.

## Danach bereits bekannte nächste Prüf-/Anbindungspunkte

Nicht automatisch exportierbare Wiederherstellungsabhängigkeiten:
- Secrets/Schlüssel;
- externe Zugangsdaten;
- externe Autorisierungen.

Auch diese müssen später entweder sicher wiederherstellbar oder mit eindeutiger Recovery-Prozedur dokumentiert sein.

## Harte Regel

Der Tresor meldet immer den ersten belegten Blocker.

Git-/Metadaten-PREPASS ≠ vollständiger Katastrophen-PASS.


## Lokaler Backup-Befund 2026-09-05

Aktueller Library-Rohbestand:
- 38 Dateien;
- 985.708.251 Bytes;
- vollständig materialisiert;
- SHA-256 je Datei berechnet;
- Export-Restore 38/38 PASS.

Lokaler Export vorbereitet:
fünf Teile + Manifest + Restore-/Hashwerkzeug.

**Noch nicht als zweite unabhängige Ablage gezählt**, solange der Nutzer diese Dateien nicht tatsächlich lokal/external gespeichert und dort geprüft hat.

Der vorhandene Git-/GitHub-PREPASS V4 ist technisch restore-geprüft, bindet aber einen älteren Campus-/Paul-Stand und ist daher heute nur noch **Restore-Beweis**, nicht aktueller 1:1-Backupstand.

Real nachgewiesene nicht exportierbare Abhängigkeit:
`ENDSTEMPEL_PRIVATE_KEY`

GitHub enthält nur das Secret, nicht den auslesbaren Originalwert.
Recovery muss separat vorhanden und praktisch geprüft sein.

Bekannter Rohartefakt-Blocker bleibt außerdem:
Pferde-Design 1.50.472 – finale Plugin-/Master-ZIPs fehlen.

ERGEBNIS BLEIBT:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`


## Werkzeug-Nachtest 2026-09-07

Aktuelles Kit:
`CAMPUS_LOCAL_TRESOR_KIT_20260907.zip`

SHA-256:
`74ebe867ddcb3920fe333f3d2bb31a9d7332bc03e0cd6c7a72a99f0a1bf033c6`

Erneuter Positiv-/Negativtest:
- gültiges Test-Git + Archiv + bestätigte Recovery → `LOCAL_BACKUP_PASS` / Exit 0;
- Recovery nicht bestätigt → `LOCAL_BACKUP_BLOCKED:RECOVERY_NOT_CONFIRMED` / Exit 3;
- Archivquelle fehlt → `BLOCK: CAMPUS_ARCHIV_SOURCE_MISSING` / Exit 2.

Werkzeuglogik:
**PASS.**

Nutzer-Lokalbackup:
**OFFEN.**
Es zählt erst, wenn Kit + fünf Archivteile tatsächlich auf einem unabhängigen lokalen Speicher liegen und dort geprüft wurden.

Ergebnis bleibt:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`


## Automatisierungs-Nachtrag V2 – 2026-09-07

Kit:
`CAMPUS_LOCAL_TRESOR_KIT_20260907_V2.zip`

SHA-256:
`bb5f28d26885fd8b58fd86bea3548375c97782f58581277daddd651b2151ca54`

Automatisiert:
- Campus-Archiv prüfen und bei Bedarf aus fünf Teilen restaurieren;
- Git-Mirror + Bundle;
- realer Restore-/Refvergleich;
- GitHub-Metadaten;
- Campus-Archiv Hash-für-Hash kopieren;
- Recovery prüfen;
- versionierten Snapshot + Manifest + SHA-256 erzeugen.

Zusätzliche GitHub-Metadaten:
- Environments;
- Actions-Secret-Namen, niemals Secret-Werte;
- Actions-Variablen;
- Actions-Berechtigungen.

V2-Harttest:
- Syntax → PASS;
- positiver Starterlauf → `LOCAL_BACKUP_PASS` / Exit 0;
- ungeprüfte Recovery → korrekt `LOCAL_BACKUP_BLOCKED:RECOVERY_NOT_CONFIRMED` / Exit 3;
- fehlendes Archiv + fehlende Teile → korrekt BLOCK / Exit 2.

Die macOS-Automatik ist vorbereitet, aber erst nach realer Installation auf dem Nutzer-Mac aktiv.


## Zielverschärfung 2026-09-07 – geschlossene Ein-Datei-Recovery

Nutzerziel:
Nach theoretischem Totalverlust soll **eine einzige lokal gespeicherte Tresordatei** reichen, um den kompletten GitHub-Campus mit allen recovery-relevanten Informationen und den gebundenen Systembestand wieder aufzubauen.

Bewertung:
- KISS → PASS, weil eine Download-/Restore-Einheit;
- Nachhaltigkeit → PASS, bei versionierten automatischen Ständen + echten Restore-Tests;
- Sicherheit → PASS nur verschlüsselt und ohne Klartext-Secrets im Repository;
- Wiederherstellbarkeit → KONZEPT PASS, realer Gesamtbeweis noch OFFEN.

Aktueller Status bleibt FAIL.

Zusätzliche offene Voraussetzungen vor echtem `TRESOR_PASS`:
1. geschlossene Ein-Datei-Kapsel technisch erzeugen;
2. alle Campus-Roharchive aktuell einbinden;
3. GitHub-Kollaborations-/Release-Daten vollständig exportieren;
4. vollständigen WordPress-Datei- und Datenbankstand anbinden;
5. Recovery-Geheimnisse verschlüsselt vollständig einbinden;
6. echten isolierten Restore ausschließlich aus dieser einen Datei durchführen.

Keine dieser Voraussetzungen wird durch das bisherige V2-Mac-Kit bereits vollständig erfüllt.


## Ein-Datei-Werkzeug V3 – 2026-09-07

Kit:
`CAMPUS_LOCAL_TRESOR_ONEFILE_KIT_20260907_V3.zip`

SHA-256:
`cab73e13c12a10e807146291521601221d05a3094660c373c95afd33e4881489`

Umgesetzt:
- vorhandenen V2-Campus-Snapshot weiterverwenden;
- lokales Masterpasswort im macOS-Schlüsselbund für Automatik;
- geschlossene verschlüsselte 7z-Kapsel mit AES-256/Header-Verschlüsselung;
- Restore-/Hashprüfung innerhalb der Kapsel;
- privates GitHub-Tresor-Repository als Release-Downloadort vorbereiten;
- neueste Kapsel per `gh release create` hochladbar;
- lokales Original bleibt unabhängig erhalten.

Fail-closed:
- lokaler Snapshot nicht PASS → BUILD BLOCK;
- Masterpasswort fehlt → BUILD BLOCK;
- 7-Zip fehlt → BUILD BLOCK;
- WordPress-Vollbackup fehlt → Datei trägt ausdrücklich `WP_MISSING` und ist kein Gesamt-Tresor;
- echter isolierter Vollrestore fehlt → niemals `TRESOR_PASS`.

Technische Aktivierung auf dem Nutzer-Mac:
OFFEN.
Der private GitHub-Tresor wird erst durch den einmaligen lokalen Setup-Schritt tatsächlich angelegt.


## Testvorbereitung V4 – 2026-09-07

Kit:
`CAMPUS_LOCAL_TRESOR_ONEFILE_TESTKIT_20260907_V4.zip`

SHA-256:
`83b80a7108c13d17af9d88b03c6da942e8191432106e786bc06af247cd5bae1d`

V3-Lücken vor Test erkannt:
1. macOS-Automatik erzeugte nur V2-Snapshot, nicht die vollständige V3-Ein-Datei-Kette;
2. GitHub-Informationsarchiv enthielt noch nicht Issue-Kommentare, PR-Reviews/-Review-Kommentare, Milestones und Release-Artefakte;
3. kein einzelner isolierter Restore-Prüfer kontrollierte Kapsel + Git + Campus + Rohakten + Recovery + WordPress-Vertrag zusammen.

V4 behebt diese Testlücken.

Zusätzlich vorbereitet:
- `TEST_VORBEREITUNG_PRUEFEN.command`;
- `TEST_ALLES.command`;
- `TEST_ONEFILE_ISOLIERT.command`;
- `TEST_GITHUB_NEUAUFBAU.command`;
- `WORDPRESS_BACKUP_PRUEFEN.command`;
- `WORDPRESS_BACKUP_VERSIEGELN.command`;
- Vollautomatik = bauen → isoliert prüfen → nur danach hochladen.

Interne Positiv-/Negativbelege:
- Shell-Syntax aller V4-Kommandos → PASS;
- synthetisches Git mit mehreren Branches + Tag → Mirror/Bundle/Restore/Refvergleich/FSCK PASS;
- WordPress-Testbackup → PASS;
- manipulierte WordPress-Datenbank → korrekt BLOCK;
- Ein-Datei-Kontrollfluss mit Test-Kryptografie-Mock → Build + isolierter Restore PASS;
- fehlendes WordPress → korrekt `BLOCKED_FOR_TRESOR_PASS`;
- beschädigte Kapsel → korrekt BLOCK.

Nicht behauptet:
Die echte AES-256-7z-Verschlüsselung wurde in dieser Prüfmaschine nicht End-to-End ausgeführt, weil dort kein 7-Zip verfügbar ist.

Reale nächste Abnahme:
Nutzer-Mac + echtes 7-Zip + echtes Masterpasswort + echter GitHub-Zugang + vollständiges Recovery + vollständiger WordPress-Backupstand.

ERGEBNIS BLEIBT:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_NOT_REDUNDANT`
bis die realen externen Voraussetzungen und Restore-Abnahmen erfüllt sind.


## Nutzerweg vereinfacht – 2026-09-07

Verbindlicher Nutzerweg:

**GitHub → Releases → neueste `TRESOR_PASS`-Komplettsicherung herunterladen → lokal speichern.**

Die bisherigen V1/V2/V3/V4-Mac-Kits und `.command`-Dateien sind ab jetzt:
**INTERNE TEST-/ENTWICKLUNGSWERKZEUGE, NICHT NUTZERWEG.**

Der Nutzer soll keine Skripte starten und keine Einzeldateien zusammensetzen müssen.

Bevorzugter Download-Ort:
bestehender GitHub-Releases-Bereich des Projekts.

Bevorzugtes Asset:
`PB_ONE_KOMPLETTSICHERUNG_YYYY-MM-DD-HHMM.tar.gz.gpg`

Bevorzugter Release-Tag:
`tresor-YYYY-MM-DD-HHMM`

Noch offen vor Produktivbetrieb:
1. server-/workflowseitige regelmäßige Erzeugung aktivieren;
2. vollständigen WordPress-Backup-Zugriff anbinden;
3. Recovery-Secrets geschlossen einbinden;
4. echten isolierten Gesamt-Restore beweisen;
5. erst danach erstmals eine Datei als `TRESOR_PASS` veröffentlichen.

Aktueller Gesamtstatus bleibt:
`TRESOR_FAIL:ARCHIVE_RAW_ARTIFACTS_INCOMPLETE`


## Serverseitiger Ein-Datei-Kandidat – 2026-09-07

Interne Technik:
`control/tresor/build_tresor_release.sh`

Inaktiver Workflow-Kandidat:
`control/tresor/campus-tresor-workflow.yml.candidate`

KISS:
GitHub erzeugt später die Sicherung serverseitig.
Der Nutzer bleibt reiner Downloader.

Real intern positiv getestet:
- verschlüsselte Ein-Datei-Kapsel erzeugt;
- exakt dieselbe Datei wieder entschlüsselt;
- Payload-Hashes PASS;
- Git-Bundle PASS;
- Git-Mirror-Restore mit mehreren Branches + Tag PASS;
- Git-FSCK PASS.

Negativ getestet:
- falsches Passwort → BLOCK;
- manipulierte WordPress-Datenbank → BLOCK;
- fehlendes Campus-Roharchiv → BLOCK.

Zusätzliche Schutzregeln:
- Recovery kommt nur als opaque/versiegeltes Bundle in den Builder;
- frühere `tresor-*`-Release-Assets werden nicht rekursiv eingebettet;
- >= 2 GiB wird vor GitHub-Release geblockt.

Noch nicht produktiv:
1. WordPress-Vollbackup-Quelle anbinden;
2. Campus-Roharchiv serverseitig erreichbar machen;
3. versiegeltes Recovery-Bundle anbinden;
4. Masterpasswort als Secret binden;
5. Workflow durch bestehende Security-Grenze kontrolliert aktivieren;
6. realen Gesamt-Restore bestehen.

Bis dahin:
**kein TRESOR_PASS-Release.**


## Aktuelle NEXT ACTION – 2026-09-07

1. fehlende exakte Design-1.50.472-Rohartefakte beschaffen/archivieren;
2. danach Campus-Roharchiv serverseitig für den Tresor-Workflow erreichbar machen;
3. vollständige WordPress-Backup-Quelle anbinden;
4. versiegeltes Recovery-Bundle + Tresor-Masterpasswort anbinden;
5. Workflow kontrolliert aktivieren;
6. echten Gesamt-Restore ausschließlich aus der veröffentlichten Ein-Datei-Sicherung durchführen.

Bis Schritt 6 PASS ist:
**kein `TRESOR_PASS`-Release.**

Hinweis:
V1–V4-Mac-Kits bleiben historische/interne Testwerkzeuge und sind kein Nutzerweg.
