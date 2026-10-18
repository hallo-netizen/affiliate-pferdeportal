# HD-003 – HOBBY DEPOT DESIGN / TEMPLATE KIT – CURRENT

<!-- CAMPUS_CURRENT_AUTHORITY_V1 -->

STAND: 2026-10-17
STATUS: **LIVE 1.50.674 / 1.50.675 CODE PASS / ERSTE ZIP NICHT ÜBERINSTALLIERBAR / KORREKTE REPACK-ZIP PASS / LIVE OFFEN**

## Fehler 1.50.674

- Fullbleed nur >1100 px;
- darunter alter 600-px-Bildpfad;
- rechter Leerraum bei bestimmten Breiten;
- Hero-Text links ohne ausreichenden Innenabstand;
- alte lange Hero-Zeile statt neuer Kurzzeile;
- Claim optisch noch alter Stand.

## Kandidat

`AFFILIATE_PORTAL_TEMPLATE_KIT_1.50.675_HOBBY_DEPOT_AUDIO_HIFI_RESPONSIVE_FULLBLEED_FIX_REPACKED_HARDPASS.zip`

SHA-256:
`356a8e9861f0c018e42620d311eb9985f48279b3a5d1ed26be321c63ddfa24bd`

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

- erster 1.50.675-Installer verworfen: Plugin-Wurzelordner fehlte;
- Repack: Top-Level `affiliate-portal-template-kit/` wie 1.50.674;
- Main-Datei: `affiliate-portal-template-kit/pferde-template-kit.php`;
- 1041/1041 Innendateien byte-identisch;
- ZIP-Test ohne Fehler;
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
