# HD-003 – EVIDENCE 1.50.713

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / NICHT LIVE

Basis:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.712_FULL_SLIM30.zip`

Kandidat:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.713_FOOTER_4COL_KI_PBONE.zip`

SHA-256:
`c1f000448c9795f1a9bb7806d3191294a49c8b6fffde748b0e5b0707671ab66b`

Größe:
27,471,653 Bytes.

## Delta gegen 1.50.712

Exakt zwei bestehende Runtime-Dateien geändert:
- `pferde-template-kit.php` – nur Version 1.50.713;
- `includes/class-hobby-depot-profile-v150709.php` – Footer-Render/CSS + Release 1.50.713.

Keine Seitentemplates geändert.

## Footerziel

Desktop:
- kein Footer-Logo;
- vier gleichwertige Spalten: Rechtliches / Wissen / Service / Anzeigenmarkt;
- Wissen: Hobbymagazin / FAQ / Glossar / Hobbyregister;
- Service: Werben im Hobby Depot / Preise / Kontakt;
- Footerlinks 14px, Überschriften 16.5px;
- Copyright-/Hinweisbereich mittig unter dem Footer;
- Zeile 1 klein: `* mithilfe von KI erstellt`;
- Zeile 2: `© [Jahr] Hobby Depot | PB one.`;
- `PB one.` verlinkt exakt auf `https://p-b.one/`.

Responsive:
- Desktop 4 Spalten;
- Tablet 2 × 2;
- Mobil 1 Spalte.

## Tests

- PHP-Lint kompletter Pluginbestand: 10/10 PASS;
- PHP-Lint Fresh-Unpack: PASS;
- ZIP Fresh-Unpack: PASS;
- Runtime-Markierung 1.50.713: PASS;
- vier Footer-Überschriften: PASS;
- Reihenfolge Rechtliches → Wissen → Service → Anzeigenmarkt: PASS;
- Wissen-Links vollständig: PASS;
- Service-Links vollständig: PASS;
- alte Überschrift Informationen: NEGATIVTEST PASS (0);
- Footer-Logo im Render: NEGATIVTEST PASS (0);
- KI-Hinweis: PASS;
- PB-one-Link: exakt 1 Treffer PASS;
- Copyright-Unterbereich: PASS.

Keine Live-Installation oder Live-Abnahme in diesem Stand.
