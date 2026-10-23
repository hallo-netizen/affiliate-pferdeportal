# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **LIVE HD-003 1.50.711 / 1.50.713 LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Live

Aktuell live und zuletzt belastbar:
**HD-003 1.50.711**.

1.50.710 bleibt verworfen.

## Neuer lokaler Kandidat 1.50.713

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.713_FOOTER_4COL_KI_PBONE.zip`

SHA-256:
`c1f000448c9795f1a9bb7806d3191294a49c8b6fffde748b0e5b0707671ab66b`

Größe:
27,471,653 Bytes.

Footerziel umgesetzt:
- Hintergrund bleibt `#f5f1e9`;
- Footer-Logo entfernt;
- Desktop vier gleichwertige Spalten;
- Rechtliches;
- Wissen: Hobbymagazin / FAQ / Glossar / Hobbyregister;
- Service: Werben im Hobby Depot / Preise / Kontakt;
- Anzeigenmarkt;
- Linkschrift auf 14px verkleinert; Überschriften 16.5px;
- Copyrightbereich weiß und mittig unter dem Footer;
- oberhalb klein `* mithilfe von KI erstellt`;
- darunter `© [Jahr] Hobby Depot | PB one.`;
- `PB one.` verlinkt auf `https://p-b.one/`;
- Tablet 2 × 2, Mobil 1 Spalte.

## Lokale Prüfung

- Basis 1.50.712 Full Slim30;
- gegen Basis exakt zwei bestehende Runtime-Dateien geändert;
- aktive Seitentemplates unverändert;
- kompletter PHP-Lint: 10/10 PASS;
- Footer-Positivrender PASS;
- Negativtests: kein Logo, keine Überschrift Informationen, kein doppelter PB-one-Link;
- ZIP/Fresh-Unpack PASS.

Plugin-Evidence:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/EVIDENCE_1.50.713.md`

## Uploadweg

WordPress-ZIP-Upload großer HD-003-Pakete wurde mit HTTP 413 abgelehnt.
Der aktuelle Installationsweg ist deshalb Cyberduck/Serverordner.

Kein Live-PASS für 1.50.713 behaupten.

## EXAKT EINE NEXT ACTION

**1.50.713 lokal entpacken → den Ordner `affiliate-portal-template-kit` per Cyberduck nach `wp-content/plugins/` hochladen und den bestehenden gleichnamigen Ordner überschreiben → danach live nur Footer + Plugin-Version prüfen.**
