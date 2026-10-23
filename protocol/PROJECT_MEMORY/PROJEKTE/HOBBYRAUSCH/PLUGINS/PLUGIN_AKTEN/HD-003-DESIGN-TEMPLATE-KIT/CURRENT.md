# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **LIVE 1.50.711 / 1.50.715 DELTA LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Live

Aktiv und zuletzt belastbar:
**1.50.711**.

## Lokaler Kandidat 1.50.715 – Delta

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.715_DELTA_FAQ_PBONE.zip`

SHA-256:
`2c6594ee4fae4d37cc9fa43a6e5183e190bcb86ae13db29c924346d73a2ae33a`

Größe:
574,666 Bytes.

Enthält exakt:
- `pferde-template-kit.php`;
- `includes/class-hobby-depot-profile-v150709.php`.

Änderungen:
- PB one öffnet in neuem Fenster mit sicherem `rel`;
- vorhandene leere Seite `/faq/` erhält die vollständige FAQ-Darstellung;
- 6 Themenbereiche / 30 Fragen;
- native aufklappbare `details`-Elemente, kein JavaScript;
- responsive FAQ-Gestaltung;
- kurze Antworten in direkter Du-Ansprache;
- FAQ-Meta-Description-Fallback.

Footer aus 1.50.713 bleibt:
- vier Spalten Rechtliches / Wissen / Service / Anzeigenmarkt;
- Logo entfernt;
- kleinere Linkschrift;
- Copyright mittig unter dem Footer;
- KI-Hinweis + PB one.

Lokale QA:
- exakt 2 Dateien im ZIP;
- PHP-Lint PASS;
- Fresh-Unpack PASS;
- FAQ-Render 6/6 Bereiche und 30/30 Fragen PASS;
- PB-one-Neues-Fenster PASS.

Evidence:
`EVIDENCE_1.50.715.md`

1.50.715 ist **nicht live**.

## EXAKT EINE NEXT ACTION

**1.50.715-Delta lokal entpacken und nur die zwei enthaltenen Dateien in `wp-content/plugins/affiliate-portal-template-kit/` an gleicher Stelle überschreiben. Danach live FAQ + PB-one-Link + Plugin-Version prüfen.**
