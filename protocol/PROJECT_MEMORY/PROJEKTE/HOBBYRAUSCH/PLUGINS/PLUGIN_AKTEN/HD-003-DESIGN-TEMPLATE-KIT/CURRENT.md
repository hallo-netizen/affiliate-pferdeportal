# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-22
STATUS: **LIVE 1.50.711 / 1.50.712 LOKAL GEPRÜFT / HTTP-413-UPLOADBLOCKER**

Plugin-ID:
`HD-003-DESIGN-TEMPLATE-KIT`

Fach-Current:
`../../../DESIGN/CURRENT_STATE.md`

## Live

Aktiv und nach Nutzer-Readback funktionsfähig:
**1.50.711**.

1.50.710 ist verworfen, weil ein falscher V150710-Runtime-/Templatepfad die Seite live beschädigt hat.

## Lokaler Kandidat 1.50.712

Vollartefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.712_FOOTER_EXACT_HEADER_LOGO_LIGHTBG_COPYRIGHT_BELOW.zip`
SHA-256:
`be9f6d59f86c5c2f8d0983bdf8013c866c468a7489a1b70037a9deed3dc6eec1`

Vollständige komprimierte Ausgabe:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.712_FULL_SLIM30.zip`
SHA-256:
`f1986b60c6628b2e43b6cade32f9ccbd4fe3664bdc8df34a06842f64c68b97e9`
Größe:
27,463,064 Bytes.

Footerziel:
- Hintergrund `#f5f1e9`;
- Header-Logo-Komponente im Footer;
- Copyright unterhalb des Footers;
- Hobbyfinder / Zeit-Budget-Platz / zusätzlicher Anbieter nicht im Footer.

Lokale QA:
- PHP-Lint PASS;
- aktive Seitentemplates gegenüber 1.50.711 unverändert;
- Footer Positiv-/Negativrender PASS;
- ZIP/Fresh-Unpack PASS.

## Upload-/Livegrenze

- 27,46 MB werden im WordPress-Plugin-Upload mit HTTP 413 abgelehnt;
- WordPress-Medienseite zeigt 128 MB;
- kleiner 561-KB-Test-Updater ließ sich hochladen, wurde nicht installiert.

1.50.712 ist daher **nicht live**.

## ERSTER OFFENER BLOCKER

**HTTP 413 verhindert derzeit die reguläre Installation des vollständigen 1.50.712-Pakets über WordPress.**

## EXAKT EINE NEXT ACTION

**Vollständige 1.50.712 über einen funktionierenden Upload-/Serverweg installieren und danach Footer live abnehmen.**
