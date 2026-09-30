# HD-001 – KATEGORIE-WORKFLOW – CURRENT

STAND: 2026-09-30
STATUS: V1.9.2 DEPLOY READBACK FIX HARD PASS / LIVE-RETEST OFFEN

## Aktuell

Plugin:
`Affiliate-Portal Kategorie-Workflow V1.9.2`

Installer:
`AFFILIATE_PORTAL_KATEGORIE_WORKFLOW_V1.9.2_DEPLOY_READBACK_FIX_HARD_PASS.zip`

Installer SHA-256:
`8d462ee585ee0921772c0deb56b9829b7e7819a618dfdfc441e06bd3afa79ff8`

Source:
`QUELLCODE_KATEGORIE_WORKFLOW_V1.9.2_DEPLOY_READBACK_FIX_HARD_PASS.zip`

Source SHA-256:
`10dd5daf5ae04cd39ef86d45128759d53b4e0af23ef6928086efbff1014a55d7`

V1.9.1 ist wegen des live reproduzierten Deployment-Readback-Fehlers superseded.

## Live gefundener Fehler

`DEPLOY_READBACK_MISMATCH | Automatischer Rollback: PASS`

Ursache:
Ein vorhandenes Exact-Slug-Zielobjekt mit gleichem Namen, aber abweichendem nativen Parent wurde in V1.9.1 als `ADOPT_EXISTING` geplant. Der Plan führte `parent` zwar als geändert, ADOPT_EXISTING schrieb den Parent jedoch nicht. Der nachgelagerte Readback erkannte die Abweichung korrekt und rollte zurück.

## Fix V1.9.2

Exact-Slug:
- native Differenz `name/slug/parent` → `UPDATE`;
- keine native Differenz → `ADOPT_EXISTING` meta-only.

## Beweise

V1.9.1 exakter Fehlerfall:
- Preflight PASS;
- action ADOPT_EXISTING;
- changed_fields [parent];
- Apply → DEPLOY_READBACK_MISMATCH;
- Auto-Rollback PASS.

V1.9.2 derselbe Fall:
- action UPDATE;
- Deploy + Readback PASS;
- Taxonomy Parent korrekt;
- Rollback stellt alten Parent wieder her PASS;
- Page Parent Korrektur PASS;
- identischer Exact-Slug ohne native Diff bleibt ADOPT_EXISTING ohne unnötigen nativen Update-Write.

Gesamt:
- Source 251/251 PASS;
- Fresh-Unpack Installer 251/251 PASS;
- PHP-Lint PASS;
- Source↔Installer Runtime-Parität 22/22 byteidentisch.

## NEXT ACTION

V1.9.2 über V1.9.1 installieren.

Der fehlgeschlagene Live-Write wurde automatisch zurückgerollt; der gespeicherte alte Dry-Run ist wegen der geänderten Aktionsplanung nicht mehr zu verwenden.

Danach denselben READ_ONLY_PREVIEW erneut als Arbeitsstand übernehmen → finale Struktur freigeben → neue WordPress-Vorschau erzeugen → neuen Plan anwenden.
