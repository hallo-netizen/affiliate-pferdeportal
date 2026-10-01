# HD-002 – HOBBY DEPOT SEO THEMENENGINE – CURRENT

STAND: 2026-10-01
STATUS: V0.1.2 AUTO OWNER HANDOFF POSITIV+NEGATIV HARD PASS / LIVE-INSTALLATION NÄCHSTES

## Live-Ausgangslage

Aktuell live:
`Hobby Depot SEO Themenengine 0.1.1`

Sichere Fresh-Install-Migration:
COMPLETE / Backend READY.

HD-001 steht jetzt produktiv live:
`Affiliate-Portal Kategorie-Workflow V1.9.4`
mit erfolgreichem Deployment + Readback.

## Problem in 0.1.1

HDTE 0.1.1 besitzt den technischen Owner-Handoff-Importer, aber keinen normalen sichtbaren Importweg im Backend.

`Gesamtbestand erfassen` benötigt den Owner-Handoff zwingend und würde ohne ihn fail-closed mit
`HDTE_EDITORIAL_OWNERSHIP_HANDOFF_REQUIRED`
blockieren.

## Fix 0.1.2

Plugin:
`Hobby Depot SEO Themenengine 0.1.2`

Installer:
`HOBBY_DEPOT_SEO_THEMENENGINE_V0.1.2_AUTO_OWNER_HANDOFF_HARD_PASS.zip`

Installer SHA-256:
`330028c8cd38f7f27664c804dfafa7649bea70e1f3647bc18229b52f2ba06003`

Source SHA-256:
`cf7e7766062d4c1241d2876d4d02d398ed6f81e8d1b3ebd93f0d74e0e7d32f9f`

Beim bestehenden Button
`Gesamtbestand erfassen`
passiert jetzt automatisch und read-only:

1. HD-001 muss Stage `deployed` besitzen.
2. gespeicherte FINAL_APPROVED-Struktur + Research werden aus dem installierten HD-001 gelesen;
3. dieselben installierten HD-001 Validator-/Research-Evidence-Regeln prüfen den Stand erneut;
4. nur ein `READY_FOR_DOWNSTREAM_EDITORIAL_PLANNING`-Handoff wird übernommen;
5. HDTE speichert ausschließlich seinen eigenen Handoff-Snapshot;
6. danach wird der normale Website-Baseline-/Portalabgleich gestartet.

HD-001 wird dabei nicht verändert.

## Exakter Buchbinden Positivtest

Echter Produktionskandidat / echtes Research:
- Owner-Handoff READY;
- 7 Owner;
- 11 ARTICLE_ONLY;
- 11/11 gebunden;
- automatischer Handoff-Sync PASS;
- HDTE Baseline CURRENT;
- 4 produktive Content-Leaf-Kategorien;
- 1 Buchbinden-Themenfamilie;
- HD-001 Workspace vor/nach Sync unverändert.

Worktree und frisch entpackter Installer: PASS.

## Negativtests

Fail-closed:
- HD-001 nicht deployed → `HDTE_UPSTREAM_CATEGORY_WORKFLOW_NOT_DEPLOYED`;
- Finalpaket fehlt → `HDTE_UPSTREAM_FINAL_PACKAGE_MISSING`;
- nicht FINAL_APPROVED → `HDTE_UPSTREAM_FINAL_PACKAGE_NOT_APPROVED`;
- notwendige Live-Kategorie fehlt → `HDTE_UPSTREAM_OWNER_CATEGORY_SET_INCOMPLETE`;
- gespeicherter Handoff manipuliert → `HDTE_EDITORIAL_OWNERSHIP_SNAPSHOT_HASH_MISMATCH`.

## Paketprüfung

- geändert gegenüber 0.1.1: exakt 3 Dateien;
- Safe-Migration-/Storage-/Performance-Code sonst byte-identisch;
- PHP Source 80/80 PASS;
- PHP Fresh Installer 80/80 PASS;
- Source ↔ Fresh Installer 135/135 Dateien identisch;
- keine zusätzliche Pluginlinie / kein Companion-Plugin.

## NEXT ACTION

V0.1.2 über V0.1.1 installieren.

Danach:
`Hobby Depot Themenengine → Übersicht → Gesamtbestand erfassen`

Kein manueller Owner-Handoff-Download.
Kein manueller Owner-Handoff-Import.

Bei Erfolg:
`Gesamtbestand erfasst.`
Danach Portalabgleich bis COMPLETE.
