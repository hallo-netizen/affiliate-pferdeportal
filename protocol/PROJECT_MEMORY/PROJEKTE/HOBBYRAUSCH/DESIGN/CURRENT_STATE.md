# HOBBYRAUSCH – DESIGN – CURRENT_STATE

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-18
STATUS: **LIVE 1.50.675 / AUDIO-CLAIM-ABSTAND + UNTERSTRICH LIVE FAIL / 1.50.676 LOCAL HARD PASS / LIVE OFFEN**

## Reales Live-Ergebnis 1.50.675

Vom Nutzer im Frontend bestätigt:
- Fullbleed-Hero und Responsive-Grundlogik funktionieren;
- aber Claim sitzt zu dicht an der H1;
- Claim soll höher;
- Pinselunterstrich ist deutlich zu lang.

Exakte Ursache:
- Claim ist Flex-Kind und wurde quer gestreckt;
- dadurch bekam der Pinselunterstrich die Breite des gestreckten Claim-Elements statt der realen Claim-Textbreite.

## 1.50.676 – nur Audio-&-HiFi-Claim-Mikrofix

Keine Bildänderung, keine andere Kategorie.

Korrektur:
- Claim wird nicht mehr gestreckt: `align-self:flex-start` + `width:max-content`;
- Unterstrich folgt damit der echten Claimbreite;
- Unterstrich zusätzlich auf 74 % der Claimbreite begrenzt;
- Claim Desktop 12 px nach oben;
- Abstand Claim -> H1 vergrößert;
- Mobil entsprechend 6 px nach oben und eigener Abstand;
- H1, Hero-Kurzsatz, Bild, Langtext und Responsive-Grundlogik unverändert.

## QA

Artefakt:
`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.676_HOBBY_DEPOT_AUDIO_CLAIM_SPACING_UNDERLINE_FIX_HARDPASS.zip`

SHA-256:
`7c898eaeac166e21e47ecfa946baa4ff217f462e5145a9485ec272647186ca82`

PASS:
- PHP 75/75;
- aktive 1.50.676-Release-Kette konsistent;
- keine aktive 1.50.675-Stale-Referenz;
- Hero-Kurztext weiterhin korrekt;
- Claim weiterhin `Klang, der begeistert.`;
- 901/901 Assets byte-identisch zu 1.50.675;
- ZIP-Wurzel exakt `affiliate-portal-template-kit/`;
- Main-Datei und Pluginversion korrekt;
- ZIP-Test PASS.

## EXAKT EINE NEXT ACTION

**1.50.676 über 1.50.675 installieren und nur Claim-Abstand + Unterstrich auf Audio & HiFi prüfen.**
