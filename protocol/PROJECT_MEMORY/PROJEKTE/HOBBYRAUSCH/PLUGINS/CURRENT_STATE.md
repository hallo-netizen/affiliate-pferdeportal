# HOBBYRAUSCH – PLUGINS – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-09-30
STATUS: HD-001 V1.9.2 HARD PASS / LIVE-RETEST OFFEN · HD-002 V0.1.1 LIVE-MIGRATION PASS

## HD-001 – Kategorie-Workflow

Aktuell:
`Affiliate-Portal Kategorie-Workflow V1.9.2`

V1.9.1 live:
`DEPLOY_READBACK_MISMATCH | Automatischer Rollback: PASS`

Root Cause reproduziert und in V1.9.2 behoben:
Exact-Slug-Objekt mit nativer Parent-Differenz wird jetzt UPDATE statt ADOPT_EXISTING.

Beweise:
- Source 251/251 PASS;
- Fresh-Unpack 251/251 PASS;
- PHP PASS;
- Runtime-Parität 22/22;
- exakter alter Fehlerfall V1.9.1 reproduziert;
- derselbe Fall V1.9.2 Deploy+Readback PASS.

Installer SHA:
`8d462ee585ee0921772c0deb56b9829b7e7819a618dfdfc441e06bd3afa79ff8`

## HD-002 – Themenengine

V0.1.1 live Migration COMPLETE.
Noch kein Gesamtbestand erfassen, bis produktiver HD-001-Kategorienstand live steht.

## NEXT ACTION

HD-001 V1.9.2 installieren → vorhandenen Buchbinden READ_ONLY_PREVIEW erneut übernehmen → Finalfreigabe → neue WordPress-Vorschau → Apply.

Danach erst HD-002 Owner-Handoff / Gesamtbestand.
