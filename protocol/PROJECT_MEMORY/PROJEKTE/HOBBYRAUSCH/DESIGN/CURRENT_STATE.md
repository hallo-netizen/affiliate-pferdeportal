# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.653–1.50.657 LIVE/INSTALL FAIL ODER VERWORFEN / SICHTBARER FEHLERSTAND SEIT 16:49 UNVERÄNDERT / RECOVERY 1.50.658 LOKAL POSITIV+NEGATIV E2E PASS / KEIN LIVE-PASS**

## Belastbarer Iststand
- Vor der Reparaturserie renderte `/gestalten/druck-foto/` sichtbar das eigene Hobby-Depot-Layout.
- Seit 16:49 zeigen die Nutzer-Screenshots denselben kritischen Fehler.
- Der zentrale Seitenbereich der Screenshots 17:21, 18:05 und 18:34 ist pixelidentisch. Die späteren Reparaturversuche haben den sichtbar gerenderten Frontendzustand damit nicht verändert.
- Die exakte Live-PHP-Fatalzeile ist ohne Serverlog nicht bekannt und wird nicht geraten.
- Das dokumentierte 1.50.652-ZIP ist in den aktuell verfügbaren Projekt-/Library-/Conversation-Dateien nicht vorhanden.
- 1.50.650 ist als Originalpaket vorhanden; 55/55 PHP-Dateien und kompletter Baum sind lokal prüfbar.

## Verworfen / nicht erneut verwenden
- 1.50.653
- 1.50.654
- 1.50.655
- 1.50.656
- `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_RUNTIME_RESTORE_NEW_IMAGES.zip`
- `HOBBY_DEPOT_REPAIR_INSTALLER_1.50.657.zip`

## Recovery 1.50.658
Paket:
`HOBBY_DEPOT_RECOVERY_1.50.658.zip`

SHA-256:
`b5cda174d9162841ad983e7f69ace02111c25f81ae338ff0cdf237694e6296e1`

### Prinzip
Kein blindes Überschreiben mehr.

1. Vor jeder Änderung echter WordPress-Loopback auf `/gestalten/druck-foto/`.
2. Aktuellen kanonischen Template-Kit-Ordner vollständig für Rollback sichern.
3. Vorhandene WordPress-Upgrade-Backups durchsuchen.
4. Falls ein echter 1.50.652-Backupstand vorhanden ist, diesen zuerst als Kandidaten verwenden.
5. Sonst exakt den eingebetteten originalen 1.50.650-Stand verwenden.
6. Alle erkannten Template-Kit-Kopien vor Kandidatenaktivierung deaktivieren.
7. Kandidat in getrenntem Request aktivieren.
8. Danach erneut echten WordPress-Loopback ausführen.
9. Kandidat bleibt nur aktiv bei HTTP 2xx/3xx + Hobby-Depot-Owned-Marker + keinem Critical-Error-Text + keinem erfassten Fatal.
10. Fehlschlag → nächster Kandidat.
11. Alle Kandidaten fehlgeschlagen → exakten vorherigen Plugin-Snapshot wiederherstellen und zuvor aktive Plugins reaktivieren.
12. Erfolg → Recovery-Plugin deaktiviert sich selbst.

### Embedded Fallback
- exakt original 1.50.650;
- **981/981 Dateien SHA-identisch**;
- **55/55 PHP-Dateien Syntax PASS**;
- kompletter `Druck & Fotografie`-Hub2-Render lokal PASS;
- keine neuen Bilder, kein CSS-Fix, keine Mappingänderung im Recovery-Fallback.

## Lokale Prüfung 1.50.658
**11/11 E2E-Szenarien PASS**, jeweils über getrennte Request-Grenzen:
- reale kaputte Ausgangsbäume 1.50.653 → Recovery PASS;
- 1.50.654 → PASS;
- 1.50.655 → PASS;
- 1.50.656 → PASS;
- vorhandenes 1.50.652-Backup wird bevorzugt und bei Frontend-PASS behalten;
- 1.50.652-Frontend-Fail → automatischer Fallback auf 1.50.650;
- 1.50.652-Aktivierungsfehler → automatischer Fallback auf 1.50.650;
- alle Kandidaten fail → vorheriger Pluginbaum exakt zurückgerollt und reaktiviert;
- beschädigter eingebetteter 1.50.650-Payload → Prüfsummenfehler, exaktes Rollback;
- aktive doppelte Template-Kit-Kopie → deaktiviert, nur kanonisches Kit bleibt bei Erfolg aktiv;
- bereits gesundes Frontend → keinerlei Ersetzung.

Zusätzlich:
- Recovery-PHP Syntax PASS;
- ZIP-Integrität PASS;
- ZIP-Extraktion bytegleich zum geprüften Quellbaum;
- Evidence: `HOBBY_DEPOT_RECOVERY_1.50.658_LOCAL_TEST_EVIDENCE.json`.

## EXAKT EINE NEXT ACTION
**Keine weiteren normalen Template-Kit-ZIPs installieren. Recovery 1.50.658 einmal als separates Plugin installieren und aktivieren. Es prüft den echten Serverzustand selbst, übernimmt nur einen Kandidaten mit echtem Frontend-PASS und rollt sonst automatisch auf den vorherigen Zustand zurück.**
