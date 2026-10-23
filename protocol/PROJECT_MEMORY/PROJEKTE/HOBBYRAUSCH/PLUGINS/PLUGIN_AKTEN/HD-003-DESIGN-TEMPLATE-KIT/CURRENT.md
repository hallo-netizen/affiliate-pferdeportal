# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **LIVE 1.50.711 / 1.50.713 LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Live

Aktiv und nach Nutzer-Readback funktionsfähig:
**1.50.711**.

1.50.710 ist verworfen.

## Lokaler Kandidat 1.50.713

Basis:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.712_FULL_SLIM30.zip`

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.713_FOOTER_4COL_KI_PBONE.zip`

SHA-256:
`c1f000448c9795f1a9bb7806d3191294a49c8b6fffde748b0e5b0707671ab66b`

Größe:
27,471,653 Bytes.

Footer:
- Logo entfernt;
- vier Spalten: Rechtliches / Wissen / Service / Anzeigenmarkt;
- Wissen = Hobbymagazin / FAQ / Glossar / Hobbyregister;
- Service = Werben im Hobby Depot / Preise / Kontakt;
- Links 14px, Überschriften 16.5px;
- Copyright mittig unter dem Footer;
- kleiner Hinweis `* mithilfe von KI erstellt`;
- `© [Jahr] Hobby Depot | PB one.`;
- PB one. → `https://p-b.one/`.

Lokale QA:
- kompletter PHP-Lint 10/10 PASS;
- nur zwei bestehende Runtime-Dateien gegenüber 1.50.712 geändert;
- keine Seitentemplates geändert;
- Footer Positiv-/Negativrender PASS;
- ZIP/Fresh-Unpack PASS.

Evidence:
`EVIDENCE_1.50.713.md`

## Installation

Der WordPress-ZIP-Uploadweg bleibt wegen HTTP 413 unbrauchbar.
Der Nutzer arbeitet deshalb über Cyberduck.

1.50.713 ist **nicht live**.

## EXAKT EINE NEXT ACTION

**1.50.713 lokal entpacken und den Ordner `affiliate-portal-template-kit` per Cyberduck über den bestehenden Serverordner `wp-content/plugins/affiliate-portal-template-kit/` kopieren/überschreiben. Danach ausschließlich Footer und Plugin-Version live prüfen.**
