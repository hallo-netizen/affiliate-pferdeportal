# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **LIVE HD-003 1.50.711 / 1.50.715 DELTA LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Live

Aktuell live und zuletzt belastbar:
**HD-003 1.50.711**.

## Lokaler Kandidat 1.50.715

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.715_DELTA_FAQ_PBONE.zip`

SHA-256:
`2c6594ee4fae4d37cc9fa43a6e5183e190bcb86ae13db29c924346d73a2ae33a`

Größe:
574,666 Bytes.

Das Delta enthält nur zwei Dateien und führt die Footeränderungen fort.

### Footer
- Logo bleibt entfernt;
- vier Spalten Rechtliches / Wissen / Service / Anzeigenmarkt;
- kleinere Linkschrift;
- Copyright mittig unter dem Footer;
- `* mithilfe von KI erstellt`;
- `© [Jahr] Hobby Depot | PB one.`;
- PB one öffnet jetzt in neuem Fenster.

### FAQ
Die bereits vorhandene WordPress-Seite `/faq/` war leer und wird jetzt gezielt durch HD-003 gefüllt:
- 6 Themenbereiche;
- 30 kurze Fragen und Antworten;
- direkte Du-Ansprache;
- einzelne Fragen nativ aufklappbar;
- kein JavaScript und kein Zusatzplugin;
- responsive Gestaltung;
- FAQ-Meta-Description-Fallback.

## Lokale Prüfung

- ZIP exakt 2 Dateien;
- PHP-Lint PASS;
- Fresh-Unpack PASS;
- FAQ-Render 6 Bereiche / 30 Fragen PASS;
- PB-one-Link neues Fenster PASS.

Plugin-Evidence:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/EVIDENCE_1.50.715.md`

Kein Live-PASS für 1.50.715 behaupten.

## EXAKT EINE NEXT ACTION

**1.50.715-Delta lokal entpacken und die zwei Dateien per Cyberduck im bestehenden Pluginordner überschreiben. Danach live FAQ, PB-one-Link und Plugin-Version prüfen.**
