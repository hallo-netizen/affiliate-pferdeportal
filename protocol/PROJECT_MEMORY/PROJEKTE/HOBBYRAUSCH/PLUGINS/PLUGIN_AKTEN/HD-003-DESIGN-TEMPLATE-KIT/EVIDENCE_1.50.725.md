# HD-003 – EVIDENCE 1.50.725 FOOTER LOGO FIX

STAND: 2026-10-23
STATUS: LOCAL HARD PASS / LIVE OFFEN

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.725_UPDATE_FOOTER_LOGO_FIX.zip`

SHA-256:
`4857b6e57d7a8b155e66e8f211843690f0db4066ced0e925740c06cef32575bf`

Größe:
767,585 Bytes.

## Ursache 1.50.724

Das Logoasset war im Paket vorhanden, der Runtime-Pfad war aber falsch doppelt verschachtelt:

`assets/hobby-depot-v150617/hobby-depot-v150617/logo-variant3-v150616.png`

Dadurch konnte das Bild live nicht geladen werden.

## Fix 1.50.725

Der Footer verweist jetzt korrekt auf:

`assets/hobby-depot-v150617/logo-variant3-v150616.png`

Die Markenleiste bleibt:
- kleines Hobby-Depot-Logo;
- Claim „Hobbys. Ideen. Möglichkeiten.“;
- darunter vier Footer-Spalten;
- separater KI-/Copyrightbereich.

QA:
- Asset physisch im UPDATE vorhanden PASS.
- erzeugter Runtime-Pfad entspricht dem physischen Assetpfad PASS.
- PHP-Lint PASS.
- Fresh-Unpack PASS.
- PB-one-Änderung erhalten.

Kein Live-PASS behaupten.
