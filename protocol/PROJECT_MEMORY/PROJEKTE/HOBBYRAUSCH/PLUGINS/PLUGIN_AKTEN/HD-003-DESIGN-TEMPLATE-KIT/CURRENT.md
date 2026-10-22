# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-22
STATUS: **1.50.712 FOOTER NUR AUF 711-BASIS / EXAKT GEPRÜFT / LIVE-READBACK OFFEN**

Plugin-ID:
HD-003-DESIGN-TEMPLATE-KIT

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.712_FOOTER_EXACT_HEADER_LOGO_LIGHTBG_COPYRIGHT_BELOW.zip`

SHA-256:
`be9f6d59f86c5c2f8d0983bdf8013c866c468a7489a1b70037a9deed3dc6eec1`

Größe:
58,829,246 Bytes.

## Basis

Direkte Basis ist der wieder funktionierende Stand 1.50.711.

Gegen 1.50.711 sind exakt zwei Dateien geändert:
- `pferde-template-kit.php` – nur Versionsnummer;
- `includes/class-hobby-depot-profile-v150709.php` – nur Footer-Render/CSS + Release.

Die beiden aktiven Seitentemplates bleiben bytegleich:
- `templates/hobby-depot-front-v150709.php`
- `templates/hobby-depot-content-v150709.php`

Keine Router-/Template-/Seitenlogikänderung.

## Footer 1.50.712

- Hintergrund: vorhandene Headerfarbe `#f5f1e9`;
- Logo: dieselbe Header-Komponente, keine separate Rohbild-Darstellung;
- Desktop: 220×146 Komponentengeometrie;
- Tablet: 194×132;
- Mobil: 196 px Vollbilddarstellung wie Header mobil;
- Rechtliches / Informationen / Anzeigenmarkt bleiben;
- Hobbyfinder, Zeit/Budget/Platz und Anbieter-Zusatz bleiben ausgeschlossen;
- Copyright wird nach `</footer>` in einer separaten weißen Zeile ausgegeben;
- HD-001-Autofooter bleibt deaktiviert.

## Tests

- PHP-Lint 138/138 PASS;
- Diff gegen 711 exakt 2 Dateien;
- aktive Front-/Content-Templates bytegleich zu 711;
- negativer Footer-Render mit absichtlich eingeschleusten Hobbyfinder/Budget/Anbieter-Einträgen: alle 0 Treffer;
- Desktop 1440: Footer #f5f1e9, Logo 220×146, Copyright unter Footer;
- Tablet 900: Logo 194×132;
- Mobil 390: Logo 196 px, Copyright unter Footer;
- ZIP CRC PASS;
- Fresh-Unpack PASS.

## EXAKT EINE NEXT ACTION

**1.50.712 installieren und ausschließlich den Footer live prüfen.**
