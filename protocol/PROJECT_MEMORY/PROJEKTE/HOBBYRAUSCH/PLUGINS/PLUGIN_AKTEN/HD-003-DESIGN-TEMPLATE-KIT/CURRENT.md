# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **MAGAZIN LIVE VOR 1.50.721 BEANSTANDET / 1.50.721 UPDATE LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Live-Hinweis

Der Nutzer hat den bisherigen Magazinstand live geprüft und zwei konkrete Fehler beanstandet:
- Werbeflächen waren nicht zwischen den 12 Themenkacheln angeordnet;
- auf den Magazin-Zielseiten fehlten die erwarteten Hero-Bilder.

1.50.718 bleibt verworfen.
1.50.720 ist durch 1.50.721 ersetzt.

## Lokaler Kandidat 1.50.721 – UPDATE

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.721_UPDATE_MAGAZIN_BANNER_ZIELSEITEN_FIX.zip`

SHA-256:
`c81f278aec7b4f80a57045269877f5df760d7e97cc4d2bace07e79e1320a93bd`

Größe:
2,103,461 Bytes.

Hauptordner unverändert:
`affiliate-portal-template-kit/`

### Magazin-Startseite
- 12 echte Editorial-Zielseiten bleiben unverändert;
- 6 Kacheln → Journal-Banner volle Breite → 3 Kacheln → direkte Werbefläche volle Breite → 3 Kacheln;
- keine Themenkachel wird für Werbung geopfert;
- Root-Beitragsbereich dupliziert den Journal-Banner nicht.

### Zielseiten
- Kachelbild und Hero greifen auf dieselbe Definition zu;
- alle 12 verwendeten Bilder werden im UPDATE physisch mitgeliefert;
- Brush-Asset wird mitgeliefert;
- Owned-Template plus Content-Fallback sichern die Ausgabe ab;
- Hero;
- grüne Schreibschrift/Brush;
- kurzer Hero-Text;
- grün hinterlegter Lead;
- nativer Aufklapper;
- vorhandene Magazin-Unteransichten/Beiträge und Monetarisierung bleiben erhalten.

### Paket
16 Dateien:
- 2 PHP;
- 1 Content-Template;
- 12 Magazinbilder;
- 1 Brush.

QA:
- PHP-Lint PASS;
- Fresh-Unpack PASS;
- 12/12 Bilder physisch vorhanden;
- exemplarischer Zielseiten-Render vollständig PASS;
- Bannerpositionen im Kachelfluss PASS.

Evidence:
`EVIDENCE_1.50.721.md`

## EXAKT EINE NEXT ACTION

**1.50.721 entpacken und den Ordner `affiliate-portal-template-kit` per Cyberduck auf `wp-content/plugins/` ziehen/zusammenführen. Danach Magazin-Startseite sowie eine Zielseite live prüfen.**
