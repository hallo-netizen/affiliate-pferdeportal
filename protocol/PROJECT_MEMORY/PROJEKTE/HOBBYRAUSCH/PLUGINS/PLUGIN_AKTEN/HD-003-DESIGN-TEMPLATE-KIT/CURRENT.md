# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **MAGAZIN-ZIELSEITEN HARDROUTE 1.50.722 / BREADCRUMBS LIVE BEANSTANDET / 1.50.723 LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Live-Hinweis

Nach 1.50.722 fehlten auf den Magazin-Zielseiten die Breadcrumbs.

## Kandidat 1.50.723

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.723_UPDATE_MAGAZIN_BREADCRUMBS.zip`

SHA-256:
`d0839a73d42008548f777ba0f2d56975ec0f2acef4f921590894ca8f4472d8d0`

Größe:
586,379 Bytes.

UPDATE mit exakt zwei Dateien:
- `pferde-template-kit.php`
- `includes/class-hobby-depot-profile-v150709.php`

Fix:
- Breadcrumb-Erzeugung nutzt auf den 12 Magazin-Zielseiten dieselbe URL-Hardroute wie das Template;
- Ausgabe: Startseite › Magazin › Zielseite;
- unabhängig von `is_singular()`.

QA:
- 12/12 Zielseiten im Hardroute-Failure-Mode PASS;
- Fresh-Unpack PASS;
- PHP-Lint PASS;
- ZIP exakt 2 Dateien PASS.

Evidence:
`EVIDENCE_1.50.723.md`

## EXAKT EINE NEXT ACTION

**1.50.723 per Cyberduck einspielen und eine Magazin-Zielseite live auf Breadcrumb + Hero + Intro prüfen.**
