# HD-004 – HOBBY DEPOT KATEGORIE-KERN – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11  
STATUS: **1.0.0 LAUT WORDPRESS-LISTE AKTIV / LOCAL HARD PASS / LIVE-FUNKTIONSPRÜFUNG OFFEN**

## Zweck

Schlanker read-only Laufzeitkern für den produktiven Kategorie-Snapshot.

Er ersetzt im Normalbetrieb nur die dauernd benötigten Teile des schweren HD-001:
- Registrierung von `journal_cat`;
- neutraler read-only Zugriff auf Revision/Snapshot/Nodes/Parents/Taxonomien/WordPress-Mapping.

Er ersetzt **nicht** den HD-001-Bearbeitungsworkflow.

## Version

**1.0.0**

Artefakt:
`HOBBY_DEPOT_KATEGORIE_KERN_HD004_V1.0.0_READONLY_LOCALPASS.zip`

SHA-256:
`f3be1e10b093a24f41981c9386ce8ca208294bb0583b6bcc4a1f5295fb5c0bfb`

Library:
`/hobby rausch/KATEGORIE_ZENTRALE/HOBBY_DEPOT_KATEGORIE_KERN_HD004_V1.0.0_READONLY_LOCALPASS.zip`

## Technischer Vertrag

- liest `apkw_target_tree_active_revision_v1`;
- liest `apkw_target_tree_active_snapshot_v1`;
- keine Kategorie-/Seiten-/Term-Writes;
- keine DataForSEO-Logik;
- kein Sync/Resume/Rollback;
- keine zweite Datenhaltung;
- registriert nur `journal_cat`, falls noch nicht registriert;
- `category` bleibt WordPress;
- `hp_listing_category` bleibt HivePress.

## API

Siehe:
`../../../SEO_KATEGORIEN/KATEGORIE_ZENTRALE/RUNTIME_API.md`

## Lokaler Hardtest

PASS:
- PHP-Lint;
- ZIP-Integrität;
- gültiger Snapshot → ready;
- Revision;
- Child-Lookup;
- Mapping;
- Page-/Term-Resolve;
- Object→Node-Lookup;
- Taxonomie-Registrierung;
- statischer Read-only-Audit: keine Kategorie-/Term-/Page-Writes;
- kein Provider-/DataForSEO-Pfad.

## WordPress-Inventarabgleich 01.11.2026

Die vom Betreiber gelieferte vollständige WordPress-Pluginliste zeigt **Version 1.0.0 als aktiv**. Der zuvor dokumentierte Entwicklungs-/Teststand 1.0.0 ist versionsgleich, aber nicht dadurch funktional live-geprüft. Ein unabhängiger Server-Quellcode-/ZIP-Readback und ein Live-Funktionstest wurden in diesem Abgleich nicht ausgeführt. Keine Plugininstallation oder Campus-CURRENT.zip-Synchronisierung. Beleg: `../../EVIDENCE_WP_PLUGINLISTE_20261101.md`; operative WordPress-Current: `../../../WORDPRESS_TECHNIK/CURRENT_STATE.md`.

## EXAKT EINE NEXT ACTION

**Die schon aktive 1.0.0 read-only in der echten WordPress-Laufzeit kontrollieren (Registry und Abhängigkeiten). Keine erneute Installation und keine Deaktivierung von HD-001 nur aufgrund des älteren Testplans.**
