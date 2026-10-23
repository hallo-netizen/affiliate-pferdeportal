# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.50.724 FOOTER-MARKENLEISTE LOCAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Basis

1.50.724 baut auf dem zuletzt geprüften 1.50.723-Stand auf.
Die Magazin-Hardroute und die Breadcrumb-Korrektur bleiben enthalten.

## Kandidat 1.50.724

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.724_UPDATE_FOOTER_MARKENLEISTE.zip`

SHA-256:
`8f45a2541b537db15cd16eea509021857568ddf9bc234fd605ad48c7e6b37e44`

Größe:
767,588 Bytes.

UPDATE, kein Full-Plugin.

Hauptordner bleibt:
`affiliate-portal-template-kit/`

Enthalten:
- `pferde-template-kit.php`;
- `includes/class-hobby-depot-profile-v150709.php`;
- vorhandenes Hobby-Depot-Logoasset.

## Footer

Neu:
- schmale Markenleiste oberhalb der Navigation;
- kleines Hobby-Depot-Logo ca. 132 px;
- Claim „Hobbys. Ideen. Möglichkeiten.“.

Unverändert:
- vier Spalten Rechtliches / Wissen / Service / Anzeigenmarkt;
- kleinere Linkschrift;
- KI-Hinweis;
- zentrierter Copyrightbereich;
- PB one öffnet im neuen Fenster.

## QA

- PHP-Lint PASS;
- Fresh-Unpack PASS;
- Logo + Claim PASS;
- vier Footer-Spalten PASS;
- PB-one target/rel PASS.

Evidence:
`EVIDENCE_1.50.724.md`

## EXAKT EINE NEXT ACTION

**1.50.724-UPDATE per Cyberduck über den bestehenden Ordner `wp-content/plugins/affiliate-portal-template-kit/` zusammenführen und den Footer live prüfen.**
