# HOBBYRAUSCH – TEXT_REDAKTION – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: PSTE 0.57.14 OWNERSHIP AUF FINALER 0.57.13 PERFORMANCE-/STORAGE-BASIS HARD PASS / BUCHBINDEN E2E LOKAL PASS / LIVE-ABNAHME OFFEN

## Rolle

Einzige aktuelle Zustandsautorität des Scopes `HOBBYRAUSCH_TEXT_REDAKTION`.

## Aktueller belastbarer Stand

Hobby Depot übernimmt keine Pferde-Atelier-Fachbestände. Verwendet wird ausschließlich der allgemeingültige technische PSTE-Kern als Basis.

### Verbindliche Basis

Neuester geprüfter PSTE-0.57.13-Stand aus Datenbankbereinigung/Performance:

`PSTE-0.57.13-DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS.zip`

SHA-256:
`bb5f3cc84dc00fa85e2c0ddf48c8994a4788c2595c6d98f0d440780377060248`

### Veralteter 0.57.14-Kandidat – NICHT INSTALLIEREN

`PSTE-0.57.14-EDITORIAL-OWNERSHIP-GATE_HARD_LOCAL_PASS.zip`

SHA-256:
`3c0d39011911a7d663adc35dad8724f81dacf671c4b971d4719e221928345871`

Dieser Kandidat basierte auf einem früheren 0.57.13-COMPAT_RECHECK und würde spätere Storage-/Performance-Korrekturen zurücknehmen. Zusätzlich enthielt er eine `.orig`-Datei.

Status:
**SUPERSEDED / NICHT INSTALLIEREN.**

### Aktueller Entwicklungskandidat

`PSTE-0.57.14-EDITORIAL-OWNERSHIP-ON-FINAL-0.57.13_HARD_PASS.zip`

SHA-256:
`1ac6fa754fc6a170adccb3ab53d9023e5b8a4caaa653a79923ca9d2ae587222e`

Er wurde frisch auf der finalen 0.57.13-PERFORMANCE_SAFE-Basis aufgebaut.

## Geschützte Datenbank-/Performance-Fixes

Folgende nachträglichen 0.57.13-Dateien bleiben im aktuellen 0.57.14 byte-identisch:
- `includes/class-pste-repository.php`;
- `includes/class-pste-research-archive.php`;
- `includes/class-pste-sandbox-record-store.php`;
- `includes/class-pste-storage-maintenance.php`.

Damit bleiben insbesondere erhalten:
- Legacy-Restore für Run-/Candidate-Speicher;
- Legacy-Restore für Research-Archive;
- Legacy-Restore für Sandbox-Records;
- Restore-/Downgrade-Modus der Storage-Pflege;
- atomarer Storage-Maintenance-Lock;
- Entfernung der alten `.orig`-Datei.

## Ownership-Ergänzung

Exakt 6 Pfade unterscheiden sich von der finalen 0.57.13:
- ADD `contracts/upstream-editorial-ownership-v1.json`;
- MOD `includes/class-pste-admin.php`;
- ADD `includes/class-pste-article-ownership-gate.php`;
- MOD `includes/class-pste-compiler-read-capability.php`;
- MOD `portal-seo-topic-engine.php`;
- MOD `uninstall.php`.

Funktion:
- liest `APKW_EDITORIAL_INTENT_OWNERSHIP_HANDOFF_V1` read-only;
- bindet Artikelkandidaten an `owner_concept_id`;
- verlangt `semantic_intent_key`;
- blockiert doppelte semantische Intent-Ownership;
- Frageform besitzt keine FAQ-/Kategorie-Owner-Autorität.

Performance-/Write-Grenze:
- keine neuen WordPress-Hooks oder Filter;
- keine neuen Hintergrundjobs;
- keine DB-Lese-/Schreiboperation beim normalen Boot durch den Ownership-Gate;
- ein neuer Option-Write nur beim ausdrücklichen Admin-Import des Ownership-Handoffs;
- Option-Read nur bei ausdrücklicher Ownership-Abfrage/Validierung;
- kein Frontend-Output;
- keine Artikel-/Kategorieerzeugung.

## Zweiter Hard-Recheck gegen den neuesten 0.57.13-Stand

Erneut frisch geprüft gegen genau:
`PSTE-0.57.13-DATABASE_STORAGE_CLEANUP_PERFORMANCE_SAFE_HARD_PASS.zip`
SHA-256 `bb5f3cc84dc00fa85e2c0ddf48c8994a4788c2595c6d98f0d440780377060248`.

Dreifachvergleich alter COMPAT_RECHECK → finaler PERFORMANCE_SAFE → 0.57.14:
- nachträgliche Optimierungsänderungen: exakt 4 MOD + 1 DELETE;
- `class-pste-repository.php`: in 0.57.14 byte-identisch zum finalen 0.57.13;
- `class-pste-research-archive.php`: byte-identisch;
- `class-pste-sandbox-record-store.php`: byte-identisch;
- `class-pste-storage-maintenance.php`: byte-identisch;
- entfernte `class-pste-sandbox-record-store.php.orig`: bleibt entfernt;
- alle übrigen nicht-Ownership-Dateien ebenfalls byte-identisch.

Gesamtdiff finaler 0.57.13 → korrigierter 0.57.14:
- Basisdateien: 132;
- Kandidat: 134;
- Unterschiede: exakt 6 vorgesehene Pfade;
- unerwartete Unterschiede: 0.

Boot-Simulation:
- Frontend: gleiche Hooks, 0 zusätzliche DB-Reads/Writes/Schedules/Remote-Calls beim Plugin-Boot;
- Admin: gleiche 13 Actions + 1 Filter, gleiche 3 Reads, 0 Writes/Schedules/Remote-Calls beim Boot;
- Ownership-Datei wird zwar zusätzlich per `require_once` geladen (11.047 Byte PHP), führt beim Laden aber keine DB-/Hook-/Remote-Arbeit aus.

Wichtig zur Versionslogik:
Der bestehende Research-Driver besitzt unverändert eine Code-Version-Recovery. Nur falls bei Installation bereits ein aktiver Research-Job im Zustand BLOCKED unter 0.57.13 existiert, kann der Versionswechsel auf 0.57.14 dessen vorhandenen Recovery-Pfad auslösen. Das ist keine zurückgenommene Performance-/Storage-Optimierung, muss vor Live-Installation aber als Zustandsprüfung beachtet werden.

Archivprüfung des korrigierten Installers:
- Archivkopie byte-identisch zum lokal geprüften Paket;
- SHA-256 erneut `1ac6fa754fc6a170adccb3ab53d9023e5b8a4caaa653a79923ca9d2ae587222e`;
- keine doppelten ZIP-Einträge;
- keine `.orig/.bak/.tmp/.old/~`-Einträge;
- keine Symlink-Einträge.

## Harte lokale Prüfung aktueller Kandidat

- Ownership Positiv/Negativ: 10/10 PASS;
- Fresh-Unpack Ownership: 10/10 PASS;
- PHP-Lint Fresh-Unpack: 79/79 PASS;
- Fresh-Unpack: 134 Dateien;
- Worktree ↔ Fresh-Unpack: byte-identisch;
- verbotene `.orig/.bak/~`: 0;
- geschützte Storage-/Performance-Dateien: 4/4 byte-identisch zur finalen 0.57.13;
- unerwartete geänderte Pfade: 0.

Prüfbeleg:
`PSTE_0.57.14_FINAL_BASE_COMPAT_EVIDENCE_20260930.txt`

## Buchbinden E2E-Realtest

V1.9.1 → PSTE 0.57.14 lokal PASS:
- korrekter Owner passiert;
- falsche FAQ-Zuordnung BLOCKED;
- semantische Doppelbelegung BLOCKED;
- fehlender `semantic_intent_key` BLOCKED;
- Frageform bleibt ohne FAQ-Autorität.

Evidenz:
`BUCHBINDEN_E2E_OWNERSHIP_REALTEST_20260930.json`

## Beleggrenze

Keine Live-Installation des korrigierten 0.57.14 durchgeführt.

## Erster offener Blocker

Kein lokaler Entwicklungsblocker.

Offen ist die reale WordPress-Abnahme zusammen mit V1.9.1.

## NEXT ACTION

Nur den **korrigierten** 0.57.14-Kandidaten verwenden.

Vor Installation:
1. V1.9.1 Kategorie-Workflow bleibt ebenfalls noch ungeändert/uninstalliert;
2. PSTE 0.57.14 erst installieren, wenn der Nutzer die Prüfung akzeptiert;
3. danach reale Abnahme V1.9.1 → Editorial-Handoff → PSTE 0.57.14.

Keine weitere PSTE-Änderung, solange die reale Abnahme keinen neuen konkreten Fehler zeigt.
