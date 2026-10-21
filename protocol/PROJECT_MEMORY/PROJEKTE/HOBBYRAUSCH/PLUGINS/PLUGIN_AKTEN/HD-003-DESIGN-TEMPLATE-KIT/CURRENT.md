# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-21
STATUS: **1.50.709 HD-001 AUTOFOOTER ROOTFIX EXAKT REPRODUZIERT / LIVE OFFEN**

Plugin-ID:
HD-003-DESIGN-TEMPLATE-KIT

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.709_HD001_AUTOFOOTER_ROOTFIX_VERIFIED.zip`

SHA-256:
`32ed94f5e45b5ae59064b19208ca90d32a74a2e33a8f15c3007bebd7228bf6cb`

Größe:
58,829,084 Bytes.

## Bewiesene Ursache

- aktuelles HD-001 1.14.16 hängt `APKW_FrontendStructure::output_auto_footer` an `wp_footer` Priorität 50;
- dieser Renderer erzeugt `.apkw-auto-footer` mit weißem Hintergrund und oberer Linie;
- mit dem realen Hobby-Depot-V7.1-Profil entstehen exakt die sichtbaren Links `Zeit, Budget & Platz` und `Anbieter`;
- Glossar rendert zuerst den dunklen HD-003-Footer und danach `wp_footer()`, daher liegt der HD-001-Autofooter darunter;
- die frühere 1.50.708-Theme-Footer-Ursache war falsch.

## Rootfix 1.50.709

- Basis 1.50.707; falsche 1.50.708-Theme-Suppressoren nicht übernommen;
- `apkw_auto_footer_enabled` wird im Hobby-Depot-Designprofil mit Priorität 9999 auf `false` gesetzt;
- nur die automatische sichtbare HD-001-Footerausgabe wird abgeschaltet;
- HD-001 Daten/API/Shortcode bleiben erhalten;
- dunkler HD-003-Footer bleibt mit größerer Schrift, ohne Hobbyfinder und mit dynamischem Copyright;
- keine DB-/Kategorie-/SEO-/Finder-/Glossaränderung.

## Exakte kombinierte Simulation

- aktuelles HD-001 reproduziert vorher exakt weißen Autofooter + `Zeit, Budget & Platz` + `Anbieter`: PASS;
- nach 1.50.709 `.apkw-auto-footer` absent: PASS;
- beide weißen Links absent: PASS;
- dunkler Footer genau einmal: PASS;
- Copyright vorhanden: PASS;
- Glossar-Resolver wählt V150709: PASS;
- PHP 138/138 PASS;
- ZIP PASS.

## EXAKT EINE NEXT ACTION

**1.50.709 installieren und nur den echten Footer live prüfen.**
