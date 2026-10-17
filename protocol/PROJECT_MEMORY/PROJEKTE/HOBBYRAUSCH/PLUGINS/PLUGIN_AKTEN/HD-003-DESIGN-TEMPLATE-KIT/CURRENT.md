# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.50.674 RESPONSIVE/TEXT FAIL / 1.50.675 CENTRAL AUDIO-HERO FIX LOCAL HARD PASS / LIVE OFFEN**

## Fehler 1.50.674

- Fullbleed nur >1100 px;
- darunter alter 600-px-Bildpfad;
- rechter Leerraum bei bestimmten Breiten;
- Hero-Text links ohne ausreichenden Innenabstand;
- alte lange Hero-Zeile statt neuer Kurzzeile;
- Claim optisch noch alter Stand.

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.675_HOBBY_DEPOT_AUDIO_HIFI_RESPONSIVE_FULLBLEED_FIX_HARDPASS.zip`

SHA-256:
`aaf1bca2d7b7b55b91f9a15e22e847b67489ceca3faf3d6c1648a6779b636307`

## Korrektur

Zentrale CSS-Klasse `hd-hub2-hero-fullbleed`, aktuell nur Audio zugewiesen.

>=901:
- Fullbleed;
- Innenabstand;
- beige Verlaufsfläche;
- Claim/H1/Kurzzeile sauber.

<=900:
- gestapelt;
- Bild 100 % breit;
- kein 600-px-Limit.

Hero-Text fest:
`Klang verstehen, Technik entdecken und selbst bauen.`

Langtext unabhängig davon.

## Performance

- ein Bild;
- CSS-only;
- kein JS;
- kein Blur;
- kein Masking;
- keine zusätzliche Abfrage.

## QA

- PHP 73/73;
- Render-Harness PASS;
- Release-Kette sauber;
- 901/901 Assets identisch;
- 1440/1180/1024/901/900/800/760/600/390 px simuliert;
- 0 Overflow;
- Bild in allen Fällen volle Hero-Breite;
- ZIP PASS.

## EXAKT EINE NEXT ACTION

**1.50.675 installieren und Audio & HiFi breit + halbbreit prüfen.**
