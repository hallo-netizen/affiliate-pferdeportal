# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-23
STATUS: **1.50.725 FOOTER-LOGO-FIX LOCAL HARD PASS / CYBERDUCK-INSTALLATION OFFEN**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Kandidat 1.50.725

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.725_UPDATE_FOOTER_LOGO_FIX.zip`

SHA-256:
`4857b6e57d7a8b155e66e8f211843690f0db4066ced0e925740c06cef32575bf`

Größe:
767,585 Bytes.

UPDATE, kein Full-Plugin.

Hauptordner:
`affiliate-portal-template-kit/`

## Ursache des fehlenden Logos

1.50.724 lieferte das Logoasset zwar mit, erzeugte aber einen doppelt verschachtelten, nicht existierenden Assetpfad.

## Fix

Runtime-Pfad und physischer Pfad sind jetzt identisch:
`assets/hobby-depot-v150617/logo-variant3-v150616.png`

Markenleiste:
- Hobby-Depot-Logo;
- Claim „Hobbys. Ideen. Möglichkeiten.“;
- vier Footer-Spalten darunter;
- KI-/Copyrightbereich separat.

QA:
- Asset physisch vorhanden PASS;
- Pfadbindung PASS;
- PHP-Lint PASS;
- Fresh-Unpack PASS.

Evidence:
`EVIDENCE_1.50.725.md`

## EXAKT EINE NEXT ACTION

**1.50.725 per Cyberduck über `wp-content/plugins/affiliate-portal-template-kit/` zusammenführen und Footer live prüfen.**
