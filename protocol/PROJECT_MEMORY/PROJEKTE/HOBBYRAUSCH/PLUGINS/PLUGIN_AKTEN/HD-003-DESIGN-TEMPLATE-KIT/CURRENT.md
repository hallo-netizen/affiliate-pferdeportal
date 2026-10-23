# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.50.727 MAGAZIN + FOOTER NAV FINAL LOCAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Kandidat 1.50.727

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.727_UPDATE_MAGAZIN_FOOTER_NAV_FINAL.zip`

SHA-256:
`71cc28631c8f0ecc77197a5cb4597b7eb8b202629f4cec8e7623a785767a51ff`

Größe:
768,293 Bytes.

Hauptordner:
`affiliate-portal-template-kit/`

## Magazin

Die Magazin-Startseite ist sichtbarer Überbau für Orientierung/Wissen.

Eigene Dreierzeile:
- Hobbyfinder;
- Hobbyregister;
- Glossar.

Die redaktionellen Magazin-Themen bleiben separat darunter.

## Footer

Markenleiste:
- Hobby-Depot-Logo;
- kleine Unterzeile des Logoassets im Footer ausgeblendet;
- kein zusätzlicher Claimtext.

Spalten:
- Rechtliches: bestehende 4 Einträge;
- Wissen: Hobbymagazin · Hobbyfinder · Hobbyregister · Glossar;
- Service: Werben im Hobby Depot · Preise · Kontakt · FAQ;
- Anzeigenmarkt: bestehende 4 Einträge.

Hobbyfinder ist damit im Footer vorhanden.
FAQ liegt nicht mehr unter Wissen.

## QA

- PHP-Lint PASS;
- Fresh-Unpack PASS;
- Wissen exakt 4 Einträge PASS;
- Service exakt 4 Einträge PASS;
- Magazin-Dreierzeile PASS;
- Footer-Logo-Crop PASS;
- PB-one-Verhalten erhalten.

Evidence:
`EVIDENCE_1.50.727.md`

## EXAKT EINE NEXT ACTION

**Gemeinsames Bundle `HOBBY_DEPOT_AKTUELL_20261023_MAGAZIN_FOOTER_REGISTER_FINAL.zip` entpacken und die beiden vorhandenen Pluginordner per Cyberduck unter `wp-content/plugins/` zusammenführen. Danach Magazin-Startseite, Footer und eine Hobbyregister-Detailseite live prüfen.**
