# HD-001 – KATEGORIE-WORKFLOW – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-11
STATUS: **1.14.8 / RULE 2.7 / FINAL VERIFIED E2E / LIVE-PASS / SCHWERER WORKFLOW KANN NACH HD-004-LIVEPASS DEAKTIVIERT WERDEN**

## Plugin

ID:
`HD-001-KATEGORIE-WORKFLOW`

Name:
`Affiliate-Portal Kategorie-Workflow`

Rolle:
Bearbeitungs-/Research-/Dry-Run-/Sync-/Resume-/Rollback-Werkzeug für Kategorieänderungen.

## Aktuelle technische Wahrheit

Codebasis:
`1.14.8`

Finales Release:
`HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

SHA-256:
`709134631895a901bcb4fc5f5d71889d317954d9928c0ed20700883990a5a52c`

Produktive Live-Profilrevision:
`HD-TARGET-3P-RULE27-CATEGORY-GAPFIX-HOBBYFINDER-20261009+0f4dbf59238a7d83`

Final:
- 2357 Zielobjekte;
- 2357 Readback;
- Frontend valid;
- 8 Welten;
- 330/330 Kategorie-Gate;
- LIVE-PASS.

## Hard-Audit Deaktivierung/Löschen

Exakter 1.14.8-Quellstand:
- kein `uninstall.php`;
- kein `register_uninstall_hook`;
- kein `register_deactivation_hook`;
- Kategorien/Seiten/Terms/Metadaten/Target-Snapshot werden beim Deaktivieren nicht gelöscht;
- WordPress-Löschen der Plugin-Dateien löst nach diesem Quellstand keinen plugin-eigenen Daten-Cleanup aus.

Dauerhaft notwendige Runtimefunktion aus HD-001:
- `journal_cat` registrieren;
- aktiven Target-Snapshot für andere Komponenten lesbar halten.

Diese Funktion wird schlank nach HD-004 ausgelagert.

## Neuer Betriebsmodus

Normal:
- HD-004 aktiv;
- HD-001 nach Live-Smoke-Test deaktiviert.

Änderung:
- HD-001 wieder aktivieren;
- Delta/Dry-Run/Sync/Readback;
- anschließend wieder deaktivieren.

DataForSEO:
nur SEO-Evidence innerhalb dieses Bearbeitungsworkflows; keine Strukturautorität und kein Dauerbetriebsgrund.

## Wiederherstellung

Exaktes ZIP zusätzlich zentral abgelegt:
`/hobby rausch/KATEGORIE_ZENTRALE/HD001_V1.14.8_RULE27_FINAL_VERIFIED_E2E_20261009.zip`

## EXAKT EINE NEXT ACTION

**HD-004 live installieren; danach HD-001 zunächst deaktivieren und Smoke-Test. Noch nicht vor diesem PASS löschen.**
