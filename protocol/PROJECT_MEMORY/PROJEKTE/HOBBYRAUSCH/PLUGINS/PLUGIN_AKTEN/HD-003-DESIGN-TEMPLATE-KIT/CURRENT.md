# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-21
STATUS: **1.50.708 FOOTER THEME-BINDING ROOTFIX LOCAL HARD PASS / LIVE OFFEN**

Plugin-ID:
HD-003-DESIGN-TEMPLATE-KIT

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.708_FOOTER_THEME_BINDING_ROOTFIX_HARDPASS.zip`

SHA-256:
`b5aa47c48a3e37b3c75bb2af0e1093cf89016f9d1a8d893294bd32657a28c09c`

Größe:
58,830,312 Bytes.

## Ursache

Im Hobby-Depot-Büro wurde der doppelte Footerpfad gefunden:
- Footer-Umzug 1.1.1 setzt Footer-Menülokationen und Footer-Widgetbindungen im Theme;
- HD-003 rendert zusätzlich den eigenen dunklen Footer;
- dadurch kann unter dem dunklen Footer der native Theme-Footer als helle Zusatzleiste erscheinen.

## Rootfix 1.50.708

- native Theme-Footer-Menülokationen im Frontend unterdrückt;
- native Footer-Widget-Sidebars im Frontend geleert;
- Footer-`wp_nav_menu` fail-safe unterdrückt;
- keine DB-Writes;
- importierte Seiten und Menüs bleiben erhalten;
- dunkler HD-003-Footer bleibt alleiniger sichtbarer Footer und liest seine Menüs direkt;
- Finder, Glossar, Kategorie-/Affiliate-/SEO-Logik unverändert.

## QA

- PHP 138/138 PASS;
- Menülocation-Rootfix PASS;
- Widget-Rootfix PASS;
- Footer-`wp_nav_menu` PASS;
- normale Menüs unverändert PASS;
- ZIP PASS.

## EXAKT EINE NEXT ACTION

**1.50.708 über aktive 1.50.706 installieren und Footer live prüfen.**
