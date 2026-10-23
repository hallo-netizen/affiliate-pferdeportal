# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **MAGAZIN LIVE VOR 1.50.721 BEANSTANDET / HD-003 1.50.721 LOKAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Letzter Live-Readback

Beanstandet:
- Werbeflächen nicht in den Themenkachelfluss integriert;
- fehlende Hero-Bilder auf den Magazin-Zielseiten.

Diese beiden Punkte sind Ziel von 1.50.721.

## Neuer Kandidat 1.50.721

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.721_UPDATE_MAGAZIN_BANNER_ZIELSEITEN_FIX.zip`

SHA-256:
`c81f278aec7b4f80a57045269877f5df760d7e97cc4d2bace07e79e1320a93bd`

Größe:
2,103,461 Bytes.

### Magazin-Startseite

Werbelogik fest:
- keine Themenkachel wird ersetzt;
- nach 6 Kacheln ein durchgehender `journal_banner`;
- nach weiteren 3 Kacheln eine durchgehende direkte Werbefläche;
- danach die letzten 3 Kacheln;
- auf Mobil ebenfalls volle Rasterbreite.

### Magazin-Zielseiten

Verbindlich:
- Hero-Bild ist dasselbe Asset wie das Kachelbild;
- alle 12 Assets werden mit 1.50.721 physisch mitgeliefert;
- gleicher bestehender Hub2-Hero-Aufbau;
- grüne Schreibschrift + Brush/Bogen;
- kurzer Hero-Text;
- darunter grüne Lead-Box;
- Resttext per nativer Aufklappfunktion;
- Inhalte nach dem bestehenden 150–200-Wort-Kategorietextvertrag.

Zusätzliche Absicherung:
- bestehendes Owned-Content-Template liegt im UPDATE;
- Content-Fallback für Magazinroot/-zielseiten;
- Legacy-CSS darf Zielseiten-Hero-Medien nicht ausblenden.

### QA

- PHP-Lint PASS;
- Fresh-Unpack PASS;
- 12/12 Bilder vorhanden;
- 12/12 Definitionen gebunden;
- exemplarischer Zielseiten-Hero inklusive identischem Asset, Brush, Lead und Details PASS;
- Werbeflächenpositionen im 12er-Kachelfluss PASS.

Plugin-Evidence:
`../PLUGINS/PLUGIN_AKTEN/HD-003-DESIGN-TEMPLATE-KIT/EVIDENCE_1.50.721.md`

## EXAKT EINE NEXT ACTION

**1.50.721 per Cyberduck einspielen und danach Magazin-Hub sowie eine Magazin-Zielseite live abnehmen.**
