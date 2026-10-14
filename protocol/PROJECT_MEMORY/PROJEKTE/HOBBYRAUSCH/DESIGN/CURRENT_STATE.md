# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-14
STATUS: **1.50.653–1.50.656 VERWORFEN / 1.50.650 IMAGE-ONLY-RESTORE LIVE FAIL / REPAIR-INSTALLER 1.50.657 LOKAL E2E PASS / KEIN LIVE-PASS**

## Exakter aktueller Befund
- 1.50.650 bleibt der letzte Stand, bei dem **Textinhalt + Grundaufteilung live bestätigt** wurden.
- 1.50.651 ist ausdrücklich LIVE FAIL / verworfen.
- 1.50.653–1.50.656 sind verworfen.
- Auch der anschließend gebaute `AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.650_RUNTIME_RESTORE_NEW_IMAGES.zip` ist **LIVE FAIL**: trotz 55/55 PHP-Dateien byte-identisch zu original 1.50.650 zeigte der reale Frontend-Aufruf weiter den WordPress-kritischen Fehler.

Damit ist belastbar:
**Der Live-Fatal ist nicht durch einen PHP-Code-Unterschied dieses letzten Restore-ZIPs gegenüber 1.50.650 erklärbar.**
Ohne Server-Fatal-Log wird keine einzelne PHP-Zeile als Ursache erfunden.

## Reparaturweg 1.50.657
Normales „Plugin hochladen → vorhandenen Ordner überschreiben“ wird vorerst nicht mehr verwendet.

Paket:
`HOBBY_DEPOT_REPAIR_INSTALLER_1.50.657.zip`

SHA-256:
`8cc88b8bf6a013aaf09fc8f20f039d68fcaa1e0ef9138c2b043278027c20201e`

### Was der Repair Installer tut
1. eingebauten Payload vollständig per SHA-256 prüfen;
2. bestehendes `affiliate-portal-template-kit` deaktivieren;
3. den gesamten alten Pluginordner rekursiv entfernen;
4. den bekannten 1.50.650-Runtime-Stand sauber neu kopieren;
5. alle 981 Payload-Dateien nach dem Kopieren erneut per SHA-256 prüfen;
6. Statcache, PHP-OPcache sowie verfügbare WordPress/Page-Caches leeren;
7. **erst im nächsten Admin-Request** das wiederhergestellte Template Kit aktivieren;
8. danach den Repair Installer selbst deaktivieren.

Dadurch werden zwei bisher bei normalen Updates nicht sauber ausgeschlossene Zustände ausdrücklich beseitigt:
- alte/stale Dateien im Pluginordner;
- alter PHP-/Object-/Page-Cache-Zustand über eine Request-Grenze.

### Payload
- Runtime-Code = originaler 1.50.650-Stand;
- **55/55 PHP-Dateien unverändert**;
- **0 Nicht-Bild-Dateien gegenüber original 1.50.650 geändert**;
- exakt **130 WebP-Dateien geändert**:
  - 65 Heroes, 600×220;
  - 65 Kategorievorschauen, 200×107.

## Lokale E2E-Simulation 1.50.657
Getestet wurden vier reale verschmutzte Ausgangsbäume:
- 1.50.653
- 1.50.654
- 1.50.655
- 1.50.656

Je Ausgangsstand drei getrennte Request-Grenzen:
1. Repair-Aktivierung;
2. Zielplugin-Aktivierung / Repair-Selbstdeaktivierung;
3. Frontend-Request `/gestalten/druck-foto/`.

Für **alle vier**:
- alter Stale-Testfile nach Repair entfernt;
- Zielordner danach byte-/prüfsummengleich zum Payload;
- Aktivierungs-Request stderr 0;
- Finish-Request stderr 0;
- Frontend-Request stderr 0;
- positive Route: `hobby-depot-content-v150650.php`;
- vollständiger Frontend-Render: 12.377 Byte;
- Hero vorhanden;
- kein kritischer Fehler;
- negativer Routingtest auf nicht eigener Seite: Theme-Template bleibt erhalten.

Negativtests:
- absichtlich beschädigter eingebauter Payload → Repair stoppt **vor** Deaktivierung/Löschen des alten Plugins;
- Zielordner nach Kopie absichtlich manipuliert → Zielplugin wird **nicht** aktiviert, Repair bleibt aktiv, Fehler wird festgehalten.

Statische Tests:
- Payload PHP: **55/55 Syntax PASS**;
- Repair-Installer PHP: Syntax PASS;
- Hero-Dimensionen: **65/65 PASS**;
- Vorschau-Dimensionen: **65/65 PASS**;
- Hero-Dubletten exakt: 0;
- Vorschau-Dubletten exakt: 0;
- ZIP-Integrität: PASS.

Evidence:
`HOBBY_DEPOT_REPAIR_1.50.657_LOCAL_TEST_EVIDENCE.json`

## EXAKT EINE NEXT ACTION
**Kein normales Template-Kit-ZIP mehr installieren. Ausschließlich den Repair Installer 1.50.657 einmal hochladen und aktivieren. Er ersetzt/deaktiviert/reaktiviert den Template-Kit automatisch über eine saubere Request-Grenze. Danach nur /gestalten/druck-foto/ live prüfen. Erst dann existiert ein Live-PASS oder ein belastbarer neuer Live-Fehler.**
