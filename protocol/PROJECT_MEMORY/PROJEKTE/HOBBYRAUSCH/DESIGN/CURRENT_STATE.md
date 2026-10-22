# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-22
STATUS: **LIVE 1.50.711 / 1.50.712 LOKAL GEPRÜFT / WORDPRESS-UPLOAD DURCH HTTP 413 BLOCKIERT**

Zielvertrag:
**ZV-HOBBYRAUSCH-DESIGN-001 Fassung 5.5 / 2026-10-19**

## Aktueller belastbarer Stand

Live installiert und nach der Reparatur wieder funktionsfähig:
**HD-003 1.50.711**.

1.50.710 war fehlerhaft:
- Runtime-/Templatepfad auf nicht vorhandene V150710-Dateien umgestellt;
- dadurch Seite im Livebetrieb sichtbar beschädigt;
- 1.50.710 ist verworfen.

1.50.711 wurde direkt aus dem funktionierenden 1.50.709-Stand gebaut:
- keine neue Runtime;
- keine neuen Seitentemplates;
- Footer-only-Reparatur;
- Seite danach live wieder intakt.

## 1.50.712 – lokaler Kandidat

Ziel:
- Footer-Hintergrund = vorhandene Headerfarbe `#f5f1e9`;
- Footer verwendet dieselbe Logo-Komponente wie der Header;
- Copyright außerhalb/unterhalb des Footers;
- keine unerwünschten Zusatzlinks.

Vollartefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.712_FOOTER_EXACT_HEADER_LOGO_LIGHTBG_COPYRIGHT_BELOW.zip`
SHA-256:
`be9f6d59f86c5c2f8d0983bdf8013c866c468a7489a1b70037a9deed3dc6eec1`
Größe:
58,829,246 Bytes.

Abgespeckte vollständige 1.50.712:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.712_FULL_SLIM30.zip`
SHA-256:
`f1986b60c6628b2e43b6cade32f9ccbd4fe3664bdc8df34a06842f64c68b97e9`
Größe:
27,463,064 Bytes.

Lokale Prüfung der 1.50.712:
- gegen 1.50.711 nur Footer-/Versionsdelta;
- aktive Seitentemplates unverändert;
- PHP-Lint PASS;
- unerwünschte Footerlinks im Negativtest 0 Treffer;
- Desktop/Tablet/Mobil lokal gerendert;
- ZIP/Fresh-Unpack PASS.

## Live-/Upload-Grenze

WordPress zeigt 128 MB Medien-Uploadlimit.

Trotzdem:
- 49,6-MB-Voll-Slim-Paket: HTTP 413;
- 27,46-MB-FULL-SLIM30: HTTP 413;
- 561-KB-Test-Updater ließ sich hochladen, wurde vom Nutzer ausdrücklich **nicht installiert**.

Damit ist 1.50.712 **nicht live**.
Kein Live-PASS behaupten.

## ERSTER OFFENER BLOCKER

**Der normale WordPress-Plugin-Upload großer HD-003-Pakete wird aktuell durch HTTP 413 blockiert.**

## EXAKT EINE NEXT ACTION

**1.50.712 als vollständiges Plugin über einen funktionierenden Uploadweg/Serverweg installieren und danach ausschließlich den Footer live prüfen.**
