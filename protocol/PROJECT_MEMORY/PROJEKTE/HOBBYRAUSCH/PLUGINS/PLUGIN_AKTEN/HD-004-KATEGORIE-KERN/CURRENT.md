# HD-004 – HOBBY DEPOT KATEGORIE-KERN – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11  
STATUS: **1.0.0 LOCAL HARD PASS / LIVE-INSTALLATION AUSSTEHEND**

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

## EXAKT EINE NEXT ACTION

**HD-004 1.0.0 installieren und aktivieren; danach HD-001 zunächst nur deaktivieren und Live-Smoke-Test durchführen.**
